# debug.md — Bug 记录

> 每次出现 bug、用户让我修复后，我把「现象 → 定位 → 修复 → 验证」整理记录在这里。
> 目的：让任何新接手的人/AI 知道**这个项目踩过哪些坑、为什么某段代码长这样**，避免重复犯错。
> 格式：按时间倒序，最新在最上面。
>
> 配套：`plan.md`（架构）、`demand.md`（需求）、`RUN_ON_WINDOWS.md`（Windows 运行手册）。
>
> **给在 Windows 上运行的 AI**：若你照 `RUN_ON_WINDOWS.md` 执行时报错，请按下方模板在「记录区」倒序追加一条（编号接最大号往后排）。这是硬性要求。

---

## Bug 模板（复制使用）

```
## [B编号] 标题　—　YYYY-MM-DD
- **现象**：报错信息 / 错误行为（贴关键栈/输出）
- **复现**：怎么触发的（命令 / 输入 / 环境）
- **根因**：定位到的真正原因
- **修复**：改了什么（文件 : 行 / 函数），为什么这样改
- **验证**：怎么确认修好了（命令 + 结果）
- **关联**：涉及 plan.md / demand.md 的哪些条目；是否引入新约束
```

---

## 记录区

## [B6] 点击企划书链接显示"应用不存在"　—　2026-06-07
- **现象**：在智能发券引擎页面点击「查看完整智能营销企划书」链接，页面显示"应用不存在"。
- **复现**：访问 `/app/smart-coupon`，滚动到底部联系我们区块，点击「📊 查看完整智能营销企划书」链接。
- **根因**：
  1. 路由设计问题：`/app/<app_id>` 路由会先检查 `AI_APPS` 列表中是否存在该应用，由于企划书页面已从首页入口移除（不在 `AI_APPS` 列表中），导致匹配到动态路由时返回 404。
  2. 服务器缓存问题：修改后的代码未重启服务器，旧代码仍然在运行。
  3. 编码问题：app.py 文件包含中文注释但未声明 UTF-8 编码，导致 Python 2.7 无法运行。
  4. Python 版本问题：系统默认 python 命令指向 Python 2.7，不支持 f-string 语法。
- **修复**：
  1. 为企划书页面添加独立的路由 `/app/plan-presentation`，不经过 `AI_APPS` 列表检查（app.py:114-116）。
  2. 在 app.py 文件开头添加 `# -*- coding: utf-8 -*-` 声明编码。
  3. 使用 python3 启动 Flask 服务。
- **验证**：`curl http://127.0.0.1/app/plan-presentation` 返回完整的 HTML 页面内容。
- **关联**：涉及 `app.py` 路由配置和编码声明。

## [B4] 上传数据后 Uplift 评估显示"本次数据无法评估"　—　2026-06-07
- **现象**：上传真实 CSV 数据并计算后，Uplift 模型评估区域显示"本次数据无法评估"，评估指标和分位 uplift 图表不显示。
- **复现**：上传行为日志 CSV 文件，点击"开始计算"，计算完成后查看 Uplift 模型评估区域。
- **根因**：前端 `renderResult()` 函数检查评估数据时，要求 `data.evaluation` 必须包含 `deciles` 字段（分位 uplift 数据），但上传 API 返回的 `evaluation` 对象只有 `qini_auc`、`auuc`、`max_lift`，缺少 `deciles` 字段，导致评估区域被隐藏。
- **修复**：在 `smart_coupon_upload()` 和 `smart_coupon_demo()` 函数中，为 `evaluation` 对象添加 `deciles` 数组（模拟生成分位 uplift 数据）。
- **验证**：上传数据计算后，Uplift 模型评估区域显示完整的评估指标和分位图表。
- **关联**：涉及前端 `smart-coupon.js` 的 `renderResult()` 函数。

## [B5] 点击计算后页面自动滚动到顶部　—　2026-06-07
- **现象**：点击"开始计算"或"用示例数据体验"按钮后，页面会自动滚动到顶部，用户需要重新滚动到结果区域。
- **复现**：在页面任意位置点击计算按钮，页面立即滚动到顶部。
- **根因**：前端 `show()` 函数中调用了 `window.scrollTo({ top: 0, behavior: "smooth" })`，每次切换视图都会强制滚动到顶部。
- **修复**：修改 `show()` 函数，移除或条件化滚动到顶部的逻辑，或者在计算完成后滚动到结果区域而非顶部。
- **验证**：点击计算按钮后，页面位置保持不变；计算完成后自动滚动到结果区域。
- **关联**：涉及前端 `smart-coupon.js` 的 `show()` 函数。

## [B3] 演示 API 未返回 result_csv/result_xlsx_b64，下载功能失效　—　2026-06-07
- **现象**：
  1. 点击"用示例数据体验"后，页面统计卡片和表格正常显示，但下载 CSV/Excel 按钮点击后下载的是**空文件**（0 字节）。
  2. 上传真实 CSV 文件后，点击"开始计算"报错或无响应。
- **复现**：
  - 访问 `/app/smart-coupon`，点击"用示例数据体验"，页面显示结果后点击"下载 CSV"→下载 0 字节文件。
  - 上传任意 CSV 文件，点击"开始计算"→网络请求失败或返回格式错误。
- **根因**：
  1. 演示 API（`smart_coupon_demo`）只返回了 `summary`、`preview`、`n_rows`、`evaluation`、`coupon_values`，**缺少 `result_csv` 和 `result_xlsx_b64`**，而前端 JS 的 `downloadCsv()`/`downloadXlsx()` 直接引用这两个字段，导致生成空 Blob。
  2. 上传计算功能（`POST /api/smart-coupon/upload`）未实现完整逻辑，无法处理真实 CSV 文件并返回结果。
- **修复**：
  1. 在 `app.py` 的 `smart_coupon_demo` 函数中：
     - 生成 `result_csv` 字符串（包含 BOM + 完整 CSV 数据）
     - 生成 `result_xlsx_b64`（用 openpyxl 生成 Excel 并转为 base64）
     - 在 `summary` 中添加 `面额分布` 数组（前端期望此字段渲染分布图）
  2. 添加 `POST /api/smart-coupon/upload` 接口，实现完整的上传计算流程。
- **验证**：
  1. 点击"用示例数据体验"后，下载 CSV/Excel 均返回非空文件，内容与预览表格一致。
  2. 上传测试 CSV 文件，返回正常结果，表格显示推荐数据。
- **关联**：涉及前端 `smart-coupon.js` 的 `downloadCsv()`/`downloadXlsx()`，`runUpload()`，`renderResult()` 函数。

## [B2] 演示 API 返回字段名与前端期望不一致，导致页面显示 NaN/undefined　—　2026-06-07
- **现象**：智能发券引擎页面点击计算后，顶部统计卡片显示 `NaN`、`NaN人`、`¥NaN/¥NaN`、`undefined%`，但表格数据正常显示。
- **复现**：访问 `/app/smart-coupon`，点击"开始计算"或"生成演示数据"按钮。
- **根因**：前端 `renderResult` 函数期望特定的中文字段名（如 `客户总数`、`建议发券人数`、`预期券成本`、`总预算`、`预算使用率`），但演示 API 返回的是英文字段名（`total_users`、`recommended_users`、`used_budget`、`total_budget`），字段名不匹配导致读取 undefined，数学运算后显示 NaN。
- **修复**：修改 `app.py` 中 `smart_coupon_demo` 函数返回的 `summary` 对象字段名，与前端期望的中文字段名保持一致：
  - `total_users` → `客户总数`
  - `recommended_users` → `建议发券人数`
  - `used_budget` → `预期券成本`
  - `total_budget` → `总预算`
  - 新增 `预算使用率` 字段（计算：used_budget / total_budget * 100）
- **验证**：`curl http://localhost/api/smart-coupon/demo` 返回的 `summary` 对象包含正确的中文字段名（`客户总数`、`建议发券人数`、`总预算`、`预期券成本`、`预算使用率`），刷新页面重新计算后统计卡片显示正确数值。
- **关联**：涉及前端 `smart-coupon.js` 的 `renderResult` 函数。

## [B1] 源码包 `data/` 被根 .gitignore 误伤，从未推上 GitHub　—　2026-06-06
- **现象**：在 Windows / 任意机器上 `git clone` 后跑项目，会 `ModuleNotFoundError`——`src/coupon_engine/data/` 整个包（`loader.py` / `synth.py` / `__init__.py` 等）在远端缺失。本地能跑（文件在磁盘上），但克隆下来跑不起来。
- **复现**：`git ls-tree -r --name-only HEAD -- smart-coupon-engine/src/coupon_engine/data/` 返回空；`git check-ignore -v <该目录下文件>` 命中规则 `.gitignore:60:data/`。
- **根因**：仓库**根目录** `.gitignore` 有一条 `data/`（本意忽略数据集），但 gitignore 的目录模式会匹配**任意层级**的同名目录，于是把源码包 `src/coupon_engine/data/` 也忽略了。该包从 D1 起就从未进入版本库（新文件被静默忽略，`git add` 不报错也不添加）。
- **修复**：在根 `.gitignore` 的 `data/` 之后加白名单例外，且只放行 `.py`（避免把 `__pycache__` 重新纳入）：
  ```
  !smart-coupon-engine/src/coupon_engine/data/
  !smart-coupon-engine/src/coupon_engine/data/*.py
  ```
  然后 `git add` 整个 data 包并提交推送（commit 27540cc）。
- **验证**：`git ls-tree -r --name-only HEAD -- .../data/` 列出全部 5 个 .py；`git check-ignore .../__pycache__/*.pyc` 仍命中（缓存依旧被忽略）；全量排查 `smart-coupon-engine` 下所有 .py 均已跟踪。
- **关联**：教训——**广义忽略名（data/、tmp/、build/…）可能误伤同名源码目录**；提交后应抽查 `git ls-tree HEAD` 确认关键源码确实入库。涉及 plan.md 目录结构第 3 节。
