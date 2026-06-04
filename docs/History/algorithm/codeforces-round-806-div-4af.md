---
title: "Codeforces Round #806 (Div. 4)(A~F)"
date: 2022-07-28
categories: [ALGORITHM, Q&amp;A, 模拟, 二分, Codeforces]
description: ""
---

## A. YES or YES?

---

### 题目大意

[Original Link](https://codeforces.com/contest/1703/problem/A)

* 判断是否是不区分大小写的“yes”字符串
  * 是则输出`YES`，否则输出`NO`

---

### 思想

* 读入字符串后暴力判断每个字符

---

### 代码
```cpp
#include &lt;bits/stdc++.h&gt;
using namespace std;

void solve(){
    string s;
    cin >> s;
    bool flag = 1;
    if(s[0] != 'y' && s[0] != 'Y') flag = 0;
    if(s[1] != 'e' && s[1] != 'E') flag = 0;
    if(s[2] != 's' && s[2] != 'S') flag = 0;
    if(s.size() == 3 && flag) cout &lt;&lt; "YES" &lt;&lt; endl;
    else cout &lt;&lt; "NO" &lt;&lt; endl;
}

int main(){
    int _;
    cin &gt;> _;
    while(_--){
        solve();
    }
    return 0;
}
```

---

## B. ICPC Balloons

---

### 题目大意

[Original Link](https://codeforces.com/contest/1703/problem/B)

* 共 $A$ 到 $Z$ 道题，第一次出现送出两个气球，后续出现送出一个气球
  * 求比赛共送出多少气球

---

### 思想

* `vis[i]`标记字母是否出现过
  * 未出现的送出两个，出现过送出一个
  * 遍历字符串求和

---

### 代码
```cpp
#include &lt;bits/stdc++.h&gt;
using namespace std;

const int N = 1010;
typedef long long LL;
bool vis[N];

void solve(){
    memset(vis, 0, sizeof vis);
    int n;
    cin >> n;
    LL cnt = 0;
    while(n--){
        char a;
        cin >> a;
        if(!vis[a]){
            cnt += 2;
            vis[a] = 1;
        }
        else cnt++;
    }
    cout &lt;&lt; cnt &lt;&lt; endl;
}

int main(){
    int _;
    cin &gt;> _;
    while(_--){
        solve();
    }
    return 0;
}
```

---

## C. Cypher

---

### 题目大意

[Original Link](https://codeforces.com/contest/1703/problem/C)

* 每个密码锁有 $n$ 个轮子，轮子上有 $0$ 到 $9$ 的数字
  * 给出最终位置显示的数字 $a_i$，和第 $i$ 个位置的 $b_i$ 次操作
  * 求原始的数字

### 思想

* 模拟
  * `ans[i]`存储第 $i$ 位的最终数字，用 `flag` 存储操作的偏移量
  * 若为 `U` 则 `flag--`，反之 `flag++`
  * 对于 `ans[i]`，加上其偏移量并取正整数模，即 `ans[i] = (ans[i] + flag % 10 + 10) % 10` 即为原始数字

---

### 代码
```cpp
#include &lt;bits/stdc++.h&gt;
using namespace std;

const int N = 1010;

int n;

int ans[N];

void solve(){
    cin >> n;
    for(int i = 1; i &lt;= n; i ++) cin &gt;> ans[i];
    for(int i = 1; i &lt;= n; i ++){
        int m;
        cin &gt;> m;
        int flag = 0;
        while(m--){
            char op;
            cin >> op;
            if(op == 'D') flag ++;
            else flag --;
        }
        ans[i] = (ans[i] + flag % 10 + 10) % 10;
    }
    for(int i = 1; i &lt;= n; i ++) cout &lt;&lt; ans[i] &lt;&lt; " ";
    cout &lt;&lt; endl;
}

int main(){
    int _;
    cin &gt;> _;
    while(_--){
        solve();
    }
    return 0;
}
```

---

## D. Double Strings

---

### 题目大意

[Original Link](https://codeforces.com/contest/1703/problem/D)

* 给定 $n$ 个长度不超过 $8$ 的字符串 $s$
  * 若对于 $s_i = s_j + s_k$ 成立，则 $s_i$ 标记为 $1$，否则标记为 $0$

---

### 思想

* $n$ 比较大，但 $s_i$ 较短
  * 对于 $s_i$，每次构造两个 $s_i$ 的子串 $s_i', s_i''$，对子串进行查询
  * 若两个子串都可以找到，则标记 $s_i$ 为 $1$，反之为 $0$
  * 利用 `s[N]` 和 `set&lt;string&gt; st` 同时存储所有的 `s[i]`
  * 遍历 `s[i]`，第一个子串从 `s[0]` 开始，长度为 `1 &lt;= j &lt;= s[i].size() - 1`，第二个子串从 `s[j]` 开始，长度为 `s[i].size() - j`
  * 利用 `st.count(s)` 查询子串 `s`

---

### 代码
```cpp
#include &lt;bits/stdc++.h&gt;
using namespace std;

void solve(){
    int n;
    cin >> n;
    bool vis[n + 10];
    memset(vis, 0, sizeof vis);
    set&lt;string&gt; st;
    string s[n + 1];

    for(int i = 0; i &lt; n; i++){
        cin &gt;> s[i];
        st.insert(s[i]);
    }

    for(int i = 0; i &lt; n; i++){
        if(s[i].size() == 1) continue;
        for(int j = 1; j &lt;= s[i].size() - 1; j++){
            string s1 = s[i].substr(0, j), s2 = s[i].substr(j, s[i].size() - j);
            if(st.count(s1) == 1 && st.count(s2) == 1){
                vis[i] = 1;
                break;  
            }
        }
    }

    for(int i = 0; i &lt; n; i++){
        if(vis[i]) cout &lt;&lt; 1;
        else cout &lt;&lt; 0;
    }

    cout &lt;&lt; endl;
}

int main(){
    int _;
    cin &gt;> _;
    while(_--){
        solve();
    }
    return 0;
}
```

---

## E. Mirror Grid

---

### 题目大意

[Original Link](https://codeforces.com/contest/1703/problem/E)

* 给定由 $0$ 和 $1$ 构成的正方形数组
  * 将数组向右旋转 90°、180°、270°
  * 求如何改变原数组中的值，使得四种形态的数组里的值都一样的改变最少操作次数

---

### 思想

* 原二维数组中的一个位置 `mp[i][j]` 旋转三次后，总共会出现在四个位置上（包括原位置）
  * 即原位置 `(i, j)`、`(j, n + 1 - i)`、`(n + 1 - i, n + 1 - j)`、`(n + 1 - j, i)`
  * 统计这四个位置的值变为相同的最小操作次数即可

---

### 代码
```cpp
#include &lt;bits/stdc++.h&gt;
using namespace std;

const int N = 110;

char mp[N][N];
bool st[N][N];

void solve() {
    int n;
    cin >> n;
    memset(st, 0, sizeof(st));

    for (int i = 1; i &lt;= n; i++) cin &gt;> mp[i] + 1;

    int ans = 0;

    for (int i = 1; i &lt;= n; i++) {
        for (int j = 1; j &lt;= n; j++) {
            if (i == j && n % 2 == 1) continue;
            if (!st[i][j]) {
                int cnt = 0;
                if (mp[i][j] == '1') cnt++;
                st[i][j] = 1;
                if (mp[j][n - i + 1] == '1') cnt++;
                st[j][n - i + 1] = 1;
                if (mp[n - i + 1][n - j + 1] == '1') cnt++;
                st[n - i + 1][n - j + 1] = 1;
                if (mp[n - j + 1][i] == '1') cnt++;
                st[n - j + 1][i] = 1;
                ans += min(cnt, 4 - cnt);
            }
        }
    }

    cout &lt;&lt; ans &lt;&lt; endl;
}

int main() {
    int _;
    cin &gt;> _;
    while (_--) {
        solve();
    }
    return 0;
}
```

---

## F. Yet Another Problem About Pairs Satisfying an Inequality

---

### 题目大意

[Original Link](https://codeforces.com/contest/1703/problem/F)

* 对于数列 $a$，找到满足 $a_i &lt; i &lt; a_j &lt; j$，$1 \le i, j \le n$ 的 $i, j$ 对数

---

### 思想

* 对于 $a_i &lt; i &lt; a_j &lt; j$，$1 \le i, j \le n$
  * 一定满足 `a[i] &lt; i`，将 `a[i] &gt;= i` 的删去，不参与后续匹配
  * 一定满足 `i &lt; a[j]`，`{i, j}` 的对数为 `i` 之前的满足 `a[i] &lt; i` 的数量
    * 枚举 `j`，二分查找最小满足 `i &lt; a[j]` 的位置，总数量加上 `i` 之前的所有满足 `a[i] &lt; i` 的数量

---

### 代码

```cpp
#include &lt;bits/stdc++.h&gt;
using namespace std;

const int N = 1e6 + 3;

int a[N];

typedef long long LL;

LL cnt;

vector&lt;int&gt; st;

void solve(){
    int n;
    cin >> n;

    st.clear();
    cnt = 0;

    for (int i = 1; i &lt;= n; i ++) cin &gt;> a[i];

    for (int i = 1; i &lt;= n; i ++){
        if (a[i] &gt;= i) continue;
        cnt += (lower_bound(st.begin(), st.end(), a[i]) - st.begin());
        st.push_back(i);
    }

    cout &lt;&lt; cnt &lt;&lt; endl;
}

int main(){
    int _;
    cin &gt;> _;

    while (_--){
        solve();
    }

    return 0;
}
```