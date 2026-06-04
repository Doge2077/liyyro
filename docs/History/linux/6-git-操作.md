---
title: "6. git 操作"
date: 2022-09-02
categories: [Linux, Linux]
description: ""
---

### 6.1 Git 基本概念

* 工作区：仓库的目录。工作区是独立于各个分支的。
  * 暂存区：数据暂时存放的区域，类似于工作区写入版本库的缓冲区。暂存区是独立于各个分支的。
  * 版本库：存放所有已经提交到本地仓库的代码版本
  * 版本结构：树结构，树中每个节点代表一个代码版本。

---

### 6.2 Git 命令

---

#### 6.2.1 全局设置

* `git config --global user.name xxx`：设置全局用户名，信息记录在`~/.gitconfig`文件中
  * `git config --global user.email xxx@xxx.com`：设置全局邮箱地址，信息记录在`~/.gitconfig`文件中
  * `git init`：将当前目录初始化为Git仓库，信息记录在隐藏的`.git`文件夹中

---

#### 6.2.2 常用命令

* `git add XX`：将XX文件添加到暂存区
  * `git commit -m "说明信息"`：将暂存区的内容提交到当前分支
  * `git status`：查看仓库状态
  * `git log`：查看当前分支的所有版本
  * `git push -u`（第一次需要加`-u`，以后不需要）：将当前分支推送到远程仓库
  * `git clone git@git.acwing.com:xxx/XXX.git`：将远程仓库`XXX`下载到当前目录下
  * `git branch`：查看所有分支和当前所处分支

---

#### 6.2.3 查看命令

* `git diff XX`：查看`XX`文件相对于暂存区修改了哪些内容
  * `git status`：查看仓库状态
  * `git log`：查看当前分支的所有版本
  * `git log --pretty=oneline`：让每个版本信息用一行显示
  * `git reflog`：查看`HEAD`指针的移动历史（包括被回滚的版本）
  * `git branch`：查看所有分支和当前所处分支
  * `git pull`：将远程仓库的当前分支与本地仓库的当前分支合并

---

#### 6.2.4 删除命令

* `git rm --cached XX`：将文件`XX`从仓库索引目录中删掉，取消版本控制
  * `git restore --staged xx`：将文件`xx`从暂存区里移除
  * `git checkout -- XX`或`git restore XX`：将`XX`文件尚未加入暂存区的修改全部撤销

---

#### 6.2.5 代码回滚

* `git reset --hard HEAD^` 或 `git reset --hard HEAD~`：回滚到上一个版本
  * `git reset --hard HEAD^^`：往上回滚两次，以此类推
  * `git reset --hard HEAD~100`：往上回滚100个版本
  * `git reset --hard` 版本号：回滚到某一特定版本

---

#### 6.2.6 远程仓库

#### 6.2.6 远程仓库命令

* `git remote add origin git@git.acwing.com:xxx/XXX.git`：将本地仓库关联到远程仓库
* `git push -u`（第一次需要 -u，以后不需要）：将当前分支推送到远程仓库
* `git push origin branch_name`：将本地的某个分支推送到远程仓库
* `git clone git@git.acwing.com:xxx/XXX.git`：将远程仓库 XXX 下载到当前目录下
* `git push --set-upstream origin branch_name`：设置本地的 `branch_name` 分支对应远程仓库的 `branch_name` 分支
* `git push -d origin branch_name`：删除远程仓库的 `branch_name` 分支
* `git checkout -t origin/branch_name`：将远程的 `branch_name` 分支拉取到本地
* `git pull`：将远程仓库的当前分支与本地仓库的当前分支合并
* `git pull origin branch_name`：将远程仓库的 `branch_name` 分支与本地仓库的当前分支合并
* `git branch --set-upstream-to=origin/branch_name1 branch_name2`：将远程的 `branch_name1` 分支与本地的 `branch_name2` 分支对应

---

#### 6.2.7 分支命令

* `git branch branch_name`：创建新分支
* `git branch`：查看所有分支和当前所处分支
* `git checkout -b branch_name`：创建并切换到 `branch_name` 这个分支
* `git checkout branch_name`：切换到 `branch_name` 这个分支
* `git merge branch_name`：将分支 `branch_name` 合并到当前分支上
* `git branch -d branch_name`：删除本地仓库的 `branch_name` 分支
* `git push --set-upstream origin branch_name`：设置本地的 `branch_name` 分支对应远程仓库的 `branch_name` 分支
* `git push -d origin branch_name`：删除远程仓库的 `branch_name` 分支
* `git checkout -t origin/branch_name`：将远程的 `branch_name` 分支拉取到本地
* `git pull`：将远程仓库的当前分支与本地仓库的当前分支合并
* `git pull origin branch_name`：将远程仓库的 `branch_name` 分支与本地仓库的当前分支合并
* `git branch --set-upstream-to=origin/branch_name1 branch_name2`：将远程的 `branch_name1` 分支与本地的 `branch_name2` 分支对应

---

#### 6.2.8 stash 暂存

**主要修复内容：**
- 统一了列表项的缩进层级（原文中部分子项错误地缩进了两级）
- 规范了括号和标点的格式（中文括号、全角标点）
- 统一了代码块与中文之间的空格

`git stash`：将工作区和暂存区中尚未提交的修改存入栈中  
- `git stash apply`：将栈顶存储的修改恢复到当前分支，但不删除栈顶元素  
- `git stash drop`：删除栈顶存储的修改  
- `git stash pop`：将栈顶存储的修改恢复到当前分支，同时删除栈顶元素  
- `git stash list`：查看栈中所有元素