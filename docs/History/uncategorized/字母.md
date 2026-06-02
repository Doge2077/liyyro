---
title: "字母"
date: 2023-03-07
categories: [Q&amp;A, DFS]
description: ""
---

[Original Link](&lt;https://www.acwing.com/problem/content/1113/&gt;)

**思想** ：

  * `DFS`。
  * 由题意易知，从左上角的字母开始搜索，最多经过 $26$ 个不同的字母。
  * 则将走过的字母利用 `vis` 数组进行标记，若走过标记为 `True`。
  * 递归处理每一个格子，每一层利用偏移量数组遍历上下左右四个方向。
  * 用 `res` 维护最大可以走过的不同字母的个数，每次更新，当 `res == 26` 时达到最大，可以提前返回。
  * 注意起始搜索的字母也需要标记。



**代码** ：
    
    
    #include &lt;bits/stdc++.h&gt;
    using namespace std;
    
    const int N = 100;
    
    int n, m, res;
    
    char mp[N][N];
    
    bool vis[N * 3];  // 记录字母 ASCII 码的状态以标记其是否走过
    
    int dx[] = {1, 0, -1, 0}, dy[] = {0, 1, 0, -1};
    
    void dfs(int x, int y, int cnt){
        res = max(res, cnt);  // 更新最大值
        if(res == 26) return;  // 达到最大值提前返回
        for(int i = 0; i < 4; i ++){
            int l = x + dx[i], r = y + dy[i];
            if(l >= 0 && l < n && r >= 0 && r < m && !vis[mp[l][r]]){  // 满足在边界内，且没有走过
                vis[mp[l][r]] = 1;  // 标记为走过
                dfs(l, r, cnt + 1);  // 递归走下一层
                vis[mp[l][r]] = 0;  // 恢复现场
            }
        }
    }
    
    void solve(){
        cin >> n >> m;
        for(int i = 0; i < n; i ++) cin >> mp[i];  // 读入地图，下标从 (0, 0) 开始
        vis[mp[0][0]] = 1;  // 标记起始点已经走过
        dfs(0, 0, 1);  // 从 (0, 0) 开始搜索
        cout << res << endl;
    }
    
    int main(){
        solve();
        return 0;
    }

* * *

### 
