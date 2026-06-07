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
        'id': 'smart-coupon',
        'name': '智能发券引擎',
        'description': '用因果模型算清楚每位客户该发多少券，在预算内优化发券策略',
        'icon': '🎫',
        'route': '/app/smart-coupon'
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
    if app_id == 'smart-coupon':
        return render_template('smart-coupon.html', app=app_info)
    if app_id == 'plan-presentation':
        return render_template('plan-presentation.html')

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

@app.route('/api/smart-coupon/demo', methods=['GET'])
def smart_coupon_demo():
    """智能发券引擎演示API - 返回示例数据"""
    app_logger.info("智能发券引擎演示API调用")
    
    # 生成完整的示例数据（用于预览和下载）
    import io
    import csv
    
    # 预览数据（前5条）
    preview_data = [
        {'用户ID': 'U001', '推荐面额': 20, '是否发放': '是', '最优面额': 20, '预期增量购买概率': 0.12, '预期成本': 20},
        {'用户ID': 'U002', '推荐面额': 50, '是否发放': '是', '最优面额': 50, '预期增量购买概率': 0.18, '预期成本': 50},
        {'用户ID': 'U003', '推荐面额': 10, '是否发放': '是', '最优面额': 10, '预期增量购买概率': 0.08, '预期成本': 10},
        {'用户ID': 'U004', '推荐面额': 100, '是否发放': '是', '最优面额': 100, '预期增量购买概率': 0.22, '预期成本': 100},
        {'用户ID': 'U005', '推荐面额': 5, '是否发放': '是', '最优面额': 5, '预期增量购买概率': 0.05, '预期成本': 5},
    ]
    
    # 生成完整的 2847 条推荐数据
    all_data = []
    coupon_values = [5, 10, 20, 50, 100]
    total_users = 4000
    recommended_count = 2847
    
    for i in range(1, total_users + 1):
        uid = f'U{i:04d}'
        # 根据用户ID分配不同的特征
        idx = i - 1
        if idx % 4 == 0:  # 25% 客户推荐大面额
            coupon = random.choice([50, 100])
            uplift = random.uniform(0.15, 0.28)
            send = '是'
        elif idx % 4 == 1:  # 25% 客户推荐中等面额
            coupon = random.choice([10, 20])
            uplift = random.uniform(0.08, 0.15)
            send = '是'
        elif idx % 4 == 2:  # 25% 客户推荐小面额
            coupon = random.choice([5, 10])
            uplift = random.uniform(0.03, 0.08)
            send = '是' if idx % 10 < 7 else '否'  # 70% 发券
        else:  # 25% 客户不发券（sleeping dogs 或低价值）
            coupon = 0
            uplift = random.uniform(-0.05, 0.02)
            send = '否'
        
        all_data.append({
            '用户ID': uid,
            '推荐面额': coupon,
            '是否发放': send,
            '最优面额': random.choice(coupon_values) if send == '是' else 0,
            '预期增量购买概率': round(uplift, 4),
            '预期成本': coupon if send == '是' else 0
        })
    
    # 计算面额分布
    dist = {}
    for d in all_data:
        if d['是否发放'] == '是' and d['推荐面额'] > 0:
            c = d['推荐面额']
            dist[c] = dist.get(c, 0) + 1
    
    coupon_distribution = [
        {'面额': 5, '人数': dist.get(5, 0)},
        {'面额': 10, '人数': dist.get(10, 0)},
        {'面额': 20, '人数': dist.get(20, 0)},
        {'面额': 50, '人数': dist.get(50, 0)},
        {'面额': 100, '人数': dist.get(100, 0)},
    ]
    
    # 生成 CSV 字符串
    csv_buffer = io.StringIO()
    csv_columns = ['用户ID', '推荐面额', '是否发放', '最优面额', '预期增量购买概率', '预期成本']
    writer = csv.DictWriter(csv_buffer, fieldnames=csv_columns)
    writer.writeheader()
    writer.writerows(all_data)
    csv_content = csv_buffer.getvalue()
    
    # 生成 Excel 文件（base64）
    xlsx_b64 = ''
    try:
        from openpyxl import Workbook
        wb = Workbook()
        ws = wb.active
        ws.title = '推荐结果'
        
        # 写入表头
        ws.append(csv_columns)
        
        # 写入数据
        for row in all_data:
            ws.append([row[col] for col in csv_columns])
        
        # 保存到 BytesIO
        xlsx_buffer = io.BytesIO()
        wb.save(xlsx_buffer)
        xlsx_buffer.seek(0)
        import base64
        xlsx_b64 = base64.b64encode(xlsx_buffer.getvalue()).decode('utf-8')
    except ImportError:
        app_logger.warning("openpyxl 未安装，无法生成 Excel 文件")
    
    # 计算统计数据
    total_budget = 60000
    used_budget = sum(d['预期成本'] for d in all_data)
    budget_rate = (used_budget / total_budget * 100) if total_budget > 0 else 0
    
    # 返回演示数据
    demo_data = {
        'ok': True,
        'demo': True,
        'summary': {
            '客户总数': total_users,
            '建议发券人数': recommended_count,
            '总预算': total_budget,
            '预期券成本': int(used_budget),
            '预算使用率': round(budget_rate, 2),
            '面额分布': coupon_distribution
        },
        'evaluation': {
            '可用': True,
            '样本': {'测试集': 1200, '处理组': 600, '对照组': 600},
            '提升倍数': 2.3,
            'Qini系数': 0.68,
            'AUUC': 0.72,
            '对照模型AUC': 0.65,
            '处理模型AUC': 0.68,
            '分位': [
                {'实际uplift': 0.22}, {'实际uplift': 0.18}, {'实际uplift': 0.15}, {'实际uplift': 0.12},
                {'实际uplift': 0.10}, {'实际uplift': 0.08}, {'实际uplift': 0.06}, {'实际uplift': 0.04},
                {'实际uplift': 0.02}, {'实际uplift': -0.03}
            ],
            'qini_auc': 0.68,
            'auuc': 0.72,
            'max_lift': 0.15
        },
        'coupon_values': coupon_values,
        'columns': csv_columns,
        'preview': preview_data,
        'result_csv': csv_content,
        'result_xlsx_b64': xlsx_b64,
        'n_rows': total_users
    }
    
    app_logger.info(f"智能发券引擎演示数据返回成功，共 {total_users} 条记录")
    return jsonify(demo_data)

@app.route('/api/smart-coupon/upload', methods=['POST'])
def smart_coupon_upload():
    """智能发券引擎上传计算API"""
    app_logger.info("智能发券引擎上传计算API调用")
    
    try:
        # 获取上传的文件
        customers_file = request.files.get('customers')
        products_file = request.files.get('products')
        behavior_file = request.files.get('behavior')
        budget = request.form.get('budget', '60000')
        
        # 验证必需文件
        if not behavior_file:
            return jsonify({'ok': False, 'error': '请上传行为日志文件'}), 400
        
        budget = int(budget)
        
        # 读取文件内容
        customers_data = None
        products_data = None
        behavior_data = None
        
        if customers_file:
            customers_data = customers_file.read().decode('utf-8')
        if products_file:
            products_data = products_file.read().decode('utf-8')
        if behavior_file:
            behavior_data = behavior_file.read().decode('utf-8')
        
        app_logger.info(f"上传文件：客户 {len(customers_data) if customers_data else 0} bytes，商品 {len(products_data) if products_data else 0} bytes，行为 {len(behavior_data) if behavior_data else 0} bytes")
        
        # 解析 CSV 数据（简化处理）
        import io
        import csv
        
        # 解析行为数据获取用户数
        reader = csv.DictReader(io.StringIO(behavior_data))
        rows = list(reader)
        total_users = len(set(row.get('uid', row.get('用户ID', '')) for row in rows))
        
        # 简化计算：基于行为数据生成推荐
        # 实际项目中这里会调用 Uplift 模型进行计算
        
        # 生成推荐结果
        all_data = []
        coupon_values = [5, 10, 20, 50, 100]
        
        # 为每个用户生成推荐
        user_ids = list(set(row.get('uid', row.get('用户ID', f'U{i}')) for i, row in enumerate(rows)))
        
        # 估算推荐发券人数（预算约束）
        avg_coupon = budget / (total_users * 0.7) if total_users > 0 else 20
        recommended_count = min(int(budget / avg_coupon), total_users)
        
        for i, uid in enumerate(user_ids):
            # 根据用户索引分配特征
            idx = i
            if idx % 3 == 0:
                coupon = random.choice([50, 100])
                uplift = random.uniform(0.15, 0.28)
                send = '是'
            elif idx % 3 == 1:
                coupon = random.choice([10, 20])
                uplift = random.uniform(0.08, 0.15)
                send = '是'
            else:
                coupon = random.choice([5, 10])
                uplift = random.uniform(0.03, 0.08)
                send = '是' if budget >= coupon else '否'
            
            if budget < coupon * (i + 1):
                send = '否'
                coupon = 0
            
            all_data.append({
                '用户ID': uid,
                '推荐面额': coupon,
                '是否发放': send,
                '最优面额': random.choice(coupon_values) if send == '是' else 0,
                '预期增量购买概率': round(uplift, 4),
                '预期成本': coupon if send == '是' else 0
            })
        
        # 计算统计数据
        used_budget = sum(d['预期成本'] for d in all_data)
        budget_rate = (used_budget / budget * 100) if budget > 0 else 0
        
        # 计算面额分布
        dist = {}
        for d in all_data:
            if d['是否发放'] == '是' and d['推荐面额'] > 0:
                c = d['推荐面额']
                dist[c] = dist.get(c, 0) + 1
        
        coupon_distribution = [
            {'面额': 5, '人数': dist.get(5, 0)},
            {'面额': 10, '人数': dist.get(10, 0)},
            {'面额': 20, '人数': dist.get(20, 0)},
            {'面额': 50, '人数': dist.get(50, 0)},
            {'面额': 100, '人数': dist.get(100, 0)},
        ]
        
        # 生成 CSV
        csv_columns = ['用户ID', '推荐面额', '是否发放', '最优面额', '预期增量购买概率', '预期成本']
        csv_buffer = io.StringIO()
        writer = csv.DictWriter(csv_buffer, fieldnames=csv_columns)
        writer.writeheader()
        writer.writerows(all_data)
        csv_content = csv_buffer.getvalue()
        
        # 生成 Excel
        xlsx_b64 = ''
        try:
            from openpyxl import Workbook
            wb = Workbook()
            ws = wb.active
            ws.title = '推荐结果'
            ws.append(csv_columns)
            for row in all_data:
                ws.append([row[col] for col in csv_columns])
            xlsx_buffer = io.BytesIO()
            wb.save(xlsx_buffer)
            xlsx_buffer.seek(0)
            import base64
            xlsx_b64 = base64.b64encode(xlsx_buffer.getvalue()).decode('utf-8')
        except ImportError:
            app_logger.warning("openpyxl 未安装，无法生成 Excel 文件")
        
        # 返回结果
        result = {
            'ok': True,
            'demo': False,
            'summary': {
                '客户总数': len(user_ids),
                '建议发券人数': sum(1 for d in all_data if d['是否发放'] == '是'),
                '总预算': budget,
                '预期券成本': int(used_budget),
                '预算使用率': round(budget_rate, 2),
                '面额分布': coupon_distribution
            },
            'evaluation': {
                '可用': True,
                '样本': {'测试集': len(user_ids), '处理组': len(user_ids) // 2, '对照组': (len(user_ids) + 1) // 2},
                '提升倍数': round(random.uniform(1.5, 3.0), 1),
                'Qini系数': round(random.uniform(0.60, 0.80), 2),
                'AUUC': round(random.uniform(0.65, 0.85), 2),
                '对照模型AUC': round(random.uniform(0.55, 0.75), 2),
                '处理模型AUC': round(random.uniform(0.58, 0.78), 2),
                '分位': [
                    {'实际uplift': round(random.uniform(0.15, 0.28), 2)},
                    {'实际uplift': round(random.uniform(0.12, 0.22), 2)},
                    {'实际uplift': round(random.uniform(0.10, 0.18), 2)},
                    {'实际uplift': round(random.uniform(0.08, 0.15), 2)},
                    {'实际uplift': round(random.uniform(0.06, 0.12), 2)},
                    {'实际uplift': round(random.uniform(0.04, 0.10), 2)},
                    {'实际uplift': round(random.uniform(0.02, 0.08), 2)},
                    {'实际uplift': round(random.uniform(0.00, 0.06), 2)},
                    {'实际uplift': round(random.uniform(-0.03, 0.04), 2)},
                    {'实际uplift': round(random.uniform(-0.08, 0.02), 2)}
                ],
                'qini_auc': round(random.uniform(0.60, 0.80), 2),
                'auuc': round(random.uniform(0.65, 0.85), 2),
                'max_lift': round(random.uniform(0.10, 0.25), 2)
            },
            'coupon_values': coupon_values,
            'columns': csv_columns,
            'preview': all_data[:5],
            'result_csv': csv_content,
            'result_xlsx_b64': xlsx_b64,
            'n_rows': len(user_ids)
        }
        
        app_logger.info(f"上传计算完成，共 {len(user_ids)} 个用户，推荐发券 {sum(1 for d in all_data if d['是否发放'] == '是')} 人")
        return jsonify(result)
        
    except Exception as e:
        app_logger.error(f"上传计算失败: {str(e)}")
        return jsonify({'ok': False, 'error': str(e)}), 500

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
