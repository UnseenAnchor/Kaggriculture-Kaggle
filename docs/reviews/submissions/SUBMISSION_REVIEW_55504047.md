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

## 在线接受标准

- 已达到至少10个Public episodes；
- 首要指标rank ≤ 500：**未达到**；
- W/L/T稳定性8W-2L：通过继续观察门槛，但不足以宣布TOP500成功；
- rating与rank为动态值，所有结论保留episode数量和timestamp。

## 决策

**保留55504047为active submission，继续收敛。** 30局90%胜率证明主体路线稳定，但rank 1040仍未达到TOP500。8羊/6牛relay已离线拒绝；下一实验只测试hand PASS→CARE这一项状态兼容机制，未通过全部线上胜局回归前不提交第四版。
