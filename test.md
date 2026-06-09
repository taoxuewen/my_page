# test.md — 测试记录（my_page 门户）

> 门户的测试清单、怎么验、与历次运行结果记录在这里。
> 范围：**整个 my_page 门户**（Flask 路由 + 页面 + 接口）。引擎单测（pytest 25 项）见 `smart-coupon-engine/test.md`。
> 每次验证（新增/改功能、修完 bug 回归）后，把结果追加到「运行记录」。
>
> 配套：`task_plan.md`（架构）· `demand.md`（需求）· `debug.md`（踩坑）。

---

## 1. 现状：门户暂无自动化测试

- 门户层（`app.py` / 模板 / 前端 JS）**目前没有 pytest 等自动化用例**，靠下方「手动冒烟清单」逐项验。
- 子项目 `smart-coupon-engine` 有完整 pytest（25 项全绿，见其 `test.md`），但门户的 `/api/smart-coupon/*` 当前未调该引擎（task_plan G1），所以引擎绿不代表门户接口正确。
- **缺口（待补，登记备查）**：用 Flask `test_client()` 给 `app.py` 写自动化用例（首页 200、各 `/app/<id>` 路由、smart-coupon demo/upload 的 JSON 结构与下载字段、pet-coin 生成、404 分支）。

---

## 2. 怎么跑（手动）

```bash
cd /home/taoxuewen/my_page
python3 app.py                 # 起服务（0.0.0.0:80, debug=True）
# 另开终端冒烟：
curl -s http://127.0.0.1/                         # 首页 200 + 应用宫格
curl -s http://127.0.0.1/app/interview            # 面试页
curl -s http://127.0.0.1/app/smart-coupon         # 智能发券对客页
curl -s http://127.0.0.1/app/plan-presentation    # 企划书页
curl -s http://127.0.0.1/api/smart-coupon/demo | head -c 400   # 演示 JSON
```

> 注意：`app.py` 写日志到 `/usr/mypage/logs/`，本地若无该目录/权限会启动报错（task_plan G3）；接口 `interview/chat` 依赖阿里云 key（task_plan G2）。

---

## 3. 手动冒烟清单

### 3.1 页面路由（`app.py` + templates）
| 用例 | 期望 |
|------|------|
| `GET /` | 200，渲染 `index.html`，6 个应用卡片齐全 |
| `GET /app/interview` | 200，面试页（输入简历 → 流式提问） |
| `GET /app/smart-coupon` | 200，对客页 5 区块（Hero/受众/案例/收费/上传计算/联系） |
| `GET /app/pet-coin` | 200，宠物冥币页 |
| `GET /app/text-generator` | 200，通用 `app.html`（mock 占位） |
| `GET /app/plan-presentation` | 200，企划书页（独立路由，B6 修复） |
| `GET /app/不存在的id` | 404 "应用不存在" |

### 3.2 接口（`app.py`）
| 用例 | 期望 |
|------|------|
| `POST /api/interview/chat` | SSE 流，逐段 `data:{content}`，结尾 `[DONE]`；异常走兜底文案 |
| `POST /api/pet-coin` | JSON，含 coinName/coinDesc/coinValue 等，随宠物类型变化 |
| `GET /api/smart-coupon/demo` | JSON，summary 为**中文字段**（B2）、含 `result_csv`/`result_xlsx_b64`（B3）、`evaluation.分位`（B4） |
| `POST /api/smart-coupon/upload` | 传 behavior CSV → 200，结构同 demo；缺 behavior → 400 |
| `POST /api/text-generator` 等 | JSON 回显 mock |

### 3.3 前端交互（`static/js/smart-coupon.js`）
| 用例 | 期望 |
|------|------|
| 点「用示例数据体验」 | 卡片数值正常（非 NaN，B2）、表格渲染、下载 CSV/Excel 非空（B3） |
| 点「开始计算」 | 页面**不回顶**、完成后定位结果区（B5） |
| 上传后看评估区 | 指标 + 分位柱图正常显示（B4） |

---

## 4. 运行记录（按时间倒序）

<!-- 新记录追加到这里（保持倒序，最新在上）：
### R? — YYYY-MM-DD · 简述
- 命令 / 环境 / 结果 / 变更点
-->

### R0 — 2026-06-09 · 门户级文档初始化（尚未自动化）
- **变更点**：新建门户级 `task_plan.md` / `demand.md` / `debug.md` / `test.md`，盘点全站现状，未改代码。
- **测试**：暂无自动化用例；上方冒烟清单为待执行基线。
- **结论**：文档就绪。下一步建议先补 Flask `test_client` 自动化（§1 缺口），再推进 task_plan M8（接真引擎）。
