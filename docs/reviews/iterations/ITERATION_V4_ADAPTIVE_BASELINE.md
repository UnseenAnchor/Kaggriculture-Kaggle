# v4 Demand-Adaptive Baseline 迭代复盘

## 目标

在不复制公开 720-step tape 的前提下，建立可解释、可复现、能从在线 replay 继续迭代的闭环 Agent baseline。

## 公开证据

- 官方 tutorial / AGENTS / engine README；
- live-meta、zero-to-top-meta、Hamburger、structured-policy 等公开 notebooks；
- Kaggle forum：Balance Changes、Daily Top Episodes、Self-play PPO、final evaluation；
- GitHub：amerob、monim343、deepeshumrao 等公开工程。

调研归档：[`research/SUMMARY.md`](../../../research/SUMMARY.md)。

## 实现与实验

1. 修复 day0 重复采购、HIRE 挤占 market order、WHEAT pickup/drop 循环和多单位重复 PICKUP。
2. 修复以 seeds==0 触发补种导致 16 melon + 17 strawberry 的过量生产。
3. 按实际 shops 需求配置 animals/crops。
4. premium 卖出阈值随赛季推进降低，避免终局 $1 清仓。
5. 修复 job priority 未进入调度评分的问题。

## 接受/否决

### 接受

- live assets + seeds 限额；
- demand-adaptive herd/crops；
- 动态卖出阈值；
- `priority*3 + distance` 调度。

调度修复在开发 seeds 上使 elite 对手均值约41.8k→46.8k、最差22.3k→37.2k；虽然对 starter 的无对抗现金下降，但仍全胜，符合 Elo 目标。

### 否决

前3小时强行补齐10/12 hands：

- starter 均值 63.6k→57.8k；
- elite 均值 46.8k→43.3k；
- 新增工人无法覆盖成本，已回退。

## 最终验证与提交

8个固定 seeds + 双 seat：starter 16W-0L，elite均值46,403。提交 ref **55501712**。

线上首局只输867，但暴露晚盘产能不足。详见 [SUBMISSION_REVIEW_55501712](../submissions/SUBMISSION_REVIEW_55501712.md)。

## 下一项预注册实验

### v5-A：Yarn demand sheep scaling

- 唯一改动：提高多 Yarn Store 下 sheep target，上限从6放宽到8–10；
- 基线：v4；
- 主要对手：episode 92927508 固定公开 action tape；
- 闸门：两 seat 都改善最终 margin，且8-seed starter胜率不下降；
- 停止条件：elite均值下降超过2,000或维护失败增加。

v5-A 完成并 Git push 前，不开始 strawberry 补种实验。
