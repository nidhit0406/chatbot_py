from flask import Flask, jsonify, request, redirect, send_from_directory, Response
from flask_cors import CORS
import datetime
import requests
from dotenv import load_dotenv
import os
import hmac
import hashlib
import json
from urllib.parse import urlencode
from shopify import Session
import shopify
import urllib.parse
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization", "X-Shop-Domain"],
        "supports_credentials": True,
        "expose_headers": ["Content-Type"]
    }
})

# Configuration
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4")
SHOPIFY_API_KEY = os.getenv("SHOPIFY_API_KEY")
SHOPIFY_API_SECRET = os.getenv("SHOPIFY_API_SECRET")
SHOPIFY_API_VERSION = os.getenv("SHOPIFY_API_VERSION", "2023-07")
APP_URL = os.getenv("APP_URL")
SHOPIFY_APP_HANDLE = os.getenv("SHOPIFY_APP_HANDLE")

# Database simulation
shops_db = {}  # {shop_domain: {access_token: str, chat_history: list}}
products_db = {}  # {shop_domain: [product1, product2...]}

# Database Connection Setup
password = "Dcmh#2026"
escaped_password = urllib.parse.quote_plus(password)
# DATABASE_URI = f'postgresql://shopifyai:{escaped_password}@103.39.131.9:5432/shopifyai'
DATABASE_URI = f'postgresql://postgres:1112@localhost:5432/shopify_ai'


def get_db_connection():
    return psycopg2.connect(DATABASE_URI, cursor_factory=RealDictCursor)

def validate_hmac(query_params):
    hmac_param = query_params.get('hmac')
    if not hmac_param or not SHOPIFY_API_SECRET:
        return False
    
    params = query_params.copy()
    params.pop('hmac', None)
    sorted_params = urlencode(sorted(params.items()))
    
    digest = hmac.new(
        SHOPIFY_API_SECRET.encode('utf-8'),
        sorted_params.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(digest, hmac_param)

def get_shopify_context(shop_domain):
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

@app.route("/")
def index():
    shop = request.args.get("shop")
    hmac = request.args.get("hmac")
    if shop and hmac:
        query_params = request.args.to_dict(flat=True)
        return redirect(f"/install?{urlencode(query_params)}")
    return """
        <html>
            <head><title>Chatbot App</title></head>
            <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
                <h1>🤖 Chatbot App</h1>
                <p>Your app is running successfully!</p>
                <p>If you installed this app in Shopify, please open it from your <b>Shopify Admin</b>.</p>
            </body>
        </html>
    """, 200

@app.route('/install')
def install():
    shop = request.args.get('shop')
    if not shop:
        return "Shop parameter missing", 400
    
    scopes = 'write_script_tags,read_products'
    redirect_uri = f"{APP_URL}/auth/callback"
    install_url = f"https://{shop}/admin/oauth/authorize?client_id={SHOPIFY_API_KEY}&scope={scopes}&redirect_uri={redirect_uri}"
    return redirect(install_url)

@app.route('/auth/callback')
def auth_callback():
    shop = request.args.get('shop')
    code = request.args.get('code')
    hmac_param = request.args.get('hmac')
    
    if not all([shop, code, hmac_param]):
        return jsonify({"error": "Missing required parameters"}), 400
    
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
 
        # 2. Embed app in Shopify admin with dynamic widget.js
        embed_url = f"https://{shop}/admin/api/2024-01/script_tags.json"
        requests.post(embed_url, json={
            "script_tag": {
                "src": f"{APP_URL}/widget.js?shop={shop}",
                "event": "onload"
            }
        }, headers={
            "X-Shopify-Access-Token": access_token
        })
        # return redirect(f"https://{shop}/admin/apps/{SHOPIFY_APP_HANDLE}")
         return redirect(f"http://localhost:3000/login?store={shop}")
    
    except requests.exceptions.RequestException as e:
        error_data = e.response.json() if hasattr(e, 'response') and e.response else {'error': str(e)}
        print(f"OAuth Error: {error_data}")
        return jsonify({
            "error": "Installation failed",
            "details": error_data
        }), 500

@app.route('/widget.js')
def serve_widget_js():
    store_id = request.args.get('shop')
    if not store_id:
        return "Error: shop parameter is required", 400

    # Use shop domain as store_id (no database query)
    # store_id = shop_domain.replace('.myshopify.com', '')  # e.g., "example-store" from "example-store.myshopify.com"
    response = f"""
    (function() {{
        var script = document.createElement('script');
        script.src = '{APP_URL}/static/chatbot-widget.js';
        script.setAttribute('data-store-id', '{store_id}');
        script.setAttribute('data-api-url', 'https://n8nflow.byteztech.in/webhook/api/ask');
        script.setAttribute('data-welcome-message', 'Hello! How can I help you today?');
        script.setAttribute('data-primary-color', '#8B5CF6');
        script.setAttribute('data-secondary-color', '#6D28D9');
        script.setAttribute('data-widget-title', 'AI Assistant');
        script.setAttribute('data-position', 'right');
        document.head.appendChild(script);
    }})();
    """
    return Response(response, mimetype='application/javascript')

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

# @app.route('/trainlist', methods=['GET'])
# def get_trainlist():
#     store_id = request.args.get('store_id')
#     if not store_id:
#         return jsonify({"message": "store_id parameter is required!"}), 400

#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor(cursor_factory=RealDictCursor)
#         cursor.execute("SELECT id AS store_id, name, client_id FROM store WHERE id = %s", (store_id,))
#         store = cursor.fetchone()

#         if not store:
#             conn.close()
#             return jsonify({"message": "Store not found!"}), 404

#         cursor.execute("SELECT id AS client_id, email, created_at FROM client WHERE id = %s", (store["client_id"],))
#         client = cursor.fetchone()

#         if not client:
#             conn.close()
#             return jsonify({"message": "Client not found!"}), 404

#         cursor.execute(
#             """
#             SELECT id AS training_id, created_at, store_id, file_jsonl, jsonl_status, 
#                    file_id, model_id, status, error_message, try, client_id, is_running, website_url
#             FROM training
#             WHERE store_id = %s
#             ORDER BY created_at DESC
#             """,
#             (store_id,)
#         )
#         training_records = cursor.fetchall()
#         conn.close()

#         return jsonify({
#             "client_id": client["client_id"],
#             "email": client["email"],
#             "created_at": client["created_at"].isoformat() if client["created_at"] else None,
#             "store": {
#                 "store_id": store["store_id"],
#                 "name": store["name"],
#             },
#             "trainings": [
#                 {
#                     "training_id": record["training_id"],
#                     "created_at": record["created_at"].isoformat() if record["created_at"] else None,
#                     "store_id": record["store_id"],
#                     "file_jsonl": record["file_jsonl"],
#                     "jsonl_status": record["jsonl_status"],
#                     "file_id": record["file_id"],
#                     "model_id": record["model_id"],
#                     "status": record["status"],
#                     "error_message": record["error_message"],
#                     "try": record["try"],
#                     "client_id": record["client_id"],
#                     "is_running": record["is_running"],
#                     "website_url": record["website_url"]
#                 }
#                 for record in training_records
#             ]
#         }), 200

#     except Exception as e:
#         print(f"Error===: {e}")
#         return jsonify({"message": "Error occurred, please try again."}), 500

@app.route('/trainlist', methods=['GET'])
def get_trainlist():
    domain = request.args.get('domain')
    if not domain:
        return jsonify({"message": "domain parameter is required!", "state": {"storeExists": False, "clientExists": False, "hasTrainings": False}}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Check if store exists
        cursor.execute("SELECT id AS store_id, name, client_id FROM store WHERE url = %s", (domain,))
        store = cursor.fetchone()

        state = {"storeExists": bool(store), "clientExists": False, "hasTrainings": False}

        client = None
        training_records = []

        if store:
            cursor.execute("SELECT id AS client_id, email, created_at FROM client WHERE id = %s", (store["client_id"],))
            client = cursor.fetchone()
            state["clientExists"] = bool(client)

            if client:
                cursor.execute(
                    """
                    SELECT id AS training_id, created_at, store_id, file_jsonl, jsonl_status, 
                           file_id, model_id, status, error_message, try, client_id, is_running, website_url
                    FROM training
                    WHERE store_id = %s
                    ORDER BY created_at DESC
                    """,
                    (store["store_id"],)
                )
                training_records = cursor.fetchall()
                state["hasTrainings"] = bool(training_records)
        
        conn.close()

        return jsonify({
            "message": "Success" if state["storeExists"] else "Store not found",
            "state": state,
            "client_id": client["client_id"] if client else None,
            "email": client["email"] if client else None,
            "created_at": client["created_at"].isoformat() if client and client.get("created_at") else None,
            "store": {"store_id": store["store_id"], "name": store["name"]} if store else None,
        }), 200 if state["storeExists"] else 404

    except Exception as e:
        print(f"Error===: {e}")
        return jsonify({"message": "Error occurred, please try again.", "state": {"storeExists": False, "clientExists": False, "hasTrainings": False}}), 500


@app.route('/shopify-store', methods=['POST'])
def add_shopify_store():
    data = request.get_json()

    raw_url = data.get('url')
    status = data.get('status')
    client_id = data.get('client_id')

    if not raw_url or not status or not client_id:
        return jsonify({"message": "client_id, url and status are required!"}), 400

    parse_target = raw_url
    if not parse_target.startswith("http://") and not parse_target.startswith("https://"):
        parse_target = "https://" + parse_target.lstrip("/")

    try:
        parsed = urllib.parse.urlparse(parse_target)
        hostname = parsed.hostname or ""
    except Exception:
        hostname = ""

    if not hostname:
        temp = raw_url
        if '://' in temp:
            temp = temp.split('://', 1)[1]
        temp = temp.lstrip('/')
        hostname = temp.split('/', 1)[0]

    if hostname.startswith('www.'):
        hostname = hostname[4:]

    parts = [p for p in hostname.split('.') if p]
    if len(parts) >= 2:
        derived_name = parts[-2]
    elif parts:
        derived_name = parts[0]
    else:
        derived_name = hostname or "store"

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id 
            FROM store 
            WHERE client_id = %s AND name = %s AND url = %s
            """,
            (client_id, derived_name, raw_url)
        )
        existing_store = cursor.fetchone()

        if existing_store:
            conn.close()
            return jsonify({
                "message": f"Store with name '{derived_name}' and URL '{raw_url}' already exists for this client!",
                "store_id": existing_store["id"] if isinstance(existing_store, dict) else existing_store[0]
            }), 200

        cursor.execute(
            """
            INSERT INTO store (client_id, name, url, status) 
            VALUES (%s, %s, %s, %s) 
            RETURNING id, created_at
            """,
            (client_id, derived_name, raw_url, status)
        )
        new_store = cursor.fetchone()
        conn.commit()
        conn.close()

        return jsonify({
            "message": "Store data added successfully!",
            "store_id": new_store["id"] if isinstance(new_store, dict) else new_store[0],
            "name": derived_name,
            "url": raw_url,
            "created_at": new_store["created_at"].isoformat() if isinstance(new_store, dict) and new_store.get("created_at") else None
        }), 201

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "Error occurred, please try again."}), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)