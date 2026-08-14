# Submission 55504047 Review

## Submission

- Time：2026-08-14 11:15:55 UTC
- Message：`v27 public Top30 route - TOP500 push`
- Artifact SHA256：`6fecd21fd0bf933f8c85c7288aa22f4de3a62447e771959063d3136b25b3c6ec`
- Initial status：PENDING；暂无Public episode
- 11:17 UTC：COMPLETE，validation rating 600.0
- Daily submissions remaining：2

## 目标

本次目标不是小幅超过v5，而是让下一提交在rating收敛后进入TOP500。提交前snapshot的TOP500门槛为2428.7。

## 提交前证据

- 6个真实线上对手 × 双seat：12W-0L，worst margin +75,207；
- 6个公开控制家族：24W-0L，worst +21,118；
- 8个未见seeds对Hamburger anchor：16W-0L；
- 8个未见seeds对collision_front：16W-0L；
- self mirror：3W-3L-10T，无灾难性克隆弱点。

完整来源、归因和审计见 [`ITERATION_TOP500_V27_PUBLIC_ROUTE`](../iterations/ITERATION_TOP500_V27_PUBLIC_ROUTE.md)。

## Validation episode 92961363

- 类型：VALIDATION self-play，不计作Public对手证据；
- 结果：57,462 vs 57,558，margin -96；
- 两个seat均完整执行生产路线，动作统计一致，无超时、异常或PASS-only故障；
- 商店：Pet Cafe×3、Yarn Store×2、Smoothie、Brunch、Farmers Market。

该局证明提交入口和线上运行正常，但不能用于判断TOP500能力。

## Public snapshot：4局

截至2026-08-14 11:34 UTC：

- Rating：**1013.0**；rank：**1710 / 4395**；
- Record：**4W-0L**；
- Margins：+109,079、+59,006、+20,580、+39,048；
- Mean margin：+56,928；worst：+20,580；
- TOP500门槛动态更新为2427.4。

| Episode | Seat | Opponent | Result | Margin |
|---:|---:|---|---|---:|
| 92962819 | 1 | JoJa | W | +109,079 |
| 92963734 | 0 | aldoktvns | W | +59,006 |
| 92964659 | 1 | Yavuz.YILMAZ | W | +20,580 |
| 92965591 | 0 | ayutin tin | W | +39,048 |

Rating与rank正在收敛，尚未达到10局接受标准。

## 在线接受标准

- 至少10个Public episodes；
- 首要指标：rank ≤ 500；
- 同时记录W/L/T、rating、对手家族、seat和margin；
- rating与rank为动态值，所有结论保留episode数量和timestamp。

## 决策

当前为 **provisional / waiting**：validation已通过，Public 4W-0L；继续等待至少10局和rank收敛。在完成最终复盘前，不使用剩余2次提交。
