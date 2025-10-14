# app.py

from flask import Flask, render_template_string, request, jsonify
from chatbot import get_response

app = Flask(__name__)

# Simple HTML UI template
HTML_PAGE = """
<!doctype html>
<html>
<head>
  <title>AI Chatbot</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 20px; }
    #chatbox {
      border: 1px solid #ccc;
      padding: 15px;
      height: 400px;
      overflow-y: auto;
      background-color: #f9f9f9;
      border-radius: 5px;
    }
    #user_input {
      padding: 10px;
      width: 80%;
      border: 1px solid #ccc;
      border-radius: 3px;
    }
    button {
      padding: 10px 20px;
      background-color: #007bff;
      color: white;
      border: none;
      border-radius: 3px;
      cursor: pointer;
    }
    button:hover { background-color: #0056b3; }
  </style>
</head>
<body>
  <h1>AI-Powered Chatbot 🤖</h1>
  <div style="max-width:600px;">
    <div id="chatbox"></div>
    <div style="margin-top:10px;">
      <input id="user_input" type="text" placeholder="Ask something..." autofocus>
      <button onclick="send()">Send</button>
    </div>
  </div>

  <script>
  function send() {
    var user_input = document.getElementById('user_input').value.trim();
    if (!user_input) return;

    fetch("/get_response", {
      method: "POST",
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({"message": user_input})
    })
    .then(res => res.json())
    .then(data => {
      var chat = document.getElementById('chatbox');
      chat.innerHTML += "<b>You:</b> " + user_input + "<br>";
      chat.innerHTML += "<b>Bot:</b> " + data.response + "<br><br>";
      chat.scrollTop = chat.scrollHeight;
      document.getElementById('user_input').value = "";
    })
    .catch(error => {
      console.error('Error:', error);
      alert('Failed to get response. Please try again.');
    });
  }

  // Send message on Enter key
  document.getElementById('user_input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') send();
  });
  </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_PAGE)

@app.route("/get_response", methods=['POST'])
def respond():
    try:
        user_input = request.json.get('message', '')
        bot_response = get_response(user_input)
        return jsonify({'response': bot_response})
    except Exception as e:
        return jsonify({'response': 'Sorry, something went wrong. Please try again.'}), 500

if __name__ == "__main__":
    app.run(debug=True)
