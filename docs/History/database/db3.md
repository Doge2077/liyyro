---
title: "3. SQL 与 MySQL 基础"
date: 2023-04-13
categories: [DataBase System]
description: ""
---

## 3.0 参考资料

---

* [【已授权】白马程序员JavaWeb](https://www.bilibili.com/video/BV1CL4y1i7qR/?spm_id_from=333.999.0.0&vd_source=ce95ad6607d316dd76f87b90ab69fa3f)
  * [菜鸟教程 SQL教程](https://www.runoob.com/sql/sql-tutorial.html)
  * [菜鸟教程 MySQL教程](https://www.runoob.com/mysql/mysql-tutorial.html)

---

## 3.1 SQL 简介

---

### 3.1.1 SQL 概念及特点

---

#### 基本概念

* `SQL`（**Structured Query Language：结构化查询语言**）用于管理关系数据库管理系统（`RDBMS`）。
  * `SQL` 的范围包括数据插入、查询、更新和删除，数据库模式创建和修改，以及数据访问控制。
  * 这类数据库包括：`MySQL`、`SQL Server`、`Access`、`Oracle`、`Sybase`、`DB2` 等。
  * `SQL` 在 `1986` 年成为 `ANSI`（American National Standards Institute 美国国家标准化组织）的一项标准，在 `1987` 年成为国际标准化组织（ISO）标准。

#### 特点

* **综合统一**：集数据定义语言、数据操纵语言、数据控制语言的功能于一体，语言风格统一。
* **高度非过程化**：无须了解存取路径。存取路径的选择以及SQL的操作过程由系统自动完成。
* **面向集合的操作方式**：采用集合操作方式，增删改查操作的对象都可以是元组的集合。
* **以同一种语法结构提供多种使用方式**：SQL 既是独立的语言，又是嵌入式语言。
* **语言简洁，易学易用**：语法简单清晰，易于学习和掌握。

---

### 3.1.2 SQL 语言的类型

---

* **数据查询语言（DQL，Data Query Language）**：基本结构是由SELECT子句、FROM子句、WHERE子句组成的查询块。
* **数据操纵语言（DML，Data Manipulation Language）**：是SQL语言中，负责对数据库对象运行数据访问工作的指令集，以INSERT、UPDATE、DELETE三种指令为核心，分别代表插入、更新与删除，是开发以数据为中心的应用程序必定会使用到的指令。
* **数据库定义语言（DDL，Data Definition Language）**：用于描述数据库中要存储的现实世界实体的语言。
* **数据库控制语言（DCL，Data Control Language）**：用来设置或更改数据库用户或角色权限的语句，包括（GRANT, DENY, REVOKE等）语句。

> 我们平时所说的CRUD其实就是增删改查（Create/Retrieve/Update/Delete）。

---

### 3.1.3 SQL 基本约定

---

#### SQL大小写不敏感

* `SQL` 对大小写不敏感：故 `SELECT` 与 `select` 是相同的，但仍建议将 `SQL` 命令语句使用纯大写字母书写，有如下优点：

```markdown
* 提高可读性：在 `SQL` 命令语句中使用纯大写可以使关键字、函数、表名等部分更加醒目，容易阅读和理解。
* 统一规范：使用纯大写可以统一 `SQL` 命令语句的书写规范，方便代码的维护和修改。
* 避免歧义：在 `SQL` 命令语句中使用纯大写可以避免大小写混用导致的语法错误和歧义。
  * 虽然 `SQL` 对大小写不敏感，但是在 `SQL` 命令语句中使用纯大写仍然是一个良好的习惯和最佳实践。

**SQL语句的分号和逗号** ：

* 某些数据库系统要求在每条 `SQL` 语句的末端使用分号。
* 分号是在数据库系统中分隔每条 `SQL` 语句的标准方法，这样就可以在对服务器的相同请求中执行一条以上的 `SQL` 语句。
* 逗号通常用来分隔列名或表达式、值或子查询等元素。
* 至于某些长语句使用逗号，在不同的数据库系统中有不同的分隔规则。

**SQL支持注释** ：

* 通过使用 `--` 或是 `#` 来编写注释内容，也可以使用 `/* 注释内容 */` 来进行多行注释。

---

### 3.1.4 MySQL 简介

---

* `MySQL` 为关系型数据库系统（Relational Database Management System）
  * `MySQL` 支持大型的数据库。可以处理拥有上千万条记录的大型数据库。
  * `MySQL` 使用标准的 `SQL` 数据语言形式。
  * `MySQL` 可以运行于多个系统上，并且支持多种语言。

---

## 3.2 基础语法

---

本节讲解 `SQL` 基础语法，具体语法示例则利用 `MySQL` 演示。

---

### 3.2.1 数据库定义语言（DDL）

---

#### 数据库操作

---

通过 `CREATE DATABASE` 来创建一个数据库：
```sql
CREATE DATABASE 数据库名
```

为了能够支持中文，我们在创建时可以设定编码格式：
```sql
CREATE DATABASE 数据库名 DEFAULT CHARSET utf8 COLLATE utf8_general_ci
```

使用 `DROP DATABASE` 来删除一个数据库：
```sql
DROP DATABASE 数据库名
```

例如在 `MySQL` 中创建数据库 `Stu_Course`：
```sql
CREATE DATABASE Stu_Course;
```

在 `MySQL` 里切换并使用指定的数据库：
```sql
USE Stu_Course;
```

设置字符集（如果创建时没有设定默认字符集，切换到需要修改的数据库下）：
```sql
SET NAMES utf8mb4;
```

查看 `MySQL` 当前字符集：
```sql
SHOW VARIABLES LIKE 'character_set%';
```

---

#### SQL 数据类型

---

以下的数据类型用于字符串存储：

* `CHAR(n)`：可以存储任意字符串，但是是固定长度为 n，如果插入的长度小于定义长度时，则用空格填充。
* `VARCHAR(n)`：也可以存储任意数量字符串，长度不固定，但不能超过 n，不会用空格填充。

以下数据类型用于存储数字：
```

* `SMALLINT`：用于存储小的整数，范围在 (-32768, 32767)；
  * `INT`：用于存储一般的整数，范围在 (-2147483648, 2147483647)；
  * `BIGINT`：用于存储大型整数，范围在 (-9,223,372,036,854,775,808, 9,223,372,036,854,775,807)；
  * `FLOAT`：用于存储单精度小数；
  * `DOUBLE`：用于存储双精度的小数；

以下数据类型用于存储时间：

* `DATE`：存储日期；
  * `TIME`：存储时间；
  * `YEAR`：存储年份；
  * `DATETIME`：存储日期和时间；

---

#### 创建表

---

数据库创建完成后，我们一般通过 `CREATE TABLE` 语句来创建一张表：
```java
CREATE TABLE 表名(
    列名 数据类型 [列级约束条件],
    列名 数据类型 [列级约束条件],
    ...
    [, 表级约束条件]
)
```

---

#### 创建索引

---

在数据量变得非常庞大时，通过创建索引，能够大大提高查询效率：
```java
# 创建索引
CREATE INDEX 索引名称 ON 表名 (列名)

# 查看表中的索引
SHOW INDEX FROM 表名
```

删除索引：
```java
DROP INDEX 索引名称 ON 表名
```

**例如**：

在 `MySQL` 中，为 SC 表的 “Grade” 字段创建一个普通索引，命名为 `sc_idx`。
```java
CREATE INDEX sc_idx ON SC (Grade);
```

**注意**：

* 虽然添加索引后会使得查询效率更高，但是我们不能过度使用索引；
  * 索引为我们带来高速查询效率的同时，也会在数据更新时产生额外建立索引的开销，同时也会占用磁盘资源。
  * 此外，`MySQL` 的索引机制将在后续章节详细介绍。

---

#### 列级约束条件

---

列级约束有六种：

* 主键：`PRIMARY KEY`；
  * 外键：`FOREIGN KEY`；
  * 唯一：`UNIQUE`；
  * 检查：`CHECK`（MySQL 不支持）；
  * 默认：`DEFAULT`；
  * 非空/空值：`NOT NULL` / `NULL`。

---

#### 表级约束条件

---

表级约束有四种：主键、外键、唯一、检查

**例如**：

在 `MySQL` 中创建如下表：

列名 | 数据类型 | 宽度 | 允许空值 | 缺省值 | 主键 | 外键 | 说明
---|---|---|---|---|---|---|---
Cno | CHAR | 4 | 否 |  | 是 |  | 课程号
Cname | CHAR | 40 | 是 |  |  |  | 课程名
Cpno | CHAR | 4 | 是 |  |  | 是 | 先行课
Ccredit | SMALLINT |  | 是 |  |  |  | 学分
```java

```sql
CREATE TABLE Course (
    Cno CHAR(4) NOT NULL COMMENT '课程号',
    Cname CHAR(40) NULL COMMENT '课程名',
    Cpno CHAR(4) NULL COMMENT '先行课',
    Ccredit SMALLINT NULL COMMENT '学分',
    PRIMARY KEY (Cno),
    FOREIGN KEY (Cpno) REFERENCES Course(Cno)
) ENGINE=INNODB DEFAULT CHARSET=utf8;
```

---

#### 修改表

如果我们想修改表结构，我们可以通过 `ALTER TABLE` 来进行修改：
```sql
ALTER TABLE 表名 
    [ADD 新列名 数据类型[列级约束条件]]
    [DROP COLUMN 列名[RESTRICT|CASCADE]]
    [ALTER COLUMN 列名 新数据类型]
```

* `ADD`：添加一个新的列。
* `DROP`：删除一个列，可以添加 `RESTRICT` 或 `CASCADE`：
  * 默认是 `RESTRICT`，表示如果此列作为其他表的约束或视图引用到此列时，将无法删除；
  * `CASCADE` 会强制连带引用此列的约束、视图一起删除。
* `ALTER`：来修改此列的属性。

**例如**：

在 `MySQL` 中给 `Course` 表增加一列，字段名为 `Ctype`（课程类型），类型为 `CHAR`，长度为10，允许为空值：
```sql
ALTER TABLE Course 
ADD Ctype CHAR(10) NULL COMMENT '课程类型';
```

删除Ctype字段：
```sql
ALTER TABLE Course 
DROP Ctype;
```

---

#### 删除表

我们可以通过 `DROP TABLE` 来删除一个表：
```sql
DROP TABLE 表名[RESTRICT|CASCADE]
```

其中 `RESTRICT` 和 `CASCADE` 的效果与修改表时一致。

**例如**：

在 `MySQL` 中删除表 `Course`：
```sql
DROP TABLE Course;
```

---

### 3.2.2 数据库操纵语言（DML）

#### 插入数据

使用 `INSERT INTO` 语句来向数据库中插入一条数据（一条记录）：
```sql
INSERT INTO 表名 VALUES(值1, 值2, 值3)
```

如果插入的数据与列一一对应，那么可以省略列名，但是如果希望向指定列上插入数据，就需要给出列名：
```sql
INSERT INTO 表名(列名1, 列名2) VALUES(值1, 值2)
```

我们也可以一次性向数据库中插入多条数据：
```sql
INSERT INTO 表名(列名1, 列名2) VALUES(值1, 值2), (值1, 值2), (值1, 值2)
```

**例如**：

在 `MySQL` 中的表格 `SC` 中：

Sno | Cno | Grade  
---|---|---  
200215121 | 1 | 92  
  
插入一条数据 `{200215122, 2, 90}`
```sql

INSERT INTO SC(Sno, Cno, Grade) VALUES(200215122, 2, 90);
```

---

#### 修改数据

---

我们可以通过 `UPDATE` 语句来更新表中的数据：
```sql

UPDATE 表名 SET 列名=值,... WHERE 条件
```

**例如** ：

在 `MySQL` 中，将Course表中的课程号为“2”的学分改为4：
```sql

UPDATE Course SET Ccredit=4 WHERE Cno='2';
```

---

#### 删除数据

---

我们可以通过使用 `DELETE` 来删除表中的数据：
```sql

DELETE FROM 表名
```

通过这种方式，将删除表中全部数据，我们也可以使用 `WHERE` 来添加条件，只删除指定的数据：
```sql

DELETE FROM 表名 WHERE 条件
```

**例如** ：

在 `MySQL` 中，删除 `Course` 表中的课程号为“2”的数据：
```sql

DELETE FROM Course WHERE Cno='2';
```

---

### 3.2.3 数据库查询语言（DQL）

---

#### 单表查询

---

使用 `SELECT` 语句来进行单表查询：
```sql

# 指定查询某一列数据
SELECT 列名[,列名] FROM 表名

# 会以别名显示此列
SELECT 列名 别名 FROM 表名

# 查询所有的列数据
SELECT * FROM 表名

# 只查询不重复的值
SELECT DISTINCT 列名 FROM 表名
```

添加 `WHERE` 子句以限定查询目标，且支持正则表达式：
```sql

SELECT * FROM 表名 WHERE 条件
```

**例如** ：

在 `MySQL` 中，在 `SC` 表中查询成绩大于90分的学生的全部信息：
```sql

SELECT * FROM SC WHERE Grade > 90;
```

---

#### 常用查询条件

---

* 一般的比较运算符，包括 `=`、`>`、`&lt;`、`&gt;=`、`&lt;=`、`!=` 等，其中 `!=` 也可以用 `&lt;&gt;` 表示；
  * 是否在集合中：`IN`、`NOT IN`；
  * 字符模糊匹配：`LIKE`，`NOT LIKE`；
  * 多重条件连接查询：`AND`、`OR`、`NOT`；

**例如** ：

在 `MySQL` 中，查询Student表中名字的第二个字是“雨”或“玉”的同学的学号Sno：
```sql

SELECT Sno FROM Student WHERE Sname LIKE '_雨%' OR Sname LIKE '_玉%'; 
```

---

#### 排序查询

---

通过 `ORDER BY` 来将查询结果进行排序：
```sql

SELECT * FROM 表名 WHERE 条件 ORDER BY 列名 ASC|DESC
```

使用 `ASC` 表示升序排序，使用 `DESC` 表示降序排序，默认为升序。

也可以同时添加多个排序：
```sql
SELECT * FROM 表名 WHERE 条件 ORDER BY 列名1 ASC|DESC, 列名2 ASC|DESC;
```

这样会先按照列名1的值进行排序，每组列名1相同的数据再按照列名2的值排序。

**例如**：
在 `MySQL` 中，在 `SC` 表中查询成绩大于90分的学生全部信息并按照分数从大到小排序：
```sql
SELECT * FROM SC WHERE Grade > 90 ORDER BY Grade DESC;
```

---

#### 聚集函数

聚集函数一般用作统计，包括：

*   `COUNT([DISTINCT]*)`：统计所有的行数（`DISTINCT` 表示去重）；
*   `COUNT([DISTINCT] 列名)`：统计某列的值个数；
*   `SUM([DISTINCT] 列名)`：求一列的和（注意必须是数字类型）；
*   `AVG([DISTINCT] 列名)`：求一列的平均值（注意必须是数字类型）；
*   `MAX([DISTINCT] 列名)`：求一列的最大值；
*   `MIN([DISTINCT] 列名)`：求一列的最小值。

一般用法：
```sql
SELECT COUNT(DISTINCT 列名) FROM 表名 WHERE 条件;
```

**例如**：
在 `MySQL` 中，通过 `SC` 表计算“2”号课程的学生平均成绩、最高分、最低分：
```sql
SELECT AVG(Grade) AS '平均成绩', MAX(Grade) AS '最高分', MIN(Grade) AS '最低分'
FROM SC
WHERE Cno = '2';
```

---

#### 分组和分页查询

通过 `GROUP BY` 来对查询结果进行分组，需结合聚合函数一起使用：
```sql
SELECT SUM(*) FROM 表名 WHERE 条件 GROUP BY 列名;
```

添加 `HAVING` 来限制分组条件：
```sql
SELECT SUM(*) FROM 表名 WHERE 条件 GROUP BY 列名 HAVING 约束条件;
```

添加 `LIMIT` 来限制查询的数量，只取前N个结果：
```sql
SELECT * FROM 表名 LIMIT 数量;
```

查询数据很多时，可以对结果进行分页：
```sql
SELECT * FROM 表名 LIMIT 起始位置, 数量;
```

**例如**：
在 `MySQL` 中，汇总总分大于200分的学生学号及总成绩：
```sql
SELECT Sno, SUM(Grade) AS '总成绩'
FROM SC
GROUP BY Sno
HAVING SUM(Grade) > 200;
```

---

#### 外连接查询

在 `SQL` 中，支持以下连接查询：

*   `INNER JOIN`：如果表中有至少一个匹配，则返回行；
*   `LEFT JOIN`：即使右表中没有匹配，也从左表返回所有的行；
*   `RIGHT JOIN`：即使左表中没有匹配，也从右表返回所有的行；
*   `FULL JOIN`：只要其中一个表中存在匹配，则返回行。

在 `MySQL` 中，外连接查询用于联合多个表格进行查询，外连接查询有以下三种方式：

* `INNER JOIN`（内连接，或等值连接）：获取两个表中字段匹配关系的记录，即**返回两个表满足条件的交集部分**。
* `LEFT JOIN`（左连接）：获取左表所有记录，即使右表没有对应匹配的记录，即**返回两个表满足条件的交集部分，也会返回左边表中的全部数据，而在右表中缺失的数据会使用 `NULL` 来代替**。
* `RIGHT JOIN`（右连接）：与 `LEFT JOIN` 相反，即**返回两个表满足条件的交集部分，也会返回右边表中的全部数据，而在左表中缺失的数据会使用 `NULL` 来代替**。

**例如**：

在 `MySQL` 中，查询所有学生的选课信息：
```sql
SELECT Student.*, SC.Cno, SC.Grade
FROM Student
LEFT JOIN SC
ON Student.Sno = SC.Sno;
```

---

#### 自身连接查询

---

除上述连接查询外，`MySQL` 还支持自身连接查询。

将表本身和表进行笛卡尔积计算，得到结果，但是由于表名相同，因此要先起一个别名：
```sql
SELECT * FROM 表名 别名1, 表名 别名2
```

---

#### 嵌套查询

---

将查询的结果作为另一个查询的条件，比如：
```sql
SELECT * FROM 表名 WHERE 列名 = (SELECT 列名 FROM 表名 WHERE 条件)
```

---

### 3.2.4 数据库控制语言（DCL）

---

#### 创建用户

---

通过 `CREATE USER` 来创建用户：
```sql
CREATE USER 用户名 IDENTIFIED BY 密码;
```

也可以不带密码：
```sql
CREATE USER 用户名;
```

**例如**：

在 `MySQL` 中创建用户：
```sql
CREATE USER 'LYS' IDENTIFIED BY '1145141919';
```

通过 `@` 来限制用户登录的 IP 地址，`%` 表示匹配所有的 IP 地址，默认使用的就是任意 IP 地址。
```sql
CREATE USER 'LYS'@'114.114.19.19' IDENTIFIED BY '514180';
```

---

#### 登录用户

---

通过 `cmd` 去登录 `mysql`：
```sql
mysql -u 用户名 -p
```

输入密码后即可登录此用户，我们输入以下命令来看看能否访问所有数据库：
```sql
SHOW DATABASES;
```

虽然此用户能够成功登录，但是并不能查看完整的数据库列表，这是因为**此用户还没有权限**！

---

#### 用户授权

---

我们可以通过 `root` 用户使用 `grant` 来为一个数据库用户进行授权：
```sql
GRANT ALL|权限1,权限2...(列1,...) ON 数据库.表 TO 用户 [WITH GRANT OPTION]
```

其中 `all` 代表授予所有权限，当数据库和表为 `*`，代表为所有的数据库和表都授权。如果在最后添加了 `WITH GRANT OPTION`，那么被授权的用户还能将已获得的授权继续授权给其他用户。

我们可以使用 `REVOKE` 来收回一个权限：
```sql
REVOKE ALL|权限1,权限2...(列1,...) ON 数据库.表 FROM 用户
```

**例如**：

在 `MySQL` 中：
```sql
GRANT ALL ON *.* TO 'LYS' WITH GRANT OPTION;  #给 LYS 用户授权所有数据库的所有权限且可以给其他用户授权

REVOKE ALL ON *.* FROM 'LYS';  # 收回 LYS 的全部权限
```

---

### 3.2.5 视图

---

#### 视图的本质

- 可以将数据库视为一个大楼，里面的房间视为表，房间里的人就是具体的数据；
- 那么视图相当于在这个房间上面开了一个“窗口”，能够根据用户的需要来查看数据；
- 可以对这个“窗口”进行调整（修改），但无论如何修改都无法影响到房间内的人（实际的数据）；
- 因此**视图的本质就是一张虚表**。

---

#### 创建视图

通过 `CREATE VIEW` 来创建视图：
```sql
CREATE VIEW 视图名称(列名) AS 子查询语句 [WITH CHECK OPTION];
```

`WITH CHECK OPTION` 是指当创建后，如果更新视图中的数据，是否要满足子查询中的条件表达式，不满足将无法插入。创建后，我们就可以使用 `SELECT` 语句来直接查询视图上的数据了，因此，还能在视图的基础上，导出其他的视图。

**注意**：

- 若视图是由两个以上基本表导出的，则此视图不允许更新。
- 若视图的字段来自字段表达式或常数，则不允许对此视图执行 `INSERT` 和 `UPDATE` 操作，但允许执行 `DELETE` 操作。
- 若视图的字段来自集函数，则此视图不允许更新。
- 若视图定义中含有 `GROUP BY` 子句，则此视图不允许更新。
- 若视图定义中含有 `DISTINCT` 短语，则此视图不允许更新。
- 若视图定义中有嵌套查询，并且内层查询的 `FROM` 子句中涉及的表也是导出该视图的基本表，则此视图不允许更新。
- 一个不允许更新的视图上定义的视图也不允许更新。

---

#### 删除视图

通过 `DROP VIEW` 来删除一个视图：
```sql
DROP VIEW 视图名称;
```

---

#### 视图示例

在 `MySQL` 中，建立一个名为 `v_stu_c` 的视图，显示学生的学号、姓名、所学课程的课程编号，并利用视图查询学号为200215122的学生情况。
```sql
CREATE VIEW v_stu_c AS 
SELECT s.Sno, s.Sname, c.Cno 
FROM Student s, Course c, SC sc 
WHERE s.Sno = sc.Sno AND c.Cno = sc.Cno;

SELECT * 
FROM v_stu_c 
WHERE Sno = '200215122';
```

---

### 3.2.6 数据库完整性

---

#### 触发器

在某种条件下会**自动触发**，在 `INSERT`/`UPDATE`/`DELETE` 时，会自动执行我们预先设定的内容。触发器通常用于检查内容的安全性，相比直接添加约束，触发器显得更加灵活。

触发器所关联的表称为基本表，当触发表上发生 `SELECT`/`UPDATE`/`DELETE` 等操作时，会自动生成两个临时的表（`NEW` 表和 `OLD` 表，只能由触发器使用）。

**例如**：

* 在 `INSERT` 操作时，新的内容会被插入到 `NEW` 表中；
* 在 `DELETE` 操作时，旧的内容会被移到 `OLD` 表中，我们仍可在 `OLD` 表中拿到被删除的数据；
* 在 `UPDATE` 操作时，旧的内容会被移到 `OLD` 表中，新的内容会出现在 `NEW` 表中。

```sql
CREATE TRIGGER 触发器名称 [BEFORE|AFTER] [INSERT|UPDATE|DELETE] ON 表名/视图名 FOR EACH ROW DELETE FROM Student WHERE Student.sno = NEW.sno
```

`FOR EACH ROW` 表示针对每一行都会生效，无论哪行进行指定操作都会执行触发器。

通过下面的命令来查看触发器：
```sql
SHOW TRIGGERS;
```

删除此触发器：
```sql
DROP TRIGGER 触发器名称;
```

---

#### 事务

---

**概念**：

* `SQL` 的事务（Transaction）是一组数据库操作的逻辑单元，这些操作被视为一个整体，必须全部完成或全部不完成，以保持数据的一致性。
* 如果其中某个操作失败，则整个事务均不会执行，已经执行过的操作会被自动回滚（撤销），从而保证数据的完整性和一致性。

事务通常使用以下语句来操作：

* `BEGIN TRANSACTION` 或 `START TRANSACTION`：开始一个新的事务。
* `COMMIT`：提交事务，并将其中的所有操作永久保存到数据库。
* `ROLLBACK`：撤销事务中的所有操作，回滚到事务开始前的状态。

`SQL` 的事务处理是保证并发控制的一个重要机制，可以**在多用户并发访问数据库时，确保数据的一致性和完整性**。

**注意**：

* 在 `MySQL` 中，只有 `Innodb` 引擎支持事务，我们可以这样来查看支持的引擎：

```sql
SHOW ENGINES;
```

`MySQL` 默认采用的是 `Innodb` 引擎，也可以去修改为其他的引擎。

* 避免在事务执行过程中使用锁表（例如通过 `LOCK TABLES` 命令）来修改数据，这会影响事务的性能和并发度。

**事务的特性**：

* 原子性：一个事务（transaction）中的所有操作，要么全部完成，要么全部不完成，不会结束在中间某个环节。事务在执行过程中发生错误，会被回滚（Rollback）到事务开始前的状态，就像这个事务从来没有执行过一样。
* 一致性：在事务开始之前和事务结束以后，数据库的完整性没有被破坏。这表示写入的数据必须完全符合所有的预设规则，这包含数据的精确性、一致性以及后续数据库可以自发性地完成预定的工作。
* 隔离性：数据库允许多个并发事务同时对其数据进行读写和修改操作，隔离性可以防止多个事务并发执行时由于交叉执行而导致数据的不一致。事务隔离分为不同级别，包括读未提交（Read uncommitted）、读已提交（Read committed）、可重复读（Repeatable read）和串行化（Serializable）。
* 持久性：事务处理结束后，对数据的修改就是永久的，即便系统故障也不会丢失。

我们通过以下例子来探究事务的使用：
```java
START TRANSACTION;  # 开始事务

INSERT INTO orders (customer_id, total_price) VALUES (1, 100.0);  # 向订单表中插入一个订单记录
UPDATE customers SET balance = balance - 100.0 WHERE id = 1;  # 更新客户表中对应的用户余额

COMMIT;  # 提交事务
# 一旦提交，就无法再进行回滚了！
```