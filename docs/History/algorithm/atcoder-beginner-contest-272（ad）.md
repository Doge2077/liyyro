---
title: "AtCoder Beginner Contest 272（A~D）"
date: 2022-10-10
categories: [ALGORITHM, Q&amp;A, 模拟, BFS, AtCoder, 思维]
description: ""
---

## A. Integer Sum

* * *

[Origional Link](&lt;https://atcoder.jp/contests/abc272/tasks/abc272_a&gt;)

**题目大意** ：

  * $N$ 个数求和。



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

    LL sum = 0;

    while(n --){
        LL x; cin >> x;
        sum += x;
    }

    cout << sum << endl;

    return ;

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

## B. Everyone is Friends

* * *

[Origional Link](&lt;https://atcoder.jp/contests/abc272/tasks/abc272_b&gt;)

**题目大意** ：

  * 给定编号 $1\sim N$ 的人和编号 $1\sim M$ 的聚会。
  * 第 $i$ 行第一个数为 $k_i$ 代表参加编号为 $M_i$ 的人共有 $k_i$ 个，之后是 $k_i$ 个参加该聚会的人的编号。
  * 问是否存在某两个人没有一起参加某个聚会。



* * *

**思想** ：

  * 模拟题。
  * 某两个人没有一起参加某个聚会，具体地，指编号为 $i$ 的人是否和除了自己本身之外所有编号的人参加了至少一次聚会。
  * 数据范围很小，可以用邻接矩阵来存储编号为 $i$ 和编号为 $j$ 的人是否一起参加过聚会的状态。
  * 最后扫一遍状态矩阵，判断是否满足题意即可。



* * *
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

const int N = 200;
const int INF = 0x3f3f3f3f, mod = 1e9 + 7;
const double eps = 1e-6, PI = acos(-1);

int n, m;

int vis[N][N];

void solve(){

    cin >> n >> m;

    for(int i = 1; i <= m; i ++){
        int t; cin >> t;
        int num[N];
        for(int j = 0; j < t; j ++) cin >> num[j];  //读入参加该聚会的人的编号

        for(int j = 0; j < t; j ++){
            for(int k = 0; k < t; k ++){
                if(k != j) vis[num[j]][num[k]] = 1;  //去除自己本身，所有参加该聚会的人两两组合。
            }
        }
    }

    bool flag = 1;

    for(int i = 1; i <= n; i ++){
        for(int j = i + 1; j <= n; j ++){
            if(vis[i][j] == 0){
                flag = 0;
                break;
            }
        }
        if(!flag) break;
    }

    if(flag) cout << "Yes" << endl;
    else cout << "No" << endl;

    return ;

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

## C. Max Even

* * *

[Origional Link](&lt;https://atcoder.jp/contests/abc272/tasks/abc272_c&gt;)

**题目大意** ：

  * 给定一个长度为 $N$ 的非负整数序列 $A = (A_1,A_2,\dots,A_N)$。
  * 求序列中某两个数之和为偶数的最大值，若不存在输出 $-1$。



* * *

**思想** ：

  * 思维题。
  * 维护最大和次大的两个奇数和偶数的值即可。
  * 不存在的条件是无法使两数相加为偶数的情况。



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

const int N = 200;
const int INF = 0x3f3f3f3f, mod = 1e9 + 7;
const double eps = 1e-6, PI = acos(-1);

LL o_1, o_2, e_1, e_2;

void solve(){

    o_1 = o_2 = e_1 = e_2 = -1;  //初始化为 -1

    int n; cin >> n;

    int O = 0, E = 0;  //O为当前维护偶数的个数，E同理

    while(n --){
        LL x; cin >> x;
        if(x % 2 == 0){  //偶数
            if(o_1 == -1 && o_2 == -1) o_1 = x, O ++;  //第一个偶数出现
            else if(o_1 != -1 && o_2 == -1) o_2 = x, O ++;  //第二个偶数出现
            else{  //第三个及之后的偶数出现
                if(x > o_2) o_2 = x;  //x大于较小偶数则更新o_2
                if(o_1 < o_2) swap(o_1, o_2);  //维护o_1为最大的偶数
            }
        }
        else{  //奇数同理
            if(e_1 == -1 && e_2 == -1) e_1 = x, E ++;
            else if(e_1 != -1 && e_2 == -1) e_2 = x, E ++;
            else{
                if(x > e_2) e_2 = x;
                if(e_1 < e_2) swap(e_1, e_2);
            }
        }
    }

    if(O == 2 && E == 2){  //两个偶数相加为偶数，两个奇数相加为偶数，两种情况取最大
        cout << max(o_1 + o_2, e_1 + e_2) << endl;
    }
    else if(O == 2 && E != 2){  //只存在两个偶数加和的情况
        cout << o_1 + o_2 << endl;
    }
    else if(O != 2 && E == 2){   //只存在两个奇数加和的情况
        cout << e_1 + e_2 << endl;
    }
    else cout << -1 << endl;  //不存在的情况

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

## D. Root M Leaper

* * *

[Origional Link](&lt;https://atcoder.jp/contests/abc272/tasks/abc272_d&gt;)

**题目大意** ：

  * 存在 $N\times N$ 的矩阵，给定正整数 $M$。
  * 可以执行如下操作数次： 
```java
* 从当前坐标 $(i,j)$ 移动到 $(k,l)$，当且仅当 $\sqrt{(i-k)^2+(j-l)^2}=\sqrt{M}$ 时。
```
  * 从 $(1,1)$ 开始执行上述操作，输出到达某点执行上述操作的最少步数，若无法走到则输出 $-1$。



**思想** ：

  * `BFS` 搜索，难点在于移动的条件如何判断。
  * 我们需要进行枚举查找对于 $(i,j)$ 满足移动的点的偏移量，从而构建偏移量数组。
  * 即使 $M$ 的值再大，我们移动的范围也不会超过 $N\times N$，故在初始化距离的同时进行计算。
  * 设当前坐标为 $(0,0)$（虽然不在矩阵范围内，但方便直接计算偏移量），我们构建偏移量数组的条件为：`i * i + j * j == m`，其中 $i,j$ 的偏移是双向的，即满足该条件的偏移量实际为 ${(i,j),(-i,j),(i,-j),(-i,-j) }$。
  * 最后套用 `BFS` 搜索最小步数即可。



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

const int N = 505;
const int INF = 0x3f3f3f3f, mod = 1e9 + 7;
const double eps = 1e-6, PI = acos(-1);

int n, m;

int ans[N][N];  //记录步数，初始化为-1

bool vis[N][N];  //标记是否走过该点

vector&lt;PII&gt; d;  //偏移量数组

void bfs(int l, int r){

    vis[l][r] = 1;  //标记起始点已经走过
    ans[l][r] = 0;  //起始点的不少恒为0

    queue&lt;PII&gt; st;

    st.push({l, r});

    while(!st.empty()){
        auto p = st.front(); st.pop();
        for(int i = 0; i < d.size(); i ++){
            int x = p.fi + d[i].fi, y = p.se + d[i].se;
            if(x >= 1 && x <= n && y >= 1 && y <= n & !vis[x][y]){  //下一步在矩阵范围内且没有走过
                ans[x][y] = ans[p.fi][p.se] + 1;  //步数为上一个格子的步数+1
                vis[x][y] = 1;
                st.push({x, y});
            }
        }
    }

}

void solve(){

    cin >> n >> m;

    for(int i = 0; i <= n; i ++){
        for(int j = 0; j <= n; j ++){
            ans[i][j] = -1;
            if(i * i + j * j == m){  //初始化偏移量
                d.push_back({i, j});
                d.push_back({i, -j});
                d.push_back({-i, j});
                d.push_back({-i, -j});
            }
        }
    }

    bfs(1, 1);  //从(1,1)开始搜索

    for(int i = 1; i <= n; i ++){
        for(int j = 1; j <= n; j ++){
            cout << ans[i][j] << ' ';
        }
        cout << endl;
    }

    return ;

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
