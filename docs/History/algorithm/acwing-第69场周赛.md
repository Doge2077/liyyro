---
title: "AcWing 第69场周赛"
date: 2022-10-10
categories: [ALGORITHM, Q&amp;A, 思维]
description: ""
---

## 4615. 相遇问题

[原题链接](https://www.acwing.com/problem/content/4618/)

**题目大意**：

* 求一维数轴上 $x$ 和 $y$ 分别以速度 $a,b$ 相向而行时，相遇所需时间是否为整数。

**思路**：

* 签到题。
  * 输出判断 $a + b$ 是否可以整除 $y - x$ 即可。

**代码**：
```cpp
#include &lt;bits/stdc++.h&gt;
using namespace std;

typedef long long LL;

void solve() {
    LL x, y, a, b;
    cin >> x >> y >> a >> b;
    if ((y - x) % (a + b) == 0)
        cout &lt;&lt; (y - x) / (a + b) &lt;&lt; endl;
    else
        cout &lt;&lt; -1 &lt;&lt; endl;
}

int main() {
    int _ = 1;
    cin &gt;> _;
    while (_--) solve();
    return 0;
}
```

---

## 4616. 击中战舰

[原题链接](https://www.acwing.com/problem/content/4619/)

**题目大意**：

* 存在长度为 $n$ 的格子，共 $a$ 个船，每个船占据连续的 $b$ 个格子。
  * 给定一个只包含 $0,1$ 的字符串 $S$，包含 $k$ 个 $1$，表示该格子受到打击，保证初始的打击不会击中船。
  * 求最少再打击几个格子可以保证下一次打击绝对命中船。
  * 输出任意方案即可。

**思路**：

* 思维题。
  * 由于船的位置不确定，那么对于每个包含连续的 $b$ 个格子的区间一定可以放下一条船。
  * 则我们最终打击的对象在于这些区间中的任意一个格子，因此我们记录所有的这些连续的 $b$ 个格子中任意一个格子的坐标。
  * 最后，由于无效打击的次数最少，假设所有可打击的区间数量为 $x$，则最少打击 $x - a + 1$ 次后，下一次的打击区间必定命中船。

**代码**：
```cpp
#include &lt;bits/stdc++.h&gt;
using namespace std;

const int N = 1e6 + 10;

int num[N];
int idx;

void solve() {
    int n, a, b, k;
    cin >> n >> a >> b >> k;
    string s;
    cin >> s;
    int cnt = 0;
    idx = 0;
    for (int i = 0; i &lt; s.size(); i++) {
        if (s[i] == '0') {
            cnt++;
            if (cnt == b) {
                num[idx++] = i + 1;
                cnt = 0;
            }
        } else {
            cnt = 0;
        }
    }
    cout &lt;&lt; idx - a + 1 &lt;&lt; endl;
    for (int i = 0; i &lt; idx - a + 1; i++) {
        cout &lt;&lt; num[i] &lt;&lt; ' ';
    }
    cout &lt;&lt; endl;
}

int main() {
    solve();
    return 0;
}
```

---

## 4617. 解方程

[原题链接](https://www.acwing.com/problem/content/4620/)

**题目大意**：

* 给定一个非负整数 $a$，请你计算方程 $a-(a \oplus x)-x=0$ 的非负整数解的数量。

**思路**：

* 数学思维题。
  * 化简该方程为： $a - x = a \oplus x$。
  * 当 $a$ 二进制上的某一位是 $1$ 时：
    * $1-0=1, 1\oplus0=1, 1-1=0, 1\oplus1=0$
    * 故此时 $a$ 与 $x$ 无论是做减法还是异或运算，结果都相同。
  * 当 $a$ 二进制上的某一位是 $0$ 时：
    * $0-0=0, 0\oplus0=0$
    * 故此时只有 $x$ 的二进制位也是 $0$ 才可使得等式成立。
  * 综上，设 $a$ 的二进制位上共有 $m$ 个位的值为 $1$，则 $x$ 的可选方案数为 $2^m$ 种。

**代码**：
```cpp
#include &lt;bits/stdc++.h&gt;
using namespace std;

typedef long long LL;

void solve() {
    LL n;
    cin >> n;
    int cnt = 0;
    while (n) {
        cnt += n & 1;
        n >>= 1;
    }
    cout &lt;&lt; (1LL &lt;&lt; cnt) &lt;&lt; endl;
}

int main() {
    int _ = 1;
    cin &gt;> _;
    while (_--) solve();
    return 0;
}
```