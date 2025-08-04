(function () {
  // Inject CSS
  const link = document.createElement('link');
  link.rel = 'stylesheet';
  link.href = 'https://chatbot-py-virid.vercel.app/chatbot-widget.css';
  document.head.appendChild(link);

  // Inject container
  const container = document.createElement('div');
  container.id = 'chatbot-widget-container';
  document.body.appendChild(container);

  // Inject JS
  const script = document.createElement('script');
  script.src = 'https://chatbot-py-virid.vercel.app/chatbot-widget.iife.js';
  script.defer = true;
  document.body.appendChild(script);
})();
