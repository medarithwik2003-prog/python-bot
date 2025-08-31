# app.py
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Ex Chat Simulator", layout="wide")

html_code = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Ex Chat Simulator</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link
      rel="stylesheet"
      href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"
    />
    <link
      href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Dancing+Script:wght@700&display=swap"
      rel="stylesheet"
    />
    <style>
      :root {
        --primary: #ff4d94;
        --primary-light: #ff85b3;
        --secondary: #c77dff;
        --accent: #ff6b6b;
        --dark: #1a1a2e;
        --darker: #0d0d1a;
        --light: #f8f9fa;
        --user-bubble: #4d79ff;
        --bot-bubble: #ff66a3;
        --header-height: 70px;
        --input-height: 70px;
      }

      * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }

      body {
        font-family: "Poppins", sans-serif;
        background: linear-gradient(135deg, var(--darker), var(--dark));
        color: var(--light);
        min-height: 100vh;
        overflow-x: hidden;
        position: relative;
      }

      body::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: radial-gradient(
            circle at 10% 20%,
            rgba(255, 109, 163, 0.15) 0%,
            transparent 20%
          ),
          radial-gradient(
            circle at 90% 80%,
            rgba(199, 125, 255, 0.15) 0%,
            transparent 20%
          ),
          radial-gradient(
            circle at 30% 60%,
            rgba(255, 107, 107, 0.1) 0%,
            transparent 25%
          ),
          radial-gradient(
            circle at 70% 30%,
            rgba(77, 121, 255, 0.1) 0%,
            transparent 25%
          );
        z-index: -1;
      }

      .floating-hearts {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
      }

      .heart {
        position: absolute;
        color: rgba(255, 77, 148, 0.3);
        font-size: 20px;
        animation: float 15s infinite linear;
      }

      @keyframes float {
        0% {
          transform: translateY(100vh) rotate(0deg);
          opacity: 0;
        }
        10% {
          opacity: 0.4;
        }
        90% {
          opacity: 0.4;
        }
        100% {
          transform: translateY(-100px) rotate(360deg);
          opacity: 0;
        }
      }

      .chat-container {
        display: flex;
        flex-direction: column;
        max-width: 900px;
        height: 100vh;
        margin: 0 auto;
        background: rgba(26, 26, 46, 0.7);
        backdrop-filter: blur(10px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        border-radius: 0;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.1);
      }

      .chat-header {
        background: linear-gradient(90deg, var(--primary), var(--secondary));
        color: white;
        padding: 15px 25px;
        display: flex;
        align-items: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        z-index: 10;
        position: relative;
      }

      .profile-pic {
        width: 45px;
        height: 45px;
        border-radius: 50%;
        background: linear-gradient(45deg, #ff85b3, #c77dff);
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 15px;
        border: 2px solid white;
        overflow: hidden;
      }

      .profile-pic i {
        font-size: 24px;
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
      }

      .header-content {
        flex: 1;
      }

      .chat-header h1 {
        font-family: "Dancing Script", cursive;
        font-size: 28px;
        font-weight: 700;
        margin: 0;
        display: flex;
        align-items: center;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      .status {
        display: flex;
        align-items: center;
        font-size: 13px;
        margin-top: 3px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }

      .status-dot {
        width: 8px;
        height: 8px;
        background-color: #4ade80;
        border-radius: 50%;
        margin-right: 6px;
        animation: pulse 1.5s infinite;
        flex-shrink: 0;
      }

      @keyframes pulse {
        0% {
          opacity: 0.7;
        }
        50% {
          opacity: 1;
        }
        100% {
          opacity: 0.7;
        }
      }

      .chat-messages {
        flex: 1;
        overflow-y: auto;
        padding: 20px;
        display: flex;
        flex-direction: column;
        gap: 20px;
        scroll-behavior: smooth;
        max-height: calc(100vh - 180px);
      }

      .message {
        max-width: 80%;
        padding: 15px 20px;
        border-radius: 25px;
        position: relative;
        line-height: 1.5;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        animation: messageAppear 0.3s ease-out;
        word-wrap: break-word;
        font-size: 16px;
      }

      @keyframes messageAppear {
        from {
          opacity: 0;
          transform: translateY(10px);
        }
        to {
          opacity: 1;
          transform: translateY(0);
        }
      }

      .message.user {
        background: linear-gradient(135deg, var(--user-bubble), #3366ff);
        color: white;
        align-self: flex-end;
        border-bottom-right-radius: 8px;
      }

      .message.bot {
        background: linear-gradient(135deg, var(--bot-bubble), #ff3385);
        color: white;
        align-self: flex-start;
        border-bottom-left-radius: 8px;
        position: relative;
      }

      .message-time {
        display: block;
        font-size: 11px;
        opacity: 0.8;
        margin-top: 5px;
        text-align: right;
      }

      .message.typing {
        display: flex;
        align-items: center;
        padding: 15px 20px;
      }

      .typing-indicator {
        display: flex;
        align-items: center;
        gap: 6px;
      }

      .typing-dot {
        width: 10px;
        height: 10px;
        background-color: white;
        border-radius: 50%;
        opacity: 0.6;
      }

      .typing-dot:nth-child(1) {
        animation: typing 1.2s infinite;
      }
      .typing-dot:nth-child(2) {
        animation: typing 1.2s infinite 0.4s;
      }
      .typing-dot:nth-child(3) {
        animation: typing 1.2s infinite 0.8s;
      }

      @keyframes typing {
        0%,
        60%,
        100% {
          transform: translateY(0);
          opacity: 0.6;
        }
        30% {
          transform: translateY(-5px);
          opacity: 1;
        }
      }

      .chat-input-area {
        display: flex;
        padding: 15px;
        background: rgba(40, 40, 70, 0.8);
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        position: sticky;
        bottom: 0;
        z-index: 5;
      }

      #userInput {
        flex: 1;
        padding: 16px 20px;
        border: none;
        border-radius: 30px;
        background: rgba(255, 255, 255, 0.1);
        color: white;
        font-size: 16px;
        outline: none;
        transition: all 0.3s;
      }

      #userInput:focus {
        background: rgba(255, 255, 255, 0.15);
        box-shadow: 0 0 0 2px var(--primary-light);
      }

      #userInput::placeholder {
        color: rgba(255, 255, 255, 0.5);
        font-size: 14px;
      }

      #sendButton {
        width: 55px;
        height: 55px;
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        color: white;
        border: none;
        border-radius: 50%;
        cursor: pointer;
        margin-left: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(199, 125, 255, 0.3);
      }

      #sendButton:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 6px 20px rgba(199, 125, 255, 0.5);
      }

      #sendButton:disabled {
        opacity: 0.5;
        transform: none;
        box-shadow: none;
        cursor: not-allowed;
      }

      .chat-messages::-webkit-scrollbar {
        width: 8px;
      }

      .chat-messages::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
      }

      .chat-messages::-webkit-scrollbar-thumb {
        background: linear-gradient(var(--primary), var(--secondary));
        border-radius: 10px;
      }

      .heart-decoration {
        position: absolute;
        font-size: 14px;
        color: var(--accent);
        opacity: 0.7;
      }

      .bot-message-decoration {
        position: absolute;
        font-size: 24px;
        color: rgba(255, 255, 255, 0.2);
      }

      .bot-message-decoration.left {
        top: -10px;
        left: -10px;
      }

      .bot-message-decoration.right {
        bottom: -10px;
        right: -10px;
      }

      .intro-message {
        text-align: center;
        padding: 30px 20px;
        opacity: 0.8;
        font-size: 14px;
      }

      .intro-message i {
        color: var(--primary);
        margin: 0 5px;
        display: inline-block;
      }

      .welcome-banner {
        text-align: center;
        padding: 15px;
        background: linear-gradient(
          90deg,
          rgba(255, 77, 148, 0.3),
          rgba(199, 125, 255, 0.3)
        );
        font-size: 14px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }

      /* Setup Form Styles */
      .setup-container {
        max-width: 600px;
        margin: 20px auto;
        padding: 30px;
        background: rgba(26, 26, 46, 0.8);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        max-height: 90vh;
        overflow-y: auto;
        scroll-behavior: smooth;
      }

      .setup-title {
        text-align: center;
        margin-bottom: 30px;
        color: var(--primary);
        font-family: "Dancing Script", cursive;
        font-size: 36px;
      }

      .form-group {
        margin-bottom: 20px;
      }

      .form-group label {
        display: block;
        margin-bottom: 8px;
        font-weight: 500;
        color: var(--light);
      }

      .form-group input,
      .form-group textarea {
        width: 100%;
        padding: 12px 16px;
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: white;
        font-size: 16px;
        transition: all 0.3s;
      }

      .form-group input:focus,
      .form-group textarea:focus {
        outline: none;
        background: rgba(255, 255, 255, 0.15);
        border-color: var(--primary);
        box-shadow: 0 0 0 2px rgba(255, 77, 148, 0.3);
        transform: translateY(-2px);
      }

      .submit-btn {
        width: 100%;
        padding: 14px;
        background: linear-gradient(90deg, var(--primary), var(--secondary));
        color: white;
        border: none;
        border-radius: 12px;
        font-size: 18px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s;
        margin-top: 10px;
      }

      .submit-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
      }

      .grid-2 {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 15px;
      }

      /* Scroll to bottom button */
      .scroll-to-bottom {
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        opacity: 0;
        transition: opacity 0.3s, transform 0.3s;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        z-index: 100;
        pointer-events: none;
        display: none; /* Initially hidden */
      }

      .scroll-to-bottom.visible {
        opacity: 1;
        pointer-events: auto;
        transform: scale(1);
        display: flex; /* Show when visible */
      }

      .scroll-to-bottom:hover {
        transform: translateY(-3px) scale(1.1);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
      }

      .setup-container::-webkit-scrollbar {
        width: 8px;
        height: 8px;
      }

      .setup-container::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
      }

      .setup-container::-webkit-scrollbar-thumb {
        background: linear-gradient(var(--primary), var(--secondary));
        border-radius: 10px;
      }

      .form-progress {
        position: sticky;
        top: 0;
        height: 5px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        margin-bottom: 20px;
        z-index: 10;
      }

      .form-progress-bar {
        height: 100%;
        background: linear-gradient(90deg, var(--primary), var(--secondary));
        border-radius: 10px;
        width: 0%;
        transition: width 0.3s ease;
      }

      @media (max-width: 768px) {
        .grid-2 {
          grid-template-columns: 1fr;
        }

        .setup-container {
          margin: 15px;
          padding: 20px;
          max-height: 85vh;
        }

        .chat-messages {
          max-height: calc(100vh - 160px);
        }

        .message {
          max-width: 90%;
        }

        .scroll-to-bottom {
          bottom: 20px;
          right: 20px;
        }

        .chat-header h1 {
          font-size: 22px;
        }

        .status {
          font-size: 12px;
        }

        .welcome-banner {
          font-size: 12px;
          padding: 12px;
        }

        #userInput::placeholder {
          font-size: 12px;
        }
      }
    </style>
  </head>
  <body>
    <!-- Floating hearts background -->
    <div class="floating-hearts" id="floatingHearts"></div>

    <!-- Scroll to bottom button for setup form -->
    <div class="scroll-to-bottom" id="scrollToBottomBtn">
      <i class="fas fa-chevron-down"></i>
    </div>

    <!-- Setup Form -->
    <div id="setupForm" class="setup-container">
      <div class="form-progress">
        <div class="form-progress-bar" id="formProgress"></div>
      </div>

      <h2 class="setup-title">Tell me about your ex 💔</h2>
      <form id="exDetailsForm">
        <div class="grid-2">
          <div class="form-group">
            <label for="exName">Ex's Name</label>
            <input type="text" id="exName" required placeholder="e.g. Anjali" />
          </div>
          <div class="form-group">
            <label for="yourNickname">What your ex used to call you</label>
            <input
              type="text"
              id="yourNickname"
              required
              placeholder="e.g. Babu"
            />
          </div>
          <div class="form-group">
            <label for="herNickname">What you used to call your ex</label>
            <input
              type="text"
              id="herNickname"
              required
              placeholder="e.g. Bubu"
            />
          </div>
          <div class="form-group">
            <label for="job">Profession</label>
            <input
              type="text"
              id="job"
              required
              placeholder="e.g. Software Engineer"
            />
          </div>
        </div>

        <div class="form-group">
          <label for="hobbies">Hobbies</label>
          <input
            type="text"
            id="hobbies"
            required
            placeholder="e.g. Painting, Reading, Badminton"
          />
        </div>

        <div class="form-group">
          <label for="personality">Personality</label>
          <input
            type="text"
            id="personality"
            required
            placeholder="e.g. Funny, Sarcastic, Caring"
          />
        </div>

        <div class="form-group">
          <label for="aboutYou">About You</label>
          <input
            type="text"
            id="aboutYou"
            required
            placeholder="e.g. Gym freak, not into coding"
          />
        </div>

        <div class="form-group">
          <label for="whatupchat"
            >Chat reference (you can even share your WhatsApp chat)</label
          >
          <textarea
            id="whatupchat"
            rows="2"
            placeholder="Rohit: Arey meri jaan bubu bubu bubu 😍 
Anjali: Kal tumne mujhe bubu nahi bulaya 😤"
          ></textarea>
        </div>

        <div class="form-group">
          <label for="chatlangage">In which language you want to chat?</label>
          <input
            type="text"
            id="chatlangage"
            required
            placeholder="e.g. Telugu, Hindi, English, Marathi"
          />
        </div>
        <div class="form-group">
          <label for="heorshee">Is your ex a boyfriend or girlfriend?</label>
          <input
            type="text"
            id="heorshee"
            required
            placeholder="e.g. boyfriend or girlfriend"
          />
        </div>

        <button type="submit" class="submit-btn">Start Chatting 💬</button>
      </form>
    </div>

    <!-- Chat Interface (Initially Hidden) -->
    <div id="chatInterface" class="chat-container" style="display: none">
      <div class="chat-header">
        <div class="profile-pic">
          <i class="fas fa-heart"></i>
        </div>
        <div class="header-content">
          <h1 id="chatPartnerName">
            Ex's Name 💔<span class="heart-pulse">❤️</span>
          </h1>
          <div class="status">
            <span class="status-dot"></span>
            Online - Last seen just now
          </div>
        </div>
      </div>

      <div class="welcome-banner">
        <i class="fas fa-heart"></i> Chat with your ex - Share your thoughts
        <i class="fas fa-heart"></i>
      </div>

      <div class="chat-messages" id="chatMessages">
        <div class="intro-message">
          Chat started. Say something to begin the conversation.
        </div>
      </div>

      <div class="chat-input-area">
        <input type="text" id="userInput" placeholder="Type your message..." />
        <button id="sendButton">
          <i class="fas fa-paper-plane"></i>
        </button>
      </div>
    </div>

    <script>
      const GEMINI_API_KEY = "AIzaSyDfZeVIS3ND_iTtt3YDMom43tBqw2WCPPI";

      let History = [];
      let systemInstruction = "";
      let exName = "";
      let howSheCallsYou = "";

      // --- DOM Elements ---
      const setupForm = document.getElementById("setupForm");
      const exDetailsForm = document.getElementById("exDetailsForm");
      const chatInterface = document.getElementById("chatInterface");
      const chatMessagesEl = document.getElementById("chatMessages");
      const userInputEl = document.getElementById("userInput");
      const sendButtonEl = document.getElementById("sendButton");
      const chatPartnerName = document.getElementById("chatPartnerName");
      const scrollToBottomBtn = document.getElementById("scrollToBottomBtn");
      const formProgress = document.getElementById("formProgress");

      // --- Floating Hearts Background ---
      function createFloatingHearts() {
        const container = document.getElementById("floatingHearts");
        const heartCount = 20;

        for (let i = 0; i < heartCount; i++) {
          const heart = document.createElement("div");
          heart.classList.add("heart");
          heart.innerHTML = "❤️";

          // Random position and animation delay
          heart.style.left = `${Math.random() * 100}%`;
          heart.style.animationDelay = `${Math.random() * 15}s`;
          heart.style.fontSize = `${10 + Math.random() * 20}px`;
          heart.style.opacity = `${0.2 + Math.random() * 0.3}`;

          container.appendChild(heart);
        }
      }

      // --- Scroll Functions for Setup Form ---
      function scrollToBottom() {
        setupForm.scrollTo({
          top: setupForm.scrollHeight,
          behavior: "smooth",
        });
      }

      function checkFormScrollPosition() {
        // Show/hide scroll to bottom button based on scroll position
        const scrollThreshold = 100; // pixels from bottom
        const isNearBottom =
          setupForm.scrollHeight -
            setupForm.scrollTop -
            setupForm.clientHeight <
          scrollThreshold;

        if (isNearBottom) {
          scrollToBottomBtn.classList.remove("visible");
        } else {
          scrollToBottomBtn.classList.add("visible");
        }

        // Update progress bar
        const scrollPercentage =
          (setupForm.scrollTop /
            (setupForm.scrollHeight - setupForm.clientHeight)) *
          100;
        formProgress.style.width = `${scrollPercentage}%`;
      }

      // --- Gemini API Interaction ---
      async function Chatting(userProblem) {
        if (!GEMINI_API_KEY) {
          throw new Error("API key not set");
        }

        // Add user message to History
        History.push({
          role: "user",
          parts: [{ text: userProblem }],
        });

        const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${GEMINI_API_KEY}`;

        const requestBody = {
          contents: History,
          systemInstruction: {
            parts: [{ text: systemInstruction }],
          },
          generationConfig: {
            temperature: 0.8,
            maxOutputTokens: 800,
          },
        };

        try {
          const response = await fetch(apiUrl, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(requestBody),
          });

          const responseData = await response.json();

          if (!response.ok) {
            console.error("API Error Response:", responseData);
            const errorMessage =
              responseData.error?.message ||
              `API request failed with status ${response.status}`;
            throw new Error(errorMessage);
          }

          let reply = "Sorry, I didn't understand that. Can you try again?";
          if (
            responseData.candidates &&
            responseData.candidates.length > 0 &&
            responseData.candidates[0].content &&
            responseData.candidates[0].content.parts &&
            responseData.candidates[0].content.parts.length > 0
          ) {
            reply = responseData.candidates[0].content.parts[0].text;

            // Remove any duplicate name prefix that might be added by the API
            // This fixes the issue where the name appears twice
            const namePrefix = `${exName}: `;
            if (reply.startsWith(namePrefix)) {
              reply = reply.substring(namePrefix.length);
            }
            
          }

          // Add AI's response to History
          History.push({
            role: "model",
            parts: [{ text: reply }], // Store without name prefix to avoid duplication
          });

          return reply;
        } catch (error) {
          console.error("Error fetching from Gemini API:", error);
          throw error;
        }
      }

      // --- Frontend UI Logic ---
      function addMessageToUI(text, sender, isTyping = false) {
        const messageElement = document.createElement("div");
        messageElement.classList.add("message", sender);

        if (isTyping) {
          messageElement.classList.add("typing");
          messageElement.innerHTML = `
                    <div class="typing-indicator">
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                    </div>
                `;
        } else {
          // Add decorative elements to bot messages
          if (sender === "bot") {
            messageElement.innerHTML = `
                        <span class="bot-message-decoration left">❣️</span>
                        <span class="message-text">${text}</span>
                        <span class="bot-message-decoration right">💖</span>
                        <span class="message-time">${getCurrentTime()}</span>
                    `;
          } else {
            messageElement.innerHTML = `
                        <span class="message-text">${text}</span>
                        <span class="message-time">${getCurrentTime()}</span>
                    `;
          }
        }

        chatMessagesEl.appendChild(messageElement);
        scrollChatToBottom();
        return messageElement;
      }

      function scrollChatToBottom() {
        chatMessagesEl.scrollTo({
          top: chatMessagesEl.scrollHeight,
          behavior: "smooth",
        });
      }

      function getCurrentTime() {
        const now = new Date();
        return `${now.getHours().toString().padStart(2, "0")}:${now
          .getMinutes()
          .toString()
          .padStart(2, "0")}`;
      }

      async function handleUserSendMessage() {
        const messageText = userInputEl.value.trim();
        if (messageText === "") return;

        addMessageToUI(messageText, "user");
        userInputEl.value = "";
        userInputEl.focus();

        const typingIndicator = addMessageToUI("", "bot", true);

        try {
          const botResponseText = await Chatting(messageText);
          chatMessagesEl.removeChild(typingIndicator);
          addMessageToUI(botResponseText, "bot");
        } catch (error) {
          console.error("Unhandled error in send message:", error);
          chatMessagesEl.removeChild(typingIndicator);
          addMessageToUI(
            "Oops! Something went wrong. Please try again.",
            "bot"
          );
        }
      }

      // --- Event Listeners ---
      document.addEventListener("DOMContentLoaded", () => {
        // Create floating hearts background
        createFloatingHearts();

        // Setup form submission
        exDetailsForm.addEventListener("submit", function (e) {
          e.preventDefault();

          // Get form values
          exName = document.getElementById("exName").value;
          howSheCallsYou = document.getElementById("yourNickname").value;
          const howYouCallHer = document.getElementById("herNickname").value;
          const hobbies = document.getElementById("hobbies").value;
          const job = document.getElementById("job").value;
          const personality = document.getElementById("personality").value;
          const aboutYou = document.getElementById("aboutYou").value;
          const whatupchat = document.getElementById("whatupchat").value;
          const chatlangage = document.getElementById("chatlangage").value;
          const heorshe = document.getElementById("heorshee").value;

          // Build system instruction (exactly as in your JS code)
          systemInstruction = `
                    You have to behave like my ex-${heorshe}. Your name is ${exName}.
                    You used to call me ${howSheCallsYou}.
                    I used to call you ${howYouCallHer}.
                    Your hobbies: ${hobbies}.
                    You work as a ${job}.
                    Your personality: ${personality}.
                    
                    About me: ${aboutYou}.
                    ${whatupchat ? `Additional notes: ${whatupchat}` : ""}

                    Respond like a real WhatsApp chat between me and you, with emotions and emojis.
                    Do not prefix your replies with your name. Just respond naturally as if we're chatting.

                    and keep the conversation in ${chatlangage} language and type in english only do not type in ${chatlangage} language.
                    It should be ${chatlangage}-in-English-letters chat style
                `;

          // Update UI
          chatPartnerName.textContent = `${exName} 💔`;

          // Switch to chat interface
          setupForm.style.display = "none";
          chatInterface.style.display = "flex";
          userInputEl.focus();

          // Add welcome message
          addMessageToUI(`Hey ${howSheCallsYou}! 😊 How are you doing?`, "bot");
        });

        // Send message event listeners
        sendButtonEl.addEventListener("click", handleUserSendMessage);
        userInputEl.addEventListener("keypress", (event) => {
          if (event.key === "Enter") {
            handleUserSendMessage();
          }
        });

        // Scroll to bottom button event listener for setup form
        scrollToBottomBtn.addEventListener("click", scrollToBottom);

        // Check scroll position when scrolling in setup form
        setupForm.addEventListener("scroll", checkFormScrollPosition);

        // Initial scroll position check
        checkFormScrollPosition();

        // Focus on first input field
        document.getElementById("exName").focus();
      });
    </script>
  </body>
</html>



"""


components.html(html_code, height=900, scrolling=True)

