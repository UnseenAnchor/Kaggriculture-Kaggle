# Kaggriculture 长期优化策略

## 一句话结论

保留 `v27 / 55504047` 作为 champion；长期研发改为 **replay 数据集 + 完整 continuation policy + champion/challenger 闸门**。停止对 720-step tape 做一个个局部 overlay、阈值和订单变体。

目标不是最大化单局现金，而是最大化 Bradley–Terry 的长期 W/L，并降低最差失败族的方差。

## 历史复盘：什么有效，什么无效

| 阶段 | 机制 | 证据 | 结论 |
|---|---|---|---|
| v4 | 需求适配、限额、优先级调度 | starter/elite 本地通过；线上上限约700 rating | 方法正确，但启发式天花板太低 |
| v5-A | Yarn 需求下 sheep scaling | 一个真实 replay 由0W-2L变2W-0L；线上随后出现约40k败局 | 局部信号能修单局，不能替代强骨架 |
| v27 | 公开 Top-30 完整 action tape | 真实早期 37W-8L，曾进入 TOP1000 | 当前最强 champion |
| v28 | 强路线中途 relay | 0W-16L，现金固定约19 | 不兼容的 hand/asset/action state 不能拼接 |
| v29 | 无条件 CARE repair | 0W-2L，动作多数无效 | 只改动作名、不验证位置状态没有意义 |
| V30/V36–V41 | SELL、Wheat cash、feed queue、开局流动性 | 基础闸门可过，但旧失败族无改善 | 市场队列不是结构性供给缺口的根因 |
| V31/V42 | 额外 hand / 劳动容量 | starter/Hamburger 不回归，但失败族不改善 | 额外劳动力必须和完整任务图、资产目标一起设计 |
| V32–V35 | 动物比例、Yarn、Milk、crop route | 均未改善多个失败族，部分破坏依赖 | 不再做条件阈值和局部路线替换 |
| V39–V45 | 高供给、CARE、近邻及 Rancher scheduler 审计 | 高供给和 CARE 是不同瓶颈；完整 Rita scheduler 反而 0W-8L 对 baseline | 不能把完整公开策略拆成安全小补丁 |

## 已确认的失败族

1. **高供给/生产吞吐族**：更多 pasture、动物、hands、Wheat/Fertilizer 和任务运输；不是单一买动物或 SELL 问题。
2. **CARE 族**：资产规模接近 v27，但大量有效 CARE 替代 PASS；不是 feed queue 单点问题。
3. **市场近邻族**：同一生产路线下的现金/价格时序差；SELL 方向已有反复否决证据。
4. **新边界近邻族**：约 5 SHEEP / 9 COW / 15 pasture 的小幅领先；同时改变动物、牧场、hire、移动和 Wheat 调度，不能归因于一只羊。

## 长期架构：Champion + typed continuation policy

### Layer 0：不可破坏的 champion

- `agents/main.py` 保持 v27 action backbone。
- 任何 challenger 都在 `research/agents/`，不得直接覆盖 active。
- 默认 fallback 永远回到 v27；异常、状态不匹配、资源不守恒都回退。

### Layer 1：回放数据注册表

每个 replay 记录：

- episode、seat、对手家族、胜负、margin、shops；
- turn 24/100/160/192/240/400/719 的 money、shed、feed reserve、hands、animals、pasture、crop counts；
- farmer/hand/market action stream hash；
- 首次 divergence turn 和 divergence 类型：production、labor、market、route、CARE。

先用最新 Public replay 更新失败族，再决定是否创建 challenger。没有新状态簇，不写新候选。

### Layer 2：完整 continuation policy，而非 raw tape relay

将策略拆成有类型的意图和状态机：

- `OpeningPlan`：step 0 的 hand/animal/seed/land 组合必须整体一致；禁止 step 1 以后拼接另一条 route。
- `FeedPlan`：以 shed + carried Wheat 计算 reserve，先保证动物存活，再允许 expansion。
- `ProductionPlan`：明确 pasture、animal、crop、hand target；目标必须能由现金流和行动预算支撑。
- `JobPlan`：每个 hand 的任务必须满足位置、携带物和每日状态，不把无效 CARE 当成 PASS 修复。
- `LiquidationPlan`：只在长期资源计划允许时卖出；不做独立 SELL overlay。
- `FallbackPlan`：任何预算、位置、hand identity 或状态不匹配时，继续执行 v27 对应 action。

关键原则：候选只能在**完整 continuation 状态**上切换，不能在 step 0 用路线 A、step 1 用路线 B，也不能只替换一个动物订单而保留不兼容的 hand tape。

### Layer 3：策略级搜索

每次只比较完整策略配置，不搜索零散阈值：

```text
policy = {
  opening_profile,
  target_animals,
  pasture_target,
  hand_ramp,
  feed_reserve,
  crop_mix,
  job_priority,
  liquidation_policy,
}
```

候选的改变必须能写成一个机制假设，并同时解释至少两个独立失败族。否则只做离线分析，不进入本地 gate。

## 长期研发循环

### A. 数据阶段

1. 每天下载 active submission 的新 replay。
2. 先统计 W/L/T、margin 和失败时点，再看动作细节。
3. 用 action hash 和 state snapshot 聚类，不按对手名字猜策略。
4. 对每个新簇写“可观测前置条件 → 状态变化 → 结果”的因果链。

### B. 候选阶段

1. 从 champion 分叉并归档 baseline。
2. 只创建一个完整机制候选。
3. 首先测试 action/resource invariants：没有非法动作、hand 数量不漂移、feed 不透支、shed 不无故溢出。
4. 再跑 starter/Hamburger 8 seeds × 双 seat 和至少三个失败族 4 seeds × 双 seat。

### C. 接受阶段

候选必须同时满足：

- starter/Hamburger 无胜率回归；
- 至少两个独立失败族改善；
- 无灾难性 margin；
- 未见 seeds 仍稳定；
- 完整 control/tape regression 通过；
- 代码、假设、结果、Git push 全部可追溯。

任何一个条件失败，候选冻结为研究资产，不调第二个阈值救活。

### D. 提交阶段

- 提交额度不是目标，合格候选才消耗额度。
- 每个 submission 至少等到第 5 个 Public episode 才做 provisional review，第 10 个后再做方向决定。
- rating 只在相同 episode 数和时间快照下比较；优先看 W/L、失败族 margin 和最差局。
- 新提交没有明确改善时，继续保留 champion，不做“为了今天提交”的替换。

## 实际优先级

1. **短期：**继续收集并标注最新 Public replay，建立失败族 registry；不写 V46 overlay。
2. **中期：**实现一个能保持 hand identity 和 resource invariants 的 typed continuation simulator，先离线复现 v27 和一个完整高供给策略。
3. **长期：**只在 simulator 能从同一 opening 生成完整、合法、可解释的 continuation 后，测试新的 production policy。
4. **暂缓：**RL、随机 portfolio、SELL 微调、CARE 单点、动物比例阈值、固定 route relay。

## 当前决策

`55504047` 仍是 champion。最新 Public 样本虽出现 0W-8L-2T，但失败仍属于已知结构族，尚无新的可隔离机制。下一次有效进展应是**新的 stateful continuation policy**，不是又一个局部动作补丁。
