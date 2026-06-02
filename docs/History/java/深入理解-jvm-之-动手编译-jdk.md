---
title: "深入理解 JVM 之——动手编译 JDK"
date: 2023-08-29
categories: [Java, jvm]
description: ""
---

本篇为深入理解 `Java` 虚拟机第一章的实战内容，推荐在学习前先掌握基础的 `Linux` 操作、编译原理基础以及扎实的 `C/C++` 功底。

该系列的 `GitHub` 仓库：&lt;https://github.com/Doge2077/learn-jvm&gt;

* * *

## 构建编译环境

* * *

### 系统准备

* * *

> 在官方文档上要求编译 `OpenJDK` 至少需要 `2～4GB` 的内存空间（CPU核心数越多，需要的内存越大），而且至少要 `6～8GB` 的空闲磁盘空间，不要看 `OpenJDK` 源码的大小只有不到 `600MB`，要完成编译，过程中会产生大量的中间文件，并且编译出不同优化级别（Product、FastDebug、SlowDebug）的 `HotSpot` 虚拟机可能要重复生成这些中间文件，这都会占用大量磁盘空间。

参考我的虚拟机配置如下：

  * `VM` 虚拟机 `Ubuntu20.04`

  * 处理器 `8` 核，内存 `8G`，硬盘 `40G`




**注意** ：所有文件所在目录都不能包含中文。

* * *

### 环境准备

* * *

下载 `JDK12` 源码：
```java


wget https://hg.openjdk.org/jdk/jdk12/archive/06222165c35f.tar.gz
```

> 通过 `Mercurial` 代码版本管理工具从 `Repository` 中直接取得源码
>     
>     
>     hg clone https://hg.openjdk.java.net/jdk/jdk12

解压：
```java


tar xvf 06222165c35f.tar.gz
```

安装 `GCC` 编译器：
```java


sudo apt-get install build-essential
```

安装后执行：
```java


gcc -v
```

如果版本为 `gcc version 9.4.0 (Ubuntu 9.4.0-1ubuntu1~20.04.1)` ，版本太高会导致后面编译失败，需要卸载重装 `gcc`：
```java


sudo apt-get remove gcc
```

安装 `gcc-7`：
```java


sudo apt-get install gcc-7
sudo apt-get install g++-7

# 设置默认选项
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-7 100
sudo update-alternatives --config gcc
sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-7 100
sudo update-alternatives --config g++
```

再次执行 `gcc -v` 可以看到版本为 `gcc version 7.5.0 (Ubuntu 7.5.0-6ubuntu2)` 即可。

进入解压后的 `jdk12-06222165c35f` 目录 ，安装在编译过程中需要的依赖 `FreeType`、`CUPS` 等若干第三方库：
```java


sudo apt-get install libfreetype6-dev
sudo apt-get install libcups2-dev
sudo apt-get install libx11-dev libxext-dev libxrender-dev libxrandr-dev libxtst-dev libxt-dev
sudo apt-get install libasound2-dev
sudo apt-get install libffi-dev 
sudo apt-get install autoconf
```

安装启动 `JDK`：
```java


sudo apt-get install openjdk-11-jdk
```

* * *

## 进行编译

* * *

在解压后的 `jdk12-06222165c35f` 目录下，执行：
```java


bash configure --enable-debug --with-jvm-variants=server
```

如果缺少未安装的库，根据报错提示安装即可，成功后显示：

![image-20230829164908588](https://image.itbaima.net/images/40/image-20230829162471905.png)

然后，编译，启动！
```java


make images
```

打开资源管理查看进程，可以看到八核线程~~汗液~~ 狂飙（

![image-20230829165553313](https://image.itbaima.net/images/40/image-20230829164444852.png)

经过长达十分钟左右的等待后，可以看到编译如下信息，提示编译成功：
```java


Finished building target 'images' in configuration 'linux-x86_64-server-fastdebug'
```

该 `linux-x86_64-server-fastdebug` 目录即为我们编译后的 `JDK` 目录，我们进入然后执行：
```java


java -version
```

可以看到编译后的 `JDK` 默认会带上编译的机器名：

![image-20230829170644862](https://image.itbaima.net/images/40/image-2023082917756908.png)

然后我们就可以对着 `JDK` 进行激情乱搞了（bushi

* * *

## 在 Clion 中调试

* * *

### 连接到虚拟机

* * *

在 `Windows Terminal` 或 `cmd` 中执行：
```java


ipconfig
```

记录本机 `IPv4` 地址 `xxx.xxx.xxx.xxx`。

在虚拟机 `Terminal` 中执行：
```java


ifconfig
```

记录虚拟机虚拟机的 `ens33:inet` 地址 `yyy.yyy.yyy.yyy`。

> 若提示 `ifconfig not found` 则执行 `sudo apt install net-tools` 安装即可。

然后打开编辑栏的虚拟网络编辑服务器：

![image-20230829224327986](https://image.itbaima.net/images/40/image-20230829223203032.png)

选择`NAT` 模式连接，进入 `NAT` 设置，添加：

![image-20230829224523863](https://image.itbaima.net/images/40/image-2023082922295393.png)

弹出的**映射传入端口** 中:

  * 主机端口，默认是 `22`
  * 虚拟机地址填写 `yyy.yyy.yyy.yyy`
  * 虚拟机端口，默认 `22`



通过上述步骤，我们就成功将主机 `xxx.xxx.xxx.xxx:22` 与 虚拟机 `yyy.yyy.yyy.yyy:22` 映射到了一起。

之后进行 `ssh` 登录即可连接，若需要继续配置免密登录，可以参考教程：[ssh 登录和 scp 传输](&lt;https://lys2021.com/?p=784&gt;)

* * *

### Clion 导入项目

* * *

建议安装 `JetBrains Gateway` 进行操作，当然你也可以直接使用 `Clion` 进行导入，步骤是一样滴（

打开 `Clion` 在远程登录选择 `SSH` 进行新建项目：

![image-20230829225754109](https://image.itbaima.net/images/40/image-20230829229218578.png)

首次连接需要选择连接的服务器：

![image-20230829225910639](https://image.itbaima.net/images/40/image-20230829229601301.png)

我们新建一个连接，左上角 `+` 号新建配置，之后填入虚拟机的 `ip` 以及登录用户：

![image-20230829230037546](https://image.itbaima.net/images/40/image-20230829234651554.png)

密码验证方式可以自行选择，最后测试连接，连接成功后选择 `Makefile` 文件导入，然后连接即可：

![image-20230829231215443](https://image.itbaima.net/images/40/image-20230829231439414.png)

由于我安装了 `JetBrains Gateway`，所以最终看起来是酱紫：

![image-20230829231825275](https://image.itbaima.net/images/40/image-20230829236499870.png)

到这一步，恭喜你可以开始愉快的玩耍了（xjbg

* * *
