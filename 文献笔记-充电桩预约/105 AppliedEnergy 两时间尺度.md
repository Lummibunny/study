---
type: 文献笔记
title: "Risk-aware day-ahead baseline scheduling and real-time rolling correction for coupled EV charging and edge-service operation under distribution-network constraints"
journal: Applied Energy
year: 2026
volume: "426"
pages: "128600"
doi: 10.1016/j.apenergy.2026.128600
pdf: "[[papers/2026_Risk_Aware_Day_Ahead_Baseline_Rolling_Correction.pdf]]"
direction: [方向③日前+临时, 方向②突发事件]
priority: 最高（框架直接可抄）
difficulty: ★★★★★
status: 未读
tags:
  - 论文/文献
  - 充电桩预约
  - 必读
---

# ⑤ 日前基线包络 + 实时滚动校正

## 一句话

日前生成**"基线包络"**，实时层在包络内做滚动校正。

## 两层结构

**日前层**：对每个区域能量聚合商构造基线包络，包含
- 充���与服务参考值
- **允许运行范围（admissible operating ranges）**
- **双向灵活裕度**
- 迁移配额（migration allowances）
- 基线状态

方法：预测中心化残差场景 + **CVaR** + 粒子群搜索（mini-batch 场景评估）

**实时层**：在已发布的包络内滚动校正
- Kalman 滤波更新部分可观测状态
- 校正后的设定点**投影回允许运行范围**
- LinDistFlow 校验馈线可接纳性

算例：深圳充电场景 + IEEE 33 节点馈线。

## 为什么关键

**「基线包络 + 允许调整范围」** 这个提法，正是 **"日前预约预留多少容量 + 临时充电能挤占多少额度"** 的数学表达。**这是你方向③最有可能立住的创新点。**

## 提醒

研究对象耦合了**边缘计算服务**，与你的场景不同。**借框架，不借场景。** Kalman 和 LinDistFlow 部分可略读。

## 我的想法

<!-- 读的时候往这里写 -->

- "包络"在我这儿对应什么？预留容量上界 + 下界？
- 挤占规则怎么写进约束里？

---

[[000 索引 · 顶刊8篇]]
