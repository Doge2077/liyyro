---
title: "浅谈 Java 中的 Lambda 表达式"
date: 2023-08-27
categories: [Java, lambda]
description: ""
---

`Lambda` 表达式是一种匿名函数，它可以作为参数传递给方法或存储在变量中。在 `Java8` 中，它和函数式接口一起，共同构建了函数式编程的框架。

---

## 什么是函数式编程

---

函数式编程是一种编程范式，也是一种思想。

它将计算视为函数求值的过程，并强调函数的纯粹性和不可变性。在函数式编程中，函数被视为一等公民，可以作为参数传递、存储在变量中，并且函数的执行不会产生副作用。

例如，我们想要输出 `List` 中的全部元素，命令式编程看起来是下面这样：
```java


public class Main {
    public static void main(String[] args) {
        List&lt;Integer&gt; list = Arrays.asList(1, 2, 3, 4, 5);
        for (Integer item : list) {
            System.out.println(item);
        }       
    }
}
```

而在函数式编程的思想下，代码则看起来是下面这样：
```java


public class Main {
    public static void main(String[] args) {
        List&lt;Integer&gt; list = Arrays.asList(1, 2, 3, 4, 5);
        list.forEach(System.out::println);
    }
}
```

从以上的两个例子中，可以看出，命令式编程需要我们自己去实现具体的逻辑细节。而函数式编程则是调用 `API` 完成需求的实现，将原本命令式的代码写成一系列嵌套的函数调用。

由此可见，在函数式编程的思想下，我们将功能的具体细节隐藏，将其抽象为了函数式接口，这就使得具有规范、稳定、可组合、高复用的特点。

---

## Lambda 与匿名内部类

---

既然函数式编程需要将功能抽象为接口，那么我们来回顾一下接口的使用。

接口作为 `java` 中的一种抽象类型，它定义了一组方法的签名（方法名、参数列表和返回类型），但**没有具体的实现** 。

因此，要使用接口，就**必须提供相应的实现类，或者包含实现接口的对象返回** 。例如，要想使用 `List` 接口，我们可以使用实现了该接口的实现类 `ArrayList`、`LinkdeList` 等，或者像上节例子一样，使用 `Arrays.asList` 的工厂方法返回了一个实现了 `List` 接口的 `ArrayList` 对象。

其中，对于实现类来说，由于接口只需要实现某种功能，我们完全可以使用匿名内部类来实现，例如，我们把输出 `List` 的全部元素抽象为一个接口 `Show`，其中提供了一个函数方法 `ShowAllItems`。
```java


public interface Show {
    void ShowAllItems(List&lt;Integer&gt; arrayList);
}
```

继续沿用之前代码示例，现在要求输出 `List` 中的全部元素：
```java


public class Main {
    public static void main(String[] args) {
        List&lt;Integer&gt; list = Arrays.asList(1, 2, 3, 4, 5);
        Show show = new Show() {
            @Override
            public void ShowAllItems(List&lt;Integer&gt; arrayList) {
                for (Integer item : arrayList) System.out.println(item);
            }
        };
        show.ShowAllItems(list);
    }
}
```

上述代码中，由于接口 `Show` 其中只有一个抽象方法 `ShowAllItems`，如果单独为该接口实现一个类未免显得太过笨拙，因此我们在使用时直接使用匿名内部类的实现，通过这种方式创建一个临时的实现子类，这就令接口的使用更加灵活。

那么问题来了，如果我们后续仍要使用多次该接口，每次使用都以匿名内部类的方式来实现，会导致我们的代码太过臃肿，有没有更好的解决办法呢？

当然有的，这就是我们今天讨论的主人公—— `Lambda` 表达式，**如果一个接口中有且只有一个待实现的抽象方法** ，那么我们可以将匿名内部类简写为 `Lambda` 表达式：
```java


public class Main {
    public static void main(String[] args) {
        List&lt;Integer&gt; list = Arrays.asList(1, 2, 3, 4, 5);
        Show show = param -> {
            for (Integer item : param) System.out.println(item);
        };
        show.ShowAllItems(list);
    }
}
```

也许上面的示例会使你感到困惑，下面我们来详细探讨一下 `Lambda` 表达式的基础语法。

---

## Lambda 表达式基础语法

---

  * 标准格式为：`([参数类型 参数名称,]...) ‐> { 代码语句，包括返回值 }`
  * 和匿名内部类不同，`Lambda` 表达式**仅支持接口** ，不支持抽象类。
  * 接口内部必须**有且仅有一个抽象方法** （可以有多个方法，但是必须保证其他方法有默认实现，必须留一个抽象方法出来）
  * `Lambda` 表达式可以在函数体中引用外部的变量，从而实现了闭包，但对进入闭包的变量有 `final` 的限制。



接下来，我们看一个简单示例，假设接口 `Test` 中有且仅有如下抽象方法：
```java


public interface Test {
    String showTestNumber(Integer param);
}
```

利用上述接口，我们使用如下匿名内部类来实现该方法：
```java


public class Main {
    public static void main(String[] args) {
        Test test = new Test() {
            @Override
            public String showTestNumber(Integer param) {
                return "Test number is " + param;
            }
        };
        System.out.println(test.showTestNumber(114));
    }
}
```

如果将其转换为 `Lambda` 的标准格式，则为：
```java


public class Main {
    public static void main(String[] args) {
        Test test = (Integer param) -> {
            return "Test number is " + param;
        };
        System.out.println(test.showTestNumber(514));
    }
}
```

由于该方法只需传递一个参数，因此可以省略参数类型及其括号：
```java


public class Main {
    public static void main(String[] args) {
        Test test = param -> {
            return "Test number is " + param;
        };
        System.out.println(test.showTestNumber(1919));
    }
}
```

又因为方法实现只有一条 `return` 语句，则后面的 `{ ... }` 也可以省略：
```java


public class Main {
    public static void main(String[] args) {
        Test test = param -> "Test number is " + param;
        System.out.println(test.showTestNumber(810));
    }
}
```

此外，如果方法已经实现，我们可以利用方法引用：
```java


public class Main {
    public static void main(String[] args) {
        Test test = Main::showTestNumber;
        System.out.println(test.showTestNumber(721));
    }

    // 提取方法实现
    private static String showTestNumber(Integer param) {
        return "Test number is " + param;
    }
}
```

在上述示例代码中，`Main::showTestNumber`是一个方法引用，它引用了 `Main` 类中的静态方法 `showTestNumber`。该方法被赋值给 `Test`接口的实例变量 `test`。

关于方法引用的使用，我们在后面还会重新提到。但这里我需要先介绍一下关于闭包的特性。

> 闭包是一个函数（或过程），它可以访问并操作其作用域外部的变量。在 `Java` 中，可以通过 `Lambda` 表达式或方法引用来创建闭包。

其实，在 `main` 方法中，我们还可以通过调用 `test.showTestNumber` 来调用闭包。闭包中的方法 `showTestNumber` 可以访问并操作其作用域外部的变量。

为了更清晰地展示 `Lambda` 的闭包过程，我们使用如下示例：
```java


public class Main {
    public static void main(String[] args) {
        String Claim = "Test number is ";
        Test test = param -> Claim + param;
        System.out.println(test.showTestNumber(2333));
    }
}
```

在上述示例代码中，`Lambda` 表达式捕获了外部变量 `Claim`，并在 `Lambda` 表达式的范围之外（main()方法内部）调用闭包时仍然可以访问和使用该变量。

**注意** ：`Java8` 不要求显式将闭包变量声明为 `final`，但如果你尝试修改闭包变量的值，则会报错。
```java


public class Main {
    public static void main(String[] args) {
        String Claim = "Test number is ";
        Claim = "Yeah~ The number is ";  // 从lambda 表达式引用的本地变量必须是最终变量或实际上的最终变量
        Test test = param -> Claim + param;  
        System.out.println(test.showTestNumber(2333));
    }
}
```

---

## Lambda 的应用

---

好了，你已经学会 $1 + 1 = 2$ 了，现在来康康更实际的东西吧（

---

### 无参的函数式接口

---

以最常用的 `Runnable` 接口为例：

在 `Java8` 之前，如果需要新建一个线程，使用匿名内部类的写法是这样：
```java


public class Main {
    public static void main(String[] args) {
        Runnable runnable = new Runnable() {
            @Override
            public void run() {
                System.out.println("哼哼哼啊啊啊~");
            }
        };
        runnable.run();
    }
}
```

如果使用 `Lambda` 表达式则看起来是这样；
```java


public class Main {
    public static void main(String[] args) {
        Runnable runnable = () -> System.out.println("哼哼哼啊啊啊~");
        runnable.run();
    }
}
```

我们来看一下具体的 `Runnable` 接口：
```java


@FunctionalInterface
public interface Runnable {
    public abstract void run();
}
```

可以看到该接口上面有 `@FunctionalInterface` 注解，该注解标识了一个接口是函数式接口。因此，我们可以使用 `Lambda` 表达式将匿名内部类进行替换。

值得注意的是，`@FunctionalInterface` 注解并不是必须的，它只是作为一种提示和约束的工具。当我们在定义接口时，如果希望该接口只包含一个抽象方法，以便可以使用 `Lambda` 表达式或方法引用进行函数式编程，可以选择添加 `@FunctionalInterface` 注解来明确表达这个意图。

即使没有添加 `@FunctionalInterface` 注解，只要该接口符合函数式接口的定义（只有一个抽象方法），它仍然可以用于函数式编程。

---

### 带参的函数式接口

---

这里假设我们需要对一个数组进行排序：

在 `Java8` 之前，对数组进行排序可以使用 `Arrays.sort` 方法，如果需要指定排序规则，只需要实现其中的 `Comparator` 方法即可：
```java


public class Main {
    public static void main(String[] args) {
        Integer[] array = new Integer[]{4, 5, 9, 3, 2, 8, 1, 0, 6};
        Arrays.sort(array, new Comparator&lt;Integer&gt;() {
            @Override
            public int compare(Integer o1, Integer o2) {
                return o1 - o2;
            }
        });
        System.out.println(Arrays.toString(array)); //按从小到大的顺序排列
    } 
}
```

转换为 `Lambda` 表达式可以是下面这样：
```java


public class Main {
    public static void main(String[] args) {
        Integer[] array = new Integer[]{4, 5, 9, 3, 2, 8, 1, 0, 6};
        Arrays.sort(array, (o1, o2) -> o1 - o2);
        System.out.println(Arrays.toString(array)); //按从小到大的顺序排列
    }
}
```

---

### 方法引用

---

`Java` 方法引用是一种简化 `Lambda` 表达式的语法，用于直接引用已经存在的方法。方法引用可以通过以下几种方式来表示：

  1. 静态方法引用：引用静态方法，使用类名或者接口名作为前缀，后面跟上方法名。例如我们在之前例子中介绍过的 `Main::showTestNumber`。

  2. 实例方法引用：引用非静态方法，使用对象名或者对象引用作为前缀，后面跟上方法名。例如，`objectName::instanceMethodName`。

  3. 特定类的任意对象方法引用：引用特定类的实例方法，使用类名作为前缀，后面跟上方法名。例如，`ClassName::instanceMethodName`。

  4. 构造方法引用：引用构造方法，使用类名后面跟上 `new` 关键字。例如，`ClassName::new`。

  5. 数组构造方法引用：引用数组的构造方法，使用数组类型后面跟上 `new` 关键字。例如，`TypeName[]::new`。




需要注意的是，方法引用的适用条件是被引用的方法的签名（参数类型和返回类型）必须与函数式接口中的抽象方法的参数类型和返回类型相匹配。

我们使用上节数组排序的情景进行举例，即使我们已经利用 `Lambda` 表达式进行了大幅度的简化，但是这还不够，我们观察 `Integer` 类，其中有一个叫做 `compare` 的静态方法：
```java


public static int compare(int x, int y) {
    return (x < y) ? -1 : ((x == y) ? 0 : 1);
}
```

该方法是一个静态方法，但是它却和 `Comparator` 需要实现的方法返回值和参数定义一模一样，因此我们直接进行方法引用：
```java


public class Main {
    public static void main(String[] args) {
        Integer[] array = new Integer[]{4, 5, 9, 3, 2, 8, 1, 0, 6};
        Arrays.sort(array, Integer::compare);
        System.out.println(Arrays.toString(array)); //按从小到大的顺序排列
    }
}
```

如果不使用静态方法，而使用普通的成员方法，即在 `Comparator` 中，我们需要实现的方法为：
```java


public int compare(Integer o1, Integer o2) {
     return o1 - o2;
}
```

其中 `o1` 和 `o2` 都是 `Integer` 类型，而在 `Integer` 类中有一个 `compareTo` 方法：
```java


public int compareTo(Integer anotherInteger) {
    return compare(this.value, anotherInteger.value);
}
```

如果是以匿名内部类的方式实现，那么代码如下：
```java


public class Main {
    public static void main(String[] args) {
        Integer[] array = new Integer[]{4, 5, 9, 3, 2, 8, 1, 0, 6};
        Arrays.sort(array, new Comparator&lt;Integer&gt;() {
            @Override
            public int compare(Integer o1, Integer o2) {
                return o1.compareTo(o2);
            }
        });
        System.out.println(Arrays.toString(array)); //按从小到大的顺序排列
    }
}
```

继续将上述匿名内部类替换为 `Lambda` 表达式如下：
```java


public class Main {
    public static void main(String[] args) {
        Integer[] array = new Integer[]{4, 5, 9, 3, 2, 8, 1, 0, 6};
        Arrays.sort(array, (o1, o2) -> o1.compareTo(o2));
        System.out.println(Arrays.toString(array)); //按从小到大的顺序排列
    }
}
```

由于该方法并非静态方法，而是所属的实例对象所有，如果我们想要引用该方法，我们需要进行实例方法引用：
```java


public class Main {
    public static void main(String[] args) {
        Integer[] array = new Integer[]{4, 5, 9, 3, 2, 8, 1, 0, 6};
        Arrays.sort(array, Integer::compareTo);
        System.out.println(Arrays.toString(array)); //按从小到大的顺序排列
    }
}
```

虽然看起来和刚才的静态方法引用没有什么区别，但实际上，当我们使用非静态方法时，会使用抽象方参数列表的第一个作为目标对象，后续参数作为目标对象成员方法的参数，即 `o1` 作为目标对象，`o2` 作为参数，正好匹配了 `compareTo` 方法。

对于构造方法引用，假设接口 `Test` 中有抽象方法 `newTest`：
```java


public interface Test {
    String newTest(String param);
}
```

对于普通的 `Lambda` 替换，代码如下：
```java


public class Main {
    public static void main(String[] args) {
        Test test = param -> param;
        System.out.println(test.newTest("哼哼哼啊啊啊~"));
    }
}
```

而我们注意到该方法其实就是 `String` 中的构造方法，因此我们直接进行构造方法引用：
```java


public class Main {
    public static void main(String[] args) {
        Test test = String::new;
        System.out.println(test.newTest("哼哼哼啊啊啊~"));
    }
}
```

---

## Lambda 表达式的本质

---

经过上面的学习，相信你已经可以熟练地使用 `Lambda` 表达式了，看起来 `Lambda` 只是一种简化匿名内部类进行实现接口的语法糖，但实际上，它们是两种本质不同的事物：

  * 匿名内部类本质是一个类，只是不需要我们显示地指定类名，编译器会自动为该类取名。
  * 而 `Lambda` 表达式本质是一个函数，当然，编译器也会为它取名，在 `JVM` 层面，这是通过 `invokedynamic` 指令实现的，编译器会将 `Lambda` 表达式转化为一个私有方法，并在需要的时候动态地生成一个函数式接口的实例。



假设我们使用上述 `Runnable` 的匿名内部类的代码进行编译，可以看到结果如下：

![image-20230827223157677](https://image.itbaima.net/images/40/image-20230827228841886.png)

可以看到， `Main$1.class` 实际上就是 `Main` 类中生成的匿名内部类文件，而将其替换为 `Lambda` 表达式后编译的结果如下：

![image-20230827224417232](https://image.itbaima.net/images/40/image-20230827222290045.png)

没有生成单独的类文件，即，匿名内部类对应的是一个 `class` 文件，而 `Lambda` 表达式对应的是它所在主类的一个私有方法。

如果你想深入了解，请移步[深入理解 JVM 之——字节码指令与执行引擎](&lt;https://lys2021.com/?p=1560&gt;)。

---

## 参考文献

---

  * [Java中的函数式编程](&lt;https://zhuanlan.zhihu.com/p/423995200&gt;)
  * [Java Lambda 表达式介绍](&lt;https://itbaima.net/document/0/4/0&gt;)
  * [在Java代码中写Lambda表达式是种怎样的体验](&lt;https://www.zhihu.com/question/37872003/answer/1009015660&gt;)



---
