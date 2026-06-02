---
title: "1. Linux 常用命令"
date: 2022-07-03
categories: [Linux, Linux]
description: ""
---

### 1.1 ctrl c && ctrl u && clear
```java


ctrl c  #取消命令，并且换行

ctrl u  #清空本行命令

clear  #清空屏幕
```

* * *

### 1.2 tab
```java


tab  #可以补全命令和文件名，补全不了连按两下tab键，显示备选项
```

* * *

### 1.3 ls && ll && tree && cat
```java


ls  #只列出文件名或目录名

ll  #列出来的结果详细，有时间，是否可读写等信息   

ls -a  #展示所有文件，包括隐藏的文件,

tree  #列出树状关系

cat #展示文件里的内容
```

* * *

### 1.4 pwd
```java


pwd  #显示当前的绝对路径
```

* * *

### 1.5 cd
```java


cd ~  #返回家目录(当前用户目录)

cd -  #返回上一次访问的目录

cd /  #返回根目录

cd .  #返回当前目录

cd ..  #返回上级目录
```

* * *

### 1.6 touch
```java


touch xxx  #在当前目录创建文件xxx

touch dir_1/xxx  #在dir_1目录下创建文件xxx
```

* * *

### 1.7 mkdir
```java


mkdir dir_1  #在当前目录下创建目录dir_1

mkdir -p dir_1/dir_2/dir_3  #在当前目录下创建多级目录
```

* * *

### 1.8 cp
```java


cp xxx yyy  #将xxx文件复制并重命名为yyy到当前目录

cp dir_2/xxx dir_2/yyy  #将dir_1目录下的xxx文件复制并重命名到dir_2目录中

cp -r dir_1 dir2/dir_3  #将目录dir_1复制到目录dir_2并重命名为目录dir_3
```

* * *

### 1.9 mv
```java


mv xxx yyy  #将xxx重命名为yyy

mv dir_1 dir_2  #将目录dir_1移动到目录dir_2下

mv dir_1/xxx dir_2/yyy  #将dir_1目录下的文件xxx剪切到目录dir_2下并重命名为yyy
```

* * *

### 1.10 rm
```java


rm -rf xxx.txt  #强制删除文件
rm -rf dir_1  #强制删除目录

#支持正则表达式
```

* * *
