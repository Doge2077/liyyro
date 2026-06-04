---
title: "AcWing 第62场周赛"
date: 2022-07-30
categories: [ALGORITHM, Q&amp;A, 数学]
description: ""
---

---

## 4500. 三个元素

---

### 原题链接

[Original Link](https://www.acwing.com/problem/content/4503/)

---

### 思想

* `pair&lt;int,int&gt; a`存储值和对应下标
  * 对值进行排序，遍历找到三个不同值
  * 若存在则输出下标

---

### 代码
```cpp
#include &lt;bits/stdc++.h&gt;
using namespace std;

const int N = 1e6 + 10;

pair&lt;int,int&gt; a[N];

void solve(){
    int n;
    cin >> n;
    for(int i = 0; i &lt; n; i ++){
        int x;
        cin &gt;> x;
        a[i] = {x, i + 1};
    }

    sort(a, a + n);

    int cnt = 0;
    int flag = a[0].first;
    int ans[10];
    ans[cnt] = a[0].second;

    for(int i = 1; i &lt; n; i ++){
        if(a[i].first != flag){
            flag = a[i].first;
            ans[++cnt] = a[i].second;
            if(cnt == 2) break;
        }
    }

    if(cnt == 2){
        for(int i = 0; i &lt;= cnt ; i ++) cout &lt;&lt; ans[i] &lt;&lt; " ";
    }
    else cout &lt;&lt; -1 &lt;&lt; " " &lt;&lt; -1 &lt;&lt; " " &lt;&lt; -1;
}

int main(){
    solve();
    return 0;
}
```

---

## 4501. 收集卡牌

---

### 原题链接

[Original Link](https://www.acwing.com/problem/content/4504/)

---

### 思想

* `vector&lt;int&gt; st`存储当前可以构成一套的数，当`st.size() == n`说明可以构成一套
  * `vis[i]`标记`i`是否在`st`中，`num`存储目前为止的未成套的数及其数量
  * 若读入的数未在`st`中，则将其加入并标记
  * 每次加入`st`对其进行判断： 
    * 若`st.size() == n`说明已成套
    * 用`string s`标记是否成套，在`st.size() == n`时进行标记
    * 将`st`和`vis`清空，遍历`num`将未成套的数加入`st`并标记
  * 输出`s`即为答案

---

### 代码
```cpp
#include &lt;bits/stdc++.h&gt;
using namespace std;

const int N = 1e6 + 10;

int n, m;
map&lt;int,int&gt; num;
bool vis[N];

void solve(){
    cin >> n >> m;
}
```

---

## 4502. 集合操作

---

### 原题链接

[Original Link](https://www.acwing.com/solution/content/128431/)

---

### 思想

* $max(s) - mean(s)$ 的最大可能值，取决于 $mean(s)$ 最小值
  * 由题可知序列单调递增
  * 则 $mean(s)$ 一定是从前面获取一段连续的数 + 该最大值
  * 加进来的数和平均值比较：
    * 如果新加进来的数比平均值小，那么这个当前状态子集元素的平均值一定会减小
    * 如果相等，平均值不变
    * 如果新加进来的数比平均值大，平均值会增加

---

### 代码
```cpp
#include &lt;bits/stdc++.h&gt;
using namespace std;

const int N = 1e6 + 10;

int idx, cnt = 1;

double a[N], s[N];

double check(int u){
    return a[idx] - (s[u - 1] + a[idx]) / u;
}

void solve(){
    int _;
    cin >> _;
    while (_ --){
        int op;
        cin >> op;
        if (op == 1) {
            cin >> a[++idx];
            s[idx] = s[idx - 1] + a[idx];
        } else {
            while (cnt + 1 &lt;= idx && check(cnt + 1) &gt; check(cnt)) ++cnt;
            printf("%.6lf\n", check(cnt));
        }
    }
}

int main() {
    solve();
    return 0;
}
```