from flask import Flask, request, jsonify, render_template_string
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blind_guide.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 数据模型（用户数据）
class UserData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    belong_user_id = db.Column(db.Integer, nullable=False)  # 数据归属用户ID

# 初始化数据库
with app.app_context():
    db.create_all()
    # 插入归属不同用户的测试数据
    if not UserData.query.first():
        data1 = UserData(
            title="用户1的私密笔记",
            content="用户1的银行卡、隐私信息等敏感内容",
            belong_user_id=1
        )
        data2 = UserData(
            title="用户2的个人资料",
            content="用户2的身份证、住址等敏感内容",
            belong_user_id=2
        )
        db.session.add(data1)
        db.session.add(data2)
        db.session.commit()

# ========================
# 存在漏洞的核心接口
# 隐式默认对象越权漏洞（盲眼向导漏洞）
# ========================
@app.route('/api/get_user_data', methods=['GET'])
def api_get_user_data():
    data_id = request.args.get('data_id')

    # 漏洞触发点：参数为空时，默认取第一条数据
    if not data_id:
        result = UserData.query.first()  # 无权限校验！
    else:
        result = UserData.query.filter_by(id=data_id).first()

    if not result:
        return jsonify({"code": 0, "msg": "数据不存在"}), 404

    # 直接返回敏感数据，无任何鉴权
    return jsonify({
        "code": 1,
        "data": {
            "id": result.id,
            "title": result.title,
            "content": result.content,
            "belong_user_id": result.belong_user_id
        },
        "漏洞标记": "此处存在 隐式默认对象越权漏洞（盲眼向导漏洞）",
        "发现者": "余悸",
        "CNVD编号": "CNVD-C-2026-137588"
    })

# 首页演示页面
@app.route('/')
def index():
    html = '''
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <title>盲眼向导漏洞演示平台 - 余悸原创</title>
        <style>
            body{font-family: Arial; padding: 30px; background: #f5f5f5;}
            .box{background: white; padding: 20px; border-radius: 10px; margin-bottom: 20px;}
            a{font-size: 18px; color: #2d8cf0; text-decoration: none;}
            .red{color: red; font-weight: bold;}
        </style>
    </head>
    <body>
        <h1>隐式默认对象越权漏洞（盲眼向导漏洞）</h1>
        <h3>原创发现者：余悸 | CNVD-C-2026-137588</h3>
        <div class="box">
            <h3>✅ 漏洞触发测试（点击即可复现）：</h3>
            <p><a href="/api/get_user_data" target="_blank">1. 不带 data_id 参数访问（触发漏洞）</a></p>
            <p><a href="/api/get_user_data?data_id=2" target="_blank">2. 带 data_id=2 正常访问</a></p>
        </div>
        <div class="box">
            <h3>⚠️ 漏洞原理：</h3>
            <p>接口未对 data_id 做非空校验 → 空参数时系统默认返回第一条数据 → 无权限判断 → 越权获取他人敏感数据</p>
            <p class="red">这是全新的通用逻辑漏洞类型！</p>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

