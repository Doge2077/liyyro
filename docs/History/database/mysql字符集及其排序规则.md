---
title: "MySQL字符集及其排序规则"
date: 2023-07-03
categories: [DataBase System]
description: ""
---

# utf8mb4基本介绍

---

## 基本特性

---

* utf8mb4是MySQL中一种字符集编码，它可以存储和处理Unicode字符。

* Unicode字符集中包含了几乎所有的字符，包括各种语言的字符、符号、表情符号等。

---

## 与utf8mb3的区别

---

### 版本上

---

* utf8mb4字符集在MySQL的版本5.5.3及之后开始支持。
  * 在此之前的MySQL版本，只支持utf8字符集，即utf8mb3。

---

### 编码上

---

* 在MySQL中，utf8字符集实际上只支持最多3字节的UTF-8编码。这意味着它无法正确存储和处理一些特殊字符，如一些表情符号和一些辅助字符。
  * 为了解决utf8字符集的限制，MySQL引入了utf8mb4字符集。utf8mb4字符集支持最多4字节的UTF-8编码，可以表示更广泛的字符范围，包括一些特殊字符和表情符号。

---

# utf8mb4排序规则

---

## 常见排序规则

---

* utf8mb4_general_ci：
  * 默认的排序规则，**不区分大小写** ，同时考虑了多语言的排序规则。
  * 在该规则下，'a'和'A'被认为是相等的。

* utf8mb4_unicode_ci：
  * 基于Unicode Collation Algorithm (UCA) 默认的排序规则，**不区分大小写** 。
  * 与utf8mb4_general_ci相比，utf8mb4_unicode_ci更加精确，能够正确地排序各种语言的字符。

* utf8mb4_bin：
  * 这个排序规则是基于二进制的排序规则，**区分大小写** 的，且按照字符的二进制值进行排序。
  * 在这个规则下，'A'会排在'a'之前。

* utf8mb4_0900_ai_ci：
  * 在MySQL 8.0.0版本中引入的，用于支持utf8mb4字符集的全新排序规则。
  * 在MySQL 8.0.0之前的版本中，utf8mb4字符集使用的是utf8mb4_general_ci排序规则。然而，这个排序规则对于一些特定的字符比较不够准确，可能会导致一些排序和比较结果不符合预期。
  * 基于Unicode Collation Algorithm (UCA) 9.0.0的排序规则，**不区分大小写** ，更准确地处理了各种字符的排序和比较。

除了上述常见的排序规则，MySQL还提供了其他一些排序规则，如utf8mb4_unicode_520_ci、utf8mb4_unicode_520_bin等。这些规则可以根据具体需求选择使用。

---

### 默认排序规则

---

当设置表的默认字符集为utf8mb4字符集但未明确指定排序规则时：

* 在MySQL 5.7版本中，默认排序规则为utf8mb4_general_ci。

* 在MySQL 8.0版本中，默认排序规则为utf8mb4_0900_ai_ci。

---

### 兼容性问题

---

由于utf8mb4_0900_ai_ci排序规则是MySQL 8.0引入的排序规则，因此将MySQL 8.0版本的表导入到MySQL 5.7或MySQL 5.6版本时，会存在字符集无法识别的问题。

* [Err] 1273 - Unknown collation: 'utf8mb4_0900_ai_ci'

* 解决办法：修改新建数据库的排序规则或手动修改 sql 文件内所有的排序规则。

---

### utf8mb4_unicode_ci 和 utf8mb4_general_ci 对比

* 准确性：
```text
* utf8mb4_unicode_ci 排序规则基于标准 Unicode 进行排序和比较，能处理特殊字符，能在各种语言中精确排序。
* utf8mb4_general_ci 排序规则没有基于标准 Unicode，无法处理部分特殊字符。
```
* 性能上：
```text
* utf8mb4_general_ci 排序规则在排序性能上相对较好；
* utf8mb4_unicode_ci 排序规则为处理特殊字符实现复杂的排序算法，性能略差。
* 在大部分场景下，两者没有明显的性能差异。
```

---

## 服务器级别排序参数控制

### collation_server

* 在 MySQL 5.6 版本中引入 `collation_server` 作为系统变量，用于指定服务器级别的默认字符集排序规则（collation）。
  * 它定义了**在创建新表时使用的默认字符集排序规则**。

查看当前 MySQL 服务器的 `collation_server` 的值：
```sql
SHOW VARIABLES LIKE 'collation_server';
```

该命令将返回一个结果集，其中包含名为 `collation_server` 的变量及其对应的值。

**注意**：

* `collation_server` 是服务器级别的变量，它的值在 MySQL 服务器启动时设置。
  * 通常在配置文件（如 my.cnf 或 my.ini）中进行配置，重新启动 MySQL 服务器生效。

---

### 默认参数规则

* 如果服务启动时未指定参数 `collation_database` 的值，则默认继承参数 `collation_server` 的值。
  * 如果创建数据库时未指定排序规则，则默认使用参数 `collation_database` 的值。

**注意**：

* 参数 `character_set_database` 和 `collation_database` 在 MySQL 5.7 版本中被废弃并将在后续版本中移除。
  * MySQL 新增参数 `default_collation_for_utf8mb4` 用于控制使用 `utf8mb4` 字符集时的默认排序规则，取值为 `utf8mb4_0900_ai_ci`、`utf8mb4_general_ci` 或 `utf8mb4_unicode_ci`。
  * 参数 `default_collation_for_utf8mb4` 在下列条件中生效：
```text
* 使用 SHOW COLLATION 和 SHOW CHARACTER SET 命令时。
* 在创建库或修改库指定 utf8mb4 但未指定排序规则时。
* 在创建表或修改表指定 utf8mb4 但未指定排序规则时。
* 在增加列或修改列指定 utf8mb4 但未指定排序规则时。
* 其他使用 utf8mb4 但未指定排序规则时。
```