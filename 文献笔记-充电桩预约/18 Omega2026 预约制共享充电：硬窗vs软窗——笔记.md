---
type: 文献笔记
title: "Shared charging strategies at the electric bus depot: A robust optimization model"
authors: Huang et al.
journal: Omega
year: 2026
pdf: "[[papers/2026_Huang_Reservation_Based_Shared_Charging_Bus_Depot.pdf]]"
direction:
  - 方向③日前+临时
priority: 最高
difficulty: ★★★★
tags:
  - 论文/文献
---

# 18 预约制共享充电：硬窗 vs 软窗
电动公交场站白天充电能力闲置 → 用**预约制（R-SC）**开放给私家车用户创收；难点是**不能牺牲公交的充电可靠性**，用鲁棒优化处理公交能耗不确定性。


| 策略 | 机制 |
|---|---|
| **硬充电时间窗 + 固定定价** | 预约时段锁死，价格固定 |
| **软充电时间窗 + 可变差异化定价** | 时段可弹性，价格区分 |

实验结果：R-SC 显著优于现状。


**"硬窗 vs 软窗"就是我"日前预留固定容量 vs 预约容量可弹性挤占"的另一种说法。** 这篇给了：
- 一个现成的**对照组设计**（我论文的实验可以做"我们比硬窗好"）
- 差异化定价作为软窗的配套工具
- Omega 是运筹学顶刊，我的参考文献里之前一篇都没有

## 可复用建模点

- 预约共享资源的**双层张力**：主用户（公交）可靠性 vs 次用户（私家车）需求
- 不确定性只放在主用户侧（公交能耗），次用户用预约锁定 → **不确定性分解**的写法
- 两种管理策略对比的实验框架


---


