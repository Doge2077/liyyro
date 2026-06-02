---
title: "Codeforces Global Round 23（A~C）"
date: 2022-10-17
categories: [ALGORITHM, Q&amp;A, Codeforces, 思维]
description: ""
---

## A. Maxmina

---

[Origional Link](&lt;https://codeforces.com/contest/1746/problem/A&gt;)

**题目大意** ：

  * 给定长度为 $n$ 只包含 $0,1$ 的序列 $a$，和一个整数 $k$，保证 $(2\le k\le n\le 50)$。
  * 不限次数进行如下操作： 
```java
* 将连续且相邻的两个元素变为较小的一个。
* 将连续的 $k$ 个区间的元素变为区间内元素最大的哪一个。
```
  * 求给出的序列是否可以变为只包含 $1$ 的序列。



---

**思想** ：

  * 签到题。
  * 保证 $(2\le k\le n\le 50)$ 即保证了只要序列里含有 $1$，便可不断执行操作二，即只要存在 $1$ 即可。



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

void solve(){

    int n, k; cin >> n >> k;

    bool flag = 0;

    for(int i = 0; i < n; i ++){
        int x; cin >> x;
        if(x == 1) flag = 1;
    }

    if(flag) cout << "YES" << endl;
    else cout << "NO" << endl;

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

## B. Rebellion

---

[Origional Link](&lt;https://codeforces.com/contest/1746/problem/B&gt;)

**题目大意** ：

  * 给定长度为 $n$ 只包含 $0,1$ 的序列 $a$。
  * 不限次数进行如下操作： 
```java
* 选择两个下标 $1 \le i,j\le n,i\ne j$。
* 使得 $a_j = a_j + a_i$；
* 将 $a_i$ 从 $a$ 中去除。
```
  * 若最终可以通过上述操作将 $a$ 变为非严格单调递增的序列，则求出最小操作次数，否则输出 $-1$。



---

**思想** ：

  * 思维题。
  * 将 $a$ 排序，与原位置不相同时只可能为原序列为 $1$ 而排序后为 $1$ 的情况。
  * 此时我们只需要执行操作一即可，等价于交换两数的值。
  * 由此我们可以利用双指针操作并记录次数，或者直接统计需要交换位置的数量除以 $2$ 即可。 



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

int a[N], b[N];

void solve(){

    int n; cin >> n;

    for(int i = 0; i < n; i ++){
        cin >> a[i];
        b[i] = a[i];
    }
    sort(b, b + n);
    int cnt = 0;
    for(int i = 0; i < n; i ++){
        if(a[i] != b[i]) cnt ++;
    }
    cout << cnt / 2 << endl;

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

## C. Permutation Operations

---

[Origional Link](&lt;https://codeforces.com/contest/1746/problem/C&gt;)

**题目大意** ：

  * 给定一个长度为 $n$ 的排列序列 $a$。
  * 在 $i$ 次操作中，你可以选择任意的 $a$ 的非空后缀，使得所有的后缀元素加 $i$。
  * 求如何操作，使得操作后的序列 $a$ 不含逆序对。
  * 输出第 $i$ 次操作的后缀的起始位置。
  * 逆序对：对于 $i,j(i\gt j)$ 满足 $a_i \lt a_j$。



---

**思想** ：

  * 思维题。
  * 记录每一对逆序对的差值，那么第 $i$ 次操作需要补足该差值。
  * 由于对后缀的操作不会影响到前面，则我们不需要考虑操作的顺序，只需考虑差值何时补齐即可。
  * 显然，我们可以对所有的差值从小到大进行排序，第 $i$ 次操作可以操作差值为 $t,t\lt i$ 的位置后缀，若无法操作输出 $1$。
  * 使用优先队列（小根堆）存储所有的差值，操作后出队，队列为空说明已经补齐了差值，此时仅需输出 $1$ 即可。 



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

int a[N];

void solve(){

    int n; cin >> n;

    for(int i = 1; i <= n; i ++) cin >> a[i];

    priority_queue&lt;PII, vector&lt;PII&gt;, greater&lt;PII&gt;&gt; b;

    for(int i = 2; i <= n; i ++){
        int t = a[i] - a[i - 1];
        if(t <= 0){
            b.push({-t + 1, i});
        }
    }

    if(b.empty()){
        for(int i = 1; i <= n; i ++) cout << 1 << ' ';
    }
    else{
        auto p = b.top();
        for(int i = 1 ; i <= n; i ++){
            if(i >= p.fi && !b.empty()){
                cout << p.se << ' ';
                b.pop(); p = b.top();
            }
            else cout << 1 << ' ';
        }
    }

    cout << endl;

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
