---
title: "AtCoder Beginner Contest 284（A~F）"
date: 2023-02-02
categories: [ALGORITHM, Q&amp;A, 并查集, AtCoder, 字符串哈希]
description: ""
---

## A - Sequence of Strings

* * *

[Original Link](&lt;https://atcoder.jp/contests/abc284/tasks/abc284_a&gt;)

**题目大意** ：

  * 输入 `N` 个字符串，倒序输出。



* * *

**思想** ：

  * 签到题。



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

string s[N];

void solve(){

    int n; cin >> n;
    for(int i = 0; i < n; i ++) cin >> s[i];
    for(int i = n - 1; i >= 0; i --) cout << s[i] << endl;

}

int main(){

    IOS;

    int _ = 1;

    // cin >> _;

    while(_ --){
        solve();
    }

    return 0;

}
```

* * *

## B - Multi Test Cases

* * *

[Original Link](&lt;https://atcoder.jp/contests/abc284/tasks/abc284_b&gt;)

**题目大意** ：

  * 统计一组数中的奇数个数。



* * *

**思想** ：

  * 签到题。



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

    int n; cin >> n;
    int cnt = 0;
    for(int i = 0; i < n; i ++){
        int x; cin >> x;
        if(x % 2 != 0) cnt ++;
    }
    cout << cnt << endl;
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

## C - Count Connected Components

* * *

[Original Link](&lt;https://atcoder.jp/contests/abc284/tasks/abc284_c&gt;)

**题目大意** ：

  * 给定一个无向图。
  * 求连通块数量。



* * *

**思想** ：

  * 并查集。



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

// const int N = 1e6 + 3;
const int INF = 0x3f3f3f3f, mod = 1e9 + 7;
const double eps = 1e-6, PI = acos(-1);

const int N = 500;

int g[N]; 

int n, m;

int cnt = 0;

int find(int u){
    if(g[u] != u) g[u] = find(g[u]);
    return g[u];
}

void solve(){

    cin >> n >> m;
    for(int i = 1; i <= n; i ++) g[i] = i;  //初始化
    for(int i = 1; i <= m; i ++){
        int a, b; cin >> a >> b;
        g[find(a)] = find(b);
    }
    for(int i = 1; i <= n; i ++){
        if(g[i] == i) cnt ++;
    }
    cout << cnt << endl;

}

int main(){

    IOS;

    int _ = 1;

    // cin >> _;

    while(_ --){
        solve();
    }

    return 0;

}
```

* * *

## D - Happy New Year 2023

* * *

[Original Link](&lt;https://atcoder.jp/contests/abc284/tasks/abc284_d&gt;)

**题目大意** ：

  * 给定一个整数 $N$。
  * 保证 $N=p^2q$，其中 $p,q$ 均为质数且 $p\ne q$。
  * 求满足条件的 $p,q$。



* * *

**思想** ：

  * **算术基本定理** ：任何一个大于$1$的自然数 $N$，如果 $N$ 不为质数，那么 $N$ 可以唯一分解成有限个质数的乘积 $N=p_1^{a_1}\times p_2^{a_2}\dots\times p_i^{a_k}$，且最多只有一个大于 $\sqrt{n}$ 的质因子。



**法一** ：

  * 可以选择线性筛预处理素数表，然后从小到大枚举不超过 $\sqrt[3]{N}$ 的素数判断即可。



**法二** ：

  * 从 $i=2$ 开始枚举因子，当枚举到 `N % i == 0` 时，$i$ 必为 $N$ 的一个因子。
  * 则 $i$ 不是 $N$ 的质因子 $q$ 就是平方因子 $q$。
  * 当 `(N / i) % i == 0` 时，说明 `i` 为平方因子 $q$，否则为质因子 `p`。



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
    LL x; cin >> x;
    for(LL i = 2; i < x ; i ++){
        if(x % i == 0){
            if((x / i) % i == 0) cout << i << ' ' << x / (i * i) << endl;
            else cout << (LL)sqrtl(x / i) << ' ' << i << endl;
            return ;
        }
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

## E - Count Simple Paths

* * *

[Original Link](&lt;https://atcoder.jp/contests/abc284/tasks/abc284_e&gt;)

**题目大意** ：

  * 给定一个 $N$ 个顶点，$M $条边的无向图。
  * 求从点 $1$ 开始，简单路径（没有重复顶点的路径）的数量 $K$。
  * 答案取 $min(K, 1\times 10^6)$。



* * *

**思想** ：

  * 图的深度优先遍历。
  * 遇到可走的路径，数量增加 $1$。
  * 超过 $10^6$ 退出，



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

const int N = 2e5 + 3;
const int INF = 0x3f3f3f3f, mod = 1e9 + 7;
const double eps = 1e-6, PI = acos(-1);

vector&lt;int&gt; g[N];
bool vis[N];

LL cnt = 0;

void dfs(int u){
    if(cnt > 1e6) return ;
    vis[u] = 1;
    cnt ++;
    for(int i = 0; i < g[u].size(); i ++){
        if(vis[g[u][i]]) continue;
        vis[g[u][i]] = 1;
        dfs(g[u][i]);
        vis[g[u][i]] = 0;
    }
}

void solve(){
    int n, m; cin >> n >> m;
    for(int i = 0; i < m; i ++){
        int a, b; cin >> a >> b;
        g[a].push_back(b);
        g[b].push_back(a);
    }
    dfs(1);
    cout << min(cnt, (LL)1000000) << endl;
}

int main(){

    IOS;

    int _ = 1;

    // cin >> _;

    while(_ --){
        solve();
    }

    return 0;

}
```

* * *

## F - ABCBAC

* * *

[Original Link](&lt;https://atcoder.jp/contests/abc284/tasks/abc284_f&gt;)

**题目大意** ：

  * 已知一个长度为 $N$ 的字符串 $S$ 和一个整数 $i(0\le i \le N)$。
  * 定义运算 $f_i(S)$ 链接的字符串如下： 
```java
* $S$ 的前 $i$ 个字符。
* $S$ 的翻转。 
* $S$ 的最后 $(N-i)$ 个字符。
```
  * 若 `S = "abc", i = 2`，则 $f_i(S) = $`"abcbac"`。
  * 现给出某个字符串 $S$ 的长度 $N$ 和经过 $f_i(S)$ 的结果。
  * 求原始字符串 $S$ 和 $i$ 的值。



* * *

**思想** ：

  * 字符串哈希。
  * 枚举 $i$，判断 $1 \sim i$ 和 $i + N + 1 \sim 2\times N$ 拼接成的字符串与 $i + 1 \sim N + i$ 翻转后的字符串是否相同即可。



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
typedef unsigned long long ULL;

typedef pair&lt;int, int&gt; PII;
typedef pair&lt;LL, LL&gt; PLL;

// const int N = 1e6 + 3;
// const int INF = 0x3f3f3f3f, mod = 1e9 + 7;
const double eps = 1e-6, PI = acos(-1);

const ULL N = 2e6 + 9;
const int hash_cnt = 2; //哈希次数

int n;
string s;

ULL Prime[] = {1998585857ul,23333333333ul};
ULL base[] = {131, 146527, 19260817, 91815541}; // 字符集大小，进制数
ULL mod[] = {1000000007, 29123,998244353,1000000009,4294967291ull}; // 模数
ULL h1[N][hash_cnt], h2[N][hash_cnt], p[N][hash_cnt];

//初始化哈希
void initHash(ULL n, ULL cnt){
    p[0][cnt] = 1;
    for(int i = 1; i <= n; ++ i) p[i][cnt] = p[i - 1][cnt] * base[cnt] % mod[cnt];
    for(int i = 1; i <= n; ++ i) h1[i][cnt] = (h1[i - 1][cnt] * base[cnt] % mod[cnt] + s[i]) % mod[cnt]; // 正序hash
    for(int i = n; i >= 1; -- i) h2[i][cnt] = (h2[i + 1][cnt] * base[cnt] % mod[cnt] + s[i]) % mod[cnt]; // 逆序hash
}

//正序HASH
ULL getHash1(ULL id, ULL l, ULL r){
    return (h1[r][id] - h1[l - 1][id] * p[r - l + 1][id] % mod[id] + mod[id]) % mod[id];
}

//逆序HASH
ULL getHash2(ULL id, ULL l, ULL r){
    return (h2[l][id] - h2[r + 1][id] * p[r - l + 1][id] % mod[id] + mod[id]) % mod[id];
}

//判断区间正逆序是否相等，如果区间正逆序哈希值一样，则回文；
bool isRe(ULL id, ULL l,ULL r){
    return getHash1(id, l, r) == getHash2(id, l, r);
}

void solve(){

    cin >> n >> s;
    s = " " + s;
    initHash(2 * n, 0);
    for(int i = 0; i <= n; i ++ ){
        ULL sum1 = ((getHash1(0, 1, i) * p[n - i][0] % mod[0] + getHash1(0, n + i + 1, 2 * n)) % mod[0]);
        ULL sum2 = getHash2(0, i + 1, n + i);
        if(sum1 == sum2){
            string st = s.substr(i + 1, n);
            reverse(st.begin(), st.end());
            cout << st << endl;
            cout << i << endl;
            return;
        }
    }
    cout << -1 << endl;
}

int main(){

    IOS;

    int _ = 1;

    // cin >> _;

    while(_ --){
        solve();
    }

    return 0;

}
```
