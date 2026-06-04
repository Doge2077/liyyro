---
title: "770.单词替换 (stringstream)"
date: 2022-06-15
categories: [ALGORITHM, Q&amp;A, 字符串]
description: ""
---

### 770.单词替换 (stringstream)

[原题链接](https://www.acwing.com/problem/content/770/) **描述**：输入一个字符串，以回车结束（字符串长度不超过 100）。

该字符串由若干个单词组成，单词之间用一个空格隔开，所有单词区分大小写。

现需要将其中的某个单词替换成另一个单词，并输出替换之后的字符串。

**输入格式**：输入共 3 行。

第 1 行是包含多个单词的字符串 s;

第 2 行是待替换的单词 a(长度不超过 100);

第 3 行是 a 将被替换的单词 b(长度不超过 100)。

**输出格式**：共一行，输出将 s 中所有单词 a 替换成 b 之后的字符串。

**输入样例：**
```text
You want someone to help you
You
I
```

**输出样例：**
```text
I want someone to help you
```

**分析**：

* 替换单词字符串，可以利用`stringstream`依次读入，判断输出

**代码**：
```cpp
#include &lt;bits/stdc++.h&gt;
using namespace std;
int main()
{
    string s, s1, a, b;
    getline(cin, s);  //读入
    cin >> a >> b;
    stringstream ssin(s);  //初始化
    while(ssin >> s1) {  //依次读入
        if(s1 == a) {  //判断
            cout &lt;&lt; b &lt;&lt; " ";
        }
        else cout &lt;&lt; s1 &lt;&lt; " ";
    }
    return 0;
}
```

---

#### string 操作

&gt;     string str1 = "abcdefghijklmn" ;
>     string str = "efg" ;
>
>     string str2 = str1.substr(2,5) ;  //将str1从下标2开始的5个字符赋值给str2
>
>     int p1 = str1.find(str) ; //从最左边开始返回str1中首次出现str首字母的下标，没有时返回-1
>
>     int p2 = str1.rfind(str) ;  //从最右边开始返回str1中首次出现str首字母的下标，没有时返回-1
>
>     string str3 = "1234.567" ;
>
>     double nums = atof(str3.c_str()) ;  //将str3转换为double类型
>
>     int num_i = atoi(str3.c_str()) ;  //将str3转换为int类型