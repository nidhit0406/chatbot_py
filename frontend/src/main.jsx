// import { StrictMode } from 'react'
// import { createRoot } from 'react-dom/client'
// import './index.css'
// import App from './App.jsx'
// import { BrowserRouter } from 'react-router-dom'

// const host = new URLSearchParams(window.location.search).get('host');

// const config = {
//   apiKey: import.meta.env.VITE_SHOPIFY_API_KEY,
//   host,
//   forceRedirect: true,
// };
// console.log('Shopify config:', config);


// createRoot(document.getElementById('root')).render(
//   <StrictMode>
//     <BrowserRouter config={config}><App /></BrowserRouter>
//   </StrictMode>,
// )
import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';
import './index.css';

// ID MUST match loader.js
const rootId = 'chatbot-widget-container'; 

// Only initialize if not already loaded
if (!document.getElementById(rootId)) {
  const container = document.createElement('div');
  container.id = rootId;
  document.body.appendChild(container);
}

// Mount React
const container = document.getElementById(rootId);
if (container) {
  createRoot(container).render(
    <React.StrictMode>
      <App />
    </React.StrictMode>
  );
}
