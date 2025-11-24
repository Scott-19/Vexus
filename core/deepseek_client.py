
import requests
import json
import time
from config import config

class DeepSeekClient:
    def __init__(self):
        self.api_key = config.DEEPSEEK_API_KEY
        self.base_url = "https://api.deepseek.com/v1/chat/completions"
        self.last_request_time = 0
        self.request_delay = 1  # Evitar rate limiting

    def chat(self, message):
        print(f"🔍 [DEEPSEEK_CLIENT] Iniciando chat...")
        print(f"🔑 API Key length: {len(self.api_key) if self.api_key else 'MISSING'}")
        
        # Verificar API key
        if not self.api_key:
            print("❌ [DEEPSEEK_CLIENT] Modo fallback: API Key não configurada")
            return self._fallback_response(message)
        
        # Rate limiting básico
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.request_delay:
            sleep_time = self.request_delay - time_since_last
            print(f"⏰ [DEEPSEEK_CLIENT] Aguardando {sleep_time:.2f}s por rate limiting")
            time.sleep(sleep_time)
        
        try:
            print(f"🌐 [DEEPSEEK_CLIENT] Preparando request para DeepSeek API...")
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "system", 
                        "content": "Você é o Vexus, um assistente pessoal inteligente e útil. Seja conciso e direto."
                    },
                    {
                        "role": "user", 
                        "content": message
                    }
                ],
                "max_tokens": 500,
                "temperature": 0.7,
                "stream": False
            }

            print(f"📤 [DEEPSEEK_CLIENT] Enviando request...")
            self.last_request_time = time.time()
            
            response = requests.post(
                self.base_url, 
                json=payload, 
                headers=headers, 
                timeout=15
            )
            
            print(f"📡 [DEEPSEEK_CLIENT] Status Code: {response.status_code}")
            print(f"📡 [DEEPSEEK_CLIENT] Response Headers: {dict(response.headers)}")

            if response.status_code == 200:
                data = response.json()
                print(f"✅ [DEEPSEEK_CLIENT] Resposta recebida com sucesso!")
                print(f"💬 [DEEPSEEK_CLIENT] Conteúdo resposta: {data['choices'][0]['message']['content'][:100]}...")
                return data['choices'][0]['message']['content']
                
            else:
                error_detail = response.text
                print(f"❌ [DEEPSEEK_CLIENT] Erro na API: {response.status_code}")
                print(f"❌ [DEEPSEEK_CLIENT] Detalhes do erro: {error_detail}")
                
                # Tratamento específico por status code
                if response.status_code == 401:
                    return "🔐 Erro de autenticação: API Key inválida ou expirada"
                elif response.status_code == 429:
                    return "⏰ Rate limiting: Muitas requisições. Tente novamente em alguns segundos."
                elif response.status_code == 403:
                    return "🚫 Acesso proibido: Verifique permissões da API Key"
                else:
                    return self._fallback_response(message)
                    
        except requests.exceptions.Timeout:
            print("⏰ [DEEPSEEK_CLIENT] Timeout na requisição")
            return "⏰ Timeout: A API demorou muito para responder."
            
        except requests.exceptions.ConnectionError:
            print("🌐 [DEEPSEEK_CLIENT] Erro de conexão")
            return "🌐 Erro de conexão: Verifique sua internet."
            
        except Exception as e:
            print(f"💥 [DEEPSEEK_CLIENT] Exception: {type(e).__name__}: {e}")
            return self._fallback_response(message)

    def _fallback_response(self, message):
        fallback_msg = f"Vexus: Processando '{message}'. (Modo autônomo - API em manutenção)"
        print(f"🔄 [DEEPSEEK_CLIENT] Usando fallback: {fallback_msg}")
        return fallback_msg

    def test_connection(self):
        """Método para testar a conexão com a API"""
        print("🧪 [DEEPSEEK_CLIENT] Testando conexão com API...")
        test_response = self.chat("Teste de conexão - responda apenas 'OK'")
        return test_response