---
title: "Codeforces Round #813 (Div. 2)(A~C)"
date: 2022-08-14
categories: [ALGORITHM, Q&amp;A, 模拟, 数学, Codeforces]
description: ""
---

## A. Wonderful Permutation

* * *

### 题目大意

[Origional Link](&lt;https://codeforces.com/contest/1712/problem/A#&gt;)

  * 给定长度为 $n$ 的数组 $a$，元素互不相同
  * 每次可选择 $a_i,a_j$ 进行交换
  * 求使得长度为 $k$ 的子序列之和达到最小的交换次数



* * *

### 思想

  * 对于子序列的和最小，应遵循最小排列
  * 即判断原序列中，前 $k$ 个元素，有多少满足 $a_i\le k$，满足该条件则不需要交换，否则需要交换



* * *

### 代码
    
    
    #include &lt;bits/stdc++.h&gt;
    using namespace std;
    
    #define re register
    
    const int N = 1e6 + 3;
    
    int a[N];
    
    void solve(){
    
        int n, k;
    
        cin >> n >> k;
    
        for(re int i = 1; i <= n; i ++) cin >> a[i];
    
        int cnt = 0;
    
        for(re int i = 1; i <= k; i ++) if(a[i] > k) cnt ++;
    
        cout << cnt << endl;
    
    }
    
    int main(){
    
    //  solve();
    
        int _;
        cin >> _;
    
        while(_ --){
            solve();
        }
    
        return 0;
    
    }

* * *

## B. Woeful Permutation

* * *

### 题目大意

[Origional Link](&lt;https://codeforces.com/contest/1712/problem/B&gt;)

  * 给定元素为 $1\sim n$ 的数组 $a$
  * 求使得 $lcm(1,a_1)+lcm(2,a_2)+\dots lcm(i,a_i)$ 最大的子序列



* * *

### 思想

  * 已知 $lcm(a,b) = \frac{a\times b}{gcd(a,b)}$
  * 若使得 $lcm(a,b)$ 最大，则应尽可能使得 $gcd(a,b) = 1$
  * 对于序列中的元素 $a_i=i$
  * 则有 $gcd(i,a_i + 1) = 1$
  * 故 $a _i = i +1, a_{i + 1} = i$ 时，满足题意
  * 即： 
    * $n$ 为偶数时，遵循排列：$2,1,4,3,6,5,\dots ,n,n-1$
    * $n$ 为奇数时，遵循排列：$1,3,2,5,4,7,6\dots ,n,n-1$



* * *

### 代码
    
    
    #include &lt;bits/stdc++.h&gt;
    using namespace std;
    
    #define re register
    
    void solve(){
    
        int n;
    
        cin >> n;
    
        if(n % 2 == 0){
            for(re int i = 2; i <= n; i += 2) cout << i << " " << i - 1 << " ";
        }
        else{
            cout << 1 << " ";
            for(re int i = 3; i <= n; i += 2) cout << i << " " << i - 1 << " ";
        }
    
        cout << endl;
    
    }
    
    int main(){
    
    //  solve();
    
        int _;
        cin >> _;
    
        while(_ --){
            solve();
        }
    
        return 0;
    
    }

* * *

## C. Sort Zero

* * *

### 题目大意

[Origional Link](&lt;https://codeforces.com/contest/1712/problem/C&gt;)

  * 给定长度为 $n$ 的数组 $a$
  * 每次操作，可以将所有 $a_i = x$ 的元素操作变为 $a_i = 0$
  * 求最少操作多少次，可以使得原数组元素不严格单调递增



* * *

### 思想

  * `int a[N]`存储数组元素，`set&lt;int&gt; b`存储当前枚举到`i`之前，需要将 $a_i$ 变为 $0$ 的 $x$ 值
  * 从`i = 2`开始枚举`a[i]`： 
    * 先判断`a[i]`是否在`b`中，若存在，则更新`a[i] = 0`
    * 若`a[i - 1] > a[i]`，说明需要将`a[i - 1]`更新，将`b.insert(a[i - 1])`，且要使得`i`之前所有的`a[j] == a[i - 1]`的元素更新为 $0$，且在更新时，要将`a[j] != 0`的元素也加入`b`中
  * 由于我们按顺序枚举，故在`i`之前的序列一定满足不严格单调递增，在枚举结束之后，`b`中元素个数即为操作次数



* * *

### 代码
    
    
    #include &lt;bits/stdc++.h&gt;
    using namespace std;
    
    #define re register
    
    const int N = 1e6 + 3;
    
    int a[N];
    
    set&lt;int&gt; b;
    
    void solve(){
    
        int n;
        cin >> n;
    
        for(re int i = 1; i <= n; i ++) cin >> a[i];
    
        for(re int i = 2; i <= n; i ++){
    
            if(b.count(a[i]) > 0) a[i] = 0;
    
            if(a[i - 1] > a[i]){
                b.insert(a[i - 1]);
                a[i - 1] = 0;
                for(re int j = i - 1; a[j] != 0 && j >= 1; j --){
                    b.insert(a[j]);
                    a[j] = 0;
                }
            }
    
        }
    
        cout << b.size() << endl;
    
        b.clear();
    
    }
    
    int main(){
    
    //  solve();
    
        int _;
        cin >> _;
    
        while(_ --){
            solve();
        }
    
        return 0;
    
    }

* * *

## 后记

  * $A$ 没有什么难度，但是做的太急(permutation是无重复元素的排列数组)，没有思考好规律
  * $B$ 真的是 $\color{red}{WA}$ 到飞起，怎么会有我这种笨比推出来 $gcd(i,a_i + 1) = 1$ 规律还解不出来的人，建议自己`remake`
  * $C$ 一开始思路很乱，后来发现模拟就好了，写完直接交一发就过，没什么算法难度
  * 手速场狂 $\color{red}{WA}$两道 $A,B$ `nt`题的我真是没救了，前几场着实给我打破防了，这回还好最后没放弃，继续努力吧 


