import { useState } from 'react';
import { SiWechat } from 'react-icons/si';
import Chatbox from './components/Chatbox';
import { PiChatCircleSlashFill } from "react-icons/pi";

function App() {
  const [isChatOpen, setIsChatOpen] = useState(false);

  const toggleChat = () => {
    setIsChatOpen(!isChatOpen);
  };

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





// from flask import Flask, jsonify, request
// from flask_cors import CORS
// import datetime
// import requests
// from dotenv import load_dotenv
// import os

// app = Flask(__name__)
// CORS(app)  # Enable CORS for React frontend

// # Load environment variables
// load_dotenv()

// AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
// AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
// AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")

// # In-memory chat history (replace with a database for production)
// chat_history = [
//     {
//         "sender": "bot",
//         "text": "Hello! How can I help you today?",
//         "time": datetime.datetime.now().strftime("%I:%M %p, %d %b %Y")
//     }
// ]

// @app.route('/api/messages', methods=['GET'])
// def get_messages():
//     return jsonify(chat_history)

// @app.route('/api/messages', methods=['POST'])
// def send_message():
//     data = request.get_json()
//     user_message = {
//         "sender": "user",
//         "text": data['text'],
//         "time": datetime.datetime.now().strftime("%I:%M %p, %d %b %Y")
//     }
//     chat_history.append(user_message)

//     # Call Azure OpenAI API for bot response
//     try:
//         headers = {
//             "Content-Type": "application/json",
//             "api-key": AZURE_OPENAI_API_KEY
//         }
//         payload = {
//             "messages": [
//                 {"role": "system", "content": "You are a helpful AI assistant."},
//                 {"role": "user", "content": data['text']}
//             ],
//             "max_tokens": 150
//         }
//         response = requests.post(
//             f"{AZURE_OPENAI_ENDPOINT}/openai/deployments/{AZURE_OPENAI_DEPLOYMENT}/chat/completions?api-version=2023-05-15",
//             headers=headers,
//             json=payload
//         )
//         response.raise_for_status()
//         bot_text = response.json()["choices"][0]["message"]["content"].strip()

//         bot_response = {
//             "sender": "bot",
//             "text": bot_text,
//             "time": datetime.datetime.now().strftime("%I:%M %p, %d %b %Y")
//         }
//         chat_history.append(bot_response)
//         return jsonify({"status": "success", "message": bot_response})
//     except requests.exceptions.RequestException as e:
//         print(f"Error calling Azure OpenAI API: {e}")
//         bot_response = {
//             "sender": "bot",
//             "text": "Sorry, I couldn't process your request. Please try again.",
//             "time": datetime.datetime.now().strftime("%I:%M %p, %d %b %Y")
//         }
//         chat_history.append(bot_response)
//         return jsonify({"status": "error", "message": bot_response}), 500

// @app.route('/api/messages/clear', methods=['POST'])
// def clear_messages():
//     global chat_history
//     chat_history = [
//         {
//             "sender": "bot",
//             "text": "Hello! How can I help you today?",
//             "time": datetime.datetime.now().strftime("%I:%M %p, %d %b %Y")
//         }
//     ]
//     return jsonify({"status": "success", "message": "Chat history cleared"})

// if __name__ == '__main__':
//     app.run(port=5000, debug=True)