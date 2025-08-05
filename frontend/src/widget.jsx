// // widget.jsx
// import React from 'react';
// import ReactDOM from 'react-dom/client';
// import Chatbox from './components/Chatbox';

// (function () {
//   const container = document.createElement('div');
//   container.id = 'chatbot-root';
//   document.body.appendChild(container);

//   const backendUrl = 'https://chatbot-bpy.clustersofttech.com'; // Adjust for production
//   const root = ReactDOM.createRoot(container);
//   root.render(React.createElement(Chatbox, { backendUrl }));
// })();

import React from 'react';
import ReactDOM from 'react-dom/client';
import ChatBox from './components/Chatbox';

(function () {
    const container = document.getElementById('chatbot-root');
    if (container) {
        const root = ReactDOM.createRoot(container);
        root.render(<ChatBox />);
    }
})();