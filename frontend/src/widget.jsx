import React from 'react';
import ReactDOM from 'react-dom/client';
import Chatbox from './components/Chatbox'; // your existing component

const container = document.createElement('div');
container.id = 'chatbot-root';
document.body.appendChild(container);

const root = ReactDOM.createRoot(container);
root.render(<Chatbox />);

