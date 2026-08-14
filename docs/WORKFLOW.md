# 提交—复盘—Git 强制工作流

每轮必须按以下顺序执行；没有复盘和 Git push，不开始下一轮。

## 1. 实验前冻结

- 写清单一假设、基线文件、固定 seeds、闸门和停止条件。
- 复制当前候选到 `agents/archive/`，避免覆盖可复现基线。

## 2. 本地验证

- 使用 `tools/run_match.py`，至少 4 个开发 seeds + 4 个未见 seeds，均跑双 seat。
- 同时对比官方 `starter` 和至少一个公开强策略。
- 记录 W/L/T、平均银行、最差局；Elo 决策优先看胜率和下限。

## 3. Kaggle 提交

```bash
D:/ke/python.exe tools/submit.py submission/main.py "<版本与唯一改动>"
```

记录 submission ref、文件 SHA256、描述、剩余提交额度和提交前证据。

## 4. 线上复盘

- 等待 status COMPLETE，记录 Public rating / rank。
- 下载所有新 episode replay；大 JSON 不进 Git。
- 每个提交新增：`docs/reviews/submissions/SUBMISSION_REVIEW_<ref>.md`。
- 每个迭代新增或更新：`docs/reviews/iterations/ITERATION_<name>.md`。
- 更新 `docs/reviews/README.md`、根 `README.md` 提交台账、关键经验和下一步。
- 复盘必须给出：结果、提交前证据、线上证据、失败机制、保留/否决决策、下一项单变量实验。

## 5. Git 提交与推送

```bash
git add -A
git commit -m "docs: review submission <ref> and set next experiment"
git push origin main
```

代码实验使用 `experiment:` / `feat:` / `fix:`；结果复盘使用 `docs:`。每次 Kaggle 提交对应至少一个可追溯 Git commit。

## 6. 下一轮启动条件

只有同时满足以下条件才能开始：

- 提交结果已写入台账；
- replay 已复盘；
- 下一假设和停止条件明确；
- 工作树 clean；
- commit 已 push 到远端。
