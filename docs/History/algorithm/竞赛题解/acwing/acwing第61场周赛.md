---
title: "AcWing第61场周赛"
date: 2022-07-24
categories: [ALGORITHM, Q&amp;A]
description: ""
---

---

## A 4497. 分糖果

---

### 描述

---

[原题链接](https://www.acwing.com/problem/content/4500/)

给定三个正整数 $a,b,c$。

请计算 $⌊\frac{a+b+c}{2}⌋$，即 $a,b,c$ 相加的和除以 $2$ 再下取整的结果。

**输入格式** 第一行包含整数 $T$，表示共有 $T$ 组测试数据。

每组数据占一行，包含三个正整数 $a,b,c$。

**输出格式** 每组数据输出一行结果，表示答案。

**数据范围** 前三个测试点满足 $1≤T≤10$。 所有测试点满足 $1≤T≤1000，1≤a,b,c≤10^{16}$。

**输入样例：**
```text
4
1 3 4
1 10 100
10000000000000000 10000000000000000 10000000000000000
23 34 45
```

**输出样例：**
```text
4
55
15000000000000000
51
```

---

### 思想

* 数据范围极大，需要使用高精度计算。
* 本题是高精度加法与高精度除以低精度的模板题。

**模板代码**

* 高精度加法：用倒序的 `vector&lt;int&gt;` 存储两个大数 `A` 和 `B`，进行高精度加法。
```cpp
// 高精度加法
vector&lt;int&gt; add(vector&lt;int&gt; &A, vector&lt;int&gt; &B) {
    if (A.size() &lt; B.size()) return add(B, A); // 确保A的长度大于等于B

    int k = 0; // 定义进位，初始化为0
    vector&lt;int&gt; C; // 存储结果

    for (int i = 0; i &lt; A.size(); i++) { // 按位相加
        k += A[i]; // 加上A的当前位
        if (i &lt; B.size()) k += B[i]; // 如果B还有当前位，则加上
        C.push_back(k % 10); // 存入当前位的结果
        k /= 10; // 更新进位
    }

    if (k) C.push_back(k); // 如果最后还有进位，则添加

    return C;
}
```

* 高精度除以低精度：用倒序的 `vector&lt;int&gt;` 存储被除数 `A`，进行高精度除以低精度运算，并获得余数。
```cpp
// 高精度除以低精度
vector&lt;int&gt; div(vector&lt;int&gt; &A, int b, int &r) {
    vector&lt;int&gt; C; // 存储结果
    r = 0; // 初始化余数为0
    for (int i = A.size() - 1; i >= 0; i--) { // 从最高位开始计算
        int k = r * 10 + A[i]; // 当前位的被除数
        C.push_back(k / b); // 存入商
        r = k % b; // 更新余数
    }
    reverse(C.begin(), C.end()); // 结果是反向存储的，需要翻转
    while (C.size() > 1 && C.back() == 0) C.pop_back(); // 去除前导零
    return C;
}
```

**完整解题代码**
```cpp
#include&lt;bits/stdc++.h&gt;
using namespace std;

// 高精度加法
vector&lt;int&gt; add(vector&lt;int&gt; &A, vector&lt;int&gt; &B) {
    if (A.size() &lt; B.size()) return add(B, A);

    int k = 0;
    vector&lt;int&gt; C;

    for (int i = 0; i &lt; A.size(); i++) {
        k += A[i];
        if (i &lt; B.size()) k += B[i];
        C.push_back(k % 10);
        k /= 10;
    }

    if (k) C.push_back(k);
    return C;
}

// 高精度除以低精度
vector&lt;int&gt; div(vector&lt;int&gt; &A, int b, int &r) {
    vector&lt;int&gt; C;
    r = 0;
    for (int i = A.size() - 1; i >= 0; i--) {
        int k = r * 10 + A[i];
        C.push_back(k / b);
        r = k % b;
    }
    reverse(C.begin(), C.end());
    while (C.size() > 1 && C.back() == 0) C.pop_back();
    return C;
}

void solve() {
    vector&lt;int&gt; A, B, C;
    string a, b, c;
    int r;
    cin >> a >> b >> c;

    for (int i = a.size() - 1; i >= 0; i--) A.push_back(a[i] - '0');
    for (int i = b.size() - 1; i >= 0; i--) B.push_back(b[i] - '0');
    for (int i = c.size() - 1; i >= 0; i--) C.push_back(c[i] - '0');

    vector&lt;int&gt; sum = add(A, B);
    sum = add(sum, C); // sum = A + B + C
    vector&lt;int&gt; res = div(sum, 2, r); // res = sum / 2

    for (int i = res.size() - 1; i >= 0; i--) cout &lt;&lt; res[i];
    cout &lt;&lt; endl;
}

int main() {
    int T;
    cin &gt;> T;
    while (T--) {
        solve();
    }
    return 0;
}
```

---

## B 4498. 指针

---

### 描述

---

[原题链接](https://www.acwing.com/problem/content/4501/)

给定一个如下图所示的全圆量角器。

![](https://cdn.jsdelivr.net/gh/Doge2077/liyyro-photo@main/images/2022/07/4498.jpg)

初始时，量角器上的指针指向刻度 0。

现在，请你对指针进行 n 次拨动操作，每次操作给定一个拨动角度 ai，由你将指针拨动 ai 度，每次的拨动方向（顺时针或逆时针）由你自由决定。

请你判断，能否通过合理选择每次拨动的方向，使得指针最终仍然指向刻度 0。

**输入格式** 第一行包含整数 n。

接下来 n 行，每行包含一个整数 ai，表示一次操作的拨动角度。

**输出格式** 如果可以做到指针最终仍然指向刻度 0，则输出 YES，否则输出 NO。

**数据范围** 前 4 个测试点满足 1≤n≤3。 所有测试点满足 1≤n≤15，1≤ai≤180。

**输入样例1：**
```
3
10
20
30
```

**输出样例1：**
```
YES
```

**输入样例2：**
```
3
10
10
10
```

**输出样例2：**
```
NO
```

**输入样例3：**
```
3
120
120
120
```

**输出样例3：**
```
YES
```

---

### 思想

* 设当所有操作结束后，指针转过的净角度大小为 $P$。
* 当且仅当 $P$ 是 360 的倍数时，指针能回到原点（即 $P \equiv 0 \pmod{360}$）。
* 由于操作次数 n 较小，可以考虑使用深度优先搜索（`dfs`）来枚举所有可能的拨动方向组合。
* 递归第 $i$ 层表示进行第 $i$ 次拨动，状态为当前累计转过的角度。

---

### 代码
```cpp
#include &lt;bits/stdc++.h&gt;
using namespace std;

int n;
int a[20]; // 角度数据
bool flag = false; // 标记是否可行

void dfs(int u, int cur_angle) {
    if (u == n) {
        if (cur_angle % 360 == 0) {
            flag = true;
        }
        return;
    }
    // 尝试顺时针（角度增加）
    dfs(u + 1, cur_angle + a[u]);
    // 尝试逆时针（角度减少）
    dfs(u + 1, cur_angle - a[u]);
}

int main() {
    cin >> n;
    for (int i = 0; i &lt; n; i++) {
        cin &gt;> a[i];
    }
    dfs(0, 0);
    if (flag) cout &lt;&lt; "YES" &lt;&lt; endl;
    else cout &lt;&lt; "NO" &lt;&lt; endl;
    return 0;
}
```

---

## C 4499. 画圆

---

### 描述

---

[原题链接](https://www.acwing.com/problem/content/4502/)

在一个二维平面内，给定一个以 (x1,y1) 为圆心，半径为 R 的圆以及一个坐标为 (x2,y2) 的点。

请你在二维平面上画一个圆，要求：

1. 平面中不存在点满足既在你画的圆上，又在给定的圆外。
2. 给定的点不能在你画的圆内（可以在圆上）。
3. 被给定圆覆盖且不被你画的圆覆盖的区域面积应尽可能小。

请输出你画的圆的圆心坐标以及半径。

**输入格式** 共一行，包含 5 个整数 R, x1, y1, x2, y2。

**输出格式** 三个实数 xans, yans, r，其中 (xans, yans) 是你画的圆的圆心坐标，r 是你画的圆的半径。

结果保留六位小数。

**数据范围** 所有测试点满足 1≤R≤10^5，|x1|,|y1|,|x2|,|y2|≤10^5。

**输入样例1：**

```
5 3 3 1 1
```

**输出样例1：**

```
3.767767 3.767767 3.914214
```

**输入样例2：**

```
10 5 5 5 15
```

**输出样例2：**

```
5.000000 5.000000 10.000000
```

---

### 思路

* 分析题目要求，我们画的圆必须完全内切于或重合于给定的圆（条件1）。
* 条件2要求给定点不能在我们画的圆内。
* 条件3要求我们画的圆应尽可能大，以最小化未被覆盖的区域。
* 因此，解决方案取决于给定点相对于给定圆的位置：
    * 若点在给定圆**外**或**圆上**，则最优解就是给定的圆本身。
    * 若点在给定圆**内**，则最优解的圆心位于从给定圆心指向给定点方向的直径延长线上，且其圆周同时经过给定点并和给定圆内切。
    * 若点与给定圆心**重合**，则无法画出同时满足所有条件的圆，但题目数据范围暗示不会出现此情况，或可视为退化情况。

---

### 代码

```cpp
#include &lt;cstdio&gt;
#include &lt;cmath&gt;

void solve() {
    double R, x1, y1, x2, y2;
    scanf("%lf%lf%lf%lf%lf", &R, &x1, &y1, &x2, &y2);

    // 计算给定圆心到给定点的距离平方
    double d_sq = (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2);
    double d = sqrt(d_sq);

    if (d_sq == 0) {
        // 点与圆心重合：无法画圆满足“点不在圆内”且最小化面积。
        // 按照题意输出一个特殊解（例如半径为0的圆心点）。
        printf("%.6lf %.6lf %.6lf\n", x1, y1, 0.0);
    } else if (d >= R) {
        // 点在圆外或圆上：答案就是给定的圆。
        printf("%.6lf %.6lf %.6lf\n", x1, y1, R);
    } else {
        // 点在圆内：最优解圆心在 (x1,y1) 到 (x2,y2) 的延长线上。
        // 新圆的半径 r = (R + d) / 2，圆心位于两点连线上距离圆心 R 的位置。
        double r = (R + d) / 2.0;
        // 方向向量
        double dir_x = (x2 - x1) / d;
        double dir_y = (y2 - y1) / d;
        // 新圆心坐标：从原圆心向点方向移动 (r - d) 的距离？ 
        // 实际上，新圆心到原圆心的距离为 (r - (R - d)/2) = (R+d)/2 - (R-d)/2 = d。
        // 更直接的方法是：新圆心在连线上，且到原点的距离为 r - (R - d) = (R+d)/2 - (R-d) = (d+R)/2 - (R-d) = (3d - R)/2? 
        // 重新思考：设新圆心为 (xc, yc)，则它到原圆心的距离为 R - r（内切条件），且它到点的距离为 r（点在圆上）。
        // 因此，新圆心位于原圆心与点的连线上，且位于点外侧。具体坐标：
        double xc = x1 + (R - r) * (x2 - x1) / d;
        double yc = y1 + (R - r) * (y2 - y1) / d;
        printf("%.6lf %.6lf %.6lf\n", xc, yc, r);
    }
}

int main() {
    solve();
    return 0;
}
```