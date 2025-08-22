// import React, { useState, useEffect, useRef } from 'react';
// import { FaUser, FaRobot, FaPaperPlane, FaTrashAlt } from 'react-icons/fa';
// import { BsRobot } from 'react-icons/bs';
// import axios from 'axios';
// import ReactMarkdown from 'react-markdown';
// import remarkGfm from 'remark-gfm';

// const ChatBox = () => {
//     const [message, setMessage] = useState('');
//     const [chat, setChat] = useState([]);
//     const [isTyping, setIsTyping] = useState(false);

//     const messagesEndRef = useRef(null);


//     // Fetch initial messages from backend
// //    useEffect(() => {
// //     axios.get(`${import.meta.env.VITE_APP_BACKEND_URL}/api/messages`) // Update to match backend port
// //         .then(response => setChat(response.data))
// //         .catch(error => console.error('Error fetching messages:', error));
// // }, []);
//    useEffect(() => {
//     axios.get(`${import.meta.env.VITE_APP_BACKEND_URL}/api/messages`) // Update to match backend port
//         .then(response => setChat(response.data))
//         .catch(error => console.error('Error fetching messages:', error));
// }, []);

//     // Auto-scroll to bottom when new messages arrive or typing indicator changes
//     useEffect(() => {
//         messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
//     }, [chat, isTyping]);



//     const sendMessage = async () => {
//         if (message.trim() === '') return;

//         // Create real-time timestamp in IST
//         const realTime = new Date().toLocaleString('en-IN', {
//             hour: '2-digit',
//             minute: '2-digit',
//             hour12: true,
//             day: '2-digit',
//             month: 'short',
//             year: 'numeric'
//         });

//         try {
//             const userMessage = {
//                 sender: 'user',
//                 text: message,
//                 time: realTime
//             };
//             setChat(prevChat => [...prevChat, userMessage]);
//             setMessage('');
//             setIsTyping(true);

//             const response = await axios.post(`${import.meta.env.VITE_APP_BACKEND_URL}/api/messages`, { text: message });
//             setChat(prevChat => [...prevChat, response.data.message]);
//             setIsTyping(false);
//         } catch (error) {
//             console.error('Error sending message:', error);
//             setIsTyping(false);
//         }
//     };

//     // const sendMessage = async () => {
//     //     if (message.trim() === '') return;
//     //     const realTime = new Date().toLocaleString('en-IN', {
//     //         hour: '2-digit',
//     //         minute: '2-digit',
//     //         hour12: true,
//     //         day: '2-digit',
//     //         month: 'short',
//     //         year: 'numeric'
//     //     });
//     //     try {
//     //         const userMessage = {
//     //             sender: 'user',
//     //             text: message,
//     //             time: realTime
//     //         };
//     //         setChat(prevChat => [...prevChat, userMessage]);
//     //         setMessage('');
//     //         setIsTyping(true);

//     //         const response = await axios.post(
//     //             `${import.meta.env.VITE_APP_BACKEND_URL}/api/messages`,
//     //             { text: message },
//     //             { headers: { 'X-Shop-Domain': shop } }
//     //         );
//     //         setChat(prevChat => [...prevChat, response.data.message]);
//     //         setIsTyping(false);
//     //     } catch (error) {
//     //         console.error('Error sending message:', error);
//     //         setIsTyping(false);
//     //     }
//     // };

//     const handleClearChat = async () => {
//         try {
//             const res = await axios.post(`${import.meta.env.VITE_APP_BACKEND_URL}/api/messages/clear`);
//             if (res.data.status === 'success') {
//                 setChat([{
//                     sender: "bot",
//                     text: "Hello! How can I help you today?",
//                     time: new Date().toLocaleString('en-IN', {
//                         hour: '2-digit',
//                         minute: '2-digit',
//                         hour12: true,
//                         day: '2-digit',
//                         month: 'short',
//                         year: 'numeric'
//                     })
//                 }]);
//             }
//         } catch (error) {
//             console.error('Error clearing chat:', error);
//         }
//     };

//     return (
//         <div className="w-full h-[460px] max-h-[90vh] shadow-lg rounded-2xl overflow-hidden">
//             {/* Header */}
//             <div className="bg-gradient-to-r from-purple-400 to-purple-600 text-white px-4 py-3 flex items-center justify-between">
//                 <div className="flex items-center gap-2">
//                     <BsRobot className="text-xl" />
//                     <div>
//                         <h1 className="font-semibold text-lg">AI Assistant</h1>
//                         <p className="text-xs text-white/80">● Online</p>
//                     </div>
//                 </div>
//                 <button
//                     onClick={handleClearChat}
//                     title="Clear chat"
//                     className="hover:text-red-300 transition-colors duration-200"
//                 >
//                     <FaTrashAlt className="text-white text-lg" />
//                 </button>
//             </div>

//             {/* Chat Window */}
//             <div className="h-80 overflow-y-auto px-4 py-2 space-y-3 bg-gray-50" style={{ scrollbarWidth: 'thin' }}>
//                 {chat.map((msg, index) => (
//                     <div key={index} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
//                         <div className="flex flex-col items-end gap-2 max-w-xs">
//                             <div className='flex gap-2'>
//                                 {msg.sender === 'bot' && (
//                                     <BsRobot className="text-gray-400 text-sm mb-1" />
//                                 )}
//                                 <div
//                                     className={`rounded-xl px-4 py-2 text-sm ${
//                                         msg.sender === 'user'
//                                             ? 'bg-purple-600 text-white rounded-br-none'
//                                             : 'bg-white text-gray-800 shadow-sm rounded-bl-none'
//                                     }`}
//                                 >
//                                     <ReactMarkdown
//                                         remarkPlugins={[remarkGfm]}
//                                         components={{
//                                             p: ({ node, ...props }) => <p className="m-0" {...props} />,
//                                             strong: ({ node, ...props }) => <strong className="font-bold" {...props} />,
//                                             ol: ({ node, ...props }) => <ol className="list-decimal list-outside ml-4" {...props} />,
//                                             ul: ({ node, ...props }) => <ul className="list-disc list-outside ml-4" {...props} />,
//                                             li: ({ node, ...props }) => <li className="mb-1" {...props} />
//                                         }}
//                                     >
//                                         {msg.text}
//                                     </ReactMarkdown>
//                                 </div>
//                             </div>
//                             <div className={`flex ${msg.sender === 'bot' ? 'text-left justify-start gap-2' : 'justify-end gap-1'}`}>
//                                 <div className="text-xs text-gray-400 self-end">
//                                     {msg.time}
//                                 </div>
//                                 {msg.sender === 'user' && (
//                                     <FaUser className="text-purple-400 text-sm mb-1" />
//                                 )}
//                             </div>
//                         </div>
//                     </div>
//                 ))}
//                 {isTyping && (
//                     <div className="flex justify-start">
//                         <div className="flex flex-col items-end gap-2 max-w-xs">
//                             <div className='flex gap-2'>
//                                 <BsRobot className="text-gray-400 text-sm mb-1" />
//                                 <div className="rounded-xl px-4 py-2 text-sm bg-white text-gray-800 shadow-sm rounded-bl-none">
//                                     <div className="animate-pulse flex justify-center items-center gap-1">
//                                         <p className='w-1 h-1 rounded-full bg-black'></p>
//                                         <p className='w-1 h-1 rounded-full bg-black'></p>
//                                         <p className='w-1 h-1 rounded-full bg-black'></p>
//                                     </div>
//                                 </div>
//                             </div>
//                         </div>
//                     </div>
//                 )}
//                 <div ref={messagesEndRef} />
//             </div>

//             {/* Input Area */}
//             <div className="border-t border-purple-400 bg-white p-3 flex items-center gap-2">
//                 <input
//                     type="text"
//                     placeholder="Type your message..."
//                     className="flex-1 border border-gray-400 rounded-full px-4 py-2 text-sm outline-none focus:border-purple-400"
//                     value={message}
//                     onChange={(e) => setMessage(e.target.value)}
//                     onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
//                 />
//                 <button
//                     onClick={sendMessage}
//                     className="not-disabled:cursor-pointer disabled:bg-purple-400 bg-purple-500 hover:bg-purple-600 text-white p-3 rounded-full transition-colors duration-200"
//                     disabled={message.trim() === '' || isTyping}
//                 >
//                     <FaPaperPlane />
//                 </button>
//             </div>
//         </div>
//     );
// };

// export default ChatBox;

import React, { useState, useEffect, useRef } from 'react';
import { FaUser, FaRobot, FaPaperPlane, FaTrashAlt } from 'react-icons/fa';
import { BsRobot } from 'react-icons/bs';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

const ChatBox = () => {
    const [inputValue, setInputValue] = useState('');
    const [messages, setMessages] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const storeId = "116"; // Ensure this is set appropriately
    const messagesEndRef = useRef(null);

    const storedSessionId = localStorage.getItem('session_id');

    // Fetch initial messages from backend
    // useEffect(() => {
    //     axios
    //         .get(`${import.meta.env.VITE_APP_BACKEND_URL}/api/messages`)
    //         .then((response) => setMessages(response.data))
    //         .catch((error) => console.error('Error fetching messages:', error));
    // }, []);

    // Auto-scroll to bottom when new messages arrive or loading state changes
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages, isLoading]);

    const addMessage = (text, sender) => {
        const realTime = new Date().toLocaleString('en-IN', {
            hour: '2-digit',
            minute: '2-digit',
            hour12: true,
            day: '2-digit',
            month: 'short',
            year: 'numeric',
        });
        setMessages((prev) => [...prev, { text, sender, time: realTime }]);
    };

    const handleSend = async () => {
        if (!inputValue.trim() || !storedSessionId) {
            if (!storedSessionId) {
                addMessage('No session ID available. Please try again.', 'bot');
            }
            return;
        }

        // Add user message
        addMessage(inputValue, 'user');
        const currentMessage = inputValue;
        setInputValue('');
        setIsLoading(true);

        try {
            const conversationHistory = messages.map((msg) => ({
                role: msg.sender === 'user' ? 'user' : 'assistant',
                content: msg.text,
            }));
            conversationHistory.push({ role: 'user', content: currentMessage });

            const response = await axios.post(`https://n8nflow.byteztech.in/webhook/api/ask`, {
                question: currentMessage,
                sessionId: storedSessionId,
                Store_id: storeId,
            });

            console.log(response, "response from backend");

            // axios puts the parsed JSON response in response.data
            let botReply = 'Sorry, I could not understand the response.';

            if (response.data && Array.isArray(response.data) && response.data[0]?.output) {
                botReply = response.data[0].output;
            }

            addMessage(botReply, 'bot');
        } catch (error) {
            console.error('Error fetching backend response:', error);
            addMessage('Sorry, something went wrong. Please try again.', 'bot');
        } finally {
            setIsLoading(false);
        }
    };


    const handleClearChat = async () => {
        try {
            const res = await axios.post(`${import.meta.env.VITE_APP_BACKEND_URL}/api/messages/clear`);
            if (res.data.status === 'success') {
                setMessages([
                    {
                        sender: 'bot',
                        text: 'Hello! How can I help you today?',
                        time: new Date().toLocaleString('en-IN', {
                            hour: '2-digit',
                            minute: '2-digit',
                            hour12: true,
                            day: '2-digit',
                            month: 'short',
                            year: 'numeric',
                        }),
                    },
                ]);
            }
        } catch (error) {
            console.error('Error clearing chat:', error);
        }
    };

    return (
        <div className="w-full h-[460px] max-h-[90vh] shadow-lg rounded-2xl overflow-hidden">
            {/* Header */}
            <div className="bg-gradient-to-r from-purple-400 to-purple-600 text-white px-4 py-3 flex items-center justify-between">
                <div className="flex items-center gap-2">
                    <BsRobot className="text-xl" />
                    <div>
                        <h1 className="font-semibold text-lg">AI Assistant</h1>
                        <p className="text-xs text-white/80">● Online</p>
                    </div>
                </div>
                <button
                    onClick={handleClearChat}
                    title="Clear chat"
                    className="hover:text-red-300 transition-colors duration-200"
                >
                    <FaTrashAlt className="text-white text-lg" />
                </button>
            </div>

            {/* Chat Window */}
            <div className="h-80 overflow-y-auto px-4 py-2 space-y-3 bg-gray-50" style={{ scrollbarWidth: 'thin' }}>
                {messages.map((msg, index) => (
                    <div key={index} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                        <div className="flex flex-col items-end gap-2 max-w-xs">
                            <div className="flex gap-2">
                                {msg.sender === 'bot' && <BsRobot className="text-gray-400 text-sm mb-1" />}
                                <div
                                    className={`rounded-xl px-4 py-2 text-sm ${msg.sender === 'user'
                                        ? 'bg-purple-600 text-white rounded-br-none'
                                        : 'bg-white text-gray-800 shadow-sm rounded-bl-none'
                                        }`}
                                >
                                    <ReactMarkdown
                                        remarkPlugins={[remarkGfm]}
                                        components={{
                                            p: ({ node, ...props }) => <p className="m-0" {...props} />,
                                            strong: ({ node, ...props }) => <strong className="font-bold" {...props} />,
                                            ol: ({ node, ...props }) => <ol className="list-decimal list-outside ml-4" {...props} />,
                                            ul: ({ node, ...props }) => <ul className="list-disc list-outside ml-4" {...props} />,
                                            li: ({ node, ...props }) => <li className="mb-1" {...props} />,
                                        }}
                                    >
                                        {msg.text}
                                    </ReactMarkdown>
                                </div>
                            </div>
                            <div className={`flex ${msg.sender === 'bot' ? 'text-left justify-start gap-2' : 'justify-end gap-1'}`}>
                                <div className="text-xs text-gray-400 self-end">{msg.time}</div>
                                {msg.sender === 'user' && <FaUser className="text-purple-400 text-sm mb-1" />}
                            </div>
                        </div>
                    </div>
                ))}
                {isLoading && (
                    <div className="flex justify-start">
                        <div className="flex flex-col items-end gap-2 max-w-xs">
                            <div className="flex gap-2">

                                <BsRobot className="text-gray-400 text-sm mb-1" />
                                <div className="rounded-xl px-4 py-2 text-sm bg-white text-gray-800 shadow-sm rounded-bl-none">
                                    <div className="animate-pulse flex justify-center items-center gap-1">
                                        <p className="w-1 h-1 rounded-full bg-black"></p>
                                        <p className="w-1 h-1 rounded-full bg-black"></p>
                                        <p className="w-1 h-1 rounded-full bg-black"></p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div className="border-t border-purple-400 bg-white p-3 flex items-center gap-2">
                <input
                    type="text"
                    placeholder="Type your message..."
                    className="flex-1 border border-gray-400 rounded-full px-4 py-2 text-sm outline-none focus:border-purple-400"
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                />
                <button
                    onClick={handleSend}
                    className="not-disabled:cursor-pointer disabled:bg-purple-400 bg-purple-500 hover:bg-purple-600 text-white p-3 rounded-full transition-colors duration-200"
                    disabled={inputValue.trim() === '' || isLoading}
                >
                    <FaPaperPlane />
                </button>
            </div>
        </div>
    );
};

export default ChatBox;