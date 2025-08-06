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
    js_code = '''
  // Updated widget.js
(function() {
  // Create chat container
  const chatContainer = document.createElement('div');
  chatContainer.id = 'shopify-chatbot-container';
  chatContainer.style.position = 'fixed';
  chatContainer.style.bottom = '20px';
  chatContainer.style.right = '20px';
  chatContainer.style.zIndex = '99999';
  chatContainer.style.width = '350px';
  chatContainer.style.height = '500px';
  chatContainer.style.display = 'none'; // Initially hidden
  chatContainer.style.backgroundColor = 'white';
  chatContainer.style.borderRadius = '12px';
  chatContainer.style.boxShadow = '0 4px 12px rgba(0,0,0,0.2)';
  chatContainer.style.overflow = 'hidden';
  
  // Create toggle button
  const toggleButton = document.createElement('button');
  toggleButton.innerHTML = '💬';
  toggleButton.style.position = 'fixed';
  toggleButton.style.bottom = '20px';
  toggleButton.style.right = '20px';
  toggleButton.style.width = '60px';
  toggleButton.style.height = '60px';
  toggleButton.style.backgroundColor = '#6d28d9'; // Purple color
  toggleButton.style.borderRadius = '50%';
  toggleButton.style.border = 'none';
  toggleButton.style.cursor = 'pointer';
  toggleButton.style.color = 'white';
  chatContainer.style.fontSize = '24px';
  toggleButton.style.zIndex = '99999';
  
  // Toggle chat visibility
  let isChatOpen = false;
  toggleButton.addEventListener('click', () => {
    isChatOpen = !isChatOpen;
    chatContainer.style.display = isChatOpen ? 'block' : 'none';
  });
  
  // Chat UI structure
  chatContainer.innerHTML = `
    <div style="height: 100%; display: flex; flex-direction: column;">
      <!-- Header -->
      <div style="background: linear-gradient(to right, #8b5cf6, #7c3aed); color: white; padding: 12px 16px; display: flex; justify-content: space-between; align-items: center;">
        <div style="display: flex; align-items: center; gap: 8px;">
          <svg style="width: 20px; height: 20px;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
          </svg>
          <div>
            <div style="font-weight: 600; font-size: 16px;">AI Assistant</div>
            <div style="font-size: 11px; opacity: 0.8;">● Online</div>
          </div>
        </div>
        <button id="chatbot-clear" style="background: none; border: none; color: white; cursor: pointer;">
          <svg style="width: 18px; height: 18px;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
          </svg>
        </button>
      </div>
      
      <!-- Messages container -->
      <div id="chatbot-messages" style="flex: 1; overflow-y: auto; padding: 16px; background: #f9fafb;"></div>
      
      <!-- Input area -->
      <div style="border-top: 1px solid #e5e7eb; padding: 12px; background: white; display: flex; gap: 8px;">
        <input 
          id="chatbot-input" 
          type="text" 
          placeholder="Type your message..." 
          style="flex: 1; border: 1px solid #d1d5db; border-radius: 9999px; padding: 8px 16px; outline: none; font-size: 14px;"
        >
        <button 
          id="chatbot-send" 
          style="background: #7c3aed; color: white; border: none; border-radius: 9999px; width: 40px; height: 40px; display: flex; justify-content: center; align-items: center; cursor: pointer;"
        >
          <svg style="width: 16px; height: 16px;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path>
          </svg>
        </button>
      </div>
    </div>
  `;
  
  // Append elements to DOM
  document.body.appendChild(chatContainer);
  document.body.appendChild(toggleButton);
  
  // Chat functionality
  const messagesContainer = document.getElementById('chatbot-messages');
  const inputField = document.getElementById('chatbot-input');
  const sendButton = document.getElementById('chatbot-send');
  const clearButton = document.getElementById('chatbot-clear');
  
  // Add initial bot message
  addMessage('Hello! How can I help you today?', 'bot');
  
  // Send message function
  function sendMessage() {
    const message = inputField.value.trim();
    if (message) {
      addMessage(message, 'user');
      inputField.value = '';
      
      // Simulate bot response (replace with actual API call)
      setTimeout(() => {
        addMessage('I received your message. This is a simulated response.', 'bot');
      }, 1000);
    }
  }
  
  // Add message to chat
  function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.style.marginBottom = '12px';
    messageDiv.style.display = 'flex';
    messageDiv.style.flexDirection = 'column';
    messageDiv.style.alignItems = sender === 'user' ? 'flex-end' : 'flex-start';
    
    const bubble = document.createElement('div');
    bubble.style.padding = '8px 12px';
    bubble.style.borderRadius = '12px';
    bubble.style.maxWidth = '80%';
    bubble.style.fontSize = '14px';
    
    if (sender === 'user') {
      bubble.style.background = '#7c3aed';
      bubble.style.color = 'white';
      bubble.style.borderBottomRightRadius = '0';
    } else {
      bubble.style.background = 'white';
      bubble.style.color = '#1f2937';
      bubble.style.borderBottomLeftRadius = '0';
      bubble.style.boxShadow = '0 1px 2px rgba(0,0,0,0.1)';
    }
    
    bubble.textContent = text;
    messageDiv.appendChild(bubble);
    
    // Add timestamp
    const timeDiv = document.createElement('div');
    timeDiv.style.fontSize = '11px';
    timeDiv.style.color = '#6b7280';
    timeDiv.style.marginTop = '4px';
    timeDiv.textContent = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    messageDiv.appendChild(timeDiv);
    
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }
  
  // Event listeners
  sendButton.addEventListener('click', sendMessage);
  inputField.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
  });
  
  clearButton.addEventListener('click', () => {
    messagesContainer.innerHTML = '';
    addMessage('Hello! How can I help you today?', 'bot');
  });
})();
    '''
    return js_code, 200, {'Content-Type': 'application/javascript'}


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
        "src": f"https://chatbot-bpy.clustersofttech.com/widget.js",
        "event": "onload"
    }
}, headers={
    "X-Shopify-Access-Token": access_token
})
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