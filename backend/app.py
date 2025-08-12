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
from flask_jwt_extended import get_jwt_identity
import psycopg2
from psycopg2.extras import RealDictCursor
import urllib.parse
from dotenv import load_dotenv
import shopify
#   (function() {
#       // Create iframe container
#       const widgetContainer = document.createElement('div');
#       widgetContainer.id = 'chatbot-widget-container';
#       widgetContainer.style.position = 'fixed';
#       widgetContainer.style.bottom = '20px';
#       widgetContainer.style.right = '20px';
#       widgetContainer.style.zIndex = '99999';
      
#       // Create iframe
#       const iframe = document.createElement('iframe');
#       iframe.src = 'https://chatbot-py-virid.vercel.app';
#       iframe.style.border = 'none';
#       iframe.style.borderRadius = '8px';
#       iframe.style.boxShadow = '0 4px 12px rgba(0,0,0,0.2)';
#       iframe.style.width = '0';
#       iframe.style.height = '0';
#       iframe.style.transition = 'all 0.3s ease';
      
#       // Create toggle button
#       const toggleButton = document.createElement('button');
#       toggleButton.innerHTML = '💬';
#       toggleButton.style.bottom = '20px';
#       toggleButton.style.right = '20px';
#       toggleButton.style.width = '60px';
#       toggleButton.style.height = '60px';
#       toggleButton.style.backgroundColor = 'gray';
#       toggleButton.style.borderRadius = '50%';
#       toggleButton.style.border = 'none';
#       toggleButton.style.cursor = 'pointer';
#       toggleButton.style.color = 'white';
#       toggleButton.style.zIndex = '99999';
      
#       // Toggle iframe visibility
#       let isOpen = false;
#       toggleButton.addEventListener('click', () => {
#         isOpen = !isOpen;
#         if (isOpen) {
#           iframe.style.width = '400px';
#           iframe.style.height = '600px';
#         } else {
#           iframe.style.width = '0';
#           iframe.style.height = '0';
#         }
#       });
      
#       // Append elements to DOM
#       widgetContainer.appendChild(iframe);
#       widgetContainer.appendChild(toggleButton);
#       document.body.appendChild(widgetContainer);
#     })();
# Initialize Flask app
app = Flask(__name__)
@app.route('/widget.js')
def serve_widget_js():
    return send_from_directory(app.static_folder, 'chatbot-widget.js')


# @app.route('/widget.js')
# def serve_widget_js():
#     js_code = '''
# (function() {

#   const iframe = document.createElement("iframe");
#   iframe.src = "https://chatbot-py-two.vercel.app";
#   iframe.style.position = "fixed";
#  iframe.style.bottom = "20px";
#  iframe.style.right = "20px";
# iframe.style.backgroundColor = "red";
# iframe.style.width = "500px";
# iframe.style.height = "500px";
 
#   document.body.appendChild(iframe);

# })();
#     '''
#     return js_code, 200, {'Content-Type': 'application/javascript'}



# ✅ Add this near the bottom of the file:
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
password = "Dcmh#2026"
escaped_password = urllib.parse.quote_plus(password)
DATABASE_URI = f'postgresql://shopifyai:{escaped_password}@103.39.131.9:5432/shopifyai'
# Load environment variables
load_dotenv()
def get_db_connection():
    return psycopg2.connect(DATABASE_URI, cursor_factory=RealDictCursor)

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

@app.route('/install')
def install():
    shop = request.args.get('shop')
    if not shop:
        return "Shop parameter missing", 400
    
    scopes = 'write_script_tags,read_products'
    redirect_uri = f"{APP_URL}/auth/callback"  # Fixed syntax
    install_url = f"https://{shop}/admin/oauth/authorize?client_id={SHOPIFY_API_KEY}&scope={scopes}&redirect_uri={redirect_uri}"
    return redirect(install_url)


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
                "src": f"{APP_URL}/widget.js",
                "event": "onload"
            }
        }, headers={
            "X-Shopify-Access-Token": access_token
        })
        
        # 3. Store access token in shops_db
        shops_db[shop] = {'access_token': access_token, 'chat_history': []}

        # 4. Redirect to /post-auth with shop and token as query parameters
        return redirect(f'/post-auth?shop={shop}&token={access_token}')

    except requests.exceptions.RequestException as e:
        error_data = e.response.json() if hasattr(e, 'response') and e.response else {'error': str(e)}
        print(f"OAuth Error: {error_data}")
        return jsonify({
            "error": "Installation failed",
            "details": error_data
        }), 500

# New route to handle /post-auth
@app.route('/post-auth')
def post_auth():
    shop = request.args.get('shop')
    access_token = request.args.get('token')
    
    if not shop or not access_token:
        return "Missing shop or token", 400

    try:
        # Call /trainlist API (assuming it needs the shop context or token)
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # Simulate a call to /trainlist with the shop context (adjust based on your needs)
        session = Session(shop, SHOPIFY_API_VERSION)
        session.token = access_token
        shopify.ShopifyResource.activate_session(session)
        
        shop_data = shopify.Shop.current().to_dict()
        cursor.execute(
            "INSERT INTO shops (shop_domain, access_token, shop_data) VALUES (%s, %s, %s) "
            "ON CONFLICT (shop_domain) DO UPDATE SET access_token = EXCLUDED.access_token, "
            "shop_data = EXCLUDED.shop_data",
            (shop, access_token, json.dumps(shop_data))
        )
        conn.commit()

        # Optionally call /trainlist for the client (if tied to a user)
        # This assumes /trainlist needs a client_id; adjust logic as per your JWT or shop mapping
        cursor.execute("SELECT id AS client_id FROM client WHERE shop_domain = %s", (shop,))
        client = cursor.fetchone()
        if client:
            trainlist_response = get_trainlist_logic(client['client_id'], shop)
            conn.close()
            # Redirect to Shopify admin after processing
            return redirect(f"https://{shop}/admin/apps/{SHOPIFY_API_KEY}")
        else:
            conn.close()
            return "Client not found for this shop", 404

    except Exception as e:
        print(f"Error in post-auth: {e}")
        return jsonify({"message": "Error occurred, please try again."}), 500

def get_trainlist_logic(client_id, shop):
    # Mock implementation of /trainlist logic
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("SELECT id AS store_id, name FROM store WHERE client_id = %s", (client_id,))
    stores = cursor.fetchall()

    cursor.execute(
        """
        SELECT id AS training_id, created_at, store_id, file_jsonl, jsonl_status, 
               file_id, model_id, status, error_message, try, client_id
        FROM training
        WHERE client_id = %s
        """,
        (client_id,)
    )
    training_records = cursor.fetchall()
    conn.close()

    grouped_trainings = {}
    for record in training_records:
        store_id = record["store_id"]
        if store_id not in grouped_trainings:
            grouped_trainings[store_id] = []
        grouped_trainings[store_id].append({
            "training_id": record["training_id"],
            "created_at": record["created_at"].isoformat() if record["created_at"] else None,
            "store_id": record["store_id"],
            "file_jsonl": record["file_jsonl"],
            "jsonl_status": record["jsonl_status"],
            "file_id": record["file_id"],
            "model_id": record["model_id"],
            "status": record["status"],
            "error_message": record["error_message"],
            "try": record["try"],
            "client_id": record["client_id"]
        })

    return {
        "client_id": client_id,
        "shop": shop,
        "stores": [
            {
                "store_id": store["store_id"],
                "name": store["name"],
                "trainings": grouped_trainings.get(store["store_id"], [])
            }
            for store in stores
        ]
    }
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