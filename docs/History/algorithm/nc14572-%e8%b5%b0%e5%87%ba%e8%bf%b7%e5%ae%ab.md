---
title: "NC14572 走出迷宫"
date: 2022-06-16
categories: [ALGORITHM, Q&amp;A, BFS, DFS]
description: ""
---

### NC14572 走出迷宫

[原题链接](&lt;https://ac.nowcoder.com/acm/problem/14572&gt;)

**描述**

小明现在在玩一个游戏，游戏来到了教学关卡，迷宫是一个N*M的矩阵。

小明的起点在地图中用“S”来表示，终点用“E”来表示，障碍物用“#”来表示，空地用“.”来表示。 障碍物不能通过。小明如果现在在点（x，y）处，那么下一步只能走到相邻的四个格子中的某一个：（x+1，y），（x-1，y），（x，y+1），（x，y-1）；

小明想要知道，现在他能否从起点走到终点。

**输入格式:** 本题包含多组数据。 每组数据先输入两个数字N,M 接下来N行，每行M个字符，表示地图的状态。

**数据范围：** 2<=N,M<=500 保证有一个起点S，同时保证有一个终点E.

**输出格式:** 每组数据输出一行，如果小明能够从起点走到终点，那么输出Yes，否则输出No

**输入样例：**
    
    
    3 3
    S..
    ..E
    ...
    3 3
    S##
    ###
    ##E

**输出样例**
    
    
    Yes
    No

**分析**

  * 走出迷宫需要对每一个点进行搜索，考虑`DFS`和`BFS`
  * 首先需要记录`S`的坐标
  * 从`S`开始搜索，需要偏移量数组
  * 对于`DFS`在搜索时，若搜到`E`点则标记答案
  * 对于`BFS`在搜随时，若搜到`E`点直接返回



**DFS代码**
    
    
    #include &lt;bits/stdc++.h&gt;
    using namespace std;
    
    const int N=510;
    
    int n,m;
    
    char mp[N][N];  //存储地图
    
    bool vis[N][N];  //标记是否走过该点
    
    int s1,s2;  //标记S的坐标
    
    int dx[]={0,0,1,-1},dy[]={1,-1,0,0};  //初始化偏移量数组
    
    bool flag;  //标记是否可以走到E
    
    void dfs(int x,int y){
    
        if(mp[x][y]=='E'){
            flag=1;  //标记答案
        }
    
        for(int i=0;i<4;i++){  //循环遍历偏移量数组，搜索四个方向
    
            int l=x+dx[i],r=y+dy[i];
            if(l>=1&&l<=n&&r>=1&&r<=m&&!vis[l][r]&&mp[l][r]!='#'){  //判断该点是否满足搜索条件
                vis[l][r]=1;  //标记该点已经走过
                dfs(l,r);  //继续以该点搜索
            }
    
        }
    
    }
    
    int main(){
    
        while(cin>>n>>m){  //多实例输入
    
            //初始化清空数据
            flag=0;
            memset(vis,0,sizeof vis);
            memset(mp,0,sizeof mp);
    
            for(int i=1;i<=n;i++){
                for(int j=1;j<=m;j++){
                    cin>>mp[i][j];
                    if(mp[i][j]=='S'){  //标记S的坐标
                        s1=i;
                        s2=j;
                    }
                }
            }
    
            dfs(s1,s2);
    
            if(flag) cout<<"Yes"<<endl;
            else cout<<"No"<<endl;
    
        }
    
        return 0;
    
    }

**BFS代码**
    
    
    #include &lt;bits/stdc++.h&gt;
    using namespace std;
    
    const int N=510;
    
    int n,m;
    
    char mp[N][N];  //存储地图
    
    bool vis[N][N];  //标记是否走过该点
    
    int s1,s2;  //标记S的坐标
    
    int dx[]={0,0,1,-1},dy[]={1,-1,0,0};  //初始化偏移量数组
    
    struct point{  //用于记录点的信息
        int x,y;
    };
    
    bool bfs(){
    
        queue&lt;point&gt; st;  //定义队列
    
        st.push({s1,s2});  //将S点的信息入队
        vis[s1][s2]=1;  //标记S点为走过
    
        while(!st.empty()){  //当队列不空时
    
            auto p=st.front();  //使p获得队头的信息
            st.pop();  //将队头出队
    
            for(int i=0;i<4;i++){  //循环遍历偏移量数组，搜索四个方向
    
                int l=p.x+dx[i],r=p.y+dy[i];
                if(l>=1&&l<=n&&r>=1&&r<=m&&!vis[l][r]&&mp[l][r]!='#'){  //判断该点是否满足搜索条件
                    if(mp[l][r]=='E') return 1;  //搜到答案直接返回
                    vis[l][r]=1;  //标记该点已经走过
                    st.push({l,r});
                }
    
            }
    
        }
    
        return 0;
    
    }
    
    int main(){
    
        while(cin>>n>>m){
    
            //初始化清空数据
            memset(vis,0,sizeof vis);
            memset(mp,0,sizeof mp);
    
            for(int i=1;i<=n;i++){
                for(int j=1;j<=m;j++){
                    cin>>mp[i][j];
                    if(mp[i][j]=='S'){  //标记S的坐标
                        s1=i;
                        s2=j;
                    }
                }
            }
    
            if(bfs()) cout<<"Yes"<<endl;
            else cout<<"No"<<endl;
    
        }
    
        return 0;
    
    }
