---
title: "1. Django 项目创建"
date: 2022-10-29
categories: [Django, Django]
description: ""
---

# 1-django-项目创建


## 1.1 服务器及 Docker 环境

---

### 1.1.1 云服务器

---

上线项目和调试需要公网 `IP`，因此需提前准备好一个云服务器，购买以及相关环境配置参考：[云服务器及 Docker 教程](https://lys2021.com/8-%e4%ba%91%e6%9c%8d%e5%8a%a1%e5%99%a8%e5%8f%8a-docker-%e6%95%99%e7%a8%8b/)。

其次，在本地或者任何方便的 `shell` 终端配置好服务器的免密登录，以便随时连接到服务器进行工作。

---

### 1.1.2 镜像和容器配置

---

配置好服务器后，在终端将课程提供的镜像 `django_lesson_1_0.tar` 上传至服务器：
```shell
scp /var/lib/acwing/docker/images/django_lesson_1_0.tar server_name:  #server_name 为配置好免密登录的服务器名称
```

接下来将镜像加载到本地：
```shell
docker load -i django_lesson_1_0.tar
```

创建并运行容器，并初始化端口映射：
```shell
docker run -p 20000:22 -p 8000:8000 --name django_server -itd django_lesson:1.0
```

* 若某主机端口被其他容器占用，可以修改端口，如 `20022:22`。
  * 若忘记初始化端口，需要停止并删除该容器，重新创建。
  * 一个主机端口只能被一个容器使用，运行中的容器添加新的端口只能将当前容器打包成镜像，重新运行。

连接容器并创建一个 `root` 用户，之后配置该容器的免密登录即可。

---

## 1.2 配置项目 Git 环境

---

打开 `tmux` 初始化新的 Django 项目：
```shell
django-admin startproject acapp  #acapp 为项目所在文件夹
```

然后将 `acapp` 项目文件夹初始化 Git 仓库，便于版本控制管理和维护，且上传云端后可以防止项目丢失。
```shell
git init  #进入 acapp 中初始化 Git 仓库
```

将该容器的公钥上传 Git，在偏好设置中添加 SSH 密钥，之后在 Git 云端创建新的项目，按照提示在终端里连接仓库。

---

## 1.3 尝试运行项目

---

在 `acapp` 文件夹下执行下方指令运行项目：
```shell
python3 manage.py runserver 0.0.0.0:8000
```

然后浏览器打开 `xx.xx.xx.xx:8000` 进入项目界面。

其中 `xx.xx.xx.xx` 为服务器的公网 IP，`8000` 为接入的端口。

首次打开会提示需要将 `xx.xx.xx.xx` 该 IP 加入到 `ALLOWED_HOSTS` 中，一般该设置所在文件位置为 `/acapp/acapp/settings.py`，使用 `vim` 打开文件 `settings.py`，找到 `ALLOWED_HOSTS` 选项添加 IP。

顺便找到 `settings.py` 里的 `TIME_ZONE` 选项，修改时区为 `'Asia/Shanghai'`，以便对应本地时间。

另一种方法直接全文查找 `grep ALLOWED_HOSTS` 返回文件位置。

**注意**：

* 运行后，控制台会显示项目主页的访问请求信息，按 `Ctrl + c` 结束进程。
  * 更新的一些相关前端文件在运行时会实时更新，控制台也会返回报错信息。

---

## 1.4 创建 Django app

---

创建一个 `Django` 子应用：
```python
python3 manage.py startapp game  #game 为该子应用的名字
```

之后的项目开发在这个子应用 `game` 文件夹下进行。

关闭运行中的控制台，同步数据库：
```python
python3 manage.py migrate
```

创建管理员账号：
```python
python3 manage.py createsuperuser
```

接下来重启控制台：
```python
python3 manage.py runserver 0.0.0.0:8000
```

浏览器打开 `xx.xx.xx.xx:8000/admin` 进入管理员登录界面，输入创建好的账号即可登录。

---

## 1.5 项目架构与逻辑

---

### 1.5.1 项目架构

---

对于每一个 `Django` 应用来说，基本存在如下结构：

* `models`：数据类库，存储预定义的 `class`。
  * `views`：存储函数及其执行逻辑。
  * `urls`：存储路由，链接的指向。
  * `templates`：存储 `html` 文件。

---

### 1.5.2 项目逻辑

---

**game/views.py**

`views` 存储函数及其执行的逻辑：
```python
from django.http import HttpResponse

def index(request):
    return HttpResponse("lys is a dog")
```

在如上例子中，当 `index()` 函数接收到用户的请求的时，就会被调用，执行 `HttpResponse("lys is a dog")`。

**game/urls.py**

`urls` 存储了相应的路由，即调用函数链接的指向，此处的路由为 `game` 子应用的路由：
```python
from django.urls import path
from game.views import index  # 从 game/views.py 中调用 index 函数

urlpatterns = [
    path('', index, name="index")
]
```

执行语句 `path('', index, name='game_index')` 意思为，在用户访问网站的 `/game` 目录时（`path`的路径为 `''`，即为空路径，默认指向当前目录的根目录）会调用 `index` 函数。

`index` 函数的定义及其执行逻辑存储在 `game/views.py` 中，故需要 `from game.views import index`，其中 `name="index"` 表示它在该 `urls.py` 里的名字。

**acapp/urls.py**

设置子应用的路由仍需要将其加入到整个项目的路由当中：

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('game.urls')),
    path('admin/', admin.site.urls)
]
```

此处的 `path` 为空路径，默认访问整个网站的根目录。由于此时调用了 `include('game.urls')`，所以会使用 `game.urls` 中的 URL 配置。

在 `game/urls.py` 中，我们已经设置了路由映射，接下来会执行在 `urls.py` 中指定的视图函数。

综上，利用上面的两个路由，在访问 `xx.xx.xx.xx:8000/` 时，实际访问的是 `xx.xx.xx.xx:8000/game` 界面，并且此时 `game/urls.py` 执行 `game/views.py` 中的 `index` 函数，该函数返回一个字符串 `"lys is a dog"` 输出在该页面中。
