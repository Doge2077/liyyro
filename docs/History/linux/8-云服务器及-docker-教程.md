---
title: "8. 云服务器及 Docker 教程"
date: 2022-10-08
categories: [Linux, Linux]
description: ""
---

### 8.1 云服务器

**作用** ：

  * 存放我们的docker容器，让计算跑在云端。
  * 获得公网IP地址，让每个人可以访问到我们的服务。
  * 部署自己的项目服务等。



主流的云服务厂商：阿里云，腾讯云，华为云等。

**配置** ：

一般新购买的服务器如果是毛坯状态，需要自己配置一些内容，以找回初恋的感觉。

  * 首先 `ssh` 登录到自己的服务器


```java


ssh root@xxx.xxx.xxx.xxx  # 注意腾讯云登录的用户不是root，而是ubuntu
```

  * 在 `root` 权限账户下创建工作用户 `user` 并赋予 `sudo` 权限


```java


adduser user  # 创建用户acs
usermod -aG sudo user  # 给用户acs分配sudo权限
```

  * 在本地或云端配置 `user` 用户的别名和免密登录
  * 将祖传配置传过去


```java


scp .bashrc .vimrc .tmux.conf server_name:  # server_name需要换成自己配置的别名
```

  * 安装 `tmux`


```java


sudo apt-get update
sudo apt-get install tmux
```

  * 打开 `tmux` 安装 `Docker`，参考官方安装[Docker](&lt;https://docs.docker.com/engine/install/ubuntu/&gt;)教程



如果 `apt-get` 下载软件速度较慢，可以参考[清华大学开源软件镜像站](&lt;https://mirrors.tuna.tsinghua.edu.cn/help/ubuntu/&gt;)中的内容，修改软件源。

---

### 8.2 Docker教程

**将当前用户添加到`docker`用户组**

为了避免每次使用 `docker` 命令都需要加上 `sudo` 权限，可以将当前用户加入安装中自动创建的 `docker` 用户组，参考[官方文档](&lt;https://docs.docker.com/engine/install/linux-postinstall/&gt;)
```java


sudo usermod -aG docker $USER
```

执行完此操作后，需要退出服务器，再重新登录回来，才可以省去 `sudo` 权限。

**镜像（images）** ：

  * `docker pull xxx`：拉取一个镜像 `xxx`
  * `docker images`：列出本地所有镜像
  * `docker image rm ubuntu:20.04` 或 `docker rmi ubuntu:20.04`：删除镜像 `ubuntu:20.04`
  * `docker [container] commit NAME:TAG`：创建某个 `container` 的镜像，其名为 `NAME`，标签为 `TAG`
  * `docker save -o ubuntu_20_04.tar ubuntu:20.04`：将镜像 `ubuntu:20.04` 导出到本地文件 `ubuntu_20_04.tar` 中
  * `docker load -i ubuntu_20_04.tar`：将镜像 `ubuntu:20.04` 从本地文件 `ubuntu_20_04.tar` 中加载出来



**容器(container)** ：

  * `docker [container] create -it ubuntu:20.04`：利用镜像 `ubuntu:20.04` 创建一个容器

  * `docker [contaienr] run -itd ubuntu:20.04`：创建并启动一个容器

```java
* `docker [contaienr] run -p 20000:22 --name MYDOCKER -itd ubuntu:20.04`： 创建使用 `ubuntu:20.04` 镜像的容器，名为 `MYDOCKER` ，且设置端口映射为：20000:22
```
  * `docker ps`：查看本地运行中的容器

```java
* `docker ps -a`：查看本地所有的容器 
```
  * `docker [container] start CONTAINER`：启动容器 `CONTAINER`

  * `docker [container] stop CONTAINER`：停止容器 `CONTAINER`

  * `docker [container] restart CONTAINER`：重启容器 `CONTAINER`

`docker [container] attach CONTAINER`：进入容器 `CONTAINER`

```java
* 先按 `Ctrl-p`，再按 `Ctrl-q` 可以挂起容器
```
  * `docker [container] exec CONTAINER COMMAND`：在容器中执行命令

  * `docker [container] rm CONTAINER`：删除容器

```java
* `docker container prune`：删除所有已停止的容器
```
  * `docker export -o xxx.tar CONTAINER`：将容器`CONTAINER`导出到本地文件`xxx.tar`中

  * `docker import xxx.tar image_name:tag`：将本地文件`xxx.tar`导入成镜像，并将镜像命名为`image_name:tag`

  * `docker export/import` 与 `docker save/load`的区别：

```java
* `export/import` 会丢弃历史记录和元数据信息，仅保存容器当时的快照状态
* `save/load` 会保存完整记录，体积更大
```
  * `docker top CONTAINER`：查看某个容器内的所有进程

  * `docker stats`：查看所有容器的统计信息，包括CPU、内存、存储、网络等信息

  * `docker cp xxx CONTAINER:xxx` 或 `docker cp CONTAINER:xxx xxx`：在本地和容器间复制文件

  * `docker rename CONTAINER1 CONTAINER2`：重命名容器

  * `docker update CONTAINER --memory 500MB`：修改容器限制




**ssh登录到容器**

  * 可通过`ssh`登录自己的对应映射端口的`docker`容器


```java


ssh root@xxx.xxx.xxx.xxx -p 20000  # 将xxx.xxx.xxx.xxx替换成自己租的服务器的IP地址 20000为映射的端口号
```

  * 记得需要去云平台控制台中修改安全组配置，放行端口20000。 
  * 同样可以配置该`docker`容器的别名和免密登录。


