---
tags:
  - SQL
---
# 一、
外连接（对位置敏感）：
> **左表 = 你要"一行都不能少"的那张表。**  
> 写查询前先问自己："题目要我保留谁？" —— 是它，就放到 `FROM` 后面。
**1. `ON` 两边交换顺序无所谓**  
`ON e.building = b.building_name` 和 `ON b.building_name = e.building` 完全等价，就是等号两边换了个位置。**真正影响结果的只有表的先后顺序**，别把这两件事混在一起。

**2. LEFT 和 RIGHT 是可以互相翻译的**
FROM buildings LEFT JOIN employees   -- 保留 buildings 全部
完全等同于
FROM employees RIGHT JOIN buildings  -- 保留 buildings 全部
==`A LEFT JOIN B` ≡ `B RIGHT JOIN A`==，只是列的显示顺序可能不一样。所以实际工作中**绝大多数人只用 LEFT JOIN**，从不写 RIGHT JOIN——把要保留的表放前面就行了，省得脑子绕。

**3. INNER JOIN 才真的无所谓左右**  
`A INNER JOIN B` 和 `B INNER JOIN A` 结果一样，因为内连接两边都只留配对成功的行，谁也不特殊。**只有外连接（LEFT/RIGHT）才对位置敏感**。

### 实战顺口溜

> 内连接：左右随意。  
> 外连接：**要留谁，谁在 FROM 后面。**（左连接）

=="没有 X 的 Y"，就用 `FROM Y LEFT JOIN X ... WHERE X.主键 IS NULL`。==

# 二、符号运算
1、`%` 是**取余运算符**，`year % 2 = 0` 就是"能被 2 整除 = 偶数"。（等价写法 `MOD(year, 2) = 0`。）
2、**判奇偶就靠 `% 2`**——`奇数 % 2 = 1`。以后"每 3 行取一行"之类也是这个思路。

# 三、常用统计函数
1、`GROUP BY` 数据分组语法可以按某个col_name对数据进行分组，
- ·如：`GROUP BY Year`指对数据按年份分组， 相同年份的分到一个组里。如果把统计函数和`GROUP BY`结合，那统计结果就是对分组内的数据统计了.  
- `GROUP BY` 分组结果的数据条数，就是分组数量，比如：`GROUP BY Year`，全部数据里有几年，就返回几条数据， 不管是否应用了统计函数.
2、![[Pasted image 20260921121823.png]]3、

