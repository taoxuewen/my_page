# progress.md — 进度日志（my_page 门户）

> planning-with-files 插件会自动读取本文件**最后若干行**（`tail -20`）注入上下文，
> 所以本文件**正序追加，最新写在最下面**（与 task_plan/demand/debug/test 的「倒序」相反）。
> 每完成一步就追加一行：`- [YYYY-MM-DD HH:MM] 做了什么 → 结果/下一步`。
>
> 配套：`task_plan.md`（活地图）· `demand.md`（需求）· `debug.md`（踩坑）· `test.md`（测试）。

---

## 进度记录

- [2026-06-09] 把 /root/my_page 迁到 /home/taoxuewen/my_page，清掉冗余的 my_page_new；main 分支 pull 到最新 87abd0e（企划书页 D9 等）。
- [2026-06-09] 新建门户级活文档 task_plan.md / demand.md / debug.md / test.md（基于 smart-coupon-engine 同名文件改写为整个门户视角），盘点 6 应用 + 企划书页现状，记录缺口 G1-G5。
- [2026-06-09] 新建本 progress.md，供 planning-with-files 自动注入最近进度。
- [2026-06-09] 下一步候选：① task_plan M8——把 /api/smart-coupon/* 接到真引擎（G1）；② 安全整改 G2/G3/G4；③ 给 app.py 补 Flask test_client 自动化用例（test.md §1 缺口）。
