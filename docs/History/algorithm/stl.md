---
title: "STL 常用操作"
date: 2022-10-24
categories: [ALGORITHM, Basic Algorithm]
description: ""
---

# STL 常用操作

---

## 1\. vector

---

### 1.1 声明
```java


#include &lt;vector&gt;   // 头文件
vector&lt;int&gt; a;      // 相当于一个长度动态变化的int数组
vector&lt;int&gt; b[233]; // 相当于第一维长233，第二位长度动态变化的int数组
struct rec{…};
vector&lt;rec&gt; c;      // 自定义的结构体类型也可以保存在vector中
```

---

### 1.2 插入和删除

`a.push_back(x)`把元素`x`插入到`vector a`的尾部。 `a.pop_back()`删除`vector a`的最后一个元素。
```java


vector&lt;int&gt; a;
a.push_back(1);
a.push_back(2);
a.pop_back();
```

---

### 1.3 大小和判空

`size`函数返回`vector`的实际长度（包含的元素个数），`empty`函数返回一个`bool`类型，表明`vector`是否为空。二者的时间复杂度都是 $\mathcal{O}(1)$。
```java


    vector&lt;int&gt; a;
    a.push_back(1);
    a.push_back(2);

    cout << a.size() << endl;

    a.pop_back();
    if(a.empty()) cout << "a is empty !" << endl; 

    a.pop_back();
    if(a.empty()) cout << "a is empty !" << endl; 
```

**Tips** ：

  * **所有的`STL`容器都支持这两个方法，含义也相同**。



---

### 1.3 清空

利用`clear`函数把`vector`清空。
```java


    vector&lt;int&gt; a;
    a.push_back(1);
    a.push_back(2);

    cout << a.size() << endl;

    a.clear();
    if(a.empty()) cout << "a is empty !" << endl; 
```

---

### 1.4 迭代器

迭代器就像`STL`容器的“指针”，可以用星号`*`操作符解除引用。

一个保存`int`的`vector`的迭代器声明方法为：
```java


vector&lt;int&gt;::iterator it;
```

`vector`的迭代器是“随机访问迭代器”，可以把`vector`的迭代器与一个整数相加减，其行为和指针的移动类似。可以把`vector`的两个迭代器相减，其结果也和指针相减类似，得到两个迭代器对应下标之间的距离。

接下来引入两个迭代器 `begin/end`，`begin`函数返回指向`vector`中第一个元素的迭代器。例如`a`是一个非空的`vector`，则`*a.begin()`与`a[0]`的作用相同。
```java


vector&lt;int&gt; a;
for(int i = 1; i <= 10; i ++) a.push_back(i);
vector&lt;int&gt;::iterator it = a.begin();
cout << *it << endl;
```

所有的容器都可以视作一个“前闭后开”的结构，`end`函数返回`vector`的尾部，即第 `n`个元素再往后的“边界”。`*a.end()`与`a[n]`都是越界访问，其中`n = a.size()`。
```java


vector&lt;int&gt; a;
for(int i = 1; i <= 10; i ++) a.push_back(i);
// vector&lt;int&gt;::iterator it = a.end();  //越界
vector&lt;int&gt;::iterator it = a.end() - 1;
cout << *it << endl;
```

此外 `vector` 支持利用 `[]` 直接访问元素。
```java


vector&lt;int&gt; a;
for(int i = 1; i <= 10; i ++) a.push_back(i);
//迭代器访问
// for(vector&lt;int&gt;::iterator it = a.begin(); it != a.end(); it ++) cout &lt;&lt; *it &lt;&lt; ' ';
//[] 访问
for(int i = 0; i < a.size(); i ++) cout << a[i] << ' ';
```

特别地，可以利用`front`函数返回`vector`的第一个元素，等价于`*a.begin()`和`a[0]`。利用`back`函数返回`vector`的最后一个元素，等价于`*--a.end()`和`a[a.size() – 1]`。
```java


vector&lt;int&gt; a;
for(int i = 1; i <= 10; i ++) a.push_back(i);

cout << a.front() << endl;
cout << *a.begin() << endl;
cout << a[0] << endl;

cout << a.back() << endl;
cout << *-- a.end() << endl;
cout << a[a.size() - 1] << endl;
```

---

## 2\. queue

---

### 2.1 声明
```java


#include &lt;queue&gt;  //头文件，包含 queue 和 priority_queue
queue&lt;int&gt; q;
struct rec{…}; queue&lt;rec&gt; q;                        //结构体rec中必须定义小于号
priority_queue&lt;int&gt; q;                              // 大根堆
priority_queue&lt;int, vector&lt;int&gt;, greater&lt;int&gt;&gt; q;   // 小根堆
priority_queue&lt;pair&lt;int, int&gt;&gt; q;
```

---

### 2.2 插入和删除

**循环队列queue**

`push` 将元素插入到队尾，`pop` 将元素从队头弹出。
```java


queue&lt;int&gt; a;
a.push(1);
a.push(2);
a.pop();
```

**优先队列priority_queue**

`push` 将元素插入堆，`pop` 删除堆顶元素。
```java


priority_queue&lt;int&gt; a;
a.push(1);
a.push(2);
a.pop();
```

---

### 2.3 访问

`queue` 和 `priority_queue` 不支持随机访问迭代器。

**循环队列queue**
```java


queue&lt;int&gt; a;
for(int i = 1; i <= 10; i ++) a.push(i);

cout << a.front() << endl;  //队头元素
cout << a.back() << endl;   //队尾元素
```

**优先队列priority_queue**
```java


priority_queue&lt;int&gt; a;
for(int i = 1; i <= 10; i ++) a.push(i);

cout << a.top() << endl;  //仅支持访问堆顶元素
```

---

## 3\. dequeue

---

### 3.1 声明及操作
```java


#include &lt;dequeue&gt;
[]              // 随机访问
begin/end       // 返回deque的头/尾迭代器
front/back      // 队头/队尾元素
push_back       // 从队尾入队
push_front      // 从队头入队
pop_back        // 从队尾出队
pop_front       // 从队头出队
clear           // 清空队列
```

双端队列`deque`是一个支持在两端高效插入或删除元素的连续线性存储空间。它就像是`vector`和`queue`的结合。与`vector`相比，`deque`在头部增删元素仅需要 $\mathcal{O}(1)$ 的时间；与`queue`相比，`deque`像数组一样支持随机访问。

用的不多，对应操作的效率不如 `vector` 和 `queue`。

---

## 4\. set

---

### 4.1 声明
```java


#include &lt;set&gt;  //头文件包括 set 和 multiset
set&lt;int&gt; s;
struct rec{…}; set&lt;rec&gt; s;  // 结构体rec中必须定义小于号
multiset&lt;double&gt; s;
```

头文件`set`主要包括`set`和`multiset`两个容器，分别是“有序集合”和“有序多重集合”，即前者的元素不能重复，而后者可以包含若干个相等的元素。`set`和`multiset`的内部实现是一棵红黑树，它们支持的函数基本相同。

---

### 4.2 插入

`a.insert(x)`把一个元素x插入到集合`a`中，时间复杂度为 $\mathcal{O}(logn)$。

在`set`中，若元素已存在，则不会重复插入该元素，对集合的状态无影响。

---

### 4.3 迭代器

`set`和`multiset`的迭代器称为“双向访问迭代器”，不支持“随机访问”，支持星号`*`解除引用，仅支持`++`和`--`两个与算术相关的操作。

一个保存`int`的`set`的迭代器声明方法为：
```java


set&lt;int&gt;::iterator it;
```

接下来亦引入 `begin/end` 这俩个特殊的迭代器，分别返回集合的首、尾迭代器，时间复杂度均为 $\mathcal{O}(1)$。

`a.begin()`是指向集合中最小元素的迭代器。`a.end()`是指向集合中最大元素的下一个位置的迭代器。换言之，就像`vector`一样，是一个“前闭后开”的形式。因此`-- a.end()`是指向集合中最大元素的迭代器。
```java


set&lt;int&gt; a;
for(int i = 10; i >= 1; i --) a.insert(i);

cout << *a.begin() << endl;
cout << * -- a.end() << endl;

//利用迭代器遍历
for(set&lt;int&gt;::iterator it = a.begin(); it != a.end(); it ++) cout &lt;&lt; *it &lt;&lt; endl;
```

---

### 4.4 查找

利用`a.find(x)`在集合`a`中查找等于`x`的元素，并返回指向该元素的迭代器。若不存在，则返回`a.end()`。时间复杂度为 $\mathcal{O}(1)$。
```java


set&lt;int&gt; a;

for(int i = 10; i >= 1; i --) a.insert(i);

set&lt;int&gt;::iterator it = a.find(11);
if(it != a.end()) cout << "YES" << endl;
else cout << "NO" << endl;
```

另外提供`a.count(x)`返回集合`a`中等于`x`的元素个数，时间复杂度为 $\mathcal{O}(k+logn)$，其中 `k` 为元素`x`的个数。
```java


set&lt;int&gt; a;

for(int i = 10; i >= 1; i --) a.insert(i);

cout << a.count(11) << endl;
```

---

### 4.5 删除

提供`erase` 方法进行删除操作。

设`it`是一个迭代器，`a.erase(it)`从`a`中删除迭代器`it`指向的元素，时间复杂度为 $\mathcal{O}(logn)$。

设`x`是一个元素，`a.erase(x)`从`a`中删除所有等于`x`的元素，时间复杂度为 $\mathcal{O}(k+logn)$，其中 `k` 是被删除的元素个数。

---

## 5\. map

---

### 5.1 声明
```java


#include &lt;map&gt;  //头文件
map&lt;key_type, value_type&gt; name;

//例如：
map&lt;long long, bool&gt; vis;
map&lt;string, int&gt; hash;
map&lt;pair&lt;int, int&gt;, vector&lt;int&gt;&gt; test;
```

`map`容器是一个键值对`key-value`的映射，其内部实现是一棵以`key`为关键码的红黑树。`map`的`key`和`value`可以是任意类型，其中`key`必须定义小于号运算符。

---

### 5.2 常用操作

`size/empty/clear/begin/end` 均于 `set` 类似，但对于 `insert/erase` 的参数为 `pair&lt;key_type, value_type&gt;`。
```java


map&lt;int, int&gt; a;
a.insert({1, 1});
a.insert({2, 1});
```

特别的，对于 `find`，`a.find(x)` 在变量名为 `a` 的 `map` 种，查找 `key` 为 `x` 的二元组。
```java


map&lt;int, int&gt; a;
a.insert({1, 1});
a.insert({2, 1});

map&lt;int, int&gt;::iterator it = a.find(2);
if(it != a.end()){
    cout << "YES" << endl;
    cout << (*it).first << ' ' << (*it).second << endl;
}
else cout << "NO" << endl;
```

---

### 5.3 访问

除了和 `set` 一样利用迭代器进行访问，`map`也支持 `[]` 操作符进行访问。我们可以很方便地通过 `a[key]` 来得到`key`对应的`value`，还可以对`a[key]`进行赋值操作，改变`key`对应的`value`。
```java


    map&lt;int, int&gt; a;
    a.insert({1, 1});
    a.insert({2, 1});

    cout << a[2] << endl;
    a[2] = 100;  //修改key = 2 的 value 为 100
    cout << a[2] << endl;

    //利用迭代器遍历
    for(map&lt;int, int&gt;::iterator it = a.begin(); it != a.end(); it ++) cout &lt;&lt; (*it).first &lt;&lt; ' ' &lt;&lt; (*it).second &lt;&lt; endl;
```

此外，`C++11` 提供了更方便的遍历 `set/map` 的方式：
```java


    map&lt;int, int&gt; a;
    a.insert({1, 1});
    a.insert({2, 1});

    for(auto &p : a) cout << p.first << ' ' << p.second << endl;

    set&lt;int&gt; b;
    b.insert(1);
    b.insert(2);

    for(auto &p : b) cout << p << endl;
```

---

## 6\. string

---

### 6.1 声明
```java


#include &lt;string&gt;  //头文件
string(const char* s); //使用字符串s初始化
string(const string& str); //使用一个string对象初始化另一个string对象
string(int n, char c); //使用n个字符c初始化
```

`string` 可以视为一个动态字符数组使用。

---

### 6.2 常用操作
```java


string str1 = "abcdefghigklmn" ;

string str2 = str1.substr(2,5) ;  //将str1从下标2开始的5个字符赋值给str2

str1.reverse(s.begin(), s.end());  //将str1 翻转

int p1 = str1.find(str); //从最左边开始返回str1中首次出现str首字母的下标，没有时返回-1

int p2 = str1.find(str,3); //从下标3开始(包括s1[3])返回str1中首次出现str首字母的下标，没有时返回-1

int p3 = str1.rfind(str);  //从最右边开始返回str1中首次出现str首字母的下标，没有时返回-1

int p4 = str1.rfind(str,3);  //下标3开始(包括s1[3])返回str1中首次出现str首字母的下标，没有时返回-1

string str3 = "1234.567" ;

double nums = atof(str3.c_str());  //将str3转换为float类型

int nums = atoi(str3.c_str());  //将str3转换为int类型
```

---

### 6.3 迭代器
```java


string s = "abcd";
cout << s[0] << endl;
cout << s.front() << endl;
cout << *s.begin() << endl;

cout << s[s.size() - 1] << endl;
cout << s.back() << endl;
cout << * -- s.end() << endl;
```

---

## 7\. pair

---

### 7.1 声明

`pair` 是标准库中定义的一个类模板。用于将两个变量关联在一起，组成一个“对”，而且两个变量的数据类型可以是不同的。
```java


pair&lt;int, int&gt; a;
pair&lt;int, int&gt; b = {1, 2};
pair&lt;int, double&gt; c; c.first = 1, c.second = 2.333;
pair&lt;int, int&gt; d[100];
```

---

### 7.2 常用操作

在 `pair` 里已经预先定义了所有的比较运算符，包括 `<`、`>`、`<=`、`>=`、`==`、`!=`。当然，这需要组成 `pair` 的两个变量所属的数据类型定义了 `==` 和/或 `<` 运算符。

其中，`<`、`>`、`<=`、`>=` 四个运算符会先比较两个 `pair` 中的第一个变量，在第一个变量相等的情况下再比较第二个变量。
```java


pair&lt;int, string&gt; name[10];

    name[0] = {3, "lys"};
    name[1] = {2, "hfcj"};
    name[2] = {3, "wjq"};

    sort(name, name + 3);

    for(int i = 0; i < 3; i ++){
        cout << name[i].first << ' ' << name[i].second << endl;
    }
```

**Tips** :

很多情况下，`map` 中存储的键值对通过 `pair` 向外暴露。

---

## 8\. lower_bound/upper_bound

---
```java


int a[100] = {0};
for(int i = 0; i < 10; i ++) a[i] = i + 1; 

sort(a, a + 10);                             //按从小到大排序 

int pos1 = lower_bound(a, a + 10, 7) - a;    //返回数组中第一个大于或等于被查数的值的下标 
int pos2 = upper_bound(a, a + 10, 7) - a;    //返回数组中第一个大于被查数的值的下标

cout << pos1 << ' ' << a[pos1] << endl;
cout << pos2 << ' ' << a[pos2] << endl;

sort(a, a + 10, greater&lt;int&gt;());                           //按从大到小排序

int pos3 = lower_bound(a, a + 10, 7, greater&lt;int&gt;()) - a;  //返回数组中第一个小于或等于被查数的值的下标 
int pos4 = upper_bound(a, a + 10, 7, greater&lt;int&gt;()) - a;  //返回数组中第一个小于被查数的值的下标

cout << pos3 << ' ' << a[pos3] <<endl;
cout << pos4 << ' ' << a[pos4] <<endl;
```

**Tips** ：

  * 适用 `vector` 返回对应元素的迭代器。
  * 适用 `map` 返回对应 `key` 的迭代器。
  * 在一般的数组和 `vector` 里，这两个函数的时间复杂度均为 $\mathcal{O}(\log n)$，但在 `set/map` 等关联式容器中，直接调用 `lower_bound(s.begin(),s.end(),val)` 的时间复杂度是 $\mathcal{O}(n)$ 的。
  * 为此 `set/map` 等关联式容器中已经封装了 `lower_bound` 等函数（像 `s.lower_bound(val)` 这样），这样调用的时间复杂度是 $\mathcal{O}(\log n)$ 的。



---

## 9\. next_permutation

---

**作用** ：

  * 将当前排列更改为全排列中的下一个排列。
  * 如果当前排列已经是全排列中的最后一个排列（元素完全从大到小排列），函数返回 `false` 并将排列更改为全排列中的第一个排列（元素完全从小到大排列）；否则，函数返回 `true`。


```java


int a[] = {1, 2, 3, 4, 5};
    do{
      for(int i = 0; i < 5; i ++) cout << a[i] << " ";
      cout << endl;
    }while(next_permutation(a, a + 5));


vector&lt;int&gt; a = {1, 2, 3, 4, 5};
    do{
      for(int i = 0; i < a.size(); i ++) cout << a[i] << " ";
      cout << endl;
    }while(next_permutation(a.begin(), a.end()));
```

---

## 10\. 参考资料&了解更多

---

  * [cppreference](&lt;https://zh.cppreference.com/w/%E9%A6%96%E9%A1%B5&gt;)
  * [OI-Wiki](&lt;https://oi-wiki.org/lang/csl/container/&gt;)



---
