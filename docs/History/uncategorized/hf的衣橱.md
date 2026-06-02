---
title: "HF的衣橱"
date: 2023-03-18
categories: [Q&amp;A, 贪心]
description: ""
---

[原题链接](&lt;http://www.haueacm.top/problem.php?id=1435&gt;)

**描述** ：

邻近联谊，$\text{HF}$ 最喜欢女装了，为了更好的取悦 $\text{LYS}$ 和观众朋友们（$\text{FRI}$），$\text{LYS}$ 特地为他准备了四种不同风格的衣服：

  * 女仆风格：$\text{LYS}$ 和 $\text{FRI}$ 的 $\text{SAN}$ 值（快乐值）均上升 $1$ 点。
  * 哥特风格：$\text{LYS}$ 的 $\text{SAN}$ 值下降 $1$ 点，$\text{FRI}$ 的 $\text{SAN}$ 值上升 $1$ 点。
  * 马猴烧酒风格：$\text{LYS}$ 的 $\text{SAN}$ 值上升 $1$ 点，$\text{FRI}$ 的 $\text{SAN}$ 值下降 $1$ 点。
  * 赛博朋克风格：$\text{LYS}$ 和 $\text{FRI}$ 的 $\text{SAN}$ 值（快乐值）均下降 $1$ 点。



在表演时，$\text{HF}$ 会更换不同风格的女装来表演，但每件衣服只能穿一次，$\text{LYS}$ 和 $\text{FRI}$ 的初始 $\text{SAN}$ 值均为 $0$，若表演过程中：

  * $\text{LYS}$ 或 $\text{FRI}$ 的 $\text{SAN}$ 值为负数，则演出将终止。
  * $\text{LYS}$ 或 $\text{FRI}$ 的 $\text{SAN}$ 值非负数，但没有其他衣服可穿了，演出也会终止。



$\text{HF}$ 想知道，他要如何安排不同风格衣服的表演顺序，才能使自己穿上女装的次数最多？

**输入格式** ：

第一行，一个整数 $T$， 表示测试样例个数。

每个测试样例输入仅一行，共四个整数 $a,b, c, d$，分别表示四种不同风格的衣服数量。

**输出格式** ：

输出共 $T$ 行，每行一个整数，表示 $\text{HF}$ 最多能穿上的衣服数量。

**数据范围** ：

$1\le T \le 1\times 10^4$，

$ 0 \le a,b,c,d \le 1 \times 10^8, 1 \le a + b + c + d$。

**样例输入** ：
```java


3
2 0 0 0
1 1 0 2
1 1 1 1
```

**样例输出** ：
```java


2
3
4
```

**提示** ：

对于样例 $1$，$\text{HF}$ 只能选择穿两件女仆风格的衣服，由于已经没有别的衣服可换了，表演结束。

对于样例 $2$，$\text{HF}$ 先穿女仆风格的衣服，再穿哥特风格的衣服，此时 $\text{LYS}$ 的 $\text{SAN}$ 值为 $0$，最后再穿一件赛博朋克风格的衣服结束表演。

**思想** ：

  * 贪心。
  * 当 $a = 0$ 时，只能穿 $1$ 次。
  * 当 $a \gt 0$ 时： 
```java
* 首先穿完所有的 $a$，使得 $\text{SAN}$ 为最大值；
* 之后，由于相同数量的 $b$ 和 $c$ 风格的衣服使得 $\text{SAN}$ 值可以互相抵消，故不会对 $\text{SAN}$ 造成影响；
* 最后，将抵消后的 $b,c$ 的剩余数量和 $d$ 相加与 $a + 1$ 比较，取最小值即为在剩余的 $b$ 或 $c$ 和 $d$ 中能穿的衣服数量。
```



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
typedef unsigned long long ULL;

typedef pair&lt;int, int&gt; PII;
typedef pair&lt;LL, LL&gt; PLL;

const int N = 1e6 + 3;
const int INF = 0x3f3f3f3f, mod = 1e9 + 7;
const double eps = 1e-6, PI = acos(-1);

void solve(){
    LL a, b, c, d; cin >> a >> b >> c >> d;
    if(a == 0) cout << 1 << endl;
    else cout << a + min(b, c) * 2 + min(a + 1, abs(b - c) + d) << endl;
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
