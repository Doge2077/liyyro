---
title: "自动拉取 GitHub 仓库更新的脚本"
date: 2023-08-15
categories: [Linux, Tips]
description: ""
---

# 自动拉取 GitHub 仓库更新的脚本

* * *

由于将 [HAUE-CS-WIKI](&lt;https://wiki.lys2021.com/&gt;) 部署到了我自己的服务器上作为国内镜像站，每次在源站更新后都需要手动拉取镜像站的更新实在是太麻烦了，因此产生了编写该脚本的需求（

读者可根据该脚本思路编写属于你自己的定时任务脚本。

* * *

## 脚本思路

* * *

  * 编写脚本文件，能够执行 `git pull` 命令以及 `mkdocs build` 构建命令。 
  * 对这些命令的执行结果和状态需要保存到相应的日志，以便查询执行状态。
  * 利用 `cron` 守护进程实现定时执行该脚本文件。



* * *

## 编写脚本文件

* * *
```java


#!/bin/bash

# 读取用户环境变量
. /etc/profile
source /root/.bashrc
source /root/.profile

# 导入 mkdocs 环境变量
MKDOCS_PATH="/usr/local/bin/mkdocs"

# 日志文件路径
LOG_FILE="/wiki/log/update.log"
ERROR_LOG_FILE="/wiki/log/error.log"

# 任务执行时间
update_time=$(date +"%Y-%m-%d %H:%M:%S")
tag_bar="====================================================================================================="

# 进入 haue-cs-wiki 目录
cd /wiki/haue-cs-wiki

# 执行 git pull 操作
git_pull_output=$(git pull 2>&1)
git_pull_status=$?

# 执行 mkdocs 构建
mk_build_output=$($MKDOCS_PATH 2>&1)
mk_build_status=$?

if [ $git_pull_status == 0 ] && [ $mk_build_status == 0 ]
then
    echo -e "$tag_bar\n$update_time: no errors occured 😘\n$tag_bar" >> "$ERROR_LOG_FILE"
    echo -e "$tag_bar\n$update_time: git pull successfully 🤗" >> "$LOG_FILE"
    echo -e "$update_time: mkdocs build successfully 😎\n$tag_bar\n" >> "$LOG_FILE"
else
    echo -e "$tag_bar\n$update_time: oops! errors occured 😅\n$tag_bar" >> "$LOG_FILE"
    echo -e "$tag_bar" >> "$ERROR_LOG_FILE"
    if [ $git_pull_status != 0 ]
    then
        echo -e "$update_time: git pull failed 🥵\nError: $git_pull_output" >> "$ERROR_LOG_FILE"
    fi
    if [ $mk_build_status != 0 ]
    then
        echo -e "$update_time: mkdocs build failed 🤡\nError: $mk_build_output" >> "$ERROR_LOG_FILE"
    fi
    echo -e "$tag_bar\n" >> "$ERROR_LOG_FILE"
fi
```

**注意** ：

  * 所有的文件目录均需要指定为绝对路径，防止脚本执行路径出错。
  * 由于后续 `cron` 定时任务执行时，不会携带用户的环境变量，因此在脚本中需要读入相应用户的配置文件和环境变量。



* * *

## 设置 cron 定时任务

* * *

使用 `crontab -e` 打开定时任务注册表

第一次使用会提示选择需要使用的编辑器，选择适合自己的即可。

在注册表中编辑：
```java


0 0 * * * /bin/bash /path/script.sh
```

其中 `/path/script.sh` 为执行脚本文件所在的绝对路径。

然后退出编辑，重新加载：
```java


sudo service cron reload
```

对于执行时间的设置，在 `crontab` 文件中，时间表达式由五个 `* * * * *` 字段组成，分别表示分钟、小时、日期、月份和星期几。

对于时间表达式 `* * * * *`，每个字段的含义如下：

  1. 第一个字段：分钟（取值范围：0-59）

```java
 * `*` 表示每分钟都匹配，即每分钟触发任务。
```
  2. 第二个字段：小时（取值范围：0-23）

```java
 * `*` 表示每小时都匹配，即每小时触发任务。
```
  3. 第三个字段：日期（取值范围：1-31）

```java
 * `*` 表示每天都匹配，即每天触发任务。
```
  4. 第四个字段：月份（取值范围：1-12）

```java
 * `*` 表示每个月都匹配，即每个月触发任务。
```
  5. 第五个字段：星期几（取值范围：0-6，其中 0 表示星期日）

```java
 * `*` 表示每个星期都匹配，即每个星期触发任务。
```



例如：设置为 `0 0 * * *` 表示每天 `0:00` 执行一次该定时任务。
