---
title: "C++面向对象程序设计"
date: 2022-08-29
categories: [c++, C/C++]
description: ""
---

# c核心编程


## C++核心编程

---

### 1 内存分区模型

`C++`程序在执行时，将内存大方向划分为**4个区域**

*   **代码区**：存放函数体的二进制代码，由操作系统进行管理。
*   **全局区**：存放全局变量、静态变量以及常量。
*   **栈区**：由编译器自动分配释放，存放函数的参数值、局部变量等。
*   **堆区**：由程序员分配和释放，若程序员不释放，程序结束时由操作系统回收。

**内存四区意义：**

不同区域存放的数据，被赋予不同的生命周期，这给我们带来了更大的编程灵活性。

---

#### 1.1 程序运行前

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
#include <iostream>
#include <string>
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
    cout << "程序运行前：" << endl;
    cout << endl;

    // 局部变量
    int a = 10;
    int b = 10;

    // 局部变量的地址
    cout << "局部变量a的地址为：" << &a << endl;
    cout << "局部变量b的地址为：" << &b << endl;

    // 全局变量的地址
    cout << "全局变量g_a的地址为：" << &g_a << endl;
    cout << "全局变量g_b的地址为：" << &g_b << endl;
    cout << endl;

    // 静态局部变量
    static int s_a = 10;
    static int s_b = 10;

    // 静态局部变量的地址
    cout << "静态局部变量s_a的地址为：" << &s_a << endl;
    cout << "静态局部变量s_b的地址为：" << &s_b << endl;

    // 静态全局变量的地址
    cout << "静态全局变量s_g_a的地址为：" << &s_g_a << endl;
    cout << "静态全局变量s_g_b的地址为：" << &s_g_b << endl;
    cout << endl;

    // 常量
    // 字符串常量
    const char* s1 = "abcd";
    const char* s2 = "abcd";
    cout << "字符串常量s1的地址为：" << (void*)s1 << endl;
    cout << "字符串常量s2的地址为：" << (void*)s2 << endl;

    // const修饰的局部常量
    const int c_a = 10;
    const int c_b = 10;
    cout << "局部常量c_a的地址为：" << &c_a << endl;
    cout << "局部常量c_b的地址为：" << &c_b << endl;
    cout << endl;

    // 全局常量地址
    cout << "全局常量g_c_a的地址为：" << &g_c_a << endl;
    cout << "全局常量g_c_b的地址为：" << &g_c_b << endl;

    return 0;
}
```
```cpp
//const 修饰的局部常量
    const int c_a=10;
    const int c_b=10;

//字符串局部常量的地址
    cout<<"字符串局部常量s1的地址为："<<&s1<<endl;
    cout<<"字符串局部常量s2的地址为："<<&s2<<endl;

//字符串全局常量的地址
    cout<<"字符串全局常量g_s1的地址为："<<&g_s1<<endl;
    cout<<"字符串全局常量g_s2的地址为："<<&g_s2<<endl;

//const 修饰的局部常量
    cout<<"const 修饰的局部常量c_a的地址为："<<&c_a<<endl;
    cout<<"const 修饰的局部常量c_b的地址为："<<&c_b<<endl;

//const 修饰的全局常量
    cout<<"const 修饰的全局常量g_c_a的地址为："<<&g_c_a<<endl;
    cout<<"const 修饰的全局常量g_c_b的地址为："<<&g_c_b<<endl;

cout<<endl;

cout<<"有全局修饰的在全局区"<<endl;
    cout<<"其他的不在全局区"<<endl;

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

#### 1.2 程序运行后

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
#include <stdio.h> 
#include <iostream>
#include <string>
#include <algorithm>
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
    cout<<"栈区数据由编译器自动分配释放, 存放函数的参数值,局部变量等"<<endl;

    //调用函数test_01 
    int* p1=test_01();

    cout<<endl;

    //输出 
    cout<<"第一次输出，编译器对局部变量做一次保留，暂时不释放： "<<*p1<<endl;

    cout<<"第二次输出，编译器不再保留栈区的数据，直接释放："<<*p1<<endl;

    cout<<"不要返回局部变量的地址！！！"<<endl;

    cout<<endl;

    //调用函数test_02
    int* p2=test_02();

    //输出
    cout<<"输出存放在堆区的数据，编译器不释放，由程序员手动释放: "<<*p2<<endl; 
    cout<<"输出存放在堆区的数据，编译器不释放，由程序员手动释放: "<<*p2<<endl; 
    cout<<"输出存放在堆区的数据，编译器不释放，由程序员手动释放: "<<*p2<<endl;

    cout<<endl;

    //释放堆中开辟的数据
    delete p2;

    cout<<"程序员手动释放后: "<<*p2<<endl;

    return 0;
}
```

---

**总结：**

堆区数据由程序员管理开辟和释放

堆区数据利用`new`关键字进行开辟内存

---

#### 1.3 new操作符

---

`C++`中利用`new`操作符在堆区开辟数据

堆区开辟的数据，由程序员手动开辟，手动释放，释放利用操作符`delete`

**语法**：`new 数据类型`

利用`new`创建的数据，会返回该数据对应的类型的指针

**示例1：开辟数据**
```cpp
#include <stdio.h> 
#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

int* test_01(){
    int* a=new int(10);  //堆区开辟数据
    return a;
}

int main(){
    int *p=test_01();

    cout<<*p<<endl;
    cout<<*p<<endl;

    //利用delete释放堆区数据
    delete p;

    cout<<*p<<endl; //已释放，输出垃圾值

    return 0;
}
```

**示例2：开辟数组**
```cpp
#include <stdio.h> 
#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

int* test_01(){
    int* a=new int[10];  //堆区中开辟数组 
    return a;
}

int main(){
    int *p=test_01();

    for(int i=0;i<10;i++) p[i]=i+1;  //赋值

    for(int i=0;i<10;i++) cout<<p[i]<<" ";  //输出

    cout<<endl;

    //未释放前输出p[0]
    cout<<*p<<endl;

    //利用delete释放堆区数据
    delete[] p;

    //已释放，输出垃圾值 
    cout<<*p<<endl;

    return 0;
}
```

---

### 2 引用及其使用

---

#### 2.1 引用的基本使用

---

**作用：** 给变量起别名

**语法：** `数据类型 &别名 = 原名`

**示例：**
```cpp
#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

int main(){
    int a = 10;

    int &b = a;  // 创建a的别名为b，必须初始化

    cout << "a = " << a << endl;
    cout << "b = " << b << endl;  // b的值同a

    // 修改a的值 
    a = 20;

    cout << "a = " << a << endl;
    cout << "b = " << b << endl;  // b的值也发生改变

    // 修改b的值 
    b = 10;

    cout << "a = " << a << endl;  // a的值也发生改变 
    cout << "b = " << b << endl;

    return 0;
}
```

---

#### 2.2 引用注意事项

---

* 引用必须初始化

* 引用在初始化后，不可以改变

示例：
```cpp
#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

int main() {
    int a = 10;
    int b = 20;
    // int &c; // 错误，引用必须初始化
    int &c = a; // 一旦初始化后，就不可以更改
    c = b; // 这是赋值操作，不是更改引用

    cout << "a = " << a << endl;
    cout << "b = " << b << endl;
    cout << "c = " << c << endl;

    return 0;
}
```

---

#### 2.3 引用做函数参数

---

**作用：** 函数传参时，可以利用引用的技术让形参修饰实参

**优点：** 可以简化指针修改实参

**示例：**
```cpp
#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

void swap(int &a, int &b){
    int t = a;
    a = b;
    b = t;
}

int main(){
    int a = 10;
    int b = 20;

    cout << "a = " << a << endl;
    cout << "b = " << b << endl;

    cout << endl;

    swap(a, b);

    cout << "a = " << a << endl;
    cout << "b = " << b << endl;

    return 0;
}
```

**总结**：通过引用参数产生的效果同按地址传递是一样的。引用的语法更清楚简单。

---

#### 2.4 引用做函数返回值

---

**作用**：引用是可以作为函数的返回值存在的

**注意**：**不要返回局部变量引用**

**用法**：函数调用作为左值

**示例：**
```cpp
#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

int& test() {
    static int a = 10; // 静态局部变量，生命周期长于函数
    return a;
}

int main() {
    int &ref = test();
    cout << "ref = " << ref << endl;

    test() = 20; // 函数调用作为左值
    cout << "ref = " << ref << endl;

    return 0;
}
```

```cpp
#include <stdio.h> 
#include <iostream>
#include <string>
#include <algorithm>
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

    cout<<"ans_01 = "<<ans_01<<endl;  //第一次输出正确是因为编译器做了保留 
    cout<<"ans_01 = "<<ans_01<<endl;  //再次输出已经被释放，输出垃圾值
    cout<<"不要返回局部变量的引用！！！"<<endl;

    cout<<endl;

    int &ans_02=test_02();

    cout<<"ans_02 = "<<ans_02<<endl;
    cout<<"ans_02 = "<<ans_02<<endl;
    cout<<"ans_02 = "<<ans_02<<endl;

    test_02()=20;  //函数调用作为左值

    cout<<"ans_02 = "<<ans_02<<endl;

    return 0;
}
```

---

#### 2.5 引用的本质

---

**本质**：引用的本质在C++内部实现是一个**指针常量**。

讲解示例：
```cpp
#include <stdio.h> 
#include <iostream>
#include <string>
#include <algorithm>
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

    cout<<"a = "<<a<<endl;
    cout<<"ref = "<<ref<<endl;

    test_01(a);

    cout<<"a = "<<a<<endl;
    cout<<"ref = "<<ref<<endl;

    return 0;
}
```

**结论**：`C++`推荐用引用技术，因为语法方便，引用本质是指针常量，但是所有的指针操作编译器都帮我们做了。

---

#### 2.6 常量引用

---

**作用：** 常量引用主要用来修饰形参，防止误操作

在函数形参列表中，可以加 `const` 修饰形参，防止形参改变实参

**示例：**
```cpp
#include <stdio.h> 
#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

int test_01(const int &a){
    int b=a+10;
//  a=b;  //报错 a被const修饰 不可修改
    return b;
}

int main(){
    int a=10;
    int b=test_01(a);
    cout<<"a = "<<a<<endl;
    cout<<"b = "<<b<<endl;
    return 0;
}
```

---

### 3 函数提高

---

#### 3.1 函数默认参数

---

在 `C++` 中，函数的形参列表中的形参是可以有默认值的。

语法：`返回值类型 函数名（参数=默认值）{}`

**示例：**
```cpp
//1. 如果某个位置参数有默认值，那么从这个位置往后，从左向右，必须都要有默认值
//2. 如果函数声明有默认值，函数实现的时候就不能有默认参数
#include <stdio.h> 
#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

int add(int a,int b=10){
    return a+b;
}

int main(){
    int a=20,b=30;
    cout<<add(a,b)<<endl;
    cout<<add(a)<<endl;  //未传入参数b，默认b=10
    return 0;
}
```

---

#### 3.2 函数占位参数

---

`C++` 中函数的形参列表里可以有占位参数，用来做占位，调用函数时必须填补该位置。

**语法：** `返回值类型 函数名（数据类型）{}`

在现阶段函数的占位参数存在意义不大，但是后面的课程中会用到该技术。

**示例：**
```cpp
//函数占位参数，占位参数也可以有默认参数
#include <stdio.h> 
#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

int add(int a,int){
    return a;
}

int main(){
    int a=20,b=30;
    cout<<add(a,b)<<endl;  //占位参数必须填补
    return 0;
}
```

#### 3.3 函数重载

---

##### 3.3.1 函数重载概述

---

**作用：** 函数名可以相同，提高复用性。

**函数重载满足条件：**

- 同一个作用域下
  - 函数名称相同
  - 函数参数 **类型不同** 或者 **个数不同** 或者 **顺序不同**

**注意：** 函数的返回值不可以作为函数重载的条件。

**示例：**
```cpp
//函数重载需要函数都在同一个作用域下
#include <stdio.h> 
#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

int add(){
    cout << "add() 的调用： " << 0 << endl;
}

int add(int a){
    cout << "add(int a) 的调用：" << a << endl;
}

int add(double a){
    cout << "add(double a) 的调用：" << a << endl;
}

int add(int a, int b){
    cout << "add(int a, int b) 的调用：" << a << "+" << b << "=" << a + b << endl;
}

int add(int a, double b){
    cout << "add(int a, double b) 的调用：" << a << "+" << b << "=" << a + b << endl;
}

int add(double a, int b){
    cout << "add(double a, int b) 的调用：" << a << "+" << b << "=" << a + b << endl;
}

int add(double a, double b){
    cout << "add(double a, double b) 的调用：" << a << "+" << b << "=" << a + b << endl;
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

##### 3.3.2 函数重载注意事项

---

* 引用作为重载条件
* 函数重载碰到函数默认参数

**示例：**

```cpp
//1、引用作为重载条件
#include <stdio.h> 
#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

void func(int &a){
    cout << "func(int &a) 的调用：" << a << endl;
}

void func(const int &a){
    cout << "func(const int &a) 的调用：" << a << endl;
}

int main(){
    int a = 10;
    func(a);    //调用无const
    func(20);   //调用有const
    return 0;
}

//函数重载碰到函数默认参数
#include <stdio.h> 
#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

void func(int a, int b = 10){
    cout << "func(int a, int b = 10) 的调用" << endl;
}

void func(int a){
    cout<<"func(int a) 的调用"<<endl;
}

int main(){
    func(10);  //报错，原因产生歧义
    return 0;
}
```

---

### **4** 类和对象

---

`C++`面向对象的三大特性为：`封装、继承、多态`

`C++`认为**万事万物皆为对象**，对象有其属性和行为

**例如：**

​ 人可以作为对象，属性有姓名、年龄、身高、体重...，行为有走、跑、跳、吃饭、唱歌...

​ 车也可以作为对象，属性有轮胎、方向盘、车灯...，行为有载人、放音乐、放空调...

​ 具有相同性质的**对象**，我们可以抽象称为**类**，人属于人类，车属于车类

---

#### 4.1 封装

---

##### 4.1.1 封装的意义

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
#include <stdio.h> 
#include <iostream>
#include <string>
#include <algorithm>
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

    cout<<"c1的周长为： "<<c1.calculate()<<endl;

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
#include <stdio.h> 
#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

class person{
    public:  //访问权限  公共的权限

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

    cout<<p1.name;  //public 类外可以访问

    //p1.money=0;  // protected 类外不可更改，不可访问 
    //cout<<p1.money;

    //p1.year=100;  //private 类外不可更改，不可访问 
    //cout<<p1.year;

    return 0;
}
```

---

##### 4.1.2 struct和class区别

---

在`C++`中 struct和class唯一的**区别** 就在于 **默认的访问权限不同**

区别：

* struct 默认权限为公共
  * class 默认权限为私有

```cpp
#include <stdio.h> 
#include <iostream>
#include <string>
#include <algorithm>
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

    //p2.x=10;
    //p2.y=20;  //错误，访问权限是私有

    return 0;
}
```

---

#### 4.2 对象的初始化和清理

---

##### 4.2.1 构造函数和析构函数

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
#include <stdio.h> 
#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

class point{
    public:
        // 构造函数
        point(){
            cout<<"point的构造函数调用"<<endl;
        }

        // 析构函数
        ~point(){
            cout<<"point的析构函数调用"<<endl;
        }
};

int main(){
    point p1;
    return 0;
}
```

---

##### 4.2.2 构造函数的分类及调用方式

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
#include <stdio.h> 
#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

class point{
    public:
        int x, y;

        point(){
            cout<<"无参构造函数调用"<<endl; 
        }

        point(int a, int b){
            x=a;
            y=b;
            cout<<"有参构造函数调用"<<endl;
        }

        point(const point &p){
            x=p.x;
            y=p.y;
            cout<<"拷贝构造函数调用"<<endl;
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

---

##### 4.2.3 拷贝构造函数调用时机

---

`C++`中拷贝构造函数调用时机通常有三种情况：

* 使用一个已经创建完毕的对象来初始化一个新对象
* 值传递的方式给函数参数传值
* 以值方式返回局部对象

**示例：**
```cpp
#include <stdio.h>
#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

class point{
    public:
        int x,y;

        point(){
            cout << "默认构造函数调用" << endl;
        }

        point(int a,int b){
            x = a;
            y = b;
            cout << "有参构造函数调用" << endl;
        }

        point(const point &p){
            x = p.x;
            y = p.y;
            cout << "拷贝构造函数调用" << endl;
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
    cout << p3.x << " " << p3.y;
}

//3. 以值方式返回局部对象
int show_x(point p){
    return p.x;
}

void test03(){
    point p4(2,3);
    cout << show_x(p4);
}

int main(){
    test01();
    test02();
    test03();
    return 0;
}
```

---

##### 4.2.4 构造函数调用规则

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
#include <stdio.h>
#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

class point{
    public:
        int x,y;

        point(){
            cout << "无参构造函数" << endl;
        }

        point(int a, int b) {
            x = a;
            y = b;
            cout << "有参构造函数" << endl;
        }

        point(const point &p) {
            x = p.x;
            y = p.y;
            cout << "拷贝构造函数" << endl;
        }

        ~point() {
            cout << "析构函数" << endl;
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
    // point p3;  // 此时如果用户自己没有提供默认构造，会出错

    point p4(3, 4);  // 用户提供的有参

    point p5(p4);  // 此时如果用户没有提供拷贝构造，编译器会提供

    // 如果用户提供拷贝构造，编译器不会提供其他构造函数
    // point p6;  // 此时如果用户自己没有提供默认构造，会出错

    // point p7(5, 6);  // 此时如果用户自己没有提供有参，会出错
    point p8(p7);    // 用户自己提供拷贝构造
}

int main() {
    test01();
    test02();
    return 0;
}
```

---

##### 4.2.5 深拷贝与浅拷贝

---

* 浅拷贝：简单的赋值拷贝操作
* 深拷贝：在堆区重新申请空间，进行拷贝操作

**示例：**
```cpp
#include <stdio.h>
#include <iostream>
#include <string>
#include <algorithm>
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
```cpp
#include <stdio.h> 
#include <iostream>
#include <string>
#include <algorithm>
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

##### 4.2.6 初始化列表

---

**作用：**`C++`提供了初始化列表语法，用来初始化属性

**语法：**`构造函数()：属性1(值1),属性2（值2）... {}`

**示例：**
```cpp
#include <stdio.h> 
#include <iostream>
#include <string>
#include <algorithm>
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

    cout<<p1.x<<" "<<p1.y<<" "<<p1.z<<endl;
}

int main(){
    test01();

    return 0;
}
```

---

##### 4.2.7 类对象作为类成员

---

`C++`类中的成员可以是另一个类的对象，我们称该成员为对象成员

**例如**：
```cpp
class A{

};

class B{
    A a;
};
```

B类中有对象A作为成员，A为对象成员当创建B对象时，**A与B的构造和析构的顺序**

**示例：**
```cpp
//构造的顺序是：先调用对象成员的构造，再调用本类构造
//析构顺序与构造相反
#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

class A{
public:
    A(){
        cout << "A的构造函数调用" << endl;
    }

    ~A(){
        cout << "A的析构函数调用" << endl;
    }
};

class B{
public:
    A a;

    B(){
        cout << "B的构造函数调用" << endl;
    }

    ~B(){
        cout << "B的析构函数调用" << endl;
    }
};

int main(){
    B b2;
    return 0;
}
```

---

##### 4.2.8 静态成员

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
#include <iostream>
#include <string>
#include <algorithm>
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
    cout << p1.x << endl;      //1、通过对象访问

    point p2;
    cout << p2.x << endl;      //共享同一份数据

    cout << point::x << endl;  //2、通过类名访问

    //cout << p2.y << endl;    //私有权限访问不到

    return 0;
}
```

**示例2：静态成员函数**
```cpp
//静态成员函数特点：
    //1 程序共享一个函数
    //2 静态成员函数只能访问静态成员变量
#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

class point{
public:
    static int x;
    int y;

    static void show_pub(){
        cout<<x<<endl;
        //cout<<y<<endl;  //错误，不可以访问非静态成员变量
    }

private:
    static int z;

    //静态成员函数也是有访问权限的
    static void show_pri(){
        cout<<z<<endl;
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

#### 4.3 C++对象模型和this指针

---

##### 4.3.1 成员变量和成员函数分开存储

---

在`C++`中，类内的成员变量和成员函数分开存储。

只有**非静态成员变量** 才属于类的对象上。

**示例**
```cpp
#include <stdio.h> 
#include <iostream>
#include <string>
#include <algorithm>
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
    cout<<sizeof(point1)<<endl;
    cout<<sizeof(point2)<<endl;
}
```

**注意**：`C++`编译器会给空类的对象分配一个字节，用于区分其存储空间。

---

##### 4.3.2 this指针概念

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
#include <stdio.h> 
#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

class point{
public:
    int x,y;

    //1、当形参和成员变量同名时，可用this指针来区分
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
};

void test01() {
    point p1(1, 2);
    cout << p1.x << " " << p1.y << endl;
}

void test02() {
    point p2(1, 1);
    point p3(0, 0);
    p3.add(p2).add(p2).add(p2);
    cout << p2.x << " " << p2.y << endl;
}

int main() {
    test01();
    test02();
    return 0;
}
```

---

##### 4.3.3 空指针访问成员函数

---

`C++`中空指针也是可以调用成员函数的，但是也要注意有没有用到this指针。

如果用到this指针，需要加以判断保证代码的健壮性。

**示例：**
```cpp
#include <stdio.h> 
#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

class point {
public:
    int x, y;

    point(int a, int b) : x(a), y(b) {}

    void show_1() {
        cout << "YES" << endl;
    }

    void show_2() {
        cout << x << " " << y << endl;  //默认使用了this指针 
//      cout << this->x << this->y << endl;  //与上一行等价
    }
};

int main() {
    point *p1 = NULL;

    p1->show_1();   //空指针，可以调用成员函数
    //p1->show_2();   //但是如果成员函数中用到了this指针，就不可以了

    return 0;
}
```

---

##### 4.3.4 const修饰成员函数

---

**常函数：**

* 成员函数后加`const`后我们称为这个函数为**常函数**
  * 常函数内不可以修改成员属性
  * 成员属性声明时加关键字`mutable`后，在常函数中依然可以修改

**常对象：**

* 声明对象前加`const`称该对象为常对象
  * 常对象只能调用常函数

**示例：**
```cpp
#include <stdio.h> 
#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

class point {
public:
    int x;
    mutable int y;  //可修改 可变的

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
        cout << x << " " << y << endl;
    }

    void show_2() {
        cout << x << " " << y << endl;
    }

    //      void show_no() const {
    //          this->x = 20;
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
```

---

#### 4.4 友元

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

##### 4.4.1 全局函数做友元

**示例**
```cpp
#include <stdio.h>
#include <iostream>
#include <string>
#include <algorithm>
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
    cout << p.x << endl << p.y << endl;
}

int main() {
    point p1;
    visit(p1);
}
```

---

##### 4.4.2 类做友元

---

**示例**
```cpp
#include <stdio.h> 
#include <iostream>
#include <string>
#include <algorithm>
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
        cout<<p1.x<<" "<<p1.y<<endl;  //可以访问类point里的私有y
    }
};

int main(){
    show s1;

    s1.visit();

    return 0;
}
```

---

##### 4.4.3 成员函数做友元

---

**示例**
```cpp
#include <stdio.h> 
#include <iostream>
#include <string>
#include <algorithm>
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
    cout << "好基友正在访问" << p->x << endl;
    cout << "好基友正在访问" << p->y << endl;
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

#### 4.5 运算符重载

---

**运算符重载概念** ：利用`operator`对已有的运算符重新进行定义，赋予其另一种功能，以适应不同的数据类型

**本质** ：

* 提供一个`operator 运算符()`函数，使得`A operator 运算符(B)`的形式可以化简为`A 运算符 B`的形式

---

##### 4.5.1 加号/减号运算符重载

**作用** ：实现两个自定义数据类型相加的运算

**示例1**
```cpp
//成员函数实现 + / -号运算符重载
#include <stdio.h> 
#include <iostream>
#include <string>
#include <algorithm>
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
    cout<<p3.x<<" "<<p3.y<<endl;
    p3=p2-p1;
    cout<<p3.x<<" "<<p3.y<<endl;
    return 0;
}
```

**示例2**
```cpp
//全局函数实现 + / -号运算符重载
#include <stdio.h> 
#include <iostream>
#include <string>
#include <algorithm>
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
    cout<<p3.x<<" "<<p3.y<<endl;
    p3=p2-p1;
    cout<<p3.x<<" "<<p3.y<<endl;
    return 0;
}
```

**总结**

* 对于内置的数据类型的表达式的运算符是不可能改变的
* 不要滥用运算符重载

---

##### 4.5.2 左移运算符重载

---

**作用**：可以输出自定义数据类型

---

**注意**：一般使用全局函数实现

**示例**
```cpp
// 全局函数实现输出运算符重载
#include <stdio.h> 
#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

class point{
public:
    int x, y;

    point(){}

    point(int a, int b): x(a), y(b){}
};

// ostream对象只能有一个
ostream& operator<<(ostream &cout, point &p){
    cout << p.x << " " << p.y << endl;
    return cout; 
}

int main(){
    point p1(1, 1);

    cout << p1 << "链式输出" << endl;

    return 0;
}
```

---

##### 4.5.3 递增运算符重载

---

**作用**：通过重载递增运算符，实现自己的整型数据

**示例**
```cpp
#include <stdio.h> 
#include <iostream>
#include <string>
#include <algorithm>
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

    cout << p1.x << " " << p1.y << endl;

    return 0;
}
```

---

##### 4.5.4 赋值运算符重载

---

`C++`编译器至少给一个类添加4个函数

1. 默认构造函数(无参，函数体为空)
2. 默认析构函数(无参，函数体为空)
3. 默认拷贝构造函数，对属性进行值拷贝
4. 赋值运算符 `operator=`, 对属性进行值拷贝

如果类中有属性指向堆区，做赋值操作时也会出现深浅拷贝问题

**示例：**
```cpp
#include <stdio.h> 
#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

class point{
public:
    int *x, *y;  // 开辟到堆区

    point(){
        x = new int(0);
        y = new int(0);
    }

    point(int a, int b) {
        x = new int(a);  // 将数据开辟到堆区
        y = new int(b);
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

    cout << "p2.x = " << *p2.x << " p2.y = " << *p2.y << endl;

    return 0;
}
```

```cpp
#include <stdio.h> 
#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

class point{
public:
    int *x, *y;  // 开辟到堆区

    point(){
        x = new int(0);
        y = new int(0);
    }

    point(int a, int b) {
        x = new int(a);  // 将数据开辟到堆区
        y = new int(b);
    }

    // 重载赋值运算符
    point& operator=(point& p) {
        if (this->x != NULL) {
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

    cout << *p1.x << " " << *p1.y << endl;

    return 0;
}
```

---

##### 4.5.5 关系运算符重载

---

**作用：** 重载关系运算符，可以让两个自定义类型对象进行对比操作。

**示例：**
```cpp
#include <stdio.h> 
#include <iostream>
#include <string>
#include <algorithm>
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

    if (p1 == p2) cout << "YES" << endl;
    else cout << "NO" << endl;

    return 0;
}
```

---

##### 4.5.6 函数调用运算符重载

---

**特点**

* 函数调用运算符 `()` 也可以重载。
  * 由于重载后使用的方式非常像函数的调用，因此称为仿函数。
  * 仿函数没有固定写法，非常灵活。

**示例：**
```cpp
#include <stdio.h>
#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

class print {
public:
    void operator()(auto s) { // 重载的 () 操作符，也称为仿函数
        cout << s << endl;
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
    cout << a(1, 2) << endl;
}

int main() {
    test01();
    test02();
    return 0;
}
```

---

#### 4.6 继承

**继承是面向对象三大特性之一。**

我们发现，定义这些类时，下级的成员除了拥有上级的共性，还有自己的特性。这个时候我们就可以考虑利用继承的技术，减少重复代码。

**定义和概念**

继承是类的重要特性。A类继承B类，我们称B类为“基类”，A类为“派生类”。A类继承了B类之后，A类就具有了B类的部分成员，具体得到了哪些成员，这由两个方面决定：
* 继承方式
* 基类成员访问权限

---

##### 4.6.1 继承的基本语法

**基本语法**：`class A : public B`

* `A` 类称为**派生类**。
* `B` 类称为**基类**。

**示例**：对于一个人来说，有姓名、年龄、性别这些基本特征，而像是职位之类的特征则是因人而异的特征。在创建“人”的类的时候，我们可以通过继承的技术，减少对基本特征的定义等操作的代码。

**普通实现：**
```cpp
#include <stdio.h>
#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

// 学生类
class student {
public:
    string name, sex;
    int year;

    student(string n, int x, string s) : name(n), year(x), sex(s) {}

    void show_name() {
        cout << "名字：" << name << endl;
    }

    void show_year() {
        cout << "年龄：" << year << endl;
    }

    void show_sex() {
        if (sex == "boy") {
            cout << "性别：男" << endl;
        } else {
            cout << "性别：女" << endl;
        }
    }

    void show_position() {
        cout << "是一个学生" << endl;
    }
};

//家长类
class parent {
public:
    string name, sex;
    int year;

    parent(string n, int x, string s) : name(n), year(x), sex(s) {}

    void show_name() {
        cout << "名字：" << name << endl;
    }

    void show_year() {
        cout << "年龄：" << year << endl;
    }

    void show_sex() {
        if (sex == "boy") {
            cout << "性别：男" << endl;
        } else {
            cout << "性别：女" << endl;
        }
    }

    void show_position() {
        cout << "是一名家长" << endl;
    }
};

//教师类
class teacher {
public:
    string name, sex;
    int year;

    teacher(string n, int x, string s) : name(n), year(x), sex(s) {}

    void show_name() {
        cout << "名字：" << name << endl;
    }

    void show_year() {
        cout << "年龄：" << year << endl;
    }

    void show_sex() {
        if (sex == "boy") {
            cout << "性别：男" << endl;
        } else {
            cout << "性别：女" << endl;
        }
    }

    void show_position() {
        cout << "是一位老师" << endl;
    }
};

int main() {
    //学生对象
    student s1("lys", 20, "boy");
    s1.show_name();
    s1.show_year();
    s1.show_position();
    cout << endl;

    //家长对象
    parent p1("mama", 40, "girl");
    p1.show_name();
    p1.show_year();
    p1.show_position();
    cout << endl;

    //教师对象
    teacher t1("yxc", 30, "boy");
    t1.show_name();
    t1.show_year();
    t1.show_position();
    cout << endl;

    return 0;
}
```
```cpp
#include <stdio.h>
#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

// 用于继承的基类
class person {
public:
    string name, sex;
    int year;

    person(string n, int x, string s) : name(n), year(x), sex(s) {}

    void show_name() {
        cout << "名字：" << name << endl;
    }

    void show_year() {
        cout << "年龄：" << year << endl;
    }

    void show_sex() {
        if (sex == "boy") {
            cout << "性别：男" << endl;
        } else {
            cout << "性别：女" << endl;
        }
    }
};

// 学生类
class student : public person {
public:
    student(string n, int x, string s) : person(n, x, s) {}

    void show_position() {
        cout << "是一个学生" << endl;  // 因人而异的特征
    }
};

// 家长类
class parent : public person {
public:
    parent(string n, int x, string s) : person(n, x, s) {}

    void show_position() {
        cout << "是一名家长" << endl;
    }
};

// 教师类
class teacher : public person {
public:
    teacher(string n, int x, string s) : person(n, x, s) {}

    void show_position() {
        cout << "是一位老师" << endl;
    }
};

int main() {
    // 学生对象
    student s1("lys", 20, "boy");
    s1.show_name();
    s1.show_year();
    s1.show_position();
    cout << endl;

    // 家长对象
    parent p1("mama", 40, "girl");
    p1.show_name();
    p1.show_year();
    p1.show_position();
    cout << endl;

    // 教师对象
    teacher t1("yxc", 30, "boy");
    t1.show_name();
    t1.show_year();
    t1.show_position();
    cout << endl;

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

##### 4.6.2 继承方式

---

继承的语法：`class 派生类 : 继承方式 基类`

**继承方式一共有三种：**

- 公共继承
- 保护继承
- 私有继承

**示例1 公共继承：**

```cpp
#include <stdio.h> 
#include <iostream>
#include <string>
#include <algorithm>
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
            cout<<"x = "<<x<<endl;
            cout<<"y = "<<y<<endl;
        }
};

int main(){
    point_Pub p1;
    p1.show();

    //类外 
    cout<<"p1.x = "<<p1.x<<endl;  //只能访问到公共权限
    //cout<<"p1.y = "<<p1.y<<endl;
    //cout<<"p1.z = "<<p1.z<<endl;

    return 0;
}
```

**示例2 保护继承：**

```cpp
#include <iostream>
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
        cout << "x = " << x << endl;
        cout << "y = " << y << endl;
    }
};

int main() {
    point_Pro p1;
    p1.show();

    // 类外
    // cout << "p1.x = " << p1.x << endl;  // 不可访问，原有的 public 权限变为了 protected 权限
    // cout << "p1.y = " << p1.y << endl;  // 不可访问，原有的 protected 权限变为了 protected 权限
    // cout << "p1.z = " << p1.z << endl;

    return 0;
}
```

**示例3 私有继承**
```cpp
#include <iostream>
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
        cout << "x = " << x << endl;
        cout << "y = " << y << endl;
    }
};

int main() {
    point_Pri p1;
    p1.show();

    // 类外
    // cout << "p1.x = " << p1.x <<

