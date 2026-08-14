# 提交复盘：55501712

## 结果

- 日期：2026-08-14
- 文件：`submission/main.py`
- 描述：`v4 adaptive demand + priority scheduler; seeded 16/16 vs starter`
- Public rating：**497.4**
- Public rank：**3184 / 4375**
- 首个 Public episode：**92927508**
- 对局：道海孤舟 67,331 vs Madhur Sabherwal 68,198
- 结果：负，差 **867**（1.27%）
- SHA256：`4aa0a1bae33910da3c135d2b9edf566287f3ff843839ab993a27c00212dc627d`

## Agent

- 1 Cow + 2 Sheep + HIRE4 动物优先开局；
- 基于 town shops 动态配置 cow/sheep/goose 与 strawberry/carrot/tomato；
- 甜瓜单次 IPO、premium 分批卖出、阈值随剩余时间降低；
- `priority*3 + distance` 调度 FEED/HARVEST/WATER；
- day 28 起清仓。

## 提交前证据

固定 8 seeds × 双 seat：

| 对手 | 战绩 | 平均银行 | 最差–最好 |
|---|---:|---:|---:|
| starter | **16W-0L** | 65,042 | 52,979–73,726 |
| hamburger elite public tape | 0W-16L | 46,403 | 21,986–68,778 |

提交目标是获得真实对手分布与 replay，而不是宣称已达到 elite 水平。

## 线上证据

### 市场环境

最终 shops：4 Yarn Store、1 Pizza、1 Brunch、1 Ice Cream、1 Pet Cafe。该随机种子极度偏向 wool，同时支持 milk/strawberry。

### 生产与销售

| 指标 | 我方 | 对手 |
|---|---:|---:|
| Sheep（最终） | 6 | 8 |
| Cow（最终） | 5 | 5 |
| Strawberry（最终） | 1 | 15 |
| WOOL 售出 | 148 | 176 |
| MILK 售出 | 120 | 138 |
| STRAWBERRY 售出 | 24 | 44 |
| PASS | 1,365 | 2 |
| Movement share | 39.9% | 73.4% |

我方动作效率更高，但后期可操作资产和供给不足。对手用更高移动成本维持了更大的生产面。

### 胜负时间线

- day 12：领先 8,036；
- day 22：领先 10,360；
- day 27：首次落后 638；
- day 29：几乎持平（落后17）；
- 最终：落后867。

这是**晚盘产能反超**，不是开局或生存机制失败。

## 失败机制

1. `sheep_target = 2 + min(4, yarn_count*2)` 把羊封顶在6；4个Yarn Store时明显不足。
2. Strawberry seed 最晚 day15 补充，早期植株衰退后最终仅剩1株；对手仍有15株。
3. 我方 BUY WHEAT 1,366、SELL WHEAT 1,125，存在大量近零净收益的 market-order 往返。
4. 仅靠降低 movement 不能取胜；空闲动作说明生产资产不足，而不是单纯路径浪费。

## 决策

- 保留开局、需求感知、动态卖出阈值和优先级调度；
- 不直接扩大所有资产，先做高 Yarn 场景 sheep target 单变量实验；
- 第二项独立实验是延长 strawberry 中盘补种窗口；
- 建立该 episode 的公开 action tape，作为反事实回放对手；
- 新版本需通过固定 seeds、双 seat、在线 tape 三重闸门后才允许提交。
