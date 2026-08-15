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

## Public snapshot：10局

截至2026-08-14 11:59 UTC：

- Rating：**1288.6**；rank：**1414 / 4396**；
- Record：**8W-2L**；
- Mean margin：+27,212；worst：-29,636；
- TOP500门槛：2431.3；
- 相比提交前约rank 2314，已提升约900名，但未达到TOP500接受标准。

新增episode：

| Episode | Seat | Opponent | Result | Margin |
|---:|---:|---|---|---:|
| 92966513 | 1 | Ahmed Berat Özer | W | +28,105 |
| 92967433 | 0 | Syed Muhammad Gillani | L | -1,724 |
| 92968376 | 0 | Devin Zhou | W | +31,212 |
| 92969308 | 1 | Takahiro Someya | W | +5,090 |
| 92970237 | 1 | JeovaAnderson | W | +11,356 |
| 92971175 | 1 | tipstar0125 | L | -29,636 |

## Public snapshot：30局

截至2026-08-14 13:10 UTC：

- Rating：**1728.6**；rank：**1040 / 4410**；
- Record：**27W-3L**（90% win rate）；
- Mean margin：+17,468；median：+12,744；worst：-29,636；
- TOP1000门槛：1769.1；TOP500门槛：2434.0。

新增19局为18W-1L。唯一新失败episode 92978681为-15,476。

## 失败家族初判

两名胜者动作/资产特征高度相似：购买8羊/6牛、种胡萝卜、卖约1,800–2,000肥料和约1,200小麦；v27固定路线仅4羊/9牛、卖235肥料和455小麦。该家族使用更多有效劳动（约50% movement、633–684 PASS），而v27为42.8% movement、995 PASS。

最差局含Bakery×3、Yarn×2；v27从day11起持续落后，最终差约30k。

第三个失败92978681不是8羊/6牛家族，而是与v27高度同构的4羊/8牛路线。其movement同为42.8%，但把约669个PASS替换为CARE（CARE 957 vs 285），最终多卖88 Milk、30 Wool和67 Fertilizer。该公开行为给出一个状态兼容、可单独验证的CARE-repair方向。

## Public snapshot：45局

截至2026-08-14 14:04 UTC，复盘范围为 Public episodes 1–45（截至 `93000180`；查询后新增的 `93001112` 为第46局，不纳入本轮45局闸门）：

- Rating：**1774.6**；rank：**996 / 4421**；
- Record：**37W-8L-0T**（82.2%胜率）；
- TOP1000门槛：1771.0，**已进入TOP1000**；TOP500门槛：2435.3，仍未达到；
- 新增第31–45局：**10W-5L-0T**；mean margin **+5,819**，median **+11,455**，worst **-22,592**；
- 45局结果由 Kaggle episode replay 逐局核对；rating/rank 仍是动态快照，不能与不同时间直接作因果比较。

| Episode | Seat | Opponent | Result | Margin | Shops（按解锁顺序） |
|---:|---:|---|:---:|---:|---|
| 92988954 | 1 | MYOUCER | W | +12,578 | BAKERY×2, PIZZA_SHOP, YARN_STORE, FARMERS_MARKET, PET_CAFE, BRUNCH_SPOT×2 |
| 92989885 | 1 | Aberrchan | W | +11,455 | FARMERS_MARKET, ICE_CREAM_SHOP, YARN_STORE×2, PET_CAFE, BRUNCH_SPOT×2, PIZZA_SHOP |
| 92990814 | 1 | Ali Haydar Özdağ | W | +15,314 | PIZZA_SHOP, FARMERS_MARKET, BRUNCH_SPOT, FARMERS_MARKET, SMOOTHIE_SHOP, YARN_STORE, BAKERY, PET_CAFE |
| 92990803 | 0 | InformaBook2 | L | -18,622 | PIZZA_SHOP, SMOOTHIE_SHOP, PET_CAFE, BAKERY, FARMERS_MARKET, BAKERY, YARN_STORE, BRUNCH_SPOT |
| 92991754 | 1 | Patrick Joël MAIRLOT-MBEZELE | W | +4,583 | ICE_CREAM_SHOP, YARN_STORE×2, BAKERY, ICE_CREAM_SHOP, SMOOTHIE_SHOP, BAKERY, FARMERS_MARKET |
| 92992675 | 1 | shiggriculture | L | -22,592 | PET_CAFE, YARN_STORE, PIZZA_SHOP, SMOOTHIE_SHOP, YARN_STORE×2, PIZZA_SHOP, FARMERS_MARKET |
| 92993619 | 0 | Rajan Nagarajan | W | +24,041 | ICE_CREAM_SHOP, PET_CAFE, SMOOTHIE_SHOP, PIZZA_SHOP, BAKERY, PIZZA_SHOP, BAKERY, FARMERS_MARKET |
| 92994559 | 0 | Gebreab K. Zewdie | L | -17,713 | SMOOTHIE_SHOP, BAKERY, PIZZA_SHOP, BAKERY, SMOOTHIE_SHOP×3, YARN_STORE, FARMERS_MARKET |
| 92995487 | 0 | Uvais | L | -666 | SMOOTHIE_SHOP, ICE_CREAM_SHOP, BRUNCH_SPOT, BAKERY, BRUNCH_SPOT, SMOOTHIE_SHOP, BRUNCH_SPOT, YARN_STORE |
| 92996437 | 1 | Marcus | W | +12,595 | FARMERS_MARKET, BRUNCH_SPOT, BAKERY, ICE_CREAM_SHOP, BAKERY, BRUNCH_SPOT, YARN_STORE×2 |
| 92996602 | 0 | ╰┈➤ˎˊ˗ www.sleepyai.org | W | +17,569 | PIZZA_SHOP, ICE_CREAM_SHOP, PIZZA_SHOP, BRUNCH_SPOT, PIZZA_SHOP, BAKERY, PIZZA_SHOP, YARN_STORE |
| 92997365 | 1 | Fajri Yanuar Shiddiq Juanda | L | -21,162 | SMOOTHIE_SHOP×3, PET_CAFE, FARMERS_MARKET, PIZZA_SHOP, BRUNCH_SPOT×2 |
| 92998312 | 0 | MYOUCER | W | +36,963 | FARMERS_MARKET×3, SMOOTHIE_SHOP, BAKERY, PET_CAFE, PIZZA_SHOP, PET_CAFE |
| 92999242 | 0 | heinado | W | +30,063 | FARMERS_MARKET, SMOOTHIE_SHOP, BAKERY, SMOOTHIE_SHOP, BRUNCH_SPOT, YARN_STORE, ICE_CREAM_SHOP, BAKERY |
| 93000180 | 0 | zhangwei02 | W | +2,878 | ICE_CREAM_SHOP, PET_CAFE, PIZZA_SHOP×4, BRUNCH_SPOT, YARN_STORE |

## Public replay：第46局补充

- Episode `93001112`，seat 0，对手 `Roshan Singh`；v27 **W**，margin **+32,980**（127,215 vs 94,235）。
- Shops：`SMOOTHIE_SHOP×2、BAKERY、YARN_STORE、ICE_CREAM_SHOP×2、PET_CAFE、PIZZA_SHOP`。
- 该局仍执行 v27 固定路线，未出现新失败机制；将 replay 记录为 45局快照之后的补充证据，不把它的结果混入 45局 rating 快照。

### 新增败局逐局结论

- **92990803 / InformaBook2：** 与 v27 同为 4 sheep / 8 cow 兼容路线，但 CARE 957（v27 为285），并销售更多 Milk/Wool/Fertilizer；最终 +18,622。属于已知 CARE/现金流失败家族，不能据此重开已拒绝的 v29 实验。
- **92992675 / shiggriculture：** 12 sheep / 6 cow、购买第三块土地，销售约1,473 Wheat 与1,748 Fertilizer；movement 49.6%、PASS 563，明显是更高劳动/肥料现金流路线，最终 +22,592。与已拒绝的 8-sheep/6-cow relay 属同类强供给压力，但不改变 relay 已拒绝结论。
- **92994559 / Gebreab K. Zewdie：** 与 v27 的 4 sheep / 9 cow 资产和 42.8% movement 高度同构，仅 PASS、DROP、Wheat 买卖等细节不同；当前 replay 不能把差异归因到单一机制，保留为未解释近邻失败。
- **92995487 / Uvais：** 10 cow / 4 sheep、50.3% movement，销售约871 Wheat 与1,487 Fertilizer，属于扩大动物/肥料供给的独立现金流压力，最终仅 -666。
- **92997365 / Fajri Yanuar Shiddiq Juanda：** 同为 v27 兼容资产路线，但 CARE 966，销售约479 Wheat、300 Fertilizer、320 Milk、154 Wool；最终 +21,162。再次观察到 CARE/现金流家族，但不撤销 v29 的拒绝。

## 在线接受标准

- 已达到至少10个Public episodes；45局主复盘已完成，第46局已作为补充 replay 复盘；
- 首要指标rank ≤ 500：**未达到**；
- TOP1000：**已达到**（rank 996 / 4421，45局快照）；
- 45局主快照 W/L/T：**37W-8L-0T**；第46局补充为 W，不改变45局 rating快照；
- rating与rank为动态值，所有结论保留episode数量和timestamp。

## 决策

**继续保留55504047为active submission，本轮优化不形成可提交候选。** 第46局以 +32,980 获胜，但没有新增可利用机制。V30 的需求排序 alpha 变体无改善；公开对手压力清仓候选在已知失败族上退化或不改善，已否决。V31 的额外 hand 肥料巡回虽通过 starter/Hamburger 基础闸门，但在三个失败 tape 上为 3W-5L、0W-8L、3W-5L，否决。V32 的羊牛配比及公开压力条件切换在三个失败 tape 上均为 0W-8L，否决。v28 relay 与 v29 CARE 实验仍明确拒绝，不重做；只有通过多失败族回归和完整本地闸门的候选才进入提交验证。
