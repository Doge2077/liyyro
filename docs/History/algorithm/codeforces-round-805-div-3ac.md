---
title: "Codeforces Round #805 (Div. 3)(A~C)"
date: 2022-07-29
categories: [ALGORITHM, Q&amp;A, 模拟, Codeforces]
description: ""
---

---

## A. Round Down the Price

---

### 题目大意

[Origional Link](&lt;https://codeforces.com/contest/1702/problem/A&gt;)

  * 对于一个数$N$，求其最接近且不大于该数的$10^m$
  * 输出$N-10^m$



---

### 思想

  * 初始化`p = 1e10`，循环枚举`p = p / 10`直到`p < n`



---

### 代码
```java


#include &lt;bits/stdc++.h&gt;
using namespace std;

typedef long long LL;

void solve(){

    LL n;
    cin >> n;

    LL p = 1e11;

    while(p > n){
        p /= 10;
    }

    cout << n - p <<endl;

}

int main(){

    int _;
    cin >> _;

    while(_--){
        solve();
    }

    return 0;

}
```

---

## B. Polycarp Writes a String from Memory

---

### 题目大意

[Origional Link](&lt;https://codeforces.com/contest/1702/problem/B&gt;)

  * 对于字符串$S$，每天只能遍历三个不同字母
  * 几天可以遍历完$S$



---

### 思想

  * 模拟
  * `vis[s[i]]`记录`s[i]`是否为新字母，`cnt`记录当天的新字母的个数
  * 当`cnt == 4`说明要开始新的一天，并清空记忆



---

### 代码
```java


#include &lt;bits/stdc++.h&gt;
using namespace std;

void solve(){

    string s;

    cin >> s;

    int flag = 0;

    bool vis[300];

    memset(vis,0,sizeof vis);

    int cnt = 0;

    for(int i = 0; i < s.size(); i ++){
        if(!vis[s[i]]){
            cnt ++;
            if(cnt == 4){
                cnt = 1;
                flag ++;
                memset(vis,0,sizeof vis);
            }
            vis[s[i]] = 1;
        }
    }   

    if(cnt) flag ++;

    cout << flag << endl;

}

int main(){

    int _;

    cin >> _;

    while(_--){
        solve();
    }

    return 0;

}

```

---

## C. Train and Queries

---

### 题目大意

[Origional Link](&lt;https://codeforces.com/contest/1702/problem/C&gt;)

  * 顺次给定$n$个车站，先经过的车站可以走到后面的车站
  * 编号可能重复出现，即可能重复经过一个车站
  * 对于$k$次询问，给出起点和终点车站编号，求是否可以从起始站到终点站



---

### 思路

  * `map&lt;int,int&gt; l, r`分别存储某一编号的站点最左边的下标和最右边的下标
  * 对于每次询问，若起始站的最左边的下标小于终点站的最右边的下标，则可行



---

### 代码
```java


#include &lt;bits/stdc++.h&gt;
using namespace std;

void solve(){

    int n, m;

    cin >> n >> m;

    map&lt;int,int&gt; l, r;

    for(int i = 1; i <= n; i ++){
        int x;
        cin >> x;
        if(l[x] == 0){
            l[x] = r[x] = i;
        }
        else{
            l[x] = min(l[x],i);
            r[x] = max(r[x],i);
        }
    }

    while(m --){
        int x, y;
        cin >> x >> y;
        if(l[x] != 0 && l[y] != 0){
            if(l[x] < r[y]) cout << "YES" << endl;
            else cout << "NO" << endl;
        }
        else cout << "NO" << endl;
    }

}

int main(){
    int _;

    cin >> _;

    while(_--){
        solve();
    }   

    return 0;

}
```

---
