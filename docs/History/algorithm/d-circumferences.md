---
title: "D - Circumferences"
date: 2022-07-14
categories: [ALGORITHM, Q&amp;A, BFS]
description: ""
---

### D - Circumferences

[原题链接](&lt;https://atcoder.jp/contests/abc259/tasks/abc259_d&gt;)

**分析**

  * 考虑`BFS`搜索，将相交的园加入搜索队列
  * 每次搜索判断终点是否位于圆上
  * 核心在于判断两圆是否相交，及点是否位于圆上，设圆心距为`d`
  * 相交：`d*d <= (r1+r2)*(r1+r2) && d*d >= (r1-r2)*(r1-r2)`
  * 点`(x,y)`在圆`(x1,y1)`上：`(x1-x)*(x1-x)+(y1-y)*(y1-y) == r1*r1`



**注意**

  * 注意数据范围需要开`long long`
  * 不能使用`sqrt`和`pow`，会产生精度问题



**代码**
```java


#include &lt;bits/stdc++.h&gt;
using namespace std;

typedef long long LL;

const LL N=1e6+3;

LL n,sx,sy,tx,ty;

struct point{   //存储圆的信息
    LL x,y,r;
}mp[N];

queue&lt;point&gt; st;  //用于搜索的队列

bool vis[N];  //记录该圆是否被搜到过

bool check(LL x_1,LL y_1,LL x_2,LL y_2,LL r_1,LL r_2){  //判断两圆是否相交
    return (x_1-x_2)*(x_1-x_2)+(y_1-y_2)*(y_1-y_2)>=(r_1-r_2)*(r_1-r_2)&&(x_1-x_2)*(x_1-x_2)+(y_1-y_2)*(y_1-y_2)<=(r_1+r_2)*(r_1+r_2);
}

bool in(LL x,LL y,LL r,LL a,LL b){  //判断点是否在圆上
    return (x-a)*(x-a)+(y-b)*(y-b)==r*r;
}

bool bfs(){

    while(!st.empty()){

        auto p=st.front();
        st.pop();

        if(in(p.x,p.y,p.r,tx,ty)) return 1;  //若终点在圆上直接返回

        for(int i=0;i<n;i++){

            if(!vis[i]){  //若没有搜到过该圆

                if(check(p.x,p.y,mp[i].x,mp[i].y,p.r,mp[i].r)){  //判断两圆是否相交
                    vis[i]=1;  //若相交，则标记该圆
                    st.push(mp[i]);  //将其加入搜索队列
                }

            }

        }

    }

    return 0;  //找不到说明走不到终点

}

int main(){

    scanf("%lld",&n);

    scanf("%lld %lld %lld %lld",&sx,&sy,&tx,&ty);

    for(int i=0;i<n;i++){
        LL a,b,c;
        scanf("%lld%lld%lld",&a,&b,&c);
        mp[i]={a,b,c};

        if(in(a,b,c,sx,sy)){  //若起始点在该圆上
            st.push(mp[i]);  //则将该圆作为搜索起始点加入搜索队列
            vis[i]=1;  //标记该圆已经搜到过
        }

    }

    if(bfs()) printf("Yes\n");
    else printf("No\n");

    return 0;

}
```
