from flask import Flask, jsonify, request, redirect, send_from_directory
from flask_cors import CORS
import datetime
import requests
from dotenv import load_dotenv
import os
import hmac
import hashlib
import json
from urllib.parse import urlencode
from shopify import Session, ShopifyResource
import shopify

# Initialize Flask app
app = Flask(__name__)
# ✅ Add this near the bottom of the file:
@app.route('/widget.js')
def serve_widget():
    return send_from_directory('static', 'widget.js')
# Configure CORS
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization", "X-Shop-Domain"],
        "supports_credentials": True,
        "expose_headers": ["Content-Type"]
    }
})

# Load environment variables
load_dotenv()

# Configuration
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4")
SHOPIFY_API_KEY = os.getenv("SHOPIFY_API_KEY")
SHOPIFY_API_SECRET = os.getenv("SHOPIFY_API_SECRET")
SHOPIFY_API_VERSION = os.getenv("SHOPIFY_API_VERSION", "2023-07")
APP_URL = os.getenv("APP_URL")

# Database simulation
shops_db = {}  # {shop_domain: {access_token: str, chat_history: list}}
products_db = {}  # {shop_domain: [product1, product2...]}

# Helper Functions
# def verify_shopify_hmac(hmac_param, query_params):
#     """Verify Shopify HMAC signature"""
#     params = query_params.copy()
#     params.pop('hmac', None)
#     sorted_params = '&'.join([f"{k}={v}" for k, v in sorted(params.items())])
    
#     digest = hmac.new(
#         SHOPIFY_API_SECRET.encode('utf-8'),
#         sorted_params.encode('utf-8'),
#         hashlib.sha256
#     ).hexdigest()
    
#     return hmac.compare_digest(digest, hmac_param)

def validate_hmac(query_params):
    """Validate Shopify HMAC signature"""
    hmac_param = query_params.get('hmac')
    if not hmac_param or not SHOPIFY_API_SECRET:
        return False
    
    # Remove hmac and sort remaining parameters
    params = query_params.copy()
    params.pop('hmac', None)
    sorted_params = urlencode(sorted(params.items()))
    
    # Calculate HMAC
    digest = hmac.new(
        SHOPIFY_API_SECRET.encode('utf-8'),
        sorted_params.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(digest, hmac_param)

def get_shopify_context(shop_domain):
    """Get Shopify store context"""
    if shop_domain not in shops_db:
        return None
    
    session = Session(shop_domain, SHOPIFY_API_VERSION)
    session.token = shops_db[shop_domain]['access_token']
    shopify.ShopifyResource.activate_session(session)
    
    try:
        shop = shopify.Shop.current()
        products = shopify.Product.find(limit=5)
        return {
            "shop_name": shop.name,
            "products": [p.to_dict() for p in products],
            "currency": shop.currency
        }
    except Exception as e:
        print(f"Error getting Shopify context: {e}")
        return None
    finally:
        shopify.ShopifyResource.clear_session()

# Routes
@app.route('/')
def root():
    """Root endpoint with Shopify OAuth handling"""
    shop = request.args.get('shop')
    hmac_param = request.args.get('hmac')
    
    # Case 1: Shopify OAuth flow
    if shop and hmac_param:
        if verify_shopify_hmac(hmac_param, request.args):
            return redirect(f'/install?{urlencode(request.args)}')
        return "Invalid HMAC signature", 400
    
    # Case 2: Direct access
    return """
    <h1>Welcome to Shopify AI Chatbot</h1>
    <p>Install this app via your Shopify Admin</p>
    <p>Or access via: <a href="/api/messages">Chat API</a></p>
    """

# @app.route('/api/shopify/install', methods=['GET'])
# def shopify_install():
#     """Initiate Shopify app installation"""
#     shop_url = request.args.get('shop')
#     if not shop_url:
#         return jsonify({"error": "Shop parameter missing"}), 400
    
#     session = Session(shop_url, SHOPIFY_API_VERSION)
#     scope = ['read_products', 'write_products', 'read_orders']
#     redirect_uri = f"{APP_URL}/api/shopify/auth/callback"
#     permission_url = session.create_permission_url(scope, redirect_uri)
    
#     return redirect(permission_url)

@app.route('/install')
def install():
    shop = request.args.get('shop')
    if not shop:
        return "Shop parameter missing", 400
    
    scopes = 'write_script_tags,read_products'
    redirect_uri = f"{APP_URL}/auth/callback"  # Fixed syntax
    install_url = f"https://{shop}/admin/oauth/authorize?client_id={SHOPIFY_API_KEY}&scope={scopes}&redirect_uri={redirect_uri}"
    return redirect(install_url)



# @app.route('/api/shopify/auth/callback')
# def auth_callback():
#     shop = request.args.get('shop')
#     code = request.args.get('code')
#     hmac_param = request.args.get('hmac')
    
#     if not all([shop, code, hmac_param]):
#         return jsonify({"error": "Missing required parameters"}), 400
    
#     if not validate_hmac(request.args):
#         return jsonify({"error": "Invalid HMAC"}), 403
    
#     try:
#         # Existing token retrieval logic...
#         token_url = f"https://{shop}/admin/oauth/access_token"
#         token_response = requests.post(token_url, json={
#             'client_id': SHOPIFY_API_KEY,
#             'client_secret': SHOPIFY_API_SECRET,
#             'code': code
#         })
#         token_response.raise_for_status()
#         access_token = token_response.json()['access_token']

#         # Add or update script tag
#         embed_url = f"https://{shop}/admin/api/2024-01/script_tags.json"
#         script_tag_response = requests.get(embed_url, headers={"X-Shopify-Access-Token": access_token})
#         if script_tag_response.status_code == 200 and not any(tag["src"] == f"https://chatbot-bpy.clustersofttech.com/widget.js" for tag in script_tag_response.json().get("script_tags", [])):
#             requests.post(embed_url, json={
#                 "script_tag": {
#                     "src": f"https://chatbot-bpy.clustersofttech.com/widget.js",
#                     "event": "onload"
#                 }
#             }, headers={"X-Shopify-Access-Token": access_token})

#         return redirect(f"https://{shop}/admin/apps/{SHOPIFY_API_KEY}")
    
#     except requests.exceptions.RequestException as e:
#         error_data = e.response.json() if hasattr(e, 'response') and e.response else {'error': str(e)}
#         return jsonify({"error": "Installation failed", "details": error_data}), 500
@app.route('/auth/callback')
def auth_callback():
    shop = request.args.get('shop')
    code = request.args.get('code')
    hmac_param = request.args.get('hmac')
    
    # Validate required parameters
    if not all([shop, code, hmac_param]):
        return jsonify({"error": "Missing required parameters"}), 400
    
    # Validate HMAC
    if not validate_hmac(request.args):
        return jsonify({"error": "Invalid HMAC"}), 403
    
    try:
        # 1. Get access token
        token_url = f"https://{shop}/admin/oauth/access_token"
        token_response = requests.post(token_url, json={
            'client_id': SHOPIFY_API_KEY,
            'client_secret': SHOPIFY_API_SECRET,
            'code': code
        })
        token_response.raise_for_status()
        access_token = token_response.json()['access_token']
 
        # 2. Embed app in Shopify admin
        embed_url = f"https://{shop}/admin/api/2024-01/script_tags.json"
        requests.post(embed_url, json={
    "script_tag": {
        "src": f"https://chatbot-bpy.clustersofttech.com/widget.js",
        "event": "onload"
    }
}, headers={
    "X-Shopify-Access-Token": access_token
})
        # embed_url = f"https://{shop}/admin/api/2024-01/script_tags.json"
        # requests.post(embed_url, json={
        #     "script_tag": {
        #         "src": f"https://chatbot-py-two.vercel.app/",
        #         "event": "onload"
        #     }
        # }, headers={
        #     "X-Shopify-Access-Token": access_token
        # })
 
        # 3. Redirect to app in admin
        return redirect(f"https://{shop}/admin/apps/{SHOPIFY_API_KEY}")
    
    except requests.exceptions.RequestException as e:
        error_data = e.response.json() if hasattr(e, 'response') and e.response else {'error': str(e)}
        print(f"OAuth Error: {error_data}")
        return jsonify({
            "error": "Installation failed",
            "details": error_data
        }), 500
chat_history = [
    {
        "sender": "bot",
        "text": "Hello! How can I help you today?",
        "time": datetime.datetime.now().strftime("%I:%M %p, %d %b %Y")
    }
]
@app.route('/api/messages', methods=['GET'])
def get_messages():
    return jsonify(chat_history)

@app.route('/api/messages', methods=['POST'])
def send_message():
    data = request.get_json()
    user_message = {
        "sender": "user",
        "text": data['text'],
        "time": datetime.datetime.now().strftime("%I:%M %p, %d %b %Y")
    }
    chat_history.append(user_message)

    # Call Azure OpenAI API for bot response
    try:
        headers = {
            "Content-Type": "application/json",
            "api-key": AZURE_OPENAI_API_KEY
        }
        payload = {
            "messages": [
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": data['text']}
            ],
            "max_tokens": 150
        }
        response = requests.post(
            f"{AZURE_OPENAI_ENDPOINT}/openai/deployments/{AZURE_OPENAI_DEPLOYMENT}/chat/completions?api-version=2023-05-15",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        bot_text = response.json()["choices"][0]["message"]["content"].strip()

        bot_response = {
            "sender": "bot",
            "text": bot_text,
            "time": datetime.datetime.now().strftime("%I:%M %p, %d %b %Y")
        }
        chat_history.append(bot_response)
        return jsonify({"status": "success", "message": bot_response})
    except requests.exceptions.RequestException as e:
        print(f"Error calling Azure OpenAI API: {e}")
        bot_response = {
            "sender": "bot",
            "text": "Sorry, I couldn't process your request. Please try again.",
            "time": datetime.datetime.now().strftime("%I:%M %p, %d %b %Y")
        }
        chat_history.append(bot_response)
        return jsonify({"status": "error", "message": bot_response}), 500
    
@app.route('/api/messages/clear', methods=['POST'])
def clear_messages():
    global chat_history
    chat_history = [
        {
            "sender": "bot",
            "text": "Hello! How can I help you today?",
            "time": datetime.datetime.now().strftime("%I:%M %p, %d %b %Y")
        }
    ]
    return jsonify({"status": "success", "message": "Chat history cleared"})

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))  # Use Render's assigned port
    app.run(host='0.0.0.0', port=port, debug=True)



# from flask import Flask, jsonify, request
# from flask_cors import CORS
# import datetime
# import requests
# from dotenv import load_dotenv
# import os

# app = Flask(__name__)
# CORS(app)  # Enable CORS for React frontend

# # Load environment variables
# load_dotenv()

# AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
# AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
# AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")

# # In-memory chat history (replace with a database for production)
# chat_history = [
#     {
#         "sender": "bot",
#         "text": "Hello! How can I help you today?",
#         "time": datetime.datetime.now().strftime("%I:%M %p, %d %b %Y")
#     }
# ]

# @app.route('/api/messages', methods=['GET'])
# def get_messages():
#     return jsonify(chat_history)

# @app.route('/api/messages', methods=['POST'])
# def send_message():
#     data = request.get_json()
#     user_message = {
#         "sender": "user",
#         "text": data['text'],
#         "time": datetime.datetime.now().strftime("%I:%M %p, %d %b %Y")
#     }
#     chat_history.append(user_message)

#     # Call Azure OpenAI API for bot response
#     try:
#         headers = {
#             "Content-Type": "application/json",
#             "api-key": AZURE_OPENAI_API_KEY
#         }
#         payload = {
#             "messages": [
#                 {"role": "system", "content": "You are a helpful AI assistant."},
#                 {"role": "user", "content": data['text']}
#             ],
#             "max_tokens": 150
#         }
#         response = requests.post(
#             f"{AZURE_OPENAI_ENDPOINT}/openai/deployments/{AZURE_OPENAI_DEPLOYMENT}/chat/completions?api-version=2023-05-15",
#             headers=headers,
#             json=payload
#         )
#         response.raise_for_status()
#         bot_text = response.json()["choices"][0]["message"]["content"].strip()

#         bot_response = {
#             "sender": "bot",
#             "text": bot_text,
#             "time": datetime.datetime.now().strftime("%I:%M %p, %d %b %Y")
#         }
#         chat_history.append(bot_response)
#         return jsonify({"status": "success", "message": bot_response})
#     except requests.exceptions.RequestException as e:
#         print(f"Error calling Azure OpenAI API: {e}")
#         bot_response = {
#             "sender": "bot",
#             "text": "Sorry, I couldn't process your request. Please try again.",
#             "time": datetime.datetime.now().strftime("%I:%M %p, %d %b %Y")
#         }
#         chat_history.append(bot_response)
#         return jsonify({"status": "error", "message": bot_response}), 500

# @app.route('/api/messages/clear', methods=['POST'])
# def clear_messages():
#     global chat_history
#     chat_history = [
#         {
#             "sender": "bot",
#             "text": "Hello! How can I help you today?",
#             "time": datetime.datetime.now().strftime("%I:%M %p, %d %b %Y")
#         }
#     ]
#     return jsonify({"status": "success", "message": "Chat history cleared"})

# if __name__ == '__main__':
#     app.run(port=5000, debug=True)