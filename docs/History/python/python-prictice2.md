---
title: "Python 第二次作业及解答"
date: 2023-01-31
categories: [python, Python]
description: ""
---

## 第二次练习

---

[下载习题](https://cdn.jsdelivr.net/gh/Doge2077/liyyro-photo@main/images/2023/01/python基础练习题二.txt)

---

## 1. 外星人颜色

---

```python
AlienColor = 'green'
if AlienColor == 'green':
    print("Player gets 5 points.")
```

---

## 2. 外星人2

---

```python
AlienColor = 'green'
if AlienColor == 'green':
    print("Player gets 5 points by shooting this alien.")
else:
    print("Player gets 10 points.")
```

---

## 3. 外星人的颜色3

---

```python
AlienColor = 'green'
if AlienColor == 'green':
    print("Player gets 5 points.")
elif AlienColor == 'yellow':
    print("Player gets 10 points.")
else:
    print("Player gets 15 points.")
```

---

## 4. 人生的不同阶段

---

```python
age = 24
if age &lt; 2:
    print("It's a baby")
elif age &gt;= 2 and age &lt; 4:
    print("It's a child")
elif age &gt;= 4 and age &lt; 13:
    print("It's a tween")
elif age &gt;= 13 and age &lt; 18:
    print("It's a teenager")
elif age &gt;= 18 and age < 65:
    print("It's an adult")
else:
    print("It's an elder")

# 另一种解法
age = 24
if age < 2:
    print("It's a baby")
elif 2 <= age < 4:
    print("It's a child")
elif 4 <= age < 13:
    print("It's a tween")
elif 13 <= age < 18:
    print("It's a teenager")
elif 18 <= age < 65:
    print("It's an adult")
else:
    print("It's an elder")
```

---

## 5. 判断序列（例如列表）为空？

---

```python
a = []
if len(a) == 0:
    print("Empty.")
else:
    print("Not empty.")

# 另一种解法
if not a:
    print("Empty.")
else:
    print("Not empty.")
```

---

## 6. 多维列表

---

```python
a = ["str, 12345", ('tunpe', 2), {'dict': {'dict': {'dict': 4}}}]
for i in range(len(a)):
    if i == 0:
        print(a[i], end=' ')
    elif i == 1:
        for j in a[i]:
            print(j, end=' ')
    elif i == 2:
        for k1, v1 in a[i].items():
            print(f"key: {k1}, value: {v1}")
            for k2, v2 in v1.items():
                print(f"key: {k2}, value: {v2}")
                for k3, v3 in v2.items():
                    print(f"key: {k3}, value: {v3}", end=' ')
    print()
```

---

## 7. 序列打包

---

```python
name = ['lys', 'wjq', 'hfcj', 'xhz', 'jcg']
age = [104, 504, 1909, 14, 3.14]
info = {k:v + 10 for k, v in zip(name, age)}
for k, v in info.items():
    print(f"Name: {k}, NowAge: {v}")
```