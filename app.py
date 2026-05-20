from flask import Flask, render_template, request, jsonify, Response
import os
import logging
import random
import json
from datetime import datetime
from aliyun_llm import AliyunLLM

app = Flask(__name__)
app.secret_key = os.urandom(24)

llm = AliyunLLM()

# 配置日志系统
LOG_DIR = '/usr/mypage/logs'
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# 设置访问日志
access_logger = logging.getLogger('access_logger')
access_logger.setLevel(logging.INFO)
access_handler = logging.FileHandler(os.path.join(LOG_DIR, 'access.log'))
access_handler.setLevel(logging.INFO)
access_formatter = logging.Formatter('%(message)s')
access_handler.setFormatter(access_formatter)
access_logger.addHandler(access_handler)

# 设置应用日志
app_logger = logging.getLogger('app_logger')
app_logger.setLevel(logging.INFO)
app_handler = logging.FileHandler(os.path.join(LOG_DIR, 'app.log'))
app_handler.setLevel(logging.INFO)
app_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
app_handler.setFormatter(app_formatter)
app_logger.addHandler(app_handler)

# 请求前钩子 - 记录访问日志
@app.before_request
def log_request():
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    remote_addr = request.remote_addr
    method = request.method
    path = request.path
    user_agent = request.headers.get('User-Agent', 'N/A')
    referrer = request.headers.get('Referrer', 'N/A')

    log_line = f"[{timestamp}] {remote_addr} - {method} {path} - UA: {user_agent} - Referrer: {referrer}"
    access_logger.info(log_line)
    app_logger.info(f"Request: {method} {path} from {remote_addr}")

AI_APPS = [
    {
        'id': 'interview',
        'name': 'AI模拟面试',
        'description': '基于阿里云大模型的智能面试助手，根据简历进行针对性面试',
        'icon': '🎯',
        'route': '/app/interview'
    },
    {
        'id': 'pet-coin',
        'name': '宠物冥币定制',
        'description': '为已故宠物定制专属冥币，让爱跨越生死',
        'icon': '💰',
        'route': '/app/pet-coin'
    },
    {
        'id': 'text-generator',
        'name': '文本生成器',
        'description': '基于大模型的智能文本生成，支持多种创作场景',
        'icon': '✍️',
        'route': '/app/text-generator'
    },
    {
        'id': 'chat-assistant',
        'name': '智能对话助手',
        'description': '多轮对话式AI助手，提供专业咨询服务',
        'icon': '💬',
        'route': '/app/chat-assistant'
    },
    {
        'id': 'summary-tool',
        'name': '文本摘要工具',
        'description': '快速提炼长文本核心内容，高效获取信息',
        'icon': '📝',
        'route': '/app/summary-tool'
    }
]

PET_TYPE_MAP = {
    'cat': {'name': '小猫咪', 'icon': '🐱', 'themes': ['小鱼干', '毛线球', '猫薄荷', '纸箱子', '晒太阳', '逗猫棒']},
    'dog': {'name': '小狗狗', 'icon': '🐶', 'themes': ['骨头', '飞盘', '网球', '火腿肠', '撒欢跑', '摇尾巴']},
    'hamster': {'name': '仓鼠', 'icon': '🐹', 'themes': ['瓜子', '跑轮', '棉花窝', '面包虫', '磨牙石', '藏食物']},
    'rabbit': {'name': '兔子', 'icon': '🐰', 'themes': ['胡萝卜', '干草', '牧草', '白菜叶', '蹦跳', '耳朵']},
    'bird': {'name': '小鸟', 'icon': '🐦', 'themes': ['谷粒', '小米', '羽毛', '歌唱', '树枝', '飞翔']},
    'fish': {'name': '小鱼', 'icon': '🐟', 'themes': ['鱼食', '水草', '小虾', '气泡', '游泳', '吐泡泡']},
    'turtle': {'name': '小乌龟', 'icon': '🐢', 'themes': ['龟粮', '晒台', '水草', '慢悠悠', '游泳', '缩壳']},
    'other': {'name': '小宠物', 'icon': '🐾', 'themes': ['爱心', '零食', '玩具', '陪伴', '快乐', '忠诚']}
}

COIN_VALUES = ['100万', '500万', '1000万', '5000万', '1亿', '5亿', '10亿']
COIN_TITLES = ['专属冥币', '特制冥币', '限定冥币', '珍藏冥币', '纪念冥币']

@app.route('/')
def index():
    return render_template('index.html', apps=AI_APPS)

@app.route('/app/<app_id>')
def app_page(app_id):
    app_info = next((a for a in AI_APPS if a['id'] == app_id), None)
    if not app_info:
        return "应用不存在", 404

    if app_id == 'pet-coin':
        return render_template('pet-coin.html', app=app_info)
    if app_id == 'interview':
        return render_template('interview.html', app=app_info)

    return render_template('app.html', app=app_info)

@app.route('/api/pet-coin', methods=['POST'])
def generate_pet_coin():
    data = request.get_json()
    pet_type = data.get('petType', 'other')
    pet_name = data.get('petName', '')
    pet_features = data.get('petFeatures', '')

    app_logger.info(f"宠物冥币生成: {pet_name} ({pet_type})")

    type_info = PET_TYPE_MAP.get(pet_type, PET_TYPE_MAP['other'])

    selected_themes = random.sample(type_info['themes'], min(2, len(type_info['themes'])))
    theme1 = selected_themes[0] if len(selected_themes) > 0 else '快乐'
    theme2 = selected_themes[1] if len(selected_themes) > 1 else '陪伴'

    coin_title = random.choice(COIN_TITLES)
    coin_value = random.choice(COIN_VALUES)

    coin_name = f"{pet_name}专属{theme1}{theme2}{coin_title}"
    coin_desc = f"为{pet_features}的{type_info['name']}{pet_name}特别定制，采用{theme1}和{theme2}图案，面值{coin_value}冥币，保佑{pet_name}在冥界富足快乐"

    response = {
        'status': 'success',
        'coinName': coin_name,
        'coinDesc': coin_desc,
        'coinTitle': coin_title,
        'coinIcon': type_info['icon'],
        'coinValue': coin_value,
        'petName': pet_name,
        'petTypeName': type_info['name'],
        'themes': selected_themes
    }

    app_logger.info(f"冥币生成成功: {coin_name}")
    return jsonify(response)

@app.route('/api/interview/chat', methods=['POST'])
def interview_chat():
    data = request.get_json()
    session_id = data.get('sessionId', '')
    message = data.get('message', '')

    app_logger.info(f"面试会话: {session_id}, 消息长度: {len(message)}")

    def generate():
        try:
            for chunk in llm.chat_stream(session_id, message):
                yield f"data: {json.dumps({'content': chunk}, ensure_ascii=False)}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            app_logger.error(f"面试API错误: {str(e)}")
            yield f"data: {json.dumps({'content': f'抱歉，发生了错误：{str(e)}'}, ensure_ascii=False)}\n\n"

    return Response(generate(), mimetype='text/event-stream')

@app.route('/api/<app_id>', methods=['POST'])
def api_call(app_id):
    data = request.get_json()
    user_input = data.get('input', '')

    app_logger.info(f"API Call: {app_id} - Input length: {len(user_input)}")

    response = {
        'status': 'success',
        'app_id': app_id,
        'input': user_input,
        'output': f'这是模拟的{app_id}返回结果。您输入的内容是：{user_input}'
    }

    app_logger.info(f"API Response: {app_id} - Success")
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
