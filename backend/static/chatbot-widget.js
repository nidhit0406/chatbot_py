(function () {
  (async function () {
    const currentScript =
      document.currentScript ||
      Array.from(document.getElementsByTagName("script")).pop();

    let store = currentScript.getAttribute("data-store-id");
    if (!store) {
      console.warn(
        "⚠️ data-store-id attribute is missing. Using hostname as store..."
      );
      store =
        window.location.hostname.replace(".myshopify.com", "") ||
        "unknown-shop";
      console.log("✅ Set store to:", store);
    }

    const config = {
      apiUrl:
        currentScript.getAttribute("data-api-url") ||
        "https://n8nflow.byteztech.in/webhook/api/ask",
      sessionApiUrl: "http://103.39.131.9:8050/create-session",
      store: store,
      welcomeMessage:
        currentScript.getAttribute("data-welcome-message") ||
        "Hello! How can I help you today?",
      primaryColor:
        currentScript.getAttribute("data-primary-color") || "#8B5CF6",
      secondaryColor:
        currentScript.getAttribute("data-secondary-color") || "#6D28D9",
      widgetTitle:
        currentScript.getAttribute("data-widget-title") || "AI Assistant",
      position: currentScript.getAttribute("data-position") || "right",
    };

    let storeIdFromApi = null;
    let clientIdFromApi = null;
    let clientEmailFromApi = null;

    // async function fetchTrainings() {
    //   try {
    //     console.log("Fetching trainings for store:", config.store);
    //     const res = await fetch(`https://chatbot-bpy.clustersofttech.com/trainlist?domain=${encodeURIComponent(config.store)}`);
    //     const data = await res.json();
    //     console.log("✅ Trainings fetched for store:", config.store, data);
    //     if (data.state && data.state.storeExists) {
    //       storeIdFromApi = data.store.store_id;
    //       clientIdFromApi = data.client_id;
    //       clientEmailFromApi = data.email;
    //     } else if (data.state && data.state.clientExists) {
    //       clientIdFromApi = data.client_id;
    //       clientEmailFromApi = data.email;
    //     }
    //     return data;
    //   } catch (err) {
    //     console.error("❌ Error fetching trainings for store:", config.store, err);
    //     return { state: { storeExists: false, clientExists: false, hasTrainings: false } };
    //   }
    // }

    async function fetchTrainings() {
      try {
        console.log("Fetching trainings for store:", config.store);
        const res = await fetch(
          // `https://chatbot-bpy.clustersofttech.com/trainlist?domain=${encodeURIComponent(config.store)}`
          `http://127.0.0.1:5000/trainlist?domain=${encodeURIComponent(
            config.store
          )}`
        );
        const data = await res.json();

        console.log("✅ Trainings fetched for store:", config.store, data);

        // Extract values safely
        storeIdFromApi = data?.store?.store_id || null;
        clientIdFromApi = data?.client_id || null;
        clientEmailFromApi = data?.email || null;

        console.log(
          "Extracted values - storeIdFromApi:",
          storeIdFromApi,
          "clientIdFromApi:",
          clientIdFromApi,
          "clientEmailFromApi:",
          clientEmailFromApi
        );

        return data;
      } catch (err) {
        console.error(
          "❌ Error fetching trainings for store:",
          config.store,
          err
        );
        return {
          state: {
            storeExists: false,
            clientExists: false,
            hasTrainings: false,
          },
        };
      }
    }

    // Call fetchTrainings exactly once
    const trainingsData = await fetchTrainings();

    // Handle navigation and client management based on state
    // if (trainingsData.state.storeExists && trainingsData.state.hasTrainings) {
    //   console.log("✅ Trainings found for store:", config.store, "→ Initializing widget with client_id:", clientIdFromApi);
    //   initWidget(config, clientIdFromApi);
    // } else if (trainingsData.state.clientExists) {
    //   console.log("⚠️ Client exists but no store/trainings, redirecting to login with prefilled email:", clientEmailFromApi);
    //   window.location.href = `http://localhost:3000/login?store=${encodeURIComponent(config.store)}&email=${encodeURIComponent(clientEmailFromApi || '')}`;
    // } else {
    //   console.log("⚠️ No client/store, redirecting to sign-up for store:", config.store);
    //   window.location.href = `http://localhost:3000/login?store=${encodeURIComponent(config.store)}`;
    // }

    if (trainingsData.state.storeExists && trainingsData.state.hasTrainings) {
      // ✅ Case 1: Store & Trainings exist → init widget
      console.log(
        "✅ Trainings found for store:",
        config.store,
        "→ Initializing widget with client_id:",
        clientIdFromApi
      );
      initWidget(config, clientIdFromApi);
    } else if (
      trainingsData.state.storeExists &&
      !trainingsData.state.clientExists
    ) {
      // ⚠️ Case 2: Store exists but NO trainings → redirect with store+email
      window.location.href = `http://localhost:3000/login?store=${encodeURIComponent(
        config.store
      )}`;
    } else if (trainingsData.state.clientExists) {
      // ⚠️ Case 3: Client exists but no store → redirect with store+email
      window.location.href =
        `http://localhost:3000/login?store=${encodeURIComponent(
          config.store
        )}` +
        ((clientEmailFromApi && clientIdFromApi)
          ? `&email=${encodeURIComponent(clientEmailFromApi)}&client_id=${encodeURIComponent(clientIdFromApi)}`
          : "");
    } else {
      // ⚠️ Case 4: Neither store nor client exist → redirect with only store
      window.location.href = `http://localhost:3000/login?store=${encodeURIComponent(
        config.store
      )}`;
    }
  })();

  async function addShopifyStoreAndRedirect(
    url,
    status,
    clientId,
    redirectUrl
  ) {
    console.log("Adding Shopify store:", url, status, clientId, redirectUrl);

    try {
      const response = await fetch(
        "https://chatbot-bpy.clustersofttech.com/shopify-store",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            url: url,
            status: status,
            client_id: clientId,
          }),
        }
      );

      const data = await response.json();
      if (response.ok) {
        console.log("Store saved:", data);
        window.location.href = redirectUrl;
      } else {
        alert("Error: " + (data.message || "Failed to add store"));
        window.location.href = redirectUrl;
      }
    } catch (err) {
      console.error("Error calling API:", err);
      alert("Something went wrong!");
      window.location.href = redirectUrl;
    }
  }

  function initWidget(config) {
    const widget = document.createElement("div");
    widget.id = "shopify-chatbot-widget";
    widget.style.position = "fixed";
    widget.style.bottom = "20px";
    widget.style[config.position] = "20px";
    widget.style.width = "450px";
    widget.style.height = "550px";
    widget.style.backgroundColor = "white";
    widget.style.borderRadius = "12px";
    widget.style.boxShadow = "0 5px 15px rgba(0,0,0,0.2)";
    widget.style.zIndex = "999999";
    widget.style.display = "none";
    widget.style.flexDirection = "column";
    widget.style.overflow = "hidden";
    widget.style.fontFamily = "system-ui, -apple-system, sans-serif";
    widget.style.transition = "all 0.3s ease";

    const header = document.createElement("div");
    header.style.display = "flex";
    header.style.alignItems = "center";
    header.style.justifyContent = "space-between";
    header.style.padding = "12px 16px";
    header.style.background = `linear-gradient(to right, ${config.primaryColor}, ${config.secondaryColor})`;
    header.style.color = "white";

    const headerTitle = document.createElement("div");
    headerTitle.style.display = "flex";
    headerTitle.style.alignItems = "center";
    headerTitle.style.gap = "8px";

    const botIcon = document.createElement("div");
    botIcon.innerHTML = `
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path stroke-linecap="round" stroke-linejoin="round" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z"/>
      </svg>
    `;
    const titleText = document.createElement("span");
    titleText.textContent = config.widgetTitle;
    titleText.style.fontWeight = "600";
    headerTitle.appendChild(botIcon);
    headerTitle.appendChild(titleText);

    const closeButton = document.createElement("button");
    closeButton.style.background = "none";
    closeButton.style.border = "none";
    closeButton.style.color = "white";
    closeButton.style.cursor = "pointer";
    closeButton.innerHTML = `
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/>
      </svg>
    `;
    header.appendChild(headerTitle);
    header.appendChild(closeButton);

    const messages = document.createElement("div");
    messages.id = "chatbot-messages";
    messages.style.flex = "1";
    messages.style.padding = "16px";
    messages.style.overflowY = "auto";
    messages.style.display = "flex";
    messages.style.flexDirection = "column";
    messages.style.gap = "12px";
    messages.style.background = "#f9fafb";

    const inputArea = document.createElement("div");
    inputArea.style.padding = "12px 16px";
    inputArea.style.borderTop = "1px solid #e5e7eb";
    inputArea.style.display = "flex";
    inputArea.style.gap = "8px";
    inputArea.style.background = "white";

    const input = document.createElement("input");
    input.type = "text";
    input.placeholder = "Type your message...";
    input.style.flex = "1";
    input.style.padding = "8px 12px";
    input.style.border = "1px solid #d1d5db";
    input.style.borderRadius = "9999px";
    input.style.outline = "none";
    input.style.fontSize = "14px";

    const sendButton = document.createElement("button");
    sendButton.innerHTML = `
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path stroke-linecap="round" stroke-linejoin="round" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"/>
      </svg>
    `;
    sendButton.style.background = config.primaryColor;
    sendButton.style.color = "white";
    sendButton.style.border = "none";
    sendButton.style.borderRadius = "9999px";
    sendButton.style.width = "36px";
    sendButton.style.height = "36px";
    sendButton.style.display = "flex";
    sendButton.style.alignItems = "center";
    sendButton.style.justifyContent = "center";
    sendButton.style.cursor = "pointer";
    inputArea.appendChild(input);
    inputArea.appendChild(sendButton);

    const toggleButton = document.createElement("button");
    toggleButton.innerHTML = "💬";
    toggleButton.style.position = "fixed";
    toggleButton.style.bottom = "20px";
    toggleButton.style[config.position] = "20px";
    toggleButton.style.width = "60px";
    toggleButton.style.height = "60px";
    toggleButton.style.borderRadius = "50%";
    toggleButton.style.backgroundColor = config.secondaryColor;
    toggleButton.style.color = "white";
    toggleButton.style.border = "none";
    toggleButton.style.cursor = "pointer";
    toggleButton.style.zIndex = "999999";
    toggleButton.style.fontSize = "24px";
    toggleButton.style.display = "flex";
    toggleButton.style.alignItems = "center";
    toggleButton.style.justifyContent = "center";
    toggleButton.style.transition = "all 0.2s ease";

    widget.appendChild(header);
    widget.appendChild(messages);
    widget.appendChild(inputArea);
    document.body.appendChild(widget);
    document.body.appendChild(toggleButton);

    let sessionId = null;
    let chatMessages = [];
    let isLoading = false;
    let isChatVisible = false;

    async function getSessionId() {
      const storedSessionId = localStorage.getItem("chatbot_session_id");
      if (storedSessionId) return storedSessionId;

      try {
        const response = await fetch(config.sessionApiUrl, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
        });
        if (!response.ok) throw new Error("Failed to get session ID");
        const data = await response.json();
        if (data.session_id) {
          localStorage.setItem("chatbot_session_id", data.session_id);
          return data.session_id;
        }
      } catch (error) {
        console.error("Error getting session ID:", error);
      }
      const fallbackId =
        "session-" + Math.random().toString(36).substring(2, 15);
      localStorage.setItem("chatbot_session_id", fallbackId);
      return fallbackId;
    }

    (async function init() {
      sessionId = await getSessionId();
      console.log("Initialized with session ID:", sessionId);
    })();

    function toggleChat() {
      isChatVisible = !isChatVisible;
      widget.style.display = isChatVisible ? "flex" : "none";
      toggleButton.innerHTML = isChatVisible ? "✕" : "💬";
      if (isChatVisible && chatMessages.length === 0) {
        addMessage(config.welcomeMessage, false);
      }
    }

    function addMessage(text, isUser) {
      const realTime = new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      });
      const message = document.createElement("div");
      message.style.display = "flex";
      message.style.flexDirection = "column";
      message.style.alignItems = isUser ? "flex-end" : "flex-start";

      const bubble = document.createElement("div");
      bubble.style.display = "flex";
      bubble.style.alignItems = "flex-start";
      bubble.style.gap = "8px";
      bubble.style.maxWidth = "90%";

      if (!isUser) {
        const botIcon = document.createElement("div");
        botIcon.innerHTML = `
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#9ca3af" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z"/>
          </svg>
        `;
        bubble.appendChild(botIcon);
      }

      const content = document.createElement("div");
      content.style.padding = "8px 12px";
      content.style.borderRadius = isUser
        ? "12px 12px 0 12px"
        : "12px 12px 12px 0";
      content.style.background = isUser ? config.primaryColor : "#f3f4f6";
      content.style.color = isUser ? "white" : "#1f2937";
      content.style.wordBreak = "break-word";
      content.textContent = text;
      bubble.appendChild(content);

      message.appendChild(bubble);
      messages.appendChild(message);
      messages.scrollTop = messages.scrollHeight;
      chatMessages.push({
        text,
        sender: isUser ? "user" : "bot",
        time: realTime,
      });
    }

    function showLoading() {
      const loading = document.createElement("div");
      loading.id = "chatbot-loading";
      loading.textContent = "...";
      messages.appendChild(loading);
      messages.scrollTop = messages.scrollHeight;
      return loading;
    }

    function hideLoading() {
      const loading = document.getElementById("chatbot-loading");
      if (loading) loading.remove();
    }

    async function sendMessage(messageText) {
      if (!messageText.trim()) return;
      if (!sessionId) sessionId = await getSessionId();
      addMessage(messageText, true);
      input.value = "";
      const loading = showLoading();
      isLoading = true;
      try {
        const response = await fetch(config.apiUrl, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            question: messageText,
            sessionId,
            store_id: storeIdFromApi || config.store,
          }),
        });
        const data = await response.json();
        let botReply = data?.[0]?.output || "Sorry, I could not understand.";
        addMessage(botReply, false);
      } catch (error) {
        addMessage("Sorry, I'm having trouble connecting.", false);
      } finally {
        hideLoading();
        isLoading = false;
      }
    }

    sendButton.addEventListener("click", () => {
      if (input.value.trim() && !isLoading) sendMessage(input.value);
    });
    input.addEventListener("keypress", (e) => {
      if (e.key === "Enter" && input.value.trim() && !isLoading)
        sendMessage(input.value);
    });
    toggleButton.addEventListener("click", toggleChat);
    closeButton.addEventListener("click", toggleChat);

    const style = document.createElement("style");
    style.textContent = `
      @keyframes bounce { 0%,100%{transform:translateY(0);} 50%{transform:translateY(-4px);} }
      @keyframes fadeIn { from{opacity:0;transform:translateY(10px);} to{opacity:1;transform:translateY(0);} }
      #chatbot-toggle:hover { transform: scale(1.1); }
    `;
    document.head.appendChild(style);

    widget.style.display = "none";
    toggleButton.style.display = "flex";
  }
})();
