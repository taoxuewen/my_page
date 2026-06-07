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
