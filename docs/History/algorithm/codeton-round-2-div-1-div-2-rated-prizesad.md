---
title: "CodeTON Round 2 (Div. 1 + Div. 2, Rated, Prizes!)(A~D)"
date: 2022-08-01
categories: [ALGORITHM, Q&amp;A, 模拟, 数学, Codeforces, 贪心]
description: ""
---

## A. Two 0-1 Sequences

---

### 题目大意

[Origional Link](&lt;https://codeforces.com/contest/1704/problem/A&gt;)

  * 给定只包含$0$和$1$的字符串$a$和$b$
  * 对$a$进行操作： 
```java
* 将$a_2 = min(a_1,a_2)$，并删除$a_1$，使得$a_2$变为新的$a_1$
* 将$a_2 = max(a_1,a_2)$，并删除$a_1$，使得$a_2$变为新的$a_1$
```
  * 上述操作不限次数，求最终是否可以使得$a=b$



---

### 思想

  * 由于我们只能对`a[1], a[2]`进行操作

  * 观察`string a, b`，发现：

```java
* 先将`a`和`b`的最左端对齐
```java
* a = "00100101"
      b =     "1101"
```java
* 与`b[0]`对其的`a[4]`不相等，`b[0]`之后对齐的与`a[4]`之后的元素均相等
```java
* 若使得`a == b`，则`a[4]`之前的元素中，必然存在某元素`a[i] == b[0]`，才可通过相关操作使得`a[4] == b[0]`
```

  * 由此可知，我们设`b[0]`与`a[k]`对齐

  * 从`a[k + 1]`开始构造`a`的字串`s1`，从`b[1]`开始构造`b`的字串`s2`

  * 若`s1 == s2 `：

```java
* 若`b[0] == a[k]`说明必然可以使得`a == b`
* 若`b[0] != a[k]`，则当`k`之前存在`a[i] == b[0]`时可以使得`a == b`，反之不行
```
  * 若`s1 != s2`，则无论如何操作都无法使得`a == b`




---

### 代码
```java


#include &lt;bits/stdc++.h&gt;
using namespace std;

void solve(){

    int n, m;

    cin >> n >> m;

    string a, b;
    cin >> a >> b;

    int k = a.size() - b.size();  //对其的位置

    string s1 = a.substr(k + 1,b.size() - 1);
    string s2 = b.substr(1,b.size() - 1);

    if(s1 == s2){

        int flag = 0;

        if(a.rfind(b[0], k) != -1) flag = 1;

        if(flag) cout << "YES" << endl;
        else cout << "NO" << endl;

    }
    else cout << "NO" << endl;

}

int main(){

    int _;
    cin >> _;
    while(_ --){
        solve();
    }

//  solve();

    return 0;

}
```

---

## B. Luke is a Foodie

---

### 题目大意

[Origional Link](&lt;https://codeforces.com/contest/1704/problem/B&gt;)

  * 对于$a_i$和固定的$x$
  * 有可以变成任意整数的$v$，使得$|v - a_i|\le x$
  * 遍历数组$a$，求$v$最小变化的次数



---

### 思想

  * 由$|v - a_i|\le x$可知$a_i - x\le v \le a_i + x$
  * 故对于`a[i]`，必然存在满足$|v - a_i|\le x$的区间`[l,r]`，`l = a[i] - x, r = a[i] + x`
  * 设`a[i + 1]`的区间`[l',r']`，`l = a[i + 1] - x, r = a[i + 1] + x`
  * 若`[l,r]`与`[l',r']`有公共区间时，`v`可以不用发生改变，并将区间更新为其公共区间
  * 若`[l,r]`与`[l',r']`无公共区间时，`v`将发生改变，并将区间变为`[l',r']`
  * 公共区间存在判断：`max(l,l') <= min(r,r')`说明存在公共区间



---

### 代码
```java


#include &lt;bits/stdc++.h&gt;
using namespace std;

typedef long long LL;

void solve(){

    LL n, x;

    cin >> n >> x;

    LL cnt = 0;

    LL t;
    cin >> t;

    LL l = t - x, r = x + t;  //初始区间 

    for(int i = 1; i < n; i ++){
        LL y;
        cin >> y;
        LL p1 = y - x, p2 = y + x;
        if(max(p1,l) <= min(p2,r)){  //是否有公共区间 
            l = max(p1,l);  //更新公共区间左边界 
            r = min(p2,r);  //更新公共区间右边界 
        }
        else{
            cnt ++;  //不存在公共区间，需要变化一次 
            l = p1;  //重置区间 
            r = p2;
        }

    }

    cout << cnt << endl;

}

int main(){

    int _;
    cin >> _;
    while(_ --){
        solve();
    }

//  solve();

    return 0;

}

```

---

## C. Virus

---

### 题目大意

[Origional Link](&lt;https://codeforces.com/contest/1704/problem/C&gt;)

  * $1\sim N$的房屋围成一圈
  * 给出初始感染病毒的房屋编号
  * 每天可选择未感染的房屋进行保护，可使其永久不被感染
  * 每天已感染的房屋其左右邻居都会受到感染
  * 求最优策略下，最终感染的房屋数量



---

### 思想

  * 贪心
  * 每次选择未感染的最长区间进行保护
  * 对于被保护的区间`[l,r]`： 
```java
* 经过第一天：
* 保护`[l,r]`的一个端点，设保护`a[l]`
* `a[l]`不会感染，`a[r]`会被感染
* 其他所有未受到保护的区间`[l',r']`里，`a[l']`和`a[r']`被感染
* 经过第二天：
* 保护`[l,r]`的另一个端点`a[r]`，由于第一天`a[r]`被感染，故只能保护`a[r - 1]`
* 其他所有未受到保护的区间`[l',r']`里，`a[l' + 1]`和`a[r' - 1]`被感染
* 即对于选择保护的区间`[l,r]`，`a[r]`被感染，我们只能保护到`[l,r - 1]`这一段，且其余所有未受到保护的区间`[l',r']`里`a[l'],a[r'],a[l' + 1],a[r' - 1]`受到感染，感染后的区间变为`[l' + 2, r' - 2]`
```
  * 综上可知，我们优先保护最长的未被感染的区间，即可实现最优策略
  * 由于选择保护的区间端点可以任选，故只需要考虑区间长度，不需要维护额外的信息
  * 注意不要忽略首尾相连的区间



---

### 代码
```java


#include &lt;bits/stdc++.h&gt;
using namespace std;

void solve(){

    int n, m;

    cin >> n >> m;

    vector&lt;int&gt; vis;  //vis存储最先被感染的房屋编号 

    for(int i = 0; i < m; i ++){
        int x;
        cin >> x;
        vis.push_back(x);
    }

    sort(vis.begin(),vis.end());  //将编号从小到大排序 

    priority_queue&lt;int&gt; st;  //优先队列维护当前最大长度的区间 

    st.push(n - vis.back() + vis[0] - 1);  //将首尾相连的区间长度加入 

    for(int i = 0; i + 1 < vis.size(); i ++){
        st.push(vis[i + 1] - vis[i] - 1);  //将未感染的区间的长度加入 
    }

    int cnt = 0;  //存储未感染的区间长度 

    for(int i = 0; i + 1 > 0; i ++){  //i代表天数 
        if(!st.empty() && st.top() - i * 4 > 0){  //经过一天，下一个区间长度 -4 
            int k = st.top() - i * 4;  //设k为当前区间经过i天后未感染的区间长度 
            if(k > 1) k --;  //对于一个端点的保护，会使另一个端点被感染(长度-1)，若区间长度仅为1，则只能保护1长度 
            cnt += k;  //累计保护到的区间长度 
            st.pop();
        }
        else break;
    }

    cout << n - cnt << endl;  //区间总长 - 保护的区间长度 = 被感染的区间长度 = 被感染的房屋数量 

}

int main(){

    int _;
    cin >> _;
    while(_ --){
        solve();
    }

//  solve();

    return 0;

}
```

---

## D. Magical Array

---

### 题目大意

[Origional Link](&lt;https://codeforces.com/contest/1704/problem/D&gt;)

  * 对于一个长度为$m$的数组$b$，构造$n$个与$b$相同的的数组$c$
  * 对于数组$c_t(1\le t \le n)$现有操作： 
```java
* 操作1：首先将$c_t[i]=c_t[i]-1,c_t[j]=c_t[j]-1$，然后将$c_t[i-1]=c_t[i-1]+1,c_t[j+1]=c_t[j+1]+1$
* 操作2：首先将$c_t[i]=c_t[i]-1,c_t[j]=c_t[j]-1$，然后将$c_t[i-1]=c_t[i-1]+1,c_t[j+2]=c_t[j+2]+1$
```
  * 选择某一个数$k(1\le k \le n)$，使得$c_k$为特别数组
  * 非特别数组$c_i(1\le i \le n,i \ne k)$只能执行操作1若干次
  * 特别数组$c_k(1\le k \le n)$只能执行操作2若干次
  * 给出这些操作后的数组$c$，找出其中的特别数组的编号$k$，及其执行了多少次操作2



---

### 思想

$$
对于c_t(1\le t \le n)\\\\\\\ \begin{aligned} （一）\\\\\\\ 对于&c;_{i-1},c_i,c_j,c_{j+1}，可以得到c_{i−1}×(i−1)+c_i×i+c_j×j+c_{j+1}×(j+1)\\\\\\\ &化简得：i×(c_{i−1}+c_i)+j×(c_j+c_{j+1})−c_{i−1}+c_{j+1}①\\\\\\\ 对于&c;_{i-1},c_i,c_j,c_{j+1}执行操作1：\\\\\\\ &(c_{i−1}+1)×(i−1)+(c_i-1)×i+(c_j-1)×j+(c_{j+1}+1)×(j+1)\\\\\\\ &化简得：i×(c_{i−1}+c_i)+j×(c_j+c_{j+1})−c_{i−1}+c_{j+1}②\\\\\\\ &可知①=②，即操作1不会改变c_i\times i的和 \\\\\\\ \end{aligned}\\\\\\\ \begin{aligned} （二）\\\\\\\ 对于&c;_{i-1},c_i,c_j,c_{j+1},c_{j+2},可以得到c_{i−1}×(i−1)+c_i×i+c_j×j+c_{j+1}×(j+1)+c_{j+2}\times (j+2)\\\\\\\ &化简得：i×(c_{i−1}+c_i)+j×(c_j+c_{j+1}+c_{j+2})−c_{i−1}+c_{j+1}+2\times c_{j+2}③\\\\\\\ 对于&c;_{i-1},c_i,c_j,c_{j+1},c_{j+2}执行操作2：\\\\\\\ &(c_{i−1}+1)×(i−1)+(c_i-1)×i+(c_j-1)×j+c_{j+1}×(j+1)+(c_{j+2}+1)\times (j+2)\\\\\\\ &化简得：i×(c_{i−1}+c_i)+j×(c_j+c_{j+1}+c_{j+2})−c_{i−1}+c_{j+1}+2\times c_{j+2}+1④\\\\\\\ &可知③=④+1，即操作1会改变c_i\times i的和，使其加1\\\\\\\ \end{aligned}\\\\\\\ 综上可知：对每一个数组c，求S_f = \sum c_i\times i\\\\\\\ 与其他数组c的S_f不同的数组即为特别数组，记为S_p\\\\\\\ 其操作2的次数为S_p-S_f\\\\\\\
$$

---

### 代码
```java


#include &lt;bits/stdc++.h&gt;
using namespace std;

typedef long long LL;

void solve(){

    LL n, m;

    cin >> n >> m;

    LL S1 = -1, S2 = -1;  //S求c_i * i的和
    LL cnt1 = 0, cnt2 = 0;  //cnt记录S的数量
    LL p1, p2;  //存储第一次出现S的编号

    for(LL i = 1; i <= n; i ++){

        LL sum = 0;

        for(LL j = 1; j <= m; j ++){
            LL x;
            cin >> x;
            sum += x * j;
        }

        if(S1 == -1){
            S1 = sum;
            p1 = i;
        }
        else if(S1 != -1 && S2 == -1 && S1 != sum){
            S2 = sum;
            p2 = i;
        }

        if(S1 == sum) cnt1 ++;
        if(S2 == sum) cnt2 ++;

    }

    if(cnt1 > cnt2){
        cout << p2 << " " << S2 - S1 << endl;
    } 
    else cout << p1 << " " << S1 - S2 << endl;

}

int main(){

    LL _;
    cin >> _;
    while(_ --){
        solve();
    }

//  solve();

    return 0;

}
```

---

## 后记

  * $A$题一开始没找到规律，找到规律后居然没有把错思路的代码删掉，狠狠的吃`WA`的铁头娃
  * ![](https://cdn.jsdelivr.net/gh/Doge2077/liyyro-photo@main/images/2022/08/屏幕截图-2022-08-01-115832.png)
  * $B$题读懂题意就很简单了，没什么好说的，就是判断公共区间
  * $C$题一直在想着怎么维护端点的信息，最后发现根本不需要，只要长度就行了QAQ
  * $D$题没时间了，太抽象了也看不懂，补题看题解发现证明的想法实在是妙极了，根本想不到
  * 最后还是没能上绿，~~我是废物~~
  * ![](https://cdn.jsdelivr.net/gh/Doge2077/liyyro-photo@main/images/2022/08/屏幕截图-2022-08-01-120032.png)


