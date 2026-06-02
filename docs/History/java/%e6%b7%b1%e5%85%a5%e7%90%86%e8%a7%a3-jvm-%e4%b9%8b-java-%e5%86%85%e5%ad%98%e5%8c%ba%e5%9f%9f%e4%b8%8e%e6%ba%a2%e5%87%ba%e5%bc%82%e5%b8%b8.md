---
title: "深入理解 JVM 之——Java 内存区域与溢出异常"
date: 2023-09-01
categories: [Java, jvm]
description: ""
---

本篇为深入理解 `Java` 虚拟机第二章内容，推荐在学习前先掌握基础的 `Linux` 操作、编译原理、计算机组成原理等计算机基础以及扎实的 `C/C++` 功底。

该系列的 `GitHub` 仓库：&lt;https://github.com/Doge2077/learn-jvm&gt;

* * *

## 运行时数据区域

* * *

`Java` 虚拟机在执行 `Java` 程序的过程中会把它所管理的内存划分为以下数据区域。

![image-20230831150214981](https://image.itbaima.net/images/40/image-20230831157163998.png)

* * *

### 程序计数器

* * *

程序计数器（Program Counter Register）是一块较小的内存空间，它可以看作是当前线程所执行的字节码的行号指示器。

在 `Java` 中，方法的执行可以分为两种情况：`Java` 方法和本地方法。`Java` 方法是用 `Java` 语言编写的方法，而本地方法是使用其他语言（如 `C` 或 `C++`）编写的方法，通过 Java Native Interface（JNI）在 `Java` 程序中调用。

由于 `Java` 虚拟机的多线程是通过线程轮流切换、分配处理器执行时间的方式来实现，因此：

  * 每条线程都有一个独立的程序计数器，各条线程之间计数器互不影响，独立存储。
  * 如果线程正在执行的是一个 `Java` 方法，这个计数器记录的是正在执行的虚拟机字节码指令的地址；如果正在执行的是本地（Native）方法，这个计数器值则应为空（Undefined）。



值得注意的是，在 《Java 虚拟机规范中》，计数器所在的内存区域是唯一一个没有规定任何 `OutOfMemoryError` 情况的区域。这意味着计数器不会因为内存不足而导致 `OutOfMemoryError` 异常。

* * *

### Java 虚拟机栈

* * *

`Java` 虚拟机中的虚拟机栈（Java Virtual Machine Stack），它是线程私有的，其生命周期与线程相同。

虚拟机栈用于描述 `Java` 方法的执行过程，每个方法在执行时都会创建一个栈帧，用于存储局部变量表、操作数栈、动态连接和方法出口等信息。**栈帧在虚拟机栈中入栈和出栈，对应着方法的调用和执行过程** 。

在 `Java` 虚拟机中，栈内存通常指的是虚拟机栈，大多数情况下指的是虚拟机栈中的局部变量表部分。

局部变量表用于存放编译期可知的各种 `Java` 虚拟机基本数据类型、对象引用和 `returnAddress` 类型。局部变量表的存储空间以局部变量槽（Slot）表示，其中 `long` 和 `double` 类型的数据占用两个变量槽，其他数据类型占用一个变量槽。

> HotSpot 虚拟机的栈容量是不可以动态扩展的，以前的 Classic 虚拟机倒是可以。所以在 HotSpot 虚拟机上是不会由于虚拟机栈无法扩展而导致 OutOfMemoryError 异常——只要线程申请栈空间成功了就不会有 OOM，但是如果申请时就失败，仍然是会出现 OOM 异常的

一般情况下，局部变量表所需的内存空间在编译期间确定，并在方法运行期间不会改变大小（变量槽的数量）。

* * *

### 本地方法栈

* * *

本地方法栈（Native Method Stacks）与虚拟机栈所发挥的作用相似，其区别只是虚拟机栈为虚拟机执行 `Java` 方法（也就是字节 码）服务，而本地方法栈则是为虚拟机使用到的本地（Native）方法服务。

《Java虚拟机规范》对本地方法栈中方法使用的语言、使用方式与数据结构并没有任何强制规定，因此具体的虚拟机可以根据需要自由实 现它。

对于HotSpot虚拟机，它将本地方法栈（Native Method Stack）和虚拟机栈（Java Virtual Machine Stack）合二为一，这意味着它可以在同一个栈中管理 `Java` 方法和本地方法的执行。

* * *

### Java 堆

* * *

`Java` 堆（Java Heap）是虚拟机所管理的内存中最大的一块，**被所有线程共享** 的一块内存区域，在虚拟机启动时创建。

  * 此内存区域的唯一目的就是**存放对象实例** ，所有的对象实例都在这里分配内存。
  * 该内存区域受到垃圾收集器管理，也被称为“GC”堆（Garbage Collected Heap）。
  * `Java` 堆可以处于物理上不连续的内存空间中，但在逻辑上它应该被视为连续的。
  * `Java` 堆既可以被实现成固定大小的，也可以是可扩展的（通过参数 `-Xmx` 和 `-Xms` 设定）。



如果在 `Java` 堆中没有内存完成实例分配，并且堆也无法再扩展时，`Java` 虚拟机将会抛出 `OutOfMemoryError` 异常。

* * *

### 方法区

* * *

方法区（Method Area）与Java堆一样，是**各个线程共享** 的内存区域：

  * 用于存储已被虚拟机加载的类型信息、常量、静态变量、即时编译器编译后的代码缓存等数据。
  * 方法区和 `Java` 堆一样不需要连续的内存和可以选择固定大小或者可扩展外，甚至还可以选择不实现垃圾收集。



> 早期 `HotSpot` 虚拟机设计团队把收集器的分代设计扩展至方法区，因此方法区也被成为“永久代”，但只是使用永久代来实现方法区而已，这种设计导致了 `Java` 应用更容易遇到内存溢出的问题，在JDK 6的时候HotSpot开发团队就有放弃永久代，逐步改为采用本地内存（Native Memory）来实现方法区的计划了，到了JDK 7的HotSpot，已经把原本放在永久代的字符串常量池、静 态变量等移出，而到了`JDK8`，终于完全废弃了永久代的概念，改用与 `JRockit`、`J9` 一样在本地内存中实现的元空间（Meta-space）来代替。

如果方法区无法满足新的内存分配需求时，将抛出 `OutOfMemoryError` 异常。

* * *

### 运行时常量池

* * *

运行时常量池（Runtime Constant Pool）是方法区的一部分：

  * `Class` 文件中包含的常量池表（Constant Pool Table），用于存放编译期生成的各种字面量与符号引用，这部分内容将在类加载后存放到方法区的运行时常量池中。
  * 并非预置入 `Class` 文件中常量池的内容才能进入方法区运行时常量池，运行期间也可以将新的常量放入池，如 `String` 类的 `intern()` 方法。



> 除了`String`类的`intern()`方法之外，还有其他方法可以将常量放入运行时常量池。以下是一些常见的方法：
> 
>   1. `Class.forName(String className)`：在使用反射加载类时，如果指定的类名在运行时常量池中不存在，会将该类名添加到运行时常量池中。
>   2. `String`类的`valueOf(Object obj)`方法：当调用`String.valueOf(Object obj)`方法时，如果运行时常量池中不存在对应的字符串，会将该字符串添加到运行时常量池中。
>   3. `StringBuilder`或`StringBuffer`类的`toString()`方法：当调用`StringBuilder`或`StringBuffer`对象的`toString()`方法时，如果返回的字符串在运行时常量池中不存在，会将该字符串添加到运行时常量池中。
> 


运行时常量池是方法区的一部分，自然受到方法区内存的限制，当常量池无法再申请到内存时会抛出 `OutOfMemoryError` 异常。

* * *

### 直接内存

* * *

直接内存（Direct Memory）并不是虚拟机运行时数据区的一部分，也不是《Java虚拟机规范》中定义的内存区域。

本机直接内存的分配不会受到 `Java` 堆大小的限制，但受到本机总内存（包括物理内存、SWAP分区或者分页文件）大小以及处理器寻址空间的限制。

配置虚拟机参数时，要根据实际内存去设置 `-Xmx` 等参数信息，忽略掉直接内存，会使得各个内存区域总和大于物理内存限制（包括物理的和操作系统级的限制），从而导致动态扩展时出现 `OutOfMemoryError` 异常。

* * *

## HotSpot 虚拟机对象

* * *

### 对象的创建

* * *

当 `Java` 虚拟机遇到一条字节码 `new` 指令时：

  * 首先将去检查这个指令的参数是否能在常量池中定位到一个类的符号引用，并且检查这个符号引用代表的类是否已被加载、解析和初始化过。若没有则执行相应的类加载过程。
  * 在类加载检查通过后，虚拟机为对象进行内存划分： 
    * 指针碰撞（Bump The Pointer）式划分：对于绝对规整的空间，通过指针划分使用和空闲的空间，**划分空间的过程等同于指针向空闲空间方向挪动一段与对象大小相等的距离** 。
    * 空闲列表（Free List）式划分：对于不规整的空间，已使用的内存和空闲内存相互交错，则虚拟机必须维护一个列表用于记录可用的内存区域，**划分空间的过程等同于从列表中找到一块足够大的空间划分给对象实例，并更新列表上的记录** 。
  * 空间分配完成后，还要对对象进行必要的设置： 
    * 将该对象的抽象类元数据信息、哈希码等存放在对象的对象头（Object Header）之中
    * 根据虚拟机当前运行状态的不同，如是否启用偏向锁等，对象头会有不同的设置方式。



在上面工作都完成之后，从虚拟机的视角来看，一个新的对象已经产生了。之后 `Java` 程序再调用其中 `Class` 文件的 `&lt;init&gt;()` 方法对该对象进行初始化。

**注意** ：

  * 如果在执行 `new` 指令时检查到该类已经被加载，虚拟机会获取到该类的运行时常量池中的直接引用，然后继续执行后续操作，如方法调用等。
  * 实际上的内存划分更为复杂，在并发情况下需要考虑到线程安全，通常采用 `CAS` 配上失败重试的方式保证更新操作的原子性，或者把内存分配的动作按照线程划分在不同的空间之中进行。
  * `Java` 编译器会在遇到 `new` 关键字的地方同时生成这两条字节码指令（但如果直接通过其他方式产生的则不一定如此），`new` 指令之后会接着执行 `&lt;init&gt;()` 方法。



* * *

### 对象的内存布局

* * *

在 `HotSpot` 虚拟机里，对象在堆内存中的存储布局可以划分为三个部分：

  * 对象头（Header）：主要存储两类信息，第一类存储对象自身的运行时数据，如哈希码（Hash Code）、GC分代年龄、锁状态标志、线程持有的锁、偏向线程ID、偏向时间戳等；第二类存储类型指针，指向它的类型元数据，用于确定是哪个类的实例。
  * 实例数据（Instance Data）：对象真正存储的有效信息，即程序员定义的各种类型的字段内容，无论是从父类继承下来的，还是在子类中定义的字段都必须记录起来。
  * 对齐填充（Padding）：这部分可有可无，起占位符的作用。



* * *

### 对象的访问定位

* * *

`Java` 程序会通过栈上的 `reference` 数据来操作堆上的具体对象，主流访问方式有以下两种：

  * 句柄访问：`Java` 堆中将可能会划分出一块内存来作为句柄池，`reference` 中存储的就是对象的句柄地址，而句柄中包含了对象实例数据与类型数据各自具体的地址信息。
  * 直接指针访问：`Java` 堆中对象的内存布局就必须考虑如何放置访问类型数据的相关信息，reference中存储的直接就是对象地址，如果只是访问对象本身的话，就不需要多一次间接访问的开销。



句柄访问在对象被移动（垃圾收集时移动对象是非常普遍的行为）时只会改变句柄中的实例数据指针，而 `reference` 本身不需要被修改。而指针访问最大的好处就是速度更快，节省了一次指针定位的时间开销。

* * *

## 实战 ：OOM 异常

* * *

### Java 堆异常

* * *
    
    
    public class HeapOOM {
        static class OOMObject {
            Long num[] = new Long[10000000];
        }
        public static void main(String[] args) {
            List&lt;OOMObject&gt; list = new ArrayList&lt;OOMObject&gt;();
            while (true) {
                list.add(new OOMObject());
                System.out.println(list.size());
            }
        }
    }

`Java` 堆用于储存对象实例，我们只要不断地创建对象并保证不被回收，最终数量一定会超出内存限制。

运行后报错：
    
    
    Exception in thread "main" java.lang.OutOfMemoryError: Java heap space

`java.lang.OutOfMemoryError: Java heap space` 表明了该异常是 `Java` 堆空间异常。

* * *

### 虚拟机栈和本地方法栈溢出

* * *

由于 `HotSpot` 虚拟机中并不区分虚拟机栈和本地方法栈，因此对于 `HotSpot` 来说，`-Xoss` 参数（设置本地方法栈大小）虽然存在，但实际上是没有任何效果的，栈容量只能由 `-Xss` 参数来设定。

关于虚拟机栈和本地方法栈，在《Java虚拟机规范》中描述了两种异常：

  * 如果线程请求的栈深度大于虚拟机栈所允许的最大深度，将递归地抛出的 `StackOverflowError` 异常。
  * 如果虚拟机的栈内存允许动态扩展，当扩展栈容量无法申请到足够的内存时，将抛出 `OutOfMemoryError` 异常。



对于第一种异常，可以设置 `-Xss` 参数调整栈容量到出现异常的值，也可以使用如下代码：
    
    
    public class JavaVMStackSOF {
        private int stackLength = 1;
        public void stackLeak() {
            stackLength ++;
            stackLeak();
        }
        public static void main(String[] args) throws Throwable {
            JavaVMStackSOF oom = new JavaVMStackSOF();
            try {
                oom.stackLeak();
            } catch (Throwable e) {
                System.out.println("stack length:" + oom.stackLength);
                throw e;
            }
        }
    }

递归调用的方法 `stackLeak()`，当虚拟机栈空间不足以容纳新的栈帧时报错如下：
    
    
    stack length:23360
    Exception in thread "main" java.lang.StackOverflowError

每次递归调用都会在虚拟机栈中申请空间，直到达到最大深度。

对于第二种异常，我们要尽可能地多占局部变量表空间，唯一能做的就是定义大量的变量来实现：
    
    
    public class JavaVMStackSOF {
        private static int stackLength = 0;
    
        public static void test() {
            long unused1, unused2, unused3, unused4, unused5, unused6, unused7, unused8, unused9, unused10,
                    unused11, unused12, unused13, unused14, unused15, unused16, unused17, unused18, unused19, unused20,
                    unused21, unused22, unused23, unused24, unused25, unused26, unused27, unused28, unused29, unused30,
                    unused31, unused32, unused33, unused34, unused35, unused36, unused37, unused38, unused39, unused40,
                    unused41, unused42, unused43, unused44, unused45, unused46, unused47, unused48, unused49, unused50,
                    unused51, unused52, unused53, unused54, unused55, unused56, unused57, unused58, unused59, unused60,
                    unused61, unused62, unused63, unused64, unused65, unused66, unused67, unused68, unused69, unused70,
                    unused71, unused72, unused73, unused74, unused75, unused76, unused77, unused78, unused79, unused80,
                    unused81, unused82, unused83, unused84, unused85, unused86, unused87, unused88, unused89, unused90,
                    unused91, unused92, unused93, unused94, unused95, unused96, unused97, unused98, unused99, unused100,
                    unused101, unused102, unused103, unused104, unused105, unused106, unused107, unused108, unused109, unused110,
                    unused111, unused112, unused113, unused114, unused115, unused116, unused117, unused118, unused119, unused120,
                    unused121, unused122, unused123, unused124, unused125, unused126, unused127, unused128, unused129, unused130,
                    unused131, unused132, unused133, unused134, unused135, unused136, unused137, unused138, unused139, unused140,
                    unused141, unused142, unused143, unused144, unused145, unused146, unused147, unused148, unused149, unused150,
                    unused151, unused152, unused153, unused154, unused155, unused156, unused157, unused158, unused159, unused160,
                    unused161, unused162, unused163, unused164, unused165, unused166, unused167, unused168, unused169, unused170,
                    unused171, unused172, unused173, unused174, unused175, unused176, unused177, unused178, unused179, unused180,
                    unused181, unused182, unused183, unused184, unused185, unused186, unused187, unused188, unused189, unused190,
                    unused191, unused192, unused193, unused194, unused195, unused196, unused197, unused198, unused199, unused200;
    
            unused1 = unused2 = unused3 = unused4 = unused5 = unused6 = unused7 = unused8 = unused9 = unused10 =
                    unused11 = unused12 = unused13 = unused14 = unused15 = unused16 = unused17 = unused18 = unused19 = unused20
                            = unused21 = unused22 = unused23 = unused24 = unused25 = unused26 = unused27 = unused28 = unused29 = unused30
                            = unused31 = unused32 = unused33 = unused34 = unused35 = unused36 = unused37 = unused38 = unused39 = unused40
                            = unused41 = unused42 = unused43 = unused44 = unused45 = unused46 = unused47 = unused48 = unused49 = unused50
                            = unused51 = unused52 = unused53 = unused54 = unused55 = unused56 = unused57 = unused58 = unused59 = unused60
                            = unused61 = unused62 = unused63 = unused64 = unused65 = unused66 = unused67 = unused68 = unused69 = unused70
                            = unused71 = unused72 = unused73 = unused74 = unused75 = unused76 = unused77 = unused78 = unused79 = unused80
                            = unused81 = unused82 = unused83 = unused84 = unused85 = unused86 = unused87 = unused88 = unused89 = unused90
                            = unused91 = unused92 = unused93 = unused94 = unused95 = unused96 = unused97 = unused98 = unused99 = unused100
                            = unused101 = unused102 = unused103 = unused104 = unused105 = unused106 = unused107 = unused108 = unused109 = unused110
                            = unused111 = unused112 = unused113 = unused114 = unused115 = unused116 = unused117 = unused118 = unused119 = unused120
                            = unused121 = unused122 = unused123 = unused124 = unused125 = unused126 = unused127 = unused128 = unused129 = unused130
                            = unused131 = unused132 = unused133 = unused134 = unused135 = unused136 = unused137 = unused138 = unused139 = unused140
                            = unused141 = unused142 = unused143 = unused144 = unused145 = unused146 = unused147 = unused148 = unused149 = unused150
                            = unused151 = unused152 = unused153 = unused154 = unused155 = unused156 = unused157 = unused158 = unused159 = unused160
                            = unused161 = unused162 = unused163 = unused164 = unused165 = unused166 = unused167 = unused168 = unused169 = unused170
                            = unused171 = unused172 = unused173 = unused174 = unused175 = unused176 = unused177 = unused178 = unused179 = unused180
                            = unused181 = unused182 = unused183 = unused184 = unused185 = unused186 = unused187 = unused188 = unused189 = unused190
                            = unused191 = unused192 = unused193 = unused194 = unused195 = unused196 = unused197 = unused198 = unused199 = unused200
                            = 1145141919810L;
            stackLength++;
            test();
        }
    
        public static void main(String[] args) {
            try {
                test();
            } catch (Error e) {
                System.out.println("stack length:" + stackLength);
                throw e;
            }
        }
    }
    

运行结果如下：
    
    
    stack length:306
    Exception in thread "main" java.lang.StackOverflowError

可以看到结果并不是我们想要的 `OutOfMemoryError` 异常。

这是因为 `HotSpot` 虚拟机的栈是不可动态扩展的，所以在 `HotSpot` 虚拟机上不会由于虚拟机栈无法扩展而导致 `OutOfMemoryError` 异常，这点我们在最初章节已经提到过了。

* * *

### 方法区和运行时常量池溢出

* * *

运行时常量池是方法区的一部分，所以这两个区域的溢出测试可以放到一起进行。

前面曾经提到 `HotSpot` 从 `JDK7`开始逐步“去永久代”的计划，并在 `JDK8` 中完全使用元空间来代替永久代，我们可以使用如下代码来进行测试：
    
    
    public class RuntimeConstantPoolOOM {
        public static void main(String[] args) {
            Set&lt;String&gt; set = new HashSet&lt;String&gt;();
            int i = 0;
            while (true) {
                set.add(String.valueOf(i ++).intern());
            }
        }
    }

执行 `javac RuntimeConstantPoolOOM.java` 进行编译，再通过 `-XX:PermSize` 和 ` -XX:MaxPermSize` 参数设置永久代大小，接着执行：
    
    
    java -XX:PermSize=6M -XX:MaxPermSize=6M RuntimeConstantPoolOOM

虚拟机报错如下：
    
    
    Java HotSpot(TM) 64-Bit Server VM warning: ignoring option PermSize=6M; support was removed in 8.0
    Java HotSpot(TM) 64-Bit Server VM warning: ignoring option MaxPermSize=6M; support was removed in 8.0

提示我们在 `JDK8` 已经将该参数移除了，如果使用 `JDK7` 及之前的版本运行，应该会出现如下结果：
    
    
    Exception in thread "main" java.lang.OutOfMemoryError: PermGen space

而我们使用的高版本则需限制 `-Xmx` 参数来调整（自 `JDK7` 起，原本存放在永久代的字符串常量池被移至Java堆）：
    
    
    java -Xmx6m RuntimeConstantPoolOOM

运行后出现如下结果：
    
    
    Exception in thread "main" java.lang.OutOfMemoryError: Java heap space

* * *

### 本机直接内存溢出

* * *

直接内存（Direct Memory）的容量大小可通过 `-XX:MaxDirectMemorySize` 参数来指定，如果不去指定，则默认与 `Java` 堆最大值（由 `-Xmx` 指定）一致。

我们使用如下代码进行测试：
    
    
    public class DirectMemoryOOM {
        private static final int _1MB = 1024 * 1024;
        public static void main(String[] args) throws Exception {
            Field unsafeField = Unsafe.class.getDeclaredFields()[0];
            unsafeField.setAccessible(true);
            Unsafe unsafe = (Unsafe) unsafeField.get(null);
            while (true) {
                unsafe.allocateMemory(_1MB);
            }
        }
    }

在编译后，我们设置执行参数如下：
    
    
    java -Xmx20M -XX:MaxDirectMemorySize=10M DirectMemoryOOM

运行后结果如下：
    
    
    Exception in thread "main" java.lang.OutOfMemoryError  

这是由于在上述代码的每次循环中，`unsafe.allocateMemory(_1MB)` 会调用 `Unsafe` 类的 `allocateMemory` 方法来分配 `1MB` 的直接内存空间，最终导致直接内存溢出。

* * *
