---
title: "5. ssh登录和scp传输"
date: 2022-09-02
categories: [Linux, Linux]
description: ""
---

### 5.1 ssh 登录

远程登录服务器：
```java


ssh user@hostname
```

  * `user`: 用户名
  * `hostname`: IP地址或域名



第一次登录时会提示：
```java


The authenticity of host '123.57.47.211 (123.57.47.211)' can't be established.
ECDSA key fingerprint is SHA256:iy237yysfCe013/l+kpDGfEG9xxHxm0dnxnAbJTPpG8.
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

输入`yes`，然后回车即可。 这样会将该服务器的信息记录在`~/.ssh/known_hosts`文件中。

然后输入密码即可登录到远程服务器中。

默认登录端口号为22。如果想登录某一特定端口：
```java


ssh user@hostname -p 22
```

---

### 5.2 配置文件

创建文件 `~/.ssh/config`。

用`Vim`打开文件中输入：
```java


Host myserver1
    HostName IP地址或域名
    User 用户名

Host myserver2
    HostName IP地址或域名
    User 用户名
```

之后再使用服务器时，可以直接使用别名`myserver1`、`myserver2`

---

### 5.3 密钥登录

创建密钥：
```java


ssh-keygen
```

然后一直回车即可。

执行结束后，`~/.ssh/`目录下会多两个文件：

  * `id_rsa`：私钥
  * `id_rsa.pub`：公钥



之后想免密码登录哪个服务器，就将公钥传给哪个服务器即可。

例如，想免密登录`myserver`服务器。则将**当前服务器公钥** 中的内容，复制到`myserver`中的`~/.ssh/authorized_keys`文件里即可。

也可以使用如下命令一键添加公钥：
```java


ssh-copy-id myserver  #mysever是配置免密登录的服务器名称
```

**总结** ：

  * 由服务器 `A` 免密登录到服务器 `B`:
  * 先在服务器 `A` 中的 `.ssh/` 文件夹下配置 `config` 文件。
  * 之后尝试 `ssh serverB` 登录一遍，检查是否异常。
  * 回到服务器 `A` 执行 `ssh-keygen` 生成该服务器的私钥和公钥（若已有则无需执行）。
  * 然后执行 `ssh-copy-id serverB` 即可，或手动将服务器 `A` 的 `id_rsa.pub` 中的内容复制到服务器 `B` 的`~/.ssh/authorized_keys`文件里即可。



---

### 5.4 scp传输

命令格式：
```java


scp source destination
```

将`source`路径下的文件复制到`destination`中

**一次复制多个文件** ：
```java


scp source1 source2 destination
```

**复制文件夹** ：
```java


scp -r ~/tmp myserver:/home/acs/  #将本地家目录中的tmp文件夹复制到myserver服务器中的/home/acs/目录下。


scp -r ~/tmp myserver:homework/  #将本地家目录中的tmp文件夹复制到myserver服务器中的~/homework/目录下。


scp -r myserver:homework .  #将myserver服务器中的~/homework/文件夹复制到本地的当前路径下。
```

**指定服务器的端口号** ：
```java


scp -P 22 source1 source2 destination
```

**注意** ： `scp`的`-r -P`等参数尽量加在`source`和`destination`之前。

> 使用`scp`配置其他服务器的`vim`和`tmux`
>     
>     
>     scp ~/.vimrc ~/.tmux.conf myserver:
