---
title: "JDK源码系列（一）"
date: 2024-10-26
categories: [Software Architect]
description: ""
---

## Object 类结构

---

### 概述

---

已知所有类的基类——`java.lang.Object`

* `Object` 类是所有类的基类，当一个类没有直接继承某个类时，默认继承 `Object` 类。
  * `Object` 类属于 `java.lang` 包，此包下的所有类在使用时无需手动导入，系统会在程序编译期间自动导入。

在编译源代码时，如果一个类没有显式标明继承的父类，编译器会为其指定一个默认的父类（即 `Object`）。而在交给虚拟机处理这个类时，由于该类已经有一个默认的父类，因此，JVM 仍然会按照常规的方法，像处理其他类一样来处理这个类。

![](https://cdn.jsdelivr.net/gh/Doge2077/liyyro-photo@main/images/2024/10/image-20220315104729779.png)

以上源码中定义了7个 `native` 方法：`registerNatives()`、`getClass()`、`hashCode()`、`clone()`、`notify()`、`notifyAll()`、`wait(long)`。

**JNI（Java Native Interface）** 的诞生是为了解决以下几种需求：
1. 标准的 Java 类库不支持应用程序所需的平台相关功能。
2. 我们已经用另一种语言编写了一个类库，需要通过 Java 代码来调用。
3. 某些运行次数特别多的方法，为了提升性能，需要用更接近硬件的语言（比如汇编或C/C++）来编写。

这三种需求的核心，其实都是如何用 Java 代码调用非 Java 语言编写的代码。JNI 正是为此而生。

`native` 关键字用于修饰方法。用 `native` 声明的方法表示该方法的实现由外部定义（通常使用C或C++），并通过JNI进行调用。简单地讲，一个 `Native Method` 就是一个 Java 调用非 Java 代码的接口。

---

### 源码解析

---

```java
package java.lang;

public class Object {

    /**
     * 一个本地方法，具体是用C(C++)在DLL中实现的，然后通过JNI调用。
     */
    private static native void registerNatives();

    /**
     * 对象初始化时自动调用此方法。
     */
    static {
        registerNatives();
    }

    /**
     * 返回此Object的运行时类。
     */
    public final native Class&lt;?&gt; getClass();
}
```

/**
     * hashCode的常规协定是：
     * 1.在Java应用程序执行期间，在对同一对象多次调用hashCode()方法时，必须一致地返回相同的整数，前提是将对象进行equals比较时所用的信息没有被修改。
     * 从某一应用程序的一次执行到同一应用程序的另一次执行，该整数无需保持一致。
     * 2.如果根据equals(Object)方法，两个对象是相等的，那么对这两个对象中的每个对象调用hashCode方法都必须生成相同的整数结果。
     * 3.如果根据equals(java.lang.Object)方法，两个对象不相等，那么对这两个对象中的任一对象上调用hashCode()方法不要求一定生成不同的整数结果。
     * 但是，应该意识到，为不相等的对象生成不同整数结果可以提高哈希表的性能。
     */
    public native int hashCode();

/**
     * 这里比较的是对象的内存地址
     */
    public boolean equals(Object obj) {
        return (this == obj);
    }

/**
     * 本地clone方法，用于对象的复制
     */
    protected native Object clone() throws CloneNotSupportedException;

/**
     * 返回该对象的字符串表示，非常重要的方法
     * getClass().getName()：获取字节码文件的对应全路径名，例如java.lang.Object。
     * Integer.toHexString(hashCode())：将哈希值转成16进制数格式的字符串。
     */
    public String toString() {
        return getClass().getName() + "@" + Integer.toHexString(hashCode());
    }

/**
     * 不能被重写，用于唤醒一个因等待该对象（调用了wait方法）而被处于等待状态（waiting 或 timed_waiting）的线程，该方法只能在同步方法或同步块中调用。
     */
    public final native void notify();

/**
     * 不能被重写，用于唤醒所有因等待该对象（调用wait方法）而被处于等待状态（waiting 或 timed_waiting）的线程，该方法只能在同步方法或同步块中调用。
     */
    public final native void notifyAll();

/**
     * 不能被重写，用于在线程调用中，导致当前线程进入等待状态（timed_waiting），timeout单位为毫秒。该方法只能在同步方法或同步块中调用，超过设置时间后线程重新进入可运行状态。
     */
    public final native void wait(long timeout) throws InterruptedException;

```java
public final void wait(long timeout, int nanos) throws InterruptedException {
        if (timeout &lt; 0) {
            throw new IllegalArgumentException("timeout value is negative");
        }

        if (nanos &lt; 0 || nanos &gt; 999999) {
            throw new IllegalArgumentException(
                    "nanosecond timeout value out of range");
        }

        if (nanos > 0) {
            timeout++;
        }

        wait(timeout);
    }

    /**
     * 在其他线程调用此对象的notify()方法或notifyAll()方法前，导致当前线程等待。换句话说，此方法的行为就好像它仅执行wait(0)调用一样。
     * 当前线程必须拥有此对象监视器。
     * 该线程发布对此监视器的所有权并等待，直到其他线程通过调用notify方法或notifyAll方法通知在此对象的监视器上等待的线程醒来，
     * 然后该线程将等到重新获得对监视器的所有权后才能继续执行。
     */
    public final void wait() throws InterruptedException {
        wait(0);
    }

    /**
     * 这个方法用于当对象被回收时调用，这个由JVM支持，Object的finalize方法默认是什么都没有做，如果子类需要在对象被回收时执行一些逻辑处理，则可以重写finalize方法。
     */
    protected void finalize() throws Throwable {
    }
}
```

---

## 类构造器

---

一个类必须要有一个构造器的存在，如果没有显式声明，那么系统会默认创建一个无参构造器。在JDK的Object类源码中，是看不到构造器的，系统会自动添加一个无参构造器。我们可以通过：

```java
// 构造一个Object类的对象。
Object obj = new Object();
```

---

## equals 方法

---

### 源码

---

* Object 类中的 equals 方法：

```java
public boolean equals(Object obj) {
    return (this == obj);
}
```

结论：

* 在 Object 类中，`==` 运算符和 `equals` 方法是等价的，都是比较两个对象的引用是否相等。从另一方面来讲，如果两个对象的引用相等，那么这两个对象一定是相等的。
* 对于我们自定义的一个对象，如果不重写 `equals` 方法，那么在比较对象的时候就是调用 Object 类的 `equals` 方法，也就是用 `==` 运算符比较两个对象。

---

### String 类重写 equals 方法

---

```java
public boolean equals(Object anObject) {
    //如果内存地址相等，那必须相等
    if (this == anObject) {
        return true;
    }

    //如果对象是String类型
    if (anObject instanceof String) {
        String anotherString = (String) anObject;
        // 获取调用方的字符串长度赋值给n
        int n = value.length;
        //判断长度相等
        if (n == anotherString.value.length) {
            char v1[] = value;
            char v2[] = anotherString.value;
            int i = 0;
            //那我们就逐个字符的比较
            while (n-- != 0) {
                //从前往后，任意一个字符不匹配，直接返回false
                if (v1[i] != v2[i])
                    return false;
                i++;
            }
            //全部匹配结束，返回true
            return true;
        }
    }
    return false;
}
```

String 是引用类型，比较时不能比较引用是否相等，重点是字符串的内容是否相等。

所以 String 类定义两个对象相等的标准是**字符串内容都相同**。

在Java规范中，对 equals 方法的使用必须遵循以下几个原则：

* 自反性：对于任何非空引用值 x，x.equals(x) 都应返回 true。
* 对称性：对于任何非空引用值 x 和 y，当且仅当 y.equals(x) 返回 true 时，x.equals(y) 才应返回 true。
* 传递性：对于任何非空引用值 x、y 和 z，如果 x.equals(y) 返回 true，并且 y.equals(z) 返回 true，那么 x.equals(z) 应返回 true。
* 一致性：对于任何非空引用值 x 和 y，多次调用 x.equals(y) 始终返回 true 或始终返回 false，前提是对象上 equals 比较中所用的信息没有被修改。
* 对于任何非空引用值 x，x.equals(null) 都应返回 false。

---

### 重写 equals 原则

---

定义一个 Person 类，然后重写其equals 方法，比较两个 Person 对象：
```java
public class Person {
    private String pname;
    private int page;

    public Person() {}
    public Person(String pname, int page) {
        this.pname = pname;
        this.page = page;
    }

    public int getPage() {
        return page;
    }

    public void setPage(int page) {
        this.page = page;
    }

    public String getPname() {
        return pname;
    }

    public void setPname(String pname) {
        this.pname = pname;
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) { // 引用相等那么两个对象当然相等
            return true;
        }

        /*if (obj == null || !(obj instanceof Person)) { // 对象为空或者不是Person类的实例
            return false;
        }*/

        if (obj == null || (getClass() != obj.getClass())) { // 对象为空或者不是Person类的实例
            return false;
        }

        Person otherPerson = (Person) obj;
        if (otherPerson.getPname().equals(this.getPname()) && otherPerson.getPage() == this.getPage()) {
            return true;
        }
        return false;
    }

    public static void main(String[] args) {
        Person p1 = new Person("Tom", 21);
        Person p2 = new Person("Marry", 20);
        System.out.println(p1 == p2); // false
        System.out.println(p1.equals(p2)); // false

        Person p3 = new Person("Tom", 21);
        System.out.println(p1.equals(p3)); // true
    }
}
```

通过重写 `equals` 方法，我们自定义两个对象相等的标尺为 Person 对象的两个属性都相等，则对象相等，否则不相等。

如果不重写 `equals` 方法，那么始终是调用 Object 类的 `equals` 方法，也就是用 `==` 比较两个对象的引用是否相等。

重写 `equals` 方法总结建议：

```java
@Override
public boolean equals(Object otherObject) {
    // 1、判断比较的两个对象引用是否相等，如果引用相等那么表示是同一个对象，那么当然相等
    if (this == otherObject) {
        return true;
    }
    // 2、如果 otherObject 为 null，直接返回false，表示不相等
    if (otherObject == null) { // 对象为空或者不是Person类的实例
        return false;
    }
    // 3、比较 this 和 otherObject 是否是同一个类（注意下面两个只能使用一种）
    // 3.1：如果 equals 的语义在每个子类中有所改变，就使用 getClass 检测
    if (this.getClass() != otherObject.getClass()) {
        return false;
    }
    // 3.2：如果所有的子类都有统一的定义，那么使用 instanceof 检测
    if (!(otherObject instanceof Person)) {
        return false;
    }

    // 4、将 otherObject 转换成对应的类类型变量
    Person other = (Person) otherObject;

    // 5、最后对对象的属性进行比较。使用 == 比较基本类型，使用 equals 比较对象。如果都相等则返回true，否则返回false
    //    使用 Objects 工具类的 equals 方法防止比较的两个对象有一个为 null 而报错，因为 null.equals() 是会抛异常的
    return Objects.equals(this.pname, other.pname) && this.page == other.page;

    // 6、注意如果是在子类中定义equals，则要包含 super.equals(other)
    // return super.equals(other) && Objects.equals(this.pname, other.pname) && this.page == other.page;
}
```

注意，无论何时重写此方法，通常都必须重写 hashCode 方法，以维护 hashCode 方法的一般约定，该方法声明相等对象必须具有相同的哈希代码。

---

## hashCode 方法

---

### hashCode 作用

---

前面我们说过判断一个元素是否相等可以通过 equals 方法。每增加一个元素，那么我们就通过 equals 方法判断集合中的每一个元素是否重复，但是如果集合中有10000个元素了，但我们新加入一个元素时，那就需要进行10000次 equals 方法的调用，这显然效率很低。

hashCode 是基于哈希算法（散列算法）生成的，是将数据依特定算法产生的结果直接指定到一个地址上。

当集合要添加新的元素时，先调用这个元素的 hashCode 方法，定位到它应该放置的物理位置上：

* 如果这个位置上没有元素，它就可以直接存储在这个位置上，不用再进行任何比较了
  * 如果这个位置上已经有元素了，就调用它的equals方法与新元素进行比较，相同的话就不存了
  * 不相同的话，也就是发生了Hash key相同导致冲突的情况，那么就在这个Hash key的地方产生一个链表，将所有产生相同HashCode的对象放到这个单链表

---

### 对象内存布局

---

当一个对象在堆内存中分配好并且初始化完成之后的结构如下：

![](https://cdn.jsdelivr.net/gh/Doge2077/liyyro-photo@main/images/2024/10/image-20220314135624491.png)

* 添加对齐填充是为了保证对象的总大小是8的整数倍个字节
  * 类型指针占4个字节是因为默认开启了指针压缩，如果不开启指针压缩，则占8个字节

hashCode 的值存储在Java对象头里的，Hotspot虚拟机的对象头主要包括两部分数据：

* Mark Word（标记字段）：用于存储对象自身的运行时数据，它是实现轻量级锁和偏向锁的关键
  * Class Pointer（类型指针）：对象指向它的类元数据的指针，虚拟机通过这个指针来确定这个对象是哪个类的实例

对象头结构如下：

![](https://cdn.jsdelivr.net/gh/Doge2077/liyyro-photo@main/images/2024/10/image-20220228140424617.png)

![](https://cdn.jsdelivr.net/gh/Doge2077/liyyro-photo@main/images/2024/10/image-20220228140345317.png)

---

### 源码解析

---

源码 Object 类中定义如下：
```java
// 是一个用 native 声明的本地方法，作用是返回对象的散列码，是 int 类型的数值。
public native int hashCode();
```

* HashCode的存在主要是为了查找的快捷性
  * HashCode是用来在散列存储结构中确定对象的存储地址

查看：`src\share\native\java\lang\Object.c`
```java
JNIEXPORT void JNICALL//jni调用
//全路径：java_lang_Object_registerNatives是java对应的包下方法
Java_java_lang_Object_registerNatives(JNIEnv *env, jclass cls)
{
     //jni环境调用；下面的参数methods对应的java方法
    (*env)->RegisterNatives(env, cls,
                            methods, sizeof(methods)/sizeof(methods[0]));
}
```

对应方法：
```java
static JNINativeMethod methods[] = {
    // JAVA方法       返回值  参数                             C++函数
    {"hashCode",    "()I",                    (void *)&JVM_IHashCode},
    {"wait",        "(J)V",                   (void *)&JVM_MonitorWait},
    {"notify",      "()V",                    (void *)&JVM_MonitorNotify},
    {"notifyAll",   "()V",                    (void *)&JVM_MonitorNotifyAll},
    {"clone",       "()Ljava/lang/Object;",   (void *)&JVM_Clone},
};
```

调用 [src/share/vm/prims/jvm.cpp](https://cr.openjdk.org/~kevinw/webrev.00/src/share/vm/prims/jvm.cpp.html) JVM_IHashCode 方法：

```cpp
/*
JVM_ENTRY is a preprocessor macro that
adds some boilerplate code that is common for all functions of HotSpot JVM API.
This API is a connection layer between the native code of JDK class library and the JVM.

JVM_ENTRY是一个预加载宏，增加一些样板代码到jvm的所有function中。
这个api是位于本地方法与jdk之间的一个连接层。

所以，此处才是生成hashCode的逻辑！
*/
JVM_ENTRY(jint, JVM_IHashCode(JNIEnv* env, jobject handle))
  JVMWrapper("JVM_IHashCode");
  // 调用了ObjectSynchronizer对象的FastHashCode
  return handle == NULL ? 0 : ObjectSynchronizer::FastHashCode(THREAD, JNIHandles::resolve_non_null(handle));
JVM_END
```

调用 [src/hotspot/share/runtime/synchronizer.cpp](https://cr.openjdk.org/~vlivanov/location_aware_resource_mark/macro/webrev.00/src/hotspot/share/runtime/synchronizer.cpp.html) 内部的 ObjectSynchronizer::FastHashCode：

```cpp
intptr_t ObjectSynchronizer::FastHashCode(Thread *Self, oop obj) {
    // 是否开启了偏向锁（Biased：偏向，倾向）
    if (UseBiasedLocking) {
        // 如果当前对象处于偏向锁状态
        if (obj->mark()->has_bias_pattern()) {
            Handle hobj(Self, obj);
            assert(Universe::verify_in_progress() ||
                   !SafepointSynchronize::is_at_safepoint(),
                   "biases should not be seen by VM thread here");
            // 那么就撤销偏向锁（达到无锁状态，revoke：废除）
            BiasedLocking::revoke_and_rebias(hobj, false, JavaThread::current());
            obj = hobj();
            // 断言下，看看是否撤销成功（撤销后为无锁状态）
            assert(!obj->mark()->has_bias_pattern(), "biases should be revoked by now");
        }
    }

    // ……

    ObjectMonitor* monitor = NULL;
    markOop temp, test;
    intptr_t hash;
    // 读出一个稳定的mark；防止对象obj处于膨胀状态；
    // 如果正在膨胀，就等它膨胀完毕再读出来
    markOop mark = ReadStableMark(obj);
```

//是否撤销了偏向锁（也就是无锁状态）（neutral：中立，不偏不斜的）
    if (mark->is_neutral()) {
        //从mark头上取hash值
        hash = mark->hash();
        //如果有，直接返回这个hashcode（xor）
        if (hash) {                       // if it has hash, just return it
            return hash;
        }
        //如果没有就新生成一个(get_next_hash)
        hash = get_next_hash(Self, obj);  // allocate a new hash code
        //生成后，原子性设置，将hash放在对象头里去，这样下次就可以直接取了
        temp = mark->copy_set_hash(hash); // merge the hash code into header
        // use (machine word version) atomic operation to install the hash
        test = (markOop) Atomic::cmpxchg_ptr(temp, obj->mark_addr(), mark);
        if (test == mark) {
            return hash;
        }
        // If atomic operation failed, we must inflate the header
        // into heavy weight monitor. We could add more code here
        // for fast path, but it does not worth the complexity.
        //如果已经升级成了重量级锁，那么找到它的monitor
        //也就是我们所说的内置锁(objectMonitor)，这是c里的数据类型
        //因为锁升级后，mark里的bit位已经不再存储hashcode，而是指向monitor的地址
        //而升级的markword呢？被移到了c的monitor里
    } else if (mark->has_monitor()) {
        //沿着monitor找header，也就是对象头
        monitor = mark->monitor();
        temp = monitor->header();
        assert(temp->is_neutral(), "invariant");
        //找到header后取hash返回
        hash = temp->hash();
        if (hash) {
            return hash;
        }
        // Skip to the following code to reduce code size
    } else if (Self->is_lock_owned((address)mark->locker())) {
        //轻量级锁的话，也是从java对象头移到了c里，叫helper
        temp = mark->displaced_mark_helper(); // this is a lightweight monitor owned
        assert(temp->is_neutral(), "invariant");
        hash = temp->hash();              // by current thread, check if the displaced
        //找到，返回
        if (hash) {                       // header contains hash code
            return hash;
        }
    }
```

**总结：**

通过分析虚拟机源码，我们证明了 hashCode 不是直接使用的内存地址，而是采取一定的算法来生成。hashCode 值存储在对象头的 Mark Word 里，与锁状态共用一段比特位，这就导致了其值与锁状态相关：

* **无锁状态**：调用 hashCode 方法后，hashCode 存储在该对象的对象头中。
* **偏向锁状态**：一旦调用 hashCode，偏向锁将被撤销，hashCode 被保存并占位 Mark Word，对象被重置为无锁状态。
* **无法撤销偏向锁**：对象将升级为轻量级锁（随后可能升级为重量级锁），hashCode 跟随 Mark Word 被移动到对象的 Object Monitor 中，之后从那里获取。

---

## getClass 方法

`getClass()` 在 Object 类中定义如下，其作用是返回对象的运行时类（`Class` 对象）。
```java
public final native Class&lt;?&gt; getClass();
```
这是一个用 `native` 关键字修饰的方法。

> `native` 用来修饰方法，表示该方法由非 Java 语言（通常为本地代码）实现，JVM 会去调用它。
> 简单地讲，一个 `native` 方法就是一个 Java 调用非 Java 代码的接口。

我们需要知道，用 `native` 修饰的方法由操作系统或底层库实现，其作用是返回一个对象的运行时类。通过这个 `Class` 对象，我们可以获取该运行时类的相关属性和方法。

---

## toString 方法

```java
public String toString() {
    return getClass().getName() + "@" + Integer.toHexString(hashCode());
}
```
* `getClass().getName()` 返回对象的全限定类名（包含包名）。
* `Integer.toHexString(hashCode())` 以十六进制无符号整数形式返回此哈希码的字符串表示。
  * 打印某个对象时，默认会调用其 `toString()` 方法，例如 `System.out.println(person)` 等价于 `System.out.println(person.toString())`。

---

## clone 方法

```java
/**
 * 本地clone方法，用于对象的复制
 */
protected native Object clone() throws CloneNotSupportedException;
```
这是一个受保护（`protected`）的 `native` 方法，用于实现对象的浅拷贝。只有实现了 `Cloneable` 接口的类才可以调用该方法，否则会抛出 `CloneNotSupportedException` 异常。

---

## finalize 方法

```java
protected void finalize() throws Throwable { }
```
当垃圾收集器（GC）确定不再有对该对象的引用时，GC 会调用该对象的 `finalize()` 方法来进行清理回收。

Java 虚拟机（JVM）会确保一个对象的 `finalize()` 方法只被调用一次，并且程序中不能直接调用 `finalize()` 方法。

`finalize()` 方法通常不可预测且存在风险，一般情况下，不建议重写（覆盖）`finalize()` 方法。

---

## registerNatives 方法

```java
private static native void registerNatives();
static {
    registerNatives();
}
```
该方法为静态 `native` 方法，在类加载时通过静态代码块调用，用于注册其他 `native` 方法。其具体实现依赖于 JVM。

```java
private static native void registerNatives();
```

这是一个本地方法。我们要知道，当一个类定义了本地方法后，想要调用操作系统的实现，**必须还要装载对应的本地库**。

```java
static {
    registerNatives();
}
```

静态代码块是类在初始化过程中必定会执行的内容。因此，在类加载时会执行该方法，从而完成本地方法的注册。