---
title: "Python 第一次作业及解答"
date: 2023-01-29
categories: [python, Python]
description: ""
---

# python-prictice1


## 第一次练习

---

[下载习题](https://cdn.jsdelivr.net/gh/Doge2077/liyyro-photo@main/images/2023/01/Python基础练习题一.txt)

---

## 1. 姓名

---
```python
names = ['wjq', 'lys', 'hfcj', 'xhz', 'jcg']
for i in names:
    print(i)
```

---

## 2. 问候

---
```python
names = ['wjq', 'lys', 'hfcj', 'xhz', 'jcg']
for i in names:
    print(f"hello,{i}!")
```

---

## 3. 嘉宾名单

---
```python
names = ['wjq', 'hfcj', 'xhz', 'jcg']
for i in names:
    print(f"Hello,{i}! Would you like to have a dinner for me?")
```

---

## 4. 修改嘉宾名单

---
```python
names = ['wjq', 'hfcj', 'xhz', 'jcg']
for i in names:
    print(f"Hello,{i}! Would you like to have a dinner for me?")
print(f"Unfortunately, {names[1]} couldn't come.")
names[1] = 'mcc'
for i in names:
    print(f"Hello,{i}! Would you like to have a dinner for me?")
```

---

## 5. 添加嘉宾

---
```python
names = ['wjq', 'hfcj', 'xhz', 'jcg']
print("I have found a bigger table for the party")
names.insert(0, 'lrh')
names.insert(len(names)//2, 'mcc')
names.append('lsh')
for i in names:
    print(f"Hello,{i}! Would you like to have a dinner for me?")
```

---

## 6. 缩减名单

---

```python
names = ['wjq', 'hfcj', 'xhz', 'jcg']
print("I have found a bigger table for the party")
names.insert(0, 'lrh')
names.insert(len(names)//2, 'mcc')
names.append('lsh')
for i in names:
    print(f"Hello,{i}! Would you like to have a dinner for me?")
print(f"Unfortunately, I could only invite two guys to the party!")
while(len(names) > 2):
    names.pop()
for i in names:
    print(f"Wow! {i} is still in the list !")
del names[:]
print(names)
```

---

## 7. 放眼世界

---

```python
locations = ['Singapore', 'Hong Kong', 'Australia', 'Russia', 'Spain', 'France']
for i in locations:
    print(i)
print(sorted(locations))
print(sorted(locations, reverse=True))
print(locations)
locations.reverse()
print(locations)
locations.reverse()
print(locations)
locations.sort()
print(locations)
locations.sort(reverse=True)
print(locations)
```
