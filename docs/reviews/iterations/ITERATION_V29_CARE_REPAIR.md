# v29：Idle CARE Repair

## 触发

Submission 55504047在前30个Public episodes中达到27W-3L。第三个失败episode 92978681（seed 453608024）为-15,476。

对手与v27 movement同为42.8%，资产也接近4羊/8牛，但动作统计为CARE 957、PASS 326；v27为CARE 285、PASS 995。

## 红灯

从公开replay提取对手action tape：

- active v27，双seat：**0W-2L**；
- score：73,569 vs 89,045，两seat精确复现。

## 单变量实验A：hand PASS → CARE

保持v27购买、移动、生产和market路线不变，只将hand的`PASS`替换为`CARE`。

结果：**0W-2L**，score仍为73,569，完全无变化。无条件CARE在当前hand位置是非法/无效动作，等价于PASS。

## 单变量实验B：all actor PASS → CARE

在A基础上也替换farmer的idle PASS。

结果：**0W-2L**，score仍为73,569，完全无变化。

## 因果审计

对手并非仅有CARE overlay。其step 0同时：

- HIRE×5，而v27为HIRE×4；
- BUY WHEAT 14并在step 1 SELL 9；
- 补买更多Wheat/Melon seeds；
- 因不同开局形成不同worker位置与资产状态，后续CARE才可能有效。

因此“PASS→CARE本身导致增产”的前提错误；不能从动作频数相关性推断单机制因果。

## 完整公开路线对照

将92978681完整observable route加入9个线上tape联赛：

- 92978681 route：14W-2L-2T，worst -26,462；
- active v27：12W-6L，worst -30,245；
- 92971175 route：17W-1L，worst -1,352。

92978681 route会被8羊/6牛家族双杀，因此也不构成替代候选。

## 决策

- 拒绝hand CARE、all-actor CARE和92978681完整路线；
- 停止CARE假设，不做第三次条件猜测；
- 不提交v29，继续保留55504047 active收敛。
