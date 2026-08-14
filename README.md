# Kaggriculture – Autonomous Farming Agent

Kaggle 模拟赛实战记录：构建能在 720 回合动态市场中自主生产、经营、交易和对抗的 Agent。

- 比赛：https://www.kaggle.com/competitions/kaggriculture
- 目标：赛季结束时银行现金高于对手；排行榜按 W/L/T 的 skill rating 排名
- 截止：2026-09-30 23:59 UTC；每日 5 次提交
- 官方规则：[`docs/competition/README.md`](docs/competition/README.md)
- 复盘索引：[`docs/reviews/README.md`](docs/reviews/README.md)
- 强制工作流：[`docs/WORKFLOW.md`](docs/WORKFLOW.md)

## 环境

- Python 3.11：`D:/ke/python.exe`
- `kaggle-environments >= 1.32.6`
- Kaggle CLI 2.2.4 + kagglesdk 0.1.37（KGAT access token）

## 项目结构

```text
agents/main.py                  当前候选 Agent
agents/archive/                 已冻结的历史候选
submission/main.py              最近一次实际提交文件
tools/run_match.py              固定种子、双 seat 本地闸门
tools/analyze_replay.py         线上 episode 复盘工具
tools/submit.py                 官方 Kaggle CLI 提交入口
research/                       公开 notebook / 论坛 / replay 研究材料
docs/reviews/submissions/       每次 Kaggle 提交复盘
docs/reviews/iterations/        每轮实验与决策复盘
```

## 提交记录

| # | 日期 | Submission | 描述 | 本地证据 | Public | 排名 | 备注 |
|---|---|---:|---|---|---:|---:|---|
| 1 | 2026-08-14 | [55501712](https://www.kaggle.com/competitions/kaggriculture/submissions/55501712) | v4 demand-adaptive + priority scheduler | starter 16W-0L，均值65,042；elite tape均值46,403 | **497.4** | **3184/4375** | 首个Public episode输867；见[复盘](docs/reviews/submissions/SUBMISSION_REVIEW_55501712.md) |

## 关键经验

1. **现金均值不是排行榜目标**：本地要同时看双 seat 胜率、最差局和对强策略稳定性。
2. **商店必须驱动供给**：shops 有放回抽样；固定作物/牲畜上限会在极端需求场景失配。
3. **限额按 live assets + seeds 计算**：只看种子是否为0会反复补种并砸盘。
4. **任务优先级必须进入分配评分**：`priority*3 + distance` 明显提高强对抗下限。
5. **线上首局是晚盘产能不足**：4个Yarn Store时仅6羊，且草莓未在中后期补种；day27后由领先转为落后，最终仅输867。

## 下一步

- [x] 建立官方环境、固定种子双-seat评测与公开精英 tape 对照
- [x] v4：作物限额、商店需求适配、动态清仓、优先级调度
- [x] 提交 v4 并下载首个 Public replay
- [x] 完成 submission 55501712 线上复盘
- [ ] 从 episode 92927508 提取可复现公开 action tape
- [ ] v5-A：只扩大高 Yarn 需求下的 sheep target，做单变量反事实
- [ ] v5-B：只延长 strawberry 补种窗口，评估 day26–29 收益
- [ ] 淘汰 wheat BUY/SELL 往返造成的 market-order 浪费
- [ ] 新候选通过固定 seeds、双 seat、线上 replay tape 三重闸门后才提交
