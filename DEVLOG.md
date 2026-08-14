# 开发日志

## 2026-08-14 — Baseline v1 完成

### 验证结果（本地，各 4 局双 seat）

| 对手 | 战绩 | 平均银行 | 区间 |
|---|---|---|---|
| `starter`（官方基线） | **4W-0L** | $61,876 | 48k–70k |
| hamburger_anchor（公开精英 tape，~$125k 水平） | 0W-4L | $46,248 | 23k–56k |

参照系：顶级 agent 自对战 ~$88k–124k；amerob 测的强 agent vs starter ~$131k。

### 已实现的 meta 要点
动物优先开局（1C+2S+HIRE4）→ 甜瓜/草莓 → NE/SW 买地（不买 SE）
→ 小批量出货 → 甜瓜先手赛跑 → 肥料早卖 → 买小麦喂牲口 → 期末清仓。

### 踩过的坑
1. day==0 采购每小时重复触发 → 开局破产（$3）
2. HIRE 占满 10 个 market order → 挤掉动物/种子订单
3. 喂牲口小麦被 DROP → pickup/drop 死循环，牲口饿死
4. h21 后须回仓 DROP，避免雇工日结时库存损失
5. 多单位 PICKUP 同一动物 → reserved 计数去重

## 2026-08-14 — v4 稳定性迭代（最终提交候选）

### 根因与改动

1. **重复补种 bug**：把“种子为 0”误作“作物不足”，实际种出 16 甜瓜 + 17 草莓；改为 `live plots + seeds` 严格限额。
2. **随机商店适配**：根据 ICE_CREAM/SMOOTHIE/PIZZA/YARN/BAKERY/PET/FARMERS 的实际数量动态配置牛、羊、鹅、草莓、胡萝卜、番茄。
3. **库存归零风险**：premium 卖出阈值随剩余天数降低，day 28 开始完整清仓，避免 50+ milk/wool 最终以 $1 变现。
4. **调度优先级 bug**：任务列表有 priority，但旧代码分配时只看距离；改为 `priority * 3 + distance`，保证 FEED/HARVEST/WATER 优先。
5. **否决实验**：前 3 小时强行补齐 10/12 雇工使弱敌均值下降 $5.8k、强敌下降 $3.6k，已回退。

### 固定种子最终验证（8 seeds × 2 seats）

| 对手 | 战绩 | 平均银行 | 区间 |
|---|---|---:|---:|
| starter | **16W-0L** | **$65,042** | $52,979–$73,726 |
| hamburger elite public tape | 0W-16L | **$46,403** | $21,986–$68,778 |

相较迭代前（同 4 个开发 seeds）：
- vs elite：均值约 $37.3k → $46.8k；最差 $12.4k → $37.2k。
- vs starter：仍全胜；牺牲部分无对抗利润，换取强对抗稳定性（Elo 只看 W/L/T）。

验证日志：`validation_starter.txt`、`validation_anchor.txt`。

### 提交状态

- 文件：`submission/main.py`
- 压缩包：`submission/kaggriculture-v4.tar.gz`
- SHA256(main.py)：`4aa0a1bae33910da3c135d2b9edf566287f3ff843839ab993a27c00212dc627d`
- 原因更正：旧 `kaggle 1.7.4.5` 不支持 KGAT；手写 REST 流程返回 403，但 token 本身有效。
- 已从 Kaggle 官方 GitHub 安装 CLI **2.2.4** + kagglesdk **0.1.37**，识别 `auth_method: ACCESS_TOKEN`。
- **提交成功**：submission ref `55501712`，描述 `v4 adaptive demand + priority scheduler; seeded 16/16 vs starter`。
- 2026-08-14 08:46:31 状态：`PENDING`；当日剩余 4 次提交。
