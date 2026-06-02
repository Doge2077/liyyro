---
title: "河南工程学院2022级新生周赛（五）题解"
date: 2022-10-23
categories: [Q&amp;A, 二分, University Activities, 思维]
description: ""
---

## A. HF 的智能小车车

* * *

[原题链接](&lt;http://www.haueacm.top/problem.php?id=1390&gt;)

**描述** ：

众嗦粥汁，$HF$ 最近天天泡在实验室里做他的智能小车车，但在调试的时候发现控制转向和行进的指令搞混了。这种小事对他来说太简单了，用他的原话说就是："有手就行"，于是他就懒得继续做下去了。

$HF$ 把这个做了一半的车子丢给了 $LYS$，如果他能解决掉这些问题，这个智能小车车就归 $LYS$ 辣。

以下是需要解决的问题：

  * 当输入右转向指令为 `R` 时，执行左转指令 `L`，反之亦然。
  * 当输入前进指令为 `U` 时，执行向后退指令 `D`，反之亦然。



$LYS$ 肥肠想要这个小车车，可是他啥也不会，现在他来找你帮忙了，你能帮帮他吗？

**输入格式** ：

一行，一个字符 $P$，表示输入的指令。

**输出格式** ：

一行，一个字符，表示执行的指令。

**数据范围** ：

$P={R,L,U,D}$。

**样例输入** ：
```java


R
```

**样例输出** ：
```java


L
```

**思想** ：

  * 签到题。



**代码** ：
```java


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

#define IOS ios::sync_with_stdio(false),cin.tie(nullptr),cout.tie(nullptr)
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

void solve(){

    char op; cin >> op;
    if(op == 'R') cout << 'L' << endl;
    else if(op == 'L') cout << 'R' << endl;
    else if(op == 'U') cout << 'D' << endl;
    else cout << 'U' << endl;
}

int main(){

    IOS;

    int _ = 1;

    // cin >> _;

    while(_ --){
        solve();
    }

    return 0;

}
```

* * *

## B. Do you like Van game?

* * *

[原题链接](&lt;http://www.haueacm.top/problem.php?id=1391&gt;)

**描述** ：

野兽仙贝想跟你 $Van$ 一个游戏，要是你赢了就能让你嘿嘿嘿，反之亦然。

野兽仙贝拿出了三个超大号皮搋子放在桌上，分别编号为 $1,2,3$，初始对应位置编号也为 $1,2,3$。其中某个的皮搋子下面藏着一个扩音器。

游戏规则：

  * 游戏一共进行 $k$ 轮。 
  * 第 $k_i$ 轮，仙贝会交换某编号为 $n_i,m_i$ 的皮搋子的位置，若皮搋子下有扩音器，扩音器也会跟着移动。
  * 一轮交换结束，你可以猜一个位置 $P_i$。
  * 若猜中了扩音器的位置，则本轮得一分，否则不得分。

野兽仙贝其实很想让你赢，所以游戏开始前，他就尽可能的把扩音器放到了你可以得最高分数的位置，现在请你计算出你最高的得分。




**输入格式** ：

第一行，一个整数 $k$，代表游戏进行几轮。

接下来 $k$ 行，每行输入两个整数 $n_i,m_i$ 和一个整数 $P_i$，分别代表皮搋子的编号和你所猜的扩音器的位置编号。

**输出格式** ：

一行，一个整数，表示你可能得到的最高分数。

**数据范围** ：

$1\le k\le 100$，$1\le n_i,m_i,P_i\le 3$。

**输入样例** ：
```java


3
1 2 1
3 2 1
1 3 1
```

**输出样例** ：
```java


2
```

**提示** ：

若扩音器最开始在皮搋子 $1$ 下面，最终你在第三轮猜中一次。

若扩音器最开始在皮搋子 $2$ 下面，最终你在第一轮和第二轮猜中，共两次。

若扩音器最开始在皮搋子 $3$ 下面，最终一次也没有猜中。

**思想1** ：

  * 暴力模拟。
  * 枚举初始位置，模拟在该开局的条件下的得分。


```java


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

#define IOS ios::sync_with_stdio(false),cin.tie(nullptr),cout.tie(nullptr)
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

int pos[N];

struct Operator{
    int l, r, p;
}op[N];

void solve(){

    int n; cin >> n;

    for(int i = 1; i <= n; i ++){
        int a, b, c; cin >> a >> b >> c;
        op[i] = {a, b, c};
    }

    int ans = 0;

    for(int i = 1; i <= 3; i ++){
        pos[1] = pos[2] = pos[3] = 0;
        pos[i] = 1;
        int cnt = 0;
        for(int j = 1; j <= n; j ++){
            swap(pos[op[j].l], pos[op[j].r]);
            cnt += pos[op[j].p];
        }
        ans = max(ans, cnt);
    }

    cout << ans << endl;

}

int main(){

    IOS;

    int _ = 1;

    // cin >> _;

    while(_ --){
        solve();
    }

    return 0;

}
```

**思想2** ：

  * 思维题。 
  * 设位置数组为 `pos[N]`，初始时位置 `i` 上的皮搋子编号为 `i`，即 `pos[1] = 1` 表示位置 $1$ 上的皮搋子编号为 $1$。
  * 设答案数组为 `ans[N]`，表示编号为 `i` 的皮搋子被猜中多少次。
  * 用 `swap()` 交换位置上的皮搋子，而询问的位置上的皮搋子对应的编号被猜中，记录次数。
  * 最后比较哪个编号的皮搋子在交换时被猜中的次数最多，那么一开始扩音器就在这个皮搋子下。



**代码2** ：
```java


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

#define IOS ios::sync_with_stdio(false),cin.tie(nullptr),cout.tie(nullptr)
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

int ans[N], pos[N];

void solve(){

    int n; cin >> n;

    for(int i = 1; i <= 3; i ++) pos[i] = i;

    for(int i = 0; i < n; i ++){
        int a, b, c; cin >> a >> b >> c;
        swap(pos[a], pos[b]);
        ans[pos[c]] ++;
    }

    cout << max(ans[1], max(ans[2], ans[3])) << endl;

}

int main(){

    IOS;

    int _ = 1;

    // cin >> _;

    while(_ --){
        solve();
    }

    return 0;

}
```

* * *

## C. 好姐姐的三角形

* * *

[原题链接](&lt;http://www.haueacm.top/problem.php?id=1393&gt;)

**描述** ：

三角形给人一种稳固的感觉，我们的好姐姐 $WJX$ 最喜欢三角形了，现在她想用一些字母拼出来等腰三角形，你能帮帮她吗？

**输入格式** ：

第一行，一个整数 $t$，表示样例数量。

接下来 $t$ 行，第 $t_i$ 行输入一个整数 $n_i$ 和一个字符 $c_i$，分别表示三角形的高度和用来拼成三角形的字符。

**输出格式** ：

共 $t$ 行，每行用所给字符输出对应高度的等腰三角形。

每个样例之间空一行。

**数据范围** ：

$1\le t,n_i\le 10$。

**样例输入** ：
```java


2
2 A
3 B
```

**样例输出** ：
```java


 A
AAA

  B
 B B
BBBBB
```

**思想** ：

  * 模拟。



**代码** ：
```java


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

#define IOS ios::sync_with_stdio(false),cin.tie(nullptr),cout.tie(nullptr)
#define re register
#define fi first
#define se second
#define endl '\n'

typedef long long LL;
typedef pair&lt;int, int&gt; PII;
typedef pair&lt;LL, LL&gt; PLL;

const int N = 1e6 + 3;
const int INF = 0x3f3f3f3f, mod = 1804;
const double eps = 1e-6, PI = acos(-1);

void solve(){

    int n; char op;
    cin >> n >> op;

    for(int i = 1; i <= n; i ++){
        if(i <= n - 1){  //不是最后一行时
            for(int j = n - i - 1; j >= 0; j --) cout << ' ';  //输出前面的空格
            cout << op;
            for(int j = 1; j <= (i - 1) * 2 - 1; j ++) cout << ' ';  //输出中间的空格
            if(i > 1) cout << op << endl;  //不是第一行再输出一个字符
            else cout << endl;
        }
        else{
            for(int j = 1; j <= i * 2 - 1; j ++) cout << op;  //最后一行不含空格
            cout << endl;
        }
    }

    cout << endl;

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

* * *

## D. 帮帮小陈

* * *

[原题链接](&lt;http://www.haueacm.top/problem.php?id=1394&gt;)

**描述** ：

我们的好姐姐 $WJX$ 在拼三角形的时候突发奇想，想要考考小陈同学，假如有 $n$ 个整数 $i$，以这 $n$ 个整数中的三个整数为边长能够构成多少个三角形？

结果小陈同学一时大意，不小心被难住了，你能帮帮他吗？

**输入格式** ：

第一行一个整数 $t$ ，表示 $t$ 个测试样例。

每个样例第一行一个整数 $n$，表示有 $n$ 个可选的边

每个样例第二行 $n$个整数 $i$，表示三角形的边长。

**输出格式** ：

共 $t$ 行，每行一个整数，表示该测试样例下能构成的三角形的数量。

**数据范围** ：

$1\le t,n, i, \le 1\times 10^3$。

**样例输入** ：
```java


1
4
2 2 3 4
```

**样例输出** ：
```java


3
```

**思想** ：

  * 排序，二分。
  * 将所有的边按照从小到大的顺序排序。
  * 枚举前两个边的长度，二分寻找最大的第三边的位置。
  * 将满足的第三边的总数累加即可。



**代码** ：
```java


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

#define IOS ios::sync_with_stdio(false),cin.tie(nullptr),cout.tie(nullptr)
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

void solve(){

    int n; cin >> n;
    for(int i = 0; i < n; i ++) cin >> a[i];

    sort(a, a + n);  //排序

    LL sum = 0;

    for(int i = 0; i + 2 < n; i ++){  //枚举第一个边
        while(a[i] == 0 && i < n) i ++;  //从不是 0 的位置开始
        for(int j = i + 1; j + 1 < n; j ++){  //枚举第二个边
            int l = j + 1, r = n - 1;
            int p = a[i] + a[j];
            while(l < r){  //二分，找到最大的 a[k] < a[i] + a[j]
                int mid = l + r + 1 >> 1;
                if(a[mid] < p) l = mid;
                else r = mid - 1;
            }
            if(a[l] < p) sum += l - j;  //特判一下是否满足
            else sum += l - j - 1;
        }
    }

    cout << sum << endl;

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

* * *

## E. 卷点

* * *

[原题链接](&lt;http://www.haueacm.top/problem.php?id=1395&gt;)

**描述** ：

小陈同学很感谢你的帮助，作为回报，他也给你出了一个有趣的问题。

现在给出一个“卷点”的定义：在一个正方形内存在某一点，使得这个点和正方形四个顶点连接而划分出的四块三角形的面积比为 $a:b:c:d$。四个数不分顺序；卷点不是唯一的。

![](https://cdn.jsdelivr.net/gh/Doge2077/liyyro-photo@main/images/2022/10/卷点.png)

现在有一个正方形，给出 $4$个整数 $a,b,c,d$，表示被某点划分出的四个三角形的面积，判断有多少个这样的卷点在正方形内部？

**输入格式** ：

第一行一个整数 $n$ ，代表 $n$ 个测试样例。

接下来 $n$ 行，每行 $4$ 个整数 $a,b,c,d$，表示四个三角形的面积。

**输出格式** ：

共 $n$ 行，每行一个整数，表示卷点的数量。

**数据范围** ：

$1\le n\le 1\times 10^2$，$1\le a,b,c,d\le1\times10^{18}$。

**样例输入** ：
```java


3
1 3 3 1
2 4 7 8
2 3 1 4
```

**样例输出** ：
```java


4
0
8
```

**思想** ：

  * 思维题。
  * 设 $a,b,c,d$ 非严格单调递增。
  * 则当 $a+d=b+c$ 时： 
```java
* 若 $a=b=c=d$ 时，则只有一个卷点；
* 若 $a=b,a\ne d$ 时，则存在 $4$ 个卷点；
* 若 $a,b,c,d$ 均不相等时，则存在 $8$ 个卷点。
```
  * 其他情况不存在卷点。



**代码** ：
```java


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

#define IOS ios::sync_with_stdio(false),cin.tie(nullptr),cout.tie(nullptr)
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

LL a[N];

void solve(){

    for(int i = 0; i < 4; i ++) cin >> a[i];
    sort(a, a + 4);
    if(a[0] + a[3] == a[1] + a[2]){
        if(a[0] == a[1] && a[1] == a[2] && a[2] == a[3]) cout << 1 << endl;
        else if(a[0] == a[1] && a[1] != a[2]) cout << 4 << endl;
        else cout << 8 << endl;
    }
    else cout << 0 << endl;

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

* * *

## F. 签个到就下班

* * *

[原题链接](&lt;http://www.haueacm.top/problem.php?id=1396&gt;)

**描述** ：

给定一个字符串 $S$ ，和两个整数 $N,M,(0\le N\le M\le 9)$，按照出现的顺序输出其中所有的在 $N\sim M$ 之间的数字字符。

**输入格式** ：

第一行，两个整数 $N,M$。

第二行，一个字符串 $S$。

**输出格式** ：

一行，若干个整数，为 $S$ 处理后的结果，每个整数间隔一个空格。

**数据范围** ：

保证 $S$ 的长度 $$
L_{(S)}
$$ 满足 $$
1\le L_{(S)} \le 1\times 10^5
$$。

**样例输入** ：
```java


1 2
abc123
```

**样例输出** ：
```java


1 2
```

**思想** ：

  * 签到题。
  * 按照规则处理即可。



**代码** ：
```java


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

#define IOS ios::sync_with_stdio(false),cin.tie(nullptr),cout.tie(nullptr)
#define re register
#define fi first
#define se second
#define endl '\n'

typedef long long LL;
typedef pair&lt;int, int&gt; PII;
typedef pair&lt;LL, LL&gt; PLL;

const int N = 1e6 + 3;
const int INF = 0x3f3f3f3f, mod = 1804;
const double eps = 1e-6, PI = acos(-1);

void solve(){

    int n, m; string s;
    cin >> n >> m >> s;

    for(int i = 0; i < s.size(); i ++){
        int t = s[i] - '0';
        if(t >= n && t <= m) cout << s[i] << ' ';
    }

}

int main(){

    IOS;

    int _ = 1;

    // cin >> _;

    while(_ --){
        solve();
    }

    return 0;

}
```

* * *

## G. 现在是摸鱼时间

* * *

[原题链接](&lt;http://www.haueacm.top/problem.php?id=1397&gt;)

**描述** ：

![](https://cdn.jsdelivr.net/gh/Doge2077/liyyro-photo@main/images/2022/10/现在是摸鱼时间.png)

$LYS$ 最喜欢摸鱼了， 现在给出一个长度为 $N$ 的序列 $A={A_1,A_2,\dots,A_N}$，表示 $LYS$ 的日程表，其中 $A_i$ 表示第 $i$ 天的摸鱼指数。

为了在排满的日程表里的摸鱼，他向摸鱼大师 $HF$ 请教，摸鱼大师给出了一个摸鱼公式：

  * $\frac{1}{A_i} - \frac{j}{A_iA_j} = \frac{1}{A_j} - \frac{i}{A_iA_j},(i\lt j)$

由公式可知，当第 $i$ 天和第 $j$ 天及其对应的摸鱼指数满足上述公式时，他就可以在第 $i$ 天和第 $j$ 天这两天摸鱼，记为一种摸鱼方案 $(i,j)$。

虽然只能摸两天的鱼，但是 $LYS$ 还是想知道，他的日程表有多少种摸鱼方案可选。




**输入格式** ：

第一行，一个整数 $N$，代表天数。

接下来 $N$ 个整数，代表第 $i$ 天的摸鱼指数 $A_i$。

**输出格式** ：

一行，一个整数，表示方案总数。

**数据范围** ：

$1\le N \le 1\times 10^6$，$1\le A_i\le 1\times 10^3$。

**输入样例** ：
```java


6
3 5 1 3 9 5
```

**输出样例** ：
```java


1
```

**提示** ：

对于样例，只有 $(4,6)$ 符合。

**思想** ：

  * 思维。
  * 化简 $\frac{1}{A_i} - \frac{j}{A_iA_j} = \frac{1}{A_j} - \frac{i}{A_iA_j},(i\lt j)$ 得 $A_j - j = A_i - i$。
  * 由此，不妨设 $B_i = A_i - i$。
  * 总方案数即求对于 $j$ 之前的与 $B_j$ 值相等的 $B_i$ 数量之和。
  * 记录已经出现过的 $B_i$ 数量，之后出现的累加即可。



**代码** ：
```java


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

#define IOS ios::sync_with_stdio(false),cin.tie(nullptr),cout.tie(nullptr)
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

void solve(){

    LL sum = 0;

    map&lt;int,int&gt; vis;

    int n; cin >> n;
    for(int i = 0; i < n; i ++){
        int x; cin >> x;
        x -= i;
        sum += vis[x];  //加上当前位置之前 x 出现过的次数
        vis[x] ++;  //更新次数
    }

    cout << sum << endl;
} 

int main(){

    IOS;

    int _ = 1;

    // cin >> _;

    while(_ --){
        solve();
    }

    return 0;

}
```

* * *

## H. 现在是摸鱼时间 PLUS

* * *

[原题链接](&lt;http://www.haueacm.top/problem.php?id=1398&gt;)

**描述** ：

在习得摸鱼大师 $HF$ 给出的公式之后，$LYS$ 发现 $HF$ 给的摸鱼公式只适用于地球上的日程表，于是他提出了“宇宙摸鱼大一统理论”，以便适应全宇宙不同摸鱼人群的需求。

![](https://cdn.jsdelivr.net/gh/Doge2077/liyyro-photo@main/images/2022/10/现在是摸鱼时间PLUS.png)

现在给出一个长度为 $N$ 的序列 $A={A_1,A_2,\dots,A_N}$，表示某一日程表，其中 $A_i$ 表示第 $i$ 天的摸鱼指数。

$LYS$ 提出的理论如下：

  * 当第 $i$ 天的摸鱼指数 $A_i$ 和第 $j$ 天的摸鱼指数 $A_j$ 互质时，可以在这两天摸鱼，若 $i=j$ 则表示只能在这一天摸鱼。
  * $i + j$ 的值越大，摸鱼的质量越高。

按照上述理论，计算在满足摸鱼条件时， $i + j$ 的最大可能值。




**输入格式** ：

第一行，一个整数 $N$，代表天数。

接下来 $N$ 个整数，代表第 $i$ 天的摸鱼指数 $A_i$。

**输出格式** ：

一行，一个整数，表示某两天满足摸鱼条件的时候 $i + j$ 的最大值。

**数据范围** ：

$1\le N \le 1\times 10^6$，$1\le A_i\le 1\times10^3$。

**输入样例** ：
```java


6
3 5 1 3 9 5
```

**输出样例** ：
```java


11
```

**提示** ：

互质：当 $A$ 和 $B$ 的最大公约数为 $1$ 时，称 $A$ 和 $B$ 互质。

对于样例，在 $i=5,j = 6$ 时满足摸鱼条件，且摸鱼质量最高。

**思想** ：

  * 离散化，最大公约数。
  * 互质的条件为 $gcd(A_i,A_j) = 1$。
  * 对于相同的 $A_i$，我们记录其所在的下标的最大值即可，不必维护所有 $A_i$ 的下标。
  * 即将 $A$ 序列去重，但保留 $A_i$ 原有的最大下标。
  * 枚举离散化存储的 $A_i$ 判断即可，满足摸鱼的条件则维护 $i + j$ 的最大值。



**代码** ：
```java


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

#define IOS ios::sync_with_stdio(false),cin.tie(nullptr),cout.tie(nullptr)
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

int gcd(int a, int b){  //求最大公约数
    return b ? gcd(b, a % b) : a;
}

void solve(){

    int res = -1;

    int n; cin >> n;

    map&lt;int, int&gt; a;  //存入出现过的状态

    for(re int i = 1; i <= n; i ++){
        int x; cin >> x;
        a[x] = i;  //保留最大下标
    }

    for(auto &p : a){
        for(auto &t : a){
            if(gcd(p.fi, t.fi) == 1) res = max(res, p.se + t.se);  //更新答案
        }
    }

    cout << res << endl;

}

int main(){

    IOS;

    int _ = 1;

    // cin >> _;

    while(_ --){
        solve();
    }

    return 0;

}
```
