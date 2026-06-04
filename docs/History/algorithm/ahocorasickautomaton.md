---
title: "AC 自动机详解"
date: 2023-02-04
categories: [ALGORITHM, Intermediate Algorithm, AC自动机, Trie树]
description: ""
---

# 前置知识

---

## 字典树 Trie

---

`Trie` 是一种能够快速插入和查询字符串的多叉树结构。它包含多个节点，每个节点拥有一个唯一的编号，根节点的编号为 `0`。树中的每条边代表一个字符。节点通常用于标记某个字符串是否插入过以及插入的次数。

---

### 支持操作

---

`Trie` 维护字符串的集合，支持两种操作：

*   向集合中插入一个字符串：`void insert(char *s)`
*   在集合中查询一个字符串：`int query(char *s)`

---

### 建字典树

---

*   儿子数组 `ch[p][j]` 存储从节点 `p` 沿着字符 `j` 对应的边走到的子节点。
    *   对于小写字母 `a` ~ `z`，字符的映射值为 `0` ~ `25`。
    *   因此，每个节点最多可以有 `26` 个子节点。
*   计数数组 `cnt[p]` 存储以节点 `p` 为终点的单词的插入次数。
*   节点编号 `idx` 用于为新节点分配编号。

---

### 实现思想

---

*   初始化时，`Trie` 仅有一个根节点，编号为 `0`。
*   插入字符串时，从根节点开始，遍历字符串的每个字符：
    *   如果当前节点存在对应字符的子节点，则移动到该子节点；
    *   如果不存在，则先创建一个新子节点，再移动到该子节点。
*   遍历完字符串后，在最后一个节点的计数器上增加一次计数。
*   例如：依次插入 `"cat", "car", "busy", "cate", "bus", "car"`：
    *   ![](https://cdn.jsdelivr.net/gh/Doge2077/liyyro-photo@main/images/2023/02/Trie树.png)

---

### 代码实现

---

```cpp
const int N = 1e6 + 3;

int n;
string s;
int ch[N][27], cnt[N], idx;

void insert(string s){
    int p = 0;
    for(int i = 0; i &lt; s.size(); i ++){
        int j = s[i] - 'a';  //字母的映射值
        if(!ch[p][j]) ch[p][j] = ++ idx;
        p = ch[p][j];
    }
    cnt[p] ++;  //插入次数
}

int query(string s){
    int p = 0;
    for(int i = 0; i &lt; s.size(); i ++){
        int j = s[i] - 'a';
        if(!ch[p][j]) return 0;
        p = ch[p][j];
    }
    return cnt[p];
}
```

---

## 例题

---

### Trie字符串统计

---

[原题链接](https://www.acwing.com/problem/content/description/837/)

维护一个字符串集合，支持两种操作：

1.  `I x` 向集合中插入一个字符串 $x$；
2.  `Q x` 询问一个字符串在集合中出现了多少次。

共有 $N$ 个操作，所有输入的字符串总长度不超过 $10^5$，字符串仅包含小写英文字母。

**输入格式**

第一行包含整数 $N$，表示操作数。

接下来 $N$ 行，每行包含一个操作指令，指令为 `I x` 或 `Q x` 中的一种。

**输出格式**

对于每个询问指令 `Q x`，都要输出一个整数作为结果，表示 $x$ 在集合中出现的次数。

每个结果占一行。

**数据范围**

$1\le N\le 2\times 10^4$

**输入样例**：
```
5
I abc
Q abc
Q ab
I ab
Q ab
```

**输出样例**：
```
1
0
1
```

**代码**：
```cpp
#include &lt;bits/stdc++.h&gt;
using namespace std;

const int N = 1e6 + 3;

int n;
string s;
int ch[N][27], cnt[N], idx;

void insert(string s){
    int p = 0;
    for(int i = 0; i &lt; s.size(); i ++){
        int j = s[i] - 'a';  //字母的映射值
        if(!ch[p][j]) ch[p][j] = ++ idx;
        p = ch[p][j];
    }
    cnt[p] ++;  //插入次数
}

int query(string s){
    int p = 0;
    for(int i = 0; i &lt; s.size(); i ++){
        int j = s[i] - 'a';
        if(!ch[p][j]) return 0;
        p = ch[p][j];
    }
    return cnt[p];
}

void solve(){
    int n; cin &gt;> n;
    while(n --){
        string op; cin >> op >> s;
        if(op == "I") insert(s);
        else cout &lt;&lt; query(s) &lt;&lt; endl;
    }
}

int main(){
    solve();
    return 0;
}
```

---

### 最大异或对

---

[题目链接](https://www.acwing.com/problem/content/145/)

在给定的 $N$ 个整数 $A_1, A_2, \cdots, A_N$ 中选出两个进行 $\text{xor}$（异或）运算，得到的结果最大是多少？

**输入格式**

第一行输入一个整数 $N$。

第二行输入 $N$ 个整数 $A_1, A_2, \cdots, A_N$。

**输出格式**

输出一个整数表示答案。

**数据范围**

$1\le N &lt; 10^5, \quad 0\le A_i \le 2^{31}$

**输入样例**：
```
3
1 2 3
```

**输出样例**：
```
3
```

**思路**：

* 异或运算即对数的二进制位进行运算，因此先将 $N$ 个整数均转化为二进制表示。
  * 二进制是 `0` 和 `1` 构成的串，可以构造 `Trie` 树，在树枝上进行异或运算。
  * 用 `Trie` 存整数，由整数的二进制位构造的 `Trie` 是一棵二叉树，深度为 `31` 层。

**本质上**：

* 用 `Trie` 存单词，由 `26` 个小写字母构造的 `Trie`，是一棵 `26` 叉树，深度为最长单词的长度。
* 用 `Trie` 存整数，由整数的二进制位构造的 `Trie`，是一棵 `2` 叉树，深度为 `31` 层。
* 用 `Trie` 存整数，由整数的十进制位构造的 `Trie`，是一棵 `10` 叉树，深度为整数的位数。

**代码**：
```cpp
#include &lt;bits/stdc++.h&gt;
using namespace std;

const int N = 1e6 + 3;

int n;
int a[N];  //存数
int ch[N * 31][3], cnt[N], idx;

void insert(int x){
    int p = 0;
    for(int i = 30; i >= 0; i --){
        int j = x >> i & 1;  //取出第 i 位
        if(!ch[p][j]) ch[p][j] = ++ idx;
        p = ch[p][j];
    }
}

int query(int x){
    int p = 0, res = 0;
    for(int i = 30; i >= 0; i --){
        int j = x >> i & 1;  //取出第 i 位
        if(ch[p][!j]){
            res += 1 &lt;&lt; i;  //累加位权
            p = ch[p][!j];
        }
        else p = ch[p][j];
    }
    return res;
}

void solve(){
    int ans = 0;
    cin &gt;> n;
    for(int i = 0; i &lt; n; i ++) cin &gt;> a[i], insert(a[i]);
    for(int i = 0; i &lt; n; i ++) ans = max(ans, query(a[i]));
    cout &lt;&lt; ans &lt;&lt; endl;
}

int main(){
    solve();
    return 0;
}
```

---

# AC自动机

---

## 基础概念

---

&gt; 自动机是一个对信号序列进行判定的数学模型。

`AC` 自动机，全称为 Aho-Corasick automaton，该算法在 `1975` 年产生于贝尔实验室，是著名的多模匹配算法。所谓多模匹配算法，最常见的例子是给出 `n` 个单词，再给出一段包含 `m` 个字符的文章，让你找出有多少个单词在文章里出现过。

AC 自动机是**以 Trie 的结构为基础**，结合 **KMP 的思想** 建立的。

---

## 实现思想

---

简单来说，建立一个 `AC` 自动机有两个必要结构：

基础的 `Trie` 结构：

*   先用 `n` 个模式串构造一棵 `Trie`。
*   `Trie` 中的一个节点表示一个从根到当前节点的**字符串**，其中，根节点表示空串。
*   如果节点对应一个模式串，则打个标记。

`KMP` 的思想：

*   对 `Trie` 上所有的节点构造失配指针。
*   即在 `Trie` 上构建两类边：回跳边和转移边。

最后就可以利用它扫描主串进行多模式匹配。

![](https://cdn.jsdelivr.net/gh/Doge2077/liyyro-photo@main/images/2023/02/AC自动机.png)

节点 $⑤$ 表示 `"s"`，节点 $⑥$ 表示 `"sh"`，节点 $⑦$ 表示 `"she"`。

具体地，对于构建两类边：

*   回跳边：
    *   `ne[v]` 存储节点 `v` 的回跳边的终点。例如 `ne[7] = 3`。
    *   回跳边指向**父节点的回跳边所指节点的子节点**。
    *   四个点（`v`，`u`，`ne[u]`，`ch[ne[u]][i]`）构成四边形。
    *   回跳边所指节点一定是当前节点的**最长后缀**。

*   转移边：
    *   `ch[u][i]` 存储节点 `u` 沿着字符 `i` 的转移边的终点。
    *   转移边指向当前节点的回跳边所指节点的对应子节点。
    *   三个点（`u`，`ne[u]`，`ch[ne[u]][i]`）构成三角形。
    *   转移边所指节点一定是当前节点的**最短路**。

![](https://cdn.jsdelivr.net/gh/Doge2077/liyyro-photo@main/images/2023/02/AC自动机的边.png)

构造 `AC` 自动机：

*   初始化，把根节点的子节点们入队。
*   只要队不空，节点 `u` 出队，枚举 `u` 的 26 个子节点：
    *   若子节点存在，则父节点帮子节点建回跳边，并把子节点入队。
    *   若子节点不存在，则父节点自建转移边。

![](https://cdn.jsdelivr.net/gh/Doge2077/liyyro-photo@main/images/2023/02/AC自动机的回跳边.png)

如图建立 `AC` 自动机的回跳边，转移边同理。

查找单词出现次数：

*   扫描主串，依次取出字符 `s[k]`。
*   `i` 指针走主串对应的节点，沿着树边或转移边走且保证不回退。
*   `j` 指针沿着回跳边搜索模式串，每次从当前节点走到根节点，把当前节点中的所有后缀模式串遍历完，保证不漏解。
*   扫描完主串，返回答案。

---

## 代码实现

---

```cpp
const int N = 5e5 + 3;

int n;
string s;
int ch[N][26], cnt[N], idx;
int ne[N];

void insert(string s) {  // Trie树
    int p = 0;
    for (int i = 0; i &lt; s.size(); i++) {
        int j = s[i] - 'a';
        if (!ch[p][j]) ch[p][j] = ++idx;
        p = ch[p][j];
    }
    cnt[p]++;
}

void build() {  // 建AC自动机
    queue&lt;int&gt; q;
    for (int i = 0; i &lt; 26; i++) {
        if (ch[0][i]) q.push(ch[0][i]);  // 根节点儿子入队
    }
    while (q.size()) {
        int u = q.front(); q.pop();
        for (int i = 0; i &lt; 26; i++) {
            int v = ch[u][i];
            if (v) ne[v] = ch[ne[u]][i], q.push(v);  // 儿子存在，爹帮儿子建回跳边，儿子入队
            else ch[u][i] = ch[ne[u]][i];  // 儿子不存在，爹自建转移边
        }
    }
}

int query(string s) {  // 扫描主串查询
    int ans = 0;
    for (int k = 0, i = 0; k &lt; s.size(); k++) {
        i = ch[i][s[k] - 'a']; 
        for (int j = i; j && ~cnt[j]; j = ne[j]) {
            ans += cnt[j], cnt[j] = -1;  // 找到后退出，加速查询
        }
    }
    return ans;
}
```

---

## 例题

---

### 搜索关键词

---

[原题链接](https://www.acwing.com/problem/content/1284/)

给定 $n$ 个长度不超过 $50$ 的由小写英文字母组成的单词，以及一篇长为 $m$ 的文章。

请问，其中有多少个单词在文章中出现了。

**注意：每个单词不论在文章中出现多少次，仅累计 1 次。**

**输入格式**

第一行包含整数 $T$，表示共有 $T$ 组测试数据。

对于每组数据，第一行一个整数 $n$，接下去 $n$ 行表示 $n$ 个单词，最后一行输入一个字符串，表示文章。

**输出格式**

对于每组数据，输出一个占一行的整数，表示有多少个单词在文章中出现。

**数据范围**

$1\le n \le 10^4, 1\le m \le 10^6$

**输入样例**：
```
1
5
she
he
say
shr
her
yasherhs
```

**输出样例**：
```
3
```

**代码**：
```cpp
#include &lt;bits/stdc++.h&gt;
using namespace std;

const int N = 5e5 + 3;

int n;
string s;
int ch[N][26], cnt[N], idx;
int ne[N];

void insert(string s){
    int p = 0;
    for(int i = 0; i &lt; s.size(); i ++){
        int j = s[i] - 'a';
        if(!ch[p][j]) ch[p][j] = ++ idx;
        p = ch[p][j];
    }
    cnt[p] ++;
}

void build(){  //建 AC 自动机
    queue&lt;int&gt; q;
    for(int i = 0; i &lt; 26; i ++){
        if(ch[0][i]) q.push(ch[0][i]);
    }
    while(q.size()){
        int u = q.front(); q.pop();
        for(int i = 0; i &lt; 26; i ++){
            int v = ch[u][i];
            if(v) ne[v] = ch[ne[u]][i], q.push(v);
            else ch[u][i] = ch[ne[u]][i];
        }
    }
}

int query(string s){
    int ans = 0;
    for(int k = 0, i = 0; k &lt; s.size(); k ++){
        i = ch[i][s[k] - 'a'];
        for(int j = i; j && ~ cnt[j]; j = ne[j]){
            ans += cnt[j], cnt[j] = -1;
        }
    }
    return ans;
}

void solve(){
    idx = 0;
    memset(ch, 0, sizeof ch);
    memset(cnt, 0, sizeof cnt);
    memset(ne, 0, sizeof ne);

    cin &gt;> n;
    for(int i = 0; i &lt; n; i ++){
        cin &gt;> s; insert(s);
    }
    build();
    cin >> s;
    cout &lt;&lt; query(s) &lt;&lt; endl;
}

int main(){
    int _; cin &gt;> _;
    while(_ --) solve();
    return 0;
}
```

### 单词

---

[原题链接](https://www.acwing.com/problem/content/1283/)

给定 $n$ 个单词，请你输出每个单词在所有单词中作为子串出现的次数。

**数据范围**

$1\le N\le 200$，所有单词长度的总和不超过 $10^6$。

**输入样例**：
```
3
a
aa
aaa
```

**输出样例**：
```
6
3
1
```

**思路**：

* 求每个单词在全文中出现的次数，即该单词在其他单词中出现次数的总和。
  * 故该单词在其他单词中的前缀和后缀即为该单词出现次数的总和。
  * 在建 `AC` 自动机时利用 `BFS` 从第 `0` 层搜索到 `n` 层，需要保留队列的信息进行递推计算，且递推计算出现的次数时必须逆序。

**代码**：
```cpp
#include &lt;bits/stdc++.h&gt;
using namespace std;

const int N = 1e6 + 3;

int n;
string s;
int ch[N][26], cnt[N], idx;
int ne[N], num[N];

int id[N];  //记录

void insert(int x){
    int p = 0;
    for(int i = 0; i &lt; s.size(); i ++){
        int j = s[i] - 'a';
        if(!ch[p][j]) ch[p][j] = ++ idx;
        p = ch[p][j];
        cnt[p] ++;  //统计前缀的次数，每一个结束的位置都代表一个字符串
    }
    id[x] = p;  //记录结束位置
}

void build(){  //构建 AC 自动机
    //由于后续递推求前缀出现的次数，故需要保留队列的信息
    int hh = 0, tt = -1;
    for(int i = 0; i &lt; 26; i ++){
        if(ch[0][i]) num[++ tt] = ch[0][i];
    }
    while(hh &lt;= tt){
        int u = num[hh ++];
        for(int i = 0; i &lt; 26; i ++){
            int v = ch[u][i];
            if(v) ne[v] = ch[ne[u]][i], num[++ tt] = v;
            else ch[u][i] = ch[ne[u]][i];
        }
    }
}

void solve(){
    cin &gt;> n;
    for(int i = 0; i &lt; n; i ++){
        cin &gt;> s; insert(i);  //i 为当前单词对应编号
    }
    build();
    //递推更新 cnt, trie 中节点编号为 0 ~ idx，一共 idx + 1 个点，0 既代表根节点又代表空节点
    for(int i = idx; i >= 0; i --) cnt[ne[num[i]]] += cnt[num[i]];  
    for(int i = 0; i < n; i ++) cout << cnt[id[i]] << endl;
}

int main(){
    solve();
    return 0;
}
```