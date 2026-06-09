# task_plan.md — my_page 个人 AI 应用展示门户 · 活地图

> 本文件是**整个 my_page 项目的活地图**。任何新加入的人（或 AI）只读这一份，就能理解：
> 这个网站是什么、有哪些功能、代码长什么样、当前状态、下一步往哪走。
> 规划一旦变动，**必须同步更新本文件**（见末尾「变更日志」）。
>
> 配套文件（同在项目根目录）：
> - `demand.md` — 需求记录（用户每次提的需求 + 讨论结论，按时间倒序）
> - `debug.md`  — bug 记录（现象 → 定位 → 修复 → 验证）
> - `test.md`   — 测试记录（用例清单 + 历次运行结果）
> - 子项目 `smart-coupon-engine/` 有自己独立的 plan/demand/debug/test.md（引擎内部细节看那边）

---

## 0. 一句话项目定义

**一个用 Flask 搭的「个人 AI 应用展示门户」**：首页列出多个 AI 小应用，每个应用一个独立页面 + 后端接口，对外展示能力、对内做 demo。其中「智能发券引擎」是重点对客产品页。

- 线上：`github.com/taoxuewen/my_page.git`，主分支 `main`。
- 运行：`python3 app.py` → Flask 监听 `0.0.0.0:80`（`debug=True`）。日志写 `/usr/mypage/logs/`。

---

## 1. 系统架构

```
                          my_page（Flask 单体应用）
┌────────────────────────────────────────────────────────────────────┐
│  app.py        路由 + 业务逻辑 + 日志（access.log / app.log）          │
│   ├── 页面路由   /  ·  /app/<app_id>  ·  /app/plan-presentation       │
│   └── 接口路由   /api/interview/chat（SSE 流式，接阿里云）             │
│                  /api/pet-coin（随机生成）                            │
│                  /api/smart-coupon/demo|upload（⚠️ 当前用随机假数据）  │
│                  /api/<app_id>（通用 mock 回显）                       │
│                                                                      │
│  aliyun_llm.py  阿里云 DashScope（通义千问）封装：面试对话流式输出      │
│                                                                      │
│  templates/     Jinja2 模板（纯 HTML，无前端构建）                     │
│  static/        css/ + js/（原生，无打包）                            │
│                                                                      │
│  smart-coupon-engine/   独立子项目：Uplift 因果发券引擎（自带文档/测试）│
│  code-main/ + .zip      原始方案代码包（demo.py、方案文档）            │
└────────────────────────────────────────────────────────────────────┘
```

设计现状与原则：
- **无前端构建**：模板直出 HTML，`static/` 下原生 CSS/JS，改完刷新即生效。
- **门户与引擎解耦但尚未打通**：`smart-coupon-engine` 是完整可跑的 Uplift 引擎，但门户页 `/api/smart-coupon/*` 目前在 `app.py` 里用 `random` 造假数据演示，**没有真正调用引擎**（见 §5 缺口 G1）。
- **LLM 仅面试用到**：`aliyun_llm.py` 调阿里云千问，做简历面试的多轮流式对话；其余应用多为前端展示或 mock。

---

## 2. 功能清单（AI_APPS + 独立页）

首页 `AI_APPS` 列表（`app.py:52`）共 6 个应用：

| id | 名称 | 状态 | 说明 |
|----|------|------|------|
| `interview` | 🎯 AI模拟面试 | ✅ 真实可用 | 接阿里云千问，SSE 流式多轮面试（专属模板 `interview.html`） |
| `smart-coupon` | 🎫 智能发券引擎 | 🟡 前端真/后端假 | 对客产品页完整；后端 demo/upload 用随机假数据，未接引擎（G1） |
| `pet-coin` | 💰 宠物冥币定制 | ✅ 可用 | 按宠物类型随机生成冥币文案（专属模板 `pet-coin.html`） |
| `text-generator` | ✍️ 文本生成器 | ⬜ 占位 | 走通用 `app.html` + `/api/<app_id>` mock 回显 |
| `chat-assistant` | 💬 智能对话助手 | ⬜ 占位 | 同上，通用 mock |
| `summary-tool` | 📝 文本摘要工具 | ⬜ 占位 | 同上，通用 mock |

独立页（不在 `AI_APPS`，单独路由）：

| 路由 | 模板 | 状态 | 说明 |
|------|------|------|------|
| `/app/plan-presentation` | `plan-presentation.html` | ✅ | 智能营销引擎企划书（对投资人/合伙人，D9） |

---

## 3. 目录结构

```
my_page/
├── task_plan.md / demand.md / debug.md / test.md   # ← 本套门户级活文档
├── app.py                  # Flask 主程序：路由 + 逻辑 + 日志
├── aliyun_llm.py           # 阿里云千问封装（面试流式对话）
├── monitor.sh              # 进程监控/守护脚本
├── .gitignore
├── templates/              # Jinja2 模板（无构建）
│   ├── index.html              # 首页（应用宫格）
│   ├── app.html                # 通用应用页（text-generator 等占位应用）
│   ├── interview.html          # AI 模拟面试
│   ├── smart-coupon.html       # 智能发券引擎对客页（Hero/受众/案例/收费/上传计算/联系）
│   ├── pet-coin.html           # 宠物冥币定制
│   └── plan-presentation.html  # 企划书展示页（D9）
├── static/
│   ├── css/  style.css · interview.css · smart-coupon.css · pet-coin.css · plan-presentation.css
│   └── js/   app.js · interview.js · smart-coupon.js · pet-coin.js
├── smart-coupon-engine/    # 独立子项目（Uplift 引擎，自带 plan/demand/debug/test.md + src/tests）
├── code-main/              # 原始方案代码包（demo.py、docs、方案 md）
├── code-main.zip
└── tracardi-growthbook-dify-智能营销引擎方案.md   # 业务方案原文
```

---

## 4. 关键接口契约（app.py）

| 方法 路由 | 入参 | 出参 | 备注 |
|-----------|------|------|------|
| `GET /` | — | `index.html`（渲染 `AI_APPS`） | 首页 |
| `GET /app/<app_id>` | path | 对应模板；未命中 `AI_APPS` 返回 `404 应用不存在` | interview/smart-coupon/pet-coin 走专属模板，其余走 `app.html` |
| `GET /app/plan-presentation` | — | `plan-presentation.html` | 独立路由，**不经 `AI_APPS` 检查**（B6 修复点） |
| `POST /api/interview/chat` | JSON `{sessionId, message}` | `text/event-stream`（`data: {content}` + `[DONE]`） | 接阿里云千问，唯一真实 LLM 路径 |
| `POST /api/pet-coin` | JSON `{petType, petName, petFeatures}` | JSON 冥币文案 | 纯随机模板，无 LLM |
| `GET /api/smart-coupon/demo` | — | JSON：summary/evaluation/preview/result_csv/result_xlsx_b64 | ⚠️ 随机假数据（4000 用户、2847 发券） |
| `POST /api/smart-coupon/upload` | multipart：customers/products/behavior + budget | 同上结构（基于上传行数） | ⚠️ 仅按行数估算，未真正跑 Uplift（G1） |
| `POST /api/<app_id>` | JSON `{input}` | JSON 回显 mock | text-generator/chat-assistant/summary-tool 共用 |

前端结果表统一列：`用户ID / 推荐面额 / 是否发放 / 最优面额 / 预期增量购买概率 / 预期成本`。

---

## 5. 已知缺口与技术债（重要，新接手必读）

| # | 缺口 | 影响 | 建议 |
|---|------|------|------|
| G1 | 门户 `/api/smart-coupon/*` 用 `random` 假数据，未调 `smart-coupon-engine` 真引擎 | 对客页展示的指标/推荐都是编的，上传的真实数据也没被真正计算 | 把 upload/demo 接到 `smart-coupon-engine` 的 `build_recommendations` / `recommend_from_tables` |
| G2 | 阿里云 API Key 硬编码在 `aliyun_llm.py`（`ALIYUN_API_KEY = "sk-..."`） | 密钥已进版本库，存在泄露风险 | 改读环境变量 / `.env`，并轮换该 key |
| G3 | 日志路径 `/usr/mypage/logs` 硬编码 | 换机器/本地跑会因目录不存在或无权限报错 | 改为相对路径或可配置，启动时自建目录 |
| G4 | 生产以 `debug=True` 跑在 80 端口 | Flask debugger 在公网可执行任意代码，安全隐患 | 生产关 debug，用 gunicorn |
| G5 | text-generator / chat-assistant / summary-tool 仅 mock 回显 | 首页列了但点进去无真实能力 | 接 LLM 或标注「演示中」 |

---

## 6. 里程碑与状态

> ⬜ 未开始 / 🟡 进行中 / ✅ 完成

| # | 里程碑 | 状态 |
|---|--------|------|
| M0 | Flask 门户骨架 + 首页应用宫格 + 日志 | ✅ |
| M1 | AI 模拟面试（接阿里云千问，SSE 流式） | ✅ |
| M2 | 宠物冥币定制（随机生成） | ✅ |
| M3 | 智能发券引擎对客页（上传/计算/下载，前端三态） | ✅ |
| M4 | 对客页营销内容：定位受众/成功案例/联系方式（D7） | ✅ |
| M5 | 对客页收费方式区块：免费试用 + 按效果分成（D8） | ✅ |
| M6 | 企划书展示页 plan-presentation（D9） | ✅ |
| M7 | 门户级活文档 task_plan/demand/debug/test.md | 🟡（本次新建） |
| M8 | 打通门户 → smart-coupon-engine 真引擎（G1） | ⬜ |
| M9 | 安全与部署整改（G2/G3/G4：密钥外置、关 debug、上 gunicorn） | ⬜ |

---

## 7. 技术选型

| 用途 | 选型 | 备注 |
|------|------|------|
| Web 框架 | Flask + Jinja2 | 单体、模板直出 |
| 前端 | 原生 HTML/CSS/JS | 无构建步骤 |
| LLM | 阿里云 DashScope（通义千问） | 仅面试用；`aliyun_llm.py` 封装流式 |
| Excel 导出 | openpyxl | 智能发券结果下载 |
| 子引擎 | smart-coupon-engine（Python + sklearn + scipy） | 独立可跑，待接入 |
| 运行/守护 | `python3 app.py` + `monitor.sh` | 端口 80 |

---

## 8. 关键设计决策（ADR 摘要）

1. **门户与引擎分仓内聚**：`smart-coupon-engine` 自带完整文档与测试，门户只做展示层；两者通过未来的接口打通（G1），而非把引擎逻辑塞进 `app.py`。
2. **企划书页用独立路由**：`/app/plan-presentation` 不走 `/app/<app_id>` 的 `AI_APPS` 校验，避免「应用不存在」404（B6 教训）。
3. **演示先于真实**：智能发券页为快速对客，先用假数据跑通前端三态与下载；真实引擎接入列为 M8，不阻塞展示。
4. **文档分层**：门户级活文档放项目根（本套），引擎内部文档留在 `smart-coupon-engine/`，各自维护、互不污染。

---

## 变更日志

- **2026-06-09**：新建门户级活文档 `task_plan.md`（本文件，基于 `smart-coupon-engine/plan.md` 改写为整个 my_page 门户视角）+ `demand.md` / `debug.md` / `test.md`。盘点全站 6 应用 + 企划书页现状，记录 5 项已知缺口（G1 引擎未接入、G2 密钥硬编码、G3 日志路径、G4 生产 debug、G5 占位应用），用于配合 planning-with-files 插件做规划与会话恢复。（by Claude）
