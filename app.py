# app.py

from flask import Flask, render_template_string, request, jsonify
from chatbot import get_response

app = Flask(__name__)

# Modern HTML UI template
HTML_PAGE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>AI Chatbot 🤖</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background: linear-gradient(135deg, #1f1c2c, #928dab);
      color: #fff;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      margin: 0;
    }
    .chat-container {
      width: 100%;
      max-width: 600px;
      height: 80vh;
      background: #2c2f33;
      border-radius: 12px;
      box-shadow: 0 8px 25px rgba(0,0,0,0.2);
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }
    .chat-header {
      background: #23272a;
      padding: 15px;
      text-align: center;
      font-size: 18px;
      font-weight: bold;
      border-bottom: 1px solid #444;
    }
    .chatbox {
      flex: 1;
      padding: 15px;
      overflow-y: auto;
      scroll-behavior: smooth;
    }
    .message {
      margin: 10px 0;
      padding: 12px 16px;
      border-radius: 20px;
      max-width: 70%;
      clear: both;
    }
    .user {
      background: #7289da;
      color: white;
      float: right;
      border-bottom-right-radius: 0;
    }
    .bot {
      background: #99aab5;
      color: black;
      float: left;
      border-bottom-left-radius: 0;
    }
    .input-area {
      display: flex;
      border-top: 1px solid #444;
    }
    .input-area input {
      flex: 1;
      padding: 12px;
      border: none;
      outline: none;
      background: #40444b;
      color: white;
      font-size: 16px;
      border-radius: 0 0 0 12px;
    }
    .input-area button {
      padding: 12px 20px;
      border: none;
      cursor: pointer;
      background: #7289da;
      color: white;
      font-size: 16px;
      border-radius: 0 0 12px 0;
      transition: background 0.3s;
    }
    .input-area button:hover {
      background: #5b6eae;
    }
  </style>
</head>
<body>
  <div class="chat-container">
    <div class="chat-header">AI Chatbot 🤖</div>
    <div id="chatbox" class="chatbox"></div>
    <div class="input-area">
      <input id="user_input" type="text" placeholder="Type a message..." onkeydown="if(event.key==='Enter') send()">
      <button onclick="send()">Send</button>
    </div>
  </div>

  <script>
    function send() {
      var user_input = document.getElementById('user_input').value;
      if (!user_input.trim()) return;
      var chat = document.getElementById('chatbox');

      // Add user message
      chat.innerHTML += "<div class='message user'>" + user_input + "</div>";
      chat.scrollTop = chat.scrollHeight;

      // Fetch bot response
      fetch("/get_response", {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({"message": user_input})
      })
      .then(res => res.json())
      .then(data => {
        chat.innerHTML += "<div class='message bot'>" + data.response + "</div>";
        chat.scrollTop = chat.scrollHeight;
      });

      document.getElementById('user_input').value = "";
    }
  </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_PAGE)

@app.route("/get_response", methods=['POST'])
def respond():
    user_input = request.json['message']
    bot_response = get_response(user_input)
    return jsonify({'response': bot_response})

if __name__ == "__main__":
    app.run(debug=True)

