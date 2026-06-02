---
title: "727. 菱形 (曼哈顿距离)"
date: 2022-06-14
categories: [ALGORITHM, Q&amp;A, 模拟]
description: ""
---

### 727\. 菱形 (曼哈顿距离)

[原题链接](&lt;https://www.acwing.com/problem/content/729/&gt;) **描述** 输入一个奇数 n，输出一个由 * 构成的 n 阶实心菱形。

**输入格式** 一个奇数 n。

**输出格式** 输出一个由 * 构成的 n 阶实心菱形。

具体格式参照输出样例。

**数据范围** 1≤n≤99 **输入样例：**
    
    
    5

**输出样例：**
    
    
      *  
     *** 
    *****
     *** 
      *  

**分析：**

  * 循环n次，每一行按照规律打印`" "`和`"*"`



**规律寻找** ~~1.观察法~~

  * 以`(n+1)/2`处为分界线分别向上下延申打印输出



2.利用曼哈顿距离

  * 以中心点向边界打印，打印输出曼哈顿距离`l <= (n-1)/2`的点 **曼哈顿距离** :矩阵任意一点只通过横向或纵向移动到达中心点的距离 计算公式：`x(x1,y1)`到中心点`m(x2,y2)`


    
    
    l = abs(x1-x2) + abs(y1-y2)

**代码** ~~1.观察法解：~~
    
    
    #include &lt;bits/stdc++.h&gt;
    using namespace std;
    int main()
    {
        int n;
        cin>>n;
        for(int i=1,k=1;i<=n;i++){
    
            for(int j=1;j<=(n+1)/2-k;j++){
                cout<<" ";
            }
            for(int j=0;j<k*2-1;j++){
                cout<<"*";
            }
            cout<<endl;
            if(i>=(n+1)/2){
                k--;
            }
            else k++;
        }
    
        return 0;
    }

2.曼哈顿解：
    
    
    //曼哈顿解 
    #include &lt;bits/stdc++.h&gt; 
    using namespace std;
    int main()
    {
        int n;
        cin>>n;
        for(int i=1;i<=n;i++){
            for(int j=1;j<=n;j++){
                if(abs((n+1)/2-i)+abs((n+1)/2-j)<=(n-1)/2){  //计算曼哈顿距离
                    cout<<"*";
                }
                else cout<<" ";
            }
            cout<<endl;
        }
        return 0;
    }

**扩展** ：只打印边框，不打印内部的空心菱形 例题：ZZULIOJ 1077: 空心菱形 [原题链接](&lt;http://acm.zzuli.edu.cn/problem.php?id=1077&gt;) **分析：**

  * 打印曼哈顿距离`==(n-1)/2`的`"*"`



**代码：**
    
    
    #include &lt;bits/stdc++.h&gt; 
    using namespace std;
    int main()
    {
        int n;
        cin>>n;
        for(int i=1;i<=n;i++){
            for(int j=1;j<=n;j++){
                if(abs((n+1)/2-i)+abs((n+1)/2-j)==(n-1)/2){  //计算曼哈顿距离
                    cout<<"*";
                }
                else cout<<" ";
            }
            cout<<endl;
        }
        return 0;
    }

* * *
