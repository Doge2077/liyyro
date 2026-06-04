---
title: "C++面向对象程序设计"
date: 2022-08-29
categories: [c++, C/C++]
description: ""
---

# C++核心编程

---

## 1 内存分区模型

`C++`程序在执行时，将内存大方向划分为**4个区域**

*   **代码区**：存放函数体的二进制代码，由操作系统进行管理。
*   **全局区**：存放全局变量、静态变量以及常量。
*   **栈区**：由编译器自动分配释放，存放函数的参数值、局部变量等。
*   **堆区**：由程序员分配和释放，若程序员不释放，程序结束时由操作系统回收。

**内存四区意义：**

不同区域存放的数据，被赋予不同的生命周期，这给我们带来了更大的编程灵活性。

---

### 1.1 程序运行前

---

在程序编译后，生成了exe可执行程序，**未执行该程序前**分为两个区域

**(1) 代码区：**

**内容**：存放CPU执行的机器指令。

**特点**：
*   代码区是**共享**的，共享的目的是对于频繁被执行的程序，只需要在内存中有一份代码即可。
*   代码区是**只读**的，使其只读的原因是防止程序意外地修改了它的指令。

**(2) 全局区：**

**内容**：全局变量和静态变量存放在此。

**特点**：
*   全局区还包含了常量区，字符串常量和其他常量也存放在此。
*   该区域的数据在程序结束后由操作系统释放。

**示例：**
```cpp
#include &lt;iostream&gt;
#include &lt;string&gt;
using namespace std;

// 全局变量
int g_a = 10;
int g_b = 10;

// 静态全局变量
static int s_g_a = 10;
static int s_g_b = 10;

// 字符串全局常量
const char* g_s1 = "abcd";
const char* g_s2 = "abcd";

// const 修饰的全局常量
const int g_c_a = 10;
const int g_c_b = 10;

int main() {
    cout &lt;&lt; "程序运行前：" &lt;&lt; endl;
    cout &lt;&lt; endl;

    // 局部变量
    int a = 10;
    int b = 10;

    // 局部变量的地址
    cout &lt;&lt; "局部变量a的地址为：" &lt;&lt; &a &lt;&lt; endl;
    cout &lt;&lt; "局部变量b的地址为：" &lt;&lt; &b &lt;&lt; endl;

    // 全局变量的地址
    cout &lt;&lt; "全局变量g_a的地址为：" &lt;&lt; &g_a &lt;&lt; endl;
    cout &lt;&lt; "全局变量g_b的地址为：" &lt;&lt; &g_b &lt;&lt; endl;
    cout &lt;&lt; endl;

    // 静态局部变量
    static int s_a = 10;
    static int s_b = 10;

    // 静态局部变量的地址
    cout &lt;&lt; "静态局部变量s_a的地址为：" &lt;&lt; &s_a &lt;&lt; endl;
    cout &lt;&lt; "静态局部变量s_b的地址为：" &lt;&lt; &s_b &lt;&lt; endl;

    // 静态全局变量的地址
    cout &lt;&lt; "静态全局变量s_g_a的地址为：" &lt;&lt; &s_g_a &lt;&lt; endl;
    cout &lt;&lt; "静态全局变量s_g_b的地址为：" &lt;&lt; &s_g_b &lt;&lt; endl;
    cout &lt;&lt; endl;

    // 常量
    // 字符串常量
    const char* s1 = "abcd";
    const char* s2 = "abcd";
    cout &lt;&lt; "字符串常量s1的地址为：" &lt;&lt; (void*)s1 &lt;&lt; endl;
    cout &lt;&lt; "字符串常量s2的地址为：" &lt;&lt; (void*)s2 &lt;&lt; endl;

    // const修饰的局部常量
    const int c_a = 10;
    const int c_b = 10;
    cout &lt;&lt; "局部常量c_a的地址为：" &lt;&lt; &c_a &lt;&lt; endl;
    cout &lt;&lt; "局部常量c_b的地址为：" &lt;&lt; &c_b &lt;&lt; endl;
    cout &lt;&lt; endl;

    // 全局常量地址
    cout &lt;&lt; "全局常量g_c_a的地址为：" &lt;&lt; &g_c_a &lt;&lt; endl;
    cout &lt;&lt; "全局常量g_c_b的地址为：" &lt;&lt; &g_c_b &lt;&lt; endl;

    return 0;
}
```cpp
//const 修饰的局部常量
    const int c_a=10;
    const int c_b=10;

//字符串局部常量的地址
    cout&lt;&lt;"字符串局部常量s1的地址为："&lt;&lt;&s1&lt;&lt;endl;
    cout&lt;&lt;"字符串局部常量s2的地址为："&lt;&lt;&s2&lt;&lt;endl;

//字符串全局常量的地址
    cout&lt;&lt;"字符串全局常量g_s1的地址为："&lt;&lt;&g_s1&lt;&lt;endl;
    cout&lt;&lt;"字符串全局常量g_s2的地址为："&lt;&lt;&g_s2&lt;&lt;endl;

//const 修饰的局部常量
    cout&lt;&lt;"const 修饰的局部常量c_a的地址为："&lt;&lt;&c_a&lt;&lt;endl;
    cout&lt;&lt;"const 修饰的局部常量c_b的地址为："&lt;&lt;&c_b&lt;&lt;endl;

//const 修饰的全局常量
    cout&lt;&lt;"const 修饰的全局常量g_c_a的地址为："&lt;&lt;&g_c_a&lt;&lt;endl;
    cout&lt;&lt;"const 修饰的全局常量g_c_b的地址为："&lt;&lt;&g_c_b&lt;&lt;endl;

cout&lt;&lt;endl;

cout&lt;&lt;"有全局修饰的在全局区"&lt;&lt;endl;
    cout&lt;&lt;"其他的不在全局区"&lt;&lt;endl;

return 0;

}
```

---

**总结** ：

* `C++`中在程序运行前分为**全局区** 和**代码区**
  * 代码区特点是共享和只读
  * 全局区中存放全局变量、静态变量、常量
  * 常量区中存放 const 修饰的全局常量和字符串常量

---

### 1.2 程序运行后

---

在程序编译后，生成了exe可执行程序，**执行该程序后** 分为两个区域

**(1) 栈区：**

* 由编译器自动分配释放, 存放函数的参数值,局部变量等

**注意事项** ：不要返回局部变量的地址，栈区开辟的数据由编译器自动释放

**(2) 堆区：**

* 由程序员分配释放,若程序员不释放,程序结束时由操作系统回收

* 在`C++`中主要利用new在堆区开辟内存

**示例：**
```cpp

#include &lt;stdio.h&gt; 
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

int* test_01(){
    int a=10;  //局部变量存储在栈区 
    return &a;  //不要返回局部变量的地址 
}

int* test_02(){
    int* m=new int(10);  //利用new将数据开辟到堆区 
    return m;
}

int main(){

cout&lt;&lt;"栈区数据由编译器自动分配释放, 存放函数的参数值,局部变量等"&lt;&lt;endl;

//调用函数test_01 
    int* p1=test_01();

cout&lt;&lt;endl;

//输出 
    cout&lt;&lt;"第一次输出，编译器对局部变量做一次保留，暂时不释放： "&lt;&lt;*p1&lt;&lt;endl;

cout&lt;&lt;"第二次输出，编译器不再保留栈区的数据，直接释放："&lt;&lt;*p1&lt;&lt;endl;

cout&lt;&lt;"不要返回局部变量的地址！！！"&lt;&lt;endl;

cout&lt;&lt;endl;
```

//调用函数test_02
    int* p2=test_02();

//输出
    cout&lt;&lt;"输出存放在堆区的数据，编译器不释放，由程序员手动释放: "&lt;&lt;*p2&lt;&lt;endl; 
    cout&lt;&lt;"输出存放在堆区的数据，编译器不释放，由程序员手动释放: "&lt;&lt;*p2&lt;&lt;endl; 
    cout&lt;&lt;"输出存放在堆区的数据，编译器不释放，由程序员手动释放: "&lt;&lt;*p2&lt;&lt;endl;

cout&lt;&lt;endl;

//释放堆中开辟的数据
    delete p2;

cout&lt;&lt;"程序员手动释放后: "&lt;&lt;*p2&lt;&lt;endl;

return 0;

}
```

---

**总结：**

堆区数据由程序员管理开辟和释放

堆区数据利用`new`关键字进行开辟内存

---

### 1.3 new操作符

---

`C++`中利用`new`操作符在堆区开辟数据

堆区开辟的数据，由程序员手动开辟，手动释放，释放利用操作符`delete`

**语法**：`new 数据类型`

利用`new`创建的数据，会返回该数据对应的类型的指针

**示例1：开辟数据**
```cpp
#include &lt;stdio.h&gt; 
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

int* test_01(){
    int* a=new int(10);  //堆区开辟数据
    return a;
}

int main(){

int *p=test_01();

cout&lt;&lt;*p&lt;&lt;endl;
    cout&lt;&lt;*p&lt;&lt;endl;

//利用delete释放堆区数据
    delete p;

cout&lt;&lt;*p&lt;&lt;endl; //已释放，输出垃圾值

return 0;

}
```

**示例2：开辟数组**
```cpp
#include &lt;stdio.h&gt; 
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

int* test_01(){
    int* a=new int[10];  //堆区中开辟数组 
    return a;
}

int main(){

int *p=test_01();

for(int i=0;i&lt;10;i++) p[i]=i+1;  //赋值

for(int i=0;i&lt;10;i++) cout&lt;&lt;p[i]&lt;&lt;" ";  //输出

cout&lt;&lt;endl;

//未释放前输出p[0]
    cout&lt;&lt;*p&lt;&lt;endl;

//利用delete释放堆区数据
    delete[] p;

//已释放，输出垃圾值 
    cout&lt;&lt;*p&lt;&lt;endl;

return 0;

}
```

---

## 2 引用及其使用

---

### 2.1 引用的基本使用

---

**作用：** 给变量起别名

**语法：** `数据类型 &别名 = 原名`

**示例：**
```cpp
```

#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

int main(){

    int a = 10;

    int &b = a;  // 创建a的别名为b，必须初始化

    cout &lt;&lt; "a = " &lt;&lt; a &lt;&lt; endl;
    cout &lt;&lt; "b = " &lt;&lt; b &lt;&lt; endl;  // b的值同a

    // 修改a的值 
    a = 20;

    cout &lt;&lt; "a = " &lt;&lt; a &lt;&lt; endl;
    cout &lt;&lt; "b = " &lt;&lt; b &lt;&lt; endl;  // b的值也发生改变

    // 修改b的值 
    b = 10;

    cout &lt;&lt; "a = " &lt;&lt; a &lt;&lt; endl;  // a的值也发生改变 
    cout &lt;&lt; "b = " &lt;&lt; b &lt;&lt; endl;

    return 0;

}
```

---

### 2.2 引用注意事项

---

* 引用必须初始化

* 引用在初始化后，不可以改变

示例：
```cpp

#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

int main() {

    int a = 10;
    int b = 20;
    // int &c; // 错误，引用必须初始化
    int &c = a; // 一旦初始化后，就不可以更改
    c = b; // 这是赋值操作，不是更改引用

    cout &lt;&lt; "a = " &lt;&lt; a &lt;&lt; endl;
    cout &lt;&lt; "b = " &lt;&lt; b &lt;&lt; endl;
    cout &lt;&lt; "c = " &lt;&lt; c &lt;&lt; endl;

    return 0;

}
```

---

### 2.3 引用做函数参数

---

**作用：** 函数传参时，可以利用引用的技术让形参修饰实参

**优点：** 可以简化指针修改实参

**示例：**
```cpp

#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

void swap(int &a, int &b){
    int t = a;
    a = b;
    b = t;
}

int main(){

    int a = 10;
    int b = 20;

    cout &lt;&lt; "a = " &lt;&lt; a &lt;&lt; endl;
    cout &lt;&lt; "b = " &lt;&lt; b &lt;&lt; endl;

    cout &lt;&lt; endl;

    swap(a, b);

    cout &lt;&lt; "a = " &lt;&lt; a &lt;&lt; endl;
    cout &lt;&lt; "b = " &lt;&lt; b &lt;&lt; endl;

    return 0;

}
```

**总结**：通过引用参数产生的效果同按地址传递是一样的。引用的语法更清楚简单。

---

### 2.4 引用做函数返回值

---

**作用**：引用是可以作为函数的返回值存在的

**注意**：**不要返回局部变量引用**

**用法**：函数调用作为左值

**示例：**
```cpp

#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

int& test() {
    static int a = 10; // 静态局部变量，生命周期长于函数
    return a;
}

int main() {

    int &ref = test();
    cout &lt;&lt; "ref = " &lt;&lt; ref &lt;&lt; endl;

    test() = 20; // 函数调用作为左值
    cout &lt;&lt; "ref = " &lt;&lt; ref &lt;&lt; endl;

    return 0;

}
```

# 修复后的文本

```cpp
#include &lt;stdio.h&gt; 
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

int &test_01(){
    int a=10;  //局部变量 
    return a;
}

int &test_02(){
    static int a=10;  //全局区变量 
    return a;
}

int main(){

    int &ans_01=test_01();

    cout&lt;&lt;"ans_01 = "&lt;&lt;ans_01&lt;&lt;endl;  //第一次输出正确是因为编译器做了保留 
    cout&lt;&lt;"ans_01 = "&lt;&lt;ans_01&lt;&lt;endl;  //再次输出已经被释放，输出垃圾值
    cout&lt;&lt;"不要返回局部变量的引用！！！"&lt;&lt;endl;

    cout&lt;&lt;endl;

    int &ans_02=test_02();

    cout&lt;&lt;"ans_02 = "&lt;&lt;ans_02&lt;&lt;endl;
    cout&lt;&lt;"ans_02 = "&lt;&lt;ans_02&lt;&lt;endl;
    cout&lt;&lt;"ans_02 = "&lt;&lt;ans_02&lt;&lt;endl;

    test_02()=20;  //函数调用作为左值

    cout&lt;&lt;"ans_02 = "&lt;&lt;ans_02&lt;&lt;endl;

    return 0;
}
```

---

### 2.5 引用的本质

---

**本质**：引用的本质在C++内部实现是一个**指针常量**。

讲解示例：
```cpp
#include &lt;stdio.h&gt; 
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

//发现是引用，转换为 int* const ref = &a;
void test_01(int& ref){
    ref=100; // ref是引用，转换为 *ref = 100
}

int main(){

    int a=10;

    //自动转换为 int* const ref = &a; 指针常量是指针指向不可改，也说明为什么引用不可更改
    int& ref=a; 
    ref=20; //内部发现ref是引用，自动帮我们转换为: *ref = 20;

    cout&lt;&lt;"a = "&lt;&lt;a&lt;&lt;endl;
    cout&lt;&lt;"ref = "&lt;&lt;ref&lt;&lt;endl;

    test_01(a);

    cout&lt;&lt;"a = "&lt;&lt;a&lt;&lt;endl;
    cout&lt;&lt;"ref = "&lt;&lt;ref&lt;&lt;endl;

    return 0;
}
```

**结论**：`C++`推荐用引用技术，因为语法方便，引用本质是指针常量，但是所有的指针操作编译器都帮我们做了。

---

### 2.6 常量引用

---

**作用：** 常量引用主要用来修饰形参，防止误操作

在函数形参列表中，可以加 `const` 修饰形参，防止形参改变实参

**示例：**
```cpp
```

---

**主要修复内容：**
1. 代码块语言标记从 `java` 改为 `cpp`
2. 统一代码缩进格式（main函数内部代码统一缩进）
3. 修复引号符号（`==const修饰形参==` 改为 `` `const` 修饰形参 ``）
4. 去除多余的符号

# 修复后文本

```cpp
#include &lt;stdio.h&gt; 
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

int test_01(const int &a){
    int b=a+10;
//  a=b;  //报错 a被const修饰 不可修改
    return b;
}

int main(){
    int a=10;
    int b=test_01(a);
    cout&lt;&lt;"a = "&lt;&lt;a&lt;&lt;endl;
    cout&lt;&lt;"b = "&lt;&lt;b&lt;&lt;endl;
    return 0;
}
```

---

## 3 函数提高

---

### 3.1 函数默认参数

---

在 `C++` 中，函数的形参列表中的形参是可以有默认值的。

语法：`返回值类型 函数名（参数=默认值）{}`

**示例：**
```cpp
//1. 如果某个位置参数有默认值，那么从这个位置往后，从左向右，必须都要有默认值
//2. 如果函数声明有默认值，函数实现的时候就不能有默认参数
#include &lt;stdio.h&gt; 
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

int add(int a,int b=10){
    return a+b;
}

int main(){
    int a=20,b=30;
    cout&lt;&lt;add(a,b)&lt;&lt;endl;
    cout&lt;&lt;add(a)&lt;&lt;endl;  //未传入参数b，默认b=10
    return 0;
}
```

---

### 3.2 函数占位参数

---

`C++` 中函数的形参列表里可以有占位参数，用来做占位，调用函数时必须填补该位置。

**语法：** `返回值类型 函数名（数据类型）{}`

在现阶段函数的占位参数存在意义不大，但是后面的课程中会用到该技术。

**示例：**
```cpp
//函数占位参数，占位参数也可以有默认参数
#include &lt;stdio.h&gt; 
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

int add(int a,int){
    return a;
}

int main(){
    int a=20,b=30;
    cout&lt;&lt;add(a,b)&lt;&lt;endl;  //占位参数必须填补
    return 0;
}
```

### 3.3 函数重载

---

#### 3.3.1 函数重载概述

---

**作用：** 函数名可以相同，提高复用性。

**函数重载满足条件：**

- 同一个作用域下
  - 函数名称相同
  - 函数参数 **类型不同** 或者 **个数不同** 或者 **顺序不同**

**注意：** 函数的返回值不可以作为函数重载的条件。

**示例：**
```cpp
// 示例代码将在此处继续...
```

//函数重载需要函数都在同一个作用域下
#include &lt;stdio.h&gt; 
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

int add(){
    cout &lt;&lt; "add() 的调用： " &lt;&lt; 0 &lt;&lt; endl;
}

int add(int a){
    cout &lt;&lt; "add(int a) 的调用：" &lt;&lt; a &lt;&lt; endl;
}

int add(double a){
    cout &lt;&lt; "add(double a) 的调用：" &lt;&lt; a &lt;&lt; endl;
}

int add(int a, int b){
    cout &lt;&lt; "add(int a, int b) 的调用：" &lt;&lt; a &lt;&lt; "+" &lt;&lt; b &lt;&lt; "=" &lt;&lt; a + b &lt;&lt; endl;
}

int add(int a, double b){
    cout &lt;&lt; "add(int a, double b) 的调用：" &lt;&lt; a &lt;&lt; "+" &lt;&lt; b &lt;&lt; "=" &lt;&lt; a + b &lt;&lt; endl;
}

int add(double a, int b){
    cout &lt;&lt; "add(double a, int b) 的调用：" &lt;&lt; a &lt;&lt; "+" &lt;&lt; b &lt;&lt; "=" &lt;&lt; a + b &lt;&lt; endl;
}

int add(double a, double b){
    cout &lt;&lt; "add(double a, double b) 的调用：" &lt;&lt; a &lt;&lt; "+" &lt;&lt; b &lt;&lt; "=" &lt;&lt; a + b &lt;&lt; endl;
}

int main(){
    add();
    add(1);
    add(1.11);
    add(1, 2);
    add(1, 2.22);
    add(1.11, 2);
    add(1.11, 2.22);
    return 0;
}
```

---

#### 3.3.2 函数重载注意事项

---

* 引用作为重载条件
* 函数重载碰到函数默认参数

**示例：**

```cpp
//1、引用作为重载条件
#include &lt;stdio.h&gt; 
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

void func(int &a){
    cout &lt;&lt; "func(int &a) 的调用：" &lt;&lt; a &lt;&lt; endl;
}

void func(const int &a){
    cout &lt;&lt; "func(const int &a) 的调用：" &lt;&lt; a &lt;&lt; endl;
}

int main(){
    int a = 10;
    func(a);    //调用无const
    func(20);   //调用有const
    return 0;
}

//函数重载碰到函数默认参数
#include &lt;stdio.h&gt; 
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

void func(int a, int b = 10){
    cout &lt;&lt; "func(int a, int b = 10) 的调用" &lt;&lt; endl;
}
```
void func(int a)
{
    cout&lt;&lt;"func(int a) 的调用"&lt;&lt;endl;
}

int main(){

func(10);  //报错，原因产生歧义

return 0;

}
```

---

## **4** 类和对象

---

`C++`面向对象的三大特性为：`封装、继承、多态`

`C++`认为**万事万物皆为对象**，对象有其属性和行为

**例如：**

​ 人可以作为对象，属性有姓名、年龄、身高、体重...，行为有走、跑、跳、吃饭、唱歌...

​ 车也可以作为对象，属性有轮胎、方向盘、车灯...，行为有载人、放音乐、放空调...

​ 具有相同性质的==对象==，我们可以抽象称为==类==，人属于人类，车属于车类

---

### 4.1 封装

---

#### 4.1.1 封装的意义

---

封装是`C++`面向对象三大特性之一

封装的意义：

* 将属性和行为作为一个整体，表现生活中的事物
  * 将属性和行为加以权限控制

**封装意义一：**

​ 在设计类的时候，属性和行为写在一起，表现事物

**语法：** `class 类名{ 访问权限： 属性 / 行为 };`

**示例1：** 设计一个圆类，求圆的周长

**示例代码：**
```cpp

//1、封装的意义
//将属性和行为作为一个整体，用来表现生活中的事物

//封装一个圆类，求圆的周长
#include &lt;stdio.h&gt; 
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

const double PI=3.1415926;

class circle{
    public:  //访问权限  公共的权限

//属性
        int r;  //半径

//行为
        double calculate(){  //计算圆的周长
            return r*r*PI;
        }

};

int main(){

//通过圆类，创建圆的对象
    circle c1;  // c1就是一个具体的圆

c1.r=10;  //给圆对象的半径 进行赋值操作

cout&lt;&lt;"c1的周长为： "&lt;&lt;c1.calculate()&lt;&lt;endl;

return 0;

}
```

**封装意义二：**

类在设计时，可以把属性和行为放在不同的权限下，加以控制

访问权限有三种：

1. public 公共权限 
  2. protected 保护权限
  3. private 私有权限

**示例：**
```cpp

//三种权限
//公共权限  public     类内可以访问  类外可以访问
//保护权限  protected  类内可以访问  类外不可以访问
//私有权限  private    类内可以访问  类外不可以访问
#include &lt;stdio.h&gt; 
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

class person{
    public:  //访问权限  公共的权限
```

//姓名  公共权限
        string name;

protected:

//钱  保护权限
        int money;

private:

//年龄 私有权限 
        int year;

public:
        void make(){  //初始化 
            name="lys";
            money=100000000;
            year=20;
        }

};

int main(){

//通过person类,创建对象p1 
    person p1;

p1.make();  //初始化p1

cout&lt;&lt;p1.name;  //public 类外可以访问

p1.money=0;  // protected 类外不可更改，不可访问 
    cout&lt;&lt;p1.money;

p1.year=100;  //private 类外不可更改，不可访问 
    cout&lt;&lt;p1.year;

return 0;

}
```

---

#### 4.1.2 struct和class区别

---

在`C++`中 struct和class唯一的**区别** 就在于 **默认的访问权限不同**

区别：

* struct 默认权限为公共
  * class 默认权限为私有

```cpp

#include &lt;stdio.h&gt; 
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

struct point_1{
    int x,y;  //默认是公共权限
};

class point_2{
    int x,y;  //默认是私有权限
};

int main(){
    point_1 p1;
    point_2 p2;

    p1.x=10;
    p1.y=20;

    p2.x=10;
    p2.y=20;  //错误，访问权限是私有

    return 0;
}
```

---

### 4.2 对象的初始化和清理

---

#### 4.2.1 构造函数和析构函数

---

对象的**初始化和清理** 也是两个非常重要的安全问题

一个对象或者变量没有初始状态，对其使用后果是未知。

同样的使用完一个对象或变量，没有及时清理，也会造成一定的安全问题。

**解决方法**：

C++利用了**构造函数** 和**析构函数** 解决上述问题，这两个函数将会被编译器自动调用，完成对象初始化和清理工作。

对象的初始化和清理工作是编译器强制要我们做的事情，因此如果**我们不提供构造和析构，编译器会提供**。

**编译器提供的构造函数和析构函数是空实现。**

* **构造函数** ：主要作用在于创建对象时为对象的成员属性赋值，构造函数由编译器自动调用，无须手动调用。
  * **析构函数** ：主要作用在于对象**销毁前** 系统自动调用，执行一些清理工作。

**构造函数语法：**`类名(){}`

1. 构造函数，**没有返回值也不写void**。
2. **函数名称与类名相同**。
3. 构造函数**可以有参数**，因此**可以发生重载**。
4. 程序在调用对象时候会自动调用构造，无须手动调用，而且只会调用一次。

**析构函数语法：** `~类名(){}`

1. 析构函数，**没有返回值也不写 void**
2. 函数名称与类名相同，在名称前加上符号 `~`
3. 析构函数**不可以有参数**，因此**不可以发生重载**
4. 程序在对象销毁前会自动调用析构，无须手动调用，而且只会调用一次
5. **不能设为私有**

```cpp
#include &lt;stdio.h&gt; 
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

class point{
    public:
        // 构造函数
        point(){
            cout&lt;&lt;"point的构造函数调用"&lt;&lt;endl;
        }

        // 析构函数
        ~point(){
            cout&lt;&lt;"point的析构函数调用"&lt;&lt;endl;
        }
};

int main(){
    point p1;
    return 0;
}
```

---

#### 4.2.2 构造函数的分类及调用方式

---

两种分类方式：

- 按参数分为：有参构造和无参构造
- 按类型分为：普通构造和拷贝构造

三种调用方式：

- 括号法
- 显示法
- 隐式转换法

**示例：**
```cpp
// 1、构造函数分类：
// 按照参数分类分为 有参和无参构造   无参又称为默认构造函数
// 按照类型分类分为 普通构造和拷贝构造
#include &lt;stdio.h&gt; 
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

class point{
    public:
        int x, y;

        point(){
            cout&lt;&lt;"无参构造函数调用"&lt;&lt;endl; 
        }

        point(int a, int b){
            x=a;
            y=b;
            cout&lt;&lt;"有参构造函数调用"&lt;&lt;endl;
        }

        point(const point &p){
            x=p.x;
            y=p.y;
            cout&lt;&lt;"拷贝构造函数调用"&lt;&lt;endl;
        }
};

int main(){
    // 括号法，常用
    point p1;       // 调用无参构造函数
    point p2(1,2);  // 调用有参构造函数
    point p3(p2);   // 调用拷贝构造函数

    // 注意：不可写成 point p1()，否则编译器会认为是函数声明而不是构造

    point p4=point();      // 调用无参构造函数
    point p5=point(3,4);   // 调用有参构造函数
    point p6=point(p5);    // 调用拷贝构造函数

    // 隐式转换法
    point p7;       // 调用无参构造函数
    point p8={5,6}; // 调用有参构造函数
    point p9=p8;    // 调用拷贝构造函数

    return 0;
}
```
return 0;
}
```

---

#### 4.2.3 拷贝构造函数调用时机

---

`C++`中拷贝构造函数调用时机通常有三种情况：

* 使用一个已经创建完毕的对象来初始化一个新对象
* 值传递的方式给函数参数传值
* 以值方式返回局部对象

**示例：**
```cpp
#include &lt;stdio.h&gt;
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

class point{
    public:
        int x,y;

        point(){
            cout &lt;&lt; "默认构造函数调用" &lt;&lt; endl;
        }

        point(int a,int b){
            x = a;
            y = b;
            cout &lt;&lt; "有参构造函数调用" &lt;&lt; endl;
        }

        point(const point &p){
            x = p.x;
            y = p.y;
            cout &lt;&lt; "拷贝构造函数调用" &lt;&lt; endl;
        }
};

//1. 使用一个已经创建完毕的对象来初始化一个新对象
void test01(){
    point p1(1,2);
    point p2(p1);
}

//2. 值传递的方式给函数参数传值
void make(point &p){
    p.x = 1;
    p.y = 2;
}

void test02(){
    point p3;
    make(p3);
    cout &lt;&lt; p3.x &lt;&lt; " " &lt;&lt; p3.y;
}

//3. 以值方式返回局部对象
int show_x(point p){
    return p.x;
}

void test03(){
    point p4(2,3);
    cout &lt;&lt; show_x(p4);
}

int main(){
    test01();
    test02();
    test03();
    return 0;
}
```

---

#### 4.2.4 构造函数调用规则

---

默认情况下，C++编译器至少给一个类添加3个函数：

1. 默认构造函数（无参，函数体为空）
2. 默认析构函数（无参，函数体为空）
3. 默认拷贝构造函数，对属性进行值拷贝

**构造函数调用规则**如下：

* 如果用户定义有参构造函数，C++不再提供默认无参构造，但是会提供默认拷贝构造
* 如果用户定义拷贝构造函数，C++不会再提供其他构造函数

**示例：**
```cpp
#include &lt;stdio.h&gt;
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

class point{
    public:
        int x,y;

        point(){
            cout &lt;&lt; "无参构造函数" &lt;&lt; endl;
        }
```cpp
point(int a, int b) {
    x = a;
    y = b;
    cout &lt;&lt; "有参构造函数" &lt;&lt; endl;
}

point(const point &p) {
    x = p.x;
    y = p.y;
    cout &lt;&lt; "拷贝构造函数" &lt;&lt; endl;
}

~point() {
    cout &lt;&lt; "析构函数" &lt;&lt; endl;
}
};

void test01() {
    point p1(1, 2);

    // 如果不写拷贝构造，编译器会自动添加拷贝构造，并且做浅拷贝操作
    point p2(p1);

    printf("p2 = (%d,%d)\n", p2.x, p2.y);
}

void test02() {
    // 如果用户提供有参构造，编译器不会提供默认构造，会提供拷贝构造
    point p3;  // 此时如果用户自己没有提供默认构造，会出错

    point p4(3, 4);  // 用户提供的有参

    point p5(p4);  // 此时如果用户没有提供拷贝构造，编译器会提供

    // 如果用户提供拷贝构造，编译器不会提供其他构造函数
    point p6;  // 此时如果用户自己没有提供默认构造，会出错

    point p7(5, 6);  // 此时如果用户自己没有提供有参，会出错
    point p8(p7);    // 用户自己提供拷贝构造
}

int main() {
    test01();
    test02();
    return 0;
}
```

---

#### 4.2.5 深拷贝与浅拷贝

---

* 浅拷贝：简单的赋值拷贝操作
* 深拷贝：在堆区重新申请空间，进行拷贝操作

**示例：**
```cpp
#include &lt;stdio.h&gt;
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

class point {
public:
    int x, y;
    int *z;

    point(int a, int b, int h) {
        x = a;
        y = b;
        z = new int(h);
    }

    // 用户未提供拷贝构造函数，执行浅拷贝

    ~point() {
        if (z != NULL) {
            delete z;
            z = NULL;
        }
    }
};

void test01() {
    point p1(1, 2, 3);
    point p2(p1);  // 用户未提供拷贝构造函数，执行浅拷贝
}

int main() {
    test01();
    return 0;
}

/*程序会崩掉，原因是在用户没有提供拷贝构造函数的前提下，
调用拷贝构造函数是编译器提供的默认拷贝构造函数，对h的地址进行拷贝，实现的是浅拷贝
在执行析构函数时，会造成h的内存重复释放的非法操作*/
```

**解决方案：**
```cpp
// 1. 用户自己提供拷贝构造函数
point(const point &p) {
    x = p.x;
    y = p.y;
    z = new int(*p.z); // 深拷贝
}
```
#include &lt;stdio.h&gt; 
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

class point{
    public:
        int x,y;
        int *z;

        point(int a,int b,int h){
            x=a;
            y=b;
            z=new int(h);
        }

        point(const point &p){
            x=p.x;
            y=p.y;
//          z=p.z;  //浅拷贝执行的操作 
            z=new int(*p.z);  //深拷贝执行的操作
        }

        ~point(){
            if(z!=NULL){
                delete z;
                z=NULL;
            }
        }

};

void test01(){

    point p1(1,2,3);

    point p2(p1);  //用户提供了拷贝函数，执行深拷贝

}

int main(){

    test01();

    return 0;
}
```

**总结**：如果属性有在堆区开辟的，一定要自己提供拷贝构造函数，防止浅拷贝带来的问题

---

#### 4.2.6 初始化列表

---

**作用：**`C++`提供了初始化列表语法，用来初始化属性

**语法：**`构造函数()：属性1(值1),属性2（值2）... {}`

**示例：**
```cpp
#include &lt;stdio.h&gt; 
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

class point{
    public:
        int x,y,z;

//传统方式初始化
//      point(int a,int b,int h){
//          x=a;
//          y=b;
//          z=h;
//      }

//初始化列表方式初始化
        point(int a,int b,int h):x(a),y(b),z(h) {}

};

void test01(){

    point p1(1,2,3);

    cout&lt;&lt;p1.x&lt;&lt;" "&lt;&lt;p1.y&lt;&lt;" "&lt;&lt;p1.z&lt;&lt;endl;

}

int main(){

    test01();

    return 0;
}
```

---

#### 4.2.7 类对象作为类成员

---

`C++`类中的成员可以是另一个类的对象，我们称该成员为对象成员

**例如**：
```cpp
class A{

};

class B{
    A a;
}
```

B类中有对象A作为成员，A为对象成员当创建B对象时，**A与B的构造和析构的顺序**

**示例：**
```cpp
```

**主要修复内容：**
1. 统一了代码块的语言标记（`cpp`）
2. 修正了类定义中的标点符号（`A a；` → `A a;`）
3. 调整了代码格式，使其更符合常规C++代码风格
4. 修正了部分文本中的标点符号

//构造的顺序是：先调用对象成员的构造，再调用本类构造
//析构顺序与构造相反
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

class A{
public:
    A(){
        cout &lt;&lt; "A的构造函数调用" &lt;&lt; endl;
    }

    ~A(){
        cout &lt;&lt; "A的析构函数调用" &lt;&lt; endl;
    }
};

class B{
public:
    A a;

    B(){
        cout &lt;&lt; "B的构造函数调用" &lt;&lt; endl;
    }

    ~B(){
        cout &lt;&lt; "B的析构函数调用" &lt;&lt; endl;
    }
};

int main(){
    B b2;
    return 0;
}
```

---

#### 4.2.8 静态成员

静态成员就是在成员变量和成员函数前加上关键字`static`，称为静态成员。

静态成员分为：

*   静态成员变量
    *   所有对象共享同一份数据
    *   在编译阶段分配内存
    *   类内声明，类外初始化
*   静态成员函数
    *   所有对象共享同一个函数
    *   静态成员函数只能访问静态成员变量

**示例1：静态成员变量**
```cpp
//静态成员变量特点：
    //1 在编译阶段分配内存
    //2 类内声明，类外初始化
    //3 所有对象共享同一份数据
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

class point{
public:
    static int x;

private:
    static int y;  //静态成员变量也是有访问权限的
};

int point::x = 10;
int point::y = 20;

int main(){
    point p1;
    p1.x = 20;
    cout &lt;&lt; p1.x &lt;&lt; endl;      //1、通过对象访问

    point p2;
    cout &lt;&lt; p2.x &lt;&lt; endl;      //共享同一份数据

    cout &lt;&lt; point::x &lt;&lt; endl;  //2、通过类名访问

    //cout &lt;&lt; p2.y &lt;&lt; endl;    //私有权限访问不到

    return 0;
}
```

**示例2：静态成员函数**
```cpp
//静态成员函数特点：
    //1 程序共享一个函数
    //2 静态成员函数只能访问静态成员变量
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

class point{
public:
    static int x;
    int y;
    // ... （后续代码）

```cpp
static void show_pub(){
    cout&lt;&lt;x&lt;&lt;endl;
    //cout&lt;&lt;y&lt;&lt;endl;  //错误，不可以访问非静态成员变量
}

private:
    static int z;

    //静态成员函数也是有访问权限的
    static void show_pri(){
        cout&lt;&lt;z&lt;&lt;endl;
    }
};

int point::x=10;
int point::z=30;

int main(){
    point p1;
    p1.y=20;
    
    //1、通过对象
    p1.show_pub();
    
    //2、通过类名
    point::show_pub();
    
    //p1.show_pri();  //私有权限访问不到
    
    return 0;
} 
```

---

### 4.3 C++对象模型和this指针

---

#### 4.3.1 成员变量和成员函数分开存储

---

在`C++`中，类内的成员变量和成员函数分开存储。

只有**非静态成员变量** 才属于类的对象上。

**示例**
```cpp
#include &lt;stdio.h&gt; 
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

class point1{
    int x;  //非静态成员变量占对象空间
};

class point2{
    int x;  //非静态成员变量占对象空间
    static int y;  //静态成员变量不占对象空间
    
    void fx(){  //函数也不占对象空间，所有函数共享一个函数实例
    }
    
    static void fy(){  //静态成员函数也不占对象空间
    }
};

int main(){
    cout&lt;&lt;sizeof(point1)&lt;&lt;endl;
    cout&lt;&lt;sizeof(point2)&lt;&lt;endl;
}
```

**注意**：`C++`编译器会给空类的对象分配一个字节，用于区分其存储空间。

---

#### 4.3.2 this指针概念

---

`C++`中成员变量和成员函数是分开存储的，每一个非静态成员函数只会产生一份函数实例，也就是说多个同类型的对象会共用一块代码。

那么**问题**是：这一块代码是如何区分哪个对象调用自己的呢？

`C++`通过提供特殊的对象指针，this指针，解决上述问题。**this指针指向被调用的成员函数所属的对象。**

**概念**

* this指针是隐含在每一个非静态成员函数内的一种指针
  * this指针不需要定义，直接使用即可

**用途**：

* 当形参和成员变量同名时，可用this指针来区分
  * 在类的非静态成员函数中返回对象本身，可使用`return *this`

**示例**
```cpp
#include &lt;stdio.h&gt; 
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

class point{
public:
    int x,y;
};
```

//1、当形参和成员变量同名时，可用this指针来区分
```c++
point(int x, int y) {
    this->x = x;
    this->y = y;
}

point& add(point p) {
    this->x += p.x;
    this->y += p.y;
    //返回对象本身
    return *this;
}
```

void test01() {
    point p1(1, 2);
    cout &lt;&lt; p1.x &lt;&lt; " " &lt;&lt; p1.y &lt;&lt; endl;
}

void test02() {
    point p2(1, 1);
    point p3(0, 0);
    p3.add(p2).add(p2).add(p2);
    cout &lt;&lt; p2.x &lt;&lt; " " &lt;&lt; p2.y &lt;&lt; endl;
}

int main() {
    test01();
    test02();
    return 0;
}
```

---

#### 4.3.3 空指针访问成员函数

---

`C++`中空指针也是可以调用成员函数的，但是也要注意有没有用到this指针。

如果用到this指针，需要加以判断保证代码的健壮性。

**示例：**
```c++
#include &lt;stdio.h&gt; 
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

class point {
public:
    int x, y;

    point(int a, int b) : x(a), y(b) {}

    void show_1() {
        cout &lt;&lt; "YES" &lt;&lt; endl;
    }

    void show_2() {
        cout &lt;&lt; x &lt;&lt; " " &lt;&lt; y &lt;&lt; endl;  //默认使用了this指针 
//      cout &lt;&lt; this-&gt;x &lt;&lt; this-&gt;y &lt;&lt; endl;  //与上一行等价
    }
};

int main() {
    point *p1 = NULL;

    p1-&gt;show_1();   //空指针，可以调用成员函数
    p1->show_2();   //但是如果成员函数中用到了this指针，就不可以了

    return 0;
}
```

---

#### 4.3.4 const修饰成员函数

---

**常函数：**

* 成员函数后加`const`后我们称为这个函数为**常函数**
  * 常函数内不可以修改成员属性
  * 成员属性声明时加关键字`mutable`后，在常函数中依然可以修改

**常对象：**

* 声明对象前加`const`称该对象为常对象
  * 常对象只能调用常函数

**示例：**
```c++
#include &lt;stdio.h&gt; 
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

class point {
public:
    int x;
    mutable int y;  //可修改 可变的
```

class point {
    //this指针的本质是一个指针常量，指针的指向不可修改
    //如果想让指针指向的值也不可以修改，需要声明常函数

    public:
        int x;

        point() {
            x = 10;
            y = 10;
        }

        void show_1() const {
            //const Type* const pointer;
            //this = NULL; //不能修改指针的指向 Person* const this;
            //this->mA = 100; //但是this指针指向的对象的数据是可以修改的

            //const修饰成员函数，表示指针指向的内存空间的数据不能修改，除了mutable修饰的变量

            this->y = 20;
            cout &lt;&lt; x &lt;&lt; " " &lt;&lt; y &lt;&lt; endl;
        }

        void show_2() {
            cout &lt;&lt; x &lt;&lt; " " &lt;&lt; y &lt;&lt; endl;
        }

    //      void show_no() const {
    //          this-&gt;x = 20;
    //      }

    private:
        int y;
};

int main() {
    point p1;

    p1.show_1();  //非常对象可以调用const函数

    const point p2;   //常量对象

    //  p2.x = 20;  //常对象不能修改成员变量的值,但是可以访问
    p2.y = 100;  //但是常对象可以修改mutable修饰成员变量

    //常对象访问成员函数
    p2.show_1();

    //  p2.show_2();  //常对象只能调用const函数

    return 0;
}

---

### 4.4 友元

---

生活中你的家有客厅(Public)，有你的卧室(Private)

客厅所有来的客人都可以进去，但是你的卧室是私有的，也就是说只有你能进去

但是呢，你也可以允许你的好闺蜜好基友进去。

在程序里，有些私有属性也想让类外特殊的一些函数或者类进行访问，就需要用到友元的技术

* 友元的目的就是让一个函数或者类访问另一个类中私有成员
* 友元的关键字为：`friend`

友元的三种实现

* 全局函数做友元
* 类做友元
* 成员函数做友元

---

#### 4.4.1 全局函数做友元

**示例**
```cpp
#include &lt;stdio.h&gt;
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

class point {
    friend void visit(point &p);  //声明友元函数

public:
    int x;

    point() {
        x = 10;
        y = 10;
    }

private:
    int y;
};

void visit(point &p) {
    cout &lt;&lt; p.x &lt;&lt; endl &lt;&lt; p.y &lt;&lt; endl;
}

int main() {
    point p1;
    visit(p1);
}
```

---

#### 4.4.2 类做友元

---

**示例**
```cpp

#include &lt;stdio.h&gt; 
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

class point{

friend class show; //声明友元类

public:
        int x;

point(){
            x=10;
            y=10;
        }

private:
        int y;

};

class show{

public:

point p1;

void visit(){
            cout&lt;&lt;p1.x&lt;&lt;" "&lt;&lt;p1.y&lt;&lt;endl;  //可以访问类point里的私有y
        }

};

int main(){

show s1;

s1.visit();

return 0;

}
```

---

#### 4.4.3 成员函数做友元

---

**示例**
```cpp

#include &lt;stdio.h&gt; 
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

class point;
class show
{
    public:
        show();
        void visit(); //让visit函数作为point的好朋友，可以访问point中私有内容

private:
        point *p;
};

class point
{
    //告诉编译器  show类中的visit成员函数 是point的好朋友，可以访问私有内容
    friend void show::visit();

public:
        point();

public:
        int x;
    private:
        int y;
};

point::point()
{
    this->x=10;
    this->y=10;
}

show::show()
{
    p = new point;
}

void show::visit()
{
    cout &lt;&lt; "好基友正在访问" &lt;&lt; p-&gt;x &lt;&lt; endl;
    cout &lt;&lt; "好基友正在访问" &lt;&lt; p-&gt;y &lt;&lt; endl;
}

void test01()
{
    show s;
    s.visit();
}

int main(){

test01();

return 0;
}
```

---

### 4.5 运算符重载

---

**运算符重载概念** ：利用`operator`对已有的运算符重新进行定义，赋予其另一种功能，以适应不同的数据类型

**本质** ：

* 提供一个`operator 运算符()`函数，使得`A operator 运算符(B)`的形式可以化简为`A 运算符 B`的形式

---

#### 4.5.1 加号/减号运算符重载

**作用** ：实现两个自定义数据类型相加的运算

**示例1**
```cpp
```

---

**修复内容汇总：**
1. 将所有代码块标记从 ` ```java ` 改为 ` ```cpp `（因为这是C++代码）
2. 修正错别字："可以**发**访问" → "可以**访问**"
3. 修正语句："是point好朋友" → "是point**的**好朋友"

```cpp
//成员函数实现 + / -号运算符重载
#include &lt;stdio.h&gt; 
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

class point{
    public:
        int x,y;

    point(){}

    point(int a,int b):x(a),y(b) {}

    point operator+(const point p){  //成员函数实现 + 号运算符重载
        point t;
        t.x=this->x+p.x;
        t.y=this->y+p.y;
        return t;
    }

    point operator-(const point p){  //成员函数实现 - 号运算符重载
        point t;
        t.x=this->x-p.x;
        t.y=this->y-p.y;
        return t;
    }

};

int main(){
    point p1(1,1);
    point p2(2,2);
    point p3=p2+p1;
    cout&lt;&lt;p3.x&lt;&lt;" "&lt;&lt;p3.y&lt;&lt;endl;
    p3=p2-p1;
    cout&lt;&lt;p3.x&lt;&lt;" "&lt;&lt;p3.y&lt;&lt;endl;
    return 0;
}
```

**示例2**
```cpp
//全局函数实现 + / -号运算符重载
#include &lt;stdio.h&gt; 
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

class point{
    public:
        int x,y;

    point(){}

    point(int a,int b):x(a),y(b){}
};

point operator+(const point &p1,const point &p2){  //全局函数实现 + 号运算符重载
    point t;
    t.x=p1.x+p2.x;
    t.y=p1.y+p2.y;
    return t;
}

point operator-(const point &p1,const point &p2){  //全局函数实现 - 号运算符重载
    point t;
    t.x=p1.x-p2.x;
    t.y=p1.y-p2.y;
    return t;
}

int main(){
    point p1(1,1);
    point p2(2,2);
    point p3=p1+p2;
    cout&lt;&lt;p3.x&lt;&lt;" "&lt;&lt;p3.y&lt;&lt;endl;
    p3=p2-p1;
    cout&lt;&lt;p3.x&lt;&lt;" "&lt;&lt;p3.y&lt;&lt;endl;
    return 0;
}
```

**总结**

* 对于内置的数据类型的表达式的运算符是不可能改变的
* 不要滥用运算符重载

---

#### 4.5.2 左移运算符重载

---

**作用**：可以输出自定义数据类型

---

**修复内容：**
1. 删除重复的"的"字："表达式的**的**运算符" → "表达式的运算符"
2. 示例2的代码块标记从 ````java` 改为 ````cpp`
3. 统一了代码缩进格式

**注意**：一般使用全局函数实现

**示例**
```cpp
// 全局函数实现输出运算符重载
#include &lt;stdio.h&gt; 
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

class point{
public:
    int x, y;

    point(){}

    point(int a, int b): x(a), y(b){}
};

// ostream对象只能有一个
ostream& operator&lt;&lt;(ostream &cout, point &p){
    cout &lt;&lt; p.x &lt;&lt; " " &lt;&lt; p.y &lt;&lt; endl;
    return cout; 
}

int main(){
    point p1(1, 1);

    cout &lt;&lt; p1 &lt;&lt; "链式输出" &lt;&lt; endl;

    return 0;
}
```

---

#### 4.5.3 递增运算符重载

---

**作用**：通过重载递增运算符，实现自己的整型数据

**示例**
```cpp
#include &lt;stdio.h&gt; 
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

class point{
public:
    int x, y;

    point(){}

    point(int a, int b): x(a), y(b){}

    // 前置递增 
    point& operator++(){
        this->x++;
        this->y++;
        return *this;
    }

    // 后置递增 
    point operator++(int){  // int用于占位 
        point temp = *this; // 先记录当前值
        this->x++;
        this->y++;
        return temp; // 返回递增前的值
    }
};

int main(){
    point p1(1, 1);

    p1++;

    ++p1;

    cout &lt;&lt; p1.x &lt;&lt; " " &lt;&lt; p1.y &lt;&lt; endl;

    return 0;
}
```

---

#### 4.5.4 赋值运算符重载

---

`C++`编译器至少给一个类添加4个函数

1. 默认构造函数(无参，函数体为空)
2. 默认析构函数(无参，函数体为空)
3. 默认拷贝构造函数，对属性进行值拷贝
4. 赋值运算符 `operator=`, 对属性进行值拷贝

如果类中有属性指向堆区，做赋值操作时也会出现深浅拷贝问题

**示例：**
```cpp
#include &lt;stdio.h&gt; 
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

class point{
public:
    int *x, *y;  // 开辟到堆区

    point(){
        x = new int(0);
        y = new int(0);
    }

    // 重载赋值运算符
    point& operator=(const point &p){
        // 先判断是否有属性在堆区，如果有，先释放干净，否则造成内存泄漏
        if(this->x != NULL || this->y != NULL){
            delete this->x;
            this->x = NULL;
            delete this->y;
            this->y = NULL;
        }

        // 深拷贝
        this->x = new int(*p.x);
        this->y = new int(*p.y);

        return *this;
    }

    ~point(){
        if(x != NULL){
            delete x;
            x = NULL;
        }
        if(y != NULL){
            delete y;
            y = NULL;
        }
    }
};

int main(){
    point p1;
    *p1.x = 10;
    *p1.y = 20;

    point p2;
    p2 = p1; // 调用赋值运算符重载

    cout &lt;&lt; "p2.x = " &lt;&lt; *p2.x &lt;&lt; " p2.y = " &lt;&lt; *p2.y &lt;&lt; endl;

    return 0;
}
```cpp
point(int a, int b) {
    x = new int(a);  // 将数据开辟到堆区
    y = new int(b);
}

// 重载赋值运算符
point& operator=(point& p) {
    if (this-&gt;x != NULL) {
        delete this->x;
        this->x = NULL;
    }
    if (this->y != NULL) {
        delete this->y;
        this->y = NULL;
    }

    // this->x = p.x;  // 编译器提供的代码是浅拷贝

    this->x = new int(*p.x);  // 提供深拷贝，解决浅拷贝的问题
    this->y = new int(*p.y);

    return *this;
}

~point() {
    if (this->x != NULL) {
        delete this->x;
        this->x = NULL;
    }
    if (this->y != NULL) {
        delete this->y;
        this->y = NULL;
    }
}
};

int main() {
    point p1(1, 1);
    point p2(2, 2);

    p1 = p2;

    cout &lt;&lt; *p1.x &lt;&lt; " " &lt;&lt; *p1.y &lt;&lt; endl;

    return 0;
}
```

---

#### 4.5.5 关系运算符重载

---

**作用：** 重载关系运算符，可以让两个自定义类型对象进行对比操作。

**示例：**
```cpp
#include &lt;stdio.h&gt; 
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

class point {
public:
    int x, y;

    point(int a, int b) : x(a), y(b) {}

    bool operator==(const point& p) {
        if (this->x == p.x && this->y == p.y) return 1;
        else return 0;
    }
};

int main() {
    point p1(1, 1);
    point p2(2, 2);

    if (p1 == p2) cout &lt;&lt; "YES" &lt;&lt; endl;
    else cout &lt;&lt; "NO" &lt;&lt; endl;

    return 0;
}
```

---

#### 4.5.6 函数调用运算符重载

---

**特点**

* 函数调用运算符 `()` 也可以重载。
  * 由于重载后使用的方式非常像函数的调用，因此称为仿函数。
  * 仿函数没有固定写法，非常灵活。

**示例：**
```cpp
```cpp
#include &lt;stdio.h&gt;
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

class print {
public:
    void operator()(auto s) { // 重载的 () 操作符，也称为仿函数
        cout &lt;&lt; s &lt;&lt; endl;
    }
};

class add {
public:
    int operator()(int a, int b) {
        return a + b;
    }
};

void test01() {
    print p;
    p("lys is dog");
}

void test02() {
    add a;
    cout &lt;&lt; a(1, 2) &lt;&lt; endl;
}

int main() {
    test01();
    test02();
    return 0;
}
```

---

### 4.6 继承

**继承是面向对象三大特性之一。**

我们发现，定义这些类时，下级的成员除了拥有上级的共性，还有自己的特性。这个时候我们就可以考虑利用继承的技术，减少重复代码。

**定义和概念**

继承是类的重要特性。A类继承B类，我们称B类为“基类”，A类为“派生类”。A类继承了B类之后，A类就具有了B类的部分成员，具体得到了哪些成员，这由两个方面决定：
* 继承方式
* 基类成员访问权限

---

#### 4.6.1 继承的基本语法

**基本语法**：`class A : public B`

* `A` 类称为**派生类**。
* `B` 类称为**基类**。

**示例**：对于一个人来说，有姓名、年龄、性别这些基本特征，而像是职位之类的特征则是因人而异的特征。在创建“人”的类的时候，我们可以通过继承的技术，减少对基本特征的定义等操作的代码。

**普通实现：**
```cpp
#include &lt;stdio.h&gt;
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

// 学生类
class student {
public:
    string name, sex;
    int year;

    student(string n, int x, string s) : name(n), year(x), sex(s) {}

    void show_name() {
        cout &lt;&lt; "名字：" &lt;&lt; name &lt;&lt; endl;
    }

    void show_year() {
        cout &lt;&lt; "年龄：" &lt;&lt; year &lt;&lt; endl;
    }

    void show_sex() {
        if (sex == "boy") {
            cout &lt;&lt; "性别：男" &lt;&lt; endl;
        } else {
            cout &lt;&lt; "性别：女" &lt;&lt; endl;
        }
    }
};
```cpp
class student {
public:
    string name, sex;
    int year;

    student(string n, int x, string s) : name(n), year(x), sex(s) {}

    void show_name() {
        cout &lt;&lt; "名字：" &lt;&lt; name &lt;&lt; endl;
    }

    void show_year() {
        cout &lt;&lt; "年龄：" &lt;&lt; year &lt;&lt; endl;
    }

    void show_sex() {
        if (sex == "boy") {
            cout &lt;&lt; "性别：男" &lt;&lt; endl;
        } else {
            cout &lt;&lt; "性别：女" &lt;&lt; endl;
        }
    }

    void show_position() {
        cout &lt;&lt; "是一个学生" &lt;&lt; endl;
    }
};

//家长类
class parent {
public:
    string name, sex;
    int year;

    parent(string n, int x, string s) : name(n), year(x), sex(s) {}

    void show_name() {
        cout &lt;&lt; "名字：" &lt;&lt; name &lt;&lt; endl;
    }

    void show_year() {
        cout &lt;&lt; "年龄：" &lt;&lt; year &lt;&lt; endl;
    }

    void show_sex() {
        if (sex == "boy") {
            cout &lt;&lt; "性别：男" &lt;&lt; endl;
        } else {
            cout &lt;&lt; "性别：女" &lt;&lt; endl;
        }
    }

    void show_position() {
        cout &lt;&lt; "是一名家长" &lt;&lt; endl;
    }
};

//教师类
class teacher {
public:
    string name, sex;
    int year;

    teacher(string n, int x, string s) : name(n), year(x), sex(s) {}

    void show_name() {
        cout &lt;&lt; "名字：" &lt;&lt; name &lt;&lt; endl;
    }

    void show_year() {
        cout &lt;&lt; "年龄：" &lt;&lt; year &lt;&lt; endl;
    }

    void show_sex() {
        if (sex == "boy") {
            cout &lt;&lt; "性别：男" &lt;&lt; endl;
        } else {
            cout &lt;&lt; "性别：女" &lt;&lt; endl;
        }
    }

    void show_position() {
        cout &lt;&lt; "是一位老师" &lt;&lt; endl;
    }
};

int main() {
    //学生对象
    student s1("lys", 20, "boy");
    s1.show_name();
    s1.show_year();
    s1.show_position();
    cout &lt;&lt; endl;

    //家长对象
    parent p1("mama", 40, "girl");
    p1.show_name();
    p1.show_year();
    p1.show_position();
    cout &lt;&lt; endl;

    //教师对象
    teacher t1("yxc", 30, "boy");
    t1.show_name();
    t1.show_year();
    t1.show_position();
    cout &lt;&lt; endl;

    return 0;
}
```cpp
#include &lt;stdio.h&gt;
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

// 用于继承的基类
class person {
public:
    string name, sex;
    int year;

    person(string n, int x, string s) : name(n), year(x), sex(s) {}

    void show_name() {
        cout &lt;&lt; "名字：" &lt;&lt; name &lt;&lt; endl;
    }

    void show_year() {
        cout &lt;&lt; "年龄：" &lt;&lt; year &lt;&lt; endl;
    }

    void show_sex() {
        if (sex == "boy") {
            cout &lt;&lt; "性别：男" &lt;&lt; endl;
        } else {
            cout &lt;&lt; "性别：女" &lt;&lt; endl;
        }
    }
};

// 学生类
class student : public person {
public:
    student(string n, int x, string s) : person(n, x, s) {}

    void show_position() {
        cout &lt;&lt; "是一个学生" &lt;&lt; endl;  // 因人而异的特征
    }
};

// 家长类
class parent : public person {
public:
    parent(string n, int x, string s) : person(n, x, s) {}

    void show_position() {
        cout &lt;&lt; "是一名家长" &lt;&lt; endl;
    }
};

// 教师类
class teacher : public person {
public:
    teacher(string n, int x, string s) : person(n, x, s) {}

    void show_position() {
        cout &lt;&lt; "是一位老师" &lt;&lt; endl;
    }
};

int main() {
    // 学生对象
    student s1("lys", 20, "boy");
    s1.show_name();
    s1.show_year();
    s1.show_position();
    cout &lt;&lt; endl;

    // 家长对象
    parent p1("mama", 40, "girl");
    p1.show_name();
    p1.show_year();
    p1.show_position();
    cout &lt;&lt; endl;

    // 教师对象
    teacher t1("yxc", 30, "boy");
    t1.show_name();
    t1.show_year();
    t1.show_position();
    cout &lt;&lt; endl;

    return 0;
}

/*
 * 总结：
 * - 继承的好处：可以减少重复的代码
 * - 通过公共继承，子类自动获得父类的成员和方法
 * - 子类可以添加自己的特有成员和重写父类的方法
 */
```

**修复内容说明：**
1. **格式规范化**：统一了缩进和空格，使代码结构更清晰易读。
2. **注释修正**：将“//用于继承的类”改为“// 用于继承的基类”，使注释更准确。
3. **条件语句格式**：将 `if` 和 `else` 的代码块用大括号 `{}` 包裹，提高代码可读性和可维护性。
4. **主函数格式**：调整了 `main` 函数内部的代码格式，添加了适当的空行和注释。
5. **总结部分格式**：将总结内容放在代码块后的注释中，使用列表形式更清晰。

代码功能保持不变，但格式更加规范和易读。

派生类中的成员，包含两大部分：

- 一类是**从基类继承过来的**（基本特征）。
- 一类是**自己增加的成员**（因人而异的特征）。

**从基类继承过来的体现其共性，而新增的成员体现了其个性。**

---

#### 4.6.2 继承方式

---

继承的语法：`class 派生类 : 继承方式 基类`

**继承方式一共有三种：**

- 公共继承
- 保护继承
- 私有继承

**示例1 公共继承：**

```cpp
#include &lt;stdio.h&gt; 
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

class point{
    public:
        int x;

    protected:
        int y;

    private:
        int z;
};

//公共继承
class point_Pub:public point{
    public:
        //类内 
        point_Pub(){
            x=10;  //可访问 public权限
            y=20;  //可访问 protected权限
            //z=30;  //不可访问 private权限 
        }

        void show(){
            cout&lt;&lt;"x = "&lt;&lt;x&lt;&lt;endl;
            cout&lt;&lt;"y = "&lt;&lt;y&lt;&lt;endl;
        }
};

int main(){
    point_Pub p1;
    p1.show();

    //类外 
    cout&lt;&lt;"p1.x = "&lt;&lt;p1.x&lt;&lt;endl;  //只能访问到公共权限
    //cout&lt;&lt;"p1.y = "&lt;&lt;p1.y&lt;&lt;endl;
    //cout&lt;&lt;"p1.z = "&lt;&lt;p1.z&lt;&lt;endl;

    return 0;
}
```

**示例2 保护继承：**

```cpp
#include &lt;stdio.h&gt; 
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

class point{
    public:
        int x;

    protected:
        int y;

    private:
        int z;
};

//保护继承
class point_Pro:protected point{
    public:
        //类内 
        point_Pro(){
            x=10;  //可访问原来的 public权限,但此时x已经变成了protected权限 
            y=20;  //可访问 protected权限
            //z=30;  //不可访问 private权限 
        }

        void show(){
            cout&lt;&lt;"x = "&lt;&lt;x&lt;&lt;endl;
            cout&lt;&lt;"y = "&lt;&lt;y&lt;&lt;endl;
        }
};
```cpp
#include &lt;iostream&gt;
using namespace std;

class point {
public:
    int x;
protected:
    int y;
private:
    int z;
};

// 保护继承
class point_Pro : protected point {
public:
    // 类内
    point_Pro() {
        x = 10;  // 可访问原来的 public 权限，但此时 x 已经变成了 protected 权限
        y = 20;  // 可访问原来的 protected 权限，但此时 y 已经变成了 protected 权限
        // z = 30;  // 不可访问 private 权限
    }

    void show() {
        cout &lt;&lt; "x = " &lt;&lt; x &lt;&lt; endl;
        cout &lt;&lt; "y = " &lt;&lt; y &lt;&lt; endl;
    }
};

int main() {
    point_Pro p1;
    p1.show();

    // 类外
    // cout &lt;&lt; "p1.x = " &lt;&lt; p1.x &lt;&lt; endl;  // 不可访问，原有的 public 权限变为了 protected 权限
    // cout &lt;&lt; "p1.y = " &lt;&lt; p1.y &lt;&lt; endl;  // 不可访问，原有的 protected 权限变为了 protected 权限
    // cout &lt;&lt; "p1.z = " &lt;&lt; p1.z &lt;&lt; endl;

    return 0;
}
```

**示例3 私有继承**
```cpp
#include &lt;iostream&gt;
using namespace std;

class point {
public:
    int x;
protected:
    int y;
private:
    int z;
};

// 私有继承
class point_Pri : private point {
public:
    // 类内
    point_Pri() {
        x = 10;  // 可访问原来的 public 权限，但此时 x 已经变成了 private 权限
        y = 20;  // 可访问原来的 protected 权限，但此时 y 已经变成了 private 权限
        // z = 30;  // 不可访问 private 权限
    }

    void show() {
        cout &lt;&lt; "x = " &lt;&lt; x &lt;&lt; endl;
        cout &lt;&lt; "y = " &lt;&lt; y &lt;&lt; endl;
    }
};

int main() {
    point_Pri p1;
    p1.show();

    // 类外
    // cout &lt;&lt; "p1.x = " &lt;&lt; p1.x &lt;&lt; endl;  // 不可访问，原有的 public 权限变为了 private 权限
    // cout &lt;&lt; "p1.y = " &lt;&lt; p1.y &lt;&lt; endl;  // 不可访问，原有的 protected 权限变为了 private 权限
    // cout &lt;&lt; "p1.z = " &lt;&lt; p1.z &lt;&lt; endl;

    return 0;
}
```

---

#### 4.6.3 继承中的对象模型

---

**问题：** 从基类继承过来的成员，哪些属于派生类对象中？

**示例：**
```cpp
#include &lt;iostream&gt;
using namespace std;

class point {
public:
    int x;
protected:
    int y;
private:
    int z; // 私有成员只是被隐藏了，但是还是会继承下去
    static int l;
};

class point_son : public point {
public:
    int m;
};

int main() {
    cout &lt;&lt; sizeof(point_son) &lt;&lt; endl;  // 大小为 16
    // 说明所有基类的非静态成员全部继承了下来
    return 0;
}
```

**结论**：基类中私有成员也被派生类继承了，只是由编译器隐藏后访问不到。

---

#### 4.6.4 继承中的对象赋值关系

---

**特点**

* 派生类对象可以赋值给基类的对象/基类的指针/基类的引用
  * 基类的指针可以通过强制类型转换赋值给派生类的指针。但是必须是基类的指针是指向派生类对象时才是安全的。

**示例**
```cpp
#include &lt;stdio.h&gt; 
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

class point{
public:
    int x, y;

    point(int a, int b): x(a), y(b){}
};

class point_son: public point{
public:
    int s_x = 10;

    point_son(int a, int b): point(a, b){}
};

void test01(){
    point_son s1(1, 1);

    point p1 = s1;  // 派生类对象可以赋值给基类对象 
    cout &lt;&lt; p1.x &lt;&lt; " " &lt;&lt; p1.y &lt;&lt; endl;

    point *p2 = &s1;  // 派生类对象可以赋值给基类指针 
    cout &lt;&lt; p2-&gt;x &lt;&lt; " " &lt;&lt; p2-&gt;y &lt;&lt; endl;

    point &p3 = s1;  // 派生类对象可以赋值给基类引用 
    cout &lt;&lt; p3.x &lt;&lt; " " &lt;&lt; p3.y &lt;&lt; endl;
}

void test02(){
    point p1(1, 1);

    // 基类对象不能赋值给派生类对象 
    // point_son s1 = p1;

    // 基类的指针可以通过强制类型转换赋值给派生类的指针
    point *p2 = &p1;      
    point_son *s2 = (point_son*)p2;  // 此情况可以转换

    // 派生类的指针不可以指向基类的指针，同引用 
    // point_son *s3 = &p1;
    // point_son &s3 = p2;

    // 派生类的对象所占的存储空间通常要比基类的对象大
    // 原因就是派生类除了继承基类的成员之外，还拥有自己的成员
    /* 所以基类的指针操作派生类的对象时，
    由于基类指针会向操作基类对象那样操作派生类对象，
    而基类对象所占用的内存空间通常小于派生类对象，
    所以基类指针不会超出派生类对象去操作数据 */
}

int main(){
    test01();
    test02();
    return 0;
}
```

---

#### 4.6.5 继承中构造和析构顺序

---

派生类继承基类后，当创建派生类对象，也会调用基类的构造函数。

**问题**：基类和派生类的构造和析构顺序是谁先谁后？

**示例**：
```cpp
#include &lt;stdio.h&gt; 
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

class point{
public:
    int x;
```cpp
point(int a):x(a){
            cout &lt;&lt; "基类的构造函数调用" &lt;&lt; endl;
        }

~point(){
            cout &lt;&lt; "基类的析构函数调用" &lt;&lt; endl;      
        }
};

class point_son:public point{
    public:
        point_son(int a):point(a){
            cout &lt;&lt; "派生类的构造函数调用" &lt;&lt; endl;
        }

~point_son(){
            cout &lt;&lt; "派生类的析构函数调用" &lt;&lt; endl;
        }
};

int main(){

    point_son p1(10);
    //继承中 先调用基类的构造函数，再调用派生类的构造函数，析构顺序与构造相反

    return 0;

}
```

**总结**：继承中，先调用基类的构造函数，再调用派生类的构造函数，析构顺序与构造顺序相反。

---

#### 4.6.6 继承同名成员处理方式

---

**问题**：当派生类与基类出现同名的成员，如何通过派生类对象，访问到派生类或基类中同名的数据呢？

* 访问派生类同名成员，直接访问即可。
* 访问基类同名成员，需要加作用域。

**示例：**
```cpp
#include &lt;stdio.h&gt; 
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

class point{

public:
        int x = 20;

void show(){
            cout &lt;&lt; "基类void show()的函数调用" &lt;&lt; endl;
        }

};

class point_son:public point{
    public:
        //当派生类与基类拥有同名的成员变量，派生类会隐藏基类中所有同名的成员变量 
        int x = 10;

//当派生类与基类拥有同名的成员函数，派生类会隐藏基类中所有版本的同名成员函数
        void show(){
            cout &lt;&lt; "子类void show()的函数调用" &lt;&lt; endl;
        }
};

int main(){

    point_son s1;

    cout &lt;&lt; "子类point_son下的x = " &lt;&lt; s1.x &lt;&lt; endl;   
    cout &lt;&lt; "基类point下的x = " &lt;&lt; s1.point::x &lt;&lt; endl;  //如果想访问基类中被隐藏的同名成员变量，需要加基类的作用域

    s1.show();
    s1.point::show();  //如果想访问基类中被隐藏的同名成员函数，需要加基类的作用域

    return 0;

}
```

**总结**：

1. 派生类对象可以直接访问到派生类中同名成员。
2. 派生类对象加作用域可以访问到基类同名成员。
3. 当派生类与基类拥有同名的成员函数，派生类会隐藏基类中同名成员函数，加作用域可以访问到基类中同名函数。

---

#### 4.6.7 继承同名静态成员处理方式

---

**问题**：继承中同名的静态成员在派生类对象上如何进行访问？

静态成员和非静态成员出现同名，处理方式一致

* 访问派生类同名成员 直接访问即可
  * 访问基类同名成员 需要加作用域

**示例：**
```cpp
#include &lt;stdio.h&gt; 
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

class point{
    public:
        static int x;
        static void show(){
            cout&lt;&lt;"基类静态成员函数的调用"&lt;&lt;endl; 
        }
};

class point_son:public point{
    public:
        static int x;
        static void show(){
            cout&lt;&lt;"派生类静态成员函数的调用"&lt;&lt;endl; 
        }   
};

int point::x=20;
int point_son::x=10;

//通过对象访问
void test01(){
    cout&lt;&lt;"通过对象访问"&lt;&lt;endl;
    point_son p1;
    cout&lt;&lt;"子类point_son下的x = "&lt;&lt;p1.x&lt;&lt;endl;
    cout&lt;&lt;"基类point下的x = "&lt;&lt;p1.point::x&lt;&lt;endl;
    p1.show();
    p1.point_son::show();
}

//通过类名访问
void test02(){
    cout&lt;&lt;"通过类名访问"&lt;&lt;endl;
    cout&lt;&lt;"子类point_son下的x = "&lt;&lt;point_son::x&lt;&lt;endl;
    cout&lt;&lt;"基类point下的x = "&lt;&lt;point::x&lt;&lt;endl;
    point::show();
    point_son::show();
    point_son::point::show();  //出现同名，派生类会隐藏掉基类中所有同名成员函数，需要加作用域访问
}

int main(){
    test01();
    cout&lt;&lt;endl;
    test02();
    return 0;
}
```

**总结** ：同名静态成员处理方式和非静态处理方式一样，只不过有两种访问的方式（通过对象 和 通过类名）

---

#### 4.6.8 多继承语法

---

`C++`允许**一个类继承多个类**

**语法** ：` class 派生类 ：继承方式 基类1 ， 继承方式 基类2...`

**注意** ：多继承可能会引发基类中有同名成员出现，需要加作用域区分

**`C++`实际开发中不建议用多继承**

**示例：**
```cpp
#include &lt;stdio.h&gt; 
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

class point_1{
    public:
        int x=10;
        point_1(){
            cout&lt;&lt;"point_1的构造函数调用"&lt;&lt;endl;
        }
```cpp
#include &lt;iostream&gt;
#include &lt;string&gt;
using namespace std;

class point_1 {
public:
    int x = 10;

    point_1() {
        cout &lt;&lt; "point_1的构造函数调用" &lt;&lt; endl;
    }

    ~point_1() {
        cout &lt;&lt; "point_1的析构函数调用" &lt;&lt; endl;
    }
};

class point_2 {
public:
    int x = 20;

    point_2() {
        cout &lt;&lt; "point_2的构造函数调用" &lt;&lt; endl;
    }

    ~point_2() {
        cout &lt;&lt; "point_2的析构函数调用" &lt;&lt; endl;
    }
};

// 语法：class 派生类 : 继承方式 基类1, 继承方式 基类2
class point_son : public point_1, public point_2 {
public:
    int x = 30;

    point_son() {
        cout &lt;&lt; "point_son的构造函数调用" &lt;&lt; endl;
    }

    ~point_son() {
        cout &lt;&lt; "point_son的构造函数调用" &lt;&lt; endl;
    }
};

int main() {
    // 多继承容易产生成员同名的情况
    // 通过使用类名作用域可以区分调用哪一个基类的成员
    point_son s1;

    cout &lt;&lt; "point_1下的x = " &lt;&lt; s1.point_1::x &lt;&lt; endl;
    cout &lt;&lt; "point_2下的x = " &lt;&lt; s1.point_2::x &lt;&lt; endl;
    cout &lt;&lt; "point_son下的x = " &lt;&lt; s1.x &lt;&lt; endl;

    return 0;
}
```

**总结**：多继承中如果基类中出现了同名情况，派生类使用时要加作用域。

---

#### 4.6.9 菱形继承

---

**菱形继承概念：**

* 两个派生类继承同一个基类
* 又有某个类同时继承这两个派生类

这种继承被称为菱形继承，或者钻石继承。

**典型的菱形继承案例：**

* 先创建一个 `person` 类作为基类
* 再创建两个 `person` 的派生类：`father` 类和 `mother` 类
* 最后创建一个 `son` 类同时继承 `father` 类和 `mother` 类

**菱形继承问题：**

1. `father` 继承了 `person` 的数据，`mother` 同样继承了 `person` 的数据，当 `son` 使用数据时，就会产生二义性。
2. `son` 继承自 `person` 的数据有两份，但通常我们只需要一份。

**示例：**

```cpp
#include &lt;iostream&gt;
#include &lt;string&gt;
using namespace std;

class person {
public:
    int year;
    string sex;
};

class father : public person {
public:
    string name;
};

class mother : public person {
public:
    string name;
};
```cpp
class son : public father, public mother {
public:
    string name;
};

int main() {
    son s1;

    s1.father::sex = "男";
    s1.father::year = 40;
    s1.father::name = "baba";

    s1.mother::sex = "女";
    s1.mother::year = 38;
    s1.mother::name = "mama";

    // 实际需要的数据
    // s1.son::year = 20;
    // s1.son::sex = "Dog";
    s1.son::name = "lys";

    // s1同时继承了father类和mother类的数据，造成了二义性和资源浪费

    cout &lt;&lt; "father: " &lt;&lt; s1.father::name &lt;&lt; endl &lt;&lt; "性别: " &lt;&lt; s1.father::sex &lt;&lt; endl &lt;&lt; "年龄: " &lt;&lt; s1.father::year &lt;&lt; endl;
    cout &lt;&lt; endl;

    cout &lt;&lt; "mother: " &lt;&lt; s1.mother::name &lt;&lt; endl &lt;&lt; "性别: " &lt;&lt; s1.mother::sex &lt;&lt; endl &lt;&lt; "年龄: " &lt;&lt; s1.mother::year &lt;&lt; endl;
    cout &lt;&lt; endl;

    // cout &lt;&lt; "son: " &lt;&lt; s1.name &lt;&lt; endl &lt;&lt; "性别: " &lt;&lt; s1.sex &lt;&lt; endl &lt;&lt; "年龄: " &lt;&lt; s1.year &lt;&lt; endl;  // 保留了两份数据，产生了二义性
    cout &lt;&lt; "son: " &lt;&lt; s1.name &lt;&lt; endl;
    cout &lt;&lt; endl;

    return 0;
}
```

**解决** ：以上菱形继承带来的问题可以使用**虚继承** 的技术来解决

**关键字** ：`virtual`

**示例**

```cpp
#include &lt;stdio.h&gt; 
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

class person {
    public:
        int year;
        string sex;
};

// 继承前加virtual关键字后，变为虚继承
// 此时公共的基类person称为虚基类
class father : virtual public person {
    public:
        string name;
};

class mother : virtual public person {
    public:
        string name;
};

class son : public father, public mother {
    public:
        string name;
};

int main() {
    son s1;

    s1.father::sex = "男"; 
    s1.father::year = 40;
    s1.father::name = "baba";

    s1.mother::sex = "女"; 
    s1.mother::year = 38;
    s1.mother::name = "mama";
```cpp
// 实际需要的数据
s1.son::year = 20;
s1.son::sex = "Dog";
s1.son::name = "lys";
// s1现在只保留最后初始化的一份数据

cout &lt;&lt; "father: " &lt;&lt; s1.father::name &lt;&lt; endl &lt;&lt; "性别： " &lt;&lt; s1.father::sex &lt;&lt; endl &lt;&lt; "年龄: " &lt;&lt; s1.father::year &lt;&lt; endl;
cout &lt;&lt; endl;

cout &lt;&lt; "mother: " &lt;&lt; s1.mother::name &lt;&lt; endl &lt;&lt; "性别： " &lt;&lt; s1.mother::sex &lt;&lt; endl &lt;&lt; "年龄: " &lt;&lt; s1.mother::year &lt;&lt; endl;
cout &lt;&lt; endl;

cout &lt;&lt; "son: " &lt;&lt; s1.name &lt;&lt; endl &lt;&lt; "性别： " &lt;&lt; s1.sex &lt;&lt; endl &lt;&lt; "年龄: " &lt;&lt; s1.year &lt;&lt; endl;
cout &lt;&lt; endl;

return 0;
```

**总结**：

* 菱形继承带来的主要问题是派生类继承两份相同的数据，导致资源浪费以及毫无意义
  * 利用虚继承可以解决菱形继承问题

---

### 4.7 多态

---

#### 4.7.1 多态的基本概念

---

**多态是 `C++` 面向对象三大特性之一**

多态分为两类

* **静态多态**：函数重载和运算符重载属于静态多态，复用函数名
* **动态多态**：派生类和虚函数实现运行时多态

静态多态和动态多态**区别**：

* 静态多态的函数地址早绑定——编译阶段确定函数地址
* 动态多态的函数地址晚绑定——运行阶段确定函数地址

**多态满足条件**：

* 有继承关系
* 派生类重写基类中的虚函数

**多态使用条件**：

* 基类指针或引用指向派生类对象

**重写**：函数返回值类型、函数名、参数列表完全一致称为重写

**示例**
```cpp
#include &lt;stdio.h&gt;
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

class person {
public:
    void show() {
        cout &lt;&lt; "是一个人" &lt;&lt; endl;
    }
};

class male : public person {
public:
    void show() {
        cout &lt;&lt; "是一个男人" &lt;&lt; endl;
    }
};

class female : public person {
public:
    void show() {
        cout &lt;&lt; "是一个女人" &lt;&lt; endl;
    }
};

// 静态多态的函数地址早绑定，编译阶段已经确定了函数地址
void show_sex(person &p) {
    p.show();  // 调用person的show()函数
}

int main() {
    male m1;
    show_sex(m1);  // 本意是想根据对象的不同调用相应的show()函数

    female f1;
    show_sex(f1);

    return 0;
}
```

---

**主要修改**：
1. 代码语言标记从 `java` 改为 `cpp`
2. 统一了代码缩进格式
3. 修正了标点符号（破折号代替连字符等）
4. 调整了列表项的缩进层级

}
```cpp

**虚函数实现**
```cpp

#include &lt;stdio.h&gt; 
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

class person{
    public:
        //函数前面加上virtual关键字，变成虚函数，那么编译器在编译的时候就不能确定函数调用了
        virtual void show(){
            cout &lt;&lt; "是一个人" &lt;&lt; endl;
        }
};

class male:public person{
    public:
        virtual void show(){  //重写的函数virtual可加可不加 
            cout &lt;&lt; "是一个男人" &lt;&lt; endl;
        }
};

class female:public person{
    public:
        void show(){
            cout &lt;&lt; "是一个女人" &lt;&lt; endl;
        }
};

//动态多态的函数地址晚绑定  运行阶段才会确定函数地址
void show_sex(person &p){
    p.show();  //调用对应的show()函数
}

int main(){
    //调用传入对象的函数
    //如果函数地址在编译阶段就能确定，那么静态联编
    //如果函数地址在运行阶段才能确定，就是动态联编

    male m1;
    show_sex(m1);

    female f1;
    show_sex(f1);

    return 0;
}
```

**多态的优点**：

*   代码组织结构清晰
*   可读性强
*   利于前期和后期的扩展维护

**示例**
```cpp

#include &lt;stdio.h&gt; 
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

//抽象计算器类
//多态优点：代码组织结构清晰，可读性强，利于前期和后期的扩展维护
class base{
    public:
        int x, y;

        virtual int calculate(){
            return 0;
        }
};

//加法计算器
class add:public base{
    public:
        int calculate(){
            return x + y;
        }
};

//减法计算器
class sub:public base{
    public:
        int calculate(){
            return x - y;
        }
};

//乘法计算器
class mul:public base{
    public:
        int calculate(){
            return x * y;
        }
};

int main(){
    // 示例用法：创建对象，设置成员变量值，调用虚函数
    // ... （此处代码未提供完整，保持原样）
    return 0;
}
```cpp
// 基类指针指向派生类对象的加法计算器
add a;
base *b1 = &a;
b1->x = 10;
b1->y = 20;
cout &lt;&lt; b1-&gt;calculate() &lt;&lt; endl;

// 基类引用指向派生类对象的减法计算器
sub s;
base &b2 = s;
b2.x = 10;
b2.y = 20;
cout &lt;&lt; b2.calculate() &lt;&lt; endl;

// 堆区开辟基类指针指向派生类的乘法计算器
base *b3 = new mul;
b3-&gt;x = 10;
b3->y = 20;
cout &lt;&lt; b3-&gt;calculate() &lt;&lt; endl;
delete b3;

return 0;
}
```

**总结**：C++ 开发提倡利用多态设计程序架构，因为多态优点很多。

---

#### 4.7.2 纯虚函数和抽象类

---

在多态中，通常基类中虚函数的实现是毫无意义的，主要都是调用派生类重写的内容。可以将虚函数改为**纯虚函数**。

**纯虚函数语法**：`virtual 返回值类型 函数名（参数列表）= 0;`

当类中有了纯虚函数，这个类也称为**抽象类**（只要有一个函数是纯虚函数，就是抽象类）。

**抽象类特点**：
- 无法实例化对象。
- 派生类必须重写抽象类中的纯虚函数，否则也属于抽象类。

**示例**：
```cpp
#include &lt;stdio.h&gt;
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

class point {
public:
    int x, y;

    // 纯虚函数
    // 类中只要有一个纯虚函数就称为抽象类
    virtual void show() = 0;
};

class point_son_1 : public point {
public:
    // 未重写纯虚函数，point_son_1 仍是抽象类
};

class point_son_2 : public point {
public:
    void show() {
        cout &lt;&lt; x &lt;&lt; " " &lt;&lt; y &lt;&lt; endl;
    }
};

void test01() {
    // point p1;          // 抽象类不能实例化对象
    // point_son_1 s1;    // 未重写纯虚函数，仍被视为抽象类，不能实例化
}

void test02() {
    point_son_2 s2;
    s2.x = 10;
    s2.y = 20;
    s2.show();

    point &p2 = s2;
    p2.show();

    point *p3 = new point_son_2;
    p3-&gt;x = 10;
    p3->y = 20;
    p3->show();
    delete p3; // 注意释放内存
}

int main() {
    test01();
    test02();
    return 0;
}
```

---

#### 4.7.3 虚析构和纯虚析构

---

多态使用时，如果**派生类中有属性开辟到堆区**，那么**基类指针**在**释放时**无法调用到派生类的析构代码。

**解决方式**：将基类中的析构函数改为**虚析构**或者**纯虚析构**

**虚析构和纯虚析构共性：**

* 可以解决基类指针释放派生类对象
* 都需要有具体的函数实现

**虚析构和纯虚析构区别：**

* 如果是纯虚析构，该类属于抽象类，无法实例化对象

**虚析构语法：**

`virtual ~类名(){}`

**纯虚析构语法：**

```cpp
virtual ~类名() = 0;
类名::~类名() {}
```

**示例：**

```cpp
#include &lt;stdio.h&gt;
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

class person {
public:
    person() {
        cout &lt;&lt; "person的构造函数调用" &lt;&lt; endl;
    }

    virtual void show() = 0;

    ~person() {
        cout &lt;&lt; "person的析构函数调用" &lt;&lt; endl;
    }
};

class student : public person {
public:
    string *name;

    student(string s) {
        cout &lt;&lt; "student的构造函数调用" &lt;&lt; endl;
        name = new string(s);
    }

    void show() {
        cout &lt;&lt; *name &lt;&lt; " is dog " &lt;&lt; endl;
    }

    ~student() {
        cout &lt;&lt; "student的析构函数调用" &lt;&lt; endl;
        if (name != NULL) {
            delete name;
            name = NULL;
        }
    }
};

int main() {
    person *p = new student("lys");
    p-&gt;show();

    // 通过基类指针去释放，会导致派生类对象可能清理不干净，造成内存泄漏
    delete p;

    return 0;
}
```

**解决方法1 将基类函数的析构函数改为虚析构**

```cpp
#include &lt;stdio.h&gt;
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

class person {
public:
    person() {
        cout &lt;&lt; "person的构造函数调用" &lt;&lt; endl;
    }

    virtual void show() = 0;

    // 利用虚析构函数解决基类释放派生类对象时不彻底的问题
    virtual ~person() {
        cout &lt;&lt; "person的虚析构函数调用" &lt;&lt; endl;
    }
};
```
class student : public person {
public:
    string *name;

    student(string s) {
        cout &lt;&lt; "student的构造函数调用" &lt;&lt; endl;
        name = new string(s);
    }

    void show() {
        cout &lt;&lt; *name &lt;&lt; " is dog " &lt;&lt; endl;
    }

    ~student() {
        cout &lt;&lt; "student的析构函数调用" &lt;&lt; endl;
        if (name != NULL) {
            delete name;
            name = NULL;
        }
    }
};

int main() {
    person *p = new student("lys");
    p-&gt;show();

    delete p;

    return 0;
}
```

**解决方法2 利用纯虚析构函数的方法**
```cpp
#include &lt;stdio.h&gt; 
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
using namespace std;

class person {
public:
    person() {
        cout &lt;&lt; "person的构造函数调用" &lt;&lt; endl;
    }

    virtual void show() = 0;

    //纯虚析构函数 
    virtual ~person() = 0;
};

//纯虚析构函数需要实现 可以将基类中开辟的数据释放 
person::~person() {
    cout &lt;&lt; "person的纯虚析构函数调用" &lt;&lt; endl;
}

class student : public person {
public:
    string *name;

    student(string s) {
        cout &lt;&lt; "student的构造函数调用" &lt;&lt; endl;
        name = new string(s);
    }

    void show() {
        cout &lt;&lt; *name &lt;&lt; " is dog " &lt;&lt; endl;
    }

    ~student() {
        cout &lt;&lt; "student的析构函数调用" &lt;&lt; endl;
        if (name != NULL) {
            delete name;
            name = NULL;
        }
    }
};

int main() {
    person *p = new student("lys");
    p-&gt;show();

    delete p;

    return 0;
}
```

**总结**：

​ 1. 虚析构或纯虚析构就是用来解决通过基类指针释放派生类对象

​ 2. 如果派生类中没有堆区数据，可以不写为虚析构或纯虚析构

​ 3. 拥有纯虚析构函数的类也属于抽象类

---

## 5 文件操作
```

程序运行时产生的数据都属于临时数据，程序一旦运行结束都会被释放。
通过**文件可以将数据持久化**。

在 `C++` 中对文件操作需要包含头文件 `&lt;fstream&gt;`。

文件类型分为两种：
1. **文本文件** - 文件以文本的 **ASCII 码** 形式存储在计算机中。
2. **二进制文件** - 文件以文本的 **二进制** 形式存储在计算机中，用户一般不能直接读懂它们。

---

### 5.1 文本文件

---

#### 5.1.1 写文件

**步骤：**

1.  包含头文件
    `#include &lt;fstream&gt;`

2.  创建流对象
    `ofstream ofs;`

3.  打开文件
    `ofs.open("文件路径", 打开方式);`

4.  写数据
    `ofs &lt;&lt; "写入的数据";`

5.  关闭文件
    `ofs.close();`

**文件打开方式：**

| 打开方式 | 解释 |
| :--- | :--- |
| ios::in | 为读文件而打开文件 |
| ios::out | 为写文件而打开文件 |
| ios::ate | 初始位置：文件尾 |
| ios::app | 追加方式写文件 |
| ios::trunc | 如果文件存在先删除，再创建 |
| ios::binary | 二进制方式 |

**注意：** 文件打开方式可以配合使用，利用 `|` 操作符。
**例如：** 用二进制方式写文件 `ios::binary | ios::out`

**示例：**
```cpp
#include &lt;iostream&gt;
#include &lt;fstream&gt;  // 包含头文件
using namespace std;

int main(){
    ofstream o1;  // 创建流对象
    o1.open("test.txt", ios::out);  // 打开文件

    // 写数据
    o1 &lt;&lt; "lys" &lt;&lt; endl;
    o1 &lt;&lt; "ege 20" &lt;&lt; endl;
    o1 &lt;&lt; "is a dog" &lt;&lt; endl;

    o1.close();  // 关闭文件
    return 0;
}
```

**总结：**

*   文件操作必须包含头文件 `fstream`。
*   写文件可以利用 `ofstream`，或者 `fstream` 类。
*   打开文件时需要指定操作文件的路径，以及打开方式。
*   利用 `&lt;&lt;` 可以向文件中写数据。
*   操作完毕，要关闭文件。

---

#### 5.1.2 读文件

---

读文件步骤如下：

1.  包含头文件
    `#include &lt;fstream&gt;`

2.  创建流对象
    `ifstream ifs;`

3.  打开文件并判断文件是否打开成功
    `ifs.open("文件路径", 打开方式);`

4.  读数据（四种方式读取）

5.  关闭文件
    `ifs.close();`

**示例：**
```cpp```

#include &lt;stdio.h&gt; 
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
#include &lt;fstream&gt;  //包含头文件   
using namespace std;

int main(){

ifstream i1;  //创建流对象

i1.open("test.txt",ios::in);  //打开文件

if(!i1.is_open()){  //判断文件是否打开成功
        cout&lt;&lt;"找不到该文件"&lt;&lt;endl;
    }

//读数据

//  //1
//  char s1[1024]={0};
//  while(i1&gt;>s1){
//      cout&lt;&lt;s1&lt;&lt;endl;  //遇到空格读出一次 
//  } 
//
//  //2
//  char s2[1024]={0};
//  while(i1.getline(s2,sizeof(s2))){
//      cout&lt;&lt;s2&lt;&lt;endl;  //遇到换行读出一次 
//  }
//
//  //3
//  char s3;
//  while((s3=i1.get())!=EOF){
//      cout&lt;&lt;s3;  //一个字符读出一次 
//  }

//4
    string s4;
    while(getline(i1,s4)){
        cout&lt;&lt;s4&lt;&lt;endl;  //遇到换行读出一次 
    }

i1.close();  //关闭文件

return 0;

}
```

**总结** ：

* 读文件可以利用 `ifstream`，或者 `fstream` 类
  * 利用 `is_open` 函数可以判断文件是否打开成功
  * `close` 关闭文件

---

### 5.2 二进制文件

---

以二进制的方式对文件进行读写操作

打开方式要指定为 `ios::binary`

---

#### 5.2.1 写文件

---

二进制方式写文件主要利用流对象调用成员函数 `write`

**函数原型** ：`ostream& write(const char * buffer, int len);`

**参数解释** ：字符指针 `buffer` 指向内存中一段存储空间。`len` 是读写的字节数

**示例：**
```cpp

#include &lt;stdio.h&gt; 
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
#include &lt;fstream&gt;  //包含头文件   
using namespace std;

int main(){

ofstream o1;  //创建流对象

o1.open("test_01.txt",ios::out|ios::binary);  //打开文件

//写数据
    char s[1024]="lys is a dog";  //string写入，在读出时会出问题
    o1.write((const char*)&s,sizeof(s));

o1.close();  //关闭文件

return 0;

}
```

**总结** ：

* 文件输出流对象可以通过 `write` 函数，以二进制方式写数据  
  * 不要读入 `string` 类型  
  * **原因**：`string` 在 `stl` 中其实是一个类，这样写入的其实是 `test_01` 这个类对象，因此写到文件的其实是这个类的数据和指向这个类的指针。同时，因为 `string` 类的字符串是用 `new` 在堆上分配的，`string` 类本身只包含字符串的指针，用 `c_str()` 这个成员函数可以获得这个指针  

---

#### 5.2.2 读文件

二进制方式读文件主要利用流对象调用成员函数 `read`。  

**函数原型**：`istream& read(char *buffer, int len);`  

参数解释：字符指针 `buffer` 指向内存中一段存储空间，`len` 是读写的字节数。  

示例：  
```cpp
#include &lt;iostream&gt;
#include &lt;string&gt;
#include &lt;algorithm&gt;
#include &lt;fstream&gt;  //包含头文件   
using namespace std;

int main() {

    ifstream i1;  //创建流对象

    i1.open("test_01.txt", ios::in | ios::binary);  //打开文件

    if (!i1.is_open()) {  //判断文件是否打开成功
        cout << "找不到该文件" << endl;
    }

    //读数据
    char s[1024];
    i1.read((char*)&s, sizeof(s));
    cout << s << endl;

    i1.close();  //关闭文件

    return 0;
}
```

**总结**：  
* 文件输入流对象可以通过 `read` 函数，以二进制方式读数据。