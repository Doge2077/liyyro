---
title: "创建线程的方式打开记事本"
date: 2023-09-20
categories: [c++, Tips]
description: ""
---

# 创建线程的方式打开记事本

* * *

今天操作系统课老师讲到进程，提出了一个有趣的小实验：能否以系统调用的方式利用 `Windows` 创建进程的系统调用函数来打开一个软件。闲着蛋疼的我立马来了兴趣，姑且写一个玩玩（

* * *

## 头文件

* * *

  * `&lt;windows.h&gt;`：包含了 `Windows API` 的核心功能。
  * `&lt;tchar.h&gt;`：提供了一种跨平台的方式来处理 `Unicode` 和 `ANSI` 字符集，防止出现一些编码错误。
  * `&lt;cstdio&gt;`：包含了 `C` 标准输入输出函数的声明。



* * *

## CreateThread

* * *

`CreateThread `是 `Windows API` 中的一个函数，用于创建一个新的线程。

这就是我们程序的核心函数，其函数的原型如下：
    
    
    HANDLE CreateThread(
      LPSECURITY_ATTRIBUTES   lpThreadAttributes,
      SIZE_T                  dwStackSize,
      LPTHREAD_START_ROUTINE  lpStartAddress,
      LPVOID                  lpParameter,
      DWORD                   dwCreationFlags,
      LPDWORD                 lpThreadId
    );

参数说明：

  * `lpThreadAttributes`：指向 `SECURITY_ATTRIBUTES` 结构的指针，用于指定新线程的安全性。可以设置为 `NULL`，表示使用默认的安全性。
  * `dwStackSize`：指定新线程的堆栈大小。可以设置为 $0$，表示使用默认的堆栈大小。
  * `lpStartAddress`：指向线程函数的指针，表示新线程的入口点。线程函数的原型为`DWORD WINAPI ThreadProc(LPVOID lpParameter)`，其中`lpParameter`为传递给线程函数的参数。
  * `lpParameter`：传递给线程函数的参数，可以是任意类型的指针。
  * `dwCreationFlags`：指定线程的创建标志。可以设置为 $0$，表示无特殊标志。
  * `lpThreadId`：指向`DWORD`类型变量的指针，用于接收新线程的标识符。



即：`CreateThread` 函数创建一个新的线程，并返回该线程的句柄。如果创建线程成功，返回值为线程的句柄；否则返回值为 `NULL`。

**句柄** ：

  * 有趣的是，在 `Windows` 里并没有进程层次的概念，所有进程的地位都是相同的。
  * 在创建进程时，父进程会得到一个特别令牌（句柄），用于控制子进程。
  * 该令牌是可以传递的，即父进程有权将该令牌传递给其他进程，以至于不存在了进程层次的概念。



**注意** ：

  * 新线程的入口点是通过 `lpStartAddress` 参数指定的线程函数。线程函数在新线程中执行，可以执行各种任务。
  * 线程函数的返回值是一个 `DWORD` 类型的值，表示线程的退出码。
  * 通过 `CreateThread` 函数创建的线程是可执行的，它可以并发地与其他线程执行，但线程的执行顺序和调度由操作系统决定。
  * 在使用`CreateThread`函数创建线程后，需要使用 `CloseHandle` 函数关闭线程句柄，以释放资源。



* * *

## 实现代码

* * *
    
    
    #include &lt;windows.h&gt;
    #include &lt;tchar.h&gt;
    #include &lt;cstdio&gt;
    
    DWORD WINAPI OpenNotepadThread(LPVOID lpParam) {
        // 定义要打开的应用程序的路径
        LPCTSTR appName = _T("notepad.exe");
    
        // 创建进程信息结构体
        STARTUPINFO startupInfo;
        PROCESS_INFORMATION processInfo;
    
        // 初始化进程信息结构体
        ZeroMemory(&startupInfo, sizeof(startupInfo));
        startupInfo.cb = sizeof(startupInfo);
        ZeroMemory(&processInfo, sizeof(processInfo));
    
        // 创建新进程
        if (!CreateProcess(
            NULL,                   // 指向可执行文件名的指针
            (LPTSTR)appName,        // 命令行参数
            NULL,                   // 进程句柄不可继承
            NULL,                   // 线程句柄不可继承
            FALSE,                  // 不继承句柄
            0,                      // 无特殊标志
            NULL,                   // 使用父进程的环境变量
            NULL,                   // 使用父进程的工作目录
            &startupInfo,           // 启动信息
            &processInfo            // 进程信息
        )) {
            _tprintf(_T("WRONGING：%d\n"), GetLastError());
            return 1;
        }
    
        // 等待新进程结束
        WaitForSingleObject(processInfo.hProcess, INFINITE);
    
        // 关闭进程和线程句柄
        CloseHandle(processInfo.hProcess);
        CloseHandle(processInfo.hThread);
    
        return 0;
    }
    
    int main() {
        // 创建线程
        HANDLE hThread = CreateThread(NULL, 0, OpenNotepadThread, NULL, 0, NULL);
    
        if (hThread == NULL) {
            _tprintf(_T("WRONGING：%d\n"), GetLastError());
            return 1;
        }
    
        // 等待线程结束
        WaitForSingleObject(hThread, INFINITE);
    
        // 关闭线程句柄
        CloseHandle(hThread);
    
        return 0;
    }
    

在上述代码中，我定义了一个名为 `OpenNotepadThread` 的函数，它是一个线程函数，用于打开记事本应用程序。该函数的参数类型为`LPVOID`，表示一个指向任意类型的指针。然后创建进程信息结构体 `STARTUPINFO` 和 `PROCESS_INFORMATION`，并对其进行了初始化。

接下来调用 `CreateProcess` 函数用于创建一个新的进程，返回进程的句柄和线程的句柄。它的参数包括可执行文件名、命令行参数、进程句柄和线程句柄是否可继承等信息。如果创建进程成功，返回值为 $0$；否则返回值为 $1$。

调用 `WaitForSingleObject` 函数用于等待一个对象的状态变为可信，即等待进程结束。它的参数包括要等待的对象句柄和等待的时间，这里使用 `INFINITE` 表示无限等待，直到进程结束。

当进程结束后，需要调用 `CloseHandle` 函数关闭进程和线程的句柄，释放资源。

* * *

## 测试效果

* * *

![image-20230920011044280](https://image.itbaima.net/images/40/image-20230920018657750.png)

🤗🤗🤗🤗🤗🤗🤗🤗🤗🤗🤗🤗🤗🤗🤗🤗🤗🤗🤗🤗🤗🤗🤗🤗🤗🤗🤗🤗🤗🤗🤗🤗🤗🤗🤗🤗🤗🤗🤗🤗🤗🤗🤗
