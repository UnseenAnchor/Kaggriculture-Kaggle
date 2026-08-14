# Kaggriculture 调研总结（2026-08-14）

> 来源：官方 Getting Started notebook、比赛论坛精华帖、Top 公开 notebook（10 个）、GitHub 公开仓库（5 个）。
> 原始材料见 `research/forum/`、`research/notebooks/`、`research/notes/`。

## 0. 参赛状态

- ❗ **尚未报名**：Kaggle API token 无法代为接受比赛规则（403），需在浏览器打开
  https://www.kaggle.com/competitions/kaggriculture 点击 "Join Competition"（约 30 秒）。
  报名后才能下载 AGENTS.md/README.md 数据包和提交 agent。

## 1. 游戏规则核心（官方 tutorial）

- 720 回合（30 天 × 24 回合/天），1v1 对战，**赛季末银行现金多者胜**（库存不计分）。
- 起始 $3000、1 块地（象限），可购 NE $1k / SW $2k / SE $4k。
- 作物：WHEAT / CARROT / TOMATO / STRAWBERRY / MELON；动物：鸡(EGG)/牛(MILK)/羊(WOOL)。
- 植物每天要浇水否则变杂草；动物每天要喂食否则逃跑。
- 雇工（farm hands）：当日第 n 个雇工费用按斐波那契增长；前 ~10 个很便宜。
- 仓库（shed）上限 100 件，超出当日销毁。
- 市场价格随库存动态变化；城镇商店随赛季解锁，每天稳定买入（抬价）。
- **提交物**：`main.py` 或含 main.py 的 tar.gz；每步约 1 秒时限（论坛讨论，待官方确认）。
- 环境：`pip install "kaggle-environments>=1.32.6"`（⚠️ 必须 ≥1.32.6，8/6 平衡性补丁）。

## 2. 关键引擎细节（强弱分水岭，来自 zero-to-top-meta / live-meta）

1. **排行只看 W/L/T（Elo）**，赢多少钱不影响积分 → 目标是胜率不是账面金额。
2. **决赛机制特殊**：提交截止后还跑 2 周 episode，最后打一次 **Bradley-Terry 锦标赛**定最终排名（防"热手"运气）。
3. **价格悬崖**：STRAWBERRY/WOOL 超供 ~60 单位、MILK ~76 就砸到 $1 地板价；MELON 158；TOMATO/CARROT 500+；WHEAT/EGG 几乎砸不穿（3000）。
4. **Melon 是唯一不可恢复的产品**：城镇没有商店需求，drain 仅 1/天，砸盘后 60 天才能恢复 → 赛季内恢复不了 → **甜瓜是纯先手赛跑**，谁先卖谁拿走 ~$21.7k，后手吃 $1 地板。
5. **小批量出货**：顶级玩家平均每单 4–8 单位，价格撑得住就一直卖。
6. **肥料可卖钱**：引擎的通用 SELL 接受 FERTILIZER，每只动物每天产 1 份 → 养殖副业现金流（但肥料也无城镇需求，会砸盘，要早卖）。
7. **SELL 只认 shed 库存**：HARVEST 进的是单位背包，要 DROP 进 shed 才能卖；年底自动入库常常太迟。
8. **甜瓜浇水窗口**：age 6–12，窗口内每浇 +1（施肥 +2），上限 6 → 完美执行 16 格 × 6 = 96 个；6–10 天漏浇水是常见隐性亏损。
9. **小麦需要施肥才能到产量上限**；甜瓜浇水即可到上限，施肥浪费。
10. **第 4 象限（SE $4k）ROI 不成立**：顶级玩家几乎只买 NE+SW；第 4 块地 + 配套雇工成本收不回。

## 3. 当前 Meta（8/14，来自 live-meta 每日追踪 + v27 分析）

- **收敛中的顶级配置**：~8 牛 + 5–6 羊 + 6–7 草莓地，NE+SW 两块地；最新一代升级为 **12 雇工 + 6 草莓 + 1 小麦（喂牲口）**。
- **开局已高度同质化**：Top-30 里 26/30 队用同一套 **1 COW + 4 SHEEP + 5/5 种子 + WHEAT 5 + HIRE4/5** 开局 → 开局分类器没有信息价值，**真正的差距在 161 步之后的 continuation（中盘路线、劳动力路径、市场执行时机）**。
- **策略家族**（zero-to-top-meta 分类）：
  - A. 纯养牛场 —— 欺负软柿子，牛奶战两败俱伤
  - B. Melon IPO —— 16 甜瓜 + day-10 抛售，资本暴涨，但被第二个抛售者砸盘
  - C. 分阶段经济养殖（C0x 系列）—— 最强公开代码家族，但被大量 fork 导致相关性亏损
  - D. 自适应领袖型 —— 动态再平衡，难被干净克隆
  - E. 稳定效率 tape —— 8c/6s 的固定精英轨迹，当前实战最好
- **镜像局关键**：大家农场相同时，**谁先往共享市场抛售谁拿好价格**；Hamburger 的 "clone-gated front-run"（检测对手与自己近乎克隆 → 提前一回合抢跑一条高端产品线）6-0 碾压锚定版本。
- **供给约束而非价格约束**（amerob 验证的价格模型）：赛季末 9 个产品里 7 个价格**高于**基准价 → 市场在"挨饿"，瓶颈是产量/劳动力，不是卖货技巧；行动预算的 **43% 花在走路上** → 路径优化=产量。

## 4. 主流打法路线（论坛共识）

| 路线 | 现状 | 代表 |
|---|---|---|
| 固定 720 步 tape（开环回放蒸馏） | 当前统治级；从排行榜 top replay 蒸馏稳定轨迹 + 少量条件分支 | kaitofukami v27、Ezzzzzekki、senkin13 |
| 规则/启发式 + 市场时机自适应 | 最强公开代码家族（C0x 系） | romantamrazov(Hamburger)、romanrozen(Barnyard Economist)、pilkwang |
| 纯 Self-play PPO/RL | ❌ 目前跑不通：720 步长视界，需要 10M+ 局样本，论坛多人尝试均不如规则法 | — |
| 混合（规则主干 + 学习模块控制模糊决策） | 论坛认为理论最优，尚无成功案例 | — |
| IL/BC（模仿学习 replay） | 有官方每日 replay 数据集支持，作为 bootstrap | chenghaoYang(heuristic+market BC) |

**顶级玩家方法论**（kaitofukami，论坛 18 票）：真实败局 → 定位一个失败机制 → 造挑战者 → 多队+双 seat 测试 → 否决大部分候选 → 冻结胜者 → 在后期 episode 回归测试。
"提交的 agent 可以是开环的，但研究过程必须闭环。"

## 5. 可用资源清单

1. **官方**：`kaggle-environments>=1.32.6`（本地跑 env + replay）；比赛数据包 AGENTS.md/README.md（报名后下载）
2. **官方每日 replay 数据集**：`kaggle/kaggriculture-episodes-index`（每天按平均 rating 排序，最多 20GB/天 replay，供 IL/统计）
3. **入门**：bovard/kaggriculture-getting-started（579 票）
4. **机制精读**：cjlcjlcjl live-meta（每日重跑）、georgymamarin 作物收益可视化、amerob GitHub（验证过的价格模型 + harness）
5. **可参考 agent 代码**：romantamrazov/hamburger、romanrozen/barnyard-economist、pilkwang/structured-economic-policy、tetsutani/adaptive-farming、raykkretzschmar/zero-to-top-meta（含完整演进日记）、kaitofukami/v27
6. **评测工具**：raykkretzschmar/kaggriculture-rank-your-agent（本地排名评估）
7. **GitHub**：monim343（实验日志+harness，方法论最规范）、deepeshumrao（mock sim 工程结构）、EmmyPencilAI/Gugu-FarmMind（含 Gemini advisor 的 LLM 混合尝试）
8. **社区**：比赛官方 Discord（见置顶帖 730708）

## 6. 平衡性变更记录（重要！）

- 2026-08-06：城镇中心需求 2x/天 → 1x/天，取消后期 2x/4x 倍率；商店改为**有放回抽样**（可能出现 4 家同类型商店，每局差异变大）→ 硬编码单一作物策略风险上升，适应性更重要。需 `kaggle-environments>=1.32.6`。

## 7. 调研结论（事实层，不含方案）

- 奖牌现实路径存在：公开 meta 已收敛且大量公开，"克隆+微创新"可快速进前 10%（铜牌区），但同质化也意味着**差异化窗口在：①镜像局抢先抛售时机 ②中盘 continuation ③对新商店抽样的适应性**。
- RL 短期内不是拿牌路径；规则主干 + 局部自适应是性价比最高的形态。
- 走路占 43% 行动预算 → 空间/路径优化是被低估的收益点。
- 最终排名由 Bradley-Terry 锦标赛决定 → 稳定性/低方差比单场爆发重要。
