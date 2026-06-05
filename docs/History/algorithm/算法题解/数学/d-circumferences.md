---
title: "D - Circumferences"
date: 2022-07-14
categories: [ALGORITHM, Q&amp;A, BFS]
description: ""
---

### D - Circumferences

[原题链接](https://atcoder.jp/contests/abc259/tasks/abc259_d)

**分析**

* 考虑 `BFS` 搜索，将相交的圆加入搜索队列。
  * 每次搜索判断终点是否位于圆上。
  * 核心在于判断两圆是否相交，以及点是否位于圆上，设圆心距为 `d`。
  * 相交条件：`d * d &lt;= (r1 + r2) * (r1 + r2) && d * d &gt;= (r1 - r2) * (r1 - r2)`
  * 点 `(x, y)` 在圆 `(x1, y1, r1)` 上的条件：`(x1 - x) * (x1 - x) + (y1 - y) * (y1 - y) == r1 * r1`

**注意**

* 注意数据范围，需要使用 `long long`。
  * 不能使用 `sqrt` 和 `pow`，避免产生精度问题。

**代码**
```cpp
#include &lt;bits/stdc++.h&gt;
using namespace std;

typedef long long LL;

const LL N = 1e6 + 3;

LL n, sx, sy, tx, ty;

struct point {  // 存储圆的信息
    LL x, y, r;
} mp[N];

queue&lt;point&gt; st;  // 用于搜索的队列

bool vis[N];  // 记录该圆是否被搜到过

// 判断两圆是否相交
bool check(LL x_1, LL y_1, LL x_2, LL y_2, LL r_1, LL r_2) {
    LL d2 = (x_1 - x_2) * (x_1 - x_2) + (y_1 - y_2) * (y_1 - y_2);
    LL dr1 = (r_1 - r_2) * (r_1 - r_2);
    LL dr2 = (r_1 + r_2) * (r_1 + r_2);
    return d2 >= dr1 && d2 <= dr2;
}

// 判断点是否在圆上
bool in(LL x, LL y, LL r, LL a, LL b) {
    return (x - a) * (x - a) + (y - b) * (y - b) == r * r;
}

bool bfs() {
    while (!st.empty()) {
        auto p = st.front();
        st.pop();

        // 若终点在圆上，直接返回
        if (in(p.x, p.y, p.r, tx, ty)) {
            return true;
        }

        for (int i = 0; i < n; i++) {
            if (!vis[i]) {  // 若没有搜到过该圆
                if (check(p.x, p.y, mp[i].x, mp[i].y, p.r, mp[i].r)) {
                    vis[i] = true;  // 标记该圆已访问
                    st.push(mp[i]); // 加入搜索队列
                }
            }
        }
    }
    return false;  // 找不到说明走不到终点
}

int main() {
    scanf("%lld", &n);
    scanf("%lld %lld %lld %lld", &sx, &sy, &tx, &ty);

    for (int i = 0; i < n; i++) {
        LL a, b, c;
        scanf("%lld %lld %lld", &a, &b, &c);
        mp[i] = {a, b, c};
    }

    // 从起点所在的圆开始搜索
    for (int i = 0; i < n; i++) {
        if (in(sx, sy, mp[i].r, mp[i].x, mp[i].y)) {
            st.push(mp[i]);
            vis[i] = true;
            break;
        }
    }

    if (bfs()) {
        printf("Yes\n");
    } else {
        printf("No\n");
    }

    return 0;
}
```