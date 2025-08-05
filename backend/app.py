from flask import Flask, jsonify, request, redirect
from flask_cors import CORS
import datetime
import requests
from dotenv import load_dotenv
import os
import hmac
import hashlib
from urllib.parse import urlencode

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
load_dotenv()

AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4")
SHOPIFY_API_KEY = os.getenv("SHOPIFY_API_KEY")
SHOPIFY_API_SECRET = os.getenv("SHOPIFY_API_SECRET")
SHOPIFY_API_VERSION = os.getenv("SHOPIFY_API_VERSION", "2023-07")
APP_URL = os.getenv("APP_URL")

chat_history = [
    {
        "sender": "bot",
        "text": "Hello! How can I help you today?",
        "time": datetime.datetime.now().strftime("%I:%M %p, %d %b %Y")
    }
]

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

@app.route('/')
def root():
    shop = request.args.get('shop')
    hmac_param = request.args.get('hmac')
    if shop and hmac_param:
        if validate_hmac(request.args):
            return redirect(f'/install?{urlencode(request.args)}')
        return "Invalid HMAC signature", 400
    return "Install this app via Shopify Admin"

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
        token_url = f"https://{shop}/admin/oauth/access_token"
        token_response = requests.post(token_url, json={
            'client_id': SHOPIFY_API_KEY,
            'client_secret': SHOPIFY_API_SECRET,
            'code': code
        })
        token_response.raise_for_status()
        access_token = token_response.json()['access_token']

        # Install script tag pointing to Vercel-hosted frontend
        script_tag_url = f"https://{shop}/admin/api/{SHOPIFY_API_VERSION}/script_tags.json"
        requests.post(script_tag_url, json={
            "script_tag": {
                "event": "onload",
                "src": f"https://your-frontend.vercel.app/assets/widget-bundle.js"  # Update with your Vercel URL
            }
        }, headers={
            "X-Shopify-Access-Token": access_token
        }).raise_for_status()

        return redirect(f"https://{shop}/admin/apps")
    except requests.exceptions.RequestException as e:
        error_data = e.response.json() if hasattr(e, 'response') and e.response else {'error': str(e)}
        return jsonify({"error": "Installation failed", "details": error_data}), 500

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
        headers = {"Content-Type": "application/json", "api-key": AZURE_OPENAI_API_KEY}
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

@app.route('/widget.js')
def serve_widget_js():
    js_code = '''
    (function() {
        const container = document.createElement('div');
        container.id = 'chatbot-root';
        document.body.appendChild(container);

        const toggleButton = document.createElement('button');
        toggleButton.innerHTML = '💬';
        toggleButton.style.position = 'fixed';
        toggleButton.style.bottom = '20px';
        toggleButton.style.right = '20px';
        toggleButton.style.width = '60px';
        toggleButton.style.height = '60px';
        toggleButton.style.backgroundColor = '#6b21a8';
        toggleButton.style.borderRadius = '50%';
        toggleButton.style.border = 'none';
        toggleButton.style.cursor = 'pointer';
        toggleButton.style.color = 'white';
        toggleButton.style.zIndex = '99999';

        let isOpen = false;
        toggleButton.addEventListener('click', () => {
            const chatbox = document.getElementById('chatbot-root');
            isOpen = !isOpen;
            chatbox.style.display = isOpen ? 'block' : 'none';
            if (isOpen && !chatbox.innerHTML) {
                const script = document.createElement('script');
                script.src = 'https://chatbot-py-virid.vercel.app/widget-bundle.js';
                script.async = true;
                document.body.appendChild(script);
            }
        });

        document.body.appendChild(toggleButton);
    })();
    '''
    return js_code, 200, {'Content-Type': 'application/javascript'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=True)