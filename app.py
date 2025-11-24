from flask import Flask, render_template, request, jsonify
import os
import requests
from core.vexus import Vexus
from config import config

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
    return jsonify({
        "api_key_exists": bool(config.DEEPSEEK_API_KEY),
        "api_key_length": len(config.DEEPSEEK_API_KEY) if config.DEEPSEEK_API_KEY else 0,
        "api_key_prefix": config.DEEPSEEK_API_KEY[:10] + "..." if config.DEEPSEEK_API_KEY else "None",
        "status": "DEBUG ACTIVE"
    })

@app.route('/test-api-direct')
def test_api_direct():
    """Teste DIRETO da API DeepSeek - sem lógica complexa"""
    
    # Payload MUITO simples
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": "Diga apenas OK"}
        ],
        "max_tokens": 5
    }
    
    headers = {
        "Authorization": f"Bearer {config.DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            json=payload,
            headers=headers,
            timeout=10
        )
        
        return jsonify({
            "status_code": response.status_code,
            "response_body": response.json() if response.status_code == 200 else response.text,
            "api_key_debug": f"{len(config.DEEPSEEK_API_KEY)} chars" if config.DEEPSEEK_API_KEY else "MISSING"
        })
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "type": type(e).__name__
        })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
