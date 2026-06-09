# debug.md — Bug 记录（my_page 门户）

> 每次出 bug、修复后，把「现象 → 复现 → 根因 → 修复 → 验证 → 关联」记录在这里。
> 目的：让任何新接手的人/AI 知道**这个项目踩过哪些坑、为什么某段代码长这样**，避免重复犯错。
> 范围：**整个 my_page 门户**（`app.py` / `templates` / `static`）。引擎内部 bug 见 `smart-coupon-engine/debug.md`。
> 格式：按时间倒序，最新在最上面。
>
> 配套：`task_plan.md`（架构）、`demand.md`（需求）、`test.md`（测试）。

---

## Bug 模板（复制使用）

```
## [B编号] 标题　—　YYYY-MM-DD
- **现象**：报错信息 / 错误行为（贴关键栈/输出）
- **复现**：怎么触发的（命令 / 输入 / 环境）
- **根因**：定位到的真正原因
- **修复**：改了什么（文件 : 行 / 函数），为什么这样改
- **验证**：怎么确认修好了（命令 + 结果）
- **关联**：涉及 task_plan / demand 的哪些条目；是否引入新约束
```

---

## 记录区

## [B7] 首页应用卡片全部显示"敬请期待"　—　2026-06-09
- **现象**：前端改版后访问首页 `/`，6 张应用卡片**全部**显示为置灰的"敬请期待"，连面试 / 发券 / 宠物币这 3 个真实应用也点不进去。
- **复现**：线上 `git pull` 拉取改版代码 → 浏览器刷新首页。（本地用真实 `AI_APPS` 渲染则正常，仅线上复现 → 提示是运行态问题。）
- **根因**：改版给 `app.py` 的 `AI_APPS` 新增了 `status` 字段（`available` / `coming_soon`），首页模板按 `{% if app.status == 'available' %}` 渲染链接、否则渲染敬请期待。线上 **Flask 进程仍在跑旧 `app.py`**（HTML/CSS 会热重载，但 Python 代码变更需进程真正重启才生效），旧 `AI_APPS` 没有 `status` 字段 → 每个 `app.status` 都是 undefined → 判断全不成立 → 6 张卡片全落到"敬请期待"分支。本质是**模板逻辑把"status 缺失"误当成"未上线"**，容错方向错了。
- **修复**：① 反转模板判断 —— 改为「**只有明确 `status == 'coming_soon'` 才显示敬请期待，其余（含 status 缺失）默认渲染为可用链接**」（`templates/index.html` 卡片循环 + 已上线计数改用 `rejectattr('status','equalto','coming_soon')`）。这样即使 `app.py` 没及时重载，也只会回退到"全部可用"，绝不会全站塌成敬请期待，失败方式更安全。② 运行层面：线上需**重启 Flask 进程**让带 `status` 的新 `app.py` 生效，才能正确区分 3 上线 + 3 敬请期待。
- **验证**：Jinja2 双场景渲染 —— 新 `app.py`（带 status）= 3 链接 + 3 敬请期待、计数"3 个已上线"；旧 `app.py`（无 status）= 6 链接 + 0 敬请期待（不再塌陷）。
- **关联**：`templates/index.html`、`app.py` `AI_APPS`；沿用 B6 的教训——**改了 `app.py` 必须重启进程**（Python 代码不随模板/静态资源热重载）。新增约束：模板对数据缺失要按"安全默认"容错，不要让缺字段触发最坏展示。

## [B6] 点击企划书链接显示"应用不存在"　—　2026-06-07
- **现象**：智能发券页点「查看完整智能营销企划书」，页面显示"应用不存在"。
- **复现**：访问 `/app/smart-coupon` → 底部联系我们 → 点「📊 查看完整智能营销企划书」。
- **根因**：① 企划书页已从首页入口移除、不在 `AI_APPS` 列表，链接走到 `/app/<app_id>` 动态路由时校验不过返回 404；② 改完代码没重启服务，旧代码仍在跑；③ `app.py` 含中文注释但未声明编码，Python 2.7 无法运行；④ 系统默认 `python` 指向 Python 2.7，不支持 f-string。
- **修复**：① 为企划书加独立路由 `/app/plan-presentation`，不经 `AI_APPS` 校验（`app.py:115-117`）；② 文件头加 `# -*- coding: utf-8 -*-`；③ 统一用 `python3` 启动 Flask。
- **验证**：`curl http://127.0.0.1/app/plan-presentation` 返回完整 HTML。
- **关联**：`app.py` 路由与编码声明；task_plan §2 独立页 / ADR 2 / D9。

## [B5] 点击计算后页面自动滚动到顶部　—　2026-06-07
- **现象**：点「开始计算」或「用示例数据体验」后，页面自动滚到顶部，用户得重新滚到结果区。
- **复现**：在页面任意位置点计算按钮。
- **根因**：前端 `show()` 里调了 `window.scrollTo({top:0,behavior:"smooth"})`，每次切视图都强制回顶。
- **修复**：改 `static/js/smart-coupon.js` 的 `show()`，移除/条件化回顶逻辑；计算完成后滚到结果区而非顶部。
- **验证**：点计算后页面位置不变；完成后自动定位到结果区。
- **关联**：`static/js/smart-coupon.js` `show()`。

## [B4] 上传后 Uplift 评估显示"本次数据无法评估"　—　2026-06-07
- **现象**：上传真实 CSV 计算后，Uplift 评估区显示"无法评估"，指标与分位图不显示。
- **复现**：上传行为日志 CSV → 开始计算 → 看评估区。
- **根因**：前端 `renderResult()` 要求 `data.evaluation` 含 `deciles`（分位 uplift），但上传 API 返回的 `evaluation` 只有 `qini_auc/auuc/max_lift`，缺 `deciles`，评估区被隐藏。
- **修复**：`app.py` 的 `smart_coupon_upload()`（及 `smart_coupon_demo()`）为 `evaluation` 补 `分位/deciles` 数组。
- **验证**：上传计算后评估区完整显示指标与分位柱图。
- **关联**：`app.py` smart-coupon 接口；`static/js/smart-coupon.js` `renderResult()`。

## [B3] 演示 API 未返回 result_csv/xlsx，下载为空文件　—　2026-06-07
- **现象**：点「用示例数据体验」后卡片/表格正常，但下载 CSV/Excel 是 0 字节；上传真实 CSV 点计算报错或无响应。
- **复现**：`/app/smart-coupon` → 体验 → 下载 CSV → 得 0 字节；或上传 CSV → 计算 → 失败。
- **根因**：① `smart_coupon_demo` 只返回 summary/preview/n_rows/evaluation/coupon_values，**缺 `result_csv` 和 `result_xlsx_b64`**，而前端 `downloadCsv()/downloadXlsx()` 直接引用这俩字段 → 空 Blob；② `POST /api/smart-coupon/upload` 当时未实现完整逻辑。
- **修复**：`app.py` 中 demo 生成带 BOM 的 `result_csv` + openpyxl 生成 `result_xlsx_b64`，summary 补 `面额分布`；新增并实现 `/api/smart-coupon/upload` 完整流程（注：当前为基于上传行数的简化估算，非真引擎，见 task_plan G1）。
- **验证**：体验/上传后下载的 CSV/Excel 均非空，内容与预览一致。
- **关联**：`app.py` `smart_coupon_demo`/`smart_coupon_upload`；`static/js/smart-coupon.js`。

## [B2] 演示 API 字段名与前端不一致，卡片显示 NaN/undefined　—　2026-06-07
- **现象**：智能发券页点计算后顶部统计卡片显示 `NaN`、`NaN人`、`¥NaN/¥NaN`、`undefined%`，但表格正常。
- **复现**：`/app/smart-coupon` → 开始计算 / 生成演示数据。
- **根因**：前端 `renderResult` 期望中文字段名（`客户总数/建议发券人数/预期券成本/总预算/预算使用率`），而 demo API 返回英文名（`total_users/recommended_users/used_budget/total_budget`），读到 undefined → 运算成 NaN。
- **修复**：`app.py` `smart_coupon_demo` 的 `summary` 字段改中文名并新增 `预算使用率`。
- **验证**：`curl http://localhost/api/smart-coupon/demo` 的 summary 含正确中文字段；刷新重算卡片数值正常。
- **关联**：`app.py` `smart_coupon_demo`；`static/js/smart-coupon.js` `renderResult`。

---

> 注：编号 B1 是引擎内部 bug（`.gitignore` 误伤 `smart-coupon-engine/src/.../data/` 源码包），记录在 `smart-coupon-engine/debug.md`，此处不重复。门户级 bug 从 B2 起。
