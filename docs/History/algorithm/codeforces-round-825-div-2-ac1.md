---
title: "Codeforces Round #825 (Div. 2) (A~C1)"
date: 2022-10-12
categories: [ALGORITHM, Q&amp;A, 双指针, 数学, Codeforces, 构造]
description: ""
---

## A. Make A Equal to B

* * *

[Origional Link](&lt;https://codeforces.com/contest/1736/problem/A&gt;)

**题目大意** ：

  * 给定只含 $0,1$ 的序列 $a,b$。
  * 对序列 $a$ 不限次数执行如下操作： 
    * 将 $a_i$ 变为 $a_i - 1$ 。
    * 将 $a$ 按照任意顺序重新排列。
  * 求最少几步可以得到和 $b$ 相同的序列 $a$。



* * *

**思想** ： 

  * 思维题。
  * 分为两种情况讨论：不排序 $a$ 直接操作和先排序 $a$ 再操作的情况。 
  * 同时遍历一遍 $a$ 和 $b$，记录 `a[i] != b[i]` 的次数即为不排序 $a$ 直接操作时，需要改变 $a_i$ 的步数，记为 $cnt$。
  * 将 $a$ 进行排序，尽可能的一一对应 $b$，由于对排序无要求，则只需记录 $a$ 和 $b$ 中相同元素出现的次数，分别设为 $t,p$。 
  * 那么在进行一次排序后，最少改变 $a$ 的步数即为 `abs(t - 1)`。
  * 综合上述两种情况最少步数为 `min(cnt, abs(t - p) + 1)`



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
    
    const int N = 1e6 + 10;
    const int INF = 0x3f3f3f3f, mod = 1e9 + 7;
    const double eps = 1e-6, PI = acos(-1);
    
    int a[N], b[N];
    
    void solve(){
    
        int n; cin >> n;
    
        int p = 0, t = 0;
        for(int i = 0; i < n; i ++){
            cin >> a[i];
            if(a[i] == 1) p ++;
        }
    
        for(int i = 0; i < n; i ++){
            cin >> b[i];
            if(b[i] == 1) t ++;
        }
    
        int cnt = 0;
        for(int i = 0; i < n; i ++){
            if(a[i] != b[i]) cnt ++;
        } 
    
        cout << min(cnt, abs(t - p) + 1) << endl;
    
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

## B. Playing with GCD

* * *

[Origional Link](&lt;https://codeforces.com/contest/1736/problem/B&gt;)

**题目大意** ：

  * 给定一个长度为 $n$ 的序列 $a$。
  * 问是否存在一个 $n + 1$ 长度的序列 $b$，使得 [latex]a_i= gcd(b_i,b_{i+1}),1\le i \le n[/latex]。



* * *

**思想** ：

  * 数学推理，构造。
  * 当 $n\le2$ 时一定存在 $b$ 成立。
  * 当 $n \gt 2$ 时，设 $2\le i \le n-2$，若 $b$ 存在，必满足： 
    * [latex]b_i=lcm(a_{i-1},a_i),b_{i+1} = lcm(a_i,a_{i+1})[/latex]。
    * 且保证 [latex]a_i=gcd(b_i,b_{i+1})[/latex]。
  * 实际上 $a_1$ 的 $b_1$ 和 [latex]a_n[/latex] 的 [latex]b_{n+1}[/latex] 是一定存在的。



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
    
    const int N = 1e6 + 10;
    const int INF = 0x3f3f3f3f, mod = 1e9 + 7;
    const double eps = 1e-6, PI = acos(-1);
    
    LL gcd(LL a, LL b){
        return b ? gcd(b, a % b) : a;
    }
    
    int a[N];
    
    void solve(){
    
        int n; cin >> n;
        for(int i = 0; i < n; i ++) cin >> a[i];
    
        bool flag = 1;
    
        if(n > 2){
            int b = a[0] * a[1] / gcd(a[0], a[1]);
    
            for(int i = 1; i + 1 < n; i ++){
                int t = a[i] * a[i + 1] / gcd(a[i], a[i + 1]);
                if(gcd(b, t) != a[i]){
                    flag = 0;
                    break;
                }
                else b = t;
            }
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

* * *

## C1. Good Subarrays (Easy Version)

* * *

[Origional Link](&lt;https://codeforces.com/contest/1736/problem/C1&gt;)

**题目大意** ：

  * 给定一个长度为 $n$ 的序列 $b$。
  * 对于一个区间 $(l,r),1\le l \le r \le n$ 满足 $b_i\ge i,l\le i \le r$，则称该区间为一个好区间。
  * 求序列 $b$ 中的好区间数量。



* * *

**思想**

  * 双指针。
  * 定义两个指针 `i` 和 `j`，`i` 表示以`i` 为起点的序列的数量，`j` 表示从`i`开始的最长序列的位置。
  * 当 `j` 是第一个不符合条件的位置时，则当前符合条件的区间长度为 `j - i`。
  * 每次 `i` 向右走一格，显然起点后移，原来符合条件的位置同样符合条件，因此此时 `j` 不需要左移，继续右移即可。
  * 统计每次 `j` 不满足条件时区间长度之和即可。



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
    
        int n; cin >> n;
        for(int i = 1; i <= n; i ++) cin >> a[i];
    
        LL sum = 0;
        for(int i = 1, j = 1; i <= n; i ++){
            while(j <= n && a[j] >= j - i + 1){
                sum += j - i + 1;
                j ++;
            }
        }
    
        cout << sum << endl;
    
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
