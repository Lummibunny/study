---
type: 文献笔记
title: "A synergistic EV charging framework for smart cities with commitment-driven penalty mechanism and preference-based optimal charging source selection"
authors: Rajapandiyan A., Subbaiyan T.
journal: Applied Energy
year: 2025
volume: "401"
pages: "126780"
doi: 10.1016/j.apenergy.2025.126780
pdf: "[[papers/2025_Rajapandiyan_Commitment_Driven_Penalty_EV_Charging.pdf]]"
direction: [方向①车主行为差异, 机制设计]
priority: 高（补"违约"空白）
difficulty: ★★★★
status: 未读
tags:
  - 论文/文献
  - 机制设计
  - 违约惩罚
---

# 21 承诺驱动的惩罚机制

## 一句话

G2V（电网→车）+ V2V（车→车）协同的能量交易框架，核心创新是**对"违约行为"设惩罚**，并用用户偏好做充电源选择。

## 三个零件

| 零件 | 作用 |
|---|---|
| **多臂老虎机（MAB）动态定价** | 学习最优价格 |
| **Gale-Shapley 匹配** | 稳定配对（车↔充电源） |
| **违约行为惩罚模型** | 保证履约率 |

目标里显式写了 **schedule adherence（履约率）**。

## 为什么重要

**"违约惩罚"这个变量我一直没有。** 我读过的第 8 篇（TSG 菜单机制）假设用户说了就照做；真实世界用户会爽约、迟到、赖着不走。这篇告诉我：
- 惩罚项怎么建模
- 怎么证明它提高了履约率
- 这正好回答审稿人必问的"用户不来怎么办"

## 可复用点

1. **Gale-Shapley 匹配协议**：用户偏好 → 稳定配对。如果我做"预约请求 ↔ 时段/桩位"的匹配，这是标准工具
2. **违约金模型**的写法
3. **履约率**作为评价指标（我现在一张指标表都没有，要从这补）

## 我的想法

<!-- 读的时候往这里写 -->

- 惩罚项在我的模型里对应什么？违约押金？信用分？
- 我的用户分类（可靠型/灵活型/高违约风险型）→ 每类的违约概率不同 → 惩罚力度也要不同？
  （如果是，这就是一个很像样的创新点）

---

[[000 索引 · 第二批12篇]]
