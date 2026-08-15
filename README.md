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
tools/eval_tape_league.py       真实线上对手 tape 联赛
tools/eval_public_controls.py   公开强策略家族控制组联赛
tools/analyze_replay.py         线上 episode 复盘工具
tools/submit.py                 官方 Kaggle CLI 提交入口
research/                       公开 notebook / 论坛 / replay 研究材料
docs/reviews/submissions/       每次 Kaggle 提交复盘
docs/reviews/iterations/        每轮实验与决策复盘
```

## 提交记录

| # | 日期 | Submission | 描述 | 本地证据 | Public rating | Episodes | 备注 |
|---|---|---:|---|---|---:|---:|---|
| 1 | 2026-08-14 | [55501712](https://www.kaggle.com/competitions/kaggriculture/submissions/55501712) | v4 demand-adaptive + priority scheduler | starter 16W-0L，均值65,042；elite tape均值46,403 | **664.0**（4局） | 3W-1L | 首局输867，后续3胜；见[复盘](docs/reviews/submissions/SUBMISSION_REVIEW_55501712.md) |
| 2 | 2026-08-14 | [55501952](https://www.kaggle.com/competitions/kaggriculture/submissions/55501952) | v5-A Yarn-demand sheep scaling | online tape 0W-2L→2W-0L；starter仍16W-0L | **612.4**（2局snapshot） | 1W-1L | 局部启发式不足以跨越TOP500差距；见[复盘](docs/reviews/submissions/SUBMISSION_REVIEW_55501952.md) |
| 3 | 2026-08-14 | [55504047](https://www.kaggle.com/competitions/kaggriculture/submissions/55504047) | v27 public Top-30 route / TOP500 push | online tape 12W-0L；controls 24W-0L；未见种子32W-0L | **1774.6**（45局snapshot） | 37W-8L-0T | rank 996/4421，进入TOP1000；TOP500仍需2435.3；见[复盘](docs/reviews/submissions/SUBMISSION_REVIEW_55504047.md) |

## 关键经验

1. **现金均值不是排行榜目标**：本地要同时看双 seat 胜率、最差局和对强策略稳定性。
2. **商店必须驱动供给**：shops 有放回抽样；固定作物/牲畜上限会在极端需求场景失配。
3. **限额按 live assets + seeds 计算**：只看种子是否为0会反复补种并砸盘。
4. **任务优先级必须进入分配评分**：`priority*3 + distance` 明显提高强对抗下限。
5. **局部启发式与精英路线存在数量级差距**：v5-A在线tape联赛10W-2L、worst -39,511；公开v27路线12W-0L、worst +75,207。

## 下一步

- [x] 建立官方环境、固定种子双-seat评测与公开精英 tape 对照
- [x] v4：作物限额、商店需求适配、动态清仓、优先级调度
- [x] 提交 v4 并下载首个 Public replay
- [x] 完成 submission 55501712 线上复盘
- [x] 从 episode 92927508 提取可复现公开 action tape
- [x] v5-A：高 Yarn 需求 sheep scaling；线上 tape 0W-2L → 2W-0L，已通过提交闸门
- [x] v5-A通过固定 seeds、双 seat、线上 replay tape三重闸门并提交（55501952）
- [x] 确认TOP500门槛2428.7，并停止用局部启发式修补冲榜
- [x] 审计公开v27路线：线上tape 12W-0L；公开控制组24W-0L；未见种子对强骨架32W-0L
- [x] 提交v27 TOP500冲刺候选（55504047）
- [x] 跟踪55504047到10个Public episodes：8W-2L，rank 1414/4396，尚未TOP500
- [x] 为episodes 92967433、92971175建立精确失败闸门：active v27为0W-4L
- [x] 审计8羊/6牛公开路线：线上tape 15W-1L，但对active v27仅7W-9L，拒绝替换
- [x] relay可行性实验：0W-16L、现金19，确认两条固定tape的资产状态不兼容
- [x] 保留55504047观察到30局：27W-3L，rank 1040/4410，仍未TOP500
- [x] CARE单变量实验：hand-only与all-actor均0W-2L、分数不变，拒绝错误因果假设
- [x] 92978681完整route为14W-2L-2T，仍被8羊/6牛家族双杀，拒绝替换
- [x] 完成55504047第31–45局 replay 复盘：新增10W-5L，总计37W-8L-0T，rank 996/4421，进入TOP1000
- [x] 补充复盘第46局93001112：v27胜Roshan Singh，+32,980，无新失败机制
- [x] V30需求排序/压力清仓实验：未跨失败族改善，否决，不提交
- [x] V31额外hand肥料巡回：基础闸门通过但失败族为3W-5L/0W-8L/3W-5L，否决
- [ ] 保留55504047继续收敛；不重做v28 relay或v29 CARE，只有新候选通过多失败族本地闸门后才提交
