import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';

// Create a container for the chatbot
const chatContainer = document.createElement('div');
chatContainer.id = 'shopify-chatbot';
document.body.appendChild(chatContainer);

// Render the App component
const root = createRoot(chatContainer);
root.render(<App />);