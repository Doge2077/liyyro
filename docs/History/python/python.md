---
title: "Python 语法基础"
date: 2023-01-29
categories: [python, Python]
description: ""
---

# 前言

---

自从对着官方文档把 `ipython` 敲了一遍，一天学完了 `Python` 的语法之后，我觉得我行了。于是屁颠屁颠地跑去写项目，结果显而易见，开发之路可谓寸步难行，一停下来就光速遗忘。

这引起了我深刻的反思：**学习这条路上，切勿取巧偷懒，切勿急于求成，切勿自以为是**。简言之就是：

> 形不成形，意不在意，再回去练一练吧。

于是便有了这篇在寒假的尾巴尖上重新学起的 `Python` 语法基础。现在回看自己的学习历程，我竟从未有过像学习 `Python` 如此认真地学习过一门语言，也因此发现了大量速成时遗漏的点。即便如此学习，我也只是处于 `Python` 的入门阶段，留下这篇笔记以作**警醒**，学途不尽，仍需努力。

* 唯一指定参考：[Python官方文档](https://docs.python.org/zh-cn/3.9/tutorial/index.html)

本篇大量参考自官方文档，亦师从好基友 [VJK](https://www.vjking.top/) 并参考其博客 [Python 系列](https://www.vjking.top/index.php/category/other/)。如有谬误之处，欢迎指出。

---

# 1. 数字类型

---

## 1.0 type()函数

---

```python
type(变量)
print(type(变量)) # 打印出变量的数据类型
```

---

## 1.1 int

---

不需要像 `C/C++` 一样先定义，直接声明即可。

```python
a = 2
print(type(a))
```

---

## 1.2 float

---

与 `C/C++` 不同，`Python` 中的 `float` 精度更高，范围在 `-3.4028235 x 10^38 ~ 3.4028235 x 10^38` 之间。

```python
a = 2.333
b = 5.
print(type(a))
print(type(b))
```

---

## 1.3 complex

---

在 `Python` 中可以直接表示复数类型。

```python
a = 1 + 2j
print(type(a))
```

---

# 2. 运算符

---

## 2.1 除法

---

* 除法：`/`
  * 向下取整除法 ：`//`

```python
a = 10
b = 3
c = a / b
d = a // b
print("c: ", c, type(c))
print("d: ", d, type(d))
```

可以得知，`/` 运算返回一个 `float` 类型，而 `//` 返回 `int` 类型。

---

## 2.2 取余

---

* 取余：`%`

```python
a = 10
b = 3
c = a % b
d = b % a
print("c: ", c, type(c))
print("d: ", d, type(d))
```

`%` 运算返回 `int` 类型。

---

## 2.3 乘法

---

* 乘法：`*`
  * 乘方：`**`

```python
a = 10
b = 3.0
c = a * b
d = a ** b
print("c: ", c, type(c))
print("d: ", d, type(d))
```

`*` 或 `**` 运算返回精度更高的类型。

---

## 2.4 比较运算符

---

* 等于：`==`
  * 不等于：`!=`
  * 大于：`>`
  * 大于等于：`>=`
  * 小于：`&lt;`
  * 小于等于：`&lt;=`

```python
a = 1
b = 2
c = 1
print(a == b)
print(a == c)
print(a != b)
print(a &gt; b)
print(a >= c)
print(a &lt; b)
print(b &lt;= c)
```

---

# 3. 字符串

---

## 3.1 基本操作

---

声明即可赋值：
```python
a = 'abcd'
b = "abcd"
c = """abcd"""
print("a: ", a, type(a))
print("b: ", b, type(b))
print("c: ", c, type(c))
print(a, b, c)
```

`\` 用于转义，例如：
```python
# a = 'a\'bc\'d'  # 错误语句
b = "a'bc'd"
c = "a\'bc\'d"
# print("a: ", a, type(a))
print("b: ", b, type(b))
print("c: ", c, type(c))
```

取消全部的转义在前面加上 `r`：
```python
print("a\nbcd")
print(r"a\nbcd")
```

字符串字面值可以包含多行，使用三重引号：`"""..."""` 或 `'''...'''`：
```python
a = """
    'a' is a string
    Python is instring
"""
print(a)
```

使用 `+` 进行拼接，`*` 进行重复：
```python
a = "abcd"
b = "efgh"
c = a + b
d = a * 2 + b * 3
print("c: ", c, type(c))
print("d: ", d, type(d))
```

---

## 3.2 索引和切片

---

### 3.2.1 索引

---

字符串支持索引（下标访问），第一个字符的索引是 0，单个字符没有专用的类型，就是长度为一的字符串：
```python
a = "abcd"
print(a[0])
print(a[2])
```

索引支持负数，用负数索引时，从右边开始计数：
```python
a = "abcd"
print(a[0])
print(a[-0])  # -0 和 0 一样
print(a[1])
print(a[-1])  # 负数索引从 -1 开始
```

`Python` 字符串不能修改，是 [immutable](https://docs.python.org/zh-cn/3.9/glossary.html#term-immutable) 的：
```python
a = "abcd"
# a[0] = "d"  # 报错
```

值得注意的是，由于 `Python` 中的字符串是不可改变的，连接两个字符串会创建一个新的字符串，而不是修改一个现有的字符串：
```python
string = "abc defg hijk"
new_string = ""
for i in string:
    if i != ' ':
        new_string += i

print(new_string)
```

---

### 3.2.2 切片

---

索引可以提取单个字符，切片则提取子字符串：

* 语法：`str[起始位:终止位:步长]`
  * 省略开始索引时，默认值为 0，省略结束索引时，默认为到字符串的结尾。
  * 切片起始包括起始位元素，截至到终止位的前一个元素，即不包含终止位元素。
  * 其中步长可省略，默认为`1`，切片返回一个新的字符串。

```python
a = "abcd"
b = a[0:2]
c = a[2:4]
d = a[:2]
e = a[2:]
f = a[:]
g = a[0:4:2]
h = a[-1::-1]
i = a[0:100]
print(b)
print(c)
print(d)  # 起始索引默认为 0
print(e)  # 结束索引默认为字符串结尾
print(f)
print(g)  # 步长为 2，每 2 个元素取一个
print(h)  # 步长为负数，从右往左切
print(i)  # 切片越界自动处理
```

**注意**：索引越界会报错，切片越界会自动处理。

---

## 3.3 常用内置函数

---
```python
a = "lys is a dog"
print(len(a))  # len() 返回字符串的长度

print(a.title())  # 给每个单词首字母大写
print(a.upper())  # 把所有字母变成大写
a = a.upper()
print(a.lower())  # 把所有字母变成小写

b = "   lys is a dog   "
print(b.lstrip())  # 去除头空格
print(b.rstrip())  # 去除尾空格
print(b.strip())  # 去除头尾空格
```

---

# 4. 列表与元组

---

`Python` 支持多种复合数据类型，可将不同值组合在一起。最常用的列表，是用方括号标注，逗号分隔的一组值。列表可以包含不同类型的元素，但一般情况下，各个元素的类型相同：
```python
a = [1, 2, 3, 4]
b = ['a', 'b', 'c', 'd']
c = ['a', '2', '3.33', "cde"]
d = a + b  # 支持 + 合并
e = c * 2 + d * 3  # 支持 * 合并
print("a: ", a, type(a))
print("b: ", b, type(b))
print("c: ", c, type(c))
print("d: ", d, type(d))
print("e: ", e, type(e))
```

---

## 4.1 列表索引和切片

---

### 4.1.1 索引

---

和数组操作相同：
```python
a = [1, 2, 3, 4]
b = ['a', 'b', 'c', 'd']
c = ['a', '2', '3.33', "cde"]
print(a[0])
print(b[1])
print(c[2])
```

与 [immutable](https://docs.python.org/zh-cn/3.9/glossary.html#term-immutable) 字符串不同，列表是 [mutable](https://docs.python.org/zh-cn/3.9/glossary.html#term-mutable) 类型，其内容可以改变：
```python
a = [1, 2, 3, 4]
b = ['a', 'b', 'c', 'd']
c = ['a', '2', '3.33', "cde"]
a[0], b[1], c[2] = 100, 'x', "abc"
print("a: ", a, type(a))
print("b: ", b, type(b))
print("c: ", c, type(c))
```

---

### 4.1.2 切片

---

切片操作返回包含请求元素的新列表，切片操作会返回列表的[浅拷贝](https://docs.python.org/zh-cn/3.9/library/copy.html#shallow-vs-deep-copy)：
```python
a = [1, 2, 3, 4]
b = a[0:2]
c = a[2:]
print(b)
print(c)
```

---

## 4.2 嵌套列表

---
```python
a = [1, 2, 3, 4]
b = ['a', 'b', 'c', 'd']
c = ['a', '2', '3.33', "cde"]
e = [a, b, c]
print("e: ", e, type(e))
print(e[0][0], e[1][1], e[2][2])
```

---

## 4.3 列表常用内置函数

---
```python
a = [1, 2, 3, 4]
print("len(a): ", len(a))  # len() 返回列表的长度

a.append(5)  # 在 a 末尾添加元素 5
print("a.append(5): ", a)

a.insert(1, 3)  # 在位置 1 处插入元素 3
print("a.insert(1, 3): ", a)

a.remove(3)  # 删除第一个值为 3 的元素
print("a.remove(3): ", a)
# a.remove(0)  删除的元素不存在则会触发 ValueError 异常

a.pop(0)  # pop(i) 删除指定位置 i 的元素
print("a.pop(0):", a)
a.pop()  # 未传入参数时默认删除末尾元素
print(a)

a = [1, 2, 3, 4, 5]
del a[1:3]  # 删除列表的切片
print("del a[1:3]:", a)

a = [6, 5, 4, 3, 2, 1, 1]
print("a.count(1): ", a.count(1))  # count(x) 返回值为 x 的元素出现的次数

a.sort()  # 默认从小到大排序
print("a.sort(): ", a)
a.sort(reverse=True)  # 传入参数从大到小排序
print("a.sort(reverse=True): ", a)
```

b = sorted(a)  # 默认从小到大排序  
print("b: ", b)  
b = sorted(a, reverse=True)  # 传入参数从大到小排序  
print("b: ", b)  

a.reverse()  # 翻转列表中的元素  
print("a.reverse()", a)  

a.clear()  # 清空  
print(len(a))  

---

## 4.4 元组  

元组由多个用逗号隔开的值组成：  

```python
a = 1, 2, 3, 4
print("a: ", a, type(a))
b = ('a', 'b', 'c', 'd', a)  # 由 () 表示一个元组，可嵌套使用
print("b: ", b, type(b))
```

输出时，元组都要由圆括号标注，这样才能正确地解释嵌套元组。输入时，圆括号可有可无，不过经常是必须的（如果元组是更大的表达式的一部分）。不允许为元组中的单个元素赋值，当然，可以创建含列表等可变对象的元组。  

元组同样支持索引和切片：  

```python
a = 1, 2, 'a', 'b'
print(a[0])
print(a[1:3])
# a[0] = 0  不可修改
```

虽然，元组与列表很像，但使用场景不同，用途也不同。元组是 [immutable](https://docs.python.org/zh-cn/3.9/glossary.html#term-immutable) （不可变的），一般可包含异质元素序列，通过解包索引访问（如果是 [`namedtuples`](https://docs.python.org/zh-cn/3.9/library/collections.html#collections.namedtuple)，可以属性访问）。列表是 [mutable](https://docs.python.org/zh-cn/3.9/glossary.html#term-mutable) （可变的），列表元素一般为同质类型，可迭代访问。  

---

## 4.5 浅拷贝与深拷贝  

`copy` 和 `deepcopy` 是 `Python` 中用于复制对象的两个函数。  

* `copy` 是浅拷贝，只复制对象的引用，如果对象内部包含子对象，修改子对象的值会影响原对象。  
  * `deepcopy` 是深拷贝，会递归复制对象的内部结构，从而生成一个完全独立的对象，不会与原对象产生任何关系。  

```python
import copy

a = [1, 2, 3]
b = [4, 5, 6]
c = [a, b]  # c 中包含 a, b 两个子对象
d = c
print("a: ", id(a))
print("b: ", id(b))
print("c: ", id(c))
print("d: ", id(d))  # id(d) == id(c) 说明 d 和 c 是相同的对象

print(d)
```

d = copy.copy(c)
print("c: ", id(c))
print("copy(d): ", id(d))  # copy(d) 生成了一个新的对象
print("a: ", id(a))
print("c[0]: ", id(c[0]))
print("copy(d[0]): ", id(d[0]))  # d[0] 和 c[0] 是相同的对象，说明新生成的对象没有改变原来 c 中的子对象

print()

d = copy.deepcopy(c)
print("c: ", id(c))
print("copy(d): ", id(d))  # copy(d) 生成了一个新的对象
print("a: ", id(a))
print("c[0]: ", id(c[0]))
print("copy(d[0]): ", id(d[0]))  # d[0] 和 c[0] 不是相同的对象，说明新生成的 d 是一个完全独立的对象

**总结**：`deepcopy` 会生成一个独立的对象，而 `copy` 只是对对象的引用。

参考链接：[What is the difference between shallow copy, deepcopy and normal assignment operation?](https://stackoverflow.com/questions/17246693/what-is-the-difference-between-shallow-copy-deepcopy-and-normal-assignment-oper)

---

# 5. 集合与字典

---

## 5.1 集合

---

集合是由**不重复元素组成的无序容器**，基本用法包括成员检测、消除重复元素。集合对象支持合集、交集、差集、对称差分等数学运算。

```python
a = {1, 2, 3, 4, 5}
print("a: ", a, type(a))
```

集合运算：

```python
a = {1, 2, 3, 4, 5}
b = {2, 4, 5}
print("1 in a is", 1 in a)
print("1 in b is", 1 in b)
print("a = b is", a == b)
print("a - b =", a - b)
print("b - a =", b - a)
print("a | b =", a | b)
print("a & b =", a & b)
print("a ^ b =", a ^ b)
```

---

## 5.2 字典

---

字典为键值对的集合，字典的键必须是唯一的：

```python
a = {1:'a', 2:'b', 3:'c', 4:'d'}
print("a: ", a, type(a))
print("a[1]: ", a[1])

b = {'a':1, "bcd":2, 3.4:"e"}
print("b: ", b, type(b))
print("b['a']: ", b['a'])
```

与以连续整数为索引的序列不同，字典以关键字为索引，关键字通常是字符串或数字，也可以是其他任意不可变类型。只包含字符串、数字、元组的元组，也可以用作关键字。但如果元组直接或间接地包含了可变对象，就不能用作关键字。列表不能当关键字，因为列表可以用索引、切片、`append()` 、`extend()` 等方法修改。
```python
a = {'name': 'wjq', 'sex': 'male', 'qq': 1145141919}
print(a.get('name'))  # 通过键获取值，且不会报错
a.pop('qq')  # 删除键为 qq 的键值对
print(a.keys())  # 获取所有的键
print(a.values())  # 获取所有的值
a['name'] = 'lys'  # 改值
print("a: ", a, type(a))
```

合并两个键值不冲突的字典可以使用如下方法：
```python
a = {1:'a', 2:'b'}
b = {3:'c', 4:'d'}

c = a
c.update(b)  # 内置函数 update

d = {**a, **b}  # 解包合并

print("c: ", c)
print("d: ", d)
```

---

# 6. if 语句

---

条件表达式为真时执行语句：
```python
a = int(input("input 'a' number: "))
if a == 0:
    print("'a' is zero", end='')
elif a &gt; 0:
    print("'a' is a positive number", end='')
else:
    print("'a' is a negative number")
```

支持嵌套：
```python
a = int(input("input 'a' number: "))
if a == 0:
    print("'a' is zero", end='')
elif a > 0:
    if a > 100:
        print("'a' is a positive number and 'a' is bigger than 100", end='')
    elif a == 100:
        print("'a' is equal to 100", end='')
    else:
        print("'a' is a positive number and 'a' is smaller than 100", end='')
else:
    print("'a' is a negative number")
```

**注意：** 条件表达式的本质是得到一个 `bool` 值，以下非条件表达式的值也会被视为 `False`：

* `False`
  * `0`
  * `None`
  * `""`，`[]`，`()`，`{}`

---

# 7. while 语句

---

[`while`](https://docs.python.org/zh-cn/3.9/reference/compound_stmts.html?highlight=while#while) 语句用于在表达式保持为真的情况下重复地执行：
```python
flag = 10
a = 0
while a &lt; flag:
    print(a, end=' ')
    a += 1
print("\na:", a)
```

其余扩展用法同 `for` 语句相同，详见下面内容。

---

# 8. for 语句

---

## 8.1 基本使用

---

`Python` 的 `for` 语句不迭代算术递增数值，也不给予用户定义迭代步骤和暂停条件的能力，而是迭代列表或字符串等任意序列，元素的迭代顺序与在序列中出现的顺序一致。
```python
a = [1, 2, 3, 4, 5]
for i in a:
    print(i, end=' ')
print()
b = [1, 2.333, 'a', "bcd"]
for i in b:
    print(i, type(i))
```

**注意**：在 `Python` 中，在使用 `for` 循环遍历列表元素时，不能直接在循环体中删除列表元素，这样会导致迭代错误。
```python
a = [1, 2, 3, 4, 5, 6, 7, 8]
for i in range(len(a)):
    if a[i] % 2 == 0:
        del a[i]
print(a)
# IndexError: list index out of range
```

要在遍历时修改集合的内容，应该**遍历该集合的副本或创建新的集合**：
```python
a = [1, 2, 3, 4, 5, 6, 7, 8]
b = []
for i in range(len(a)):
    if a[i] % 2 != 0:
        b.append(a[i])
print(b)
```

---

## 8.2 range() 函数

---

[`range`](https://docs.python.org/zh-cn/3.9/library/stdtypes.html#range) 类型表示不可变的数字序列，通常用于在 [`for`](https://docs.python.org/zh-cn/3.9/reference/compound_stmts.html#for) 循环中循环指定的次数。
```python
for i in range(10):
    print(i, end=' ')

a = list(range(10))  # 生成一个列表 [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
print(a)
```

生成的序列不包含给定的终止数值；`range(10)` 生成 `10` 个值，这是一个长度为 `10` 的序列，其中的元素索引都是合法的。

* `range(起始值,终止值,步进)`
  * 起始值省略，默认为 `0`。
  * 步进值省略时默认为 `1`，可以为负数。

```python
for i in range(1, 10):
    print(i, end=' ')
print()
for i in range(0, 10, 2):
    print(i, end=' ')
print()
for i in range(0, -10, -1):
    print(i, end=' ')
```

[`range()`](https://docs.python.org/zh-cn/3.9/library/stdtypes.html#range) 和 [`len()`](https://docs.python.org/zh-cn/3.9/library/functions.html#len) 组合在一起，可以按索引迭代序列，等价于 [`enumerate()`](https://docs.python.org/zh-cn/3.9/library/functions.html#enumerate) 函数：

```python
a = [1, 2, 3, 4, 5]
for i in range(len(a)):
    print(f"index: {i}, value: {a[i]}")
print()
for i, v in enumerate(a):
    print(f"index: {i}, value: {v}")
```

只输出 `range()`：

```python
print(range(1, 10))
# range(1, 10)  输出内容
```

[`range()`](https://docs.python.org/zh-cn/3.9/library/stdtypes.html#range) 返回的对象操作方式和列表很像，但其实两者并非同一类对象。迭代时，该对象基于所需的序列返回连续项，并不会真正生成列表，从而节省内存。

这类对象称为[可迭代对象（iterable）](https://docs.python.org/zh-cn/3.9/glossary.html#term-iterable)，函数或程序结构可通过它获取连续项，直到所有元素迭代完毕。[`for`](https://docs.python.org/zh-cn/3.9/reference/compound_stmts.html#for) 语句就是这样的结构，[`sum()`](https://docs.python.org/zh-cn/3.9/library/functions.html#sum) 是一种接收可迭代对象作为参数的函数：

```python
print(sum(range(1, 5)))  # sum 计算了 1 + 2 + 3 + 4 的值
# 10  输出内容
```

---

## 8.3 循环嵌套语句

---

### 8.3.1 嵌套 if 语句

---

```python
a = [1, 2, 3, 4, 5, 6, 7, 8]
for i in a:
    if i % 2 == 0:
        print(i, end=' ')
    else:
        print(-1, end=' ')
```

---

### 8.3.2 嵌套循环语句

---

```python
a = [0, 1, 2, 3, 4, 5]
b = [[], []]
for i in range(len(b)):
    for j in a:
        b[i].append(j)
print(b)
```

---

### 8.3.3 break、continue、pass 语句

---

a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
for i in a:
    if i % 2 == 0:
        continue
        # pass  不执行任何内容，此处效果和continue 相同
    elif i % 3 == 0:
        print(i, end=' ')
print()
for i in a:
    if i % 5 != 0:
        print(i, end=' ')
    else:
        break  # 提前跳出本层循环

---

## 8.4 循环的技巧

---

在字典中循环时，用 `items()` 方法可同时取出键和对应的值：
```python
a = {1:'a', 2:'b', 3:'c', 4:'d'}
for k, v in a.items():
    print(f"key:{k}, value:{v}")
```

若只需要字典中的值，可以用 `values()` 方法：
```python
a = {1:'a', 2:'b', 3:'c', 4:'d'}
for v in a.values():
    print(f"value:{v}")
```

在序列中循环时，用 `enumerate()` 函数可以同时取出位置索引和对应的值：
```python
a = [1, 2, 3, 4, 5]
for i, v in enumerate(a):
    print(f"index:{i}, value:{v}")
```

同时循环两个或多个序列时，用 `zip()` 函数可以将其内的元素一一匹配：
```python
questions = ['name', 'quest', 'favorite color']
answers = ['lys', 'the holy grail', 'blue']
for q, a in zip(questions, answers):
    # print(f"What is your {q}? It is {a}.")
    print("What is your {0}? It is {1}.".format(q, a))
```

逆向循环序列时，调用 `reversed()` 函数：
```python
a = [1, 2, 3, 4, 5]
for i in reversed(a):
    print(i, end=' ')
```

按指定顺序循环序列，可以用 `sorted()` 函数，在不改动原序列的基础上，返回一个重新排序的序列：
```python
a = [2, 5, 1, 4, 3]
for i in sorted(a):
    print(i, end=' ')
print()
for i in sorted(a, reverse=True):
    print(i, end=' ')
print()
for i in a:
    print(i, end=' ')
```

使用 [`set()`](https://docs.python.org/zh-cn/3.9/library/stdtypes.html#set) 去除序列中的重复元素。使用 [`sorted()`](https://docs.python.org/zh-cn/3.9/library/functions.html#sorted) 加 [`set()`](https://docs.python.org/zh-cn/3.9/library/stdtypes.html#set) 则按排序后的顺序，循环遍历序列中的唯一元素：
```python
a = [1, 3, 1, 2, 3, 4, 5, 4, 3, 2, 1, 5, 4]
for i in sorted(set(a)):
    print(i, end=' ')
```

`for` 支持推导式表达：
```python
a = list(range(1, 10))
print("a: ", a)
b = [i*i for i in a]  # b 为 a 中元素的平方
print("b: ", b)
c = {k:v for k,v in zip(a, b)}
print("c: ", c)
```

---

# 9. 格式化输出

---

## 9.1 格式化字符串字面值

---

[格式化字符串字面值](https://docs.python.org/zh-cn/3.9/reference/lexical_analysis.html#f-strings) （简称为 f-字符串）在字符串前加前缀 `f` 或 `F`，通过 `{expression}` 表达式，把 `Python` 表达式的值添加到字符串内：
```python
a = 100
b = 'lys'
print(f"{b} is {a} years old")
```

格式说明符是可选的，写在表达式后面，可以更好地控制格式化值的方式。下例将 `pi` 舍入到小数点后三位：
```python
import math
print(f'The value of pi is approximately {math.pi:.3f}.')
```

在 `':'` 后传递整数，为该字段设置最小字符宽度，常用于列对齐：
```python
table = {1:'a', 2:'bc', 3:'def', 4:'ghij'}
for k, v in table.items():
    print(f'key is {k:5} ==&gt; value is {v:5} in this table')
```

---

## 9.2 字符串 format() 方法

---

[`str.format()`](https://docs.python.org/zh-cn/3.9/library/stdtypes.html#str.format) 方法的基本用法如下所示：
```python
print("{} is a {}.".format('lys', 'dog'))
```

花括号及之内的字符（称为格式字段）被替换为传递给 [`str.format()`](https://docs.python.org/zh-cn/3.9/library/stdtypes.html#str.format) 方法的对象。花括号中的数字表示传递给 [`str.format()`](https://docs.python.org/zh-cn/3.9/library/stdtypes.html#str.format) 方法的对象所在的位置：
```python
print("{0} is a {2} and {1} is a {2}, too.".format('lys', 'wjq', 'dog'))
```

[`str.format()`](https://docs.python.org/zh-cn/3.9/library/stdtypes.html#str.format) 方法中使用关键字参数名引用值：
```python
print("{name1} is a {name3} and {name2} is a {name3}, too.".format(name1='lys', name2='wjq', name3='dog'))
```

上述方法也可以交叉使用：
```python
print("{name1} is a {0} and {name2} is a {0}, too.".format('dog', name1='lys', name2='wjq'))
```

---

# 10. 异常处理

---

## 10.1 异常处理语句

---

利用 `try`，`except`，`finally`，`else` 语句处理异常：
```python
a = 100
b = 0
d = [1, 2, 3, 4]
try:
    c = a / b
    e = d[10]  # 前两条语句异常，只会处理第一条语句异常，直接跳出 try，进入 except 匹配异常
    f = a + b  # 若前两条语句无异常，执行 else 中的语句
except ValueError:  # 异常匹配
    print("ValueError")
except ZeroDivisionError:
    print("ZeroDivisionError")
except IndexError:
    print("IndexError")
else:
    print("No Error Exist")  # try 无异常则执行
finally:  # 无论是否有其他异常都会执行
    print("Over")
```

主要修复内容：
1. 将所有代码块标记从 ` ```java ` 修正为 ` ```python `
2. 移除链接中的多余尖括号，修正为标准 Markdown 链接格式
3. 修正章节编号中的反斜杠转义符，改为标准 Markdown 格式
4. 移除代码中不必要的分号符号

* 首先，执行 `try` 子句（[`try`](https://docs.python.org/zh-cn/3.9/reference/compound_stmts.html#try) 和 [`except`](https://docs.python.org/zh-cn/3.9/reference/compound_stmts.html#except) 关键字之间的（多行）语句）。
  * 如果没有触发异常，则跳过 `except` 子句，[`try`](https://docs.python.org/zh-cn/3.9/reference/compound_stmts.html#try) 语句执行完毕。
  * 如果执行 `try` 子句时发生了异常，则跳过该子句中剩下的部分。如果异常的类型与 [`except`](https://docs.python.org/zh-cn/3.9/reference/compound_stmts.html#except) 关键字后面的异常匹配，则执行 `except` 子句。
  * 如果发生的异常不是 `except` 子句中列示的异常，则将其传递到外部的 [`try`](https://docs.python.org/zh-cn/3.9/reference/compound_stmts.html#try) 语句中；如果没有找到处理程序，则它是一个未处理异常，语句执行将终止。
  * 如果 `try` 子句没有触发异常，但又必须执行一些代码时，可使用 `else` 子句。**注意**，该子句只能放在所有的 `except` 子句之后。
  * 最后无论是否出现异常，都会执行 `finally` 子句。

其中，`except` 可以用元组指定多个异常类型：
```python
a = 100
b = 0
d = [1, 2, 3, 4]
Errors = (ValueError, RuntimeError, FloatingPointError, IndexError, TypeError, ZeroDivisionError)
try:
    c = a / b
    e = d[10]  # 前两条语句异常，只会处理第一条语句异常，直接跳出 try，进入 except 匹配异常
    f = a + b  # 若前两条语句无异常，执行 else 中的语句
except Errors:
    print("Errors")
else:
    print("No Error Exist")  # try 无异常则执行
finally:  # 无论是否有其他异常都会执行
    print("Over")
    # print(f)
```

---

## 10.2 抛出异常

---

[`raise`](https://docs.python.org/zh-cn/3.9/reference/simple_stmts.html#raise) 语句支持强制触发指定的异常：
```python
raise ValueError("参数错误")
```

a = 100
b = 0
try:
    c = b / a
    raise ZeroDivisionError('Zero can be divided')
except ZeroDivisionError:
    print("ZeroDivisionError")
    raise
finally:
    print("Over")
```

---

# 11. 函数

---

## 11.1 定义函数

---

使用关键字 [`def`](https://docs.python.org/zh-cn/3.9/reference/compound_stmts.html#def) 定义函数，后跟函数名与括号内的形参列表：
```python
def solve(n):
    """Print 1 to n"""
    for i in range(1, n + 1):
        print(i, end=' ')

a = int(input())
solve(a)
```

函数内的第一条语句是字符串时，该字符串就是文档字符串，也称为 _docstring_ ，详见[文档字符串](https://docs.python.org/zh-cn/3.9/tutorial/controlflow.html#tut-docstrings)。利用文档字符串可以自动生成在线文档或打印版文档。
```python
print(solve.__doc__)  # 打印出 solve 的说明
```

---

## 11.2 默认值参数和关键字参数

---

函数定义时，参数列表的值可以设置初始值作为默认值参数：
```python
def solve(age=24, name="lys", status="dog"):
    print(f"{name} is", end=' ')
    print(f"{age} years old, and {name}", end=' ')
    print(f"is a {status} .")

solve()  # 函数参数都存在默认值调用
```

若存在未初始化的参数，则可以 `kwarg=value` 形式的 [关键字参数](https://docs.python.org/zh-cn/3.9/glossary.html#term-keyword-argument) 调用函数：
```python
def solve(age, name="lys", status="dog"):
    print(f"{name} is", end=' ')
    print(f"{age} years old, and {name}", end=' ')
    print(f"is a {status} .")

solve(114514)  # 第一个参数是必选参数，剩余参数可不选
solve(114514, "LYS")  # 不声明关键字会默认匹配除默认参数后的最近的关键字参数
solve(114514, name="LYS")
solve(14, status="debu cat", name="Hiiro")  # 传入关键字参数与参数列表的关键字对应
```

除上述调用方法外，以下调用非法：
```python
solve()  # 默认 age 参数
solve(name="Hiiro")  # 默认 age 参数
solve(age=114514, "debu cat")  # "debu cat" 需要提供关键字
solve(114514, age=1919)  # age 存在多个不同的值
```

**总结**：

* 函数调用时，关键字参数必须位于位置参数后面。
  * 所有传递的关键字参数都必须匹配一个函数接受的有效参数。
  * 关键字参数的顺序并不重要，但不能对同一个参数多次赋值。

---

## 11.3 解包实参列表

---

需要将序列作为参数时，用 `*` 操作符把实参从列表或元组解包出来：
```python
name1 = [114514, 'Lys', 'dog']
name2 = (14, 'Hiiro', 'debu cat')

def solve(age, name, status):
    print(f"{name} is", end=' ')
    print(f"{age} years old, and {name}", end=' ')
    print(f"is a {status} .")

solve(*name1)
solve(*name2)
```

同样，字典可以用 `**` 操作符传递关键字参数：
```python
name1 = {'age': 114514, 'name': 'Lys', 'status': 'dog'}

def solve(age=24, name='Van', status='XainBei'):
    print(f"{name} is", end=' ')
    print(f"{age} years old, and {name}", end=' ')
    print(f"is a {status} .")

solve(**name1)
# solve(*name1)  # 输出: name is age years old, and name is a status .
```

---

## 11.4 函数的返回值

---

[`return`](https://docs.python.org/zh-cn/3.9/reference/simple_stmts.html#return) 语句返回函数的值。`return` 语句不带表达式参数时，返回 `None`。函数执行完毕退出也返回 `None`：
```python
# 返回值
def solve(n):
    """Show 1 * 2 * ... * n"""
    if n > 1:
        return solve(n - 1) * n
    else:
        return 1

a = int(input())
print(solve(a))

# 返回一个 list
def solve(n):
    """Create a list which is the first n terms of the Fibonacci series"""
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i - 1] + fib[i - 2])
    return fib

a = int(input())
print(solve(a))
```

# 返回多个值
def solve(a, b):
    return a + b, a - b

n , m = solve(1, 2)  # 用对应数量的变量接收
print(f"n = {n}, m = {m}")

t = solve(1, 2)  # 用一个值接收，则会返回一个元组
print(f"t: {t}", type(t))

---

## 11.5 变量作用域

---

函数内部只作引用的 `Python` 变量隐式视为全局变量。如果在函数内部任何位置为变量赋值，则除非明确声明为全局变量，否则均将其视为局部变量：
```python
a = 1

def use():
    print(f"use: {a}")

def change():
    a = 114514

use()
change()  # 调用函数

print(a)  # a 的值不发生改变
```

可以看到，`use()` 函数在只做引用的情况下将 `a` 视为了全局变量，而在 `change()` 函数中对 `a` 做修改，则将 `a` 视为了局部变量，并没有改变其值。

使用关键词 [`global`](https://docs.python.org/zh-cn/3.9/reference/simple_stmts.html#global) 声明变量，将被视为全局变量，在函数对象中更改不再视为局部变量：
```python
a = 1

def use():
    print(f"use: {a}")

def change():
    global a
    a = 114514

use()
change()  # 调用函数

print(a)  # a 的值发生改变（原注释错误）
```

---

## 11.6 Lambda表达式

---

[`lambda`](https://docs.python.org/zh-cn/3.9/reference/expressions.html#lambda) 表达式（有时称为 lambda 构型）被用于创建匿名函数。 表达式 `lambda parameters: expression` 会产生一个函数对象 ：
```python
f = lambda a, b: a + b
print(f(1, 2))

def solve(n):
    return lambda t: t + n

a = 114
f = solve(a)
print(f(1000))

print(solve(114)(1000))  # 或直接调用
```

---

## 11.7 函数闭包

---

函数闭包是一种特殊的函数，它不仅包含函数代码，还引用了它外部作用域中的一些变量。这种引用关系使得闭包可以在外部作用域中的变量保持其生存周期，即使闭包被销毁。

闭包可以用于缓存函数的结果，避免重复计算；也可以用于实现装饰器等高阶函数。
```python
def outer_function(x):
    def inner_function(y):
        return x + y
    return inner_function

closure = outer_function(10)
print(closure(5))  # Output: 15
```

---

## 11.8 装饰器

---

装饰器其实也是一种闭包，作为一种[语法糖](https://en.wikipedia.org/wiki/Syntactic_sugar)在 `Python` 中广泛使用，当对某个冗长的函数加上其他功能，利用装饰器可以在不修改原本函数内容的同时增添新的功能：

现在有 `solve()` 函数如下：
```python
def solve():
    print("Function solve is called.")
```

若要求再输出一行 `"Calling finished."`

简单方法如下：
```python
def solve():
    print("Function solve is called.")
    print("Calling finished.")
```

闭包思路如下：
```python
def solve():
    print("Function solve is called.")

def addition(func):
    def inner():
        func()
        print("Calling finished.")
    return inner

Func = addition(solve)
Func()
```

语法糖思路如下：
```python
def addition(func):
    def inner():
        func()
        print("Calling finished.")
    return inner

@addition
def solve():
    print("Function solve is called.")

solve()
```

由此可以看出，利用语法糖可以在不改变原函数内容和调用的情况下增添功能。

---

## 11.9 生成器

`yield`是用于实现迭代器。它可以在函数中生成多个值，每次运行到 `yield` 语句时都会暂停函数的执行并返回一个值。下次调用函数时，会从上次暂停的地方继续执行：
```python
def solve():
    for i in range(1, 10):
        yield i

func = solve()  # 得到生成器对象
print(func)  # 得到生成器时，是不会执行函数内部代码的

# 使用next()方法进入生成器，执行代码，同时可以用变量得到 yield 的返回值
num = next(func)
print(num)

num = next(func)
print(num)

# next 方法在执行完后会抛出 StopIteration 异常表示生成器已经结束，需要捕获该异常
# 若没有执行完用 del 释放资源
del func

# 重新得到生成器对象并用 for 迭代所有数据，此方法不会抛出异常
func = solve()
for i in func:
    print(i, end=' ')
```

生成器是一种特殊的迭代器，可以动态生成值。它可以使代码简洁，并且对大数据集的处理效率更高。

实际上，在生成器函数中，我们可以使用 `变量1 = yield 变量2` 的方式将生成器**封存**，直到下次对生成器对象使用 `send(value)` 方法将 `value` 的值赋给 `变量1` 之后，才可以继续往下执行代码。
```python
def solve():
    for i in range(10):
        v = yield i
        print(v)

func = solve()  # 得到生成器对象

func.send(None)  # 传入第一个值必须为 None

num = func.send("Counting: ")
print(num)

num = func.send("Counting: ")
print(num)

del func

func = solve()
func.send(None)

for i in range(9):
    num = func.send("Counting: ")
    print(num)
```

---

# 12. 模块

---

模块是包含 `Python` 定义和语句的文件。其文件名是模块名加后缀名 `.py`。在模块内部，通过全局变量 `__name__` 可以获取模块名（即字符串）。

模块包含可执行语句及函数定义。这些语句用于初始化模块，且仅在 `import` 语句第一次遇到模块名时执行。

首先创建一个名为 `solve.py` 的文件：
```python
def Sum(n):
    """Calculate the sum of list and return the result"""
    t = 0
    for i in range(len(n)):
        t += n[i]
    return t

def Fib(n):
    """Create a list which is the first n terms of the Fibonacci series"""
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i - 1] + fib[i - 2])
    return fib
```

在该文件中，我们定义了 `Sum` 和 `Fib` 函数，接下来在另一个 `.py` 文件里导入并使用：
```python
from solve import Sum
from solve import Fib
a = [1, 2, 3, 4]
print(Fib(Sum(a)))
```

也可以一次性导入该模块中所有的函数定义：
```python
from solve import *
a = [1, 2, 3, 4]
print(Fib(Sum(a)))
```

---

# 13. 类

---

**类把数据与功能绑定在一起**。

创建新类就是创建新的对象类型，从而创建该类型的新实例。类实例具有多种保持自身状态的属性。类实例还支持（由类定义的）修改自身状态的方法。

`Python` 的类是 `C++` 和 `Modula-3` 中类机制的结合体，而且支持所有面向对象编程（OOP）的标准特性：

* 类继承机制支持多个基类。
  * 派生类可以覆盖基类的任何方法。
  * 类的方法可以调用基类中相同名称的方法。
  * 对象可以包含任意数量和类型的数据。

和模块一样，类也拥有 `Python` 天然的动态特性：

*   在运行时创建，创建后也可以修改。

如果用 `C++` 术语来描述的话，类成员（包括数据成员）通常是 `public` 的（例外的情况见[私有变量](https://docs.python.org/zh-cn/3.9/tutorial/classes.html#tut-private)），所有成员函数都是 `virtual` 的。与 `C++` 不同，`Python` 的内置类型可以用作基类，供用户扩展。此外，与 `C++` 一样，算术运算符、下标等具有特殊语法的内置运算符都可以为类实例重新定义。

---

## 13.1 作用域和命名空间

---

### 13.1.1 命名空间

---

`namespace`（命名空间）是一个从名字到对象的映射。当前大部分命名空间都由 `Python` 字典实现，但一般情况下基本不会去关注它们（除了要面对性能问题时），而且也有可能在将来更改。

下面是几个命名空间的例子：

*   包含内置函数（如 [`abs()`](https://docs.python.org/zh-cn/3.9/library/functions.html#abs) ）和内置异常等的集合；

*   模块中的全局名称；

*   函数调用中的局部名称。

从某种意义上说，对象的属性集合也是一种命名空间的形式。关于命名空间的重要一点是，不同命名空间中的名称之间绝对没有关系；例如，两个不同的模块都可以定义一个 `maximize` 函数而不会产生混淆——模块的用户必须在其前面加上模块名称。

命名空间在不同时刻被创建，拥有不同的生存期。包含内置名称的命名空间是在 `Python` 解释器启动时创建的，永远不会被删除。模块的全局命名空间在模块定义被读入时创建；通常，模块命名空间也会持续到解释器退出。被解释器的顶层调用执行的语句，从一个脚本文件读取或交互式地读取，被认为是 [`__main__`](https://docs.python.org/zh-cn/3.9/library/__main__.html#module-__main__) 模块调用的一部分，因此它们拥有自己的全局命名空间。（内置名称实际上也存在于一个模块中；这个模块被称作 [`builtins`](https://docs.python.org/zh-cn/3.9/library/builtins.html#module-builtins) 。）

函数的本地命名空间在调用该函数时创建，并在函数返回或抛出不在函数内部处理的错误时被删除。当然，每次递归调用都会有自己的本地命名空间。

---

### 13.1.2 作用域

---

一个作用域是一个命名空间可直接访问的 `Python` 程序的文本区域。这里的“可直接访问”意味着对名称的非限定引用会尝试在命名空间中查找名称。

虽然作用域是静态地确定的，但它们会被动态地使用。在执行期间的任何时刻，会有 `3` 或 `4` 个命名空间可被直接访问的嵌套作用域：

*   最先搜索的最内部作用域包含局部名称。

*   从最近的封闭作用域开始搜索的任何封闭函数的作用域包含非局部名称，也包括非全局名称。

*   倒数第二个作用域包含当前模块的全局名称。

*   最外面的作用域（最后搜索）是包含内置名称的命名空间。

如果一个名称被声明为全局变量，则所有引用和赋值将直接指向包含该模块的全局名称的中间作用域。要重新绑定在最内层作用域以外找到的变量，可以使用 [`nonlocal`](https://docs.python.org/zh-cn/3.9/reference/simple_stmts.html#nonlocal) 语句声明为非本地变量。如果没有被声明为非本地变量，这些变量将是只读的（尝试写入这样的变量只会在最内层作用域中创建一个新的局部变量，而同名的外部变量保持不变）。

通常，当前局部作用域将引用当前函数的局部名称。在函数以外，局部作用域将引用与全局作用域相一致的命名空间：模块的命名空间。类定义将在局部命名空间内再放置另一个命名空间。

在一个模块内定义的函数的全局作用域就是该模块的命名空间，无论该函数从什么地方或以什么别名被调用。另一方面，实际的名称搜索是在运行时动态完成的。

`Python` 的一个特殊规定是这样的：

*   如果不存在生效的 [`global`](https://docs.python.org/zh-cn/3.9/reference/simple_stmts.html#global) 或 [`nonlocal`](https://docs.python.org/zh-cn/3.9/reference/simple_stmts.html#nonlocal) 语句；
*   则对名称的赋值总是会进入最内层作用域。

赋值不会复制数据，它们只是将名称绑定到对象。删除也是如此：语句 `del x` 会从局部作用域所引用的命名空间中移除对 `x` 的绑定。事实上，所有引入新名称的操作都是使用局部作用域：特别地，[`import`](https://docs.python.org/zh-cn/3.9/reference/simple_stmts.html#import) 语句和函数定义会在局部作用域中绑定模块或函数名称。

[`global`](https://docs.python.org/zh-cn/3.9/reference/simple_stmts.html#global) 语句可被用来表明特定变量生存于全局作用域并且应当在其中被重新绑定；[`nonlocal`](https://docs.python.org/zh-cn/3.9/reference/simple_stmts.html#nonlocal) 语句表明特定变量生存于外层作用域中并且应当在其中被重新绑定。

---

### 13.1.3 示例

---

> 对象之间相互独立，多个名称（在多个作用域内）可以绑定到同一个对象。

下面示例引用不同作用域和名称空间，以及 [`global`](https://docs.python.org/zh-cn/3.9/reference/simple_stmts.html#global) 和 [`nonlocal`](https://docs.python.org/zh-cn/3.9/reference/simple_stmts.html#nonlocal) 会如何影响变量绑定：

```python
def solve():
    def do_local():
        spam = "local spam"  # 此处创建 solve() 中 spam 的局部副本，不影响外部变量
        print("Inside do_local, spam:", spam)

    def do_nonlocal():
        nonlocal spam
        spam = "nonlocal spam"

    def do_global():
        global spam
        spam = "global spam"

    spam = "test spam"  # 此处 spam 为 solve() 命名空间下的一个局部变量
    do_local()
    print("After local assignment:", spam)  # 调用 do_local() 修改 spam 会隐式地视为 do_local() 的局部变量
    do_nonlocal()
    print("After nonlocal assignment:", spam)  # 此处 spam 被 nonlocal 修饰，会绑定之前在最近的包含作用域中绑定的除全局变量以外的变量，即其绑定到了 solve() 命名空间下的 spam
    do_global()
    print("After global assignment:", spam)  # 此处 spam 被 global 修饰，即此处的 spam 为全局变量，位置在 solve 之外的全局区

solve()
print("In global scope:", spam)
```

---

## 13.2 定义类

---

使用 `class` 关键字定义一个类：
```python
class ClassName:
    """This is a Class"""
```

类定义与函数定义 ([`def`](https://docs.python.org/zh-cn/3.9/reference/compound_stmts.html#def) 语句) 一样必须被执行才会起作用，支持文档字符串。

进入类定义时，将创建一个新的命名空间，并将其用作局部作用域。因此，所有对局部变量的赋值都是在这个新命名空间之内。 特别的，函数定义会绑定到这里的新函数名称。

---

## 13.3 类对象

---

类对象支持两种操作：

* 属性引用
  * 实例化

属性引用使用 `Python` 中所有属性引用所使用的标准语法: `obj.name`。 有效的属性名称是类对象被创建时存在于类命名空间中的所有名称。 因此，如果类定义是这样的:
```python
class MyClass:
    """A simple example class"""
    i = 114514

    def f(self):
        print("Lys is a dog.")
```

那么 `MyClass.i` 和 `MyClass.f()` 就是有效的属性引用，将分别返回一个整数和一个函数对象。 类属性也可以被赋值，因此可以通过赋值来更改 `MyClass.i` 的值。 `__doc__` 也是一个有效的属性，将返回所属类的文档字符串: `"A simple example class"`。

类的实例化使用函数表示法。 可以把类对象视为是返回该类的一个新实例的不带参数的函数：
```python
class MyClass:
    """A simple example class"""
    i = 114514

    def f(self):
        print("Lys is a dog.")

x = MyClass()  # 获得一个类的实例
```

创建类的新实例并将此对象分配给局部变量 `x`。

实例化操作（“调用”类对象）会创建一个空对象。许多类喜欢创建带有特定初始状态的自定义实例。为此，类定义可能包含一个名为 [`__init__()`](https://docs.python.org/zh-cn/3.9/reference/datamodel.html#object.__init__) 的特殊方法，就像这样：

```python
def __init__(self):
    self.data = []
```

当一个类定义了 [`__init__()`](https://docs.python.org/zh-cn/3.9/reference/datamodel.html#object.__init__) 方法时，类的实例化操作会自动为新创建的类实例发起调用 [`__init__()`](https://docs.python.org/zh-cn/3.9/reference/datamodel.html#object.__init__)。因此在这个示例中，可以通过以下语句获得一个经初始化的新实例：

```python
class MyClass:
    """A simple example class"""

    def __init__(self):
        self.i = 1919

    def f(self):
        print("Lys is a dog.")

x = MyClass()  # 获得一个经过初始化的实例，其中 x.i = 1919
```

当然，[`__init__()`](https://docs.python.org/zh-cn/3.9/reference/datamodel.html#object.__init__) 方法还可以有额外参数以实现更高灵活性。在这种情况下，提供给类实例化运算符的参数将被传递给 [`__init__()`](https://docs.python.org/zh-cn/3.9/reference/datamodel.html#object.__init__)，如：

```python
class MyClass:
    """A simple example class"""

    def __init__(self, num1, num2):
        self.i = num1
        self.j = num2

    def f(self):
        print("Lys is a dog.")

x = MyClass(114514, 1919)

x.f()
print(x.i, x.j)
```

**注意**：在我们执行 `x = MyClass()`，生成了一个实例对象 `x`，这个实例对象有两种有效的属性名称：

* 数据属性
* 方法

```python
class MyClass:
    def __init__(self):
        i = 114514

i = 1919

def hello(self):
    return "Hello world"

print(MyClass.i)
print(MyClass.hello)

x = MyClass()
print(x.i)
print(x.hello)
print(x.hello())
```

* `MyClass.i` 是类变量，它的值可以通过类名直接访问，它的值在所有实例之间共享。
* `MyClass.hello` 是类方法，这是一个可调用的对象，但需要通过实例调用，而不是直接通过类名调用，直接调用返回该方法的地址。
* `x.i` 是实例变量，它的值必须通过实例名访问，它的值在不同实例之间互不影响。
* `x.hello` 是实例方法，它的值必须通过实例名访问，它只能在实例内部调用。
* `x.hello()` 则是调用实例方法，它会执行方法内部的代码并返回结果。

---

## 13.4 继承

---

### 13.4.1 单继承

---

和 `C++` 等支持面向对象的语言一样，`Python` 的类也支持继承，其派生类定义语法如下：
```python
class DerivedClassName(BaseClassName):
    """This is a derived class"""
```

名称 `BaseClassName` 必须定义于包含派生类定义的作用域中。

子类不声明新属性将全部继承父类属性和方法：
```python
class Father:
    """This is father class."""
    def __init__(self):
        self.i = 114514
        self.j = 1919

    def show(self, num):
        print(f"{self.__doc__}: {num}")

class Son(Father):
    """This is son class"""

x = Father()
x.show(x.i)

y = Son()
y.show(y.i)  # 子类继承了父类全部属性和方法
```

子类声明新属性，父类属性不继承，但可以直接调用父类方法：
```python
class Father:
    """This is father class."""
    def __init__(self):
        self.i = 114514
        self.j = 1919

    def show(self, num):
        print(f"{self.__doc__}: {num}")

class Son(Father):
    """This is son class"""
    def __init__(self):
        self.k = 1145141919

x = Father()
x.show(x.i)

y = Son()
# y.show(y.i)  # 不再继承父类属性
y.show(y.k)  # 但仍继承父类方法
```

若仍要保留父类属性，可再次初始化父类属性：
```python
class Father:
    """This is father class."""
    def __init__(self):
        self.i = 114514
        self.j = 1919

    def show(self, num):
        print(f"{self.__doc__}: {num}")

class Son(Father):
    """This is son class"""
    def __init__(self):
        super().__init__()  # 调用父类的 __init__ 方法来初始化父类属性
        self.k = 1145141919

x = Father()
x.show(x.i)

y = Son()
y.show(y.i)  # 由于调用了 super().__init__()，此行现在可以正常工作
y.show(y.k)
```

class Son(Father):
    """This is son class"""
    def __init__(self):
        Father.__init__(self)  # 调用父类的初始化属性
        self.k = 1145141919

x = Father()
x.show(x.i)

y = Son()
y.show(y.i)  # 重新继承了父类属性
y.show(y.k)  # 仍继承父类方法
```

---

### 13.4.2 多重继承

---

`Python` 也支持一种多重继承。 带有多个基类的类定义语句如下所示：
```python
class DerivedClassName(Base1, Base2, Base3):
    """This is a multiple derived class"""
```

注意，多重继承需要子类调用基类的 `__init__` 方法，否则只继承第一个基类的属性：
```python
class Father:
    """This is father class."""
    def __init__(self):
        self.i = 114514

class Mother:
    """This is mother class."""
    def __init__(self):
        self.j = 1919

class Son(Father, Mother):
    """This is son class"""

x = Son()
print(x.i)
# print(x.j)  # 缺少调用父类的 __init__ 方法的情况下，j 属性未定义。

class Father:
    """This is father class."""
    def __init__(self):
        self.i = 114514

class Mother:
    """This is mother class."""
    def __init__(self):
        self.j = 1919

class Son(Father, Mother):
    """This is son class"""
    def __init__(self):  # 调用基类的 __init__ 方法
        Father.__init__(self)
        Mother.__init__(self)

x = Son()
print(x.i)
print(x.j)
```

在一般情况下，搜索从父类所继承属性的操作是深度优先、从左至右的，当层次结构中存在重叠时不会在同一个类中搜索两次。 因此，如果某一属性在 `DerivedClassName` 中未找到，则会到 `Base1` 中搜索它，然后（递归地）到 `Base1` 的基类中搜索，如果在那里未找到，再到 `Base2` 中搜索，依此类推。

真实情况比这个更复杂一些；方法解析顺序会动态改变以支持对 [`super()`](https://docs.python.org/zh-cn/3.9/library/functions.html#super) 的协同调用。 这种方式在某些其他多重继承型语言中被称为后续方法调用，它比单继承型语言中的 `super()` 调用更强大。

---

### 13.4.3 私有变量

---

在 Python 中，并不存在真正的、仅限从对象内部访问的“私有”实例变量。但是，大多数 Python 代码都遵循一个约定：以一个下划线开头的名称（例如 `_spam`）应被视为 API 的非公有部分（无论它是函数、方法还是数据成员）。这应被看作是一个实现细节，可能在没有通知的情况下发生改变。

任何以 `__spam`（至少两个前导下划线，至多一个尾随下划线）形式出现的标识符文本，都会被替换为 `_classname__spam`，其中 `classname` 是去除了前导下划线的当前类名。这种重写不考虑标识符的语法位置，只要它出现在类定义内部就会进行。

直观上，这些被重写的名称不会被子类继承，这有助于子类重载方法而不破坏类内的方法调用：

```python
class Father:
    """This is father class."""

    def __init__(self):
        self.i = 114514
        self.__j = 1919

    def show(self, num):
        print(f"{self.__doc__}: {num}")

class Son(Father):
    """This is son class"""

y = Son()
y.show(y.i)  # 子类继承了 i
# y.show(y.j)  # 没有继承 j
```

---

## 13.5 魔法方法

---

魔法方法（Magic Methods）是 Python 中的内置方法，通常以双下划线开头和结尾，例如 `__init__`、`__del__` 等。它们被称为“魔法”方法，是因为在进行特定操作时，这些方法会被自动调用。

---

### 13.5.1 常见的魔法方法

---

#### `__doc__`

表示类的描述信息：

```python
class Solve:
    """This is a class."""

print(Solve.__doc__)
```

---

#### `__module__` 和 `__class__`

* `__module__` 表示当前操作的对象所在的模块。
* `__class__` 表示当前操作的对象所在的类。

```python
class Solve:
    """This is a class."""

x = Solve()
print(x.__module__)
print(x.__class__)
```

---

#### `__init__` 和 `__new__`

`__init__()` 是初始化方法，`__new__()` 是构造方法。当通过类创建对象时，它们会自动触发执行。`__new__` 负责创建并返回类的实例，而 `__init__` 则负责对传入的参数来初始化该实例：

* `__new__()` 在创建对象时调用，会返回当前对象的一个实例。
* `__init__()` 在创建完对象后调用，对当前对象的实例属性进行初始化，无返回值。

值得注意的是，`__new__` 被调用以创建一个 `cls` 类的新实例。它会将所请求实例所属的类作为第一个参数，其余的参数会被传递给对象构造器表达式（即对类的调用）。返回值应为新对象实例（通常是 `cls` 的实例）。

如果 `__new__()` 在构造对象期间被发起调用并且它返回了一个 `cls` 的实例，则新实例的 `