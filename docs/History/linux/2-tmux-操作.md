---
title: "2. Tmux 操作"
date: 2022-07-06
categories: [Linux]
description: ""
---

### 2.1 Tmux 简介

**功能：**

*   分屏操作
*   允许断开 Terminal 连接后，继续运行进程。

**结构：**

一个 tmux 可以包含多个 session，一个 session 可以包含多个 window，一个 window 可以包含多个 pane。
实例：
tmux:
    session 0:
        window 0:
            pane 0
            pane 1
            pane 2
            ...
        window 1
        window 2
        ...
    session 1
    session 2
    ...

**注意：** 本操作支持的前缀键由默认的 `Ctrl+b` 更改为 `Ctrl+a`。

---

### 2.2 打开和关闭操作

*   `tmux`：新建一个 `session`，其中包含一个 `window`，`window` 中包含一个 `pane`，`pane` 里打开了一个 `shell` 对话框。
*   `Ctrl + d`：关闭当前 `pane`。如果关闭后当前 `window` 的所有 `pane` 均已关闭，则自动关闭该 `window`；如果进一步导致当前 `session` 的所有 `window` 均已关闭，则自动关闭该 `session`。

---

### 2.3 分屏操作

*   按下 `Ctrl + a` 后松开，然后按 `%`：将当前 `pane` 左右平分成两个 `pane`。
*   按下 `Ctrl + a` 后松开，然后按 `"`（注意是双引号）：将当前 `pane` 上下平分成两个 `pane`。

---

### 2.4 pane 操作

*   按下 `Ctrl + a` 后松开，然后按方向键：选择相邻的 `pane`。
*   按住 `Ctrl + a` 的同时按方向键：可以调整 `pane` 之间分割线的位置。
*   按下 `Ctrl + a` 后松开，然后按 `z`：将当前 `pane` 全屏或取消全屏。

---

### 2.5 session 操作

*   按下 `Ctrl + a` 后松开，然后按 `s`：选择其它 `session`。在选择界面中：
    *   方向键 ↑：选择上一项 `session/window/pane`。
    *   方向键 ↓：选择下一项 `session/window/pane`。
    *   方向键 →：展开当前选中的 `session/window`。
    *   方向键 ←：折叠当前选中的 `session/window`。
*   按下 `Ctrl + a` 后松开，然后按 `c`：在当前 `session` 中创建一个新的 `window`。

---

### 2.6 挂起和唤醒

*   按下 `Ctrl + a` 后松开，然后按 `d`：挂起（detach）当前 `session`。
*   `tmux a`：唤醒（attach）之前挂起的 `session`。

---

### 2.7 复制和粘贴

*   在 `tmux` 中选中文本时，要按住 `shift` 键：
    *   按下 `Ctrl + a` 后松开手指，然后按 `[`，之后用鼠标选中文本，即可复制到 `tmux` 的剪贴板。
    *   按下 `Ctrl + a` 后松开手指，然后按 `]`，可粘贴到光标处。