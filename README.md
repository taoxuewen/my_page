<div align="center">

# ✶ AI Studio

**一个用 Flask 搭建的个人 AI 应用展示门户**

把好用的 AI，做成真正能用的产品。

</div>

---

## 简介

AI Studio 是一个个人 AI 应用展示门户：首页以应用墙形式列出多个 AI 小应用，每个应用都有独立页面与后端接口，对外展示能力、对内做 Demo。其中「智能发券引擎」是面向 B2B 的重点对客产品页，并配有完整的智能营销引擎企划书。

整站采用统一的 **「Editorial Tech / 精炼科技编辑风」** 设计系统：暖白纸感底 + 近黑墨字 + 墨绿强调色，Fraunces 衬线标题搭配 Hanken Grotesk 正文，刻意避开千篇一律的「AI 紫色渐变」审美。

## 在线应用

| 应用 | 状态 | 说明 |
|------|------|------|
| 🎯 AI 模拟面试 | ✅ 可用 | 接入阿里云通义千问，根据简历进行 SSE 流式多轮面试 |
| 🎫 智能发券引擎 | 🟡 前端完整 | 基于 Uplift 因果模型计算每位客户的最优券面额（对客页 + 上传计算 Demo） |
| 💰 宠物冥币定制 | ✅ 可用 | 按宠物类型与特点生成专属冥币 |
| ✍️ 文本生成器 / 💬 智能对话助手 / 📝 文本摘要工具 | 🚧 敬请期待 | 占位中 |

> 另有独立路由 `/app/plan-presentation`：智能营销引擎完整企划书展示页。

## 技术栈

- **后端**：Flask + Jinja2（单体应用，模板服务端直出）
- **前端**：原生 HTML / CSS / JS，**无构建步骤**；统一设计系统 `static/css/design-system.css` + 布局基类 `templates/base.html`
- **LLM**：阿里云 DashScope（通义千问），用于面试流式对话
- **导出**：openpyxl（发券结果 Excel 下载）
- **子引擎**：`smart-coupon-engine/`（Python + scikit-learn + scipy 的 Uplift 因果发券引擎，独立可跑）

## 快速开始

```bash
# 1. 克隆
git clone https://github.com/taoxuewen/my_page.git
cd my_page

# 2. 安装依赖
pip install flask openpyxl dashscope

# 3. 配置阿里云 API Key（面试功能需要）
export ALIYUN_API_KEY="你的-dashscope-key"

# 4. 启动
python3 app.py
```

启动后访问 `http://localhost`（默认监听 `0.0.0.0:80`）。

> ⚠️ 当前默认以 `debug=True` 运行，仅适合开发/演示；生产环境请关闭 debug 并改用 gunicorn 等 WSGI 服务器。

## 项目结构

```
my_page/
├── app.py                  # Flask 主程序：路由 + 业务逻辑 + 日志
├── aliyun_llm.py           # 阿里云通义千问封装（面试流式对话）
├── templates/              # Jinja2 模板（base.html 为统一布局基类）
├── static/
│   ├── css/                # design-system.css（设计令牌+组件）+ 各页样式
│   └── js/                 # 原生 JS，无打包
├── smart-coupon-engine/    # 独立子项目：Uplift 因果发券引擎
├── docs/superpowers/       # 设计规格与实现计划
└── task_plan.md / demand.md / debug.md / test.md   # 项目活文档
```

## 项目文档

本项目维护一套「活文档」，新接手的人（或 AI）读这几份即可上手：

- **`task_plan.md`** — 项目活地图：架构、功能清单、接口契约、已知缺口、里程碑、协作规则
- **`demand.md`** — 需求记录（每个功能为满足什么需求而存在）
- **`debug.md`** — Bug 记录（现象 → 根因 → 修复 → 验证）
- **`DEPLOY_NOW.md`** — 部署生效指引（每次改动后覆盖重写，告诉部署服务器是否需重启）

## 作者

逃学文 · [github.com/taoxuewen](https://github.com/taoxuewen)

---

<div align="center">
<sub>© 2026 逃学文 · AI Studio</sub>
</div>
