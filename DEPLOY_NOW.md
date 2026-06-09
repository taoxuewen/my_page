# DEPLOY_NOW.md — 部署生效指引（给部署服务器的 AI）

> ⚠️ **本文件每次有改动就会被覆盖重写，只反映「最近一次改动」该如何生效。**
> 你（运行在部署服务器 `/usr/mypage` 上的 AI）在 `git pull` 之后，照这份做即可。
> 应用运行方式：`python3 app.py` → Flask 监听 `0.0.0.0:80`（`debug=True`），由 `monitor.sh` 守护。

---

## 本次改动（2026-06-09）

- **内容**：① 全站前端专业化改版（统一设计系统 + 7 个页面重做）；② 修复首页应用卡片全部显示「敬请期待」的 bug（B7）。
- **改动文件**：
  - `app.py` ← **改了**（`AI_APPS` 新增 `status` 字段）→ **需要重启**
  - `templates/*.html`、`static/css/*`、`static/js/*` ← 改了（模板/静态资源，刷新即生效）
  - `smart-coupon-engine/web/*` ← 改了（独立 dashboard，若单独部署需各自刷新）

## 👉 本次结论：**需要重启 Flask 进程**

因为改了 `app.py`。光 `git pull` + 浏览器刷新只能让 HTML/CSS 生效，`AI_APPS` 的 `status`（首页「3 上线 / 3 敬请期待」的区分）**必须重启进程**才会加载。

---

## 生效步骤

```bash
# 1. 拉取最新代码
cd /usr/mypage && git pull

# 2. 重启 Flask 进程（结束旧进程，monitor.sh 会自动拉起；若没有守护则手动启动）
pkill -f "python3.*app.py"
sleep 2
# 若 monitor.sh 未托管自动重启，则手动后台启动：
nohup python3 app.py > /dev/null 2>&1 &

# 3. 验证：HTTP 200 且首页卡片正常
sleep 3
curl -s -o /dev/null -w "首页 HTTP: %{http_code}\n" http://127.0.0.1/
```

**人工核对**：打开首页，应看到 **3 张可点击应用卡片**（AI模拟面试 / 智能发券引擎 / 宠物冥币定制）+ **3 张置灰「敬请期待」卡片**（文本生成器 / 智能对话助手 / 文本摘要工具）。CSS 若没更新，浏览器 **Ctrl+F5** 强刷绕缓存。

---

## 通用判断规则（下次改动时套用）

| 改了什么 | 是否需重启 | 怎么生效 |
|---|---|---|
| `app.py` / `aliyun_llm.py` / 任何 `.py` | ✅ **需重启** | `git pull` → 重启进程 → 验证 |
| 仅 `templates/*.html` | ❌ 不用 | `git pull` → 浏览器刷新（debug 自动重载模板） |
| 仅 `static/css/*` 或 `static/js/*` | ❌ 不用 | `git pull` → 浏览器 Ctrl+F5 强刷 |
| `smart-coupon-engine/web/*`（独立 dashboard） | 看其单独部署方式 | 各自刷新/重启 |

> 重启兜底：`monitor.sh` 每次运行会检测 `http://127.0.0.1/` 是否 200，异常则自动 `pkill` 重启。手动改完直接 `pkill -f "python3.*app.py"` 让它重新拉起也可以。
