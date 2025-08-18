// // chatbot-widget.js
// (function() {
//   // 1. Configuration - Get settings from script attributes
//   const currentScript = document.currentScript || 
//     Array.from(document.getElementsByTagName('script')).pop();
  
//   const config = {
//     apiUrl: currentScript.getAttribute('data-api-url') || "https://n8nflow.byteztech.in/webhook/api/ask",
//     sessionApiUrl: "http://103.39.131.9:8050/create-session",
//     storeId: currentScript.getAttribute('data-store-id') || "116",
//     welcomeMessage: currentScript.getAttribute('data-welcome-message') || "Hello! How can I help you today?",
//     primaryColor: currentScript.getAttribute('data-primary-color') || "#8B5CF6",
//     secondaryColor: currentScript.getAttribute('data-secondary-color') || "#6D28D9",
//     widgetTitle: currentScript.getAttribute('data-widget-title') || "AI Assistant",
//     position: currentScript.getAttribute('data-position') || "right"
//   };

//   // 2. Create UI Elements
//   const widget = document.createElement('div');
//   widget.id = 'shopify-chatbot-widget';
//   widget.style.position = 'fixed';
//   widget.style.bottom = '20px';
//   widget.style[config.position] = '20px';
//   widget.style.width = '350px';
//   widget.style.height = '500px';
//   widget.style.backgroundColor = 'white';
//   widget.style.borderRadius = '12px';
//   widget.style.boxShadow = '0 5px 15px rgba(0,0,0,0.2)';
//   widget.style.zIndex = '999999';
//   widget.style.display = 'none';
//   widget.style.flexDirection = 'column';
//   widget.style.overflow = 'hidden';
//   widget.style.fontFamily = 'system-ui, -apple-system, sans-serif';
//   widget.style.transition = 'all 0.3s ease';

//   // Header with configurable colors
//   const header = document.createElement('div');
//   header.style.display = 'flex';
//   header.style.alignItems = 'center';
//   header.style.justifyContent = 'space-between';
//   header.style.padding = '12px 16px';
//   header.style.background = `linear-gradient(to right, ${config.primaryColor}, ${config.secondaryColor})`;
//   header.style.color = 'white';
  
//   // Header title
//   const headerTitle = document.createElement('div');
//   headerTitle.style.display = 'flex';
//   headerTitle.style.alignItems = 'center';
//   headerTitle.style.gap = '8px';
  
//   const botIcon = document.createElement('div');
//   botIcon.innerHTML = `
//     <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
//       <path stroke-linecap="round" stroke-linejoin="round" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z"/>
//     </svg>
//   `;
  
//   const titleText = document.createElement('span');
//   titleText.textContent = config.widgetTitle;
//   titleText.style.fontWeight = '600';
//   headerTitle.appendChild(botIcon);
//   headerTitle.appendChild(titleText);
  
//   // Close button
//   const closeButton = document.createElement('button');
//   closeButton.id = 'chatbot-close';
//   closeButton.style.background = 'none';
//   closeButton.style.border = 'none';
//   closeButton.style.color = 'white';
//   closeButton.style.cursor = 'pointer';
//   closeButton.innerHTML = `
//     <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
//       <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/>
//     </svg>
//   `;
//   header.appendChild(headerTitle);
//   header.appendChild(closeButton);
  
//   // Messages container
//   const messages = document.createElement('div');
//   messages.id = 'chatbot-messages';
//   messages.style.flex = '1';
//   messages.style.padding = '16px';
//   messages.style.overflowY = 'auto';
//   messages.style.display = 'flex';
//   messages.style.flexDirection = 'column';
//   messages.style.gap = '12px';
//   messages.style.background = '#f9fafb';
  
//   // Input area
//   const inputArea = document.createElement('div');
//   inputArea.style.padding = '12px 16px';
//   inputArea.style.borderTop = '1px solid #e5e7eb';
//   inputArea.style.display = 'flex';
//   inputArea.style.gap = '8px';
//   inputArea.style.background = 'white';
  
//   const input = document.createElement('input');
//   input.type = 'text';
//   input.placeholder = 'Type your message...';
//   input.style.flex = '1';
//   input.style.padding = '8px 12px';
//   input.style.border = '1px solid #d1d5db';
//   input.style.borderRadius = '9999px';
//   input.style.outline = 'none';
//   input.style.fontSize = '14px';
  
//   const sendButton = document.createElement('button');
//   sendButton.innerHTML = `
//     <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
//       <path stroke-linecap="round" stroke-linejoin="round" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"/>
//     </svg>
//   `;
//   sendButton.style.background = config.primaryColor;
//   sendButton.style.color = 'white';
//   sendButton.style.border = 'none';
//   sendButton.style.borderRadius = '9999px';
//   sendButton.style.width = '36px';
//   sendButton.style.height = '36px';
//   sendButton.style.display = 'flex';
//   sendButton.style.alignItems = 'center';
//   sendButton.style.justifyContent = 'center';
//   sendButton.style.cursor = 'pointer';
//   inputArea.appendChild(input);
//   inputArea.appendChild(sendButton);
  
//   // Toggle button
//   const toggleButton = document.createElement('button');
//   toggleButton.id = 'chatbot-toggle';
//   toggleButton.innerHTML = '💬';
//   toggleButton.style.position = 'fixed';
//   toggleButton.style.bottom = '20px';
//   toggleButton.style[config.position] = '20px';
//   toggleButton.style.width = '60px';
//   toggleButton.style.height = '60px';
//   toggleButton.style.borderRadius = '50%';
//   toggleButton.style.backgroundColor = config.secondaryColor;
//   toggleButton.style.color = 'white';
//   toggleButton.style.border = 'none';
//   toggleButton.style.cursor = 'pointer';
//   toggleButton.style.zIndex = '999999';
//   toggleButton.style.fontSize = '24px';
//   toggleButton.style.display = 'flex';
//   toggleButton.style.alignItems = 'center';
//   toggleButton.style.justifyContent = 'center';
//   toggleButton.style.transition = 'all 0.2s ease';
  
//   // Build widget
//   widget.appendChild(header);
//   widget.appendChild(messages);
//   widget.appendChild(inputArea);
//   document.body.appendChild(widget);
//   document.body.appendChild(toggleButton);
  
//   // 3. Session Management
// // 3. Session Management
// let sessionId = null;
// let chatMessages = [];
// let isLoading = false;
// let isChatVisible = false;

//   // Get or create session ID from API
//   async function getSessionId() {
//     // First check localStorage
//     const storedSessionId = localStorage.getItem('chatbot_session_id');
//     if (storedSessionId) {
//       return storedSessionId;
//     }

//     // If not in localStorage, fetch from API
//     try {
//       const response = await fetch(config.sessionApiUrl, {
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json' }
//       });
      
//       if (!response.ok) throw new Error('Failed to get session ID');
      
//       const data = await response.json();
      
//       if (data.session_id) {
//         // Store the API-provided session ID
//         localStorage.setItem('chatbot_session_id', data.session_id);
//         return data.session_id;
//       } else {
//         throw new Error('No session_id in response');
//       }
//     } catch (error) {
//       console.error('Error getting session ID:', error);
//       // Fallback: generate a local session ID
//       const fallbackId = 'session-' + Math.random().toString(36).substring(2, 15);
//       localStorage.setItem('chatbot_session_id', fallbackId);
//       return fallbackId;
//     }
//   }

//   // Initialize session when widget loads
//   (async function init() {
//     sessionId = await getSessionId();
//     console.log('Initialized with session ID:', sessionId);
//   })();

//   // 4. Chat Functions
//   function toggleChat() {
//     isChatVisible = !isChatVisible;
//     widget.style.display = isChatVisible ? 'flex' : 'none';
//     toggleButton.innerHTML = isChatVisible ? '✕' : '💬';
    
//     if (isChatVisible) {
//       widget.style.animation = 'fadeIn 0.3s ease forwards';
//       setTimeout(() => input.focus(), 300);
//     }
    
//     if (isChatVisible && chatMessages.length === 0) {
//       addMessage(config.welcomeMessage, false);
//     }
//   }

//   function addMessage(text, isUser) {
//     const realTime = new Date().toLocaleString('en-IN', {
//       hour: '2-digit',
//       minute: '2-digit',
//       hour12: true
//     });
    
//     const message = document.createElement('div');
//     message.style.display = 'flex';
//     message.style.flexDirection = 'column';
//     message.style.alignItems = isUser ? 'flex-end' : 'flex-start';
//     message.style.marginBottom = '12px';
    
//     const bubble = document.createElement('div');
//     bubble.style.display = 'flex';
//     bubble.style.alignItems = 'flex-start';
//     bubble.style.gap = '8px';
//     bubble.style.maxWidth = '80%';
    
//     if (!isUser) {
//       const botIcon = document.createElement('div');
//       botIcon.innerHTML = `
//         <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#9ca3af" stroke-width="2">
//           <path stroke-linecap="round" stroke-linejoin="round" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z"/>
//         </svg>
//       `;
//       bubble.appendChild(botIcon);
//     }
    
//     const content = document.createElement('div');
//     content.style.padding = '8px 12px';
//     content.style.borderRadius = isUser ? '12px 12px 0 12px' : '12px 12px 12px 0';
//     content.style.background = isUser ? config.primaryColor : '#f3f4f6';
//     content.style.color = isUser ? 'white' : '#1f2937';
//     content.style.wordBreak = 'break-word';
//     content.textContent = text;
//     bubble.appendChild(content);
    
//     message.appendChild(bubble);
    
//     const meta = document.createElement('div');
//     meta.style.display = 'flex';
//     meta.style.alignItems = 'center';
//     meta.style.gap = '4px';
//     meta.style.marginTop = '4px';
//     meta.style.fontSize = '11px';
//     meta.style.color = '#9ca3af';
    
//     const time = document.createElement('span');
//     time.textContent = realTime;
//     meta.appendChild(time);
    
//     if (isUser) {
//       const userIcon = document.createElement('div');
//       userIcon.innerHTML = `
//         <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="${config.primaryColor}" stroke-width="2">
//           <path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
//         </svg>
//       `;
//       meta.appendChild(userIcon);
//     }
    
//     message.appendChild(meta);
//     messages.appendChild(message);
//     messages.scrollTop = messages.scrollHeight;
    
//     chatMessages.push({
//       text: text,
//       sender: isUser ? 'user' : 'bot',
//       time: realTime
//     });
//   }

//   function showLoading() {
//     const loading = document.createElement('div');
//     loading.id = 'chatbot-loading';
//     loading.style.display = 'flex';
//     loading.style.alignItems = 'center';
//     loading.style.gap = '8px';
//     loading.style.padding = '8px 12px';
//     loading.style.background = '#f3f4f6';
//     loading.style.borderRadius = '12px 12px 12px 0';
//     loading.style.maxWidth = '80px';
//     loading.style.marginBottom = '12px';
    
//     for (let i = 0; i < 3; i++) {
//       const dot = document.createElement('div');
//       dot.style.width = '6px';
//       dot.style.height = '6px';
//       dot.style.background = '#9ca3af';
//       dot.style.borderRadius = '50%';
//       dot.style.animation = `bounce 1s infinite ${i * 0.2}s`;
//       loading.appendChild(dot);
//     }
    
//     messages.appendChild(loading);
//     messages.scrollTop = messages.scrollHeight;
//     return loading;
//   }

//   function hideLoading() {
//     const loading = document.getElementById('chatbot-loading');
//     if (loading) loading.remove();
//   }

//   // 5. API Communication
//   async function sendMessage(messageText) {
//     if (!messageText.trim()) return;
    
//     // Ensure we have a session ID
//     if (!sessionId) {
//       sessionId = await getSessionId();
//       if (!sessionId) {
//         addMessage('Unable to start chat session. Please try again.', false);
//         return;
//       }
//     }
    
//     addMessage(messageText, true);
//     input.value = '';
    
//     const loading = showLoading();
//     isLoading = true;
    
//     try {
//       const response = await fetch(config.apiUrl, {
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json' },
//         body: JSON.stringify({
//           question: messageText,
//           sessionId: sessionId,  // Passing the sessionId to API
//           Store_id: config.storeId
//         })
//       });
      
//       if (!response.ok) throw new Error('API request failed');
      
//       const data = await response.json();
//       let botReply = 'Sorry, I could not understand the response.';
      
//       if (data && Array.isArray(data) && data[0]?.output) {
//         botReply = data[0].output;
//       }
      
//       addMessage(botReply, false);
//     } catch (error) {
//       console.error('Chat error:', error);
//       addMessage("Sorry, I'm having trouble connecting. Please try again later.", false);
//     } finally {
//       hideLoading();
//       isLoading = false;
//     }
//   }

//   // 6. Event Listeners
//   sendButton.addEventListener('click', () => {
//     if (input.value.trim() && !isLoading) sendMessage(input.value);
//   });
  
//   input.addEventListener('keypress', (e) => {
//     if (e.key === 'Enter' && input.value.trim() && !isLoading) sendMessage(input.value);
//   });
  
//   toggleButton.addEventListener('click', toggleChat);
//   closeButton.addEventListener('click', toggleChat);
  
//   // 7. Add animation styles
//   const style = document.createElement('style');
//   style.textContent = `
//     @keyframes bounce {
//       0%, 100% { transform: translateY(0); }
//       50% { transform: translateY(-4px); }
//     }
//     @keyframes fadeIn {
//       from { opacity: 0; transform: translateY(10px); }
//       to { opacity: 1; transform: translateY(0); }
//     }
//     #chatbot-toggle:hover {
//       transform: scale(1.1);
//     }
//   `;
//   document.head.appendChild(style);
  
//   // 8. Initial state
//   widget.style.display = 'none';
//   toggleButton.style.display = 'flex';
// })();

// chatbot-widget.js
(function() {
  // 1. Configuration - Get settings from script attributes
  const currentScript = document.currentScript || 
    Array.from(document.getElementsByTagName('script')).pop();
  
  const config = {
    apiUrl: currentScript.getAttribute('data-api-url') || "https://n8nflow.byteztech.in/webhook/api/ask",
    sessionApiUrl: "http://103.39.131.9:8050/create-session",
    storeId: currentScript.getAttribute('data-store-id') || "116",
    welcomeMessage: currentScript.getAttribute('data-welcome-message') || "Hello! How can I help you today?",
    primaryColor: currentScript.getAttribute('data-primary-color') || "#8B5CF6",
    secondaryColor: currentScript.getAttribute('data-secondary-color') || "#6D28D9",
    widgetTitle: currentScript.getAttribute('data-widget-title') || "AI Assistant",
    position: currentScript.getAttribute('data-position') || "right"
  };

  console.log("apiUrl:", config.apiUrl);
  

  // 2. Check if trainings exist before showing chatbot
  fetch(`${config.apiUrl}/trainlist?store_id=${config.storeId}`)
    .then(res => res.json())
    .then(data => {
      if (data.trainings && data.trainings.length > 0) {
        console.log("Trainings found → showing chatbot");
        initWidget(config);   // init if trainings exist
      } else {
        console.log("No trainings found → chatbot hidden");
      }
    })
    .catch(err => console.error("Error checking trainings:", err));

  // ========= Widget Initializer =========
  function initWidget(config) {
    // 3. Create UI Elements
    const widget = document.createElement('div');
    widget.id = 'shopify-chatbot-widget';
    widget.style.position = 'fixed';
    widget.style.bottom = '20px';
    widget.style[config.position] = '20px';
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
    widget.style.transition = 'all 0.3s ease';

    // Header
    const header = document.createElement('div');
    header.style.display = 'flex';
    header.style.alignItems = 'center';
    header.style.justifyContent = 'space-between';
    header.style.padding = '12px 16px';
    header.style.background = `linear-gradient(to right, ${config.primaryColor}, ${config.secondaryColor})`;
    header.style.color = 'white';
    
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
    titleText.textContent = config.widgetTitle;
    titleText.style.fontWeight = '600';
    headerTitle.appendChild(botIcon);
    headerTitle.appendChild(titleText);

    const closeButton = document.createElement('button');
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
    sendButton.style.background = config.primaryColor;
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
    toggleButton.innerHTML = '💬';
    toggleButton.style.position = 'fixed';
    toggleButton.style.bottom = '20px';
    toggleButton.style[config.position] = '20px';
    toggleButton.style.width = '60px';
    toggleButton.style.height = '60px';
    toggleButton.style.borderRadius = '50%';
    toggleButton.style.backgroundColor = config.secondaryColor;
    toggleButton.style.color = 'white';
    toggleButton.style.border = 'none';
    toggleButton.style.cursor = 'pointer';
    toggleButton.style.zIndex = '999999';
    toggleButton.style.fontSize = '24px';
    toggleButton.style.display = 'flex';
    toggleButton.style.alignItems = 'center';
    toggleButton.style.justifyContent = 'center';
    toggleButton.style.transition = 'all 0.2s ease';

    // Build widget
    widget.appendChild(header);
    widget.appendChild(messages);
    widget.appendChild(inputArea);
    document.body.appendChild(widget);
    document.body.appendChild(toggleButton);

    // ========= Session Management =========
    let sessionId = null;
    let chatMessages = [];
    let isLoading = false;
    let isChatVisible = false;

    async function getSessionId() {
      const storedSessionId = localStorage.getItem('chatbot_session_id');
      if (storedSessionId) return storedSessionId;

      try {
        const response = await fetch(config.sessionApiUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' }
        });
        if (!response.ok) throw new Error('Failed to get session ID');
        const data = await response.json();
        if (data.session_id) {
          localStorage.setItem('chatbot_session_id', data.session_id);
          return data.session_id;
        }
      } catch (error) {
        console.error('Error getting session ID:', error);
      }
      const fallbackId = 'session-' + Math.random().toString(36).substring(2, 15);
      localStorage.setItem('chatbot_session_id', fallbackId);
      return fallbackId;
    }

    (async function init() {
      sessionId = await getSessionId();
      console.log('Initialized with session ID:', sessionId);
    })();

    // ========= Chat Functions =========
    function toggleChat() {
      isChatVisible = !isChatVisible;
      widget.style.display = isChatVisible ? 'flex' : 'none';
      toggleButton.innerHTML = isChatVisible ? '✕' : '💬';
      if (isChatVisible && chatMessages.length === 0) {
        addMessage(config.welcomeMessage, false);
      }
    }

    function addMessage(text, isUser) {
      const realTime = new Date().toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'});
      const message = document.createElement('div');
      message.style.display = 'flex';
      message.style.flexDirection = 'column';
      message.style.alignItems = isUser ? 'flex-end' : 'flex-start';

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
      content.style.borderRadius = isUser ? '12px 12px 0 12px' : '12px 12px 12px 0';
      content.style.background = isUser ? config.primaryColor : '#f3f4f6';
      content.style.color = isUser ? 'white' : '#1f2937';
      content.style.wordBreak = 'break-word';
      content.textContent = text;
      bubble.appendChild(content);

      message.appendChild(bubble);
      messages.appendChild(message);
      messages.scrollTop = messages.scrollHeight;
      chatMessages.push({ text, sender: isUser ? 'user' : 'bot', time: realTime });
    }

    function showLoading() {
      const loading = document.createElement('div');
      loading.id = 'chatbot-loading';
      loading.textContent = '...';
      messages.appendChild(loading);
      messages.scrollTop = messages.scrollHeight;
      return loading;
    }

    function hideLoading() {
      const loading = document.getElementById('chatbot-loading');
      if (loading) loading.remove();
    }

    async function sendMessage(messageText) {
      if (!messageText.trim()) return;
      if (!sessionId) sessionId = await getSessionId();
      addMessage(messageText, true);
      input.value = '';
      const loading = showLoading();
      isLoading = true;
      try {
        const response = await fetch(config.apiUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ question: messageText, sessionId, Store_id: config.storeId })
        });
        const data = await response.json();
        let botReply = data?.[0]?.output || 'Sorry, I could not understand.';
        addMessage(botReply, false);
      } catch (error) {
        addMessage("Sorry, I'm having trouble connecting.", false);
      } finally {
        hideLoading();
        isLoading = false;
      }
    }

    // ========= Event Listeners =========
    sendButton.addEventListener('click', () => {
      if (input.value.trim() && !isLoading) sendMessage(input.value);
    });
    input.addEventListener('keypress', (e) => {
      if (e.key === 'Enter' && input.value.trim() && !isLoading) sendMessage(input.value);
    });
    toggleButton.addEventListener('click', toggleChat);
    closeButton.addEventListener('click', toggleChat);

    // ========= Styles =========
    const style = document.createElement('style');
    style.textContent = `
      @keyframes bounce { 0%,100%{transform:translateY(0);} 50%{transform:translateY(-4px);} }
      @keyframes fadeIn { from{opacity:0;transform:translateY(10px);} to{opacity:1;transform:translateY(0);} }
      #chatbot-toggle:hover { transform: scale(1.1); }
    `;
    document.head.appendChild(style);

    // Initial state
    widget.style.display = 'none';
    toggleButton.style.display = 'flex';
  }
})();
