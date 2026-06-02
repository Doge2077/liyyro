---
title: "动态规划专题——线性DP"
date: 2022-08-13
categories: [ALGORITHM, DP, Intermediate Algorithm, 线性DP]
description: ""
---

## 1\. 数字三角形模型

---

### 1.1 模板题

---

#### 898\. 数字三角形

[原题链接](&lt;https://www.acwing.com/activity/content/problem/content/1002/&gt;)

**描述**

给定一个如下图所示的数字三角形，从顶部出发，在每一结点可以选择移动至其左下方的结点或移动至其右下方的结点，一直走到底层，要求找出一条路径，使路径上的数字的和最大。
```java


        7
      3   8
    8   1   0
  2   7   4   4
4   5   2   6   5
```

**输入格式** 第一行包含整数 n，表示数字三角形的层数。

接下来 n 行，每行包含若干整数，其中第 i 行表示数字三角形第 i 层包含的整数。

**输出格式** 输出一个整数，表示最大的路径数字和。

**数据范围** 1≤n≤500, −10000≤三角形中的整数≤10000 **输入样例：**
```java


5
7
3 8
8 1 0 
2 7 4 4
4 5 2 6 5
```

**输出样例：**
```java


30
```

**思想**

  * 状态表示： 
```java
* 集合：`dp[i][j]`表示从`a[0,0]`走到`a[i,j]`的路径的数字之和
* 属性：数字之和的最大值
```
  * 状态计算： 
```java
* 对于`a[i][j]`，可以由左上方的点`a[i - 1][j - 1]`或右上方的点`a[i - 1][j]`走到
* 从`a[i - 1][j - 1]`走来：`dp[i][j] = dp[i - 1][j - 1] + a[i][j]`
* 从`a[i - 1][j]`走来：`dp[i][j] = dp[i - 1][j] + a[i][j]`
* 集合属性为数字之和的最大值，取两方案`max()`：`dp[i][j] = max(dp[i - 1][j - 1],dp[i - 1][j]) + a[i][j]`
```



**代码**
```java


#include &lt;bits/stdc++.h&gt;
using namespace std;

const int N = 510;

int dp[N][N];

int a[N][N];

void solve(){

    int n;

    cin >> n ;

    for(int i = 1; i <= n; i ++){
        for(int j = 1; j <= i; j ++){
            cin >> a[i][j];
        }
    }

    memset(dp, -0x3f, sizeof dp);

    dp[1][1] = a[1][1];

    for(int i = 2; i <= n; i ++){
        for(int j = 1; j <= i; j ++){
            dp[i][j] = max(dp[i - 1][j - 1], dp[i -1][j]) + a[i][j]; 
        }
    }

    int res  = -0x3f3f3f3f;

    for(int i = 1; i <= n; i ++){
        res = max(res,dp[n][i]);
    }

    cout << res << endl;

}

int main(){

    solve();

    return 0;

}
```

---

### 1.2 提高练习

---

#### 1015\. 摘花生

[原题链接](&lt;https://www.acwing.com/problem/content/1017/&gt;)

**描述**

Hello Kitty想摘点花生送给她喜欢的米老鼠。

她来到一片有网格状道路的矩形花生地(如下图)，从西北角进去，东南角出来。

地里每个道路的交叉点上都有种着一株花生苗，上面有若干颗花生，经过一株花生苗就能摘走该它上面所有的花生。

Hello Kitty只能向东或向南走，不能向西或向北走。

问Hello Kitty最多能够摘到多少颗花生。

**输入格式** 第一行是一个整数T，代表一共有多少组数据。

接下来是T组数据。

每组数据的第一行是两个整数，分别代表花生苗的行数R和列数 C。

每组数据的接下来R行数据，从北向南依次描述每行花生苗的情况。每行数据有C个整数，按从西向东的顺序描述了该行每株花生苗上的花生数目M。

**输出格式** 对每组输入数据，输出一行，内容为Hello Kitty能摘到得最多的花生颗数。

**数据范围** 1≤T≤100, 1≤R,C≤100, 0≤M≤1000
```java


2
2 2
1 1
3 4
2 3
2 3 4
1 6 5
```

**输出样例：**

**输出样例：**
```java


8
16
```

**思想**

  * 状态表示： 
```java
* 集合：`dp[i][j]`表示从`a[0,0]`走到`a[i,j]`的路径的花生数目之和
* 属性：花生数目之和的最大值
```
  * 状态计算： 
```java
* 对于`a[i][j]`，可以由上方的点`a[i - 1][j]`或左方的点`a[i][j - 1]`走到
* 从`a[i - 1][j]`走来：`dp[i][j] = dp[i - 1][j] + a[i][j]`
* 从`a[i][j - 1]`走来：`dp[i][j] = dp[i][j - 1] + a[i][j]`
* 集合属性为花生数目之和的最大值，取两方案`max()`：`dp[i][j] = max(dp[i - 1][j],dp[i][j - 1]) + a[i][j]`
```



**代码**
```java


#include &lt;bits/stdc++.h&gt;
using namespace std;

const int N = 110;

int mp[N][N];

int dp[N][N];

void solve(){

    int n, m;

    cin >> n >> m;

    for(int i = 1; i <= n; i ++){
        for(int j = 1; j <= m; j ++){
            cin >> mp[i][j];
        }
    }

    dp[1][1] = mp[1][1];

    for(int i = 1; i <= n; i ++){
        for(int j = 1; j <= m; j ++){
            dp[i][j] = max(dp[i - 1][j],dp[i][j - 1]) + mp[i][j];
        }
    }

    cout << dp[n][m] << endl;

}

int main(){

    int _ ;
    cin >> _;
    while(_ --){
        solve();
    }

    return 0;

}
```

---

#### 1018\. 最低通行费

[原题链接](&lt;https://www.acwing.com/problem/content/1020/&gt;)

**描述**

一个商人穿过一个 N×N 的正方形的网格，去参加一个非常重要的商务活动。

他要从网格的左上角进，右下角出。

每穿越中间 1 个小方格，都要花费 1 个单位时间。

商人必须在 (2N−1) 个单位时间穿越出去。

而在经过中间的每个小方格时，都需要缴纳一定的费用。

这个商人期望在规定时间内用最少费用穿越出去。

请问至少需要多少费用？

注意：不能对角穿越各个小方格（即，只能向上下左右四个方向移动且不能离开网格）。

**输入格式** 第一行是一个整数，表示正方形的宽度 N。

后面 N 行，每行 N 个不大于 100 的正整数，为网格上每个小方格的费用。

**输出格式** 输出一个整数，表示至少需要的费用。

**数据范围** 1≤N≤100 **输入样例：**
```java


5
1  4  6  8  10
2  5  7  15 17
6  8  9  18 20
10 11 12 19 21
20 23 25 29 33
```

**输出样例：**
```java


109
```

**思想**

  * 状态表示： 
```java
* 集合：`dp[i][j]`表示从`a[0,0]`走到`a[i,j]`的路径的通行费之和
* 属性：通行费的最小值
```
  * 状态计算： 
```java
* 对于`a[i][j]`，可以由上方的点`a[i - 1][j]`或左方的点`a[i][j - 1]`走到
* 从`a[i - 1][j]`走来：`if(i > 1) dp[i][j] = dp[i - 1][j] + a[i][j]`
* 从`a[i][j - 1]`走来：`if(j > 1) dp[i][j] = dp[i][j - 1] + a[i][j]`
* 集合属性为通行费之和的最大值，取两方案`min()`
* 由于`i - 1`和`j - 1`可能等于$0$，故需要将`dp[N][N]`初始化为`dp[i][j] = 0x3f3f3f3f`
```



**代码**
```java


#include &lt;bits/stdc++.h&gt;
using namespace std;

const int N = 110;

int dp[N][N];

int a[N][N];

void solve(){

    int n;

    cin >> n;

    for(int i = 1; i <= n; i ++){
        for(int j = 1; j <= n; j ++){
            cin >> a[i][j];
        }
    }

    memset(dp, 0x3f, sizeof dp);

    dp[1][1] = a[1][1];

    for(int i = 1; i <= n; i ++){
        for(int j = 1; j <= n; j ++){
            if(i > 1) dp[i][j] = min(dp[i][j], dp[i - 1][j] + a[i][j]);
            if(j > 1) dp[i][j] = min(dp[i][j], dp[i][j - 1] + a[i][j]);
        }
    }

    cout << dp[n][n] << endl;

}

int main(){

    solve();

    return 0;

}
```

---

#### 1027\. 方格取数

[原题链接](&lt;https://www.acwing.com/problem/content/1029/&gt;)

**描述**

设有 N×N 的方格图，我们在其中的某些方格中填入正整数，而其它的方格中则放入数字0。

某人从图中的左上角 A 出发，可以向下行走，也可以向右行走，直到到达右下角的 B 点。

在走过的路上，他可以取走方格中的数（取走后的方格中将变为数字0）。

此人从 A 点到 B 点共走了两次，试找出两条这样的路径，使得取得的数字和为最大。

**输入格式** 第一行为一个整数N，表示 N×N 的方格图。

接下来的每行有三个整数，第一个为行号数，第二个为列号数，第三个为在该行、该列上所放的数。

行和列编号从 1 开始。

一行“0 0 0”表示结束。

**输出格式** 输出一个整数，表示两条路径上取得的最大的和。

**数据范围** N≤10 **输入样例：**
```java


8
2 3 13
2 6 6
3 5 7
4 4 14
5 2 21
5 6 4
6 3 15
7 2 14
0 0 0
```

**输出样例：**
```java


67
```

**思想**

  * 状态表示： 
```java
* 集合：`dp[k][i][j]`表示路径长度为`k`,第一条路线到`i`,第二条路线到`j`的所有方案物品的总价值
* 属性：物品的总价值最大
```
  * 状态计算： 
```java
* 线路1从左方及线路2从左方到达：`dp[k][i][j] = dp[k - 1][i - 1][j - 1] + a[i][j]`
* 线路1从左方及线路2从上方到达：`dp[k][i][j] = dp[k - 1][i - 1][j] + a[i][j]`
* 线路1从上方及线路2从左方到达：`dp[k][i][j] = dp[k - 1][i][j - 1] + a[i][j]`
* 线路1从上方及线路2从上方到达：`dp[k][i][j] = dp[k - 1][i][j] + a[i][j]`
```



**代码**
```java


#include &lt;bits/stdc++.h&gt;
using namespace std;

const int N = 50;

int dp[N][N][N];

int a[N][N];

void solve(){

    int n;

    cin >> n;

    int l, r, x;
    while(cin >> l >> r >> x && l) a[l][r] = x;

    for(int k = 2; k <= 2 * n; k ++){
        for(int i = 1; i <= n; i ++){
            for(int j = 1; j <= n; j ++){
                int &t = dp[k][i][j];
                //越界判断
                if (k - i <= 0 || k - i > n || k - j <= 0 || k - j > n) continue;
                //判断是否两条路线走到了相同的格子
                int v = a[i][k - i];
                if (i != j) v += a[j][k - j];//如果两条路线走到一个格子中，则只累加一次物品的价值
                t = max(t, dp[k - 1][i - 1][j - 1]);
                t = max(t, dp[k - 1][i][j - 1]);
                t = max(t, dp[k - 1][i - 1][j]);
                t = max(t, dp[k - 1][i][j]);
                t += v;

            }
        }
    }

    cout << dp[n * 2][n][n] << endl;

}

int main(){

    solve();

    return 0;

}
```

---

#### 275\. 传纸条

[原题链接](&lt;https://www.acwing.com/problem/content/277/&gt;)

**描述**

小渊和小轩是好朋友也是同班同学，他们在一起总有谈不完的话题。

一次素质拓展活动中，班上同学安排坐成一个 m 行 n 列的矩阵，而小渊和小轩被安排在矩阵对角线的两端，因此，他们就无法直接交谈了。

幸运的是，他们可以通过传纸条来进行交流。

纸条要经由许多同学传到对方手里，小渊坐在矩阵的左上角，坐标 (1,1)，小轩坐在矩阵的右下角，坐标 (m,n)。

从小渊传到小轩的纸条只可以向下或者向右传递，从小轩传给小渊的纸条只可以向上或者向左传递。 

在活动进行中，小渊希望给小轩传递一张纸条，同时希望小轩给他回复。

班里每个同学都可以帮他们传递，但只会帮他们一次，也就是说如果此人在小渊递给小轩纸条的时候帮忙，那么在小轩递给小渊的时候就不会再帮忙，反之亦然。 

还有一件事情需要注意，全班每个同学愿意帮忙的好感度有高有低（注意：小渊和小轩的好心程度没有定义，输入时用 0 表示），可以用一个 0∼100 的自然数来表示，数越大表示越好心。

小渊和小轩希望尽可能找好心程度高的同学来帮忙传纸条，即找到来回两条传递路径，使得这两条路径上同学的好心程度之和最大。

现在，请你帮助小渊和小轩找到这样的两条路径。

**输入格式** 第一行有 2 个用空格隔开的整数 m 和 n，表示学生矩阵有 m 行 n 列。

接下来的 m 行是一个 m×n 的矩阵，矩阵中第 i 行 j 列的整数表示坐在第 i 行 j 列的学生的好心程度，每行的 n 个整数之间用空格隔开。

**输出格式** 输出一个整数，表示来回两条路上参与传递纸条的学生的好心程度之和的最大值。

**数据范围** 1≤n,m≤50 **输入样例：**
```java


3 3
0 3 9
2 8 5
5 7 0
```

**输出样例：**
```java


34
```

**思想**

  * 同方格取数
  * 唯一区别在于两条路径都经过的点可以找到额外的一条或两条路线，使得新的路线不发生重合



**代码**
```java


#include &lt;bits/stdc++.h&gt;
using namespace std;

const int N = 100;

int dp[N][N][N];

int a[N][N];

void solve(){

    int n, m;

    cin >> n >> m;

    for(int i = 1; i <= n; i ++){
        for(int j = 1; j <= m; j ++){
            cin >> a[i][j];
        }
    }

    for(int k = 2; k <= n + m; k ++){
        for(int i = 1; i <= n; i ++){
            for(int j = 1; j <= n; j ++){
                int &t = dp[k][i][j];
                //判断是否两条路线走到了相同的格子
                int v = a[i][k - i];
                if (i != j) v += a[j][k - j];//如果两条路线走到一个格子中，则只累加一次物品的价值
                t = max(t, dp[k - 1][i - 1][j - 1]);
                t = max(t, dp[k - 1][i][j - 1]);
                t = max(t, dp[k - 1][i - 1][j]);
                t = max(t, dp[k - 1][i][j]);
                t += v;

            }
        }
    }

    cout << dp[n + m][n][n] << endl;

}

int main(){

    solve();

    return 0;

}
```

---

## 2\. 最长上升子序列模型

---

### 2.1 模板题

---

#### 895\. 最长上升子序列 I

[原题链接](&lt;https://www.acwing.com/solution/content/10483/&gt;)

**描述**

给定一个长度为 N 的数列，求数值严格单调递增的子序列的长度最长是多少。

**输入格式** 第一行包含整数 N。

第二行包含 N 个整数，表示完整序列。

**输出格式** 输出一个整数，表示最大长度。

**数据范围** 1≤N≤1000， −109≤数列中的数≤109 **输入样例：**
```java


7
3 1 2 1 8 5 6
```

**输出样例：**
```java


4
```

**思想**

  * 状态表示： 
```java
* 集合：`dp[i]`表示以`a[i]`结尾的上升子序列的集合
* 属性： 集合中的上升子序列长度的最大值
```
  * 状态计算： 
```java
* 枚举`a[j]`为上升子序列的倒数第二个数，最小长度为`dp[i] = 1`
* 若 `a[j] < a[i]` 则 `dp[i] = max(dp[i], dp[j] + 1)`
```



**代码**
```java


#include &lt;bits/stdc++.h&gt;
using namespace std;

const int N = 1010;

int a[N];

int dp[N];

void solve(){

    int n;

    cin >> n;

    for(int i = 1; i <= n; i ++) cin >> a[i];

    int res = 0;

    for(int i = 1; i <= n; i ++){
        dp[i] = 1;
        for(int j = 1; j < i; j ++){
            if(a[i] > a[j]) dp[i] = max(dp[i],dp[j] + 1);
        }

        res = max(res,dp[i]);

    }

    cout << res << endl;

}

int main(){

    solve();

    return 0;

}
```

---

#### 896\. 最长上升子序列 II

[原题链接](&lt;https://www.acwing.com/problem/content/898/&gt;)

**描述**

给定一个长度为 N 的数列，求数值严格单调递增的子序列的长度最长是多少。

**输入格式** 第一行包含整数 N。

第二行包含 N 个整数，表示完整序列。

**输出格式** 输出一个整数，表示最大长度。

**数据范围** 1≤N≤100000， −109≤数列中的数≤109 **输入样例：**
```java


7
3 1 2 1 8 5 6
```

**输出样例：**
```java


4
```

**思想**

  * 贪心
  * 较小的数开头的数作为的子序列优于较大的数作为开头的子序列
  * 数组`q[N]`，存储以长度为`i`的上升子序列中末尾元素最小的数
  * `q[N]`初始为空，长度为0
  * 枚举每个数`x`，对于当前数`x`, 二分找到一个最大的小于等于当前数的数
  * 先定义边界，`l = 0, r = res`, 其中`res`是`q[N]`的长度
  * `r + 1 > res `时, 表示超出了二分边界，这时就要`res ++`更新`q[N]`的长度



**代码**
```java


#include &lt;bits/stdc++.h&gt;
using namespace std;

const int N = 1e6 + 3;

int n;

int a[N],  q[N];

void solve(){

    cin >> n;

    for(int i = 0; i < n; i ++) cin >> a[i];

    int res = 0;

    for(int i = 0; i < n; i ++){
        int l = 0, r = res;
        while(l < r){
            int mid = l + r + 1 >> 1;
            if(q[mid] < a[i]) l = mid;
            else r = mid - 1;
        }
        q[r + 1] = a[i];
        res = r + 1 > res ? res + 1 : res;
    }

    cout << res << endl;

}

int main(){

    solve();

    return 0;

}
```

---

#### 897\. 最长公共子序列

[原题链接](&lt;https://www.acwing.com/problem/content/899/&gt;)

**描述**

给定两个长度分别为 N 和 M 的字符串 A 和 B，求既是 A 的子序列又是 B 的子序列的字符串长度最长是多少。

**输入格式** 第一行包含两个整数 N 和 M。

第二行包含一个长度为 N 的字符串，表示字符串 A。

第三行包含一个长度为 M 的字符串，表示字符串 B。

字符串均由小写字母构成。

**输出格式** 输出一个整数，表示最大长度。

**数据范围** 1≤N,M≤1000 **输入样例：**
```java


4 5
acbd
abedc
```

**输出样例：**
```java


3
```

**思想**

  * 状态表示： 
```java
* 集合：`dp[i][j]`表示`a[i]`前`i`个字母和`b[i]`前`j`个字母的公共子序列长度
* 属性：最大长度
```
  * 状态计算： 
```java
* 字母相同：`dp[i][j] = dp[i - 1][j - 1] + 1`
* 字母不同：
* `dp[i][j] = dp[i - 1][j]`
* `dp[i][j] = dp[i][j - 1]`
* 集合属性为最大值：上述方案取`max()`
```



**代码**
```java


#include &lt;bits/stdc++.h&gt;
using namespace std;

const int N = 1010;

int dp[N][N];

char a[N],b[N];

void solve(){

    int n, m;
    cin >> n >> m >> a + 1 >> b + 1;

    for(int i = 1; i <= n; i ++){
        for(int j = 1; j <=m; j ++){
            dp[i][j] = max(dp[i][j - 1],dp[i - 1][j]);
            dp[i][j] = max(dp[i][j], dp[i - 1][j - 1] + (a[i] == b[j]));
        }
    }

    cout << dp[n][m] << endl;

}

int main(){

    solve();

    return 0;

}
```

---

#### 902\. 最短编辑距离

[原题链接](&lt;https://www.acwing.com/problem/content/904/&gt;)

**描述**

给定两个字符串 A 和 B，现在要将 A 经过若干操作变为 B，可进行的操作有：

删除–将字符串 A 中的某个字符删除。 插入–在字符串 A 的某个位置插入某个字符。 替换–将字符串 A 中的某个字符替换为另一个字符。 现在请你求出，将 A 变为 B 至少需要进行多少次操作。

**输入格式** 第一行包含整数 n，表示字符串 A 的长度。

第二行包含一个长度为 n 的字符串 A。

第三行包含整数 m，表示字符串 B 的长度。

第四行包含一个长度为 m 的字符串 B。

字符串中均只包含大小写字母。

**输出格式** 输出一个整数，表示最少操作次数。

**数据范围** 1≤n,m≤1000 **输入样例：**
```java


10 
AGTCTGACGC
11 
AGTAAGTAGGC
```

**输出样例：**
```java


4
```

**思想**

  * 状态表示： 
```java
* 集合：`dp[i][j]`表示`a[N]`中的前`i`个字母变成 `b[N]`中前`j`个字母的操作集合
* 属性：操作的最小次数
```
  * 状态计算： 
```java
* 添加字母：添加一个字母之后变得相同，说明没有添加前，`a[N]`的前`i`个字母已经和`b[N]`的前j`j - 1`个字母已经相同，即`dp[i][j] = dp[i][j - 1] + 1`
* 删除字母：删除一个字母之后变得相同，说明没有添加前，`a[N]`的前`i - 1`个字母已经和`b[N]`的前j`j`个字母已经相同，即`dp[i][j] = dp[i - 1][j] + 1`
* 替换字母：替换说明对应结尾字母不同，则看倒数第二个，即`dp[i][j] = dp[i - 1][j - 1] + 1`
* 集合属性为最小次数，上述方案取`min()`
```
  * 初始化：将添加和删除进行初始化，即`dp[i][0] = i,dp[0][j] = j`



**代码**
```java


#include &lt;bits/stdc++.h&gt;
using namespace std;

const int N = 1010;

int dp[N][N];

char a[N], b[N];

void solve(){

    int n, m;
    cin >> n >> a + 1 >> m >> b + 1;

    for(int i = 1; i <= max(n,m); i ++) dp[i][0] = dp[0][i] = i;

    for(int i = 1; i <= n; i ++){
        for(int j = 1; j <= m; j ++){
            dp[i][j] = min(dp[i - 1][j],dp[i][j - 1]) + 1;
            dp[i][j] = min(dp[i][j],dp[i - 1][j - 1] + (a[i] != b[j]));
        }
    }

    cout << dp[n][m] << endl;

}

int main(){

    solve();

    return 0;

}
```

---

### 2.2 提高练习

---

#### 899\. 编辑距离

[原题链接](&lt;https://www.acwing.com/problem/content/901/&gt;)

**描述**

给定 n 个长度不超过 10 的字符串以及 m 次询问，每次询问给出一个字符串和一个操作次数上限。

对于每次询问，请你求出给定的 n 个字符串中有多少个字符串可以在上限操作次数内经过操作变成询问给出的字符串。

每个对字符串进行的单个字符的插入、删除或替换算作一次操作。

**输入格式** 第一行包含两个整数 n 和 m。

接下来 n 行，每行包含一个字符串，表示给定的字符串。

再接下来 m 行，每行包含一个字符串和一个整数，表示一次询问。

字符串中只包含小写字母，且长度均不超过 10。

**输出格式** 输出共 m 行，每行输出一个整数作为结果，表示一次询问中满足条件的字符串个数。

**数据范围** 1≤n,m≤1000,

**输入样例：**
```java


3 2
abc
acd
bcd
ab 1
acbd 2
```

**输出样例：**
```java


1
3
```

**思想**

  * 同**902\. 最短编辑距离**
  * 区别在于，对于每次询问，遍历所有的原字符串，进行计算



**代码**
```java


#include &lt;bits/stdc++.h&gt;
using namespace std;

const int N = 20;

const int M = 1e3 + 10;

int n, _;

char str[M][N];

int dp[N][N];

int ans(char a[], char b[]){
    int l = strlen(a + 1), r = strlen(b + 1);

    for(int i = 1; i <= max(l,r); i ++) dp[i][0] = dp[0][i] = i;

    for (int i = 1; i <= l; i++) {
        for (int j = 1; j <= r; j++) {
            dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1);
            dp[i][j] = min(dp[i][j], dp[i - 1][j - 1] + (a[i] != b[j]));
        }
    }

    return dp[l][r];

}

void solve(){

    int cnt = 0, p = 0;

    char s[N];

    cin >> (s + 1) >> p;

    for (int i = 0; i < n; i++) if(ans(str[i],s) <= p) cnt ++;

    cout << cnt << endl;

}

int main(){

    cin >> n >> _;

    for (int i = 0; i < n; i++) cin >> (str[i] + 1);

    while(_ --) {
        solve();
    }

    return 0;
}

```

---

#### 1017\. 怪盗基德的滑翔翼

[原题链接](&lt;https://www.acwing.com/problem/content/1019/&gt;)

**描述**

假设城市中一共有N幢建筑排成一条线，每幢建筑的高度各不相同。

初始时，怪盗基德可以在任何一幢建筑的顶端。

他可以选择一个方向逃跑，但是不能中途改变方向（因为中森警部会在后面追击）。

因为滑翔翼动力装置受损，他只能往下滑行（即：只能从较高的建筑滑翔到较低的建筑）。

他希望尽可能多地经过不同建筑的顶部，这样可以减缓下降时的冲击力，减少受伤的可能性。

请问，他最多可以经过多少幢不同建筑的顶部(包含初始时的建筑)？

**输入格式** 输入数据第一行是一个整数K，代表有K组测试数据。

每组测试数据包含两行：第一行是一个整数N，代表有N幢建筑。第二行包含N个不同的整数，每一个对应一幢建筑的高度h，按照建筑的排列顺序给出。

**输出格式** 对于每一组测试数据，输出一行，包含一个整数，代表怪盗基德最多可以经过的建筑数量。

**数据范围** 1≤K≤100, 1≤N≤100, 0<h<10000 **输入样例：**
```java


3
8
300 207 155 299 298 170 158 65
8
65 158 170 298 299 155 207 300
10
2 1 3 4 5 6 7 8 9 10
```

**输出样例：**
```java


6
6
9
```

**思想**

  * 最长上升子序列模型
  * 注意可以选择两个方向，故需要从不同方向做两次状态转移



**代码**
```java


#include &lt;bits/stdc++.h&gt;
using namespace std;

const int N = 110;

int dp1[N],dp2[N];

int h1[N], h2[N];

void solve(){

    memset(dp1, 0, sizeof dp1);
    memset(dp2, 0, sizeof dp2);

    int n;
    cin >> n;

    for(int i = 1; i <= n; i ++){
        cin >> h1[i];
        h2[n - i + 1] = h1[i];
    }

    int flag = 0;

    for(int i = 1; i <= n; i ++){
        dp1[i] = dp2[i] = 1;
        for(int j = 1; j < i; j ++){
            if(h1[i] > h1[j]) dp1[i] = max(dp1[i],dp1[j] + 1);
            if(h2[i] > h2[j]) dp2[i] = max(dp2[i],dp2[j] + 1);
        }
        flag = max(flag,max(dp1[i],dp2[i]));
    }

    cout << flag << endl;

}

int main(){

    int _;

    cin >> _;

    while(_ --){
        solve();
    }

    return 0;

}
```

---

#### 1014\. 登山

[原题链接](&lt;https://www.acwing.com/problem/content/1016/&gt;)

**描述**

五一到了，ACM队组织大家去登山观光，队员们发现山上一共有N个景点，并且决定按照顺序来浏览这些景点，即每次所浏览景点的编号都要大于前一个浏览景点的编号。

同时队员们还有另一个登山习惯，就是不连续浏览海拔相同的两个景点，并且一旦开始下山，就不再向上走了。

队员们希望在满足上面条件的同时，尽可能多的浏览景点，你能帮他们找出最多可能浏览的景点数么？

**输入格式** 第一行包含整数N，表示景点数量。

第二行包含N个整数，表示每个景点的海拔。

**输出格式** 输出一个整数，表示最多能浏览的景点数。

**数据范围** 2≤N≤1000 **输入样例：**
```java


8
186 186 150 200 160 130 197 220
```

**输出样例：**
```java


4
```

**思想**

  * 先分别求正序和倒序的最长上升公共子序列
  * `flag != 1`时，遍历`dp1[N]`和`dp2[N]`，最大值即为`max(dp1[i],dp[n - i + 1])`
  * 由于当`n`为偶数时，`i = n / 2 `时`i == n - i + 1`，会重复计算一个点，故`if(n % 2 == 0 && flag != n) flag --`



**代码**
```java


#include &lt;bits/stdc++.h&gt;
using namespace std;

const int N = 1010;

int dp1[N],dp2[N];

int h1[N], h2[N];

bool vis1[N], vis2[N];

void solve(){

    int n;
    cin >> n;

    for(int i = 1; i <= n; i ++){
        cin >> h1[i];
        h2[n - i + 1] = h1[i];
    }

    int flag = 0;

    for(int i = 1; i <= n; i ++){
        dp1[i] = dp2[i] = 1;
        for(int j = 1; j < i; j ++){
            if(h1[i] > h1[j]) dp1[i] = max(dp1[i],dp1[j] + 1);
            if(h2[i] > h2[j]) dp2[i] = max(dp2[i],dp2[j] + 1);
        }

        flag = max(flag, max(dp1[i], dp2[i]));

    }

    if(flag != 1) for(int i = 1; i <= n; i ++){
        if(dp1[i] != 1 && dp2[i] != 1) flag = max(flag,dp1[i] + dp2[n - i + 1]);
    }

    if(n % 2 == 0 && flag != n) flag --;

    cout << flag << endl;

}

int main(){

    solve();

    return 0;

}
```

---

#### 482\. 合唱队形

[原题链接](&lt;https://www.acwing.com/problem/content/484/&gt;)

**描述**

N 位同学站成一排，音乐老师要请其中的 (N−K) 位同学出列，使得剩下的 K 位同学排成合唱队形。 

合唱队形是指这样的一种队形：设 K 位同学从左到右依次编号为 1，2…，K，他们的身高分别为 T1，T2，…，TK， 则他们的身高满足 T1<…Ti+1>…>TK(1≤i≤K)。 

你的任务是，已知所有 N 位同学的身高，计算最少需要几位同学出列，可以使得剩下的同学排成合唱队形。

**输入格式** 输入的第一行是一个整数 N，表示同学的总数。

第二行有 N 个整数，用空格分隔，第 i 个整数 Ti 是第 i 位同学的身高(厘米)。

**输出格式** 输出包括一行，这一行只包含一个整数，就是最少需要几位同学出列。

**数据范围** 2≤N≤100, 130≤Ti≤230 **输入样例：**
```java


8
186 186 150 200 160 130 197 220
```

**输出样例：**
```java


4
```

**思想**

  * 先分别求正序和倒序的最长上升公共子序列
  * `flag != 1`时，遍历`dp1[N]`和`dp2[N]`，能排列成合唱队的最大人数为`max(dp1[i],dp[n - i + 1])`
  * 由于当`n`为偶数时，`i = n / 2 `时`i == n - i + 1`，会重复计算一个人，故`if(n % 2 == 0 && flag != n) flag --`



**代码**
```java


#include &lt;bits/stdc++.h&gt;
using namespace std;

const int N = 1010;

int dp1[N],dp2[N];

int h1[N], h2[N];

bool vis1[N], vis2[N];

void solve(){

    int n;
    cin >> n;

    for(int i = 1; i <= n; i ++){
        cin >> h1[i];
        h2[n - i + 1] = h1[i];
    }

    int flag = 0;

    for(int i = 1; i <= n; i ++){
        dp1[i] = dp2[i] = 1;
        for(int j = 1; j < i; j ++){
            if(h1[i] > h1[j]) dp1[i] = max(dp1[i],dp1[j] + 1);
            if(h2[i] > h2[j]) dp2[i] = max(dp2[i],dp2[j] + 1);
        }

        flag = max(flag, max(dp1[i], dp2[i]));

    }

    if(flag != 1) for(int i = 1; i <= n; i ++){
        flag = max(flag,dp1[i] + dp2[n - i + 1]);
    }

    if(n % 2 == 0) flag --;

    cout << n - flag << endl;

}

int main(){

    solve();

    return 0;

}
```

---

#### 1012\. 友好城市

[原题链接](&lt;https://www.acwing.com/problem/content/1014/&gt;)

**描述**

Palmia国有一条横贯东西的大河，河有笔直的南北两岸，岸上各有位置各不相同的N个城市。

北岸的每个城市有且仅有一个友好城市在南岸，而且不同城市的友好城市不相同。

每对友好城市都向政府申请在河上开辟一条直线航道连接两个城市，但是由于河上雾太大，政府决定避免任意两条航道交叉，以避免事故。

编程帮助政府做出一些批准和拒绝申请的决定，使得在保证任意两条航线不相交的情况下，被批准的申请尽量多。

**输入格式** 第1行，一个整数N，表示城市数。

第2行到第n+1行，每行两个整数，中间用1个空格隔开，分别表示南岸和北岸的一对友好城市的坐标。

输出格式 仅一行，输出一个整数，表示政府所能批准的最多申请数。

**数据范围** 1≤N≤5000, 0≤xi≤10000 **输入样例：**
```java


7
22 4
2 6
10 3
15 12
9 8
17 17
4 2
```

**输出样例：**
```java


4
```

**思想**

  * `pair&lt;int,int&gt; a[N]`存储友好城市关系，`a[i].first`与`a[i].second`为友好城市
  * 将其中一个城市的坐标从小到大排序，另一个城市的最长上升子序列的长度即为答案



**代码**
```java


#include &lt;bits/stdc++.h&gt;
using namespace std;

const int N = 1e6 + 3;

int dp[N];

pair&lt;int,int&gt; a[N];

void solve(){

    int n;

    cin >> n;

    for(int i = 1; i <= n; i ++) cin >> a[i].first >> a[i].second;

    sort(a + 1, a + n + 1);

    int res = 0;

    for(int i = 1; i <= n; i ++){
        dp[i] = 1;
        for(int j = 1; j < i; j ++){
            if(a[i].second > a[j].second) dp[i] = max(dp[i],dp[j] + 1);
        }
        res = max(res,dp[i]);
    }

    cout << res << endl;

}

int main(){

    solve();

    return 0;

}
```

---

#### 1016\. 最大上升子序列和

[原题链接](&lt;https://www.acwing.com/problem/content/1018/&gt;)

**描述**

一个数的序列 bi，当 b1<b2<…<bS 的时候，我们称这个序列是上升的。

对于给定的一个序列(a1,a2,…,aN)，我们可以得到一些上升的子序列(ai1,ai2,…,aiK)，这里1≤i1<i2<…<iK≤N。

比如，对于序列(1,7,3,5,9,4,8)，有它的一些上升子序列，如(1,7),(3,4,8)等等。

这些子序列中和最大为18，为子序列(1,3,5,9)的和。

你的任务，就是对于给定的序列，求出最大上升子序列和。

注意，最长的上升子序列的和不一定是最大的，比如序列(100,1,2,3)的最大上升子序列和为100，而最长上升子序列为(1,2,3)。

**输入格式** 输入的第一行是序列的长度N。

第二行给出序列中的N个整数，这些整数的取值范围都在0到10000(可能重复)。

**输出格式** 输出一个整数，表示最大上升子序列和。

**数据范围** 1≤N≤1000 **输入样例：**
```java


7
1 7 3 5 9 4 8
```

**输出样例：**
```java


18
```

**思想**

  * 状态表示： 
```java
* 集合：`dp[i]`表示以`a[i]`结尾的上升子序列的**和** 的集合
* 属性： 集合中的上升子序列和的最大值
```
  * 状态计算： 
```java
* 枚举`a[j]`为上升子序列的倒数第二个数，最小值之和为`dp[i] = a[i]`
* 若 `a[j] < a[i]` 则 `dp[i] = max(dp[i], dp[j] + a[i])`
```



**代码**
```java


#include &lt;bits/stdc++.h&gt;
using namespace std;

const int N = 1e6 + 3;

int dp[N];

int a[N];

void solve(){

    int n;
    cin >> n;

    for(int i = 1; i <= n; i ++) cin >> a[i];

    int res = 0;

    for(int i = 1; i <= n; i ++){
        dp[i] = a[i];
        for(int j = 1; j < i; j ++){
            if(a[i] > a[j]) dp[i] = max(dp[i],dp[j] + a[i]);
        }
        res = max(res,dp[i]);
    }

    cout << res << endl;

}

int main(){

    solve();

    return 0;

}
```

---

#### 1010\. 拦截导弹

[原题链接](&lt;https://www.acwing.com/problem/content/1012/&gt;)

**描述**

某国为了防御敌国的导弹袭击，发展出一种导弹拦截系统。

但是这种导弹拦截系统有一个缺陷：虽然它的第一发炮弹能够到达任意的高度，但是以后每一发炮弹都不能高于前一发的高度。

某天，雷达捕捉到敌国的导弹来袭。

由于该系统还在试用阶段，所以只有一套系统，因此有可能不能拦截所有的导弹。

输入导弹依次飞来的高度（雷达给出的高度数据是不大于30000的正整数，导弹数不超过1000），计算这套系统最多能拦截多少导弹，如果要拦截所有导弹最少要配备多少套这种导弹拦截系统。

**输入格式** 共一行，输入导弹依次飞来的高度。

**输出格式** 第一行包含一个整数，表示最多能拦截的导弹数。

第二行包含一个整数，表示要拦截所有导弹最少要配备的系统数。

**数据范围** 雷达给出的高度数据是不大于 30000 的正整数，导弹数不超过 1000。

**输入样例：**
```java


389 207 155 300 299 170 158 65
```

**输出样例：**
```java


6
2
```

**思想**

  * 对于第一问，即求最长不上升子序列
  * 对于第二问，即求最长上升子序列



**代码**
```java


#include &lt;bits/stdc++.h&gt;
using namespace std;

const int N = 1e6 + 3;

int dp[N];

int f[N];

int a[N];

void solve(){

    int cnt = 1;

    while(cin >> a[cnt]) cnt ++;

    int res = 0, ans = 0;

    for(int i = 1; i < cnt; i ++){
        dp[i] = f[i] = 1;
        for(int j = 1; j < i; j ++){
            if(a[i] <= a[j]) dp[i] = max(dp[i],dp[j] + 1);
            else f[i] = max(f[i],f[j] + 1);
        }
        res = max(res,dp[i]);
        ans = max(ans,f[i]);
    }

    cout << res << endl << ans << endl;

}

int main(){

    solve();

    return 0;

}
```

---

#### 272\. 最长公共上升子序列

[原题链接](&lt;https://www.acwing.com/problem/content/274/&gt;)

**描述**

熊大妈的奶牛在小沐沐的熏陶下开始研究信息题目。

小沐沐先让奶牛研究了最长上升子序列，再让他们研究了最长公共子序列，现在又让他们研究最长公共上升子序列了。

小沐沐说，对于两个数列 A 和 B，如果它们都包含一段位置不一定连续的数，且数值是严格递增的，那么称这一段数是两个数列的公共上升子序列，而所有的公共上升子序列中最长的就是最长公共上升子序列了。

奶牛半懂不懂，小沐沐要你来告诉奶牛什么是最长公共上升子序列。

不过，只要告诉奶牛它的长度就可以了。

数列 A 和 B 的长度均不超过 3000。

**输入格式** 第一行包含一个整数 N，表示数列 A，B 的长度。

第二行包含 N 个整数，表示数列 A。

第三行包含 N 个整数，表示数列 B。

**输出格式** 输出一个整数，表示最长公共上升子序列的长度。

**数据范围** 1≤N≤3000,序列中的数字均不超过 231−1。

**输入样例：**
```java


4
2 2 1 3
2 1 2 3
```

**输出样例：**
```java


2
```

**思想**

  * 状态表示： 
```java
* 集合：`dp[i][j]`表示`a[N]`中前`i`个数字，`b`中前`j`个数字 ，且当前以`b[j]`结尾的公共上升子序列的长度
* 属性：公共上升子序列的长度的最大值
```
  * 状态计算： 
```java
* 依据公共子序列中是否包含`a[i]`，将`dp[i][j]`所代表的集合划分成两个不重不漏的子集
* 不包含`a[i]`的子集，最大值是`dp[i][j] = dp[i - 1][j]`
* 包含`a[i]`的子集，将该子集继续划分，依据是子序列的倒数第二个元素在`b[N]`中是哪个数：
* 子序列只包含`b[j]`一个数，长度是1；
* 子序列的倒数第二个数是`b[1]`的集合，最大长度是`dp[i - 1][1] + 1`；
* …
* 子序列的倒数第二个数是`b[j - 1]`的集合，最大长度是`dp[i - 1][j - 1] + 1`；
* 即包含`a[i]`的子集，最大值是 `dp[i][j] = max(dp[i][j], dp[i - 1][k] + 1)`
* 由于包含`a[i]`的子集在进行状态计算时用到的状态都是第`i - 1`个阶段的状态，故可以利用`maxn`来承接`a[i]`前面的最大的状态值
```



**代码**
```java


#include &lt;bits/stdc++.h&gt;
using namespace std;

const int N = 3080;

int dp[N][N];

int a[N], b[N];

void solve(){

    int n;
    cin >> n;

    for(int i = 1; i <= n; i ++) cin >> a[i];
    for(int i = 1; i <= n; i ++) cin >> b[i];

    int res = 0;

    for(int i = 1; i <= n; i ++){
        int maxn = 1;
        for(int j = 1; j <= n; j ++){
            dp[i][j] = dp[i - 1][j];
            if(a[i] == b[j]) dp[i][j] = max(maxn,dp[i][j]);
            if(a[i] > b[j]) maxn = max(maxn,dp[i - 1][j] + 1);
        }
    }

    for (int i = 0; i <= n; i ++) res = max(res, dp[n][i]);

    cout << res << endl;

}

int main(){

    solve();

    return 0;

}
```
