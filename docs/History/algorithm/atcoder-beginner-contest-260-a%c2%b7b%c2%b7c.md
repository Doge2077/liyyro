---
title: "AtCoder Beginner Contest 260 (A·B·C)"
date: 2022-07-26
categories: [ALGORITHM, Q&amp;A, AtCoder, DP]
description: ""
---

* * *

## A - A Unique Letter

* * *

### 题目大意

[Origional Link](&lt;https://atcoder.jp/contests/abc260/tasks/abc260_a&gt;)

对于$S$包含三个字符，输出只出现一次的字符，多个答案输出任意一个

* * *

### 思想

  * 用`a[N]`存储`s[i]`出现的次数



* * *

### 代码
    
    
    #include &lt;bits/stdc++.h&gt;
    using namespace std;
    
    const int N = 1000;
    
    int a[N];
    
    int main(){
    
        string s;
    
        cin >> s;
    
        for(int i = 0; i < s.size(); i ++){
            a[s[i]]++;
        }
    
        for(int i = 'a'; i <= 'z'; i ++){
            if(a[i] == 1){
                cout << (char)i << endl;
                return 0;
            }
        }
    
        cout << -1 << endl;
    
        return 0;
    
    }

* * *

## B - Better Students Are Needed!

* * *

### 题目大意

[Origional Link](&lt;https://atcoder.jp/contests/abc260/tasks/abc260_b&gt;)

共有$N$个学生，给出其数学和英语成绩分别为$A_i,B_i$，对于$X$名数学成绩最高的学生进行录取，然后从剩余的未录取学生中选择$Y$名英语成绩最高的学生进行录取，最后从剩余的未录取学生中选择$Z$名总成绩最高的学生进行录取，若分数相同录取编号小的学生。

* * *

### 思想

  * 结构体排序
  * 分别对数学，英语和总成绩由高到低进行排序
  * 选择相应数量的符合要求的学生，并将录取的学生进行标记



* * *

### 代码
    
    
    #include &lt;bits/stdc++.h&gt;
    using namespace std;
    
    const int N = 1e6 + 3;
    
    struct students{
        int m,e,p;
    }stu[N];
    
    int n,x,y,z; 
    
    bool vis[N];
    
    //对数学成绩排序
    bool cmp1(students &s1,students &s2){
        if(s1.m == s2.m){
            return s1.p < s2.p;
        }
        else return s1.m > s2.m;
    }
    
    //对英语成绩排序
    bool cmp2(students &s1,students &s2){
        if(s1.e == s2.e){
            return s1.p < s2.p;
        }
        else return s1.e > s2.e;
    }
    
    //对总成绩排序
    bool cmp3(students &s1,students &s2){
        if(s1.m + s1.e == s2.m + s2.e){
            return s1.p < s2.p;
        }
        else return s1.m + s1.e > s2.m + s2.e;
    }
    
    int main(){
    
        cin >> n >> x >> y >> z;
    
        for(int i = 0; i < n; i ++){
            cin >> stu[i].m;
            stu[i].p = i + 1;
        }
    
        for(int i = 0; i < n; i ++) cin >> stu[i].e;
    
        if(x){
            int flag = 0;
            sort(stu,stu + n,cmp1);
            for(int i = 0; flag < x; i ++){
                if(!vis[stu[i].p]){
                    vis[stu[i].p] = 1;
                    flag++;
                }
            }
        }
    
        if(y){
            int flag = 0;
            sort(stu,stu + n,cmp2);
            for(int i = 0; flag < y; i ++){
                if(!vis[stu[i].p]){
                    vis[stu[i].p] = 1;
                    flag++;
                }
            }
        }
    
        if(z){
            int flag = 0;
            sort(stu,stu + n,cmp3);
            for(int i = 0; flag < z; i ++){
                if(!vis[stu[i].p]){
                    vis[stu[i].p] = 1;
                    flag++;
                }
            }
        }
    
        for(int i = 1; i <= n; i ++) if(vis[i]) cout << i << endl;
    
        return 0;
    
    }

* * *

## C - Changing Jewels

* * *

### 题目大意

[Origional Link](&lt;https://atcoder.jp/contests/abc260/tasks/abc260_c&gt;)

  * 一颗等级为$n$的红宝石可以变成一颗等级为$n-1$的红宝石和$X$颗等级为$n$的蓝宝石
  * 一颗等级为$n$的蓝宝石可以变成一颗等级为$n-1$的红宝石和$Y$颗等级为$n-1$的蓝宝石
  * 只有宝石等级$n>2$时才可以进行转化
  * 给出一颗红宝石的等级$N$和转换比例$X,Y$，不限制转化次数，求可以得到多少蓝宝石



* * *

### 思想

  * 动态规划
  * 状态表示： 
    * `red[i]`表示从一颗等级为$i$的红宝石转化到等级为$1$的蓝宝石的最大数量
    * `blue[i]`表示一颗等级为$i$的蓝宝石转化到等级为$1$的蓝宝石的最大数量
  * 状态计算： 
    * 先计算`blue[i] = red[i - 1] + blue[i - 1] * Y`的状态
    * 再计算`red[i] = red[i - 1] + blue[i] * X`的状态
    * 最后`red[n]`即为转化的最大值



* * *

### 代码
    
    
    #include &lt;bits/stdc++.h&gt;
    using namespace std;
    
    typedef long long LL;
    
    const int N = 20; 
    
    LL n, x, y;
    
    LL m = 1;
    
    LL red[N], blue[N];
    
    int main(){
    
        cin >> n >> x >> y;
    
        red[1] = 0, blue[1] = 1;
    
        for(int i = 2; i <= n; i ++){
            blue[i] = red[i - 1] + blue[i - 1] * y;
            red[i] = red[i - 1] + blue[i] * x;
        }
    
    //  for(int i = 1; i <= n; i ++) cout << blue[i] << ' ' ;
    //  cout << endl;
    
        cout << red[n] << endl;
    
        return 0;
    
    }

* * *
