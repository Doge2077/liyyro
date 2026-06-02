---
title: "剪绳子"
date: 2023-02-20
categories: [Q&amp;A, 二分]
description: ""
---

[Original Link](&lt;https://www.acwing.com/problem/content/682/&gt;)

**思想** ：

  * 二分。
  * 绳子最长为 `1e9`。
  * 考虑二分： 
    * 若当前绳长满足要求，则说明还有可能取更长的绳长；
    * 若当前绳长不满足要求，则说明当前绳长不可能是最终答案；
    * 由于绳子长度保留两位小数，则当二分的边界取到两者差值不超过 `eps = 1e-4` 即可。
  * 利用 `a[N]` 存储绳长数据，第 `a[i]` 根绳子可截取的长度为 `int(a[i] / mid)`。



**代码** ：
    
    
    #include &lt;bits/stdc++.h&gt;
    using namespace std;
    
    int n, m;
    
    const int N = 1e6 + 3;
    
    const double eps = 1e-4;
    
    int a[N];
    
    bool check(double x){  //判断是否满足条件
        int cnt = 0;
        for(int i = 0; i < n; i ++){
            cnt += int(a[i] / x);
            if(cnt >= m) return 1;  //当前分割数量已经满足，提前返回 true
        }
        return 0;
    }
    
    void solve(){
        cin >> n >> m;
        for(int i = 0; i < n; i ++) cin >> a[i];
        double l = 0, r = 1e9;
        while(l < r){
            double mid = (l + r) / 2;
            if(check(mid)) l = mid;  //满足条件，说明绳子有可能更长
            else r = mid;  //不满足条件，说明绳子需要缩短
            if(r - l < eps) break;  //差值小于 eps 结束二分
        }
        printf("%.2lf", l);
    }
    
    int main(){
        solve();
        return 0;
    }
