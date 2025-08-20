from flask import Flask, jsonify, request, redirect, send_from_directory, render_template_string
from flask_cors import CORS
import datetime
import requests
from dotenv import load_dotenv
import os
import hmac
import hashlib
from urllib.parse import urlencode
import urllib.parse
import psycopg2
from psycopg2.extras import RealDictCursor

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
SHOPIFY_API_KEY = os.getenv("SHOPIFY_API_KEY")
SHOPIFY_API_SECRET = os.getenv("SHOPIFY_API_SECRET")
SHOPIFY_API_VERSION = os.getenv("SHOPIFY_API_VERSION", "2024-01")
APP_URL = os.getenv("APP_URL")
SHOPIFY_APP_HANDLE = os.getenv("SHOPIFY_APP_HANDLE")

# Database setup
password = "Dcmh#2026"
escaped_password = urllib.parse.quote_plus(password)
DATABASE_URI = f'postgresql://shopifyai:{escaped_password}@103.39.131.9:5432/shopifyai'

def get_db_connection():
    return psycopg2.connect(DATABASE_URI, cursor_factory=RealDictCursor)

# Store access tokens
shops_db = {}

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

@app.route("/")
def index():
    shop = request.args.get("shop")
    hmac_param = request.args.get("hmac")

    if shop and hmac_param:
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
    install_url = f"https://{shop}/admin/oauth/authorize?client_id={SHOPIFY_API_KEY}&scope={scopes}&redirect_uri={redirect_uri}&state=random_state_string"
    
    return redirect(install_url)

@app.route('/auth/callback')
def auth_callback():
    shop = request.args.get('shop')
    code = request.args.get('code')
    hmac_param = request.args.get('hmac')
    host = request.args.get('host')
    
    if not all([shop, code, hmac_param]):
        return jsonify({"error": "Missing required parameters"}), 400
    
    if not validate_hmac(request.args):
        return jsonify({"error": "Invalid HMAC"}), 403
    
    try:
        # Get access token
        token_url = f"https://{shop}/admin/oauth/access_token"
        token_response = requests.post(token_url, json={
            'client_id': SHOPIFY_API_KEY,
            'client_secret': SHOPIFY_API_SECRET,
            'code': code
        })
        token_response.raise_for_status()
        access_token = token_response.json()['access_token']
        
        # Store access token
        shops_db[shop] = {'access_token': access_token}
 
        # Install script tag
        embed_url = f"https://{shop}/admin/api/{SHOPIFY_API_VERSION}/script_tags.json"
        requests.post(embed_url, json={
            "script_tag": {
                "src": f"{APP_URL}/widget.js",
                "event": "onload"
            }
        }, headers={
            "X-Shopify-Access-Token": access_token
        })
        
        # Redirect to embedded app
        embedded_app_url = f"{APP_URL}/embedded?shop={shop}&host={host}"
        return redirect(embedded_app_url)
    
    except requests.exceptions.RequestException as e:
        print(f"OAuth Error: {e}")
        return jsonify({"error": "Installation failed"}), 500

@app.route('/embedded')
def embedded_app():
    shop = request.args.get('shop')
    host = request.args.get('host')
    
    if not shop or not host:
        return "Missing shop or host parameters", 400
    
    # Simple HTML that redirects to React app with embedded flag
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Chatbot App</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <script>
            // Store shop info and redirect to React app
            localStorage.setItem('shopify_shop', '{{ shop }}');
            localStorage.setItem('shopify_host', '{{ host }}');
            localStorage.setItem('shopify_embedded', 'true');
            window.location.href = '{{ app_url }}?embedded=true&shop={{ shop }}';
        </script>
    </head>
    <body>
        <div style="text-align: center; padding: 50px; font-family: Arial, sans-serif;">
            <h2>Loading Chatbot App...</h2>
            <p>Redirecting to your application</p>
        </div>
    </body>
    </html>
    """
    
    return render_template_string(html_template, shop=shop, host=host, app_url=APP_URL)
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

@app.route('/trainlist', methods=['GET'])
def get_trainlist():
    store_id = request.args.get('store_id')  # Get store_id from query parameters
    
    if not store_id:
        return jsonify({"message": "store_id parameter is required!"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # Fetch store details
        cursor.execute("SELECT id AS store_id, name, client_id FROM store WHERE id = %s", (store_id,))
        store = cursor.fetchone()

        if not store:
            conn.close()
            return jsonify({"message": "Store not found!"}), 404

        # Fetch client details
        cursor.execute("SELECT id AS client_id, email, created_at FROM client WHERE id = %s", (store["client_id"],))
        client = cursor.fetchone()

        if not client:
            conn.close()
            return jsonify({"message": "Client not found!"}), 404

        # Fetch all training records for the given store_id
        cursor.execute(
            """
            SELECT id AS training_id, created_at, store_id, file_jsonl, jsonl_status, 
                   file_id, model_id, status, error_message, try, client_id, is_running, website_url
            FROM training
            WHERE store_id = %s
            ORDER BY created_at DESC
            """,
            (store_id,)
        )
        training_records = cursor.fetchall()
        conn.close()

        return jsonify({
            "client_id": client["client_id"],
            "email": client["email"],
            "created_at": client["created_at"].isoformat() if client["created_at"] else None,
            "store": {
                "store_id": store["store_id"],
                "name": store["name"],
            },
            "trainings": [
                {
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
                    "client_id": record["client_id"],
                    "is_running": record["is_running"],
                    "website_url": record["website_url"]
                }
                for record in training_records
            ]
        }), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "Error occurred, please try again."}), 500
    
    

# @app.route('/trainlistByStoreName', methods=['GET'])
# def get_trainlist():
#     store = request.args.get('store')  # Get store_id from query parameters
#     store_id = 0
    
#     if not store:
#         return jsonify({"message": "store_id parameter is required!"}), 400
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor(cursor_factory=RealDictCursor)
        

#         # Fetch store details
#         cursor.execute("SELECT id AS store_id, name, client_id FROM store WHERE name = %s", (store))
#         store = cursor.fetchone()
#         store_id = store["store_id"] if store else None

#         if not store:
#             conn.close()
#             return jsonify({"message": "Store not found!"}), 404

#         # Fetch client details
#         cursor.execute("SELECT id AS client_id, email, created_at FROM client WHERE id = %s", (store["client_id"],))
#         client = cursor.fetchone()

#         if not client:
#             conn.close()
#             return jsonify({"message": "Client not found!"}), 404

#         # Fetch all training records for the given store_id
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
#         print(f"Error: {e}")
#         return jsonify({"message": "Error occurred, please try again."}), 500
    

@app.route('/shopify-store', methods=['POST'])
def add_shopify_store():
    data = request.get_json()

    raw_url = data.get('url')
    status = data.get('status')
    client_id = data.get('client_id')  # now client_id should come from the request

    if not raw_url or not status or not client_id:
        return jsonify({"message": "client_id, url and status are required!"}), 400

    # Derive store name from the domain (remove protocol and TLDs), but keep URL as-is
    parse_target = raw_url
    if not parse_target.startswith("http://") and not parse_target.startswith("https://"):
        parse_target = "https://" + parse_target.lstrip("/")

    try:
        parsed = urllib.parse.urlparse(parse_target)
        hostname = parsed.hostname or ""
    except Exception:
        hostname = ""

    if not hostname:
        # Fallback parsing if urlparse failed
        temp = raw_url
        if '://' in temp:
            temp = temp.split('://', 1)[1]
        temp = temp.lstrip('/')
        hostname = temp.split('/', 1)[0]

    if hostname.startswith('www.'):
        hostname = hostname[4:]

    parts = [p for p in hostname.split('.') if p]
    if len(parts) >= 2:
        derived_name = parts[-2]  # e.g., amazon from amazon.in / amazon.com
    elif parts:
        derived_name = parts[0]
    else:
        derived_name = hostname or "store"

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check duplicate store (same client, same name and url)
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

        # Insert new store
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