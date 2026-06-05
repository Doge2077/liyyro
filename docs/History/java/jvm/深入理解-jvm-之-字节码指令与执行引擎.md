---
title: "深入理解 JVM 之——字节码指令与执行引擎"
date: 2023-09-06
categories: [Java, jvm]
description: ""
---

# 类文件结构

---

## Write Once, Run Anywhere

---

对于 `C` 语言从程序到运行需要经过编译的过程，只有经历了编译后，我们所编写的代码才能够翻译为机器可以直接运行的二进制代码，并且在不同的操作系统下，我们的代码都需要进行一次编译之后才能运行。

而 `Java` 不同于 `C`，由于 `JVM` 内置了解释器和即时编译器，这使得 `.java` 可以不经过编译就直接通过解释的方式直接运行。关于解释器和即时编译器的内容我们将在以后介绍。

我们来看一段简单的代码：
```java
public class Hello {
    public static void main(String[] args) {
        System.out.println("Hello world");
    }
}
```

我们将其保存为 `Hello.java`，然后运行：
```shell
java Hello.java
```

可以看到不出意外地输出了：

![image-20230905163020567](https://image.itbaima.net/images/40/image-20230905167713407.png)

这样我们就通过解释的方式运行了刚刚编写的 `.java` 文件，但为了更好的理解 `Java` 的类文件结构，我们接下来对 `.java` 文件进行编译：
```shell
javac Hello.java
```

可以看到在当前目录下生成了一个 `Hello.class` 文件：

![image-20230905163351158](https://image.itbaima.net/images/40/image-20230905164213676.png)

接下来我们运行：
```shell
java Hello
```

可以看到不出意外的输出了：

![image-20230905163722881](https://image.itbaima.net/images/40/image-20230905163889038.png)

这样我们就以运行编译后的文件方式运行了 `.class` 文件。

如果我们以十六进制打开该文件：

![image-20230905163517473](https://image.itbaima.net/images/40/image-20230905165686984.png)

你会看到上述文件充满了以两个字节为一组的字节码，前两组四个字节被称为“魔数”，说明该文件是否为一个能被虚拟机接受的 `Class` 文件，而 `Java` 的 `Class` 文件的魔数值为 `0xCAFEBABE` ☕👶。

“一次编写，到处运行”——这是 `Java` 在刚刚诞生之时提出的非常著名的宣传口号，而 `Java` 的解决方案便是将像上面这样的源代码编译为平台无关的中间格式——字节码文件（`.class` 文件），并通过对应的 `Java` 虚拟机读取和运行这些中间格式的编译文件，这就使得语言本身实现了跨平台。

---

## 类文件结构概述

---

`Java` 源代码经过编译器编译后会生成类似上面的字节码文件（`.class` 文件），其中字节码文件的结构如下：

1. 魔数（Magic Number）：字节码文件的前四个字节是一个固定的魔数（`0xCAFEBABE`），用于标识该文件为 `Java` 字节码文件。

2. 版本信息（Version）：紧随魔数之后的两个字节表示字节码文件的版本信息，分别是主版本号和次版本号。

3. 常量池（Constant Pool）：紧随版本信息之后是一个常量池表（Constant Pool Table），用于存储编译时生成的各种常量、符号引用和字面量。常量池中的每个项目都有一个索引，通过索引可以在运行时查找和使用。

4. 访问标志（Access Flags）：紧随常量池之后的两个字节表示类或接口的访问标志，用于指示该类或接口的访问级别和特性。

5. 类索引、父类索引和接口索引（Class Indexes）：紧随访问标志之后的两个字节表示类索引，用于指向常量池中该类的全限定名。接着是两个字节的父类索引，用于指向常量池中父类的全限定名。接口索引表紧随父类索引之后，用于指向常量池中实现的接口的全限定名。

6. 字段表（Field Table）：紧随接口索引之后是字段表，用于描述类或接口中定义的字段的访问标志、字段名、字段类型等信息。

7. 方法表（Method Table）：紧随字段表之后是方法表，用于描述类或接口中定义的方法的访问标志、方法名、方法参数、方法返回类型等信息。

8. 属性表（Attribute Table）：紧随方法表之后是属性表，用于存储与类、字段或方法相关的附加信息，如注解、代码行号表、异常表等。

---

# 字节码指令

---

## 生成反编译文件

---

由于字节码实在难以理解（如果你感兴趣全部读懂可以自行深入学习），我们还是看看能理解一点的东西吧。

我们利用 `javap` 命令对 `.class` 文件反编译，将其输出到文本：

```shell
javap -v Hello.class > Hello.txt
```

> `javap` 命令的一些常用选项包括：
> - `-c`：显示字节码指令。
> - `-l`：显示行号和本地变量表。
> - `-s`：显示内部类型签名。
> - `-verbose`：显示所有信息，可简化为 `-v`。

然后打开 `Hello.txt` 查看：

```
Classfile /L:/JAVA/BasicSyntax/Learn_JVM/code/Hello.class
  Last modified 2023年9月5日; size 415 bytes
  SHA-256 checksum 35b1e377d78c81fc0a324af427c3e67c3a468b293c544de8715343f4d97c0c52
  Compiled from "Hello.java"
public class Hello
  minor version: 0
  major version: 61
  flags: (0x0021) ACC_PUBLIC, ACC_SUPER
  this_class: #21                         // Hello
  super_class: #2                         // java/lang/Object
  interfaces: 0, fields: 0, methods: 2, attributes: 1
Constant pool:
   #1 = Methodref          #2.#3          // java/lang/Object."&lt;init&gt;":()V
   #2 = Class              #4             // java/lang/Object
   #3 = NameAndType        #5:#6          // "&lt;init&gt;":()V
   #4 = Utf8               java/lang/Object
   #5 = Utf8               &lt;init&gt;
   #6 = Utf8               ()V
   #7 = Fieldref           #8.#9          // java/lang/System.out:Ljava/io/PrintStream;
   #8 = Class              #10            // java/lang/System
   #9 = NameAndType        #11:#12
  #10 = Utf8               java/lang/System
  #11 = Utf8               out
  #12 = Utf8               Ljava/io/PrintStream;
  #13 = String             #14            // Hello world
  #14 = Utf8               Hello world
  #15 = Methodref          #16.#17        // java/io/PrintStream.println:(Ljava/lang/String;)V
  #16 = Class              #18            // java/io/PrintStream
  #17 = NameAndType        #19:#20        // println:(Ljava/lang/String;)V
  #18 = Utf8               java/io/PrintStream
  #19 = Utf8               println
  #20 = Utf8               (Ljava/lang/String;)V
  #21 = Class              #22            // Hello
  #22 = Utf8               Hello
  #23 = Utf8               Code
  #24 = Utf8               LineNumberTable
  #25 = Utf8               main
  #26 = Utf8               ([Ljava/lang/String;)V
  #27 = Utf8               SourceFile
  #28 = Utf8               Hello.java
{
  public Hello();
    descriptor: ()V
    flags: (0x0001) ACC_PUBLIC
    Code:
      stack=1, locals=1, args_size=1
         0: aload_0
         1: invokespecial #1                  // Method java/lang/Object."&lt;init&gt;":()V
         4: return
      LineNumberTable:
        line 1: 0

  public static void main(java.lang.String[]);
    descriptor: ([Ljava/lang/String;)V
    flags: (0x0009) ACC_PUBLIC, ACC_STATIC
    Code:
      stack=2, locals=1, args_size=1
         0: getstatic     #7                  // Field java/lang/System.out:Ljava/io/PrintStream;
         3: ldc           #13                 // String Hello world
         5: invokevirtual #15                 // Method java/io/PrintStream.println:(Ljava/lang/String;)V
         8: return
      LineNumberTable:
        line 3: 0
        line 4: 8
}
SourceFile: "Hello.java"
```

上述文件内容就是利用 `javap` 反汇编得到的全部信息，这实际上是因为 `Class` 文件采用了一种类似于 `C` 中结构体的伪结构来存储数据。

---

## 常见字节码指令

---

⚠大量定义警告⚠：以下将出现大量指令，用到查表即可，建议简单了解加载和存储指令和基本的运算指令即可，重点放在学习最后的方法调用指令实现重写和重载的细节（重中之重）。

---

### 加载和存储指令

---

加载和存储指令用于将数据在栈帧中的局部变量表和操作数栈之间来回传输：

1.  局部变量加载指令（Load Instructions）：

    *   `iload`: 从局部变量表加载一个 `int` 类型的变量到操作数栈。
    *   `lload`: 从局部变量表加载一个 `long` 类型的变量到操作数栈。
    *   `fload`: 从局部变量表加载一个 `float` 类型的变量到操作数栈。
    *   `dload`: 从局部变量表加载一个 `double` 类型的变量到操作数栈。
    *   `aload`: 从局部变量表加载一个引用类型的变量到操作数栈。

2.  局部变量存储指令（Store Instructions）：

    *   `istore`: 将一个 `int` 类型的数值从操作数栈存储到局部变量表。
    *   `lstore`: 将一个 `long` 类型的数值从操作数栈存储到局部变量表。
    *   `fstore`: 将一个 `float` 类型的数值从操作数栈存储到局部变量表。
    *   `dstore`: 将一个 `double` 类型的数值从操作数栈存储到局部变量表。
    *   `astore`: 将一个引用类型的数值从操作数栈存储到局部变量表。

3.  常量加载指令（Constant Instructions）：

    *   `iconst`: 将 `int` 类型的常量加载到操作数栈。
    *   `lconst`: 将 `long` 类型的常量加载到操作数栈。
    *   `fconst`: 将 `float` 类型的常量加载到操作数栈。
    *   `dconst`: 将 `double` 类型的常量加载到操作数栈。
    *   `aconst_null`: 将 `null` 引用加载到操作数栈。

4.  操作数栈指令（Stack Instructions）：

    *   `bipush`: 将一个字节大小的常量加载到操作数栈。
    *   `sipush`: 将一个短整型大小的常量加载到操作数栈。

---

### 运算相关指令

---

1. 加法指令（Addition Instructions）：

    *   `iadd`: 执行两个 `int` 类型操作数的相加操作。
    *   `ladd`: 执行两个 `long` 类型操作数的相加操作。
    *   `fadd`: 执行两个 `float` 类型操作数的相加操作。
    *   `dadd`: 执行两个 `double` 类型操作数的相加操作。

2. 减法指令（Subtraction Instructions）：

    *   `isub`: 执行两个 `int` 类型操作数的相减操作。
    *   `lsub`: 执行两个 `long` 类型操作数的相减操作。
    *   `fsub`: 执行两个 `float` 类型操作数的相减操作。
    *   `dsub`: 执行两个 `double` 类型操作数的相减操作。

3. 乘法指令（Multiplication Instructions）：

    *   `imul`: 执行两个 `int` 类型操作数的相乘操作。
    *   `lmul`: 执行两个 `long` 类型操作数的相乘操作。
    *   `fmul`: 执行两个 `float` 类型操作数的相乘操作。
    *   `dmul`: 执行两个 `double` 类型操作数的相乘操作。

4. 除法指令（Division Instructions）：

    *   `idiv`: 执行两个 `int` 类型操作数的相除操作。
    *   `ldiv`: 执行两个 `long` 类型操作数的相除操作。
    *   `fdiv`: 执行两个 `float` 类型操作数的相除操作。
    *   `ddiv`: 执行两个 `double` 类型操作数的相除操作。

5. 求余指令（Remainder Instructions）：

    *   `irem`: 执行两个 `int` 类型操作数的求余操作。
    *   `lrem`: 执行两个 `long` 类型操作数的求余操作。
    *   `frem`: 执行两个 `float` 类型操作数的求余操作。
    *   `drem`: 执行两个 `double` 类型操作数的求余操作。

6. 取反指令（Negation Instructions）：

    *   `ineg`: 对一个 `int` 类型操作数进行取反操作。
    *   `lneg`: 对一个 `long` 类型操作数进行取反操作。
    *   `fneg`: 对一个 `float` 类型操作数进行取反操作。
    *   `dneg`: 对一个 `double` 类型操作数进行取反操作。

7. 位移指令（Shift Instructions）：

    *   `ishl`: 对一个 `int` 类型操作数进行左移操作。
    *   `ishr`: 对一个 `int` 类型操作数进行带符号右移操作。
    *   `iushr`: 对一个 `int` 类型操作数进行无符号右移操作。
    *   `lshl`: 对一个 `long` 类型操作数进行左移操作。
    *   `lshr`: 对一个 `long` 类型操作数进行带符号右移操作。
    *   `lushr`: 对一个 `long` 类型操作数进行无符号右移操作。

8. 按位或指令（Bitwise OR Instructions）：

    *   `ior`: 对两个 `int` 类型操作数进行按位或操作。
    *   `lor`: 对两个 `long` 类型操作数进行按位或操作。

9. 按位与指令（Bitwise AND Instructions）：

    *   `iand`: 对两个 `int` 类型操作数进行按位与操作。
    *   `land`: 对两个 `long` 类型操作数进行按位与操作。

10. 按位异或指令（Bitwise XOR Instructions）：

    *   `ixor`: 对两个 `int` 类型操作数进行按位异或操作。
    *   `lxor`: 对两个 `long` 类型操作数进行按位异或操作。

11. 局部变量自增指令（Increment Instructions）：

    *   `iinc`: 对一个 `int` 类型的局部变量进行自增操作。

12. 比较指令（Comparison Instructions）：

    *   `dcmpg`: 比较两个 `double` 类型操作数的大小（带NaN处理）。
    *   `dcmpl`: 比较两个 `double` 类型操作数的大小（带NaN处理）。
    *   `fcmpg`: 比较两个 `float` 类型操作数的大小（带NaN处理）。
    *   `fcmpl`: 比较两个 `float` 类型操作数的大小（带NaN处理）。
    *   `lcmp`: 比较两个 `long` 类型操作数的大小。

---

### 类型转换指令

---

1. 整数类型转换指令（Integer Conversion Instructions）：

    *   `i2l`: 将 `int` 类型转换为 `long` 类型。
    *   `i2f`: 将 `int` 类型转换为 `float` 类型。
    *   `i2d`: 将 `int` 类型转换为 `double` 类型。
    *   `l2i`: 将 `long` 类型转换为 `int` 类型。
    *   `l2f`: 将 `long` 类型转换为 `float` 类型。
    *   `l2d`: 将 `long` 类型转换为 `double` 类型。
    *   `f2i`: 将 `float` 类型转换为 `int` 类型。
    *   `f2l`: 将 `float` 类型转换为 `long` 类型。
    *   `f2d`: 将 `float` 类型转换为 `double` 类型。
    *   `d2i`: 将 `double` 类型转换为 `int` 类型。
    *   `d2l`: 将 `double` 类型转换为 `long` 类型。
    *   `d2f`: 将 `double` 类型转换为 `float` 类型。

2. 类型强制转换指令（Type Casting Instructions）：

    *   `checkcast`: 检查对象是否可以强制转换为指定类型。
    *   `instanceof`: 检查对象是否是指定类型的实例。

3. 数值拓宽和缩窄指令（Numeric Widening and Narrowing Instructions）：

    *   `i2b`: 将 `int` 类型转换为 `byte` 类型。
    *   `i2c`: 将 `int` 类型转换为 `char` 类型。
    *   `i2s`: 将 `int` 类型转换为 `short` 类型。

---

### 对象创建与访问指令

---

1. 对象创建指令（Object Creation Instructions）：

    *   `new`: 创建一个新的对象，并将其引用推送到操作数栈上。
    *   `newarray`: 创建一个指定类型的新数组，并将其引用推送到操作数栈上。
    *   `anewarray`: 创建一个引用类型的新数组，并将其引用推送到操作数栈上。
    *   `multianewarray`: 创建一个多维数组，并将其引用推送到操作数栈上。

2. 对象访问指令（Object Access Instructions）：

    *   `getfield`: 从对象中获取实例字段的值，并将其推送到操作数栈上。
    *   `putfield`: 将一个值存储到对象的实例字段中。
    *   `getstatic`: 获取静态字段的值，并将其推送到操作数栈上。
    *   `putstatic`: 将一个值存储到静态字段中。
    *   `arraylength`: 获取数组的长度，并将其推送到操作数栈上。
    *   `aload`: 从局部变量表加载一个引用类型的变量到操作数栈上。

---

### 操作数栈管理指令

---

1. 出栈指令（Pop Instructions）：

    *   `pop`: 将操作数栈的栈顶元素出栈。
    *   `pop2`: 将操作数栈的栈顶的一个或两个元素出栈。

2. 复制指令（Duplicate Instructions）：

    *   `dup`: 复制操作数栈的栈顶元素，并将复制值重新压入栈顶。
    *   `dup2`: 复制操作数栈的栈顶的一个或两个元素，并将复制值或双份的复制值重新压入栈顶。
    *   `dup_x1`: 复制操作数栈的栈顶元素，并将复制值插入栈顶下面的一个元素之前。
    *   `dup2_x1`: 复制操作数栈的栈顶的一个或两个元素，并将复制值或双份的复制值插入栈顶下面的一个元素之前。
    *   `dup_x2`: 复制操作数栈的栈顶元素，并将复制值插入栈顶下面的两个元素之前。
    *   `dup2_x2`: 复制操作数栈的栈顶的一个或两个元素，并将复制值或双份的复制值插入栈顶下面的两个元素之前。

3. 交换指令（Swap Instruction）：

    *   `swap`: 将操作数栈最顶端的两个数值互换。

---

### 控制转移指令

---

1. 条件分支指令：

    *   `ifeq`: 如果栈顶值等于0，则跳转到指定位置。
    *   `iflt`: 如果栈顶值小于0，则跳转到指定位置。
    *   `ifle`: 如果栈顶值小于等于0，则跳转到指定位置。
    *   `ifne`: 如果栈顶值不等于0，则跳转到指定位置。
    *   `ifgt`: 如果栈顶值大于0，则跳转到指定位置。
    *   `ifge`: 如果栈顶值大于等于0，则跳转到指定位置。
    *   `ifnull`: 如果栈顶值为null，则跳转到指定位置。
    *   `ifnonnull`: 如果栈顶值不为null，则跳转到指定位置。
    *   `if_icmpeq`: 如果栈顶两个int值相等，则跳转到指定位置。
    *   `if_icmpne`: 如果栈顶两个int值不相等，则跳转到指定位置。
    *   `if_icmplt`: 如果栈顶第二个int值小于栈顶第一个int值，则跳转到指定位置。
    *   `if_icmpgt`: 如果栈顶第二个int值大于栈顶第一个int值，则跳转到指定位置。
    *   `if_icmple`: 如果栈顶第二个int值小于等于栈顶第一个int值，则跳转到指定位置。
    *   `if_icmpge`: 如果栈顶第二个int值大于等于栈顶第一个int值，则跳转到指定位置。
    *   `if_acmpeq`: 如果栈顶两个引用值相等，则跳转到指定位置。
    *   `if_acmpne`: 如果栈顶两个引用值不相等，则跳转到指定位置。

2. 复合条件分支指令：

    *   `tableswitch`: 根据一个索引值进行跳转，通过索引值在一张表中查找跳转位置。
    *   `lookupswitch`: 根据一个键值进行跳转，通过键值在一张表中查找跳转位置。

3. 无条件分支指令：

    *   `goto`: 无条件跳转到指定位置。
    *   `goto_w`: 无条件跳转到指定位置（扩展索引）。
    *   `jsr`: 跳转到指定位置，并将返回地址压入栈顶。
    *   `jsr_w`: 跳转到指定位置（扩展索引），并将返回地址压入栈顶。
    *   `ret`: 返回到指定的局部变量索引位置。

---

### 方法返回指令

---

方法返回指令根据返回值的类型区分：

* `ireturn`: 该指令用于返回boolean、byte、char、short和int类型的返回值。它将操作数栈顶的值弹出，并将其作为方法的返回值。然后，将返回值传递给调用该方法的指令。
* `lreturn`: 该指令用于返回long类型的返回值。它将操作数栈顶的两个元素（高位和低位）弹出，并将它们作为方法的返回值。然后，将返回值传递给调用该方法的指令。
* `freturn`: 该指令用于返回float类型的返回值。它将操作数栈顶的值弹出，并将其作为方法的返回值。然后，将返回值传递给调用该方法的指令。
* `dreturn`: 该指令用于返回double类型的返回值。它将操作数栈顶的两个元素（高位和低位）弹出，并将它们作为方法的返回值。然后，将返回值传递给调用该方法的指令。
* `areturn`: 该指令用于返回引用类型（Object类型）的返回值。它将操作数栈顶的引用值弹出，并将其作为方法的返回值。然后，将返回值传递给调用该方法的指令。
* `return`: 该指令用于结束方法的执行，并返回到调用该方法的指令。该指令通常用于声明为void的方法、实例初始化方法、类和接口的类初始化方法。它没有返回值。

# 虚拟机字节码执行引擎

---

## 执行引擎概述

---

我们在 `Java` 内存模型的篇章已经介绍了虚拟机的运行时区域，不熟悉的朋友可以快速回顾一番 [深入理解 JVM 之——Java 内存区域与溢出异常](https://lys2021.com/?p=1553)。

![image-20230831150214981](https://image.itbaima.net/images/40/image-20230831157163998.png)

那么现在我们应该来讲讲执行引擎了——**执行引擎是Java虚拟机核心的组成部分之一**。

执行引擎（Execution Engine）：负责执行加载到内存中的字节码指令，将其转换为机器码并执行。执行引擎通常包括解释器（Interpreter）和即时编译器（Just-In-Time Compiler，JIT）两个部分。

* 解释器：逐行解释执行字节码指令，相对较慢但具有跨平台的优势。
  * 即时编译器：将热点代码编译为本地机器码，以提高执行速度。即时编译器会根据代码的执行情况进行优化，以获得更好的性能。

> 在《Java虚拟机规范》中制定了Java虚拟机字节码执行引擎的概念模型，在不同的虚拟机实现中，执行引擎在执行字节码的时候，通常会有解释执行（通过解释器执行）和编译执行（通过即时编译器产生本地代码执行）两种选择，也可能两者兼备，还可能会有同时包含几个不同级别的即时编译器一起工作的执行引擎。

所有的 `Java` 虚拟机的执行引擎输入、输出都是一致的：**输入的是字节码二进制流，处理过程是字节码解析执行的等价过程，输出的是执行结果**。

---

## 运行时的栈帧结构

---

`Java` 虚拟机的栈帧是支持方法调用和方法执行的数据结构，**它是虚拟机栈的元素之一**。

栈帧存储了方法的局部变量表、操作数栈、动态连接和方法返回地址等信息。

1.  局部变量表（Local Variable Table）：栈帧中的局部变量表用于存储方法中的局部变量和参数。局部变量表是一个数字索引的数组，用于存储各种数据类型的值，包括基本类型和对象引用。
2.  操作数栈（Operand Stack）：栈帧中的操作数栈用于执行方法的操作。它是一个后进先出（LIFO）的栈结构，用于存储方法执行过程中的临时数据和计算结果。字节码指令对操作数栈进行操作。
3.  动态连接（Dynamic Linking）：栈帧中的动态连接用于支持方法调用和方法执行过程中的动态链接。它包含了方法的运行时常量池引用，用于在运行时解析符号引用。
4.  方法返回地址（Return Address）：栈帧中的方法返回地址用于记录方法调用完成后的返回位置。当方法执行完成后，程序将返回到该地址继续执行。

**重点**：

* 栈帧是方法调用和方法执行的基本单位，每个方法在虚拟机栈中都对应一个栈帧。
* 栈帧的大小在编译阶段就确定，并且与程序运行期变量数据无关。
* 在执行过程中，只有位于栈顶的方法对应的栈帧是生效的，被称为当前栈帧，与之关联的方法称为当前方法。
* 执行引擎针对当前栈帧进行操作，执行字节码指令。

---

## 字节码的解释执行

---

`Java` 语言经常被人们定位为“解释执行”的语言，在 `Java` 初生的 `JDK1.0` 时代，这种定义还算是比较准确的，但当主流的虚拟机中都包含了即时编译器后，`Class` 文件中的代码到底会被解释执行还是编译执行，就成了只有虚拟机自己才能准确判断的事。

---

### 基于栈的指令集和基于寄存器的指令集

---

我们在前文提到过用 `javac` 编译器将 `.java` 文件编译成 `.class` 文件，这个过程其实就是 `Javac` 编译器输出字节码指令流的过程，这个过程实际上是一种基于栈的指令集架构（`Instruction Set Architecture, ISA`）完成的，通过这种方式得到的字节码指令流里面的指令大部分都是零地址指令，它们**依赖操作数栈进行工作**。

与“基于栈的指令集架构”相对的是“基于寄存器的指令集”，如我们最熟悉的 `x86` 二地址指令集，这也是当今主流 `PC` 机中物理硬件直接支持的指令集架构，这些指令**依赖寄存器进行工作**。

例如计算：$1 + 1$，两种指令集看起来是下面这样：

基于栈的指令集：
```assembly
iconst_1
iconst_1
iadd
istore_0
```

对于上面的指令：

1.  `iconst_1`：将常量值 $1$ 压入操作数栈顶。
2.  `iconst_1`：将常量值 $1$ 压入操作数栈顶。
3.  `iadd`：从操作数栈中弹出两个整数值，将它们相加，并将结果压入操作数栈顶。
4.  `istore_0`：将栈顶的整数值存储到局部变量表中索引为 $0$ 的位置。

基于寄存器的指令集：
```assembly
mov eax, 1
add eax, 1
```

对于上面的指令：

1.  `mov eax, 1`：将整数值 $1$ 存储到 `eax` 寄存器中。
2.  `add eax, 1`：这是一个将寄存器 `eax` 中的值与常量值 $1$ 相加，并将结果存储回 `eax` 寄存器中的操作。

这两套指令集同时并存和发展，各有优势。

基于栈的指令集：

*   优点：
    *   **可移植性**：由于不直接依赖硬件寄存器，栈指令集更具可移植性，可以在不同的硬件平台上运行。
    *   **代码紧凑**：栈指令集的指令相对较少，使得生成的字节码更紧凑。
    *   **简化编译器实现**：栈指令集不需要考虑寄存器分配等问题，编译器的实现相对简单。
*   缺点：
    *   **执行速度较慢**：栈指令集需要频繁进行栈操作和内存访问，内存访问开销大，相对于基于寄存器的指令集执行速度较慢。

基于寄存器的指令集：

*   优点：
    *   **较高的执行速度**：基于寄存器的指令集在执行速度上通常较快，因为寄存器操作速度快，无需频繁的内存访问。
    *   **更接近物理机的指令集**：主流物理机的指令集都是基于寄存器的，因此基于寄存器的指令集更贴近硬件实现。
*   缺点：
    *   **硬件依赖性**：基于寄存器的指令集直接依赖硬件寄存器，因此在不同的硬件平台上可能存在差异，可移植性较差。
    *   **编译器复杂性**：基于寄存器的指令集需要考虑寄存器分配等复杂问题，编译器的实现相对较复杂。

---

### 基于栈的解释器执行过程

---

接下来我们具体看一个实际的代码示例：
```java
public class Test {
    public static void main(String[] args) {
        int a = 114;
        int b = 514;
        int c = a + b;
    }
}
```

将上述代码保存为 `Test.java` 然后对其进行编译和反编译：

```bash
javac Test.java
javap -v Test.class
```

可以看到输出了如下内容：

```
Classfile /L:/JAVA/BasicSyntax/Learn_JVM/code/Test.class
  Last modified 2023年9月6日; size 276 bytes
  SHA-256 checksum 4064a19d96fe4d72c9d780ef819e1e937b120c31b37482e0b74c70e37c2a5601
  Compiled from "Test.java"
public class Test
  minor version: 0
  major version: 61
  flags: (0x0021) ACC_PUBLIC, ACC_SUPER
  this_class: #7                          // Test
  super_class: #2                         // java/lang/Object
  interfaces: 0, fields: 0, methods: 2, attributes: 1
Constant pool:
   #1 = Methodref          #2.#3          // java/lang/Object."&lt;init&gt;":()V
   #2 = Class              #4             // java/lang/Object
   #3 = NameAndType        #5:#6          // "&lt;init&gt;":()V
   #4 = Utf8               java/lang/Object
   #5 = Utf8               &lt;init&gt;
   #6 = Utf8               ()V
   #7 = Class              #8             // Test
   #8 = Utf8               Test
   #9 = Utf8               Code
  #10 = Utf8               LineNumberTable
  #11 = Utf8               main
  #12 = Utf8               ([Ljava/lang/String;)V
  #13 = Utf8               SourceFile
  #14 = Utf8               Test.java
{
  public Test();
    descriptor: ()V
    flags: (0x0001) ACC_PUBLIC
    Code:
      stack=1, locals=1, args_size=1
         0: aload_0
         1: invokespecial #1                  // Method java/lang/Object."&lt;init&gt;":()V
         4: return
      LineNumberTable:
        line 1: 0

  public static void main(java.lang.String[]);
    descriptor: ([Ljava/lang/String;)V
    flags: (0x0009) ACC_PUBLIC, ACC_STATIC
    Code:
      stack=2, locals=4, args_size=1
         0: bipush        114
         2: istore_1
         3: sipush        514
         6: istore_2
         7: iload_1
         8: iload_2
         9: iadd
        10: istore_3
        11: return
      LineNumberTable:
        line 3: 0
        line 4: 3
        line 5: 7
        line 6: 11
}
SourceFile: "Test.java"
```

我们专注于下列信息：
```
public static void main(java.lang.String[]);
    descriptor: ([Ljava/lang/String;)V
    flags: (0x0009) ACC_PUBLIC, ACC_STATIC
    Code:
      stack=2, locals=4, args_size=1
         0: bipush        114
         2: istore_1
         3: sipush        514
         6: istore_2
         7: iload_1
         8: iload_2
         9: iadd
        10: istore_3
        11: return
```

其中：

*   `public static void main(String[] args)`：表示这是一个公共的静态方法，方法名为 `main`，它接受一个 `String` 类型的数组作为参数。
    *   `descriptor: ([Ljava/lang/String;)V`：说明了方法的描述符，其中 `([Ljava/lang/String;)` 表示参数类型为 `String` 类型的数组，`V` 表示方法的返回类型为 `void`。
    *   `flags: (0x0009) ACC_PUBLIC, ACC_STATIC`：这是方法的标志，其中 `ACC_PUBLIC` 表示该方法是公共的，`ACC_STATIC` 表示该方法是静态的。

我们针对其中的 `main` 入口代码 `Code` 展示解释器的执行过程，其中：
```
stack=2, locals=4, args_size=1
```

提示我们这段代码需要深度为 2 的操作数栈、4 个变量槽的局部变量空间和 1 个方法参数。

根据给定的字节码指令，我们可以模拟执行程序并跟踪操作数栈、局部变量表和程序计数器的动态变化过程。

首先，我们创建一个操作数栈（operand stack）和一个局部变量表（local variable table），并初始化程序计数器（program counter）为0。

```
执行：0: bipush        114
操作数栈状态：[114（栈顶）, null]
局部变量表状态：[this（索引起始）, null, null, null]
程序计数器状态：0

执行：2: istore_1
操作数栈状态：[null（栈顶）, null]
局部变量表状态：[this, 114, null, null]
程序计数器状态：2

执行：3: sipush        514
操作数栈状态：[514（栈顶）, null]
局部变量表状态：[this, 114, null, null]
程序计数器状态：3

执行：6: istore_2
操作数栈状态：[null（栈顶）, null]
局部变量表状态：[this, 114, 514, null]
程序计数器状态：6

执行：7: iload_1
操作数栈状态：[114（栈顶）, null]
局部变量表状态：[this, 114, 514, null]
程序计数器状态：7

执行：8: iload_2
操作数栈状态：[114（栈顶）, 514]
局部变量表状态：[this, 114, 514, null]
程序计数器状态：8

执行：9: iadd
操作数栈状态：[628（栈顶）, null]
局部变量表状态：[this, 114, 514, null]
程序计数器状态：9

执行：10: istore_3
操作数栈状态：[null（栈顶）, null]
局部变量表状态：[this, 114, 514, 628]
程序计数器状态：10

执行：11: return
操作数栈状态：[null（栈顶）, null]
局部变量表状态：[this, 114, 514, 628]
程序计数器状态：11
```

上面的执行过程仅仅是一种概念模型，**虚拟机最终会对执行过程做出一系列优化来提高性能** ，实际的运作过程并不会完全符合概念模型的描述。

更确切地说，实际情况会和上面描述的概念模型差距非常大，差距产生的根本原因是虚拟机中解析器和即时编译器都会对输入的字节码进行优化，即使解释器中也不是按照字节码指令去逐条执行的。

关于编译器优化的细节，我们会在以后的系列文章中提到。

---

# 方法调用指令

针对调用不同类型的方法，字节码指令集里设计了不同的指令：

1. `invokestatic`：用于调用静态方法。可以在类加载时将符号引用解析为直接引用。

2. `invokespecial`：用于调用实例构造器 `&lt;init&gt;()` 方法、私有方法和父类中的方法。也可以在类加载时将符号引用解析为直接引用。

3. `invokevirtual`：用于调用所有的虚方法。根据对象的实际类型进行分派（虚方法分派）。

4. `invokeinterface`：用于调用接口方法，会在运行时确定实现该接口的对象，并选择适合的方法进行调用。

5. `invokedynamic`：先在运行时动态解析出调用点限定符所引用的方法，然后再执行该方法。分派逻辑由用户设定的引导方法决定。

这些调用指令可以根据对象的类型和方法的特性进行不同的分派和调用。

`invokedynamic` 指令是在 JDK 7 时加入到字节码中的，当时确实只为了做动态语言（如 JRuby、Scala）支持，Java 语言本身并不会用到它。而到了 JDK 8 时代，Java 有了 Lambda 表达式和接口的默认方法，它们在底层调用时就会用到 `invokedynamic` 指令。

其中，`invokestatic` 和 `invokespecial` 指令可以调用非虚方法，包括静态方法、私有方法、实例构造器和父类方法。而 `invokevirtual` 和 `invokeinterface` 指令用于调用虚方法，根据对象的实际类型进行分派。

也许这些指令看起来简单但很难理解，这是因为我们在上文多次提到过“方法调用”、“解析”、“分派”这些东西。别急，如果想要真正弄清楚这些指令，我们需要一步步来。

---

## 方法调用概述

---

**方法调用并不等同于方法中的代码被执行**，方法调用阶段唯一的任务就是确定被调用方法的版本（即调用哪一个方法），暂时还未涉及方法内部的具体运行过程。

一切方法调用在 `Class` 文件里面存储的都只是符号引用，而不是方法在实际运行时内存布局中的入口地址（直接引用）。

这个特性给 `Java` 带来了更强大的动态扩展能力，但也使得 `Java` 方法调用过程变得相对复杂，某些调用需要在类加载期间，甚至到运行期间才能确定目标方法的直接引用。

在 `Java` 中，方法调用过程中同时存在解析（Resolution）和分派（Dispatch）两个过程，方法调用过程中首先进行解析，将符号引用转化为直接引用，然后根据实际对象的类型进行分派，确定方法的实际执行版本。

---

## 解析

---

**解析**：

* 在类加载的解析阶段将方法调用的符号引用转化为直接引用的过程。

**解析的前提**：

* 方法在程序编写、编译阶段就有一个可确定的调用版本，并且这个版本在运行期是不可改变的。
  * 必须是静态方法、私有方法和被 `final` 修饰的实例方法，因为它们都不可能通过继承或其他方式重写出其他版本。

**解析调用过程**：

* 解析调用是静态的过程，**在编译期间就完全确定**，不延迟到运行期再完成。
  * 在类加载的解析阶段，涉及的符号引用会被转变为明确的直接引用，存储在常量池中。

这种转化使得方法调用在运行时可以更高效地执行，无需再进行符号解析，直接使用已经解析的直接引用。

---

## 分派（重点）

---

`Java` 作为一门面向对象的编程语言，具备继承、封装和多态这三个基本特征。

而分派调用过程在 `Java` 虚拟机中揭示了多态性的体现，特别是在方法的重载和重写方面：

1.  **重载（Overloading）**：重载是指在同一个类中定义多个方法，它们具有相同的名称但参数列表不同。在虚拟机中实现重载时，会根据方法调用的静态类型（声明类型）选择合适的方法版本。这属于静态分派，根据参数的静态类型来确定方法的版本。

2.  **重写（Overriding）**：重写是指子类重新定义父类中已有的方法，具有相同的名称和参数列表。在虚拟机中实现重写时，会根据方法调用的实际类型（运行时类型）选择合适的方法版本。这属于动态分派，根据实际对象的类型来确定方法的版本。

下面我们就来揭示 `JVM` 实现重载和重写的底层原理，这也是我们真正的重点部分。

---

### 静态分派

---

> "分派"（Dispatch）这个词本身就具有动态性，一般不应用在静态语境之中，这部分原本在英文原版的《Java虚拟机规范》和《Java语言规范》里的说法都是"Method Overload Resolution"，即应该归入上节的"解析"里去讲解，但部分其他外文资料和国内翻译的许多中文资料都将这种行为称为"静态分派"。

为了解释静态分派和重载，我们看如下示例代码：
```java
public class StaticDispatch {
    static abstract class Human {
    }

    static class Man extends Human {
    }

    static class Woman extends Human {
    }

    public void sayHello(Human guy) {
        System.out.println("hello,guy!");
    }

    public void sayHello(Man guy) {
        System.out.println("hello,gentleman!");
    }

    public void sayHello(Woman guy) {
        System.out.println("hello,lady!");
    }

    public static void main(String[] args) {
        Human man = new Man();
        Human woman = new Woman();
        StaticDispatch sr = new StaticDispatch();
        sr.sayHello(man);
        sr.sayHello(woman);
    }
}
```

上面的代码中定义了一个 `StaticDispatch` 类，包含了一个抽象类 `Human` 和两个继承自 `Human` 的子类 `Man` 和 `Woman`。类中定义了三个重载的 `sayHello` 方法，分别接受 `Human`、`Man` 和 `Woman` 类型的参数，并输出相应的问候语。

理论上我们重载了 `sayHello()` 方法，运行结果应该是：
```
hello,gentleman!
hello,lady!
```

但实际上控制台输出了：
```
hello, guy!
hello, guy!
```

你先别急，让我先急 🤡

这里我们仍需要先提出几个概念：

* 静态类型（Static Type）：在编译时已知的变量类型，编译器根据静态类型进行方法的选择和类型检查。
  * 实际类型（Actual Type）：在程序运行时确定的变量类型，由对象的实际创建类型决定。

在上面的代码中，`Human` 是静态类型（也叫外观类型），而 `Man` 和 `Woman` 则是实际类型（也叫运行时类型）。

我们用 `javap` 查看反编译结果：
```
Compiled from "StaticDispatch.java"
public class StaticDispatch {
  public StaticDispatch();
    Code:
       0: aload_0
       1: invokespecial #1                  // Method java/lang/Object."&lt;init&gt;":()V
       4: return

  public void sayHello(StaticDispatch$Human);
    Code:
       0: getstatic     #7                  // Field java/lang/System.out:Ljava/io/PrintStream;
       3: ldc           #13                 // String "hello,guy!"
       5: invokevirtual #15                 // Method java/io/PrintStream.println:(Ljava/lang/String;)V
       8: return

  public void sayHello(StaticDispatch$Man);
    Code:
       0: getstatic     #7                  // Field java/lang/System.out:Ljava/io/PrintStream;
       3: ldc           #21                 // String "hello,gentleman!"
       5: invokevirtual #15                 // Method java/io/PrintStream.println:(Ljava/lang/String;)V
       8: return

  public void sayHello(StaticDispatch$Woman);
    Code:
       0: getstatic     #7                  // Field java/lang/System.out:Ljava/io/PrintStream;
       3: ldc           #23                 // String "hello,lady!"
       5: invokevirtual #15                 // Method java/io/PrintStream.println:(Ljava/lang/String;)V
       8: return

  public static void main(java.lang.String[]);
    Code:
       0: new           #25                 // class StaticDispatch$Man
       3: dup
       4: invokespecial #27                 // Method StaticDispatch$Man."&lt;init&gt;":()V
       7: astore_1
       8: new           #28                 // class StaticDispatch$Woman
      11: dup
      12: invokespecial #30                 // Method StaticDispatch$Woman."&lt;init&gt;":()V
      15: astore_2
      16: new           #31                 // class StaticDispatch
      19: dup
      20: invokespecial #33                 // Method "&lt;init&gt;":()V
      23: astore_3
      24: aload_3
      25: aload_1
      26: invokevirtual #34                 // Method sayHello:(LStaticDispatch$Human;)V
      29: aload_3
      30: aload_2
      31: invokevirtual #34                 // Method sayHello:(LStaticDispatch$Human;)V
      34: return
}
```

可以明显地看到 `main` 方法里面的偏移量 `26` 和 `31` 处是我们的方法调用：
```
26: invokevirtual #34                 // Method sayHello:(LStaticDispatch$Human;)V
......
31: invokevirtual #34                 // Method sayHello:(LStaticDispatch$Human;)V
```

反编译结果已经指明，尽管 `invokevirtual` 在运行时可以根据对象的实际类型进行动态分派，但在静态分派的情况下，编译器在编译期已经确定了要调用的方法，因此不会进行动态分派，而是直接调用编译时选择的方法。

也就是说，**在静态分派的规则下，方法的选择是基于参数的静态类型，而不是其实际运行时的类型**。

这样也就很容易理解了：由于 `man` 和 `woman` 的静态类型都是 `Human`，因此都会调用 `Human` 的 `sayHello()` 方法。

但如果我们对原代码稍作修改：
```java
public static void main(String[] args) {
        Human man = new Man();
        Human woman = new Woman();
        StaticDispatch sr = new StaticDispatch();
        sr.sayHello((Man) man);  
        sr.sayHello((Woman) woman);
}
```

再次编译运行，可以看到结果如下：

```
hello,gentleman!
hello,lady!
```

我们用 `javap` 查看反编译结果：

```
26: checkcast     #25                 // class StaticDispatch$Man
29: invokevirtual #34                 // Method sayHello:(LStaticDispatch$Man;)V
......
34: checkcast     #28                 // class StaticDispatch$Woman
37: invokevirtual #38                 // Method sayHello:(LStaticDispatch$Woman;)V
```

可以看到在调用方法之前，先进行了 `checkcast` 检查，确认了 `man` 和 `woman` 强制转换为了对应的实际类型，这样在 `invokevirtual` 指令进行方法调用时，指向的就是对应实际类型的 `sayHello()` 方法了。通过进行强制类型转换，即使在静态类型已经确定的情况下，我们仍绕过了静态分派的规则，使得方法的选择基于实际类型而不是静态类型。

---

### 动态分派

---

动态分派（Dynamic Dispatch）是一种在运行时根据对象的实际类型来选择调用的方法的机制，它与 `Java` 语言多态性的另外一个重要体现——重写（Override）有着很密切的关联。

我们将上节示例代码稍作修改：

```java
public class DynamicDispatch {
    static abstract class Human {
        protected abstract void sayHello();
    }
    static class Man extends Human {
        @Override
        protected void sayHello() {
            System.out.println("man say hello");
        }
    }
    static class Woman extends Human {
        @Override
        protected void sayHello() {
            System.out.println("woman say hello");
        }
    }
    public static void main(String[] args) {
        Human man = new Man();
        Human woman = new Woman();
        man.sayHello();
        woman.sayHello();
        man = new Woman();
        man.sayHello();
    }
}
```

在上述代码中，`Human` 是一个抽象类，其中声明了一个抽象方法 `sayHello()`，`Man` 和 `Woman` 类都是 `Human` 类的子类，它们分别重写了 `sayHello()` 方法。我们首先创建了 `Man` 和 `Woman` 的实例对象 `man` 和 `woman` 并调用了相应的 `sayHello()` 方法，然后让 `man` 重新赋值为 `Woman` 的实例，并调用其 `sayHello()` 方法。

理论上运行结果应该为：
```
man say hello
woman say hello
woman say hello
```

实际上：
```
man say hello
woman say hello
woman say hello
```

这个运行结果相信不会出乎任何人的意料 🤗

对于习惯了面向对象思维的我们来说，这是一个理所应当的结果，但问题在于 `Java` 虚拟机是如何根据实际类型来分派方法执行版本的呢？

我们继续用 `javap` 大法查看反编译结果：
```
Compiled from "DynamicDispatch.java"
public class DynamicDispatch {
  public DynamicDispatch();
    Code:
       0: aload_0
       1: invokespecial #1                  // Method java/lang/Object."&lt;init&gt;":()V
       4: return

  public static void main(java.lang.String[]);
    Code:
       0: new           #7                  // class DynamicDispatch$Man
       3: dup
       4: invokespecial #9                  // Method DynamicDispatch$Man."&lt;init&gt;":()V
       7: astore_1
       8: new           #10                 // class DynamicDispatch$Woman
      11: dup
      12: invokespecial #12                 // Method DynamicDispatch$Woman."&lt;init&gt;":()V
      15: astore_2
      16: aload_1
      17: invokevirtual #13                 // Method DynamicDispatch$Human.sayHello:()V
      20: aload_2
      21: invokevirtual #13                 // Method DynamicDispatch$Human.sayHello:()V
      24: new           #10                 // class DynamicDispatch$Woman
      27: dup
      28: invokespecial #12                 // Method DynamicDispatch$Woman."&lt;init&gt;":()V
      31: astore_1
      32: aload_1
      33: invokevirtual #13                 // Method DynamicDispatch$Human.sayHello:()V
      36: return
}
```

在 `main` 方法中：
```java
Human man = new Man();
Human woman = new Woman();
```

对应字节码指令为：
```
0: new           #7                  // class DynamicDispatch$Man
 3: dup
 4: invokespecial #9                  // Method DynamicDispatch$Man."&lt;init&gt;":()V
 7: astore_1
 8: new           #10                 // class DynamicDispatch$Woman
11: dup
12: invokespecial #12                 // Method DynamicDispatch$Woman."&lt;init&gt;":()V
15: astore_2
```

而调用方法：
```java
man.sayHello();
woman.sayHello();
```

对应字节码指令为：
```
17: invokevirtual #13                 // Method DynamicDispatch$Human.sayHello:()V
......
21: invokevirtual #13                 // Method DynamicDispatch$Human.sayHello:()V
```

可以看到 `invokevirtual` 指令注释已经显示了这个常量是 `DynamicDispatch` 类下 `Human.sayHello()` 的符号引用，但是这两句指令最终执行的目标方法并不相同。

我们从 `invokevirtual` 指令本身入手，其运行时解析过程大致分为以下几步：

*   找到操作数栈顶的第一个元素所指向的对象的实际类型，记作 $C$。
    *   如果在类型 $C$ 中找到与常量中的描述符和简单名称都相符的方法，则进行访问权限校验，如果通过则返回这个方法的直接引用，查找过程结束；不通过则返回 `java.lang.IllegalAccessError` 异常。
    *   否则，按照继承关系从下往上依次对 $C$ 的各个父类进行第二步的搜索和验证过程。
    *   如果始终没有找到合适的方法，则抛出 `java.lang.AbstractMethodError` 异常。

因此，`invokevirtual` 指令在执行时会先确定接收者的实际类型，所以两次调用中的 `invokevirtual` 指令并不是把常量池中方法的符号引用解析到直接引用上就结束了，还会根据方法接收者的实际类型来选择方法版本。

---

### 单分派与多分派

方法的接收者与方法的参数统称为方法的宗量，根据分派基于多少种宗量，可以将分派划分为单分派和多分派两种：

1.  单分派指的是根据方法调用的接收者的类型来确定使用哪个方法实现。
    *   在单分派中，方法的选择仅仅依赖于接收者的类型，不考虑方法参数的类型。
2.  多分派指的是根据方法调用的接收者和参数的类型来确定使用哪个方法实现。
    *   在多分派中，方法的选择不仅依赖于接收者的类型，还依赖于方法参数的类型。

对于 `Java` 来说：

*   静态分派根据方法调用时的静态类型和参数的静态类型来选择目标方法，属于多分派。
*   动态分派根据方法调用时的实际类型来选择目标方法，属于单分派。

---

### invokedynamic

`JDK 7` 为了更好地支持动态类型语言，引入了第五条方法调用的字节码指令 `invokedynamic`。如果你看过我之前写过的[浅谈 Java 中的 Lambda 表达式](https://lys2021.com/?p=1544)，其中在 `Lambda` 的本质一节我也提到了它，那么接下来我们好好看看到底怎么回事。

我们沿用其中的示例：
```java
public class LambdaTest {

    public static interface Test {
        String showTestNumber(Integer param);
    }

    public static void main(String[] args) {
        Test test = param -> "Test number is " + param;
        System.out.println(test.showTestNumber(114514));
    }
}
```

`javac` 编译后再 `javap` 反编译回去，得到下面的内容：
```
Classfile /L:/JAVA/BasicSyntax/Learn_JVM/code/LambdaTest.class
  Last modified 2023年9月6日; size 1445 bytes
  SHA-256 checksum 3a71d05fe531173bda2fd05e7b9a5a12dc0fd040047f87a59add471744a6a2be
  Compiled from "LambdaTest.java"
public class LambdaTest
  minor version: 0
  major version: 61
  flags: (0x0021) ACC_PUBLIC, ACC_SUPER
  this_class: #38                         // LambdaTest
  super_class: #2                         // java/lang/Object
  interfaces: 0, fields: 0, methods: 3, attributes: 4
Constant pool:
   #1 = Methodref          #2.#3          // java/lang/Object."&lt;init&gt;":()V
   #2 = Class              #4             // java/lang/Object
   #3 = NameAndType        #5:#6          // "&lt;init&gt;":()V
   #4 = Utf8               java/lang/Object
   #5 = Utf8               &lt;init&gt;
   #6 = Utf8               ()V
   #7 = InvokeDynamic      #0:#8          // #0:showTestNumber:()LLambdaTest$Test;
   #8 = NameAndType        #9:#10         // showTestNumber:()LLambdaTest$Test;
   #9 = Utf8               showTestNumber
  #10 = Utf8               ()LLambdaTest$Test;
  #11 = Fieldref           #12.#13        // java/lang/System.out:Ljava/io/PrintStream;
  #12 = Class              #14            // java/lang/System
  #13 = NameAndType        #15:#16        // out:Ljava/io/PrintStream;
  #14 = Utf8               java/lang/System
  #15 = Utf8               out
  #16 = Utf8               Ljava/io/PrintStream;
  #17 = Integer            114514
  #18 = Methodref          #19.#20        // java/lang/Integer.valueOf:(I)Ljava/lang/Integer;
  #19 = Class              #21            // java/lang/Integer
  #20 = NameAndType        #22:#23        // valueOf:(I)Ljava/lang/Integer;
  #21 = Utf8               java/lang/Integer
  #22 = Utf8               valueOf
  #23 = Utf8               (I)Ljava/lang/Integer;
  #24 = InterfaceMethodref #25.#26        // LambdaTest$Test.showTestNumber:(Ljava/lang/Integer;)Ljava/lang/String;
  #25 = Class              #27            // LambdaTest$Test
  #26 = NameAndType        #9:#28         // showTestNumber:(Ljava/lang/Integer;)Ljava/lang/String;
  #27 = Utf8               LambdaTest$Test
  #28 = Utf8               (Ljava/lang/Integer;)Ljava/lang/String;
  #29 = Methodref          #30.#31        // java/io/PrintStream.println:(Ljava/lang/String;)V
  #30 = Class              #32            // java/io/PrintStream
  #31 = NameAndType        #33:#34        // println:(Ljava/lang/String;)V
  #32 = Utf8               java/io/PrintStream
  #33 = Utf8               println
  #34 = Utf8               (Ljava/lang/String;)V
  #35 = InvokeDynamic      #1:#36         // #1:makeConcatWithConstants:(Ljava/lang/Integer;)Ljava/lang/String;
  #36 = NameAndType        #37:#28        // makeConcatWithConstants:(Ljava/lang/Integer;)Ljava/lang/String;
  #37 = Utf8               makeConcatWithConstants
  #38 = Class              #39            // LambdaTest
  #39 = Utf8               LambdaTest
  #40 = Utf8               Code
  #41 = Utf8               LineNumberTable
  #42 = Utf8               main
  #43 = Utf8               ([Ljava/lang/String;)V
  #44 = Utf8               lambda$main$0
  #45 = Utf8               SourceFile
  #46 = Utf8               LambdaTest.java
  #47 = Utf8               NestMembers
  #48 = Utf8               BootstrapMethods
  #49 = MethodHandle       6:#50          // REF_invokeStatic java/lang/invoke/LambdaMetafactory.metafactory:(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodHandle;Ljava/lang/invoke/MethodType;)Ljava/lang/invoke/CallSite;
  #50 = Methodref          #51.#52        // java/lang/invoke/LambdaMetafactory.metafactory:(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodHandle;Ljava/lang/invoke/MethodType;)Ljava/lang/invoke/CallSite;
  #51 = Class              #53            // java/lang/invoke/LambdaMetafactory
  #52 = NameAndType        #54:#55        // metafactory:(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodHandle;Ljava/lang/invoke/MethodType;)Ljava/lang/invoke/CallSite;
  #53 = Utf8               java/lang/invoke/LambdaMetafactory
  #54 = Utf8               metafactory
  #55 = Utf8               (Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodHandle;Ljava/lang/invoke/MethodType;)Ljava/lang/invoke/CallSite;
  #56 = MethodType         #28            //  (Ljava/lang/Integer;)Ljava/lang/String;
  #57 = MethodHandle       6:#58          // REF_invokeStatic LambdaTest.lambda$main$0:(Ljava/lang/Integer;)Ljava/lang/String;
  #58 = Methodref          #38.#59        // LambdaTest.lambda$main$0:(Ljava/lang/Integer;)Ljava/lang/String;
  #59 = NameAndType        #44:#28        // lambda$main$0:(Ljava/lang/Integer;)Ljava/lang/String;
  #60 = MethodHandle       6:#61          // REF_invokeStatic java/lang/invoke/StringConcatFactory.makeConcatWithConstants:(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/invoke/CallSite;
  #61 = Methodref          #62.#63        // java/lang/invoke/StringConcatFactory.makeConcatWithConstants:(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/invoke/CallSite;
  #62 = Class              #64            // java/lang/invoke/StringConcatFactory
  #63 = NameAndType        #37:#65        // makeConcatWithConstants:(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/invoke/CallSite;
  #64 = Utf8               java/lang/invoke/StringConcatFactory
  #65 = Utf8               (Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/invoke/CallSite;
  #66 = String             #67            // Test number is \u0001
  #67 = Utf8               Test number is \u0001
  #68 = Utf8               InnerClasses
  #69 = Utf8               Test
  #70 = Class              #71            // java/lang/invoke/MethodHandles$Lookup
  #71 = Utf8               java/lang/invoke/MethodHandles$Lookup
  #72 = Class              #73            // java/lang/invoke/MethodHandles
  #73 = Utf8               java/lang/invoke/MethodHandles
  #74 = Utf8               Lookup
{
  public LambdaTest();
    descriptor: ()V
    flags: (0x0001) ACC_PUBLIC
    Code:
      stack=1, locals=1, args_size=1
         0: aload_0
         1: invokespecial #1                  // Method java/lang/Object."&lt;init&gt;":()V
         4: return
      LineNumberTable:
        line 1: 0
}

  public static void main(java.lang.String[]);
    descriptor: ([Ljava/lang/String;)V
    flags: (0x0009) ACC_PUBLIC, ACC_STATIC
    Code:
      stack=3, locals=2, args_size=1
         0: invokedynamic #7,  0              // InvokeDynamic #0:showTestNumber:()LLambdaTest$Test;
         5: astore_1
         6: getstatic     #11                 // Field java/lang/System.out:Ljava/io/PrintStream;
         9: aload_1
        10: ldc           #17                 // int 114514
        12: invokestatic  #18                 // Method java/lang/Integer.valueOf:(I)Ljava/lang/Integer;
        15: invokeinterface #24,  2           // InterfaceMethod LambdaTest$Test.showTestNumber:(Ljava/lang/Integer;)Ljava/lang/String;
        20: invokevirtual #29                 // Method java/io/PrintStream.println:(Ljava/lang/String;)V
        23: return
      LineNumberTable:
        line 8: 0
        line 9: 6
        line 10: 23
}
SourceFile: "LambdaTest.java"
NestMembers:
  LambdaTest$Test
BootstrapMethods:
  0: #49 REF_invokeStatic java/lang/invoke/LambdaMetafactory.metafactory:(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodHandle;Ljava/lang/invoke/MethodType;)Ljava/lang/invoke/CallSite;
    Method arguments:
      #56 (Ljava/lang/Integer;)Ljava/lang/String;
      #57 REF_invokeStatic LambdaTest.lambda$main$0:(Ljava/lang/Integer;)Ljava/lang/String;
      #56 (Ljava/lang/Integer;)Ljava/lang/String;
  1: #60 REF_invokeStatic java/lang/invoke/StringConcatFactory.makeConcatWithConstants:(Ljava/lang/invoke/