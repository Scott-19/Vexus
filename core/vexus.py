from .deepseek_client import DeepSeekClient

class Vexus:
    def __init__(self):
        self.version = "1.0-ai"
        self.deepseek = DeepSeekClient()
        self.capabilities = ["chat_basic", "deepseek_integration"]
        
    def process_message(self, message):
        ai_response = self.deepseek.chat(message)
        
        return {
            "response": ai_response,
            "version": self.version,
            "sources": ["deepseek_api"]
}
