# v28：8羊/6牛强路线与relay实验

## 触发

Submission 55504047前10个Public episodes为8W-2L。两局失败：

- 92967433：-1,724；
- 92971175：-29,636。

两名对手均购买8羊/6牛，并使用胡萝卜、大量肥料和小麦销售；当前v27为4羊/9牛固定路线。

## 精确失败闸门

从公开replay提取对手action tape，保留来源、team和seat归因：

- seed 2103638568：v27 0W-2L；
- seed 847064548：v27 0W-2L；
- 合计：**0W-4L**，红灯可重复。

加入原6个线上对手后，v27为12W-4L，worst -30,245。

## 路线筛选

将两名胜者的公开observable action route跨全部8个线上tape评估：

| Route | Online tape | Worst |
|---|---:|---:|
| v27 active | 12W-4L | -30,245 |
| episode 92967433 | 14W-2L | -2,424 |
| episode 92971175 | **15W-1L** | **-1,352** |

92971175 route对6个公开控制家族为24W-0L，mean +37,394，worst +13,193。

## 预注册直接替换闸门

接受条件：8个此前未用于该route的seed × 双seat，对active v27至少12W-4L。

实际：**7W-9L**，未达标准，拒绝直接替换。该route虽然克制本次强家族，但会丢失v27面对同源公开路线时的通用优势。

## 稀疏分类器与relay可行性

step 1的公开WHEAT market inventory能反映对手step 0买量，因此理论上可识别开局家族。但两route在step 0已经分叉：

- v27：HIRE×4、Cow×1、Sheep×4；
- 强route：HIRE×5、Cow×2、Sheep×2，并立即BUILD_PASTURE。

单变量实验“强route step 0，step 1起切回v27”结果：**0W-16L，最终现金固定19**。切换后的hand count、资产和动作tape错位，relay不可行；信号出现时间晚于可安全分流的时间。

## 决策

- 拒绝直接替换、relay和基于step 1的route classifier；
- 不消耗第四次提交；
- 保留55504047 active并继续观察rating收敛；
- 若继续开发，必须构建真正状态驱动的策略或能在step 0之前获得的合法信号，不能拼接不兼容tape。
