---
title: "Codeforces Round #784 (Div. 4)（A~F）"
date: 2022-10-21
categories: [ALGORITHM, Q&amp;A, 模拟, 离散化, Codeforces, 思维]
description: ""
---

## A. Division?

* * *

[Origional Link](&lt;https://codeforces.com/group/50jVAfUiqO/contest/1669/problem/A&gt;)

**题目大意**

  * 按照分数区间输出对应的难度。



* * *

**思想** ：

  * 签到题。



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
        cout << "Division ";
        if(n <= 1399) cout << 4 << endl;
        else if(n <= 1599 && n >= 1400) cout << 3 << endl;
        else if(n >= 1600 && n <= 1899) cout << 2 << endl;
        else cout << 1 << endl;
    
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

## B. Triple

* * *

[Origional Link](&lt;https://codeforces.com/group/50jVAfUiqO/contest/1669/problem/B&gt;)

**题目大意** ：

  * 判断一个序列是否存在某个数至少出现了三次。



* * *

**思想** ：

  * 签到题。
  * 用 `map&lt;int,int&gt;` 存出现次数。



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
        int flag = -1;
    
        map&lt;int, int&gt; st;
    
        for(int i = 0; i < n; i ++){
            int x; cin >> x;
            st[x] ++;
            if(st[x] >= 3) flag = x;
        }
    
        cout << flag << endl;
    
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

## C. Odd/Even Increments

* * *

[Origional Link](&lt;https://codeforces.com/group/50jVAfUiqO/contest/1669/problem/C&gt;)

**题目大意** ：

  * 给定一个序列 $a$，对于其中的元素可以进行如下操作： 
    * 将下标为奇数的元素 $a_i$ 变为 $a_i+ 1$。
    * 将下标为偶数的元素 $a_i$ 变为 $a_i + 1$。
  * 判断如上述操作之后，序列是否可以变成只含有奇数或者只含有偶数的序列。



* * *

**思想** ：

  * 签到题。
  * 判断下标为奇数的元素的奇数个数和偶数个数，要么全为奇数，要么全是偶数。
  * 判断下标为偶数的元素的奇数个数和偶数个数，要么全为奇数，要么全是偶数。
  * 只有上述两个条件都满足时，才能符合题意。



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
        int odd1 = 0, even1 = 0;
        int odd2 = 0, even2 = 0;
        for(int i = 0; i < n; i ++){
            int x; cin >> x;
            if(i % 2 == 0){
                if(x % 2 == 0) even2 ++;
                else odd2 ++;
            }
            else{
                if(x % 2 == 0) even1 ++;
                else odd1 ++;
            }
        }
    
        if((odd1 == 0 || even1 == 0) && (odd2 == 0 || even2 == 0)) cout << "YES" << endl;
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

## D. Colorful Stamp

* * *

[Origional Link](&lt;https://codeforces.com/group/50jVAfUiqO/contest/1669/problem/D&gt;)

**题目大意** ：

  * 一个只包含 $W$ 字符串 $S$ 可以进行如下变换： 
    * 将任意相邻的两个字符变为 $RB$ 或 $BR$。
  * 现给出一个变换之后的字符串 $S$，问是否可以从最初全是 $W$ 的状态转换为当前状态。



* * *

**思想** ：

  * 模拟。
  * 特判 $S$ 长度为 $1$ 和 $2$ 的情况。
  * 其余情况我们以 $S$ 中的每一个 $W$ 来切割，判断字串的状态： 
    * 当字串长度小于 $2$ 时，只有 $RB$ 或 $BR$ 符合条件；
    * 当字串长度大于 $2$ 时，只含有 $R$ 或者只含有 $B$ 时不符合条件.
  * 模拟完成后，特判被最后一个 $W$ 分割之后剩余的字串即可。



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
        string s; cin >> s;
    
        //特判两种情况
        if(s.size() == 1){
            if(s == "W") cout << "YES" << endl;
            else cout << "NO" << endl;
        }
        else if(s.size() == 2){
            if(s == "RB" || s == "WW" || s == "BR") cout << "YES" << endl;
            else cout << "NO" << endl;
        }
        else{
            //将 S 以 W 进行分割，判断每个 W 分割的字串
            int r = 0, b = 0;
            for(int i = 0; i < n; i ++){
                if(s[i] == 'W'){  //当遇到 W 则判断截至到上一个 W 的字串的情况
                    if(r + b < 2){  //小于 2 时
                        if(r == b && r == 0) continue;  //上一个字串不含 RB 跳过
                        else{
                            cout << "NO" << endl;  //否则无法变成，直接返回
                            return ;
                        }
                    }
                    else{  //大于 2 时
                        if(r == 0 || b == 0){  //只含有 R 或者只含有 B 无法满足，直接返回
                            cout << "NO" << endl;
                            return ;
                        }
                        else r = b = 0;  //否则可以满足，此时重置字串状态
                    }
                }
                else{  //没遇到 W 更新字串状态
                    if(s[i] == 'R') r ++;
                    else b ++;
                }
            }
    
            if(r + b < 2){  //扫完 S 剩余的最后一个 W 切割的字串
                if(r == b && b == 0) cout << "YES" << endl;
                else cout << "NO" << endl;
            }
            else{
                if(r == 0 || b == 0) cout << "NO" << endl;
                else cout << "YES" << endl;
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

* * *

## E. 2-Letter Strings

* * *

[Origional Link](&lt;https://codeforces.com/group/50jVAfUiqO/contest/1669/problem/E&gt;)

**题目大意** ：

  * 给定 $n$ 个长度为 $2$ 的只含有小写字母 $a\sim k$ 的字符串 $S$。
  * 判断有多少对这样的字符串，满足其中一个对应位置的字母不同，而另一个位置相同。



* * *

**思想** ：

  * 离散化。
  * 记录所有相同的 $S$ 的数量。
  * 每次加入新的 $S$ 枚举进行统计。
  * 字符只有 $a\sim k$，组合共 $11^2$ 种组合，最坏的情况为 $11^2\times 2\times 10^5$ ，实际远小于该时间复杂度。



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
    
    bool check(string s1, string s2){
        if(s1[0] == s2[0] && s1[1] != s2[1]) return 1;
        if(s1[0] != s2[0] && s1[1] == s2[1]) return 1;
        return 0;
    }
    
    void solve(){
    
        LL sum = 0;
    
        map&lt;string, LL&gt; st;
    
        int n; cin >> n;
        for(int i = 0; i < n; i ++){
            string s; cin >> s;
            st[s] ++;
            for(auto &p : st){
                if(check(p.fi, s)) sum += p.se;
            }
        }
    
        cout << sum << endl;
    
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

* * *

## F. Eating Candies

* * *

[Origional Link](&lt;https://codeforces.com/group/50jVAfUiqO/contest/1669/problem/F&gt;)

**题目大意**

  * 给定若干个糖及其重量 $w_i$。
  * 两个人从两头开始吃，不能跳过顺序。
  * 保证两人吃到的重量相同的情况下，最多能吃掉几颗糖。



* * *

**思想** ：

  * 双指针，模拟。
  * 分别记录两人当前吃掉的糖的重量。
  * 当前一个人吃掉的重量大于后一个人，则后一个人吃糖（指针移动），反之亦然。
  * 每当吃掉的糖重量相等时，更新吃掉的糖果的数量。



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
    
        int n; cin >> n;
        for(int i = 1; i <= n; i ++) cin >> a[i];
    
        int l = 1, r = n;
    
        LL sum = 0;
    
        LL x = 0, y = 0;
    
        while(l <= r){
            if(x == y) sum = l + n - r - 1;
            if(x <= y) x += a[l ++];
            else y += a[r --];
        }
        if(x == y) sum = n;
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
