# 提交复盘：55501952（provisional）

## 结果 snapshot

- 日期：2026-08-14
- 文件：`submission/main.py`
- 描述：`v5-A yarn-demand sheep scaling; replay tape 0-2 to 2-0`
- SHA256：`d261142e4ca6bec2586c502467ad5e0378ee6ab72244ccc0dee4fd5e449f760a`
- Public rating：**703.0**（1个Public episode后；会动态变化）
- 当前团队 rank：**2312 / 4378**
- Public episodes：**1W-0L**
- 当日剩余提交额度：3

## 提交前证据

- episode 92927508 observable tape：v4 0W-2L → v5-A **2W-0L**；
- starter固定8 seeds双seat：16W-0L，均值65,042→65,689；
- hamburger elite tape：均值46,403→46,176（-227，闸门允许-2,000）。

详见 [ITERATION_V5A_YARN_SCALING](../iterations/ITERATION_V5A_YARN_SCALING.md)。

## 首个 Public episode

- Episode：92931235
- Seat：0
- 对手：ShirrleyChen
- 结果：**Win**
- 我方：63,492
- 对手：41,916
- Margin：**+21,576**
- Shops：Bakery×2、Yarn×1、Ice Cream×1、Pet Cafe×1、Brunch×1、Smoothie×1、Farmers Market×1

该局只有1个Yarn Store，没有充分触发v5-A的高Yarn扩张分支，因此它证明“没有明显普通场景回归”，但尚不能在线证明sheep scaling的因果收益。

## 与v4的正确比较方式

v4当前4个Public episodes为3W-1L、rating 664.0；v5-A当前仅1W-0L、rating 703.0。由于simulation rating会随新episode和对手rating变化，**不能据此宣布v5-A已经优于v4**。

## 决策

- v5-A保持active，继续收集Public episodes；
- 达到至少5个Public episodes前，不提交v5-B、不扫描参数；
- 第5局后按W/L/T、失败shop组合、晚盘margin共同复盘；
- 若出现高Yarn场景，重点核对新增sheep是否改善day27–29产能且未造成feed/labor崩溃。
