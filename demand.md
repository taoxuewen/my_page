# demand.md — 需求记录（my_page 门户）

> 用户每次提出的需求 + 与 AI 讨论后的结论，记录在这里。
> 目的：让任何新接手的人/AI 知道**每个功能是为了满足什么需求**而存在。
> 范围：**整个 my_page 门户**。引擎内部需求（数据契约、模型评估等）见 `smart-coupon-engine/demand.md`。
> 格式：按时间倒序，最新在最上面。
>
> 配套：`task_plan.md`（怎么做）、`debug.md`（出过什么 bug）、`test.md`（测了什么）。

---

## 需求模板（复制使用）

```
## [编号] 标题　—　YYYY-MM-DD
- **原始诉求**：用户原话/转述
- **背景**：为什么有这个需求
- **讨论结论 / 实现**：最终怎么做、范围边界、取舍
- **影响范围**：涉及哪些文件 / task_plan.md 哪些条目
- **状态**：待开发 / 开发中 / 已交付
```

---

## [D11] 文档维护规则 + 可覆盖部署指引文件　—　2026-06-09
- **原始诉求**：在 `task_plan.md` 加一条规则——AI 每次新增的需求记进 `demand.md`、修的 bug 记进 `debug.md`；另外写一个会被不断覆盖的 md 文件，告诉另一台部署服务器的 AI 如何重启服务让改动生效。
- **背景**：开发机与部署机分离（部署在 `/usr/mypage`），改了 `app.py` 需重启进程才生效（B6、B7 都踩过这个坑）；同时希望文档始终跟随真实状态。
- **讨论结论 / 实现**：① `task_plan.md` 新增 §9「AI 协作与文档维护规则」并在顶部加醒目指引；② 新建 `DEPLOY_NOW.md`——覆盖式部署指引，每次改动后重写，标明本次改了哪些文件、是否需重启、具体重启与验证命令，并附「改 .py 需重启 / 仅模板静态资源刷新即可」的通用判断表。
- **影响范围**：`task_plan.md`（§9 + 顶部 + 变更日志）、新增 `DEPLOY_NOW.md`。
- **状态**：已交付（2026-06-09）。

## [D10] 全站前端专业化改版　—　2026-06-09
- **原始诉求**：把项目里所有前端页面做一次专业优化（用 frontend-design 思路）。
- **背景**：原页面是紫色渐变 + emoji 的「通用 AI 味」，且新旧页面设计语言割裂，缺乏统一专业的视觉系统。
- **讨论结论 / 实现**：确立「Editorial Tech 精炼科技编辑风」——暖白纸感 + 近黑墨 + 墨绿强调，Fraunces 衬线标题 + Hanken Grotesk 正文（中文系统字体）。抽出设计系统 `static/css/design-system.css`（令牌 + 通用组件）+ Jinja 布局基类 `templates/base.html`；7 个页面（首页/通用页/面试/宠物币/发券介绍/企划书/独立 dashboard）全部对齐。首页新增占位应用「敬请期待」态（`AI_APPS` 加 `status` 字段）。不引入构建工具、不动路由/接口/后端逻辑。规格与计划见 `docs/superpowers/`。
- **影响范围**：`app.py`（AI_APPS status）、`templates/*`、`static/css/*`、`static/js/app.js`、`smart-coupon-engine/web/*`、新增 `design-system.css` / `base.html`；task_plan §9 变更日志、debug B7。
- **状态**：已交付（2026-06-09）。

## [D9] 智能营销引擎企划书静态展示页　—　2026-06-07
- **原始诉求**：基于 `tracardi-growthbook-dify-智能营销引擎方案.md` 做一个高级简洁的静态网页，向投资人/合伙人展示项目价值、商业模式、市场与行动方案。
- **背景**：需要一个专业门面，把方案文档变成可对外讲的页面。
- **讨论结论 / 实现**：新增 `templates/plan-presentation.html` + `static/css/plan-presentation.css`，蓝白灰配色、大留白；结构含 Hero / 产品定位 / 三方案对比 / 市场分析 / 商业模式（按效果分成）/ 4 阶段路线图 / 核心优势 / 团队需求与联系方式。`app.py` 加独立路由 `/app/plan-presentation`（不走 `AI_APPS` 校验）。
- **影响范围**：`templates/plan-presentation.html`、`static/css/plan-presentation.css`、`app.py:115-117`；task_plan §2 独立页、M6。
- **状态**：已交付（2026-06-07）。

## [D8] 智能发券对客页：收费方式区块（免费试用 + 按节省分成）　—　2026-06-07
- **原始诉求**：向客户展示收费方式，强调不预付费、不一次性收费，而是前期免费 + 收取「帮用户节省的券成本」的一定比例，达到双赢；苹果风、简洁大气。
- **背景**：商家对 SaaS 预付费有顾虑，需要低风险合作方式建立信任。
- **讨论结论 / 实现**：在「成功案例」与「快速入门」之间新增「收费方式」区块，核心「零成本起步 · 按效果付费」，三层级：① 前 3 个月免费 ② 仅收节省券成本的 20% ③ 没省到不收费。延续苹果风（大留白、渐变卡片）。
- **影响范围**：`templates/smart-coupon.html`、`static/css/smart-coupon.css`；task_plan M5。
- **状态**：已交付（2026-06-07）。

## [D7] 智能发券对客页：定位受众 / 成功案例 / 联系方式　—　2026-06-07
- **原始诉求**：在智能发券页增加对客内容：产品定位与受众、已有案例（多列指标）、保留上传计算的简单入门、微信联系方式（taoxuecwen）。
- **背景**：原页面只有上传计算，缺说服力，要让商家一眼看懂「这是什么、给谁用、效果如何、怎么开始、找谁」。
- **讨论结论 / 实现**：页面改为 5 区块——Hero / 定位与受众（扫码点单商户、独立小程序电商、私域社群）/ 3 个成功案例卡（uplift 倍数、ROI、券成本节省、转化率）/ 3 步上手（保留上传计算）/ 联系我们（微信 taoxuecwen，定制·数据诊断·私有化部署）。纯前端内容扩展，不动后端。
- **影响范围**：`templates/smart-coupon.html`、`static/css/smart-coupon.css`；task_plan M4。
- **状态**：已交付（2026-06-07）。

## [D-portal] 个人 AI 应用展示门户初版　—　（门户起始）
- **原始诉求**：用 Flask 搭一个个人 AI 应用展示站点，首页宫格列出多个 AI 小应用，点进去各有页面与接口。
- **背景**：需要一个对外展示 AI 能力、对内做 demo 的统一门户。
- **讨论结论 / 实现**：`app.py` 维护 `AI_APPS` 列表（interview / smart-coupon / pet-coin / text-generator / chat-assistant / summary-tool）；首页 `index.html` 渲染宫格；`/app/<app_id>` 按 id 分发模板；接入阿里云千问做面试流式对话（`aliyun_llm.py`），宠物冥币随机生成，其余应用先用通用 mock 占位。日志写 `/usr/mypage/logs`。
- **影响范围**：`app.py`、`aliyun_llm.py`、`templates/*`、`static/*`。
- **状态**：已交付。interview / pet-coin / smart-coupon 页可用；text-generator / chat-assistant / summary-tool 为 mock 占位（task_plan G5）。

---

## 待办需求池（尚未受理，登记备查）
- **接通真引擎（对应 task_plan G1）**：把 `/api/smart-coupon/demo|upload` 从随机假数据改为真正调用 `smart-coupon-engine`，让对客页展示与上传计算用真实 Uplift 结果。
- **安全整改（G2/G3/G4）**：阿里云 key 外置 + 轮换、日志路径可配置、生产关闭 Flask debug 并上 gunicorn。
- **占位应用补真（G5）**：text-generator / chat-assistant / summary-tool 接入 LLM，或在首页标注「演示中」。

---

## 工作约定（与用户确认）
- 代码与文档放在 `/home/taoxuewen/my_page/`（不要往 `/root` 丢文件）。
- 需要「传到 github」时，默认推送到 `git@github.com:taoxuewen/code.git`（注意：本仓库 origin 为 `my_page.git`，推送目标以当次确认为准）。
- 每次新需求先聊清楚再记进本文件；规划变动同步 `task_plan.md`；修完 bug 记进 `debug.md`；跑完测试记进 `test.md`。
