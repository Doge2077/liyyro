---
title: "Codeforces Round #674 (Div. 3)（A~D）"
date: 2022-10-12
categories: [ALGORITHM, Q&amp;A, Codeforces, 贪心, 前缀和, 思维]
description: ""
---

## A. Floor Number

* * *

[Origional Link](&lt;https://codeforces.com/group/gsTQwPns6J/contest/1426/problem/A&gt;)

**题目大意** ：

  * 给定目标房间编号 $n$ 及一层楼住户数量 $x$。
  * 第一层楼只有 $2$ 个住户，求目标房间所在楼层。



* * *

**思想** ：

  * 签到题。
  * $n\le2$ 时在第一层。
  * $n\gt 2$ 时： 
    * 若 $x$ 可以整除 $n-2$，则在 $\frac{n-2}{m} + 1$ 层；
    * 反之在 $\frac{n-2}{m} + 2$ 层。



* * *

**代码** ：
    
    
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
    
        int n, x;
    
        cin >> n >> x;
    
        if(n <= 2) cout << 1 << endl;
        else{
            int t = (n - 2) / x + 1;
            if((n - 2) % x != 0) t ++;
            cout << t << endl;
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

* * *

## B. Symmetric Matrix

* * *

[Origional Link](&lt;https://codeforces.com/group/gsTQwPns6J/contest/1426/problem/B&gt;)

**题目大意** ：

  * 给定 $n$ 个 $2\times 2$ 的矩阵，每个矩阵有无限多个。
  * 求这些矩阵是否可以组合成一个 $m\times m$ 的大矩阵，且使得大矩阵的元素关于主对角线对称。



* * *

**思想** ：

  * 思维题。
  * 可以构成的大前提条件是 $2$ 可以整除 $m$。 
  * 其次使得大矩阵的元素关于主对角线对称，只需要每个小矩阵的元素次对角线上的元素相同即可。



* * *

**代码** ：
    
    
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
    
        int n, m; cin >> n >> m;
    
        bool flag = 0;
    
        for(int i = 0; i < n; i ++){
            int a, b, c, d;
            cin >> a >> b >> c >> d;
            if(b == c) flag = 1;
        }
    
        if(flag && m % 2 == 0) cout << "YES" << endl;
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

* * *

## C. Increase and Copy

* * *

[Origional Link](&lt;https://codeforces.com/group/gsTQwPns6J/contest/1426/problem/C&gt;)

**题目大意** ：

  * 给定一个序列 $a = [1]$。
  * 不限次数进行如下操作： 
    * 选择 $a_i$ 使其变为 $a_i+1$；
    * 选择 $a_i$ 将其复制并加入到 $a$ 的末尾。
  * 给定一个整数 $n$，求最少经过多少次操作可以使得 $a$ 的元素之和至少是 $n$。



* * *

**思想** ：

  * 思维题。
  * 最快的方法是将 $a_i$ 不断变为 $a_i + 1$，之后不断执行复制操作，直到总和 $sum \ge n$。
  * 我们设 $a_i$ 通过 $i$ 次 $+1$ 操作最后得到的数为 $x$，复制 $x$ 共 $j$ 次后得到大于等于 $n$ 的数，即： 
    * $x \times (j+1) \ge n$
  * 求 $i+j$ 的最小值等价于先求 $x + (j+1) $ 的最小值，显然地，当 $x$ 和 $j + 1$ 尽可能接近 $\sqrt{n}$ 时可以使得 $x+(j+1)$ 最小。
  * 综上所述，我们需要找到尽可能接近 $\sqrt{n}$ 的最大整数。



* * *

**代码** ：
    
    
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
        int t = sqrt(n);
        if(t * t == n) cout << 2 * (t - 1) << endl;
        else if(t * (t + 1) >= n) cout << 2 * t - 1 << endl;
        else cout << 2 * t  << endl;
    
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

* * *

## D. Non-zero Segments

* * *

[Origional Link](&lt;https://codeforces.com/group/gsTQwPns6J/contest/1426/problem/D&gt;)

**题目大意** ：

  * 给定一个序列 $a$，可以在任意相邻对中添加任意大小的数，最终使得不存在一个子序列的和为 $0$ 。
  * 求最少的添加次数。



* * *

**思想** ;

  * 前缀和，贪心。
  * 破坏所有连续的区间和为 $0$ 的区间，可以使用前缀和预处理区间和。
  * 当区间 `[l,r]` 和为 $0$ 时，有 `a[l - 1] = a[r]`。
  * 从左往右扫描每个区间的左端点，用 `map&lt;LL, int&gt; st` 存储出现过的前缀。
  * 那么当出现相同的前缀和，说明存在和为 $0$ 的子序列，此时需要在其区间加上一个数。
  * 保证在此之前的所有子序列没有存在和为 $0$ 的前缀，则当前位置改变，其左边区间可以不再考虑，记录操作并且清空 `st`。
  * 注意，由于子区间有可能在端点处重合，这种情况不属于有重复部分，所以清空 `st` 以后还需要插入当前位置左侧一位置的前缀和。



* * *

**代码** ：
    
    
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
    
    void solve(){
    
        map&lt;LL, int&gt; st; 
    
        int n; cin >> n;
        for(int i = 1; i <= n; i ++){
            cin >> a[i];
            a[i] += a[i - 1];
        }
    
        LL cnt = 0;
    
        for(int i = 1; i <= n; i ++){
            if(st[a[i]] > 0){
                cnt ++;
                st.clear();
            }
            st[a[i - 1]] ++;
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
