---
title: "Codeforces Round #828 (Div. 3) （A~D）"
date: 2022-10-17
categories: [ALGORITHM, Q&A, 模拟, Codeforces, 贪心, 思维]
description: ""
---

# codeforces-round-828-div-3-（ad）


## A. Number Replacement

---

[Original Link](https://codeforces.com/contest/1744/problem/A)

**题目大意**

* 给定一个序列 $a$ 和一个字符串 $s$。
  * 可以将相同的 $a_i$ 替换为 $s_i$，条件是 $a_i$ 对应的替换规则唯一。
  * 求是否可以在满足上述条件下完成替换。

---

**思想**：

* 思维题。
  * 遍历数组，当 $a_i$ 首次出现时，将其对应的字符规则设定为 $s_i$。
  * 若 $a_i$ 已经出现过，但其规则与当前 $s_i$ 不同，则说明无法完成替换。

---

**代码**：
```cpp
#include <iostream>
#include <cstring>

using namespace std;

const int N = 1e6 + 3;

int a[N];

int main(){
    int t;
    cin >> t;
    while(t--){
        int n;
        cin >> n;
        for(int i = 0; i < n; i++) cin >> a[i];
        string s;
        cin >> s;
        
        char rule[1010]; // 用于存储每个a_i对应的字符规则
        bool ok = true;
        memset(rule, 0, sizeof(rule));
        
        for(int i = 0; i < n; i++){
            int val = a[i];
            if(rule[val] == 0){
                // 首次出现，建立规则
                rule[val] = s[i];
            } else {
                // 规则已存在，检查是否匹配
                if(rule[val] != s[i]){
                    ok = false;
                    break;
                }
            }
        }
        
        if(ok) cout << "YES" << endl;
        else cout << "NO" << endl;
    }
    return 0;
}
```

---

## B. Even-Odd Increments

---

[Original Link](https://codeforces.com/contest/1744/problem/B)

**题目大意**

* 给定一个序列 $a$ 和 $q$ 次操作：
  * 操作 $0~~x_j$ 表示将序列中所有的偶数加上 $x_j$。
  * 操作 $1~~x_j$ 表示将序列中所有的奇数加上 $x_j$。
  * 求每次操作之后的序列之和。

---

**思想** ：

* 思维题。
  * 记录 $a$ 之和以及其偶数和奇数的数量。
  * 操作为 $0$ 时：
    * 偶数加偶数，偶数数量不变；
    * 偶数加奇数，奇数数量增加当前偶数的数量。
  * 操作为 $1$ 时：
    * 奇数加偶数，奇数数量不变；
    * 奇数加奇数，偶数数量增加当前奇数的数量。

---

**代码** ：
```cpp
#include <iostream>
#include <cstring>
#include <cstdio>
#include <algorithm>
#include <cmath>
#include <sstream>
#include <vector>
#include <queue>
#include <stack>
#include <map>
#include <set>
#include <unordered_map>
#include <unordered_set>

using namespace std;

#define IOS ios::sync_with_stdio(false),cin.tie(nullptr),cout.tie(nullptr)
#define re register
#define fi first
#define se second
#define endl '\n'

typedef long long LL;
typedef pair<int, int> PII;
typedef pair<LL, LL> PLL;

const int N = 1e6 + 3;
const int INF = 0x3f3f3f3f, mod = 1e9 + 7;
const double eps = 1e-6, PI = acos(-1);

void solve(){
    LL sum = 0;
    LL odd = 0, even = 0;

    int n, q; cin >> n >> q;
    for(int i = 0; i < n; i ++){
        LL x; cin >> x;
        if(x % 2 == 0) even ++;
        else odd ++;
        sum += x;
    }
    while(q --){
        int op, k; cin >> op >> k;
        if(op == 0){
            if(k % 2 == 0) sum += even * k;
            else{
                sum += even * k;
                odd += even; even = 0;
            }
        }
        else{
            if(k % 2 == 0) sum += odd * k;
            else{
                sum += odd * k;
                even += odd; odd = 0;
            }
        }
        cout << sum << endl;
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

---

## C. Traffic Light

---

[Original Link](https://codeforces.com/contest/1744/problem/C)

**题目大意** ：

* 给定一个长度为 $n$ 且只包含 $r,y,g$ 的字符串 $s$ 代表红绿灯的信号周期。
  * 给出当前的信号为 $c$ 表示当前的状态。
  * 求最长等待可以遇到 $g$ 的时间。

---

**思想** ：

* 模拟。
  * 将 $s$ 加长，使得一个周期首尾相连。
  * 从每个信号为 $c$ 的位置开始，找到下一个为 $g$ 的位置。
  * 更新最大的区间长度。

---

**代码** ：
```cpp
#include <iostream>
#include <cstring>
#include <cstdio>
#include <algorithm>
#include <cmath>
#include <sstream>
#include <vector>
#include <queue>
#include <stack>
#include <map>
#include <set>
#include <unordered_map>
#include <unordered_set>

using namespace std;

#define IOS ios::sync_with_stdio(false),cin.tie(nullptr),cout.tie(nullptr)
#define re register
#define fi first
#define se second
#define endl '\n'

typedef long long LL;
typedef pair<int, int> PII;
typedef pair<LL, LL> PLL;

const int N = 1e6 + 3;
const int INF = 0x3f3f3f3f, mod = 1e9 + 7;
const double eps = 1e-6, PI = acos(-1);

void solve() {
    int n;
    string op;
    cin >> n >> op;
    string s;
    cin >> s;
    int t = s.size();
    s = s + s;
    int pos = s.find(op);
    int res = -1;
    for (int i = 0; i < t + pos + 1; i++) {
        int cnt = 0;
        if (s[i] == op[0]) {
            while (s[i] != 'g' && i < s.size()) {
                cnt++;
                i++;
            }
            res = max(res, cnt);
        }
    }
    cout << res << endl;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);
    int _ = 1;
    cin >> _;
    while (_--) {
        solve();
    }
    return 0;
}
```

---

## D. Divisibility by 2^n

---

[Original Link](https://codeforces.com/contest/1744/problem/D)

**题目大意**：

* 给定一个长度为 $n$ 的正整数序列 $a$，要求通过操作使得所有元素的乘积可以被 $2^n$ 整除。
  * 可以进行如下操作：
    * 将 $a_i$ 变为 $a_i \times i$。
  * 上述操作每个位置只能进行一次。
  * 求满足题意的最少操作次数。

---

**思想**：

* 贪心。
  * 设 $a_i$ 乘积为 $k$，则满足 $2^n \mid k$ 的条件为 $k$ 因数分解中，$2$ 的因子数量大于等于 $n$。
  * 显然，当 $2$ 的因子数量不足时，使得操作数最小的方案即为优先选择 $i$ 包含 $2$ 因子数量多的位置进行操作。

---

**代码**：
```cpp
#include <iostream>
#include <cstring>
#include <cstdio>
#include <algorithm>
#include <cmath>
#include <sstream>
#include <vector>
#include <queue>
#include <stack>
#include <map>
#include <set>
#include <unordered_map>
#include <unordered_set>

using namespace std;

#define IOS ios::sync_with_stdio(false), cin.tie(nullptr), cout.tie(nullptr)
#define re register
#define fi first
#define se second
#define endl '\n'

typedef long long LL;
typedef pair<int, int> PII;
typedef pair<LL, LL> PLL;

const int N = 1e6 + 3;
const int INF = 0x3f3f3f3f, mod = 1e9 + 7;
const double eps = 1e-6, PI = acos(-1);

int f(LL n) {
    int cnt = 0;
    while (n % 2 == 0) {
        n /= 2;
        cnt++;
    }
    return cnt;
}

void solve() {
    LL sum = 0;
    priority_queue<int> st;
    int n;
    cin >> n;
    for (int i = 1; i <= n; i++) {
        LL x;
        cin >> x;
        sum += f(x);
        st.push(f(i));
    }
    int cnt = 0;
    while (!st.empty() && sum < n) {
        sum += st.top();
        st.pop();
        cnt++;
    }
    if (sum >= n) {
        cout << cnt << endl;
    } else {
        cout << -1 << endl;
    }
}

int main() {
    IOS;
    int _ = 1;
    cin >> _;
    while (_--) {
        solve();
    }
    return 0;
}
```

