---
title: "JDK源码系列（四）"
date: 2024-10-29
categories: [Software Architect]
description: ""
---

# Synchronized 类

* * *

## 基础概念

* * *

如果某一个资源被多个线程共享，为了避免因为资源抢占导致资源数据错乱，我们需要对线程进行同步，那么synchronized就是实现线程同步的关键字

synchronized 的作用是保证在同一时刻， 被修饰的代码块或方法只会有一个线程执行，以达到保证并发安全的效果。

* * *

### synchronized 的特性

* * *

  * **原子性** ：所谓原子性就是指一个操作或者多个操作，要么全部执行并且执行的过程不会被任何因素打断，要么就都不执行。
  * **可见性** ： 可见性是指多个线程访问一个资源时，该资源的状态、值信息等对于其他线程都是可见的。（通过“在执行unlock之前，必须先把此变量同步回主内存”实现）
  * **有序性** ：有效解决重排序问题（通过“一个变量在同一时刻只允许一条线程对其进行lock操作”）



* * *

### synchronized 的用法

* * *

从语法上讲，Synchronized可以把任何一个非 null 对象作为"锁"

在HotSpot JVM实现中，锁有个专门的名字：对象监视器（Object Monitor）。

三种用法：

  * 修饰静态方法
  * 修饰成员函数
  * 直接定义代码块


    
    
    // （1）修饰静态方法
    public synchronized static void helloStatic(){
        System.out.println("hello world static");
    }
    
    // （2）修饰成员函数
    public synchronized void hello(){
        System.out.println("hello world");
    }
    
    // （3）直接定义代码块
    public void test(){
        SynchronizedTest test = new SynchronizedTest();        
        synchronized (test){
            System.out.println("hello world");
        }
    }

* * *

## synchronized 底层原理

* * *

synchronized 有两种形式上锁

  * 对方法上锁
  * 构造同步代码块



他们的底层实现其实都一样：

  * 在进入同步代码之前先获取锁
  * 获取到锁之后锁的计数器+1，同步代码执行完锁的计数器-1
  * 如果获取失败就阻塞式等待锁的释放



他们在同步块识别方式上有所不一样，从class字节码文件可以表现出来，一个是通过方法flags标志，一个是monitorenter和monitorexit指令操作。

* * *

### 同步代码块

* * *

定义一个同步代码块：
    
    
    package test;
    
    public class Main {
        public static void main(String[] args) {
            Object o = new Object();
            synchronized (o) {
                System.out.println("Hello World");
            }
        }
    }

javac 编译出class字节码，然后反编译 javap -c 找到该 method 方法所在的指令块：
    
    
    Compiled from "Main.java"
    public class test.Main {
      public test.Main();
        Code:
           0: aload_0
           1: invokespecial #1                  // Method java/lang/Object."&lt;init&gt;":()V
           4: return
    
      public static void main(java.lang.String[]);
        Code:
           0: new           #2                  // class java/lang/Object
           3: dup
           4: invokespecial #1                  // Method java/lang/Object."&lt;init&gt;":()V
           7: astore_1
           8: aload_1
           9: dup
          10: astore_2
          11: monitorenter
          12: getstatic     #3                  // Field java/lang/System.out:Ljava/io/PrintStream;
          15: ldc           #4                  // String Hello World
          17: invokevirtual #5                  // Method java/io/PrintStream.println:(Ljava/lang/String;)V
          20: aload_2
          21: monitorexit
          22: goto          30
          25: astore_3
          26: aload_2
          27: monitorexit
          28: aload_3
          29: athrow
          30: return
        :
           from    to  target type
              12    22    25   any
              25    28    25   any
    }

由此可见第 11 行出现了 monitorenter 指令，第 21 和 27 行出现了 monitorexit 指令

[JVM 规范——monitorenter](&lt;https://docs.oracle.com/javase/specs/jvms/se8/html/jvms-6.html#jvms-6.5.monitorenter&gt;) 中的解释，每个对象有一个监视器锁（monitor）。

当 monitor 被占用时就会处于锁定状态，线程执行 monitorenter 指令时尝试获取 monitor 的所有权，过程如下：

  * 如果 monitor 的进入数为 0，则该线程进入 monitor，然后将进入数设置为 1，该线程即为monitor的所有者
  * 如果线程已经占有该 monitor，只是重新进入，则进入monitor 的进入数加 1
  * 如果其他线程已经占用了monitor，则该线程进入阻塞状态，直到 monitor 的进入数为 0，再重新尝试获取 monitor 的所有权



[JVM 规范——monitorexit](&lt;https://docs.oracle.com/javase/specs/jvms/se8/html/jvms-6.html#jvms-6.5.monitorexit&gt;) 中的解释：

  * 执行monitorexit 的线程必须是 objectref 所对应的 monitor 的所有者
  * 指令执行时，monitor 的进入数减 1，如果减 1 后进入数为 0，那线程退出 monitor，不再是这个monitor的所有者
  * 其他被这个 monitor 阻塞的线程可以尝试去获取这个 monitor 的所有权。 



**注意** ：

  * 这里的 monitorenter 只进行了一次，但是 monitorexit 却出现了两次
  * 观察 Exception table，发现会捕获 12 ~ 22 之间的代码异常，而在进入该部分代码前已经执行过 monitorenter
  * 因此发生异常后跳转到 target 25行后执行，需要在 27 行再次执行 monitorexit 保证锁的释放



* * *

### 同步方法

* * *

将 synchorized 定义到方法上：
    
    
    package test;
    
    public class Main {
    
        public synchronized void hello() {
            System.out.println("Hello World");
        }
    
        public static void main(String[] args) {
        }
    
    }

javac 编译出class字节码，然后反编译 javap -c 找到该 method 方法所在的指令块：
    
    
      public synchronized void hello();
        descriptor: ()V
        flags: (0x0021) ACC_PUBLIC, ACC_SYNCHRONIZED
        Code:
          stack=2, locals=1, args_size=1
             0: getstatic     #2                  // Field java/lang/System.out:Ljava/io/PrintStream;
             3: ldc           #3                  // String Hello World
             5: invokevirtual #4                  // Method java/io/PrintStream.println:(Ljava/lang/String;)V
             8: return
          LineNumberTable:
            line 9: 0
            line 10: 8

从编译的结果来看，方法的同步并没有通过指令 `monitorenter` 和 `monitorexit` 来完成（理论上其实也可以通过这两条指令来实现），不过相对于普通方法，其常量池中多了 `ACC_SYNCHRONIZED` 标示符。

JVM就是根据该标示符来实现方法的同步的：

  * 当方法调用时，调用指令将会检查方法的 ACC_SYNCHRONIZED 访问标志是否被设置
  * 如果设置了，执行线程将先获取monitor，获取成功之后才能执行方法体，方法执行完后再释放monitor
  * 在方法执行期间，其他任何线程都无法再获得同一个monitor对象。



两种同步方式本质上没有区别，只是方法的同步是一种隐式的方式来实现，无需通过字节码来完成。

两个指令的执行是JVM通过调用操作系统的互斥原语 mutex 来实现，被阻塞的线程会被挂起、等待重新调度，会导致“用户态和内核态”两个态之间来回切换，对性能有较大影响。

* * *

### 监视器原理

* * *

在 Java 中，synchronized 是非公平锁，也是可以重入锁：

  * 所谓的非公平锁是指，线程获取锁的顺序不是按照访问的顺序先来先到的，而是由线程自己竞争，随机获取到锁。
  * 可重入锁指的是，一个线程获取到锁之后，可以重复得到该锁。这些内容是理解接下来内容的前置知识。



任何一个对象都有一个Monitor与之关联，当且一个Monitor被持有后，它将处于锁定状态。

Synchronized在JVM里的实现都是 基于进入和退出Monitor对象来实现方法同步和代码块同步，虽然具体实现细节不一样，但是都可以通过成对的MonitorEnter和MonitorExit指令来实现。 

  * MonitorEnter指令：插入在同步代码块的开始位置，当代码执行到该指令时，将会尝试获取该对象Monitor的所有权，即尝试获得该对象的锁；
  * MonitorExit指令：插入在方法结束处和异常处，JVM保证每个MonitorEnter必须有对应的MonitorExit；



在 HotSpot 虚拟机中，Monitor 底层是由 C++实现的，它的实现对象是 ObjectMonitor，ObjectMonitor 结构体的实现如下：
    
    
    ObjectMonitor::ObjectMonitor() {  
      _header       = NULL;  
      _count       = 0;  
      _waiters      = 0,  
      _recursions   = 0;       //线程的重入次数
      _object       = NULL;  
      _owner        = NULL;    //标识拥有该monitor的线程
      _WaitSet      = NULL;    //等待线程组成的双向循环链表，_WaitSet是第一个节点
      _WaitSetLock  = 0 ;  
      _Responsible  = NULL ;  
      _succ         = NULL ;  
      _cxq          = NULL ;    //多线程竞争锁进入时的单向链表
      FreeNext      = NULL ;  
      _EntryList    = NULL ;    //_owner从该双向循环链表中唤醒线程结点，_EntryList是第一个节点
      _SpinFreq     = 0 ;  
      _SpinClock    = 0 ;  
      OwnerIsThread = 0 ;  
    } 

在以上代码中有几个关键的属性：

  * _count：记录该线程获取锁的次数（也就是前前后后，这个线程一共获取此锁多少次）。
  * _recursions：锁的重入次数。
  * _owner：The Owner 拥有者，是持有该 ObjectMonitor（监视器）对象的线程；
  * _EntryList：EntryList 监控集合，存放的是处于阻塞状态的线程队列，在多线程下，竞争失败的线程会进入 EntryList 队列。
  * _WaitSet：WaitSet 待授权集合，存放的是处于 wait 状态的线程队列，当线程执行了 wait() 方法之后，会进入 WaitSet 队列。 ![image.png](https://cdn.jsdelivr.net/gh/Doge2077/liyyro-photo@main/images/2024/10/屏幕截图-2024-10-29-145205.png)



监视器执行的流程如下：

  * 线程通过 CAS（对比并替换）尝试获取锁，如果获取成功，就将 _owner 字段设置为当前线程，说明当前线程已经持有锁，并将 _recursions 重入次数的属性 +1。如果获取失败则先通过自旋 CAS 尝试获取锁，如果还是失败则将当前线程放入到 EntryList 监控队列（阻塞）。
  * 当拥有锁的线程执行了 wait 方法之后，线程释放锁，将 owner 变量恢复为 null 状态，同时将该线程放入 WaitSet 待授权队列中等待被唤醒。
  * 当调用 notify 方法时，随机唤醒 WaitSet 队列中的某一个线程，当调用 notifyAll 时唤醒所有的 WaitSet 中的线程尝试获取锁。
  * 线程执行完释放了锁之后，会唤醒 EntryList 中的所有线程尝试获取锁。



* * *

## 锁升级

* * *

### 无锁

* * *

对于共享资源，不涉及多线程的竞争访问。

* * *

### 偏向锁

* * *

共享资源首次被访问时，JVM会对该共享资源对象做一些设置：

  * 比如将对象头中是否偏向锁标志位置为1，对象头中的线程ID设置为当前线程ID（注意：这里是操作系统的线程ID）
  * 后续当前线程再次访问这个共享资源时，会根据偏向锁标识跟线程ID进行比对是否相同，比对成功则直接获取到锁，进入**临界区域** （就是被锁保护，线程间只能串行访问的代码），这也是synchronized锁的可重入功能



* * *

### 轻量级锁

* * *

当多个线程同时申请共享资源锁的访问时，这就产生了竞争

  * JVM会先尝试使用轻量级锁，以CAS方式来获取锁（一般就是自旋加锁，不阻塞线程采用循环等待的方式），成功则获取到锁，状态为轻量级锁
  * 失败（达到一定的自旋次数还未成功）则锁升级到重量级锁



* * *

### 重量级锁

* * *

  * 如果共享资源锁已经被某个线程持有，此时是偏向锁状态，未释放锁前，再有其他线程来竞争时，则会升级到重量级锁
  * 另外轻量级锁状态多线程竞争锁时，也会升级到重量级锁，重量级锁由操作系统来实现，所以性能消耗相对较高



这4种级别的锁，在获取时性能消耗：重量级锁 > 轻量级锁 > 偏向锁 > 无锁

* * *

### 锁优化

* * *

前面我们看到了synchronized在字节码层面是对应 `monitorenter` 和 `monitorexit`，而真正实现互斥的锁其实依赖操作系统底层的`Mutex Lock`来实现。

首先要明确一点，这个锁是一个重量级的锁，由操作系统直接管理，要想使用它，需要将当前线程挂起并从用户态切换到内核态来执行，这种切换的代价是非常昂贵的。

![](https://cdn.jsdelivr.net/gh/Doge2077/liyyro-photo@main/images/2024/10/image-20220315193108505.png)

确实 JDK 1.6之前每次获取的都是重量级锁，无疑在很多场景下性能不高，故JDK1.6对 synchronized 做了很大程度的优化，其目的就是为了减少这种重量级锁的使用。

整体锁升级的过程大致可以分为两条路径，如下：

![](https://cdn.jsdelivr.net/gh/Doge2077/liyyro-photo@main/images/2024/10/image-20220315193128071.png)

上述过程就是锁膨胀，会因实际情况进行膨胀升级，其膨胀方向是：无锁 -> 偏向锁 -> 轻量级锁 -> 重量级锁，并且膨胀方向不可逆。

这里推荐阅读[浅析synchronized锁升级的原理与实现](&lt;https://www.cnblogs.com/star95/p/17542850.html&gt;)。

* * *
