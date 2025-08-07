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
    (function() {
        // Create widget container
        const widget = document.createElement('div');
        widget.id = 'shopify-chatbot-widget';
        widget.style.position = 'fixed';
        widget.style.bottom = '20px';
        widget.style.right = '20px';
        widget.style.width = '350px';
        widget.style.height = '500px';
        widget.style.backgroundColor = 'white';
        widget.style.borderRadius = '12px';
        widget.style.boxShadow = '0 5px 15px rgba(0,0,0,0.2)';
        widget.style.zIndex = '999999';
        widget.style.display = 'none';
        widget.style.flexDirection = 'column';
        widget.style.overflow = 'hidden';
        widget.style.fontFamily = 'system-ui, -apple-system, sans-serif';

        // Header
        const header = document.createElement('div');
        header.style.display = 'flex';
        header.style.alignItems = 'center';
        header.style.justifyContent = 'space-between';
        header.style.padding = '12px 16px';
        header.style.background = 'linear-gradient(to right, #8B5CF6, #6D28D9)';
        header.style.color = 'white';
        
        // Header title with icon
        const headerTitle = document.createElement('div');
        headerTitle.style.display = 'flex';
        headerTitle.style.alignItems = 'center';
        headerTitle.style.gap = '8px';
        
        const botIcon = document.createElement('div');
        botIcon.innerHTML = `
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z"/>
            </svg>
        `;
        
        const titleText = document.createElement('span');
        titleText.textContent = 'AI Assistant';
        titleText.style.fontWeight = '600';
        
        headerTitle.appendChild(botIcon);
        headerTitle.appendChild(titleText);
        
        // Close button
        const closeButton = document.createElement('button');
        closeButton.id = 'chatbot-close';
        closeButton.style.background = 'none';
        closeButton.style.border = 'none';
        closeButton.style.color = 'white';
        closeButton.style.cursor = 'pointer';
        closeButton.innerHTML = `
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/>
            </svg>
        `;
        
        header.appendChild(headerTitle);
        header.appendChild(closeButton);
        
        // Messages container
        const messages = document.createElement('div');
        messages.id = 'chatbot-messages';
        messages.style.flex = '1';
        messages.style.padding = '16px';
        messages.style.overflowY = 'auto';
        messages.style.display = 'flex';
        messages.style.flexDirection = 'column';
        messages.style.gap = '12px';
        messages.style.background = '#f9fafb';
        
        // Input area
        const inputArea = document.createElement('div');
        inputArea.style.padding = '12px 16px';
        inputArea.style.borderTop = '1px solid #e5e7eb';
        inputArea.style.display = 'flex';
        inputArea.style.gap = '8px';
        inputArea.style.background = 'white';
        
        const input = document.createElement('input');
        input.type = 'text';
        input.placeholder = 'Type your message...';
        input.style.flex = '1';
        input.style.padding = '8px 12px';
        input.style.border = '1px solid #d1d5db';
        input.style.borderRadius = '9999px';
        input.style.outline = 'none';
        input.style.fontSize = '14px';
        
        const sendButton = document.createElement('button');
        sendButton.innerHTML = `
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"/>
            </svg>
        `;
        sendButton.style.background = '#8b5cf6';
        sendButton.style.color = 'white';
        sendButton.style.border = 'none';
        sendButton.style.borderRadius = '9999px';
        sendButton.style.width = '36px';
        sendButton.style.height = '36px';
        sendButton.style.display = 'flex';
        sendButton.style.alignItems = 'center';
        sendButton.style.justifyContent = 'center';
        sendButton.style.cursor = 'pointer';
        
        inputArea.appendChild(input);
        inputArea.appendChild(sendButton);
        
        // Toggle button
        const toggleButton = document.createElement('button');
        toggleButton.id = 'chatbot-toggle';
        toggleButton.innerHTML = '💬';
        toggleButton.style.position = 'fixed';
        toggleButton.style.bottom = '20px';
        toggleButton.style.right = '20px';
        toggleButton.style.width = '60px';
        toggleButton.style.height = '60px';
        toggleButton.style.borderRadius = '50%';
        toggleButton.style.backgroundColor = '#6d28d9';
        toggleButton.style.color = 'white';
        toggleButton.style.border = 'none';
        toggleButton.style.cursor = 'pointer';
        toggleButton.style.zIndex = '999999';
        toggleButton.style.fontSize = '24px';
        toggleButton.style.display = 'flex';
        toggleButton.style.alignItems = 'center';
        toggleButton.style.justifyContent = 'center';
        
        // Build widget
        widget.appendChild(header);
        widget.appendChild(messages);
        widget.appendChild(inputArea);
        document.body.appendChild(widget);
        document.body.appendChild(toggleButton);
        
        // Store configuration
        const storeId = "116";
        const apiUrl = "https://n8nflow.byteztech.in/webhook/api/ask";
        
        // Session management
        let sessionId = localStorage.getItem('chatbot_session_id');
        if (!sessionId) {
            sessionId = 'session-' + Math.random().toString(36).substring(2, 15);
            localStorage.setItem('chatbot_session_id', sessionId);
        }
        
        // Chat state
        let chatMessages = [];
        let isLoading = false;
        
        // Add message to UI
        function addMessage(text, isUser) {
            const realTime = new Date().toLocaleString('en-IN', {
                hour: '2-digit',
                minute: '2-digit',
                hour12: true,
                day: '2-digit',
                month: 'short',
                year: 'numeric'
            });
            
            const message = document.createElement('div');
            message.style.display = 'flex';
            message.style.flexDirection = 'column';
            message.style.alignItems = isUser ? 'flex-end' : 'flex-start';
            message.style.marginBottom = '12px';
            
            // Message bubble
            const bubble = document.createElement('div');
            bubble.style.display = 'flex';
            bubble.style.alignItems = 'flex-start';
            bubble.style.gap = '8px';
            bubble.style.maxWidth = '80%';
            
            if (!isUser) {
                const botIcon = document.createElement('div');
                botIcon.innerHTML = `
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#9ca3af" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z"/>
                    </svg>
                `;
                bubble.appendChild(botIcon);
            }
            
            const content = document.createElement('div');
            content.style.padding = '8px 12px';
            content.style.borderRadius = isUser 
                ? '12px 12px 0 12px' 
                : '12px 12px 12px 0';
            content.style.background = isUser ? '#8b5cf6' : '#f3f4f6';
            content.style.color = isUser ? 'white' : '#1f2937';
            content.style.wordBreak = 'break-word';
            content.textContent = text;
            bubble.appendChild(content);
            
            message.appendChild(bubble);
            
            // Timestamp and user icon
            const meta = document.createElement('div');
            meta.style.display = 'flex';
            meta.style.alignItems = 'center';
            meta.style.gap = '4px';
            meta.style.marginTop = '4px';
            meta.style.fontSize = '11px';
            meta.style.color = '#9ca3af';
            
            const time = document.createElement('span');
            time.textContent = realTime;
            meta.appendChild(time);
            
            if (isUser) {
                const userIcon = document.createElement('div');
                userIcon.innerHTML = `
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#8b5cf6" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                    </svg>
                `;
                meta.appendChild(userIcon);
            }
            
            message.appendChild(meta);
            messages.appendChild(message);
            
            // Scroll to bottom
            messages.scrollTop = messages.scrollHeight;
            
            // Store message
            chatMessages.push({
                text: text,
                sender: isUser ? 'user' : 'bot',
                time: realTime
            });
        }
        
        // Show loading indicator
        function showLoading() {
            const loading = document.createElement('div');
            loading.id = 'chatbot-loading';
            loading.style.display = 'flex';
            loading.style.alignItems = 'center';
            loading.style.gap = '8px';
            loading.style.padding = '8px 12px';
            loading.style.background = '#f3f4f6';
            loading.style.borderRadius = '12px 12px 12px 0';
            loading.style.maxWidth = '80px';
            loading.style.marginBottom = '12px';
            
            for (let i = 0; i < 3; i++) {
                const dot = document.createElement('div');
                dot.style.width = '6px';
                dot.style.height = '6px';
                dot.style.background = '#9ca3af';
                dot.style.borderRadius = '50%';
                dot.style.animation = `bounce 1s infinite ${i * 0.2}s`;
                loading.appendChild(dot);
            }
            
            messages.appendChild(loading);
            messages.scrollTop = messages.scrollHeight;
            
            return loading;
        }
        
        // Hide loading indicator
        function hideLoading() {
            const loading = document.getElementById('chatbot-loading');
            if (loading) {
                loading.remove();
            }
        }
        
        // Send message to API
        async function sendMessage(messageText) {
            if (!messageText.trim() || !sessionId) {
                if (!sessionId) {
                    addMessage('No session ID available. Please try again.', false);
                }
                return;
            }
            
            addMessage(messageText, true);
            input.value = '';
            
            const loading = showLoading();
            isLoading = true;
            
            try {
                const response = await fetch(apiUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        question: messageText,
                        sessionId: sessionId,
                        Store_id: storeId
                    })
                });
                
                if (!response.ok) throw new Error('API request failed');
                
                const data = await response.json();
                let botReply = 'Sorry, I could not understand the response.';
                
                if (data && Array.isArray(data) && data[0]?.output) {
                    botReply = data[0].output;
                }
                
                addMessage(botReply, false);
            } catch (error) {
                console.error('Chat error:', error);
                addMessage("Sorry, I'm having trouble connecting. Please try again later.", false);
            } finally {
                hideLoading();
                isLoading = false;
            }
        }
        
        // Clear chat history
        function clearChat() {
            messages.innerHTML = '';
            chatMessages = [];
            addMessage("Hello! How can I help you today?", false);
        }
        
        // Event listeners
        sendButton.addEventListener('click', () => {
            if (input.value.trim() && !isLoading) {
                sendMessage(input.value);
            }
        });
        
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && input.value.trim() && !isLoading) {
                sendMessage(input.value);
            }
        });
        
        toggleButton.addEventListener('click', () => {
            widget.style.display = widget.style.display === 'none' ? 'flex' : 'none';
            toggleButton.style.display = widget.style.display === 'none' ? 'flex' : 'none';
        });
        
        closeButton.addEventListener('click', () => {
            widget.style.display = 'none';
            toggleButton.style.display = 'flex';
        });
        
        // Add animation style
        const style = document.createElement('style');
        style.textContent = `
            @keyframes bounce {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-4px); }
            }
        `;
        document.head.appendChild(style);
        
        // Initial greeting
        widget.style.display = 'flex';
        toggleButton.style.display = 'none';
        addMessage("Hello! How can I help you today?", false);
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