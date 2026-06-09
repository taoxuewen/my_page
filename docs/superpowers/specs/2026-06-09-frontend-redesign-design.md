# 前端专业化优化 — 设计规格

- **日期**: 2026-06-09
- **范围**: AI Studio 平台全部 7 个前端页面(含独立 dashboard)
- **实现路线**: 路线 A —— 统一设计系统 + Jinja `base.html` 布局基类,原生 CSS,不引入构建工具
- **状态**: 已经用户批准设计方向,待评审规格

---

## 1. 背景与目标

这是一个 Flask 服务端渲染的多页应用("AI Studio"),展示若干 AI 应用 + 一个面向 B2B 的智能营销引擎方案。当前存在的问题:

1. **两套割裂的设计语言**:`index / app / interview / pet-coin` 是旧的紫色渐变 + emoji 风格("通用 AI 味");`plan-presentation / smart-coupon / dashboard` 已较现代(Inter 字体、BEM、hero/section)。
2. **重复前端**:`templates/smart-coupon.html`(营销介绍)与 `smart-coupon-engine/web/index.html`(实际 dashboard)视觉割裂。
3. **首页有 6 个应用卡片,仅 3 个有真实页面**(interview / smart-coupon / pet-coin);其余 3 个(文本生成 / 对话 / 摘要)指向通用 `app.html`,点进去是空壳。
4. 页脚版权信息不统一。

**目标**:抽出一套统一、专业、克制的设计系统,把所有页面收敛到同一视觉语言,不增加部署复杂度。

---

## 2. 设计语言

方向:**Editorial Tech / 精炼科技编辑风**。刻意避开满屏紫色渐变 + emoji 的通用 AI 味。核心气质:克制、自信、专业、有呼吸感。

### 2.1 色彩令牌

| 角色 | 值(建议,实现时可微调) | 用途 |
|---|---|---|
| `--color-paper` | `#FAFAF8` | 暖白基底背景 |
| `--color-ink` | `#16161A` | 近黑主文字 |
| `--color-accent` | `#1F6F5C`(墨绿/青灰系) | 唯一主强调色 |
| `--color-accent-hover` | accent 加深一档 | 交互态 |
| 中性灰阶 | `--gray-100`…`--gray-500` 共 5 档 | 边框 / 次要文字 / 分隔 |
| 语义色 | `--color-success` / `--color-warning` / `--color-error` 各一 | 状态反馈 |
| Hero 深色 | deep ink 背景反白 | hero 视觉锚点(不用彩色渐变) |

### 2.2 字体令牌

- 西文 / 数字:**Inter**(沿用 plan-presentation 已引入的)
- 中文:系统字体栈 `PingFang SC, "Microsoft YaHei", system-ui`,不引入外部中文字体
- 字阶:模块化比例 1.25,完整 scale(约 12px → 64px),用 `--text-xs`…`--text-5xl` 令牌

### 2.3 质感令牌

- 阴影:`--shadow-sm` / `--shadow-md` / `--shadow-lg` 三档,极克制的软阴影
- 圆角:`--radius-sm`(8px)/ `--radius-md`(12px)/ `--radius-lg`(16px)
- 动效:`--transition-fast` / `--transition-base` + 统一缓动;微交互克制(hover 轻微位移 + 阴影)
- 间距:基于 4px 栅格的间距令牌 `--space-1`…`--space-16`

---

## 3. 技术架构(路线 A)

```
templates/
  base.html               ← 新增:统一 head / 导航 / 页脚 / 资源引用,定义 block
  index.html              ← 改:extends base,应用墙重构
  app.html                ← 改:extends base
  interview.html          ← 改:extends base
  pet-coin.html           ← 改:extends base
  smart-coupon.html       ← 改:extends base
  plan-presentation.html  ← 改:对齐设计令牌(结构基本保留)
static/css/
  design-system.css       ← 新增:设计令牌 + 通用组件(按钮/卡片/表单/导航/页脚)
  <page>.css              ← 各页只保留页面特有样式,公共部分上移到 design-system.css
smart-coupon-engine/web/
  styles.css              ← 同步同一套设计令牌(独立部署,复制一份 tokens)
```

**原则**:
- 所有 Flask 模板 `{% extends "base.html" %}`,消除重复的 head / nav / footer。
- `design-system.css` 是样式的唯一真理来源;页面级 CSS 只写自己独有部分。
- `base.html` 提供可覆盖的 block(如 `title` / `extra_css` / `nav` / `content` / `footer` / `extra_js`)。
- dashboard(`smart-coupon-engine/web/`)是独立部署单元,无法共享 Flask static,故复制一份设计令牌保持视觉一致。

---

## 4. 各页面处理计划

| 页面 | 处理 |
|---|---|
| **首页 index** | 加平台简介 hero;应用墙重构为 3 个真实应用卡片 + 3 个"敬请期待"占位卡片(置灰、不可点击)。 |
| **app(通用页)** | 重设计输入 / 输出区,作为占位应用的统一容器。 |
| **interview** | 三阶段(简历 / 对话 / 完成)套用新组件;聊天气泡专业化。 |
| **pet-coin** | 表单 + 冥币展示;保留趣味性但用新令牌;冥币动效打磨。 |
| **smart-coupon** | 营销介绍页,对齐 hero / section 组件。 |
| **plan-presentation** | 已较成熟,主要对齐令牌、统一导航与页脚。 |
| **dashboard (engine/web)** | 同步设计令牌,与 smart-coupon 介绍页视觉连贯。 |

**统一收尾**:页脚版权统一为 "© 2026 逃学文 / AI Studio"。

### 首页"敬请期待"占位卡片

- 数据来源:`app.py` 的 `AI_APPS` 列表中 `text-generator` / `chat-assistant` / `summary-tool` 三项。
- 实现方式:在 `AI_APPS` 数据项上加一个标记字段(如 `'status': 'coming_soon'`),首页模板据此渲染为不可点击的置灰卡片。真实应用无此字段或标 `'available'`。

---

## 5. 改动边界与验证

**会改**:HTML 结构、CSS、必要时同步 JS 中的 DOM 选择器、`app.py` 中 `AI_APPS` 增加 status 字段。

**不会改**:Flask 路由、API 接口、后端业务逻辑、部署方式、JS 的功能逻辑。

**验证方式**:
- 本地启动 Flask(`python app.py`),逐页人工核对:布局、响应式(移动 / 桌面)、交互功能(面试对话流、发券 demo、宠物币生成)。
- 确认所有现有 API 调用与交互在改版后行为不变。
- 独立 dashboard 单独本地打开核对。

---

## 6. 非目标(YAGNI)

- 不引入构建工具 / npm / Tailwind / 前端框架。
- 不为占位应用(文本生成 / 对话 / 摘要)实现真实功能。
- 不做与本次视觉统一无关的后端重构。
- 不新增暗色模式切换(hero 局部深色即可,不做全站主题切换)。
