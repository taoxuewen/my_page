import requests
import json
from typing import List, Dict, Optional

ALIYUN_API_KEY = "sk-d138bfeb74ea413284900ae38a106c9e"
ALIYUN_API_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"

SYSTEM_PROMPT = """你是一位专业的面试官，正在进行一场模拟面试。
- 首先仔细阅读用户的简历
- 根据简历内容提出2-5个针对性问题
- 问题要逐步深入，从简单到复杂
- 每次只问一个问题
- 每个问题后面标注预估回答时间，格式：[⏱️ X分钟]
- 语气要专业、友好
- 面试过程中根据回答进行追问
- 最后给出面试总结和建议"""


class AliyunLLM:
    def __init__(self, api_key: str = ALIYUN_API_KEY):
        self.api_key = api_key
        self.session_store: Dict[str, List[Dict]] = {}

    def chat(self, session_id: str, user_input: str, system_prompt: str = SYSTEM_PROMPT) -> str:
        if session_id not in self.session_store:
            self.session_store[session_id] = [
                {"role": "system", "content": system_prompt}
            ]

        self.session_store[session_id].append({
            "role": "user",
            "content": user_input
        })

        try:
            response = self._call_api(self.session_store[session_id])
            assistant_response = response.get("output", {}).get("text", "")

            self.session_store[session_id].append({
                "role": "assistant",
                "content": assistant_response
            })

            return assistant_response
        except Exception as e:
            return f"抱歉，发生了错误：{str(e)}"

    def chat_stream(self, session_id: str, user_input: str, system_prompt: str = SYSTEM_PROMPT):
        if session_id not in self.session_store:
            self.session_store[session_id] = [
                {"role": "system", "content": system_prompt}
            ]

        self.session_store[session_id].append({
            "role": "user",
            "content": user_input
        })

        full_response = ""
        try:
            for chunk in self._call_api_stream(self.session_store[session_id]):
                if chunk:
                    full_response += chunk
                    yield chunk

            if full_response:
                self.session_store[session_id].append({
                    "role": "assistant",
                    "content": full_response
                })

        except Exception as e:
            yield f"抱歉，发生了错误：{str(e)}"

    def _call_api(self, messages: List[Dict]) -> Dict:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "qwen-turbo",
            "input": {
                "messages": messages
            },
            "parameters": {
                "result_format": "message"
            }
        }

        response = requests.post(ALIYUN_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()

    def _call_api_stream(self, messages: List[Dict]):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "text/event-stream"
        }

        payload = {
            "model": "qwen-turbo",
            "input": {
                "messages": messages
            },
            "parameters": {
                "result_format": "message",
                "incremental_output": True
            }
        }

        response = requests.post(ALIYUN_API_URL, headers=headers, json=payload, stream=True)
        response.raise_for_status()

        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data:'):
                    try:
                        data = json.loads(line[5:])
                        if 'output' in data and 'choices' in data['output']:
                            for choice in data['output']['choices']:
                                if 'message' in choice and 'content' in choice['message']:
                                    yield choice['message']['content']
                    except Exception:
                        continue

    def clear_session(self, session_id: str):
        if session_id in self.session_store:
            del self.session_store[session_id]

    def get_session_history(self, session_id: str) -> List[Dict]:
        return self.session_store.get(session_id, [])
