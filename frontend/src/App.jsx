// import { useEffect, useState } from 'react';
// import { SiWechat } from 'react-icons/si';
// import Chatbox from './components/Chatbox';
// import { PiChatCircleSlashFill } from "react-icons/pi";
// import axios from 'axios';

// function App() {
//   const [isChatOpen, setIsChatOpen] = useState(false);

//   const toggleChat = () => {
//     setIsChatOpen(!isChatOpen);
//   };

//        const [sessionId, setSessionId] = useState('');
// console.log(sessionId, "sessionId");  
//     useEffect(() => {
//         console.log('sessionId changed');

//   const getSessionId = async () => {
//     let storedSessionId = localStorage.getItem('session_id');
//     if (storedSessionId) {
//       setSessionId(storedSessionId);
//     } else {
//       try {
//         const response = await axios.post(`${import.meta.env.VITE_APP_API_URL}/create-session`, {}, {
//           headers: { 'Content-Type': 'application/json' },
//         });
//         const data = response.data;
//         console.log(data, "data");

//         if (data.session_id) {
//           localStorage.setItem('session_id', data.session_id);
//           setSessionId(data.session_id);
//         } else {
//           console.warn('No session_id in response');
//         //   addMessage('Failed to initialize session. Please try again.', 'error');
//         }
//       } catch (error) {
//         console.error('Error fetching session_id:', error);
//         // addMessage('Unable to connect to session service. Please try again later.', 'error');
//       }
//     }
//   };

//   getSessionId();
// }, []);

// import { useEffect, useState } from 'react';
// import { SiWechat } from 'react-icons/si';
// import Chatbox from './components/Chatbox';
// import { PiChatCircleSlashFill } from "react-icons/pi";
// import axios from 'axios';

// function App() {
//   const [isChatOpen, setIsChatOpen] = useState(false);
//   const [isIframe, setIsIframe] = useState(false);

//   // Detect if we're running in an iframe
//   useEffect(() => {
//     setIsIframe(window.self !== window.top);
//   }, []);

//   const toggleChat = () => {
//     setIsChatOpen(!isChatOpen);
//   };

//   // Only initialize session if not in iframe
//   const [sessionId, setSessionId] = useState('');
//   useEffect(() => {
//     if (!isIframe) {
//       const getSessionId = async () => {
//         let storedSessionId = localStorage.getItem('session_id');
//         if (storedSessionId) {
//           setSessionId(storedSessionId);
//         } else {
//           try {
//             const response = await axios.post(`${import.meta.env.VITE_APP_API_URL}/create-session`, {}, {
//               headers: { 'Content-Type': 'application/json' },
//             });
//             if (response.data.session_id) {
//               localStorage.setItem('session_id', response.data.session_id);
//               setSessionId(response.data.session_id);
//             }
//           } catch (error) {
//             console.error('Error fetching session_id:', error);
//           }
//         }
//       };
//       getSessionId();
//     }
//   }, [isIframe]);

//   // Adjust styles based on iframe context
//   const containerStyles = isIframe ? {
//     width: '100%',
//     height: '100%',
//     justifyContent: 'flex-end',
//     alignItems: 'flex-end',
//     backgroundColor: 'transparent'
//   } : {
//     width: '100vw',
//     height: '100vh',
//     justifyContent: 'center',
//     alignItems: 'center',
//     backgroundColor: '#f3f4f6'
//   };

//   return (
//     <div style={containerStyles} className="flex">
//       {/* Only show toggle button when not in iframe */}
//       {!isIframe && !isChatOpen && (
//         <button
//           onClick={toggleChat}
//           className="fixed bottom-5 right-5 bg-purple-500 hover:bg-purple-600 text-white p-4 rounded-full shadow-lg transition-colors duration-200"
//         >
//           <SiWechat className="text-2xl" />
//         </button>
//       )}

//       {/* Chatbox - always visible in iframe, toggleable when standalone */}
//       {(isIframe || isChatOpen) && (
//         <div className={`${isIframe ? 'w-full h-full' : 'w-[90%] max-w-md fixed bottom-5 right-5'} flex flex-col items-end`}>
//           <Chatbox isIframe={isIframe} />
//           {!isIframe && (
//             <button
//               onClick={toggleChat}
//               className="mt-2 bg-red-500 hover:bg-red-600 text-white p-2 rounded-full shadow-lg transition-colors duration-200"
//             >
//               <PiChatCircleSlashFill />
//             </button>
//           )}
//         </div>
//       )}
//     </div>
//   );
// }
// export default App;



// import { useEffect, useState } from 'react';
// import { SiWechat } from 'react-icons/si';
// import Chatbox from './components/Chatbox';
// import { PiChatCircleSlashFill } from "react-icons/pi";
// import axios from 'axios';

// function App() {
//   const [isChatOpen, setIsChatOpen] = useState(false);

//   const toggleChat = () => {
//     setIsChatOpen(!isChatOpen);
//   };

//   const [sessionId, setSessionId] = useState('');
//   console.log(sessionId, "sessionId");
//   useEffect(() => {
//     console.log('sessionId changed');
//     const getSessionId = async () => {
//       let storedSessionId = localStorage.getItem('session_id');
//       if (storedSessionId) {
//         setSessionId(storedSessionId);
//       } else {
//         try {
//           const response = await axios.post(`${import.meta.env.VITE_APP_API_URL}/create-session`, {}, {
//             headers: { 'Content-Type': 'application/json' },
//           });
//           const data = response.data;
//           console.log(data, "data");

//           if (data.session_id) {
//             localStorage.setItem('session_id', data.session_id);
//             setSessionId(data.session_id);
//           } else {
//             console.warn('No session_id in response');
//             //   addMessage('Failed to initialize session. Please try again.', 'error');
//           }
//         } catch (error) {
//           console.error('Error fetching session_id:', error);
//           // addMessage('Unable to connect to session service. Please try again later.', 'error');
//         }
//       }
//     };

//     getSessionId();
//   }, []);


//   return (
//     <div className="w-screen h-screen flex justify-center items-center bg-gray-100">
//       {/* WeChat Icon */}
//       {!isChatOpen && (
//         <button
//           onClick={toggleChat}
//           className="fixed bottom-5 right-5 bg-purple-500 hover:bg-purple-600 text-white p-4 rounded-full shadow-lg transition-colors duration-200"
//         >
//           <SiWechat className="text-2xl" />
//         </button>
//       )}

//       {/* Chatbox */}
//       {isChatOpen && (
//         <div className="w-[90%] max-w-md fixed bottom-5 right-5 flex flex-col items-end">
//           <Chatbox />
//           <button
//             onClick={toggleChat}
//             className="mt-2 bg-red-500 hover:bg-red-600 text-white p-2 rounded-full shadow-lg transition-colors duration-200"
//           >
//             <PiChatCircleSlashFill />
//           </button>
//         </div>
//       )}
//     </div>
//   );
// }

// export default App;

import { useEffect, useState } from 'react';
import { SiWechat } from 'react-icons/si';
import Chatbox from './components/Chatbox';
import { PiChatCircleSlashFill } from "react-icons/pi";
import axios from 'axios';

function App() {
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [sessionId, setSessionId] = useState('');
  const [isShopifyInstall, setIsShopifyInstall] = useState(false);
  const [isEmbedded, setIsEmbedded] = useState(false);
  const [loading, setLoading] = useState(false);
  const [shopName, setShopName] = useState('');

  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const shop = urlParams.get('shop');
    const hmac = urlParams.get('hmac');
    const embedded = urlParams.get('embedded');
    
    // Check if embedded in Shopify Admin
    if (embedded === 'true' && shop) {
      console.log('Running in Shopify Admin embedded mode');
      setIsEmbedded(true);
      setIsChatOpen(true);
      setShopName(shop.replace('.myshopify.com', ''));
      return;
    }

    // Check localStorage for embedded flag (from redirect)
    const storedEmbedded = localStorage.getItem('shopify_embedded');
    const storedShop = localStorage.getItem('shopify_shop');
    if (storedEmbedded === 'true' && storedShop) {
      console.log('Running in embedded mode from localStorage');
      setIsEmbedded(true);
      setIsChatOpen(true);
      setShopName(storedShop.replace('.myshopify.com', ''));
      // Clear the stored values
      localStorage.removeItem('shopify_embedded');
      localStorage.removeItem('shopify_shop');
      localStorage.removeItem('shopify_host');
      return;
    }

    // Check if Shopify installation request
    if (shop && hmac) {
      console.log('Shopify installation detected');
      setIsShopifyInstall(true);
      setLoading(true);
      handleDirectRedirect();
    } else {
      initializeSession();
    }
  }, []);

  const handleDirectRedirect = () => {
    const urlParams = new URLSearchParams(window.location.search);
    const queryString = urlParams.toString();
    window.location.href = `${import.meta.env.VITE_APP_BACKEND_URL}/install?${queryString}`;
  };

  const initializeSession = async () => {
    console.log('Initializing normal chat session');
    let storedSessionId = localStorage.getItem('session_id');
    if (storedSessionId) {
      setSessionId(storedSessionId);
    } else {
      try {
        const response = await axios.post(`${import.meta.env.VITE_APP_API_URL}/create-session`, {}, {
          headers: { 'Content-Type': 'application/json' },
        });
        const data = response.data;

        if (data.session_id) {
          localStorage.setItem('session_id', data.session_id);
          setSessionId(data.session_id);
        }
      } catch (error) {
        console.error('Error fetching session_id:', error);
      }
    }
  };

  // Embedded mode in Shopify Admin
  if (isEmbedded) {
    return (
      <div style={{ 
        padding: '20px', 
        height: '100vh', 
        background: '#f9fafb',
        fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
      }}>
        <div style={{ 
          background: 'white', 
          borderRadius: '8px', 
          padding: '20px', 
          boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
          marginBottom: '20px'
        }}>
          <h2 style={{ margin: '0 0 10px 0', color: '#333' }}>🤖 AI Chatbot</h2>
          <p style={{ margin: 0, color: '#666', fontSize: '14px' }}>
            Welcome to your store's AI assistant{shopName ? ` for ${shopName}` : ''}
          </p>
        </div>
        <Chatbox embedded={true} />
      </div>
    );
  }

  // Shopify Installation Flow
  if (isShopifyInstall) {
    return (
      <div className="w-screen h-screen flex justify-center items-center bg-gray-100">
        <div className="text-center p-8 bg-white rounded-lg shadow-md max-w-md">
          {loading && (
            <>
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-500 mx-auto mb-4"></div>
              <h2 className="text-xl font-semibold text-gray-800 mb-2">Installing Shopify App</h2>
              <p className="text-gray-600">Redirecting to installation...</p>
            </>
          )}
        </div>
      </div>
    );
  }

  // Standalone Chat App
  return (
    <div className="w-screen h-screen flex justify-center items-center bg-gray-100">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-800 mb-4">🤖 AI Chatbot</h1>
        <p className="text-gray-600">Open the chat widget to start conversation</p>
      </div>

      {!isChatOpen && (
        <button
          onClick={() => setIsChatOpen(true)}
          className="fixed bottom-5 right-5 bg-purple-500 hover:bg-purple-600 text-white p-4 rounded-full shadow-lg transition-colors duration-200"
        >
          <SiWechat className="text-2xl" />
        </button>
      )}

      {isChatOpen && (
        <div className="w-[90%] max-w-md fixed bottom-5 right-5 flex flex-col items-end">
          <Chatbox />
          <button
            onClick={() => setIsChatOpen(false)}
            className="mt-2 bg-red-500 hover:bg-red-600 text-white p-2 rounded-full shadow-lg transition-colors duration-200"
          >
            <PiChatCircleSlashFill />
          </button>
        </div>
      )}
    </div>
  );
}

export default App;

// import { useState } from 'react';
// import { SiWechat } from 'react-icons/si';
// import Chatbox from './components/Chatbox';
// import { PiChatCircleSlashFill } from "react-icons/pi";

// function App() {
//   const [isChatOpen, setIsChatOpen] = useState(false);

//   const toggleChat = () => {
//     setIsChatOpen(!isChatOpen);
//   };

//   return (
//     <div className="w-screen h-screen flex justify-center items-center bg-gray-100">
//       {!isChatOpen && (
//         <button
//           onClick={toggleChat}
//           className="fixed bottom-5 right-5 bg-purple-500 hover:bg-purple-600 text-white p-4 rounded-full shadow-lg transition-colors duration-200"
//         >
//           <SiWechat className="text-2xl" />
//         </button>
//       )}

//       {isChatOpen && (
//         <div className="w-[90%] max-w-md fixed bottom-5 right-5 flex flex-col items-end">
//           <Chatbox />
//           <button
//             onClick={toggleChat}
//             className="mt-2 bg-red-500 hover:bg-red-600 text-white p-2 rounded-full shadow-lg transition-colors duration-200"
//           >
//             <PiChatCircleSlashFill />
//           </button>
//         </div>
//       )}
//     </div>
//   );
// }

// export default App;