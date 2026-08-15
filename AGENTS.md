# Kaggriculture Agent 行动指南

## 目标与保护线

- 目标：寻找能通过严格本地闸门并改善多个线上失败族的候选，目标 TOP500。
- `agents/main.py` 与 Kaggle submission `55504047` 是 active baseline，未经完整证据不得修改或替换。
- 没有合格候选时，保持 `55504047`，不为了“有新版本”而提交。
- 不重做已拒绝的 v28 relay、v29 CARE、V30–V38 方向。

## 开始任何实验前

1. 写出一句机制假设：必须解释至少两个独立失败族，而不是只描述一个局部症状。
2. 指定可观测前置条件、预期改变的状态量和失败判据。
3. 先做 replay/state 对比；没有因果证据时不写候选代码。
4. 明确说明为什么实验不是以下已关闭方向：SELL 排序、hand 数量、CARE、羊牛比例、Yarn 阈值、固定 route relay。

## 候选实验流程

1. 冻结 `agents/main.py`，候选只能放在 `research/agents/`。
2. 每个机制只允许一个候选；不得连续做阈值、alpha 或顺序的盲目变体。
3. 先跑 smoke gate：三个固定失败族各 4 seeds × 双 seat，并同时检查 starter 与 Hamburger。
4. 任一失败族没有改善，或 starter/Hamburger 回归，立即否决；不得扩展到完整回归。
5. 只有 smoke gate 通过，才跑未见 seeds、完整 control/tape regression 和最终 block。
6. 候选必须同时满足：基础闸门无损、至少两个独立失败族改善、无灾难性 margin、动作与资源守恒正常。

标准命令：

```bash
D:/ke/python.exe tools/run_match.py <candidate> <opponent> <comma-separated-seeds>
```

## 停止规则

- 一个机制未改善多个失败族：停止，不调参救活它。
- 发现问题来自结构性产能、劳动、动物或现金流差距：不要伪装成市场 queue 问题。
- 不再继续微调 SELL、hand、CARE、羊牛比例或 Yarn 阈值。
- 不为候选复制整份大文件，除非机制已经通过 smoke gate；优先使用最小 overlay 或明确的独立实现。
- 本地 runner 出现异常时，先确认入口函数和环境；入口错误不能当作策略结果。

## 记录与提交

- 每个实验必须有 `docs/reviews/iterations/ITERATION_*.md`，记录假设、命令、W/L/T、均值、失败族结论和决定。
- 同步更新 `docs/reviews/README.md` 与根 `README.md`。
- 提交信息必须明确写出 accept/reject；实验文件不得改变 active baseline。
- 只有候选通过完整闸门、文档完成、Git commit/push 完成后，才考虑 Kaggle submission。
- 没有合格候选时，明确报告“保留 55504047”，不制造提交压力。
