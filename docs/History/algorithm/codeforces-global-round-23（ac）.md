---
title: "Codeforces Global Round 23（A~C）"
date: 2022-10-17
categories: [ALGORITHM, Q&amp;A, Codeforces, 思维]
description: ""
---

## A. Maxmina

---

[Original Link](https://codeforces.com/contest/1746/problem/A)

**题目大意** ：

* 给定长度为 $n$ 只包含 $0,1$ 的序列 $a$，和一个整数 $k$，保证 $(2\le k\le n\le 50)$。
  * 不限次数进行如下操作：
1. 将连续且相邻的两个元素变为较小的一个。
2. 将连续的 $k$ 个区间的元素变为区间内元素最大的那个。
  * 求给出的序列是否可以变为只包含 $1$ 的序列。

---

**思想** ：

* 签到题。
  * 保证 $(2\le k\le n\le 50)$ 即保证了只要序列里含有 $1$，便可不断执行操作二，即只要存在 $1$ 即可。

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

void solve(){

int n, k; cin >> n >> k;

bool flag = 0;

for(int i = 0; i &lt; n; i ++){
        int x; cin &gt;> x;
        if(x == 1) flag = 1;
    }

if(flag) cout &lt;&lt; "YES" &lt;&lt; endl;
    else cout &lt;&lt; "NO" &lt;&lt; endl;

}

int main(){

IOS;

int _ = 1;

cin &gt;> _;

while(_ --){
        solve();
    }

return 0;

}
```

---

## B. Rebellion

---

[Original Link](https://codeforces.com/contest/1746/problem/B)

**题目大意**：

* 给定长度为 $n$ 只包含 $0,1$ 的序列 $a$。
  * 不限次数进行如下操作：
```text
* 选择两个下标 $1 \le i,j\le n,i\ne j$。
* 使得 $a_j = a_j + a_i$；
* 将 $a_i$ 从 $a$ 中去除。
```
  * 若最终可以通过上述操作将 $a$ 变为非严格单调递增的序列，则求出最小操作次数，否则输出 $-1$。

---

**思想**：

* 思维题。
  * 将 $a$ 排序，与原位置不相同时只可能为原序列中为 $1$ 但排序后应为 $0$ 的情况。
  * 此时我们只需要执行一次操作，等价于交换两数的值。
  * 由此我们可以利用双指针操作并记录次数，或者直接统计需要交换位置的数量除以 $2$ 即可。

---

**代码**：
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

int a[N], b[N];

void solve(){
    int n; cin >> n;
    for(int i = 0; i &lt; n; i ++){
        cin &gt;> a[i];
        b[i] = a[i];
    }
    sort(b, b + n);
    int cnt = 0;
    for(int i = 0; i &lt; n; i ++){
        if(a[i] != b[i]) cnt ++;
    }
    cout &lt;&lt; cnt / 2 &lt;&lt; endl;
}

int main(){
    IOS;
    int _ = 1;
    cin &gt;> _;
    while(_ --){
        solve();
    }
    return 0;
}
```

---

**C. Permutation Operations**

[Original Link](https://codeforces.com/contest/1746/problem/C)

**题目大意**：

* 给定一个长度为 $n$ 的排列序列 $a$。
  * 在第 $i$ 次操作中，你可以选择 $a$ 的任意非空后缀，使得该后缀中的所有元素增加 $i$。
  * 求如何操作，使得操作后的序列 $a$ 不含逆序对。
  * 输出每次操作的后缀起始位置。
  * 逆序对：对于 $i, j$（$i > j$），满足 $a_i &lt; a_j$。

---

**思路**：

* 思维题。
  * 记录每一对逆序对的差值（绝对值），第 $i$ 次操作需要补足该差值。
  * 由于对后缀的操作不会影响到前面的元素，因此不需要考虑操作顺序，只需考虑差值何时被补足。
  * 显然，可以对所有差值从小到大排序，第 $i$ 次操作可以处理差值为 $t$（$t \le i$）的位置的后缀，若无法操作则输出 $1$。
  * 使用优先队列（小根堆）存储所有差值，操作后出队，队列为空时说明所有逆序对已被处理，此时输出 $1$ 即可。

---

**代码**：
```cpp
#include &lt;iostream&gt;
#include &lt;vector&gt;
#include &lt;queue&gt;
#include &lt;algorithm&gt;

using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector&lt;int&gt; a(n + 1);
    for (int i = 1; i &lt;= n; ++i) {
        cin &gt;> a[i];
    }

    // 存储 (差值, 位置) 的小根堆
    priority_queue&lt;pair&lt;int, int&gt;, vector&lt;pair&lt;int, int&gt;>, greater&lt;pair&lt;int, int&gt;>> pq;
    for (int i = 2; i &lt;= n; ++i) {
        if (a[i] &lt; a[i - 1]) {
            int diff = a[i - 1] - a[i];
            pq.push({diff, i});
        }
    }

    for (int i = 1; i &lt;= n; ++i) {
        if (pq.empty() || pq.top().first &gt; i) {
            cout &lt;&lt; 1 &lt;&lt; " ";
        } else {
            cout &lt;&lt; pq.top().second &lt;&lt; " ";
            pq.pop();
        }
    }
    cout &lt;&lt; "\n";

    return 0;
}
```

void solve() {
    if (b.empty()) {
        for (int i = 1; i &lt;= n; i++) cout &lt;&lt; 1 &lt;&lt; ' ';
    } else {
        auto p = b.top();
        for (int i = 1; i &lt;= n; i++) {
            if (i &gt;= p.first && !b.empty()) {
                cout &lt;&lt; p.second &lt;&lt; ' ';
                b.pop();
                p = b.top();
            } else {
                cout &lt;&lt; 1 &lt;&lt; ' ';
            }
        }
    }

    cout &lt;&lt; endl;
}

int main() {
    IOS;

    int _ = 1;
    cin &gt;> _;

    while (_--) {
        solve();
    }

    return 0;
}