---
title: "AtCoder Beginner Contest 273（A~D）"
date: 2022-10-17
categories: [ALGORITHM, Q&amp;A, 模拟, 二分, AtCoder]
description: ""
---

## A - A Recursive Function

---

[Original Link](https://atcoder.jp/contests/abc273/tasks/abc273_a)

**题目大意** ：

* 求 $f(k)$ 如下： 
```java
* $f(0) = 1$;
* $f(k) = k \times f(k - 1)$
```

---

**思想** ：

* 签到题。

---

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

LL f(LL n){
    if(n == 0) return 1;
    else return n * f(n - 1);
}

void solve(){

LL n; cin >> n;
    cout &lt;&lt; f(n) &lt;&lt; endl;

}

int main(){

IOS;

int _ = 1;

// cin &gt;> _;

while(_ --){
        solve();
    }

return 0;

}
```

---

## B - Broken Rounding

---

[Original Link](https://atcoder.jp/contests/abc273/tasks/abc273_b)

**题目大意** ：

* 给定一个整数 $x$，可以进行 $k$ 次操作。
  * 每次将 $x$ 改为一个与 $10^i$ 的倍数相差最小的数字。

---

**思想** ：

* 模拟。
  * 每次操作找到与 $\lfloor \frac{x}{10^i} \rfloor x$ 和 $\lceil \frac{x}{10^i} \rceil x$ 最接近的数，并取代即可。

---

**代码** ：
```java
```cpp
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

void solve() {
    LL x; int k;
    cin >> x >> k;
    LL fac = 1;
    for (int i = 1; i &lt;= k; i++) {
        fac *= 10;
        LL a = x / fac, b = ceil(1.0 * x / fac);
        a *= fac; b *= fac;
        if (abs(a - x) &lt; abs(b - x)) x = a;
        else x = b;
    }
    cout &lt;&lt; x &lt;&lt; endl;
}

int main() {
    IOS;
    int _ = 1;
    // cin &gt;> _;
    while (_--) {
        solve();
    }
    return 0;
}
```

## C - (K+1)-th Largest Number

---

[Original Link](https://atcoder.jp/contests/abc273/tasks/abc273_c)

**题目大意**：

* 给定一个长度为 $n$ 的整数序列 $A={A_1,A_2,\dots,A_n}$。
  * 对于 $k = 0,1,2,\dots,N-1$：
    * 在序列 $A$ 中，统计有多少个元素 $A_i$ 恰好有 $k$ 个数大于 $A_i$。

---

**思想**：

* 记录每个不同值出现的次数，并从大到小排序。
  * 通过二分查找确定每个 $A_i$ 的排名，即大于 $A_i$ 的数的数量，并存储结果。

---

**代码**：
```cpp
// 此处应填写对应问题的C++代码
```
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

LL a[N];
int idx;
LL b[N];
LL c[N];
map&lt;LL,int&gt; vis;

void solve() {
    int n; cin >> n;
    for (int i = 0; i &lt; n; i++) {
        cin &gt;> a[i];
        if (vis[a[i]] == 0) {
            vis[a[i]] = 1;
            b[idx++] = a[i];
        }
    }

    sort(b, b + idx, greater&lt;LL&gt;());

    for (int i = 0; i &lt; n; i++) {
        int t = lower_bound(b, b + idx, a[i], greater&lt;LL&gt;()) - b;
        c[t]++;
    }

    for (int i = 0; i &lt; n; i++) {
        cout &lt;&lt; c[i] &lt;&lt; endl;
    }
}

int main() {
    IOS;

    int _ = 1;
    // cin &gt;> _;
    while (_--) {
        solve();
    }

    return 0;
}
```

---

## D - LRUD Instructions

---

[Original Link](https://atcoder.jp/contests/abc273/tasks/abc273_d)

**题目大意** ：

* 给定 $h\times w$ 的矩阵，起始点为 $(rs,cs)$。
  * 给定 $n$ 个 $(r_i,c_i)$ 的坐标表示为墙。
  * 给定 $q$ 次操作，对于 $q_i$ 给出行进方向 $d_i$ 和次数 $l_i$。
  * 遇到边界或者墙则停止操作。
  * 对于每次操作，输出执行完毕后的位置。

---

**思想** ：

* 二分，模拟。 
  * 朝着某一方向走 $l_i$ 步，我们需要快速定位到在其方向上最近的墙的位置或者边界的位置。
  * 考虑二分，同时我们需要存储每一个行对应的列坐标，每一个列对应的行坐标。
  * 由于坐标范围很大，所以我们考虑 `map&lt;LL, set&lt;LL&gt;&gt;` 来快速查询。

---

**代码** ：
```cpp
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

map&lt;LL, vector&lt;LL&gt;&gt; dx, dy;

void solve(){

LL l, w, x, y; cin >> l >> w >> x >> y;

map&lt;LL,set&lt;LL&gt;&gt; dx, dy;

int n; cin >> n;
    while(n --){
        LL a, b;
        cin >> a >> b;
        dx[a].insert(b);
        dy[b].insert(a);
    }

for (auto &&i : dx){
        i.second.insert(0);
        i.second.insert(w + 1);
    }
    for (auto &&i : dy){
        i.second.insert(0);
        i.second.insert(l + 1);
    }
```

int q;
cin >> q;
while (q-- > 0) {
    char op;
    LL k;
    cin >> op >> k;

    if (op == 'L') {
        LL ny = y - k;
        if (dx.find(x) == dx.end()) {
            y = max(ny, (LL)1);
        } else {
            auto it = dx[x].lower_bound(y);
            it = prev(it);
            y = max(*it + 1, ny);
        }
    } else if (op == 'R') {
        LL ny = y + k;
        if (dx.find(x) == dx.end()) {
            y = min(ny, w);
        } else {
            auto it = dx[x].lower_bound(y);
            y = min(*it - 1, ny);
        }
    } else if (op == 'U') {
        LL nx = x - k;
        if (dy.find(y) == dy.end()) {
            x = max(nx, (LL)1);
        } else {
            auto it = dy[y].lower_bound(x);
            it = prev(it);
            x = max(*it + 1, nx);
        }
    } else {
        LL nx = x + k;
        if (dy.find(y) == dy.end()) {
            x = min(nx, l);
        } else {
            auto it = dy[y].lower_bound(x);
            x = min(*it - 1, nx);
        }
    }

    cout &lt;&lt; x &lt;&lt; ' ' &lt;&lt; y &lt;&lt; endl;
}

int main() {
    IOS;

    int _ = 1;
    // cin &gt;> _;
    while (_--) {
        solve();
    }

    return 0;
}