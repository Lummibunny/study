---
tags: SQL
---

# SQL 零基础入门速查（刷题前必看）


> 整理日期：2026-09-14
> 适用：SQLZoo / LeetCode 刷题前的语法速查 ｜ 面向有 Python 基础但零 SQL 基础的同学
> 配套计划：《W1_SQL七天刷题计划.md》

---

## 一、核心概念（先建立直觉）

SQL 操作的对象是**二维表格**，和 pandas 的 DataFrame 完全同构：

| 概念 | 说明 | 例子 |
|------|------|------|
| 表 table | 一张二维表 | `world`（各国信息表） |
| 列 column | 字段 | `name` / `population` / `area` |
| 行 row | 一条记录 | France, Europe, 67158000 |
| 查询 | 从表里取数据 | `SELECT ... FROM ... WHERE ...` |

**一句话**：SQL = 用一句话描述"我想要表里的哪些行、哪些列"。

---

## 二、语法骨架（一条完整查询）

```sql
SELECT 列1, 列2          -- ① 要哪些列
FROM 表名                -- ② 从哪张表
WHERE 条件               -- ③ 筛哪些行（不能用聚合函数）
GROUP BY 列              -- ④ 分组
HAVING 分组条件           -- ⑤ 筛分组（可以用聚合函数）
ORDER BY 列 DESC         -- ⑥ 排序（DESC 降序 / ASC 升序）
LIMIT 10;                -- ⑦ 只取前 10 行
```

### 书写顺序 vs 执行顺序（重点！）

- **书写顺序**：SELECT → FROM → WHERE → GROUP BY → HAVING → ORDER BY → LIMIT
- **执行顺序**：FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT

**理解要点**：
- `WHERE` 在分组**之前**筛（管行），所以不能写 `COUNT(*)`
- `HAVING` 在分组**之后**筛（管组），所以能写 `COUNT(*)`
- `ORDER BY` 在 SELECT 之后执行，所以可以用 SELECT 里起的别名排序

---

## 三、常用语法速查表（含 Python 对照）

| SQL 写法 | 作用 | Python 对照 |
|---|---|---|
| `SELECT a, b` | 取哪些列 | `df[['a','b']]` |
| `SELECT *` | 取所有列（刷题可用，工作慎用） | `df` |
| `FROM world` | 从哪张表 | 数据来源 |
| `WHERE x = 'v'` | 等于 | `df[df['x']=='v']` |
| `WHERE x <> 'v'` 或 `!=` | 不等于 | `df[df['x']!='v']` |
| `WHERE a AND b` | 且 | `&` |
| `WHERE a OR b` | 或 | `\|` |
| `WHERE NOT a` | 非 | `~` |
| `WHERE x IN ('a','b')` | 在列表中 | `.isin(['a','b'])` |
| `WHERE x BETWEEN 1 AND 9` | 范围（**含边界**） | `.between(1,9)` |
| `WHERE name LIKE 'A%'` | 模糊匹配（%任意多字符，_单字符） | `.str.startswith('A')` |
| `WHERE x IS NULL` | 判空（不能用 `= NULL`） | `.isna()` |
| `ORDER BY x DESC` | 降序排序 | `.sort_values(ascending=False)` |
| `ORDER BY x ASC` | 升序（默认） | `.sort_values()` |
| `LIMIT 10` | 取前 10 行 | `.head(10)` |
| `SELECT DISTINCT x` | 去重 | `.unique()` |
| `COUNT(*) / COUNT(x)` | 计数 | `.count()` |
| `SUM(x) / AVG(x)` | 求和 / 平均 | `.sum() / .mean()` |
| `MIN(x) / MAX(x)` | 最小 / 最大 | `.min() / .max()` |
| `GROUP BY x` | 分组 | `.groupby('x')` |
| `HAVING COUNT(*)>5` | 筛选分组 | `.filter()` |
| `AS 别名` | 起列名 | `.rename()` |
| `ROUND(x, 2)` | 四舍五入保留2位 | `.round(2)` |
| `CONCAT(a, b)` | 字符串拼接 | `a + b` |

---

## 四、聚合函数（GROUP BY 的搭档）

```sql
SELECT continent, COUNT(*) AS cnt, AVG(population) AS avg_pop
FROM world
GROUP BY continent
HAVING COUNT(*) > 3
ORDER BY cnt DESC;
```

**关键规则**：
- `GROUP BY` 之后，SELECT 里**只能出现：分组列 + 聚合函数**
  - ✅ `SELECT continent, COUNT(*)`
  - ❌ `SELECT continent, name, COUNT(*)`（name 没分组也没聚合，报错）
- `COUNT(*)` 数所有行；`COUNT(列名)` **跳过该列的 NULL 值**
- **一个 NULL 参与聚合时的行为**：SUM/AVG 会自动忽略 NULL；COUNT(列) 也会忽略 NULL

---

## 五、JOIN 连接（最重要，笔试必考）

JOIN = 把两张表按**共同列**拼起来（等价 pandas 的 `merge`）。

```sql
SELECT a.name, b.score
FROM students a
INNER JOIN scores b ON a.id = b.student_id;
```

### 四种连接的区别

| 类型 | 含义 | 结果 |
|------|------|------|
| `INNER JOIN` | 只保留两边都匹配的 | 交集 |
| `LEFT JOIN` | 左表全保留，右表无匹配填 NULL | **最常用** |
| `RIGHT JOIN` | 右表全保留 | 少用 |
| `FULL JOIN` | 两边都全保留 | 少用 |

### 高频套路（记牢）

- **"找出没做过 X 的人"** → `LEFT JOIN` + `WHERE 右表列 IS NULL`
  ```sql
  SELECT c.name
  FROM customers c
  LEFT JOIN orders o ON c.id = o.customer_id
  WHERE o.id IS NULL;   -- 从未下单的顾客
  ```
- **多表连接**：继续 `JOIN ... ON ...` 往下接即可
- **自连接**：同一张表起两个别名连接（如员工表查"比经理工资高的人"）

---

## 六、新手必踩的 8 个坑（重点记）

1. **字符串用单引号**：`'Germany'` ✅｜`"Germany"`（MySQL 勉强可以但不规范）｜`Germany` ❌
2. **判空用 `IS NULL`**，不能用 `= NULL`（= NULL 永远返回空）
3. **`WHERE` 里不能写聚合函数**，要写到 `HAVING`
4. **`GROUP BY` 后 SELECT 只能有分组列+聚合**（见上文）
5. **`COUNT(*)` vs `COUNT(列名)`**：后者跳过 NULL
6. **大小写**：关键字不敏感（select = SELECT），建议关键字大写、其余小写
7. **标点必须英文半角**：中文逗号 `，`、中文引号 `""` 会直接报错（复制题解时特别注意）
8. **语句以分号 `;` 结尾**（SQLZoo 单句可省略，工作中多语句必加）

---

## 七、常见报错信息对照

| 报错 | 原因 | 解决 |
|------|------|------|
| `You have an error in your SQL syntax` | 语法错误（多因中文标点、拼写错） | 检查标点、关键字拼写 |
| `Unknown column 'xxx'` | 列名写错了 | 核对表结构 |
| `Column 'x' must appear in GROUP BY` | GROUP BY 后选了非分组列 | 加进 GROUP BY 或用聚合包起来 |
| 结果为空但觉得应该有 | 条件写错（如 NULL 比较） | 用 IS NULL；检查字符串引号 |
| `Ambiguous column name` | 多表连接时列名重复未加表前缀 | 写成 `a.name` |

---

## 八、学习顺序建议（配合 W1 计划）

```
第 1 步：SELECT / FROM / WHERE         → SQLZoo [0][1][2]
第 2 步：ORDER BY / LIMIT / DISTINCT   → SQLZoo [1][2] 练习
第 3 步：IN / BETWEEN / LIKE / NULL    → SQLZoo [3] + [7]
第 4 步：聚合 + GROUP BY + HAVING      → SQLZoo [4]
第 5 步：JOIN（重点）                  → SQLZoo [5][6]
第 6 步：子查询                        → SQLZoo [3]
第 7 步：窗口函数                      → SQLZoo [9]
```

**刷题方法**：先看题 → 手写思路（伪代码）→ 写 SQL → 对比题解 → 记录考点到错题本

---

*先通读本文档一遍，再回到 SQLZoo 刷题，会顺利很多。遇到看不懂的关键字回来查表即可。*
