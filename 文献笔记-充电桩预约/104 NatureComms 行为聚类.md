---
type: 文献笔记
title: Behavioral uncertainty in EV charging drives heterogeneous grid load variability under climate goals
authors: Zhang B., Xin Q., Chen S., Wang Z., Lu Y., Niu N., Zhang F., Liu G., Bansal P.
journal: Nature Communications
year: 2026
volume: "17"
doi: 10.1038/s41467-025-66796-4
pdf: "[[papers/2026_Zhang_Behavioral_Uncertainty_EV_Charging_Grid_Load.pdf]]"
direction:
  - 方向①车主行为差异
priority: 高（解决"凭什么这么分类"）
tags:
  - 文献笔记
---

# ④ 用真实数据聚类出 5 类充电行为

## 一句话

用国家级新能源车监测平台的高分辨率真实充电数据，按 6 个特征聚类，识别出 **5 类充电行为**，并量化每类对负荷波动的影响。

## 五类行为

| 类别 | 占比 |
|---|---|
| 有序充电 | 12% |
| 快充 | 6% |
| 里程焦虑 | 35% |
| 峰时部分充 | 31% |
| 峰时充满 | 16% |

聚类特征：开始时间、时长、初/末 SOC、充电量、最大电流。用**轮廓系数**定类数。

## 为什么重要

北京理工大学 + 新加坡国立大学，**中国数据、顶刊**——这是你写引言时能 cite 的"中国场景"依据。而且它直接解决方向①最致命的质疑：**"你凭什么这么分类？"**

## 可复用的范式

**特征提取 → 聚类 → 定类数 → 命名 → 验证**，完整闭环。还有：
- 把分类结果与系统指标挂钩的论证方式
- 顶刊 Discussion 章节的写法

## 提醒

它是宏观电网视角，**只借分类方法论**，别被带偏到电力系统规划。

## 我的想法

<!-- 读的时候往这里写 -->

- 这 5 类能否收敛成我的 3 类？（如：履约可靠型 / 灵活型 / 高违约风险型）
- 我的分类依据要用什么数据？没有真实数据怎么办？

---

[[000 索引 · 顶刊8篇]]
