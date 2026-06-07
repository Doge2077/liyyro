---
title: "JDK源码系列（三）"
date: 2024-10-29
categories: [Software Architect]
description: ""
---

# jdk源码系列（三）


## HashMap 类

---

### 基础概念

---

#### 定义

---

Hash 表也称为散列表，也有直接译作哈希表。Hash 表是一种根据键值对（Key-Value）直接进行访问的数据结构。

哈希表通过把键值映射到表中一个位置来访问记录，从而加快查找的速度。这个映射函数叫做**散列函数**，存放记录的数组叫做**散列表**，查找的时间复杂度为 **O(1)**。

HashMap 的实现不是同步的，这意味着它不是**线程安全**的。它的 key、value 都可以为 null，但 HashMap 中的映射不是有序的。

**注意**：

* 散列函数可能存在冲突，解决冲突有两种方法：
  * 开放寻址法：从冲突的位置开始，向后查找第一个可以插入的位置。
  * 拉链法：在冲突的位置后面追加节点，使之成为链表。

由于开放寻址法可能造成二次冲突，因此大多情况下采用拉链法解决。

---

#### 版本对比

---

##### JDK 8 之前 HashMap 的数据结构

---

* JDK 8 以前 HashMap 的实现是**数组 + 链表**。即使哈希函数取得再好，也很难达到元素百分百均匀分布。
  * 当 HashMap 中有大量的元素都存放到同一个桶中时，这个桶下会有一条长长的链表。极端情况下，HashMap 就相当于一个单链表。假如单链表有 n 个元素，遍历的时间复杂度就是 O(n)，完全失去了它的优势。

![](https://cdn.jsdelivr.net/gh/Doge2077/liyyro-photo@main/images/2024/10/image-20220221182804565.png)

---

##### JDK 8 之后 HashMap 的数据结构

---

* JDK 8 之后 HashMap 的实现是**数组 + 链表 + 红黑树**。
  * 桶中的结构可能是链表，也可能是红黑树。当**链表长度大于阈值**（默认为 8）并且**当前数组的长度大于 64** 时，此索引位置上的所有数据将改为使用红黑树存储。

![](https://cdn.jsdelivr.net/gh/Doge2077/liyyro-photo@main/images/2024/10/image-20220224112415112.png)

---

### 类构造器

```java
public class HashMap<K,V> extends AbstractMap<K,V>
    implements Map<K,V>, Cloneable, Serializable {
```

![](https://cdn.jsdelivr.net/gh/Doge2077/liyyro-photo@main/images/2024/10/image-20220222100327933.png)

JDK 为我们提供了一个抽象类 AbstractMap，该抽象类实现了 Map 接口。因此，如果我们不想实现所有的 Map 接口方法，就可以选择继承抽象类 AbstractMap。

HashMap 集合实现了 Cloneable 接口以及 Serializable 接口，分别用于对象克隆以及序列化。

**注意**：HashMap 类既继承了 AbstractMap 抽象类，也实现了 Map 接口，这样做的主要目的是为了确保同时满足抽象类和接口的规范要求。

> 据 Java 集合框架的创始人 Josh Bloch 描述，这样的写法是一个失误。在 Java 集合框架中，类似这样的写法很多，最开始写 Java 集合框架的时候，他认为这样写，在某些地方可能是有价值的，直到他意识到错了。显然地，JDK 的维护者后来不认为这个小小的失误值得去修改，所以就这样存在下来了。

---

### 字段属性

---
```java

//序列化和反序列化时，通过该字段进行版本一致性验证
private static final long serialVersionUID = 362498820763181265L;
//默认 HashMap 集合初始容量为16（必须是 2 的倍数）
static final int DEFAULT_INITIAL_CAPACITY = 1 << 4; // aka 16
//集合的最大容量，如果通过带参构造指定的最大容量超过此数，默认还是使用此数
static final int MAXIMUM_CAPACITY = 1 << 30;
//默认的填充因子
static final float DEFAULT_LOAD_FACTOR = 0.75f;
//当桶(bucket)上的节点数大于这个值时会转成红黑树(JDK1.8新增)
static final int TREEIFY_THRESHOLD = 8;
//当桶(bucket)上的节点数小于这个值时会转成链表(JDK1.8新增)
static final int UNTREEIFY_THRESHOLD = 6;
/** (JDK1.8新增)
 * 当集合中的容量大于这个值时，表中的桶才能进行树形化，否则桶内元素太多时会扩容，
 * 而不是树形化。为了避免进行扩容、树形化选择的冲突，这个值不能小于 4 * TREEIFY_THRESHOLD
 */
static final int MIN_TREEIFY_CAPACITY = 64;

/**
 * 初始化使用，长度总是 2 的幂
 */
transient Node<K,V>[] table;

/**
 * 保存缓存的 entrySet（）
 */
transient Set<Map.Entry<K,V>> entrySet;

/**
 * 此映射中包含的键值映射的数量。（集合存储键值对的数量）
 */
transient int size;

/**
 * 跟前面 ArrayList 和 LinkedList 集合中的字段 modCount 一样，记录集合被修改的次数
 * 主要用于迭代器中的快速失败
 */
transient int modCount;

/**
 * 调整大小的下一个大小值（容量 * 加载因子）。capacity * load factor
 */
int threshold;

/**
 * 散列表的加载因子。
 */
final float loadFactor;
```

下面我们重点介绍上面几个字段：

* `Node&lt;K,V&gt;[] table`：
```java
* 我们说 HashMap 是由数组 + 链表 + 红黑树组成，这里的数组就是 table 字段
* 初始化长度默认是 DEFAULT_INITIAL_CAPACITY = 16，且 JDK 声明数组的长度总是 2 的 n 次方（一定是合数）
```
* `size`：
```java
* 集合中存放 key-value 的实时对数
```
* `loadFactor`：
```java
* 装载因子，是用来衡量 HashMap 满的程度
* 计算 HashMap 的实时装载因子的方法是：size/capacity，而不是占用桶的数量去除以 capacity
* capacity 是桶的数量，也就是 table 的长度 length
* 默认的负载因子 0.75 是对空间和时间效率的一个平衡选择，建议不要修改，除非在时间和空间比较特殊的情况下，如果内存空间很多而又对时间效率要求很高，可以降低负载因子 loadFactor 的值；相反，如果内存空间紧张而对时间效率要求不高，可以增加负载因子 loadFactor 的值，这个值可以大于 1。
```
* `threshold`：
```java
* 计算公式：capacity * loadFactor
* 这个值是当前已占用数组长度的最大值。超过这个数目就重新 resize（扩容），扩容后的 HashMap 容量是之前容量的两倍
```

---

### 构造函数

---

#### 默认无参构造函数
```java
/**
 * 默认构造函数，初始化加载因子 loadFactor = 0.75
 */
public HashMap() {
    this.loadFactor = DEFAULT_LOAD_FACTOR;
}
```

---

#### 指定初始容量的构造函数
```java
/**
*
* @param initialCapacity 指定初始化容量
* @param loadFactor 加载因子 0.75
*/
public HashMap(int initialCapacity, float loadFactor) {
    //初始化容量不能小于 0 ，否则抛出异常
    if (initialCapacity < 0)
        throw new IllegalArgumentException("Illegal initial capacity: " +
                                           initialCapacity);
    //如果初始化容量大于2的30次方，则初始化容量都为2的30次方
    if (initialCapacity > MAXIMUM_CAPACITY)
        initialCapacity = MAXIMUM_CAPACITY;
    //如果加载因子小于0，或者加载因子是一个非数值，抛出异常
    if (loadFactor <= 0 || Float.isNaN(loadFactor))
        throw new IllegalArgumentException("Illegal load factor: " +
                                           loadFactor);
    this.loadFactor = loadFactor;
    this.threshold = tableSizeFor(initialCapacity);
}
// 返回大于等于initialCapacity的最小的二次幂数值。
// >>> 操作符表示无符号右移，高位补0。
// | 按位或运算
static final int tableSizeFor(int cap) {
    int n = cap - 1;
    n |= n >>> 1;
    n |= n >>> 2;
    n |= n >>> 4;
    n |= n >>> 8;
    n |= n >>> 16;
    return (n < 0) ? 1 : (n >= MAXIMUM_CAPACITY) ? MAXIMUM_CAPACITY : n + 1;
}
```

---

### 确定哈希桶数组索引位置

---

前面我们讲解哈希表的时候，我们知道是用散列函数来确定索引的位置。

散列函数设计得越好，使得元素分布得越均匀。

HashMap 是数组+链表+红黑树的组合，我们希望在有限个数组位置时，尽量每个位置的元素只有一个，那么当我们用散列函数求得索引位置的时候，我们能马上知道对应位置的元素是不是我们想要的，而不是要进行链表的遍历或者红黑树的遍历，这会大大优化我们的查询效率。

我们看 HashMap 中的哈希算法：
```java

static final int hash(Object key) {
    int h;
    return (key == null) ? 0 : (h = key.hashCode()) ^ (h >>> 16);
}

i = (table.length - 1) & hash;//这一步是在后面添加元素putVal()方法中进行位置的确定
```

主要分为三步：

* 取 hashCode 值： key.hashCode()
* 高位参与运算：h >>> 16
* 取模运算：(n-1) & hash

这里获取的 hashCode() 值是变量，但是我们知道，对于任意给定的对象，只要它的 hashCode() 返回值相同，那么程序调用 hash(Object key) 所计算得到的哈希码值总是相同的。

为了让数组元素分布均匀，我们首先想到的是把获得的哈希码对数组长度取模运算（hash % length），但是计算机都是二进制进行操作，取模运算相对开销还是很大的，那该如何优化呢？

HashMap 使用的方法很巧妙，它通过 hash & (table.length - 1) 来得到该对象的保存位。前面说过 HashMap 底层数组的长度总是 2 的 n 次方，这是 HashMap 在速度上的优化：

* 当 length 总是 2 的 n 次方时，hash & (length - 1) 运算等价于对 length 取模，也就是 hash % length
* 但是 & 比 % 具有更高的效率，比如 n % 32 = n & (32 - 1)

在 JDK 1.8 中还有另一个优化点，高位参与运算。hashCode() 得到的是一个 32 位 int 类型的值，是通过 hashCode() 的高 16 位**异或**低 16 位实现的：

* (h = k.hashCode()) ^ (h >>> 16)，主要是从速度、功效、质量来考虑的
* 这么做可以在数组 table 的 length 比较小的时候，也能保证考虑到高低 bit 都参与到哈希的计算中，同时不会有太大的开销

最后一点：

* 当 length 为 2 的 n 次方时，参与计算时 length - 1 的最低一位是 1
* 因此，hashcode 和 length - 1 做 & 运算时，最后一位的结果取决于 hashcode 的最后一位，可能是 0 或 1
* 这使得散列函数能够利用数组的全部空间，提高分布的均匀性

这也解释了为什么数组的长度必须是 2 的 n 次方。

---

### 添加元素

---

```java
//hash(key)就是上面讲的hash方法，对其进行了第一步和第二步处理
public V put(K key, V value) {
    return putVal(hash(key), key, value, false, true);
}
```

```java
/**
 * @param hash 索引的位置
 * @param key  键
 * @param value 值
 * @param onlyIfAbsent true 表示不要更改现有值
 * @param evict false 表示 table 处于创建模式
 * @return
 */
final V putVal(int hash, K key, V value, boolean onlyIfAbsent,
               boolean evict) {
    Node<K,V>[] tab; Node<K,V> p; int n, i;
    // 如果 table 为 null 或者长度为 0，则进行初始化
    // resize() 方法本来是用于扩容，由于初始化没有实际分配空间，这里用该方法进行空间分配，后面会详细讲解该方法
    if ((tab = table) == null || (n = tab.length) == 0)
        n = (tab = resize()).length;
    // 注意：这里用到了前面讲解获得 key 的 hash 码的第三步，取模运算，下面的 if-else 分别是 tab[i]（数组桶）为 null 和不为 null
    if ((p = tab[i = (n - 1) & hash]) == null)
        tab[i] = newNode(hash, key, value, null); // tab[i] 为 null，直接将新的 key-value 插入到计算的索引 i 位置
    else { // tab[i] 不为 null，表示该位置已经有值了
        Node<K,V> e; K k;
        if (p.hash == hash &&
            ((k = p.key) == key || (key != null && key.equals(k))))
            e = p; // 节点 key 已经有值了，直接用新值覆盖
        // 该链是红黑树
        else if (p instanceof TreeNode)
            e = ((TreeNode<K,V>)p).putTreeVal(this, tab, hash, key, value);
        // 该链是链表
        else {
            for (int binCount = 0; ; ++binCount) {
                if ((e = p.next) == null) {
                    p.next = newNode(hash, key, value, null);
                    // 链表长度大于 8，转换成红黑树
                    if (binCount >= TREEIFY_THRESHOLD - 1) // -1 for 1st
                        treeifyBin(tab, hash);
                    break;
                }
                // key 已经存在，直接覆盖 value
                if (e.hash == hash &&
                    ((k = e.key) == key || (key != null && key.equals(k))))
                    break;
                p = e;
            }
        }
        if (e != null) { // existing mapping for key
            V oldValue = e.value;
            if (!onlyIfAbsent || oldValue == null)
                e.value = value;
            afterNodeAccess(e);
            return oldValue;
        }
    }
    ++modCount; // 用于并发修改的快速失败
    if (++size > threshold) // 超过最大容量，进行扩容
        resize();
    afterNodeInsertion(evict);
    return null;
}
```

①、判断键值对数组 table 是否为空或为null，如果是，则执行resize()进行扩容；

②、根据键key计算hash值得到插入的数组索引i，如果table[i]==null，直接新建节点添加，转向⑥，如果table[i]不为空，转向③；

③、判断table[i]的首个元素是否和key一样，如果相同直接覆盖value，否则转向④，这里的相同指的是hashCode以及equals；

④、判断table[i] 是否为treeNode，即table[i] 是否是红黑树，如果是红黑树，则直接在树中插入键值对，否则转向⑤；

⑤、遍历table[i]，判断链表长度是否大于8，大于8的话把链表转换为红黑树，在红黑树中执行插入操作，否则进行链表的插入操作；遍历过程中若发现key已经存在直接覆盖value即可；

⑥、插入成功后，判断实际存在的键值对数量size是否超过了阈值threshold，如果超过，进行扩容。

⑦、如果新插入的key不存在，则返回null，如果新插入的key存在，则返回原key对应的value值（注意新插入的value会覆盖原value值）

**注意** ：
```java

if (++size > threshold)//超过最大容量，进行扩容
    resize();
```

如果在添加元素时，发生冲突，会将冲突的元素放在链表上，当链表长度超过 8 时，会自动转换成红黑树

---

### 扩容机制

---

扩容（resize），我们知道集合是由数组+链表+红黑树构成，向 HashMap 中插入元素时，如果HashMap 集合的元素已经大于最大承载容量threshold（capacity * loadFactor），这里的threshold不是数组的最大长度。那么必须扩大数组的长度，Java中数组是无法自动扩容的，我们采用的方法是用一个更大的数组代替这个小的数组，然后将小数组里面的元素向大数组转移。

JDK1.8融入了红黑树的机制，比较复杂，这里我们先介绍 JDK1.7的扩容源码，便于理解，然后再介绍JDK1.8的源码。
```java

//参数 newCapacity 为新数组的大小
void resize(int newCapacity) {
    Entry[] oldTable = table;//引用扩容前的 Entry 数组
    int oldCapacity = oldTable.length;
    if (oldCapacity == MAXIMUM_CAPACITY) {//扩容前的数组大小如果已经达到最大(2^30)了
        threshold = Integer.MAX_VALUE;//修改阈值为int的最大值(2^31-1)，这样以后就不会扩容了
        return;
    }

    Entry[] newTable = new Entry[newCapacity];//初始化一个新的Entry数组
    transfer(newTable, initHashSeedAsNeeded(newCapacity));//将数组元素转移到新数组里面
    table = newTable;
    threshold = (int)Math.min(newCapacity * loadFactor, MAXIMUM_CAPACITY + 1);//修改阈值
}

void transfer(Entry[] newTable, boolean rehash) {
    int newCapacity = newTable.length;
    for (Entry<K,V> e : table) {//遍历数组
        while(null != e) {
            Entry<K,V> next = e.next;
            if (rehash) {
                e.hash = null == e.key ? 0 : hash(e.key);
            }
            int i = indexFor(e.hash, newCapacity);//重新计算每个元素在数组中的索引位置
            e.next = newTable[i];//标记下一个元素，添加是链表头添加
            newTable[i] = e;//将元素放在链上
            e = next;//访问下一个 Entry 链上的元素
        }
    }
}
```

从这个方法中我们可以看到，JDK1.7中首先是创建一个新的大容量数组，然后依次重新计算原数组中所有元素的索引，并重新赋值。如果数组某个位置发生了哈希冲突，使用的是单链表的头插入方法，同一位置的新元素总是放在链表的头部，这样与原数组中的链表对比，扩容之后的链表可能就会变成倒序的了。

下面我们再看看JDK1.8的：
```java
final Node<K,V>[] resize() {
    Node<K,V>[] oldTab = table;
    int oldCap = (oldTab == null) ? 0 : oldTab.length; // 原数组如果为null，则长度赋值0
    int oldThr = threshold;
    int newCap, newThr = 0;
    if (oldCap > 0) { // 如果原数组长度大于0
        if (oldCap >= MAXIMUM_CAPACITY) { // 数组大小如果已经大于等于最大值(2^30)
            threshold = Integer.MAX_VALUE; // 修改阈值为int的最大值(2^31-1)，这样以后就不会扩容了
            return oldTab;
        }
        // 原数组长度大于等于初始化长度16，并且原数组长度扩大1倍也小于2^30次方
        else if ((newCap = oldCap << 1) < MAXIMUM_CAPACITY &&
                 oldCap >= DEFAULT_INITIAL_CAPACITY)
            newThr = oldThr << 1; // 阈值扩大1倍
    }
    else if (oldThr > 0) // 旧阈值大于0，则将新容量直接等于旧阈值
        newCap = oldThr;
    else { // 阈值等于0，oldCap也等于0（集合未进行初始化）
        newCap = DEFAULT_INITIAL_CAPACITY; // 数组长度初始化为16
        newThr = (int)(DEFAULT_LOAD_FACTOR * DEFAULT_INITIAL_CAPACITY); // 阈值等于16*0.75=12
    }
    // 计算新的阈值上限
    if (newThr == 0) {
        float ft = (float)newCap * loadFactor;
        newThr = (newCap < MAXIMUM_CAPACITY && ft < (float)MAXIMUM_CAPACITY ?
                  (int)ft : Integer.MAX_VALUE);
    }
    threshold = newThr;
    @SuppressWarnings({"rawtypes","unchecked"})
    Node<K,V>[] newTab = (Node<K,V>[])new Node[newCap];
    table = newTab;
    if (oldTab != null) {
        // 把每个bucket都移动到新的buckets中
        for (int j = 0; j < oldCap; ++j) {
            Node<K,V> e;
            if ((e = oldTab[j]) != null) {
                oldTab[j] = null; // 原数据j位置置为null，便于垃圾回收
                if (e.next == null) // 数组没有下一个引用（不是链表）
                    newTab[e.hash & (newCap - 1)] = e;
                else if (e instanceof TreeNode) // 红黑树
                    ((TreeNode<K,V>)e).split(this, newTab, j, oldCap);
                else { // preserve order
                    Node<K,V> loHead = null, loTail = null;
                    Node<K,V> hiHead = null, hiTail = null;
                    Node<K,V> next;
                    do {
                        next = e.next;
                        // 原索引
                        if ((e.hash & oldCap) == 0) {
                            if (loTail == null)
                                loHead = e;
                            else
                                loTail.next = e;
                            loTail = e;
                        }
                        // 原索引+oldCap
                        else {
                            if (hiTail == null)
                                hiHead = e;
                            else
                                hiTail.next = e;
                            hiTail = e;
                        }
                    } while ((e = next) != null);
                    // 原索引放到bucket里
                    if (loTail != null) {
                        loTail.next = null;
                        newTab[j] = loHead;
                    }
                    // 原索引+oldCap放到bucket里
                    if (hiTail != null) {
                        hiTail.next = null;
                        newTab[j + oldCap] = hiHead;
                    }
                }
            }
        }
    }
    return newTab;
}
```

该方法分为两部分，首先是计算新桶数组的容量 newCap 和新阈值 newThr，然后将原集合的元素重新映射到新集合中。

相比于 JDK1.7，1.8 使用的是 2 的幂次扩展（指长度扩为原来的 2 倍），因此，元素的位置要么是在原位置，要么是在原位置加上原容量（oldCap）的偏移处。

我们在扩充 HashMap 的时候，不需要像 JDK1.7 的实现那样重新计算 hash，只需要看看原来的 hash 值新增的那个 bit 是 1 还是 0 就好了，是 0 的话索引没变，是 1 的话索引变成“原索引 + oldCap”。

---

### 删除元素

---

HashMap 删除元素首先是要找到桶的位置，之后进行判断：

* 如果是链表，则进行链表遍历，找到需要删除的元素后，进行删除。
* 如果是红黑树，则进行树的遍历，找到元素删除后，进行平衡调节。注意，当红黑树的节点数小于 6 时，会退化为链表。

```java
public V get(Object key) {
    Node<K,V> e;
    return (e = getNode(hash(key), key)) == null ? null : e.value;
}

final Node<K,V> getNode(int hash, Object key) {
    Node<K,V>[] tab; Node<K,V> first, e; int n; K k;
    if ((tab = table) != null && (n = tab.length) > 0 &&
        (first = tab[(n - 1) & hash]) != null) {
        // 根据 key 计算的索引，检查该位置上的第一个节点
        if (first.hash == hash && // always check first node
            ((k = first.key) == key || (key != null && key.equals(k))))
            return first;
        // 如果第一个节点不是目标，继续查找后续节点
        if ((e = first.next) != null) {
            // 如果第一个节点是树节点，则进入红黑树查找
            if (first instanceof TreeNode)
                return ((TreeNode<K,V>)first).getTreeNode(hash, key);
            // 否则，遍历链表查找
            do {
                if (e.hash == hash &&
                    ((k = e.key) == key || (key != null && key.equals(k))))
                    return e;
            } while ((e = e.next) != null);
        }
    }
    return null;
}
```

---

### 查找元素

通过 key 查找 value：

首先通过 key 计算索引，找到桶位置。
  * 先检查桶中的第一个节点，如果匹配则直接返回。
  * 如果第一个节点不匹配，则判断其数据结构：若是红黑树则进入树中查找；否则，遍历其后的链表进行查找。
  * 如果遍历整个桶仍未找到，则返回 null。

```java
public V get(Object key) {
    Node<K,V> e;
    // 通过调用内部方法获取节点，若节点为空则返回null，否则返回其value。
    return (e = getNode(hash(key), key)) == null ? null : e.value;
}

final Node<K,V> getNode(int hash, Object key) {
    Node<K,V>[] tab; Node<K,V> first, e; int n; K k;
    // 1. 根据key的hash值，计算并获取对应的桶（数组元素）。
    if ((tab = table) != null && (n = tab.length) > 0 &&
        (first = tab[(n - 1) & hash]) != null) {
        // 2. 总是先检查桶的第一个节点。
        if (first.hash == hash &&
            ((k = first.key) == key || (key != null && key.equals(k))))
            return first;
        // 3. 如果第一个节点不是目标，则检查该桶的后续结构。
        if ((e = first.next) != null) {
            // 如果是红黑树结构，则进入树中进行查找。
            if (first instanceof TreeNode)
                return ((TreeNode<K,V>)first).getTreeNode(hash, key);
            // 如果是链表结构，则遍历链表进行查找。
            do {
                if (e.hash == hash &&
                    ((k = e.key) == key || (key != null && key.equals(k))))
                    return e;
            } while ((e = e.next) != null);
        }
    }
    // 4. 如果走到这里，说明没有找到匹配的节点，返回null。
    return null;
}
```

