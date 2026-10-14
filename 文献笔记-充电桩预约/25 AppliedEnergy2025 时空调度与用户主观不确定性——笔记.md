---
type: 文献笔记
title: "A spatial-temporal scheduling framework for EV charging with multi-mode coordination and user subjective uncertainty"
authors: Zhang Z. et al.
journal: Applied Energy
year: 2025
volume: "401"
pages: "126818"
doi: 10.1016/j.apenergy.2025.126818
pdf: "[[papers/2025_Zhang_Spatial_Temporal_Subjective_Uncertainty.pdf]]"
direction: [方向①车主行为差异, 方向②突发事件]
priority: 中
difficulty: ★★★★
status: 未读
tags:
  - 论文/文献
  - 不确定性
  - 用户行为
---

# 25 时空调度 + 用户主观不确定性

## 一句话

多模式协同的时空调度框架，核心关键词是 **user subjective uncertainty（用户主观不确定性）**。

## 为什么对方向① 有价值

我读的 CPT 那篇（TR-C 2019）是把"主观"用**前景理论**表达的。这篇是**另一个角度**：

- **主观不确定性**作为一种**独立的不确定性来源**——不是客观概率分布不够准，而是**用户自己也不确定自己要什么**
- 这和"客观随机"（到达时间随机）是两回事

如果我打算把方向① 做深，这是区别于 CPT 的**备选理论工具**。好处是：不用引入前景理论那套参数标定（α、λ 很难说服审稿人）。

## 我的想法

<!-- 读的时候往这里写 -->

- 我的用户分类是不是可以把"主观不确定性"作为分类维度之一？
  - 如：目标明确型（离站时间确定） vs 目标模糊型（自己都不知道几点走）
- 这一类用户才是"预留容量"最难服务的——因为连他自己都不知道要多少

---

[[000 索引 · 第二批12篇]]
