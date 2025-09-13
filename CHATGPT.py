# chatbot_app.py
from flask import Flask, request, jsonify, render_template_string
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Choose a conversational model (small, runs locally on CPU; change to medium/large if you have GPU)
MODEL_NAME = "microsoft/DialoGPT-small"

print("Loading model... (this may take a minute)")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
model.eval()

app = Flask(__name__)

# Keep a simple history per session id (in-memory). For production use a DB or Redis.
conversations = {}

HTML_UI = """
<!doctype html>
<title>Mini AI Chat</title>
<style>
body{font-family:sans-serif;display:flex;align-items:center;flex-direction:column;padding:20px}
#chat{width:720px;max-width:95%;height:420px;border:1px solid #ddd;padding:12px;overflow:auto;background:#fafafa}
.user{color:#0a58ca;margin:6px 0}
.bot{color:#111;margin:6px 0}
form{width:720px;max-width:95%;display:flex;margin-top:8px}
input{flex:1;padding:8px}
button{padding:8px 12px}
</style>
<div id=chat></div>
<form id=f>
<input id=q autocomplete="off" placeholder="Say something..." />
<button>Send</button>
</form>
<script>
const chat=document.getElementById('chat'), f=document.getElementById('f'), q=document.getElementById('q');
f.onsubmit=async e=>{
  e.preventDefault();
  const text=q.value.trim(); if(!text) return;
  append('You', text, 'user');
  q.value='';
  const res=await fetch('/ask', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({q:text, sid:'default'})});
  const j=await res.json();
  append('AI', j.answer, 'bot');
  chat.scrollTop=chat.scrollHeight;
}
function append(name, text, cls){
  const d=document.createElement('div'); d.className=cls; d.textContent = name + ': ' + text; chat.appendChild(d);
}
</script>
"""

def generate_reply(session_id, user_text, max_length=200):
    # Keep chat history token ids for DialoGPT
    history = conversations.get(session_id, None)
    new_user_input_ids = tokenizer.encode(user_text + tokenizer.eos_token, return_tensors='pt')
    if history is not None:
        bot_input_ids = torch.cat([history, new_user_input_ids], dim=-1)
    else:
        bot_input_ids = new_user_input_ids

    with torch.no_grad():
        chat_history_ids = model.generate(
            bot_input_ids,
            max_length=bot_input_ids.shape[-1] + 50,
            pad_token_id=tokenizer.eos_token_id,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            temperature=0.7,
            eos_token_id=tokenizer.eos_token_id
        )

    # store conversation history for session
    conversations[session_id] = chat_history_ids
    reply_ids = chat_history_ids[:, bot_input_ids.shape[-1]:]
    reply_text = tokenizer.decode(reply_ids[0], skip_special_tokens=True)
    return reply_text

@app.route("/")
def index():
    return render_template_string(HTML_UI)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(force=True)
    q = data.get("q", "")
    sid = data.get("sid", "default")
    if not q:
        return jsonify({"answer": "I didn't get that. Try again."})
    try:
        ans = generate_reply(sid, q)
    except Exception as e:
        ans = "Sorry, error generating reply: " + str(e)
    return jsonify({"answer": ans})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
