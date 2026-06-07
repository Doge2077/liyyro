---
title: "MySQL字符集及其排序规则"
date: 2023-07-03
categories: [DataBase System]
description: ""
---

# mysql字符集及其排序规则


## utf8mb4 基本介绍

### 基本特性

- utf8mb4 是 MySQL 中一种字符集编码，它可以存储和处理 Unicode 字符。
- Unicode 字符集中包含了几乎所有的字符，包括各种语言的字符、符号、表情符号等。

### 与 utf8mb3 的区别

#### 版本支持

- utf8mb4 字符集在 MySQL 5.5.3 及之后版本开始支持。
    - 在此之前的 MySQL 版本，只支持 utf8 字符集，即 utf8mb3。

#### 编码方式

- 在 MySQL 中，utf8 字符集实际上只支持最多 3 字节的 UTF-8 编码。这意味着它无法正确存储和处理一些特殊字符，如部分表情符号和辅助字符。
    - 为了解决 utf8 字符集的限制，MySQL 引入了 utf8mb4 字符集。utf8mb4 字符集支持最多 4 字节的 UTF-8 编码，可以表示更广泛的字符范围，包括各种特殊字符和表情符号。

### utf8mb4 排序规则

#### 常见排序规则

- **utf8mb4_general_ci**：
    - 默认的排序规则，**不区分大小写**，支持多语言排序。
    - 在该规则下，'a' 和 'A' 被认为是相等的。

- **utf8mb4_unicode_ci**：
    - 基于 Unicode Collation Algorithm (UCA) 的排序规则，**不区分大小写**。
    - 与 utf8mb4_general_ci 相比，utf8mb4_unicode_ci 更加精确，能够正确地排序各种语言的字符。

- **utf8mb4_bin**：
    - 基于二进制的排序规则，**区分大小写**，且按照字符的二进制值进行排序。
    - 在此规则下，'A' 会排在 'a' 之前。

- **utf8mb4_0900_ai_ci**：
    - 在 MySQL 8.0.0 版本中引入，用于支持 utf8mb4 字符集。
    - 在 MySQL 8.0.0 之前的版本中，utf8mb4 字符集使用 utf8mb4_general_ci 排序规则。该规则对部分特定字符的比较不够准确，可能导致排序和比较结果不符合预期。
    - 基于 Unicode Collation Algorithm (UCA) 9.0.0 的排序规则，**不区分大小写**，能更准确地处理各种字符的排序和比较。

除了上述常见排序规则，MySQL 还提供了其他一些排序规则，如 utf8mb4_unicode_520_ci、utf8mb4_unicode_520_bin 等。可根据具体需求选择使用。

#### 默认排序规则

当设置表的默认字符集为 utf8mb4 但未明确指定排序规则时：

- 在 MySQL 5.7 版本中，默认排序规则为 utf8mb4_general_ci。
- 在 MySQL 8.0 版本中，默认排序规则为 utf8mb4_0900_ai_ci。

#### 兼容性问题

由于 utf8mb4_0900_ai_ci 是 MySQL 8.0 引入的排序规则，因此将 MySQL 8.0 版本的表导入到 MySQL 5.7 或 5.6 版本时，会存在字符集无法识别的问题。

- `[Err] 1273 - Unknown collation: 'utf8mb4_0900_ai_ci'`
- **解决办法**：修改新建数据库的排序规则，或手动修改 SQL 文件内所有的排序规则。

#### utf8mb4_unicode_ci 与 utf8mb4_general_ci 对比

- **准确性**：
    - utf8mb4_unicode_ci 排序规则基于标准 Unicode 进行排序和比较，能处理特殊字符，在各种语言中精确排序。
    - utf8mb4_general_ci 排序规则没有基于标准 Unicode，无法处理部分特殊字符。

- **性能**：
    - utf8mb4_general_ci 排序规则在排序性能上相对较好。
    - utf8mb4_unicode_ci 排序规则为处理特殊字符实现了更复杂的排序算法，性能略差。
    - 在大部分场景下，两者没有明显的性能差异。

### 服务器级别排序参数控制

#### collation_server

- 在 MySQL 5.6 版本中引入了系统变量 `collation_server`，用于指定服务器级别的默认字符集排序规则。
    - 它定义了**创建新表时使用的默认字符集排序规则**。

查看当前 MySQL 服务器的 `collation_server` 的值：
```sql
SHOW VARIABLES LIKE 'collation_server';
```

该命令将返回一个结果集，其中包含名为 `collation_server` 的变量及其对应的值。

**注意**：

- `collation_server` 是服务器级别的变量，其值在 MySQL 服务器启动时设置。
    - 通常在配置文件（如 my.cnf 或 my.ini）中进行配置，修改后需重新启动 MySQL 服务器生效。

#### 参数继承规则

- 如果服务启动时未指定参数 `collation_database` 的值，则默认继承参数 `collation_server` 的值。
    - 如果创建数据库时未指定排序规则，则默认使用参数 `collation_database` 的值。

**注意**：

- 参数 `character_set_database` 和 `collation_database` 在 MySQL 5.7 版本中已被废弃，并将在后续版本中移除。
    - MySQL 新增了参数 `default_collation_for_utf8mb4`，用于控制使用 `utf8mb4` 字符集时的默认排序规则，取值可为 `utf8mb4_0900_ai_ci`、`utf8mb4_general_ci` 或 `utf8mb4_unicode_ci`。
    - 参数 `default_collation_for_utf8mb4` 在下列情况中生效：
        - 使用 `SHOW COLLATION` 和 `SHOW CHARACTER SET` 命令时。
        - 在创建或修改库时指定 `utf8mb4` 但未指定排序规则时。
        - 在创建或修改表时指定 `utf8mb4` 但未指定排序规则时。
        - 在增加或修改列时指定 `utf8mb4` 但未指定排序规则时。
        - 其他使用 `utf8mb4` 但未指定排序规则时。
