---
title: "AtCoder Beginner Contest 261 (A·B·C·D)"
date: 2022-07-25
categories: [ALGORITHM, Q&amp;A, 模拟, AtCoder, DP]
description: ""
---

* * *

## A - Intersection

* * *

### 题目大意

[Originoal Link](&lt;https://atcoder.jp/contests/abc261/tasks/abc261_a&gt;)

给定两个染色区间的端点$L_1,R_1,L_2,R_2$，求同时染上两种颜色的区间长度

* * *

### 思想

  * 数据范围小，暴力枚举区间
  * 遍历两个区间，用`res[i]`记录被染色的情况
  * 遍历染色后的区间，计算区间长度



* * *

### 代码
```java


#include &lt;bits/stdc++.h&gt;
using namespace std;

const int N = 1e6 + 10;

int res[N];

int main(){

    int a, b, c, d;

    cin >> a >> b >> c >> d;

    for(int i = a; i <= b; i ++) res[i]++;

    for(int i = c; i <= d; i ++) res[i]++;

    int cnt = 0;
    for(int i = 0; i <= 200; i ++) if(res[i] == 2) cnt++;

    if(cnt) cout << cnt - 1 << endl;
    else cout << 0 << endl;

    return 0;

}
```

* * *

## B - Tournament Result

* * *

### 题目大意

[Origional Link](&lt;https://atcoder.jp/contests/abc261/tasks/abc261_b&gt;)

给定$N\times N$的表，单元$A_{i,j}$记录了+$i$与$j$的对局输赢平的三种情况，若记录有冲突说明该表不正确

* * *

### 思想

  * 遍历表格，遍历$i$行，每一行从$j = i + 1$列开始
  * 判断$A _{i,j}$和$A_{j,i}$的记录是否符合事实
  * 不符合事实进行标记并退出



* * *

### 代码
```java


#include &lt;bits/stdc++.h&gt;
using namespace std;

const int N = 1010;

char mp[N][N];

int n;

int main(){

    cin >> n;

    for(int i = 1; i <= n; i ++){
        for(int j = 1; j <= n; j++) cin >> mp[i][j];
    }

    bool flag = 1;
    for(int i = 1; i <= n; i ++){
        for(int j = i + 1; j <= n; j ++){
            if(mp[i][j] == 'D' && mp[j][i] != 'D'){
                flag = 0;
                break;
            }
            else if(mp[i][j] == 'W' && mp[j][i] != 'L'){
                flag = 0;
                break;
            }
            else if(mp[i][j] == 'L' && mp[j][i] != 'W'){
                flag = 0;
                break;
            }
        }
        if(!flag) break;
    }

    if(flag) cout << "correct" << endl;
    else cout << "incorrect" << endl;

    return 0;

}
```

* * *

## C - NewFolder(1)

* * *

### 题目大意

[Origional Link](&lt;https://atcoder.jp/contests/abc261/tasks/abc261_c&gt;)

给定$N$个`string`类型的$S$串，按照给出$S$的顺序，对于总共出现过$m$次$S_i$，若当前的$S_i$第一次出现，输出$S_i$，否则输出$S_i(u-1)$，$u$表示第几次出现

* * *

### 思想

  * `string s[N]`存储读入$S$的顺序
  * `map&lt;string,int&gt; a,`进行记录当前的$S_i$出现了多少次
  * 遍历`s[N]`，使得`a[s[i]]++`，若`a[s[i]] - 1 == 0`说明是第一次出现



* * *

### 代码
```java


#include &lt;bits/stdc++.h&gt;
using namespace std;

map&lt;string,int&gt; a;

int n;

const int N = 1e6 + 3;

string s[N];

int main(){

    cin >> n;

    for(int i = 0; i < n; i ++) cin >> s[i];

    for(int i = 0; i < n; i ++){

        a[s[i]]++;
        int t = a[s[i]] - 1;
        if(t != 0){
            cout << s[i] << '(' << t << ')' << endl;
        }
        else cout << s[i] << endl;

    }

    return 0;

}
```

* * *

## D - Flipping and Bonus

* * *

### 题目大意

[Origional Link](&lt;https://atcoder.jp/contests/abc261/tasks/abc261_d&gt;)

投掷硬币为正面，计数器增加，反之计数器清零，给定$N$次投掷硬币为正面得到的钱$X_i$，给定$M$个奖励规则，若计数器的数值达到$C_i$，将获得$Y_i$的奖励，求如何使得得到的钱最多

* * *

### 思想

  * `a[N]`记录$X_i$，`b[N]`记录$Y_i$
  * 状态表示：`dp[i][j]`表示前`i`次投掷，当前计数器值为`j`时得到的钱
  * 状态计算： 
```java
* 若投掷结果为正：则`dp[i][j] = dp[i - 1][j - 1] + a[i] + b[j]`
* 反之计数器清零，更新之后的结果：`dp[i][0] = max(dp[i][0],dp[i - 1][j])`
```
  * 注意开`long long`



* * *

### 代码
```java


#include &lt;bits/stdc++.h&gt;
using namespace std;

typedef long long LL;

LL n,m;

const LL N = 5010;

LL dp[N][N];

LL a[N];
LL b[N];

int main(){

    cin >> n >> m;

    for(int i = 1; i <= n; i ++) cin >> a[i];

    for(int i = 0; i < m; i ++){
        int x, y;
        cin >> x >> y;
        b[x] = y;
    }

    for(int i = 1; i <= n; i ++){
        for(int j = 1; j <= i; j ++){
            dp[i][j] = dp[i - 1][j - 1] + a[i] + b[j];
        }

        for(int j = 0; j < i; j ++){
            dp[i][0] = max(dp[i][0],dp[i - 1][j]);
        }

    }

    LL ans = 0;

    for(int i = 0; i <= n; i ++) ans = max(ans,dp[n][i]);

    cout << ans << endl;

    return 0;

}
```
