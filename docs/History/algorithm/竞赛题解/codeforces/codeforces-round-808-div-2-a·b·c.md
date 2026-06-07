---
title: "Codeforces Round #808 (Div 2.) A·B·C"
date: 2022-07-19
categories: [ALGORITHM, Q&A, 数学, Codeforces, 贪心]
description: ""
---

# codeforces-round-808-div-2-a·b·c


---

## A. Difference Operations

---

### 原题链接

[Original Link](https://codeforces.com/contest/1708/problem/A)

---

### 思想

* 若 $a_i (i>=2)$ 可以通过
  $$
  a_i = a_i - a_{i-1}
  $$
  变为 $0$
  * 说明：$a_{i-1} | a_i$
* 若
  $$
  a_{i-1} (i>=2)
  $$
  可以通过
  $$
  a_{i-1} = a_{i-1} - a_{i-2}
  $$
  变为 $0$
  * 说明：$a_{i-2} | a_{i-1}$
  * 由此可得，当 $a_i (i>=2)$ 可以变为 $0$ 时
  * 说明：$a_1 | a_i$

---

### 代码

```cpp
#include <bits/stdc++.h>
using namespace std;

const int N = 1e6 + 3;

int a[N];

void solve() {
    int n;
    cin >> n;
    for (int i = 1; i <= n; i++) {
        cin >> a[i];
    }

    bool flag = 1;
    int t = a[1];
    for (int i = 2; i <= n; i++) {
        if (a[i] % t != 0) {
            flag = 0;
            break;
        }
    }

    if (flag)
        cout << "YES" << "\n";
    else
        cout << "NO" << "\n";
}

int main() {
    int tt;
    cin >> tt;
    while (tt--) {
        solve();
    }
    return 0;
}
```

---

## B. Difference of GCDs

---

### 原题链接

[Original Link](https://codeforces.com/contest/1708/problem/B)

---

### 思想

* 要求 $gcd(i, a_i)$ 所构成的序列里，$gcd(i, a_i)$ 均不同
  * 说明 $gcd(i, a_i) = i$，即 $i | a_i$
  * 故需要在区间 $[l, r]$ 中寻找 $i$ 的倍数
  * 对于 $a_i$，若 $l \leqslant a_i = \lfloor \frac{r}{i} \rfloor \times i \leqslant r$，则满足条件

---

### 代码

```cpp
#include <bits/stdc++.h>
using namespace std;

const int N = 1e6 + 3;

int a[N];

void solve() {
    int n, l, r;
    cin >> n >> l >> r;

    bool flag = 1;

    for (int i = 1; i <= n; i++) {
        a[i] = r / i * i;
        if (a[i] < l) {
            flag = 0;
            break;
        }
    }
    // 代码未完，需补充后续逻辑及输出
}
```

---

## C. Doremy's IQ

---

### 原题链接

[Original Link](https://codeforces.com/contest/1708/problem/C)

---

### 思想

*   逆向贪心
    *   从最后一天考虑，设智商上限为 $Q$，最后一天的智商为 $q_i=0$。
    *   若 $a_i \leqslant q_i$，则第 $i$ 天的比赛需要打。
    *   若 $a_i &gt; q_i$，且 $q_i &lt; Q$ 时，若第 $i$ 天打比赛，则 $q_i = q_i + 1$。
    *   由于 $a_i &gt; q_i$ 的比赛最多打 $Q$ 次，对于前面的比赛要继续打，需要 $q_i$ 尽可能的大。
    *   故当 $a_i > q_i$，且 $q_i &lt; Q$ 时，该第 $i$ 天的比赛必须打，$q_i = q_i + 1$。
    *   若 $a_i &gt; q_i$，且 $q_i = Q$ 时，第 $i$ 天的比赛不能打。

---

### 代码

```cpp
#include <bits/stdc++.h>
using namespace std;

const int N = 1e6 + 3;

int a[N];

void solve() {
    int n, m;
    cin >> n >> m;

    string s(n, '0');

    for (int i = 0; i < n; i++) cin >> a[i];

    int q = 0;

    for (int i = n - 1; i >= 0; i--) {
        if (a[i] <= q) s[i] = '1';
        else if (a[i] > q && q < m) {
            q++;
            s[i] = '1';
        }
    }

    cout << s << "\n";
}

int main() {
    int tt;
    cin >> tt;

    while (tt--) {
        solve();
    }

    return 0;
}
```

---

### 后记

*   这天比赛脑子有点抽风。
    *   $A$ 和 $B$ 居然都是数学证明的类型，考虑麻烦了，把自己陷了进去。
    *   赛后补题发现 $A$ 和 $B$ 原来这么简单，还是自己数学基础不好，吃大亏 QAQ。
    *   $C$ 题一眼 `DP`，赛时考虑了贪心，但是没证出来，逆向贪心的问题不知道怎么处理。
    *   希望早日变绿。。。。。。（我好笨比）

