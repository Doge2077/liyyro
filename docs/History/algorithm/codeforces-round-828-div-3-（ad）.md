---
title: "Codeforces Round #828 (Div. 3) （A~D）"
date: 2022-10-17
categories: [ALGORITHM, Q&amp;A, 模拟, Codeforces, 贪心, 思维]
description: ""
---

## A. Number Replacement

* * *

[Origional Link](&lt;https://codeforces.com/contest/1744/problem/A&gt;)

**题目大意**

  * 给定一个序列 $a$ 和一个字符串 $s$。
  * 可以将相同的 $a_i$ 替换为 $s_i$，若$a_i$ 对应的替换规则唯一。
  * 求是否可以在满足上述条件下完成替换。



* * *

**思想** ：

  * 思维。
  * 当 $s_i$ 所对应的 $a_i$ 首次出现时建立对应规则。
  * 若 $s_i$ 对应的 $a_i$ 出现过且规则不同说明无法完成替换。



* * *

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

    int vis[1010] = {0};

    int n; cin >>n;
    for(int i = 0; i < n; i ++) cin >> a[i];
    string s; cin >> s;
    for(int i = 0; i < s.size(); i ++){
        if(vis[a[i]] == 0){
            vis[a[i]] = s[i];
        }
        else{
            if(vis[a[i]] != s[i]){
                cout << "NO" << endl;
                return ;
            }
        }
    }

    cout << "YES" << endl;

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

* * *

## B. Even-Odd Increments

* * *

[Origional Link](&lt;https://codeforces.com/contest/1744/problem/B&gt;)

**题目大意**

  * 给定一个序列 $a$ 和 $q$ 次操作： 
```java
* 操作 $0~~x_j$ 表示将序列中所有的偶数加上 $x_j$。
* 操作 $1~~x_j$ 表示将序列中所有的奇数加上 $x_j$。
```
  * 求每次操作之后的序列之和。



* * *

**思想** ：

  * 思维题。
  * 记录 $a$ 之和以及其偶数和奇数的数量。
  * 操作为 $0$ 时： 
```java
* 偶数加偶数，偶数数量不变；
* 偶数加奇数，奇数数量增加当前偶数的数量。
```
  * 操作为 $1$ 时： 
```java
* 奇数加偶数，奇数数量不变；
* 奇数加奇数，偶数数量增加当前奇数的数量。
```



* * *

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

    LL sum = 0;

    LL odd = 0, even = 0;

    int n, q; cin >> n >> q;
    for(int i = 0; i < n; i ++){
        LL x; cin >> x;
        if(x % 2 == 0) even ++;
        else odd ++;
        sum += x;
    }

    while(q --){
        int op, k; cin >> op >> k;
        if(op == 0){
            if(k % 2 == 0) um += even * k;
            else{
                sum += even * k;
                odd += even; even = 0;
            }
        }
        else{
            if(k % 2 == 0) sum += odd * k;
            else{
                sum += odd * k;
                even += odd; odd = 0;
            }
        }
        cout << sum << endl;
    }

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

* * *

## C. Traffic Light

* * *

[Origional Link](&lt;https://codeforces.com/contest/1744/problem/C&gt;)

**题目大意** ：

  * 给定一个长度为 $n$ 且只包含 $r,y,g$ 的字符串 $s$ 代表红绿灯的信号周期。
  * 给出当前的信号为 $c$ 表示当前的状态。
  * 求最长等待可以遇到 $g$ 的时间。



* * *

**思想** ：

  * 模拟。
  * 将 $s$ 加长，使得一个周期首尾相连。
  * 从每个信号为 $c$ 的位置开始，找到下一个为 $g$ 的位置。
  * 更新最大的区间长度。



* * *

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

    int n;
    string op;
    cin >> n >> op;
    string s; cin >> s;
    int t = s.size();
    s = s + s;
    int pos = s.find(op);
    int res = -1;
    for(int i = 0; i < t + pos + 1; i ++){
        int cnt = 0;
        if(s[i] == op[0]){
            while(s[i] != 'g' && i < s.size()){
                cnt ++; i ++;
            }
            res = max(res, cnt);
        }
    }

    cout << res << endl;

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

* * *

## D. Divisibility by 2^n

* * *

[Origional Link](&lt;https://codeforces.com/contest/1744/problem/D&gt;)

**题目大意** ：

  * 给定一个长度为 $n$ 的正整数序列 $a$，使得所有元素的乘积可以被 $2^n$ 整除。
  * 可以进行如下操作： 
```java
* 对 $a_i = a_i \times i$。
```
  * 上述操作每个位置只能进行一次。
  * 求满足题意的最少操作次数。



* * *

**思想**

  * 贪心。
  * 设 $a_i$ 乘积为 $k$，则满足 $2^n | k$ 的条件为 $k$ 因数分解中，$2$ 的因子数量大于等于 $n$。
  * 显然，当 $2$ 的因子数量不足时，使得操作数最小的方案即为优先选择 $i$ 包含 $2$ 因子数量多的位置进行操作。



* * *

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

int f(LL n){
    int cnt = 0;
    while(n % 2 == 0){
        n /= 2;
        cnt ++;
    }
    return cnt ;
}

void solve(){

    LL sum = 0;

    priority_queue&lt;int&gt; st;

    int n; cin >> n;
    for(int i = 1; i <= n; i ++){
        LL x; cin >> x;
        sum += f(x);
        st.push(f(i));
    }

    int cnt = 0;
    while(!st.empty() && sum < n){
        sum += st.top(); st.pop();
        cnt ++;
    }
    if(sum >= n) cout << cnt << endl;
    else cout << -1 << endl;

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
