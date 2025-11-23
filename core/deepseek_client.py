import requests
import json
from config import config

class DeepSeekClient:
    def __init__(self):
        self.api_key = config.DEEPSEEK_API_KEY
        self.base_url = config.DEEPSEEK_API_URL
        
    def chat(self, message):
        if not self.api_key:
            return self._fallback_response(message)
            
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "Você é o Vexus, um assistente pessoal inteligente e útil."},
                    {"role": "user", "content": message}
                ],
                "stream": False
            }
            
            response = requests.post(self.base_url, json=payload, headers=headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return data['choices'][0]['message']['content']
            else:
                return self._fallback_response(message)
                
        except Exception as e:
            print(f"Erro DeepSeek: {e}")
            return self._fallback_response(message)
    
    def _fallback_response(self, message):
        return f"Vexus: Processando '{message}'. (Modo autônomo ativado)"
