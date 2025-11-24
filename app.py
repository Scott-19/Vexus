from flask import Flask, render_template, request, jsonify
import os
from core.vexus import Vexus

app = Flask(__name__)
vexus = Vexus()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    response = vexus.process_message(user_message)
    return jsonify(response)

@app.route('/health')
def health():
    return jsonify({
        "status": "VEXUS AI ONLINE", 
        "version": "1.0-ai",
        "capabilities": ["deepseek_integration"]
    })

@app.route('/debug')
def debug():
    from config import config
    return jsonify({
        "api_key_exists": bool(config.DEEPSEEK_API_KEY),
        "api_key_length": len(config.DEEPSEEK_API_KEY) if config.DEEPSEEK_API_KEY else 0,
        "api_key_prefix": config.DEEPSEEK_API_KEY[:10] + "..." if config.DEEPSEEK_API_KEY else "None",
        "status": "DEBUG ACTIVE"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
