---
title: "Python提取文本中出现的全部合法日期"
date: 2023-07-05
categories: [Python, Tips]
description: ""
---

## 需求

* * *

  * 给定一段文本，要求提取其中出现的所有合法日期；
  * 将这些日期统一格式，从小到大排序并去重后，并返回一个列表。



* * *

## 思路

* * *

  * 首先利用正则表达式，提取所有的日期：
  * 可能出现的日期格式： 
```java
* xxxx.xx.xx
* xxxx-xx-xx
* xxxx年xx月xx日
* xxxx年xx月xx号
```
  * 将所有提取到的日期转换成为 xxxx.xx.xx 的标准格式；
  * 利用 `datetime` 库判断日期是否合法，然后排序去重即可。



* * *

## 代码

* * *
```java


from datetime import datetime
import re

def extractDates(text):
    pattern = r"\b(\d{4})[年.-](\d{1,2})[月.-]?(\d{1,2})?[日号]?\b"
    dates = sorted(
        [
            f"{year}.{month.zfill(2)}.{day.zfill(2) if day else '01'}"
            for year, month, day in re.findall(pattern, text)
            if isValidDate(f"{year}.{month.zfill(2)}.{day.zfill(2) if day else '01'}")
        ],
        key=lambda x: tuple(map(int, x.split('.')))
    )
    return dates

def isValidDate(dateStr):
    try:
        datetime.strptime(dateStr, "%Y.%m.%d")
        return True
    except ValueError:
        return False

text = "2022.2.31, 2020.2.29-2022.3.1, 2023.10, 2023.1, 2023年7月5日, 2023年7月, 2023年7月5号, 2023-07-05, 2023-7-5"
dates = extractDates(text)
print(dates)  # outputs: ['2020.02.29', '2022.03.01', '2023.01.01', '2023.07.01', '2023.07.05', '2023.07.05', '2023.07.05', '2023.07.05', '2023.10.01']
```
