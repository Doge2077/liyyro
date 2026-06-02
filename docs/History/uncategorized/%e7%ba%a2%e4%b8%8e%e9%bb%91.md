---
title: "红与黑"
date: 2023-03-16
categories: [Q&amp;A, BFS]
description: ""
---

[Original Link](&lt;https://www.acwing.com/problem/content/1115/&gt;)

**思想** ：

  * `BFS`。
  * 将搜索的起始点，即坐标为 `@` 的点入队开始搜索。
  * 利用偏移量数组遍历四个方向，将搜索到的点入队，记录 `res ++`。
  * 取出队头，扩展队头搜索，直到清空队列即可。



**代码** ：
    
    
    #include &lt;bits/stdc++.h&gt;
    using namespace std;
    
    const int N = 50;
    
    int n, m, res, sx, sy;
    
    int dx[] = {1, 0, -1, 0}, dy[] = {0, 1, 0, -1};
    
    char mp[N][N];
    bool vis[N][N];
    
    int bfs(int x, int y){
        vis[x][y] = 1;  // 标记起始点
        queue&lt;pair&lt;int, int&gt;&gt; st; st.push({x, y});  // 将起始点入队
        while(!st.empty()){
            auto p = st.front(); st.pop();  // 取出队头
            for(int i = 0; i < 4; i ++){
                int l = p.first + dx[i], r = p.second + dy[i];  // 加上偏移量后的位置
                if(l >= 0 && l < n && r >= 0 && r < m && !vis[l][r] && mp[l][r] == '.'){  // 满足在边界内，不能为 #，且未走过
                    vis[l][r] = 1;  // 标记为走过
                    st.push({l, r});  // 将该点入队
                    res ++;  // 记录数量增加
                }
            }
        }
        return res;  // 返回计数
    }
    
    void solve(){
        res = 1;  // 重置
        for(int i = 0; i < n; i ++){
            cin >> mp[i];  // 读入地图，多组数据直接覆盖
            for(int j = 0; j < m; j ++){
                vis[i][j] = 0;  // 清空标记
                if(mp[i][j] == '@') sx = i, sy = j;  // 标记入口
            }
        }
        cout << bfs(sx, sy) << endl;
    }
    
    int main(){
        while(cin >> m >> n && n && m) solve();
        return 0;
    }
