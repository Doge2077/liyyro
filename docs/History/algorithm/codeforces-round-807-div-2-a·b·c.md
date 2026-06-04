---
title: "Codeforces Round #807 (Div 2.) A·B·C"
date: 2022-07-18
categories: [ALGORITHM, Q&amp;A, 模拟, 字符串, Codeforces]
description: ""
---

---

## A. Mark the Photographer

---

### 原题链接

[Original Link](https://codeforces.com/contest/1705/problem/A)

---

### 思想

* 将所有人的身高存入数组，用`sort`排序
  * 利用双指针，以`n`为中间位置，判断是否满足条件
  * 前`n`个人的身高`+ x`应小于等于后`n`个人的身高

---

### 代码
```cpp
#include &lt;bits/stdc++.h&gt;
using namespace std;

const int N=1e6+3;
int a[N];

int main(){
    int t;
    scanf("%d",&t);
    while(t--){
        int n,x;
        scanf("%d%d",&n,&x);
        for(int i=0;i&lt;n*2;i++) scanf("%d",&a[i]);
        sort(a,a+n*2);  //排序

        bool flag=1;
        for(int i=0,j=n;i&lt;n;i++,j++){  //i从0~n-1  j从n~2*n-1
            if(a[j]-a[i]&lt;x){
                flag=0;
                break;
            }
        }
        if(flag) printf("YES\n");
        else printf("NO\n");
    }
    return 0;
}
```

---

## B. Mark the Dust Sweeper

---

### 原题链接

[Original Link](https://codeforces.com/contest/1705/problem/B)

---

### 思想

* 由题意可知当`i`与`j`之间不存在 $a_i=0$ 时，可以进行操作。
  * 则对存入数组的数据进行遍历，直到从头遍历到 $a_i \neq 0$ 为止。
  * 此时，后方的 $a_i=0$ 的房间都可以通过 $a_j \neq 0$ 的房间来填充一次，使得操作继续。

---

### 代码
```cpp
#include &lt;bits/stdc++.h&gt;
using namespace std;

int t;
const int N=1e6+3;
int a[N];

int main(){
    cin>>t;
    while(t--){
        int n;
        cin>>n;
        for(int i=0;i&lt;n;i++) cin&gt;>a[i];
        int p=0;
        while(p&lt;n && a[p]==0) p++;
        long long cnt=0;
        for(int i=p;i&lt;n-1;i++){
            cnt+=a[i];
            if(a[i]==0) cnt++;
        }
        cout&lt;&lt;cnt&lt;&lt;endl;
    }
    return 0;
}
```

---

## C. Mark and His Unfinished Essay

---

### 原题链接

[Original Link](https://codeforces.com/contest/1705/problem/C)

---

### 思想

* 由于数据范围极大，想用`string`存下来是不可能的
  * 对于每次的`copy`操作，记录`l`和`r`
  * 同时记录`copy`之后的`l`和`r`的新位置，记为`nl`和`nr`
  * 对于每次询问，要找到`k`所在的`nl`和`nr`的区间
  * 即要找到进行第几次`copy`操作后，满足`l`和`r`更新的区间`nl`和`nr`，使得`nl &lt;= k &lt;= nr`
  * 找到后，将`k`更新为`k' = k - (nl - l)`，使得`k'`在`l`和`r`所在的区间内，即`l &lt;= k' &lt;= r`
  * 不断重复上述步骤更新`k`，直到`1 &lt;= k &lt;= n`
  * 由于操作次数很少，在寻找对应区间时可以直接从大到小进行枚举

---

### 代码
```cpp
#include &lt;bits/stdc++.h&gt;
using namespace std;

const int N = 1e6 + 3;

typedef long long LL;

LL l[N], r[N], nl[N], nr[N];
// l和r数组存储每次copy的l和r
// nl和nr数组存储copy之后，l和r的位置

void solve() {
    LL n, m, q;
    cin >> n >> m >> q;

    string s;
    cin >> s;

    nl[0] = 0, nr[0] = n;
    for (int i = 1; i &lt;= m; i++) {
        cin &gt;> l[i] >> r[i];
        nl[i] = nr[i - 1] + 1;  // 更新nl
        nr[i] = nl[i] + (r[i] - l[i] + 1) - 1;  // 更新nr
    }

    while (q--) {
        LL k;
        cin >> k;
        for (int i = m; i >= 1; i--) {  // 枚举区间
            if (nl[i] &lt;= k && k &lt;= nr[i]) k -= nl[i] - l[i];
        }
        cout &lt;&lt; s[k - 1] &lt;&lt; endl;
    }
}

int main() {
    LL t;
    cin &gt;> t;
    while (t--) {
        solve();
    }
    return 0;
}
```

---

## 后记

* $A$题非常简单，没有被`hack`也没什么感觉
  * $B$题比赛时写麻烦了，最后`TLE`了，补题才发现自己把自己绕晕了
  * $C$题实在是难到怀疑人生了，前后搞了好几个小时才想通，希望自己以后不要这么笨了
  * 剩下的题实在是不行，毕竟还是个大菜鸟，交给未来吧，加油！！！