---
title: "深入理解 JVM 之——垃圾回收与内存分配策略"
date: 2023-09-05
categories: [Java, jvm]
description: ""
---

# 垃圾回收策略

---

> 说起垃圾收集（Garbage Collection，下文简称GC），有不少人把这项技术当作Java语言的伴生产物。事实上，垃圾收集的历史远远比Java久远，在1960年诞生于麻省理工学院的Lisp是第一门开始使用内存动态分配和垃圾收集技术的语言。

---

## 回收三问

---

### 哪些区域的内存需要回收？

---

  * `Java` 内存运行时区域的各个部分，特别是程序计数器、虚拟机栈和本地方法栈这三个区域随线程而生、随线程而灭，而栈帧则在方法的进入和退出过程中执行出栈和入栈操作。这些区域的内存分配和回收是确定性的，因为在类结构确定时就已知每个栈帧分配的内存大小。
  * 而对于 `Java` 堆和方法区则具有不确定性，因为接口的不同实现类和方法的不同条件分支可能需要不同的内存。只有在运行时才能确定程序会创建哪些对象以及创建多少个对象，因此这部分内存的分配和回收是动态的。**垃圾收集器的主要任务是管理这部分内存的分配和回收。**
  * 通过垃圾回收，可以避免内存泄漏且大幅优化内存使用以减轻开发人员的负担，避免了手动管理内存的复杂性和错误。



---

### 什么时候回收？

---

内存回收的时机是由垃圾回收器（Garbage Collector）来决定的，而垃圾回收器的具体策略和时机会根据不同的实现而有所差异。一般情况下，以下几种情况会触发内存回收：

  1. 对象不再被引用：当一个对象不再被任何活动的引用所引用时，它就成为垃圾对象。垃圾回收器会周期性地扫描内存，找出这些不再被引用的对象，并将它们标记为可回收的。这是最常见的回收时机。

  2. 内存不足：当系统中的可用内存接近极限时，垃圾回收器会被触发来回收一些不再使用的对象，以释放内存空间。这种情况下的回收被称为压力驱动的回收。

  3. 程序显式调用：在某些情况下，程序可以显式地调用垃圾回收器来进行内存回收。例如，在程序中使用 `System.gc()` 方法可以建议垃圾回收器执行回收操作，但并不能保证立即执行回收。

  4. 程序空闲时：当程序处于空闲状态时，即没有活动的线程在运行，垃圾回收器可以利用这段时间来回收内存。例如，在 `Java` 中，当所有线程都处于等待状态或者没有活动时，垃圾回收器可能会被触发。




---

### 如何回收？

---

垃圾回收（Garbage Collection）是 `JVM` 自动管理内存的过程，它负责释放不再使用的对象所占用的内存空间，以便其他对象可以使用。垃圾回收器通过以下步骤来执行垃圾回收：

  1. 标记（Marking）：垃圾回收器首先标记出所有仍然被活动对象引用的对象。
  2. 垃圾扫描（Garbage Scanning）：垃圾回收器扫描堆内存，找到未被标记的对象，并将其标记为垃圾。
  3. 垃圾回收（Garbage Collection）：垃圾回收器回收被标记为垃圾的对象所占用的内存空间，并将其释放。
  4. 内存整理（Memory Compaction）：垃圾回收器对内存空间进行整理，将存活的对象向一端移动，以便为新对象分配连续的内存空间。



---

## 确认存活

---

### 引用计数法

---

引用计数法是一种简单的垃圾回收算法：

  * 在每个对象上维护一个引用计数器，**记录着该对象的被引用数量** 。
  * 当对象被引用时，引用计数器加 $1$；当引用失效时，引用计数器减 $1$。
  * 当引用计数器为 $0$ 时，表示该对象不再被引用，即对象已经死亡。



垃圾回收器会**定期扫描内存中的对象** ，将引用计数为 $0$ 的对象回收释放内存。

引用计数法**无法解决循环引用的问题** ，即若存在两个或多个对象之间形成循环引用，它们的引用计数器永远不会为 $0$，导致这些对象无法被回收，造成内存泄漏。

---

### 可达性分析

---

可达性分析是一种更为常见和有效的垃圾回收算法：

  * 通过**判断对象是否可达来确定对象是否已经死亡** 。
  * 从一组称为"根"的起始对象开始，通过对象之间的引用关系，逐个遍历对象，并标记可达的对象。
  * 未被标记的对象即为不可达对象，即已经死亡。



**垃圾回收器会将不可达对象进行回收释放内存** 。

可达性分析算法能够解决循环引用的问题，因为只有可达的对象能够被标记，**形成循环引用的对象将无法被标记** ，最终被判定为不可达对象，从而被回收。

现代 `JVM` 一般采用可达性分析算法来进行垃圾回收。

---

### 引用详解（重点）

---

无论是通过引用计数算法判断对象的引用数量，还是通过可达性分析算法判断对象是否引用链可达，判定对象是否存活都和“引用”离不开关系。

在 `JDK1.2` 版之前对象只有“被引用”和“未被引用”之分，在其之后进行了扩充，将引用分为了如下四种：

  * 强引用（Strong Reference）：最常见的引用类型，通过强引用指向的对象，即使在内存紧张的情况下也不会被垃圾回收器回收。只有当强引用被显式地解除时，对象才会被回收。
  * 软引用（Soft Reference）：软引用也是一种较强引用弱化的引用类型，比弱引用更强一些。当内存不足时，垃圾回收器会尽量保留软引用对象，只有在内存真正不足时才会回收。软引用通常用于实现内存敏感的高速缓存。在 `JDK1.2` 版之后提供了 `SoftReference` 类来实现软引用。
  * 弱引用（Weak Reference）：弱引用是一种较强引用弱化的引用类型。当对象只被弱引用引用时，垃圾回收器可以在下一次回收时将其回收。弱引用通常用于实现缓存、观察者模式等场景。在 `JDK1.2` 版之后提供了 `WeeakReference` 类来实现弱引用。
  * 虚引用（Phantom Reference）：虚引用是一种最弱的引用类型，几乎没有引用价值。虚引用的主要作用是跟踪对象被垃圾回收的状态，无法通过虚引用来获取对象实例。虚引用通常用于管理直接内存。在 `JDK1.2` 版之后提供了 `PhantomReference` 类来实现虚引用。



我们提供如下示例代码进行验证：
```java


public class TestReference {
    public static void main(String[] args) {
        // 创建一个强引用对象
        Object hardReference = new Object();

        // 创建一个软引用对象
        SoftReference&lt;Object&gt; softReference = new SoftReference&lt;&gt;(new Object());

        // 创建一个弱引用对象
        WeakReference&lt;Object&gt; weakReference = new WeakReference&lt;&gt;(new Object());

        // 创建一个弱引用对象，并将其引用赋给一个强引用变量
        WeakReference&lt;Object&gt; weakUseReference = new WeakReference&lt;&gt;(new Object());
        Object hardUseReference = weakUseReference.get();

//        WeakReference&lt;Object&gt; weakUseReference = new WeakReference&lt;&gt;(hardReference);
//        Object hardUseReference = weakUseReference;

        // 创建一个虚引用对象，并指定引用队列
        ReferenceQueue&lt;Object&gt; referenceQueue = new ReferenceQueue&lt;&gt;();
        PhantomReference&lt;Object&gt; phantomReference = new PhantomReference&lt;&gt;(new Object(), referenceQueue);

        // 执行垃圾回收
        System.gc();

        // 输出各个引用对象的状态
        System.out.println("HardReference Obj = " + hardReference);
        System.out.println("SoftReference Obj = " + softReference.get());
        System.out.println("WeakReference Obj = " + weakReference.get());
        System.out.println("HardUseReference Obj = " + hardUseReference);
        System.out.println("WeakUseReference Obj = " + weakUseReference.get());
        System.out.println("PhantomReference Obj = " + phantomReference.get());
    }
}
```

在上述代码中，我们进行了如下过程试验：

  * 强引用 `hardReference`：创建了一个强引用对象，该对象不会被垃圾回收器回收，除非显式解除引用。
  * 软引用 `softReference`：创建了一个软引用对象，当内存不足时，垃圾回收器会尽量保留该对象，直到内存真正不足时才会回收。
  * 弱引用 `weakReference`：创建了一个弱引用对象，当对象只被弱引用引用时，垃圾回收器可以在下一次回收时将其回收。
  * 弱引用 `weakUseReference`：创建了一个弱引用对象，并将其引用赋给一个强引用变量，此时对象不会被回收。
  * 虚引用 `phantomReference`：创建了一个虚引用对象，并指定了引用队列 `referenceQueue`。虚引用的主要作用是跟踪对象被垃圾回收的状态，无法通过虚引用来获取对象实例。
  * 执行垃圾回收：调用 `System.gc()` 来触发垃圾回收。最后输出所有被引用的对象状态进行验证。



我在弱引用下添加了被注释的代码片段：
```java


WeakReference&lt;Object&gt; weakUseReference = new WeakReference&lt;&gt;(hardReference);
Object hardUseReference = weakUseReference;
```

在这段代码中，`weakUseReference` 弱引用对象是通过将 `hardReference` 强引用对象作为参数传递给构造函数创建的。然后，将 `weakUseReference` 赋值给 `hardUseReference` 强引用变量。

不同于原来的：
```java


WeakReference&lt;Object&gt; weakUseReference = new WeakReference&lt;&gt;(new Object());
Object hardUseReference = weakUseReference.get();
```

`weakUseReference` 弱引用对象通过直接创建一个新的匿名对象传递给构造函数创建的。然后，通过调用 `weakUseReference.get()` 来获取弱引用对象所引用的对象，并将其赋值给 `hardUseReference` 强引用变量。

虽然两者在创建弱引用对象的方式和强引用变量的赋值方式不同，但结果上 `weakUseReference` 都没有被回收，本质上来看这两者都是在创建时都被赋值给了强引用变量 `hardUseReference`。即使只有弱引用引用该对象，只要存在强引用变量引用该弱引用对象，该对象就不会被垃圾回收。

---

### 再抢救一下

---

如果某个对象没有与 `GC Roots` 相连接的引用链，则被认为是不可达的，理论上已经可以将其视为~~辣鸡~~ 进行回收了，但实际上还能抢救一下：

  * 第一次标记：对于不可达的对象，进行第一次标记，并进行筛选，判断是否需要执行 `finalize()` 方法。
  * `finalize()` 方法的执行：如果对象需要执行 `finalize()` 方法，将其放置在 `F-Queue` 队列中，由 `Finalizer` 线程去执行。执行finalize()方法并不保证等待其运行结束。
  * 第二次标记：稍后收集器会对 `F-Queue` 中的对象进行第二次标记，如果对象在 `finalize()` 方法中成功拯救自己，重新与引用链上的对象建立关联，那么在第二次标记时将被移出"即将回收"的集合。
  * 对象的回收：如果对象无法在 `finalize()` 方法中拯救自己，那么它将被回收。



我们来看如下代码示例：
```java


public class FinalizeEscapeGC {
    public static FinalizeEscapeGC SAVE_HOOK = null;

    public void isAlive() {
        System.out.println("I feel gooooooooooood :)");
    }

    @Override
    protected void finalize() throws Throwable {
        super.finalize();                   // 调用父类的 finalize() 方法
        FinalizeEscapeGC.SAVE_HOOK = this;  // 重新连接
        System.out.println("finalize() method executed!");
    }

    public static void main(String[] args) throws Throwable {

        // 创建对象 link start!
        SAVE_HOOK = new FinalizeEscapeGC();

        for (int i = 0; i < 5; i++) {
            // 断开连接
            SAVE_HOOK = null;
            System.out.println("God ! Please! no ! Please do something! Save me!");
            System.gc();
            // 因为Finalizer方法优先级很低，暂停0.5秒，以等待它
            Thread.sleep(500);
            if (SAVE_HOOK != null) {
                SAVE_HOOK.isAlive();
            } else {
                System.out.println("Wasted :(");
            }
        }
    }
}
```

在上述代码中：

  * 首先创建了一个`FinalizeEscapeGC`对象，并将其引用赋值给`SAVE_HOOK`。
  * 进入循环，循环执行 $5$ 次。
  * 在每次循环开始时，将`SAVE_HOOK`置为`null`，断开对象的引用。
  * 之后调用`System.gc()`方法，请求垃圾回收。
  * 程序暂停 $0.5$ 秒，等待 `finalize()` 方法执行自救。
  * 判断`SAVE_HOOK`是否为`null`，如果不为`null`，说明对象被成功拯救，并调用`isAlive()`方法输出一条信息。
  * 如果`SAVE_HOOK`为`null`，说明对象未被成功拯救，输出一条信息表示对象已经被销毁。



运行后，可以看到与i那些结果如下：
```java


God ! Please! no ! Please do something! Save me!
finalize() method executed!
I feel gooooooooooood :)
God ! Please! no ! Please do something! Save me!
Wasted :(
God ! Please! no ! Please do something! Save me!
Wasted :(
God ! Please! no ! Please do something! Save me!
Wasted :(
God ! Please! no ! Please do something! Save me!
Wasted :(
```

可以看到被强制断开连接的对象只成功逃出了第一次回收，这是因为任何一个对象的 `finalize()` 方法都只会被系统自动调用一次，如果对象面临下一次回收，它的 `finalize()` 方法不会被再次执行，因此后续所有的自救都失败了。

---

## 垃圾回收

---

### 分代收集理论

---

分代收集理论是一种基于经验法则的内存管理策略，它建立在两个分代假说之上

  1. 弱分代假说（Weak Generational Hypothesis）：

```java
 * 弱分代假说认为绝大多数对象都是朝生夕灭的，即它们在创建后很快就变成垃圾对象。
 * 这意味着大部分对象的生命周期相对较短，它们很可能在不久后就不再被程序使用，成为垃圾对象。
 * 基于这个假设，分代收集理论将内存中的对象划分为不同的代，将对象按照生命周期的长短分为新生代和老年代，以便更有效地进行垃圾回收。
```
  2. 强分代假说（Strong Generational Hypothesis）：

```java
 * 强分代假说认为经过多次垃圾收集过程后仍然存活的对象越来越难以消亡。
 * 即对象在经历了多次垃圾收集后，它们的存活概率会逐渐增加。这是因为在多次垃圾收集过程中，存活下来的对象往往是具有较长生命周期的对象，它们可能是程序中的核心数据结构或全局变量等，对程序的执行起着重要作用。
 * 基于这个假设，分代收集理论将老年代作为存放较长生命周期对象的区域，采用更耗时但更全面的垃圾收集算法来处理老年代中的对象。
```



即使这两个假说已经很完善了，但在进行新生代的垃圾收集（Minor GC）时，若新生代中的对象有被老年代所引用，为了准确地确定新生代中的存活对象，必须额外遍历整个老年代中的所有对象，以确保可达性分析结果的正确性。然而，遍历整个老年代的所有对象会给内存回收带来很大的性能负担。因此便追加提出了第三条假说：

  3. 跨代引用假说（Intergenerational Reference Hypothesis）： 
```java
 * 跨代引用相对于同代引用来说仅占极少数。
```



由此我们可以得出推论：**存在互相引用关系的两个对象，是应该倾向于同时生存或者同时消亡的** 。

但无论如何，分代收集理论的核心思想是，**新生代中的对象往往具有较高的垃圾产生率，而老年代中的对象则具有较低的垃圾产生率** 。

因此，针对不同代的对象采用不同的垃圾收集策略，可以提高垃圾收集的效率。

---

### 标记算法

---

基于先前的可达性分析和分代收集理论，有如下三种经典的垃圾回收算法：

  1. 标记-清除算法（Mark and Sweep）： 
```java
 * 基本的垃圾收集算法之一，共分为标记阶段和清除阶段。
 * 标记阶段：从根对象开始，递归地遍历所有可达对象，并将其标记为活动对象。
 * 清除阶段：遍历整个堆内存，将未被标记的对象认定为垃圾对象，并将其回收。
 * 缺点：执行效率不稳定，且多次执行后会产生大量不连续的内存碎片，进而导致当以后在程序运行过程中需要分配较大对象时无法找到足够的连续内存而不得不提前触发另一次垃圾收集动作。
```
  2. 标记-复制算法（Copying）： 
```java
 * 该算法是一种针**对新生代的标记算法** 。
 * 它将新生代的内存空间划分为两个相等的部分，每次只使用其中一部分。
 * 在垃圾收集过程中，将存活的对象从一个部分复制到另一个部分，同时清除非存活对象。这样，每次垃圾收集后，都会有一部分内存是空闲的，**不会产生内存碎片** 。
 * 缺点：该算法仅适用于新生代中垃圾产生率较高的情况，如果新生代内存中多数对象都是存活的，这种算法将会产生大量的内存间复制的开销。
```
  3. 标记-整理算法（Mark and Compact）： 
```java
 * 该算法是一种**针对老年代的标记算法** 。
 * 它和“标记-清除法”一样首先使用标记阶段来标记活动对象。但在清除阶阶段做法不同，而是将存活的对象向一端移动，最后清理掉边界之外的内存。
 * 这样可以保持存活对象的连续性，减少内存碎片的产生。
 * 缺点：该算法仅适用于老年代中垃圾产生率较低的情况，如果老年代大部分的对象都是死亡的，那么移动存活对象并更新所有引用这些对象的地方将会是一种极为负重的操作。
```



> 除了上述三种策略，还有一种“和稀泥式”解决方案可以不在内存分配和访问上增加太大额外负担，做法是让虚拟机平时多数时间都采用标记-清除算法，暂时容忍内存碎片的存在，直到内存空间的碎片化程度已经大到影响对象分配时，再采用标记-整理算法收集一次，以获得规整的内存空间。

---

## 经典垃圾收集器

---

### Serial 收集器

---

在 `JDK1.3.1` 之前，是虚拟机新生代区域收集器的唯一选择。

![image-20230306165527009](https://image.itbaima.net/images/40/image-20230905141290031.png)

特点：

  * 这是一款**单线程** 的垃圾收集器，当开始进行垃圾回收时，需要暂停所有的线程，直到垃圾收集工作结束（~~咋瓦鲁多~~ ）。
  * 对于新生代收集算法采用的是标记复制算法，而老年代采用标记整理算法。



由于在用户的桌面应用场景中，内存一般不大，可以在较短时间内完成垃圾收集，只要不频繁发生，使用串行回收器是可以接受的。

所以，在客户端模式（一般用于一些桌面级图形化界面应用程序）下的新生代中，默认垃圾收集器至今依然是 `Serial` 收集器。

---

### ParNew 收集器

---

![image-20230306165542516](https://image.itbaima.net/images/40/image-20230905144550098.png)

特点：

  * 该垃圾收集器相当于 `Serial` 收集器的多线程版本，它能够支持多线程垃圾收集。



除了多线程支持以外，其他内容基本与 `Serial` 收集器一致，并且目前某些JVM默认的服务端模式新生代收集器就是使用的ParNew收集器。

---

### Parallel Scavenge/Parallel Old收集器

---

![image-20230306165555265](https://image.itbaima.net/images/40/image-20230905141089741.png)

特点：

  * `Parallel Scavenge` 是面向新生代的垃圾收集器，采用标记复制算法实现。
  * `Parallel Old` 是面向老年代的垃圾收集器，采用标记整理算法实现。



与 `ParNew` 收集器不同的是，它会自动衡量一个吞吐量，并根据吞吐量来决定每次垃圾回收的时间，这种自适应机制，能够很好地权衡当前机器的性能，根据性能选择最优方案。

目前 `JDK8` 采用的就是这种 `Parallel Scavenge + Parallel Old` 的垃圾回收方案。

---

### CMS 收集器

---

在 `JDK1.5`，`HotSpot` 推出了一款在强交互应用中几乎可认为有划时代意义的垃圾收集器：CMS（Concurrent-Mark-Sweep）收集器，这款收集器**第一次实现了让垃圾收集线程与用户线程同时工作** 。

![image-20230306165610810](https://image.itbaima.net/images/40/image-20230905142191995.png)

特点：

  * 回收采用标记-清除法执行老年代垃圾回收，分为如下阶段：
  * 初始标记（Initial Mark）：暂停应用程序线程，标记出从根对象直接可达的对象，这个阶段会产生一些停顿。
  * 并发标记（Concurrent Mark）：与应用程序线程并发执行，遍历整个对象图标记出所有可达的对象。
  * 并发预清理（Concurrent PreClean）：与应用程序线程并发执行，处理一些在并发标记阶段发生变化的对象引用关系。
  * 最终标记（Final Remark）：暂停应用程序线程，修正并发标记阶段中发生变化的对象引用关系。
  * 并发清除（Concurrent Sweep）：与应用程序线程并发执行，清除未标记的对象，回收内存空间。



由于采用标记-清除算法会产生大量的内存碎片，长此以往会有更高的概率触发 `Full GC`，并且在与用户线程并发执行的情况下，也会占用一部分的系统资源，导致用户线程的运行速度一定程度上减慢。但这仍是当初低延迟最佳的选择，直到 `G1` 收集器的问世。

---

### Garbage First (G1) 收集器

---

该垃圾收集器也是一款划时代的垃圾收集器，在 `JDK7` 的时候推出，主要面向于服务端的垃圾收集器，并且在 `JDK9` 时，取代了`JDK8`默认的 `Parallel Scavenge + Parallel Old` 的回收方案。

`G1` 收集器使用了一种称为"分代收集"的算法，将堆内存划分为多个大小相等的区域（Region），并根据垃圾回收的需求进行动态调整。

![image-20230306165629129](https://image.itbaima.net/images/40/image-20230905155983614.png)

其回收过程与CMS大体类似：

![image-20230306165641872](https://image.itbaima.net/images/40/image-20230905157561586.png)

`G1` 收集器分为以下几个阶段：

  * 初始标记（Initial Mark）：暂停应用程序线程，标记出从根对象直接可达的对象，这个阶段会产生一些停顿。
  * 并发标记（Concurrent Mark）：与应用程序线程并发执行，遍历整个对象图标记出所有可达的对象。
  * 最终标记（Final Remark）：暂停应用程序线程，修正并发标记阶段中发生变化的对象引用关系。
  * 筛选回收（Cleanup）：与应用程序线程并发执行，对未被引用的对象进行回收。



`G1` 收集器会对每个区域独立进行垃圾回收，从而避免了全堆扫描的开销，减少了停顿时间。相比于 `CMS` 收集器，`G1` 收集器在垃圾回收的停顿时间上有更好的表现，并且可以避免碎片化问题。

---

# 内存分配策略

---

## 常见的内存分配策略

---

`JVM` 的内存分配策略决定了如何为新对象分配内存空间。常见的内存分配策略有两种：

  1. 对象优先在 `Eden` 区分配： 
```java
 * `JVM` 将堆内存划分为不同的区域，其中 `Eden` 区是新对象分配的主要区域。
 * 当程序创建新对象时，`JVM` 将其分配到 `Eden` 区。当 `Eden` 区满时，触发 `Minor GC`（新生代垃圾回收），将仍然存活的对象移动到 `Survivor` 区或老年代。
```
  2. 大对象直接进入老年代： 
```java
 * 如果对象的大小超过了一定的阈值，`JVM` 会将其直接分配到老年代。
 * 这是因为大对象往往具有较长的生命周期，直接分配到老年代可以减少在新生代的复制操作。
```



---

## 其他内存分配策略

---

  1. 长期存活的对象将进入老年代： 
```java
 * `JVM` 给每个对象定义了一个对象年龄（Age）计数器，存储在对象头中。
 * 在 `Eden` 区诞生的对象经历一次 `Minor GC` 后存活会被移动到 `Survivor` 区且年龄计数器加一；
 * 后续在 `Survivor` 区每经历一次 `Minor GC` 且存活继续计数，当年龄计数器达到阈值（默认为15）则会将其移动到老年代。
 * 在虚拟机中可以通过参数 `-XX:MaxTenuringThreshold` 来设置对象晋升到老年代的年龄阈值。
```
  2. 动态对象年龄判定： 
```java
 * 为了能更好地适应不同程序的内存状况，`HotSpot` 虚拟机并不是永远要求对象的年龄必须达到 `-XX：MaxTenuringThreshold`才能晋升老年代。
 * 如果在 `Survivor` 空间中相同年龄所有对象大小的总和大于 `Survivor` 空间的一半，年龄大于或等于该年龄的对象就可以直接进入老年代，无须等到 `-XX：MaxTenuringThreshold` 中要求的年龄。
```



这种动态对象年龄判定的策略可以有效减少垃圾回收的频率，提高垃圾回收的效率，同时也能够更好地适应不同对象的生命周期。通过将长期存活的对象分配到老年代，并根据对象的年龄进行晋升判定，可以更好地管理内存，并减少垃圾回收对系统性能的影响。

---

## 空间分配担保机制

---

在 `Java` 虚拟机中，进行 `Minor GC`（新生代垃圾回收）之前，需要检查老年代的可用空间是否足够容纳新生代所有对象。如果足够，那么进行 `Minor GC` 是安全的。如果不足够，虚拟机会根据参数设置来决定如何处理。

如果允许担保失败（Handle Promotion Failure），虚拟机会进一步检查老年代的可用空间是否大于历次晋升到老年代对象的平均大小。如果大于平均大小，虚拟机会尝试进行一次有风险的 `Minor GC`。这是因为如果大量对象在 `Minor GC` 后仍然存活，需要老年代进行分配担保，将无法容纳在 `Survivor` 空间中的对象直接送入老年代。这种担保需要老年代有足够的剩余空间来容纳这些对象。

为了确定是否进行 `Full GC` 来释放更多空间，虚拟机会将之前每次回收晋升到老年代对象容量的平均大小与老年代的剩余空间进行比较。这样做是为了估计有多少对象会在这次回收中存活下来。如果存活对象的数量远远高于历史平均值，就有可能导致担保失败。

当发生担保失败时，虚拟机需要重新发起一次 `Full GC`，停顿时间会很长。为了避免频繁进行 `Full GC`，通常会打开 `HandlePromotionFailure` 开关，以便进行有风险的 `Minor GC`，而不是立即进行 `Full GC`。

---
