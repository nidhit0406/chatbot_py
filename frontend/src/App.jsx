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



import { useEffect, useState } from 'react';
import { SiWechat } from 'react-icons/si';
import Chatbox from './components/Chatbox';
import { PiChatCircleSlashFill } from "react-icons/pi";
import axios from 'axios';

function App() {
  const [isChatOpen, setIsChatOpen] = useState(false);

  const toggleChat = () => {
    setIsChatOpen(!isChatOpen);
  };

  const [sessionId, setSessionId] = useState('');
  console.log(sessionId, "sessionId");
  useEffect(() => {

    // const urlParams = new URLSearchParams(window.location.search);
    // const shop = urlParams.get('shop');
    // const hmac = urlParams.get('hmac');

    // if (shop && hmac) {
    //   console.log('shopify installation detected');
      
    //   // Redirect to backend install API
    //   const queryString = urlParams.toString();
    //   window.location.href = `${import.meta.env.VITE_APP_BACKEND_URL}/install?${queryString}`;
    //   return; // Exit early to prevent further execution
    // }

    const urlParams = new URLSearchParams(window.location.search);
    const shop = urlParams.get('shop');
    const hmac = urlParams.get('hmac');

    if (shop && hmac) {
      console.log('shopify installation detected');
      // Instead of direct redirect, send a message to the parent window or handle via backend
      if (window.parent) {
        window.parent.postMessage({ type: 'shopifyInstall', shop, hmac }, '*');
      }
      return; // Exit early if Shopify installation is detected
    }

    console.log('sessionId changed');
    const getSessionId = async () => {
      let storedSessionId = localStorage.getItem('session_id');
      if (storedSessionId) {
        setSessionId(storedSessionId);
      } else {
        try {
          const response = await axios.post(`${import.meta.env.VITE_APP_API_URL}/create-session`, {}, {
            headers: { 'Content-Type': 'application/json' },
          });
          const data = response.data;
          console.log(data, "data");

          if (data.session_id) {
            localStorage.setItem('session_id', data.session_id);
            setSessionId(data.session_id);
          } else {
            console.warn('No session_id in response');
            //   addMessage('Failed to initialize session. Please try again.', 'error');
          }
        } catch (error) {
          console.error('Error fetching session_id:', error);
          // addMessage('Unable to connect to session service. Please try again later.', 'error');
        }
      }
    };

    getSessionId();
  }, []);


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

// import { useEffect, useState } from 'react';
// import { SiWechat } from 'react-icons/si';
// import Chatbox from './components/Chatbox';
// import { PiChatCircleSlashFill } from "react-icons/pi";
// import axios from 'axios';

// function App() {
//   const [isChatOpen, setIsChatOpen] = useState(false);
//   const [sessionId, setSessionId] = useState('');

//   const toggleChat = () => {
//     setIsChatOpen(!isChatOpen);
//   };

//   useEffect(() => {
//     // Check if this is a Shopify installation request
//     const urlParams = new URLSearchParams(window.location.search);
//     const shop = urlParams.get('shop');
//     const hmac = urlParams.get('hmac');

//     if (shop && hmac) {
//       // Redirect to backend install API
//       const queryString = urlParams.toString();
//       window.location.href = `${import.meta.env.VITE_APP_BACKEND_URL}/install?${queryString}`;
//       return; // Exit early to prevent further execution
//     }

//     // Normal session initialization for regular chat usage
//     console.log('Initializing normal chat session');
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
//           }
//         } catch (error) {
//           console.error('Error fetching session_id:', error);
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