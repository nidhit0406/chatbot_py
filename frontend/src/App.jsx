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
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const toggleChat = () => {
    setIsChatOpen(!isChatOpen);
  };

  useEffect(() => {
    // Check if this is a Shopify installation request
    const urlParams = new URLSearchParams(window.location.search);
    const shop = urlParams.get('shop');
    const hmac = urlParams.get('hmac');

    if (shop && hmac) {
      console.log('Shopify installation detected - shop:', shop, 'hmac:', hmac);
      setIsShopifyInstall(true);
      setLoading(true);
      
      // Call backend install API with all the query parameters
      handleShopifyInstall();
    } else {
      // Normal session initialization for regular chat usage
      initializeSession();
    }
  }, []);

  const handleShopifyInstall = async () => {
    try {
      setLoading(true);
      setError('');
      
      // Get all query parameters from URL
      const urlParams = new URLSearchParams(window.location.search);
      const params = Object.fromEntries(urlParams.entries());
      
      console.log('Calling backend install with params:', params);
      
      // Use fetch instead of axios to better handle redirects
      const queryString = new URLSearchParams(params).toString();
      const backendUrl = `${import.meta.env.VITE_APP_BACKEND_URL}/install?${queryString}`;
      
      const response = await fetch(backendUrl, {
        method: 'GET',
        redirect: 'manual' // Don't automatically follow redirects
      });

      // Handle redirect responses (302, 301, etc.)
      if (response.status >= 300 && response.status < 400) {
        const redirectUrl = response.headers.get('Location');
        console.log('Redirecting to:', redirectUrl);
        if (redirectUrl) {
          window.location.href = redirectUrl;
          return;
        } else {
          throw new Error('No redirect location found');
        }
      }

      // Handle non-redirect responses
      if (response.ok) {
        const data = await response.json();
        console.log('Backend response:', data);
        
        if (data.redirect_url) {
          window.location.href = data.redirect_url;
        } else {
          throw new Error('No redirect URL in response');
        }
      } else {
        throw new Error(`Backend returned status: ${response.status}`);
      }
      
    } catch (error) {
      console.error('Shopify installation error:', error);
      setError(`Failed to install Shopify app: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  // Alternative approach using iframe for redirects
  const handleShopifyInstallWithIframe = () => {
    const urlParams = new URLSearchParams(window.location.search);
    const queryString = urlParams.toString();
    const backendUrl = `${import.meta.env.VITE_APP_BACKEND_URL}/install?${queryString}`;
    
    // Create a hidden iframe to handle the redirect
    const iframe = document.createElement('iframe');
    iframe.style.display = 'none';
    iframe.src = backendUrl;
    iframe.onload = () => {
      console.log('Iframe loaded, installation should be complete');
      // Check if we're now in the Shopify admin
      if (window.location.href.includes('admin.shopify.com')) {
        console.log('Successfully redirected to Shopify admin');
      } else {
        setError('Installation may have completed. Please check your Shopify admin.');
      }
    };
    iframe.onerror = () => {
      setError('Failed to load installation iframe');
    };
    
    document.body.appendChild(iframe);
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
        } else {
          console.warn('No session_id in response');
        }
      } catch (error) {
        console.error('Error fetching session_id:', error);
      }
    }
  };

  // Show loading/error state during Shopify installation
  if (isShopifyInstall) {
    return (
      <div className="w-screen h-screen flex justify-center items-center bg-gray-100">
        <div className="text-center p-8 bg-white rounded-lg shadow-md max-w-md">
          {loading && (
            <>
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-500 mx-auto mb-4"></div>
              <h2 className="text-xl font-semibold text-gray-800 mb-2">Installing Shopify App</h2>
              <p className="text-gray-600">Redirecting to Shopify for authentication...</p>
              <p className="text-sm text-gray-500 mt-2">
                If you're not redirected automatically, check your popup blocker.
              </p>
            </>
          )}
          
          {error && (
            <>
              <div className="text-red-500 text-4xl mb-4">⚠️</div>
              <h2 className="text-xl font-semibold text-red-800 mb-2">Installation Issue</h2>
              <p className="text-red-600 mb-4">{error}</p>
              
              <div className="space-y-2">
                <button
                  onClick={handleShopifyInstall}
                  className="w-full bg-purple-500 hover:bg-purple-600 text-white px-6 py-2 rounded-lg font-medium"
                >
                  Try Again (Fetch API)
                </button>
                
                <button
                  onClick={handleShopifyInstallWithIframe}
                  className="w-full bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded-lg font-medium"
                >
                  Try Again (Iframe Method)
                </button>
                
                <button
                  onClick={() => {
                    // Direct browser redirect as fallback
                    const urlParams = new URLSearchParams(window.location.search);
                    const queryString = urlParams.toString();
                    window.location.href = `${import.meta.env.VITE_APP_BACKEND_URL}/install?${queryString}`;
                  }}
                  className="w-full bg-green-500 hover:bg-green-600 text-white px-6 py-2 rounded-lg font-medium"
                >
                  Direct Redirect
                </button>
              </div>
              
              <p className="text-sm text-gray-500 mt-4">
                If issues persist, try installing directly from your Shopify admin.
              </p>
            </>
          )}
        </div>
      </div>
    );
  }

  // Normal chat app interface
  return (
    <div className="w-screen h-screen flex justify-center items-center bg-gray-100">
      {/* WeChat Icon */}
      {!isChatOpen && (
        <button
          onClick={toggleChat}
          className="fixed bottom-5 right-5 bg-purple-500 hover:bg-purple-600 text-white p-4 rounded-full shadow-lg transition-colors duration-200"
        >
          <SiWechat className="text-2xl" />
        </button>
      )}

      {/* Chatbox */}
      {isChatOpen && (
        <div className="w-[90%] max-w-md fixed bottom-5 right-5 flex flex-col items-end">
          <Chatbox />
          <button
            onClick={toggleChat}
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