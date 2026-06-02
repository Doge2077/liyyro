---
title: "Codeforces Round #826 (Div. 3)（A~D）"
date: 2022-10-14
categories: [ALGORITHM, Q&amp;A, 模拟, Codeforces, 前缀和, 构造]
description: ""
---

## A. Compare T-Shirt Sizes

* * *

[Origional Link](&lt;https://codeforces.com/contest/1741/problem/A&gt;)

**题目大意** ：

  * 给定不同衬衫大小的尺寸编号如：$S,M,L$。
  * 除 $M$ 之外，$X$ 作为尺寸前缀代表其倍数大小。
  * 如：$XXL\gt XL,XXS\lt XS$。
  * 给定两个代表衬衫尺寸的字符串，判断衬衫大小。



* * *

**思想** ：

  * 签到题。
  * 判断模拟即可。



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
    string s1, s2;
    cin >> s1 >> s2;
    if(s1 == s2) cout << "=" << endl;
    else{
        char p1 = s1.back(), p2 = s2.back();
        int t1 = s1.size(), t2 = s2.size();
        if(p1 == 'S'){
            if(p2 == 'S'){
                if(t1 > t2) cout << "<" << endl;
                else cout << ">" << endl;
            }
            else cout << "<" << endl;
        }
        else if(p1 == 'M'){
            if(p2 == 'S') cout << ">" << endl;
            else cout << "<" << endl;
        }
        else{
            if(p2 == 'L'){
                if(t1 > t2) cout << ">" << endl;
                else cout << "<" << endl;
            }
            else cout << ">" << endl;
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

## B. Funny Permutation

* * *

[Origional Link](&lt;https://codeforces.com/contest/1741/problem/B&gt;)

**题目大意** ：

  * 给定一个 $1\sim N$ 的序列 $p$。
  * 求是否存在一种排列形式，使得： 
```java
* 对于 $p_i$ 至少存在一个相邻的元素保证他们之差不超过 $1$。
* 且保证 $p_i\ne i$。
```
  * 存在输出任意满足条件的序列，不存在输出 $-1$。



* * *

**思想** ：

  * 构造。
  * 将一个 $1\sim N$ 的序列从中间拆分，两两组合。
  * 特判 $n = 1,3$ 时不存在满足条件的排列。



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
    if(n == 1 || n == 3) cout << -1 << endl;
    else{
        int j = n;
        if(n % 2 == 0){
            for(int i = n; i >= n / 2; i --) cout << i << ' ';
            for(int i = 1; i < n / 2; i ++) cout << i << ' ';
        }
        else{
            int t = (n - 1) / 2;
            int p = n;
            for(int i = 1; i <= t; i ++){
                cout << p << ' '; p --;
            }
            for(int i = 1; i <= n - p + 1; i ++) cout << i << ' ';
        }
        cout << endl;
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

## C. Minimize the Thickness

* * *

[Origional Link](&lt;https://codeforces.com/contest/1741/problem/C&gt;)

**题目大意** ：

  * 给定一个长度为 $n$ 的数组，将其分成连续不重合的若干区间，使得各区间内部元素之和相等。
  * 求满足上述条件的切分方案下，最长的一个区间的最小可能值。



* * *

**思想** ：

  * 前缀和，模拟。
  * 从 $1$ 枚举区间长度，设当前区间的和为 $t$。
  * 每次向后枚举找到和 $t$ 相等的区间，并且更新最长的区间。
  * 当枚举到和大于 $t$ 的区间剪枝。
  * 枚举结束，判断是否切分掉了所有的区间，最后更新答案区间。



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

LL a[N];

void solve(){

    int n; cin >> n;

    for(int i = 1; i <= n; i ++){
        cin >> a[i];
        a[i] += a[i - 1];
    }

    int res = INF;

    for(int i = 1; i <= n; i ++){
        int t = a[i] - a[0];
        int p = i;
        int k = i + 1;  //当前的区间长度
        for(int j = i + 1; j <= n; j ++){
            if(a[j] - a[k - 1] == t){
                p = max(p, j - k + 1);  //最大的区间长度
                k = j + 1; 
            }
            else if(a[j] - a[k - 1] > t) break;  //剪枝
        }
        if(k != n + 1) p = INF;  //若最后内部和相等的区间没有用完，则此次切分不成立
        res = min(res, p);
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

## D. Masha and a Beautiful Tree

* * *

[Origional Link](&lt;https://codeforces.com/contest/1741/problem/D&gt;)

**题目大意** ：

  * 给定一个满二叉树（即树的叶子节点数目为 $2^n$），叶子节点的权值是 $1 - n$ 的排列，每个节点拥有不同的权值。
  * 一次操作可以交换一个子树的两个儿子，求最小化交换的操作使得叶子节点上的权值递增。



* * *

**思想** ：

  * 归并。
  * 子儿子交换的过程，类比于归并排序的过程。



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

int n, ans;
int q[N], t[N];
bool vis;

void merge_sort(int q[], int l, int r){
    if(l >= r) return ;
    int mid = l + r >> 1;
    merge_sort(q, l, mid), merge_sort(q, mid + 1, r);

    int k = 0, i = l, j = mid + 1;
    bool flag1 = 1, flag2 = 1;
    while(i <= mid && j <= r){
        if(q[i] <= q[j]) t[k ++] = q[i ++], flag2 = 0;
        else{
            t[k ++] = q[j ++];
            if(flag1) ans ++, flag1 = 0;
        }
    } 
    if(!flag2 && i <= mid) vis = 0;
    while(i <= mid) t[k ++] = q[i ++];
    if(!flag1 && j <= r) vis = 0;
    while(j <= r) t[k ++] = q[j ++];
    for(int i = l, j = 0; j <= k - 1; ) q[i ++] = t[j ++];
}

void solve(){

    cin >> n;

    vis = 1; ans = 0;
    for(int i = 0; i <= n; i ++) q[i] = t[i] = 0;

    for(int i = 1; i <= n; i ++) cin >> q[i];

    if(n == 1){
        cout << 0 << endl;
        return ;
    }

    merge_sort(q, 1, n);
    if(vis) cout << ans << endl;
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
