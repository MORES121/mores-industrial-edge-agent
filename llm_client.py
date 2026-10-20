# ==============================================================================
# MORES Industrial Edge Agent - LLM Gateway
# 大模型网关接口，支持 DeepSeek / Qwen 等云端模型。
# ==============================================================================

import requests
import os

class LLMClient:
    def __init__(self, provider="deepseek"):
        self.provider = provider
        self.deepseek_key = os.getenv('DEEPSEEK_API_KEY', 'YOUR_DEEPSEEK_API_KEY')
        self.qwen_key = os.getenv('QWEN_API_KEY', 'YOUR_QWEN_API_KEY')

    def chat(self, prompt):
        result = self._call_deepseek(prompt)
        if result and 'choices' in result:
            return result
        return {"choices": [{"message": {"content": "服务暂时不可用，请稍后重试"}}]}

    def _call_deepseek(self, prompt):
        try:
            response = requests.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.deepseek_key}"
                },
                json={
                    "model": "deepseek-chat",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7
                },
                timeout=30
            )
            return response.json()
        except Exception as e:
            print(f"DeepSeek 请求失败: {e}")
            return None

llm = LLMClient()