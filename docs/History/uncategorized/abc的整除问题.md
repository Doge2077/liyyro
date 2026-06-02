---
title: "ABC的整除问题"
date: 2023-02-25
categories: [Q&amp;A, 思维]
description: ""
---

[原题链接](&lt;http://www.haueacm.top/problem.php?id=1423&gt;)

**描述** ：

给定三个非负整数 $A,B,C$，且保证 $A\le B,C\ne 0$，求在区间 $[A, B]$ 中，存在多少个整数可以被 $C$ 整除？

**输入格式** ：

第一行，一个整数 $T$，代表 $T$ 个测试样例。

接下来 $T$ 行，每行给出三个非负整数 $A,B,C$。

**输出格式** ：

共 $T$ 行，每行输出一个整数，代表在区间 $[A, B]$ 中可以被 $C$ 整除的数的数量。

**数据范围** ：

$1\le A\le B\le 1\times 10^{18}, 1\le C\le 1\times 10^{18}$。

**样例输入** ：
```java


2
4 8 2
3 100 4
```

**样例输出** ：
```java


3
25
```

**思想** ：

  * 签到题。
  * 考虑 $A$ 和 $B$ 是 $C$ 的最大多少整数倍，得到差值。
  * 然后考虑 $A$ 是否可以被 $C$ 整除，若可以，则差值加一即可。



**代码** ：
```java


#include &lt;iostream&gt;
#include &lt;cstring&gt;
#include &lt;cstdio&gt;
#include &lt;algorithm&gt;
#include &lt;cmath&gt;
#include &lt;sstream&gt;
#include &lt;vector&gt;
#include &lt;queue&gt;
#include &lt;stack&gt;
#include &lt;map&gt;
#include &lt;set&gt;
#include &lt;unordered_map&gt;
#include &lt;unordered_set&gt;
#include &lt;bits/stdc++.h&gt;

using namespace std;

#define IOS ios::sync_with_stdio(false),cin.tie(nullptr),cout.tie(nullptr)
#define re register
#define fi first
#define se second
#define endl '\n'

typedef long long LL;
typedef pair&lt;int, int&gt; PII;
typedef pair&lt;LL, LL&gt; PLL;

const int N = 1e6 + 3;
const int INF = 0x3f3f3f3f, mod = 1e9 + 7;
const double eps = 1e-6, PI = acos(-1);

LL a, b, c;

void solve(){
    cin >> a >> b >> c;
    cout << b / c - a / c + (a % c == 0) << endl;
}

int main(){

    IOS;

    int _ = 1;

    cin >> _;

    while(_ --){
        solve();
    }

    return 0;

}
```

---
