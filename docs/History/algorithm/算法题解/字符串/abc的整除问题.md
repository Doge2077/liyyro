---
title: "ABC的整除问题"
date: 2023-02-25
categories: [Q&A, 思维]
description: ""
---

# abc的整除问题


[原题链接](http://www.haueacm.top/problem.php?id=1423)

**描述**：

给定三个非负整数 $A,B,C$，且保证 $A\le B,C\ne 0$，求在区间 $[A, B]$ 中，存在多少个整数可以被 $C$ 整除？

**输入格式**：

第一行，一个整数 $T$，代表 $T$ 个测试样例。

接下来 $T$ 行，每行给出三个非负整数 $A,B,C$。

**输出格式**：

共 $T$ 行，每行输出一个整数，代表在区间 $[A, B]$ 中可以被 $C$ 整除的数的数量。

**数据范围**：

$1\le A\le B\le 1\times 10^{18}, 1\le C\le 1\times 10^{18}$。

**样例输入**：
```text
2
4 8 2
3 100 4
```

**样例输出**：
```text
3
25
```

**思想**：

* 签到题。
  * 考虑 $A$ 和 $B$ 是 $C$ 的最大多少整数倍，得到差值。
  * 然后考虑 $A$ 是否可以被 $C$ 整除，若可以，则差值加一即可。

**代码**：
```cpp
#include <iostream>
#include <cstring>
#include <cstdio>
#include <algorithm>
#include <cmath>
#include <sstream>
#include <vector>
#include <queue>
#include <stack>
#include <map>
#include <set>
#include <unordered_map>
#include <unordered_set>
#include <bits/stdc++.h>

using namespace std;

#define IOS ios::sync_with_stdio(false),cin.tie(nullptr),cout.tie(nullptr)
#define re register
#define fi first
#define se second
#define endl '\n'

typedef long long LL;
typedef pair<int, int> PII;
typedef pair<LL, LL> PLL;

const int N = 1e6 + 3;
const int INF = 0x3f3f3f3f, mod = 1e9 + 7;
const double eps = 1e-6, PI = acos(-1);

LL a, b, c;

void solve() {
    cin >> a >> b >> c;
    cout << b / c - a / c + (a % c == 0) << endl;
}

int main() {
    IOS;
    int _ = 1;
    cin >> _;
    while (_--) {
        solve();
    }
    return 0;
}
```

