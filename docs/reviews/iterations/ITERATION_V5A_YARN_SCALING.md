# v5-A Yarn-Demand Sheep Scaling 迭代复盘

## 假设

submission 55501712 的首个线上 episode 有4个Yarn Store。v4将 sheep target 封顶在6，导致 day27 后晚盘产能被8羊对手反超。

本轮只修改一个机制：高 Yarn 需求下的 sheep target 与扩张节奏。

## 改动

- `demand_sheep_target`：`2 + min(4, yarn_count*2)` → `2 + min(8, yarn_count*2)`；
- sheep staging：`2 + day//4` → `2 + day//3`；
- 只允许 sheep 扩张延长到 day24；cow/goose 仍在 day22 停止。

其他开局、作物、市场、调度和卖出逻辑保持不变。

## 线上 replay tape 闸门

对手：episode 92927508 中 Madhur Sabherwal 的720步公开 observable action tape；seed 518120964。

| 版本 | Seat 0 | Seat 1 | 战绩 |
|---|---:|---:|---:|
| v4 | -867 | -526 | 0W-2L |
| v5-A | **+1,570** | **+4,479** | **2W-0L** |

v5-A 精确解决了预注册失败机制。

## 固定种子回归（8 seeds × 双 seat）

| 对手 | v4 | v5-A | 变化 |
|---|---:|---:|---:|
| starter | 16W-0L，均值65,042 | **16W-0L，均值65,689** | +647 |
| hamburger elite tape | 均值46,403 | 均值46,176 | -227 |

预注册容忍线为 elite 均值下降不超过2,000；实际只下降227，且starter胜率不变。

## 决策

**通过并允许提交。**

原因：线上真实失败场景从双败变双胜，跨种子没有显著回归；这是由 replay 证据驱动的单变量改进，不是相邻参数盲扫。

## 提交后检查

- 观察初始 rating 和前5个 episode，而不是只看第一局；
- 核对极端无Yarn场景是否维持原策略；
- 若线上提高，下一轮做 v5-B strawberry late replant；
- 若线上下降，优先检查新增 sheep 的 feed/labor 外溢，不把两个机制混在一起修。
