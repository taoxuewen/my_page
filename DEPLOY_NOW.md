# DEPLOY_NOW.md — 部署生效指引（给部署服务器的 AI）

> ⚠️ **本文件每次有改动就会被覆盖重写，只反映「最近一次改动」该如何生效。**
> 你（运行在部署服务器 `/usr/mypage` 上的 AI）在 `git pull` 之后，照这份做即可。
> 应用运行方式：`python3 app.py` → Flask 监听 `0.0.0.0:80`（`debug=True`），由 `monitor.sh` 守护。

---

## 本次改动（2026-06-09）

- **内容**：新增项目根目录 `README.md`（GitHub 仓库首页介绍）。
- **改动文件**：
  - `README.md` ← 新增（纯文档）
  - `demand.md` / `DEPLOY_NOW.md` ← 文档同步

## 👉 本次结论：**无需重启，也无需任何操作**

本次只动了文档，**不影响运行中的网站**。部署服务器可选地 `git pull` 一下保持代码同步即可，无需重启、无需刷新。

```bash
cd /usr/mypage && git pull   # 可选，仅为保持本地代码最新
```

---

## 通用判断规则（下次改动时套用）

| 改了什么 | 是否需重启 | 怎么生效 |
|---|---|---|
| `app.py` / `aliyun_llm.py` / 任何 `.py` | ✅ **需重启** | `git pull` → 重启进程 → 验证 |
| 仅 `templates/*.html` | ❌ 不用 | `git pull` → 浏览器刷新（debug 自动重载模板） |
| 仅 `static/css/*` 或 `static/js/*` | ❌ 不用 | `git pull` → 浏览器 Ctrl+F5 强刷 |
| 仅文档（`*.md` / `docs/`） | ❌ 不用 | 无需操作；可选 `git pull` 保持同步 |
| `smart-coupon-engine/web/*`（独立 dashboard） | 看其单独部署方式 | 各自刷新/重启 |

## 重启 Flask 进程的标准命令（需要时用）

```bash
cd /usr/mypage && git pull
pkill -f "python3.*app.py"
sleep 2
nohup python3 app.py > /dev/null 2>&1 &   # 若 monitor.sh 未自动拉起则手动启动
sleep 3
curl -s -o /dev/null -w "首页 HTTP: %{http_code}\n" http://127.0.0.1/
```

> 重启兜底：`monitor.sh` 每次运行会检测 `http://127.0.0.1/` 是否 200，异常则自动 `pkill` 重启。
