import React from "react";
import ReactDOM from "react-dom/client";
import ChatBox from "./components/Chatbox";

const div = document.createElement("div");
div.id = "chatbox-container";
div.style.position = "fixed";
div.style.bottom = "20px";
div.style.right = "20px";
div.style.zIndex = "99999";
document.body.appendChild(div);

const root = ReactDOM.createRoot(div);
root.render(<ChatBox />);
