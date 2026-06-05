---
title: "Educational Codeforces Round 137 (Rated for Div. 2)（A~D）"
date: 2022-10-18
categories: [ALGORITHM, Q&amp;A, Codeforces, 贪心, 思维, 构造]
description: ""
---

## A. Password

---

[Original Link](https://codeforces.com/contest/1743/problem/A)

**题目大意**：

* 给定 \( n \) 个 \(0 \sim 9\) 之间不能使用的数字，保证剩余的数字数量大于 \(2\)。
  * 任意两个数字组合，每个数字可使用两次，组成一个四位密码。
  * 求在剩余的可选数字中，能组成的密码数量。

---

**思路**：

* 签到题。
  * 任意两个数字可组成的密码数量固定为 \(6\)。
  * 则总数量为剩余数字的两两组合数乘以 \(6\)。
  * 即设剩余的数字数量为 \(x = 10 - n\)，总密码数为 \(\frac{x \times (x - 1)}{2} \times 6\)。

---

**代码**：
```cpp
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

#define IOS ios::sync_with_stdio(false), cin.tie(nullptr), cout.tie(nullptr)
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

void solve()
{
    int n;
    cin >> n;
    for (int i = 0; i &lt; n; i++) {
        int x;
        cin &gt;> x;
    }
    n = 10 - n;
    cout &lt;&lt; 6 * n * (n - 1) / 2 &lt;&lt; endl;
}

int main()
{
    IOS;
    int _ = 1;
    cin &gt;> _;
    while (_--) {
        solve();
    }
    return 0;
}
```

---

## B. Permutation Value

---

[Original Link](https://codeforces.com/contest/1743/problem/B)

**题目大意**：

* 给定一个长度为 $n$ 的排列。
  * 定义其一个连续的子序列也为一种排列。
  * 构造一个排列使得满足上述条件的子序列的数量最少。
  * 输出任意满足条件的排列即可。

---

**思想**：

* 构造。
  * 只需要将 $1$ 提到最前面，然后倒序输出剩余的数即可。

---
```cpp
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

#define IOS ios::sync_with_stdio(false), cin.tie(nullptr), cout.tie(nullptr)
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

void solve()
{
    int n;
    cin >> n;
    cout &lt;&lt; 1 &lt;&lt; ' ';
    for (int i = n; i &gt;= 2; i--) cout &lt;&lt; i &lt;&lt; ' ';
    cout &lt;&lt; endl;
}

int main()
{
    IOS;
    int _ = 1;
    cin &gt;> _;
    while (_--) {
        solve();
    }
    return 0;
}
```

---

## C. Save the Magazines

---

[Original Link](https://codeforces.com/contest/1743/problem/C)

**题目大意**：

* 给定一个长为 $n$ 且只包含 $0,1$ 的字符串 $s$，$1$ 表示 $a_i$ 有盖，反之则无。
  * 接下来给出 $a_i$ 个箱子内部所含的杂志数量，雨会淋湿没有盖盖子的箱子里的所有杂志。
  * 每个有盖子的箱子仅可操作一次，将盖子移动到 $a_i-1$ 上。
  * 求最佳方案下最大能保护的杂志数量。

---

**思想**：

### 贪心

对于某个连续的 `1` 的区间 `[i, j]`，我们可以移动的盖子范围在 `a[i-1] ~ j`。那么在区间 `[i-1, j]` 中必然存在一个箱子没有盖子。

故需要将区间 `[i-1, j]` 中所含箱子数量最少的盖子移除，提供给没有盖子的箱子。

---

**代码**：

```cpp
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

#define IOS ios::sync_with_stdio(false), cin.tie(nullptr), cout.tie(nullptr)
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

int a[N];

void solve()
{
    int n;
    cin >> n;
    string s;
    cin >> s;
    for (int i = 0; i &lt; n; i++) cin &gt;> a[i];
    
    LL sum = 0;
    int pos = s.find("1");
    
    // cout &lt;&lt; pos &lt;&lt; endl;
    if (pos == -1) {
        cout &lt;&lt; 0 &lt;&lt; endl;
        return;
    }
}
```

---

## D. Problem with Random Tests

---

[Original Link](https://codeforces.com/contest/1743/problem/D)

**题目大意**：

* 给定一个只包含 $0,1$ 的序列。
  * 可以通过一个字串与其按位“或”运算得到一个新的 $0,1$ 序列。
  * 求如何操作使得该序列的二进制数最大。

---

**思想**：

* 贪心，枚举。
  * 该题的数据具有随机性。
  * 贪心发现，两个字符一定是从某一点位置开始，其中一个字符右移几个位置，然后或运算。
  * 那么我们需要从第一个出现的 $0$ 的位置开始“或”运算，然后暴力匹配即可。

---

**代码**：

```cpp
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

#define IOS ios::sync_with_stdio(false), cin.tie(nullptr), cout.tie(nullptr)
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

int a[N];

void solve()
{
    int n;
    cin >> n;
    string s;
    cin >> s;
    s = " " + s;
    
    int pos = 1;
    bool flag = false;
    
    for (int i = 1; i &lt;= n; i++) {
        if (s[i] == '1') flag = true;
        if (flag && s[i] == '0') {
            pos = i;
            break;
        }
    }
    
    int st = pos;
    int len = n - pos + 1;
    string ans = s;
    
    for (int i = 1; i &lt; st; i++) {
        for (int j = i + len - 1; j &lt;= n; j++) {
            string temp = s;
            for (int k = n - len + 1, u = i; u &lt;= j; u++, k++)
                if (s[u] == '1') temp[k] = '1';
            ans = max(ans, temp);
        }
    }
    
    flag = false;
    for (int i = 1; i &lt;= n; i++) {
        if (ans[i] == '1') flag = true;
        if (flag) cout &lt;&lt; ans[i];
    }
    if (!flag) cout &lt;&lt; 0;
    cout &lt;&lt; endl;
}

int main()
{
    ios::sync_with_stdio(false);
    cin.tie(0);
    cout.tie(0);
    
    int _ = 1;
    // cin &gt;> _;
    while (_--) {
        solve();
    }
    return 0;
}
```