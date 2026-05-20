import requests
import json
import logging
from typing import List, Dict, Optional
from datetime import datetime

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

# 配置AI交互日志
ai_logger = logging.getLogger('ai_interaction')
ai_logger.setLevel(logging.INFO)
ai_handler = logging.FileHandler('/usr/mypage/logs/ai_interaction.log')
ai_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ai_handler.setFormatter(ai_formatter)
ai_logger.addHandler(ai_handler)


class AliyunLLM:
    def __init__(self, api_key: str = ALIYUN_API_KEY):
        self.api_key = api_key
        self.session_store: Dict[str, List[Dict]] = {}
        ai_logger.info("=" * 80)
        ai_logger.info("AliyunLLM 初始化完成")

    def chat(self, session_id: str, user_input: str, system_prompt: str = SYSTEM_PROMPT) -> str:
        ai_logger.info("=" * 80)
        ai_logger.info(f"[会话 {session_id}] 开始聊天")
        
        if session_id not in self.session_store:
            self.session_store[session_id] = [
                {"role": "system", "content": system_prompt}
            ]
            ai_logger.info(f"[会话 {session_id}] 创建新会话，已设置系统提示词")

        self.session_store[session_id].append({
            "role": "user",
            "content": user_input
        })
        ai_logger.info(f"[会话 {session_id}] 用户输入: {user_input[:100]}..." if len(user_input) > 100 else f"[会话 {session_id}] 用户输入: {user_input}")

        try:
            ai_logger.info(f"[会话 {session_id}] 正在调用阿里云大模型API...")
            response = self._call_api(self.session_store[session_id])
            assistant_response = response.get("output", {}).get("text", "")
            
            ai_logger.info(f"[会话 {session_id}] [大模型返回] 成功获取响应")
            ai_logger.info(f"[会话 {session_id}] [大模型返回] 内容: {assistant_response[:200]}..." if len(assistant_response) > 200 else f"[会话 {session_id}] [大模型返回] 内容: {assistant_response}")

            self.session_store[session_id].append({
                "role": "assistant",
                "content": assistant_response
            })

            return assistant_response
        except Exception as e:
            error_msg = f"抱歉，发生了错误：{str(e)}"
            ai_logger.error(f"[会话 {session_id}] [兜底回答] API调用失败，返回兜底错误信息: {error_msg}")
            return error_msg

    def chat_stream(self, session_id: str, user_input: str, system_prompt: str = SYSTEM_PROMPT):
        ai_logger.info("=" * 80)
        ai_logger.info(f"[会话 {session_id}] 开始流式聊天")
        
        if session_id not in self.session_store:
            self.session_store[session_id] = [
                {"role": "system", "content": system_prompt}
            ]
            ai_logger.info(f"[会话 {session_id}] 创建新会话，已设置系统提示词")

        self.session_store[session_id].append({
            "role": "user",
            "content": user_input
        })
        ai_logger.info(f"[会话 {session_id}] 用户输入: {user_input[:100]}..." if len(user_input) > 100 else f"[会话 {session_id}] 用户输入: {user_input}")

        full_response = ""
        try:
            ai_logger.info(f"[会话 {session_id}] 正在调用阿里云大模型流式API...")
            for chunk in self._call_api_stream(self.session_store[session_id]):
                if chunk:
                    full_response += chunk
                    yield chunk

            ai_logger.info(f"[会话 {session_id}] [大模型返回] 流式响应完成")
            ai_logger.info(f"[会话 {session_id}] [大模型返回] 完整内容: {full_response[:200]}..." if len(full_response) > 200 else f"[会话 {session_id}] [大模型返回] 完整内容: {full_response}")

            if full_response:
                self.session_store[session_id].append({
                    "role": "assistant",
                    "content": full_response
                })

        except Exception as e:
            error_msg = f"抱歉，发生了错误：{str(e)}"
            ai_logger.error(f"[会话 {session_id}] [兜底回答] API调用失败，返回兜底错误信息: {error_msg}")
            yield error_msg

    def _call_api(self, messages: List[Dict]) -> Dict:
        ai_logger.info(f"[API调用] 发送消息数: {len(messages)}")
        
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

        ai_logger.info(f"[API调用] 请求URL: {ALIYUN_API_URL}")
        response = requests.post(ALIYUN_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        ai_logger.info(f"[API调用] HTTP状态码: {response.status_code}")
        
        return result

    def _call_api_stream(self, messages: List[Dict]):
        ai_logger.info(f"[流式API调用] 发送消息数: {len(messages)}")
        
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

        ai_logger.info(f"[流式API调用] 请求URL: {ALIYUN_API_URL}")
        response = requests.post(ALIYUN_API_URL, headers=headers, json=payload, stream=True)
        response.raise_for_status()
        
        ai_logger.info(f"[流式API调用] HTTP状态码: {response.status_code}")

        chunk_count = 0
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data:'):
                    try:
                        data = json.loads(line[5:])
                        if 'output' in data and 'choices' in data['output']:
                            for choice in data['output']['choices']:
                                if 'message' in choice and 'content' in choice['message']:
                                    content = choice['message']['content']
                                    chunk_count += 1
                                    if chunk_count % 10 == 0:
                                        ai_logger.debug(f"[流式API调用] 已接收 {chunk_count} 个数据块")
                                    yield content
                    except Exception:
                        continue
        
        ai_logger.info(f"[流式API调用] 共接收 {chunk_count} 个数据块")

    def clear_session(self, session_id: str):
        if session_id in self.session_store:
            del self.session_store[session_id]

    def get_session_history(self, session_id: str) -> List[Dict]:
        return self.session_store.get(session_id, [])
