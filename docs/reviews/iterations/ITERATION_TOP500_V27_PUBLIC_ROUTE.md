# TOP500 Push：Public v27 Route 审计

## 目标与门槛

2026-08-14 09:13 UTC leaderboard snapshot：

- 当前团队约701.7，rank 2314/4379；
- TOP1000门槛：1762.7；
- **TOP500门槛：2428.7**；
- TOP100门槛：2856.1。

从约700到2428.7无法靠v5式局部调参一次跨越。本轮切换为“公开精英tape骨架 + 我们自己的多层验证与后续稀疏控制器研究”。

## 候选来源与归因

- Kaggle notebook：`kaitofukami/25-27-strict-future-v27-midgame-meta-reset`；
- 原始main.py：20,813 bytes；
- 原始SHA256：`f48c21166eac68d1b05a401f04f94a2eb6154e65415af64893672365ff33c7b8`；
- notebook公开证据：current inner 28/30、development outer 29/30、strict-future 25/27；
- 路线来自公开observable replay behavior，notebook明确记录归因；不声称恢复了他人私有源码。

提交文件只增加3行来源注释，行为不变；最终候选SHA256：`6fecd21fd0bf933f8c85c7288aa22f4de3a62447e771959063d3136b25b3c6ec`。

## 评测层1：线上真实对手 tape 联赛

6个已遭遇线上对手 × 双seat：

| 候选 | 战绩 | Mean margin | Worst margin |
|---|---:|---:|---:|
| v5-A heuristic | 10W-2L | +10,174 | -39,511 |
| Hamburger anchor | 12W-0L | +94,619 | +59,953 |
| **v27 reset** | **12W-0L** | **+99,857** | **+75,207** |

## 评测层2：公开控制家族

对 Hamburger anchor、Frontier v12、Kaito v21、Replay Shield v15、Scenario v14、Soil v25，2 seeds × 双seat：

- v27：**24W-0L**，mean margin +36,320，worst +21,118；
- collision_front：22W-2L，worst -18,803；
- v27 对 Frontier：4W-0L，修复了 Hamburger 家族主要盲区。

## 评测层3：未见种子与镜像

8 seeds × 双seat：

- vs Hamburger anchor：**16W-0L**；
- vs collision_front：**16W-0L**；
- v27 self mirror：3W-3L-10T；输赢主要由seat/seed对称性决定，无灾难性克隆弱点。

## 决策

**通过，作为下一次且唯一一次TOP500冲刺候选。**

它相比v5不是相邻参数改动，而是经Top-30公开研究、线上对手联赛、控制家族和镜像测试共同验证的数量级升级。

## 风险与停止条件

- Public路线会被大量复制，rating需通过持续episode才能收敛，无法保证提交完成瞬间即显示TOP500；
- 若10个Public episodes后仍低于TOP1000，先复盘实际对手家族，不立即追加第四次提交；
- 下一研发重点不是改固定tape本体，而是在真实失败上添加有归因的稀疏闭环控制器。
