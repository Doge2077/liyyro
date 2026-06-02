---
title: "Educational Codeforces Round 132 (Rated for Div. 2) A·B·C"
date: 2022-07-22
categories: [ALGORITHM, Q&amp;A, 模拟, Codeforces, 贪心, 前缀和]
description: ""
---

---

## A. Three Doors

---

### 原题链接

[Origional Link](&lt;https://codeforces.com/contest/1709/problem/A&gt;)

---

### 思想

  * 从拿到钥匙的门开始，用其得到的钥匙遍历对应的门
  * 直到钥匙为$0$，若共打开了$3$道门，则为`YES`



---

### 代码
```java


#include &lt;bits/stdc++.h&gt;
using namespace std;

const int N = 10;

void solve(){

    int a[N];

    int n;

    cin >> n;

    int flag = 1;  //记录打开的门的数量

    for(int i = 1; i <= 3; i++) cin >> a[i];

    for(int i = n; a[i] != 0; i = a[i]) flag++; 

    if(flag == 3) cout << "YES" << "\n";
    else cout << "NO" << "\n";

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

## B. Also Try Minecraft

---

### 原题链接

[Origional Link](&lt;https://codeforces.com/contest/1709/problem/B&gt;)

---

### 思想

  * 利用前缀和与后缀和预处理区间的伤害值
  * 对于每个询问：$l&lt;r$ 为前缀，$l&gt;r$ 为后缀



**注意** ：开`long long`！开`long long`！开`long long`！

---

### 代码
```java


#include &lt;bits/stdc++.h&gt;
using namespace std;

#define int long long

const int N = 1e6 + 10;

int a[N];

int b[N],c[N];

void solve(){

    int n, m;

    cin >> n >> m;

    for(int i = 1 ; i <= n ; i++){

        cin >> a[i];

        if(a[i] < a[i-1]){
            b[i] = a[i-1] - a[i];  //处理前缀   
        }
        else if(a[i] > a[i-1]){
            c[i] = a[i] - a[i-1];   //处理后缀
        }

        b[i] += b[i-1];  //构造前缀和数组
        c[i] += c[i-1];  //构造后缀和数组

    }   

    while(m--){

        int l, r;

        cin >> l >> r;

        if(l < r){
            cout << b[r] - b[l] << "\n";
        }
        else cout << c[l] - c[r] << "\n";

    }

}

signed main(){

    solve();

    return 0;

}
```

---

## C. Recover an RBS

---

### 原题链接

[Origional Link](&lt;https://codeforces.com/contest/1709/problem/C&gt;)

---

### 思想

  * 贪心
  * 设`dep`表示当前遍历到的还未配对的`(`的数量，`vis`表示当前遍历到的`?`的数量
  * 从左边向右遍历括号序列`s`
```java
* `dep`：若`s[i] == '('`，则`dep++`，若`s[i] == ')'`，则`dep--`
* `vis`：若`s[i] == '?'`，则`vis++`，
```
  * 在遍历过程中，`dep`的状态会影响序列的唯一性 
```java
* 若`dep < 0`，则在之前遍历的序列中，必然存在至少一个`?`即(`vis>0`)，使得括号序列合法，且`?`的状态将唯一确定，此时`dep++,vis--`
* 若`dep == 0 && vis == 1`，则在之前遍历的序列中，`?`的状态也将唯一确定，此时`dep++,vis--`
```
  * 遍历结束后，由于遍历时`dep`和`vis`唯一确定的状态已经消去，故现在只剩下了还未确定唯一性状态的`dep`和`vis`
  * 若`abs(dep) == vis`，说明剩下的状态也将唯一确定并消去，该括号序列合法且唯一，反之则不符合。



---

### 代码
```java


#include &lt;bits/stdc++.h&gt;
using namespace std;

void solve(){

    string s;

    cin >> s;

    int dep = 0, vis = 0;

    for(int i = 0 ; i < s.size() ; i++){

        if(s[i] == '(') dep++;
        else if(s[i] == ')'){dep--;
            if(dep < 0){
                if(vis > 0)dep++, vis--;
                else{  //vis <= 0 说明无法匹配，序列非法
                    dep = 1, vis = 0;
                    break;
                }
            }
        }
        else vis++;

        if(dep == 0 && vis == 1) dep++, vis--; 

    }

    if(abs(dep) == vis) cout << "YES" << '\n';
    else cout << "NO" << '\n';

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

## 后记

  * $A$题肥肠煎蛋，不过由于可选性的方法太多，一时间不知道选哪个最好，写的时候有点乱套
  * $B$题居然是以[Terraira](&lt;https://terraria.org/&gt;)为背景的，~~本来还激动了一下~~ ，读懂题之后发现是前缀和，比较简单 
```java
* 但是做的时候眼瞎，没看见$a_i$的范围，不开`long long`吃了四发`WA`，~~活该（）~~
* ![](https://cdn.jsdelivr.net/gh/Doge2077/liyyro-photo@main/images/2022/07/WA.png)
* 记得开`long long`！！！
* 记得开`long long`！！！
* 记得开`long long`！！！
```
  * $C$题遇到括号序列就不会，这次好好补补，贪心学不会的无力感QAQ
  * 最后发现$D$过的居然比$C$多？！$D$好像是`st表`的模板题，还没学，等我学完之后回来复仇
  * 读英文题一定要理解清楚，读假题太伤了。


