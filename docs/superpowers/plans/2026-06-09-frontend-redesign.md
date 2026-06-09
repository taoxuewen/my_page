# 前端专业化优化 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. **每个页面的实际视觉实现必须调用 `frontend-design` 技能指导,避免通用 AI 审美。**

**Goal:** 把 AI Studio 平台全部 7 个前端页面收敛到一套统一、专业、克制的「Editorial Tech」设计系统。

**Architecture:** 路线 A —— 新增 `static/css/design-system.css`(设计令牌 + 通用组件)作为唯一样式真理来源;新增 Jinja `base.html` 布局基类消除各页 head/nav/footer 重复;各页 `{% extends %}` 并只保留页面特有样式。不引入构建工具,不改 Flask 路由 / API / 后端逻辑。独立 dashboard 复制一份令牌保持视觉一致。

**Tech Stack:** Flask + Jinja2 模板、原生 CSS(CSS 自定义属性)、原生 JS。无 npm / 无构建步骤。

**验证范式:** 本任务无单元测试。每个任务的验证 = 本地启动 Flask(`python app.py`,默认 5000 端口)+ 浏览器逐页人工核对布局/响应式/交互,确认现有功能不回归。每个任务结束后 commit。

---

## 文件结构

```
templates/
  base.html               ← 新增:统一 head/nav/footer,定义 block
  index.html app.html interview.html pet-coin.html smart-coupon.html
  plan-presentation.html  ← 全部改为 extends base 并对齐令牌
static/css/
  design-system.css       ← 新增:令牌 + 通用组件
  style.css interview.css pet-coin.css smart-coupon.css plan-presentation.css
                          ← 公共部分上移,各页只留特有样式
static/js/                ← 仅在 DOM 选择器变动时同步,功能逻辑不动
smart-coupon-engine/web/styles.css ← 复制同一套令牌
app.py                    ← AI_APPS 增加 status 字段
```

---

## Task 1: 建立设计系统基础(design-system.css 令牌层)

**Files:**
- Create: `static/css/design-system.css`

- [ ] **Step 1: 创建 design-system.css,写入设计令牌**

写入以下令牌(`:root` 层),作为全站唯一真理来源:

```css
/* ===== Design Tokens ===== */
:root {
  /* 色彩 */
  --color-paper: #FAFAF8;
  --color-surface: #FFFFFF;
  --color-ink: #16161A;
  --color-ink-soft: #3A3A42;
  --color-accent: #1F6F5C;
  --color-accent-hover: #185847;
  --color-accent-soft: #E7F1ED;
  --gray-100: #F2F2EF;
  --gray-200: #E4E4E0;
  --gray-300: #CFCFC8;
  --gray-400: #9A9A92;
  --gray-500: #6B6B63;
  --color-success: #2E7D5B;
  --color-warning: #B97A0E;
  --color-error: #C0392B;
  --color-ink-deep: #111014; /* hero 深色背景 */

  /* 字体 */
  --font-sans: 'Inter', 'PingFang SC', 'Microsoft YaHei', system-ui, -apple-system, sans-serif;
  --text-xs: 0.75rem; --text-sm: 0.875rem; --text-base: 1rem;
  --text-lg: 1.25rem; --text-xl: 1.5rem; --text-2xl: 2rem;
  --text-3xl: 2.5rem; --text-4xl: 3.25rem; --text-5xl: 4rem;
  --leading-tight: 1.15; --leading-normal: 1.6;

  /* 间距(4px 栅格) */
  --space-1: 4px; --space-2: 8px; --space-3: 12px; --space-4: 16px;
  --space-6: 24px; --space-8: 32px; --space-12: 48px; --space-16: 64px;
  --space-24: 96px;

  /* 圆角 */
  --radius-sm: 8px; --radius-md: 12px; --radius-lg: 16px; --radius-full: 999px;

  /* 阴影(克制) */
  --shadow-sm: 0 1px 2px rgba(22,22,26,0.05);
  --shadow-md: 0 4px 16px rgba(22,22,26,0.08);
  --shadow-lg: 0 12px 40px rgba(22,22,26,0.12);

  /* 动效 */
  --transition-fast: 150ms cubic-bezier(0.4,0,0.2,1);
  --transition-base: 250ms cubic-bezier(0.4,0,0.2,1);

  /* 布局 */
  --container-max: 1160px;
}
```

- [ ] **Step 2: 在同文件追加 reset + 基础排版**

包含 `*{box-sizing:border-box;margin:0;padding:0}`、`body` 使用 `--color-paper`/`--color-ink`/`--font-sans`/`--leading-normal`、`.container{max-width:var(--container-max);margin:0 auto;padding:0 var(--space-6)}`、标题字阶、链接默认样式。

- [ ] **Step 3: 提交**

```bash
git add static/css/design-system.css
git commit -m "新增：设计系统令牌层（design-system.css）"
```

---

## Task 2: 通用组件层(button / card / form / nav / footer)

**Files:**
- Modify: `static/css/design-system.css`

- [ ] **Step 1: 用 frontend-design 技能指导,在 design-system.css 追加通用组件**

实现并以 BEM/工具类暴露以下组件类(具体视觉打磨遵循 frontend-design):
- `.btn` / `.btn--primary`(accent 实心)/ `.btn--secondary`(描边)/ `.btn--ghost` / `.btn--dark`,统一 padding/radius/transition/hover 位移。
- `.card`(surface 背景 + shadow-sm + radius-md),`.card--hover`(hover 抬升)。
- 表单:`.field`、`label`、`input/textarea/select`(统一边框 `--gray-200`、focus 用 accent 描边)。
- `.site-nav`(顶部导航)+ `.site-footer`(统一页脚)。
- `.badge`(小标签,用于 hero badge 和"敬请期待")。
- `.spinner`(统一加载动画)。

- [ ] **Step 2: 验证**

新建一个临时 `templates/_styleguide.html` 或直接在浏览器开发者工具中粘贴各组件,确认渲染正常。验证后删除临时文件(不提交)。

- [ ] **Step 3: 提交**

```bash
git add static/css/design-system.css
git commit -m "新增：设计系统通用组件层（按钮/卡片/表单/导航/页脚）"
```

---

## Task 3: Jinja 布局基类 base.html

**Files:**
- Create: `templates/base.html`

- [ ] **Step 1: 创建 base.html**

结构包含:`<head>` 统一引入 `design-system.css` + Inter 字体(preconnect + fonts.googleapis）+ 可覆盖 block。骨架:

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{% block title %}AI Studio{% endblock %}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/static/css/design-system.css">
  {% block extra_css %}{% endblock %}
</head>
<body>
  {% block nav %}{% endblock %}
  <main>{% block content %}{% endblock %}</main>
  {% block footer %}
  <footer class="site-footer"><div class="container">© 2026 逃学文 · AI Studio</div></footer>
  {% endblock %}
  {% block extra_js %}{% endblock %}
</body>
</html>
```

- [ ] **Step 2: 验证**

base.html 无独立路由,留待后续页面继承时一并验证。语法自检:确认 block 名称与后续页面引用一致(`title`/`extra_css`/`nav`/`content`/`footer`/`extra_js`)。

- [ ] **Step 3: 提交**

```bash
git add templates/base.html
git commit -m "新增：Jinja 布局基类 base.html"
```

---

## Task 4: 首页 index + 占位应用状态字段

**Files:**
- Modify: `app.py`(`AI_APPS` 列表)
- Modify: `templates/index.html`
- Modify: `static/css/style.css`

- [ ] **Step 1: 在 app.py 的 AI_APPS 给三个占位应用加 status**

给 `text-generator` / `chat-assistant` / `summary-tool` 三项各加 `'status': 'coming_soon'`;真实应用(interview/smart-coupon/pet-coin)加 `'status': 'available'`。

- [ ] **Step 2: 重构 index.html 继承 base**

`{% extends "base.html" %}`,在 `content` block 写平台简介 hero + 应用墙。模板循环按 `app.status` 区分:available 渲染 `<a class="app-card">`;coming_soon 渲染 `<div class="app-card app-card--soon">` 含 `.badge` "敬请期待"、不可点击。用 frontend-design 指导视觉。

- [ ] **Step 3: 清理 style.css**

把 index 用到的、已在 design-system.css 提供的公共样式删除;`style.css` 只保留首页特有样式(hero、app-card、app-card--soon)。

- [ ] **Step 4: 验证**

运行 `python app.py`,访问 `/`。确认:6 张卡片正确显示;3 张真实卡片可点击跳转;3 张占位卡片置灰、带"敬请期待"、点击无跳转;响应式正常。

- [ ] **Step 5: 提交**

```bash
git add app.py templates/index.html static/css/style.css
git commit -m "重构：首页应用墙 + 占位应用敬请期待状态"
```

---

## Task 5: 通用应用页 app.html

**Files:**
- Modify: `templates/app.html`
- Modify: `static/css/style.css`(app-page 相关)

- [ ] **Step 1: 重构 app.html 继承 base**

`{% extends "base.html" %}`;`content` block 内放返回链接 + 应用标题 + 输入区(textarea + 提交按钮用 `.btn--primary`)+ 输出区(`.card`)。保留 `currentAppId` script 与 `app.js` 引用(放 `extra_js` block)。用 frontend-design 指导。

- [ ] **Step 2: 验证**

运行 Flask,访问 `/app/text-generator`(占位应用仍可直达此通用页)。确认布局正常、提交交互不报错。检查 `static/js/app.js` 选择器(`#userInput`/`#submitBtn`/`#outputArea`)与新结构一致,不一致则同步。

- [ ] **Step 3: 提交**

```bash
git add templates/app.html static/css/style.css static/js/app.js
git commit -m "重构：通用应用页 app.html"
```

---

## Task 6: AI 模拟面试 interview

**Files:**
- Modify: `templates/interview.html`
- Modify: `static/css/interview.css`
- Modify(如需): `static/js/interview.js`

- [ ] **Step 1: 重构 interview.html 继承 base**

三阶段(resumeStage / interviewStage / completeStage)保留相同 id;套用 `.card` / `.btn` / `.field` / `.spinner` 组件;聊天气泡(`.messages`)专业化。进度指示器用令牌重做。用 frontend-design 指导。`interview.js` 放 `extra_js`。

- [ ] **Step 2: 清理 interview.css**

公共样式上移,只留面试特有(进度条、聊天气泡、阶段切换)。

- [ ] **Step 3: 验证**

运行 Flask,访问 `/app/interview`。确认:简历输入→开始面试→对话流式返回→完成阶段 整条交互链正常(依赖 `/api/interview/chat`)。核对 interview.js 选择器与新结构一致。

- [ ] **Step 4: 提交**

```bash
git add templates/interview.html static/css/interview.css static/js/interview.js
git commit -m "重构：AI 模拟面试页"
```

---

## Task 7: 宠物冥币 pet-coin

**Files:**
- Modify: `templates/pet-coin.html`
- Modify: `static/css/pet-coin.css`
- Modify(如需): `static/js/pet-coin.js`

- [ ] **Step 1: 重构 pet-coin.html 继承 base**

表单区(formSection)套用 `.card` / `.field` / `.btn`;结果区(resultSection)冥币展示保留趣味性但用令牌重做配色与动效。保留所有 id(petType/petName/petFeatures/generateBtn/coinTitle 等)。用 frontend-design 指导。

- [ ] **Step 2: 清理 pet-coin.css**

公共样式上移,保留冥币卡片、硬币动效等特有样式。

- [ ] **Step 3: 验证**

运行 Flask,访问 `/app/pet-coin`。确认:填表→生成(依赖 `/api/pet-coin`)→冥币结果展示→"再来一张" 正常。核对 pet-coin.js 选择器。

- [ ] **Step 4: 提交**

```bash
git add templates/pet-coin.html static/css/pet-coin.css static/js/pet-coin.js
git commit -m "重构：宠物冥币定制页"
```

---

## Task 8: 智能发券介绍页 smart-coupon

**Files:**
- Modify: `templates/smart-coupon.html`
- Modify: `static/css/smart-coupon.css`

- [ ] **Step 1: 重构 smart-coupon.html 继承 base**

已用 hero/section 结构,对齐到 design-system 令牌:hero 用深色锚点、section/audience-card 套用 `.card`,按钮统一 `.btn`。保留内容文案。用 frontend-design 指导。

- [ ] **Step 2: 清理 smart-coupon.css**

公共样式上移,保留 hero、section、audience-grid 等特有布局。

- [ ] **Step 3: 验证**

运行 Flask,访问 `/app/smart-coupon`。确认布局、响应式、内部锚点/链接正常。

- [ ] **Step 4: 提交**

```bash
git add templates/smart-coupon.html static/css/smart-coupon.css
git commit -m "重构：智能发券引擎介绍页"
```

---

## Task 9: 企划书展示页 plan-presentation 对齐令牌

**Files:**
- Modify: `templates/plan-presentation.html`
- Modify: `static/css/plan-presentation.css`

- [ ] **Step 1: 对齐令牌**

结构基本保留(已较成熟)。把 plan-presentation.css 中硬编码的颜色/字阶/圆角/阴影替换为 design-system 令牌引用;navbar/footer 与全站统一(可继承 base 或对齐组件类)。注意:此页已自带 Inter 引入,继承 base 后去重。

- [ ] **Step 2: 验证**

运行 Flask,访问 `/app/plan-presentation`。确认视觉与其他页连贯、导航锚点、案例故事区(最近新增)显示正常。

- [ ] **Step 3: 提交**

```bash
git add templates/plan-presentation.html static/css/plan-presentation.css
git commit -m "调整：企划书展示页对齐设计令牌"
```

---

## Task 10: 独立 dashboard 同步令牌

**Files:**
- Modify: `smart-coupon-engine/web/styles.css`
- Modify(如需): `smart-coupon-engine/web/index.html`

- [ ] **Step 1: 复制令牌到 dashboard styles.css**

把 design-system.css 的 `:root` 令牌层复制到 `smart-coupon-engine/web/styles.css` 顶部(独立部署,无法共享 static)。把该文件内 hero/card/btn/drop/table 等样式改为引用令牌,与 smart-coupon 介绍页视觉连贯。用 frontend-design 指导。

- [ ] **Step 2: 验证**

直接用浏览器打开 `smart-coupon-engine/web/index.html`(或按其 README 启动 dashboard),确认上传区、结果表格、图表区视觉与主站一致,交互(`app.js`)不回归。

- [ ] **Step 3: 提交**

```bash
git add smart-coupon-engine/web/styles.css smart-coupon-engine/web/index.html
git commit -m "同步：独立 dashboard 对齐主站设计令牌"
```

---

## Task 11: 全站收尾与回归核验

**Files:** 无新增,跨页核对

- [ ] **Step 1: 页脚统一核对**

确认所有页面页脚均为 base 提供的统一版权(`© 2026 逃学文 · AI Studio`),无遗留旧文案("版权归逃学文所有" / 旧 "© 2026 AI Studio")。

- [ ] **Step 2: 全站逐页回归**

运行 Flask,依次访问 `/`、`/app/interview`、`/app/smart-coupon`、`/app/pet-coin`、`/app/text-generator`、`/app/plan-presentation`,逐页核对:桌面 + 移动响应式、字体加载、交互功能不回归。dashboard 单独核对。

- [ ] **Step 3: 提交(如有收尾改动)**

```bash
git add -A
git commit -m "收尾：全站页脚统一与回归核验"
```

---

## Self-Review(已执行)

- **Spec 覆盖**:设计令牌(Task 1)、组件(Task 2)、base.html(Task 3)、首页含占位卡片(Task 4)、app(5)、interview(6)、pet-coin(7)、smart-coupon(8)、plan-presentation(9)、dashboard(10)、页脚统一+回归(11)——spec 各节均有对应任务。✓
- **占位符扫描**:无 TBD/TODO;CSS 令牌已写死实值。逐页视觉细节交由 frontend-design 技能在执行时产出(本计划已显式标注),属合理委派而非占位。✓
- **一致性**:base.html 的 block 名(title/extra_css/nav/content/footer/extra_js)在 Task 4–9 引用一致;各页保留原有 DOM id,JS 选择器核对步骤已内置。✓
- **改动边界**:不动 Flask 路由/API/后端逻辑,与 spec 一致。✓
