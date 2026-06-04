---
title: "ZooKeeper 高级应用"
date: 2023-12-30
categories: [Software Architect]
description: ""
---

### 概述

---

ZooKeeper 是 Apache 软件基金会的一个软件项目，它为大型分布式计算提供开源的**分布式配置服务**、**同步服务**和**命名注册**，在架构上，通过**冗余服务**实现高可用性（CP）。

ZooKeeper 的设计目标是将那些复杂且容易出错的分布式一致性服务封装起来，构成一个高效可靠的原语集，并以一系列简单易用的接口提供给用户使用。

---

## 基础回顾

---

### 数据结构

---

ZooKeeper 本身是一个树形目录服务（名称空间），非常类似于标准文件系统，以 `key-value` 的形式存储。名称 `key` 由斜线 `/` 分割的一系列路径元素，例如：`/node`，ZooKeeper 名称空间中的每个节点都是由一个路径来标识的。

**注意**：

*   每个路径下的节点 `key`（完整路径，名称）是唯一的，即同一级节点 `key` 名称是唯一的
    *   每个节点中存储了节点 `value` 和对应的状态属性，其中属性可能有多个

**节点类型**：

*   PERSISTENT：默认创建节点的类型，持久的节点
    *   PERSISTENT_SEQUENTIAL：持久顺序节点，会在路径后加上单调递增的后缀，适用于分布式锁和分布式选举，创建时添加 -s 参数
    *   EPHEMERAL：临时节点（不可拥有子节点），和会话绑定，断开服务后自动失效，创建时添加 -e 参数
    *   EPHEMERAL_SEQUENTIAL：临时顺序节点（不可再拥有子节点），会加上后缀，会话断开后删除，创建时添加 -e -s 参数
    *   CONTAINER：容器节点，当子节点都被删除后，Container 也随即删除，创建时添加 -c 参数
    *   PERSISTENT_WITH_TTL：如果该节点在 TTL 内没有被修改或没有子节点则过期删除，创建时添加 -t 参数

---

### 基础操作

---

节点操作的基础命令：

*   `ls`：查看某个路径下目录列表，可选参数 -s 返回状态信息，-w 监听节点变化，-R 递归查看某路径下目录列表
    *   `create`：创建节点并赋值，可选参数和节点的类型相对应，注意临时节点不能创建子节点
    *   `set`：修改节点存储的数据
    *   `get`：获取节点数据和状态信息，可选参数 -s 返回状态信息，-w 返回数据并对节点进行事件监听
    *   `stat`：查看节点状态信息，也可选 -w 参数
    *   `delete/deleteall`：删除某节点，如果某节点不为空，则不能用 `delete` 命令删除

**注意**：-w 监听节点只能生效一次，在节点信息变化后返回变化信息并失效

---

## 分布式锁

---

### 原理实现

---

ZooKeeper 实现简单的分布式锁：

*   注册临时节点，谁注册成功谁获取锁，其他监听该节点的删除事件
    *   一旦该临时节点被删除，通知其他客户端，再次重复该流程

但是上述方式存在问题——羊群效应：

*   当临时节点释放时，会通知到所有监听该节点的服务
    *   多个服务又会同时发起重新注册的请求，导致 ZooKeeper 服务压力较大

---

### 高级实现

---

为了解决上面产生的问题，我们给出更为完善的方案：

所有服务注册临时顺序节点，并写入基本信息。
所有服务获取节点列表并判断自己的节点是否为最小的节点，如果是则表示获取到了锁。
未获取锁的客户端监听前一个节点的删除事件。
当锁被释放或持有锁的客户端宕机后，节点被删除，下一个节点的客户端收到通知，并重复上述流程。

基于上述解决方案，我们将临时顺序节点的创建进行细分，分为读锁节点和写锁节点：
对于读锁节点，只需要关心前一个写锁节点的释放。
对于写锁节点，只需要关心前一个节点的释放，而不需要关心前一个节点是写锁节点还是读锁节点。

这样就基于 ZooKeeper 实现了共享锁和排他锁。在使用时，一般利用 Curator 客户端实现：

```java
import org.apache.curator.RetryPolicy;
import org.apache.curator.framework.CuratorFramework;
import org.apache.curator.framework.CuratorFrameworkFactory;
import org.apache.curator.framework.recipes.locks.InterProcessLock;
import org.apache.curator.framework.recipes.locks.InterProcessSemaphoreMutex;
import org.apache.curator.retry.ExponentialBackoffRetry;
import org.apache.curator.utils.CloseableUtils;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;

public class DistributedLockDemo {

    // ZooKeeper 锁节点路径，分布式锁的相关操作都是在这个节点上进行
    private final String lockPath = "/distributed-lock";

    // ZooKeeper 服务地址，单机格式为：(127.0.0.1:2181)，
    // 集群格式为：(127.0.0.1:2181,127.0.0.1:2182,127.0.0.1:2183)
    private String connectString;

    // Curator 客户端重试策略
    private RetryPolicy retry;

    // Curator 客户端对象
    private CuratorFramework client;

    // client2 用于模拟其他客户端
    private CuratorFramework client2;

    // 初始化资源
    @Before
    public void init() throws Exception {
        // 设置 ZooKeeper 服务地址为本机的 2181 端口
        connectString = "192.168.200.168:2181";
        // 重试策略
        // 初始休眠时间为 1000ms, 最大重试次数为 3
        retry = new ExponentialBackoffRetry(1000, 3);
        // 创建一个客户端, 60000(ms)为 session 超时时间, 15000(ms)为连接超时时间
        client = CuratorFrameworkFactory.newClient(connectString, 60000, 15000, retry);
        client2 = CuratorFrameworkFactory.newClient(connectString, 60000, 15000, retry);
        // 创建会话
        client.start();
        client2.start();
    }

    // 释放资源
    @After
    public void close() {
        CloseableUtils.closeQuietly(client);
    }

    @Test
    public void sharedLock() throws Exception {
        // 创建共享锁
        final InterProcessLock lock = new InterProcessSemaphoreMutex(client, lockPath);
        // lock2 用于模拟其他客户端
        final InterProcessLock lock2 = new InterProcessSemaphoreMutex(client2, lockPath);

        new Thread(new Runnable() {

            @Override
            public void run() {
                // 获取锁对象
                try {
                    lock.acquire();
                    System.out.println("======== client1 get lock ========");
                    // 测试锁重入
                    Thread.sleep(5 * 1000);
                    lock.release();
                    System.out.println("======== client1 release lock ========");
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }).start();

        new Thread(new Runnable() {
            @Override
            public void run() {
                // 获取锁对象
                try {
                    lock2.acquire();
                    System.out.println("======== client2 get lock ========");
                    Thread.sleep(5 * 1000);
                    lock2.release();
                    System.out.println("======== client2 release lock ========");
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }).start();

        Thread.sleep(20 * 1000);
    }
}
```

*   `InterProcessMutex`：分布式可重入排它锁（可重入可以借助 `LocalMap` 存计数器）
*   `InterProcessSemaphoreMutex`：分布式排它锁
*   `InterProcessMultiLock`：将多个锁作为单个实体管理的容器
*   `InterProcessReadWriteLock`：分布式读写锁

---

## 集群应用

---

### 集群节点配置

---

对于搭建 ZooKeeper 集群的节点往往采用**奇数** 个：

*   保证容错：需要保证集群能够有半数进行投票，例如：
    ```java
    // 三台集群，至少 2 台正常运行才行（3的半数为 1.5，半数以上最少为 2）
    // 因此，正常运行可以允许 1 台服务器挂掉
    ```
*   防止脑裂：需要保证集群在通信不可达的情况下分裂产生小集群，例如：
    ```java
    // 3 台集群，投票选举半数为 1.5，1 台服务裂开，和另外 2 台服务器无法通信
    // 这时候 2 台服务器的集群（2票大于半数1.5票），所以可以选举出leader，而 1 台服务器的集群无法选举
    ```

综上可知，搭建集群所需的最少节点配置为 3，如果是 4 台，则发生脑裂时会造成没有 leader 节点的错误。

---

### 选举算法

---

ZooKeeper 采用的是基于 Paxos 算法的 ZAB 协议，这里先提一下 Paxos 算法：

*   Paxos 是一个分布式选举算法，该算法定义了三种角色：
    *   Proposer：提案发起者
    *   Acceptor：提案接收者，可同意或不同意
    *   Learners：虽然不同意提案，但也只能被动接收学习；或者是后来的，只能被动接受
    *   该算法的提案遵循少数服从多数的原则，即过半原则

ZAB 协议在 Paxos 算法基础上进行了扩展，全称为原子消息广播协议（ZooKeeper Atomic Broadcast）。

ZAB 协议支持原子广播、崩溃恢复，保证 Leader 广播的变更序列被顺序地处理，该协议下的节点有四种状态：
- LOOKING：系统刚启动时或者 Leader 崩溃后正处于选举状态
- FOLLOWING：表示 Follower 节点所处的状态，同步 Leader 状态，参与投票
- LEADING：表示 Leader 所处状态
- OBSERVING：观察状态，同步 Leader 状态，不参与投票

该算法下，也遵循过半原则。

我们查看 ZooKeeper 的源码，在 `FastLeaderElection.java` 中：

```java
protected boolean totalOrderPredicate(long newId, long newZxid, long newEpoch, long curId, long curZxid, long curEpoch) {
    LOG.debug(
        "id: {}, proposed id: {}, zxid: 0x{}, proposed zxid: 0x{}",
        newId,
        curId,
        Long.toHexString(newZxid),
        Long.toHexString(curZxid));

    if (self.getQuorumVerifier().getWeight(newId) == 0) {
        return false;
    }

    /*
     * We return true if one of the following three cases hold:
     * 1- New epoch is higher
     * 2- New epoch is the same as current epoch, but new zxid is higher
     * 3- New epoch is the same as current epoch, new zxid is the same
     *  as current zxid, but server id is higher.
     */
    /*
     * 对应上面代码的解释（两个节点之间使用比较的方法来决定选票给谁，三种比较规则）：
     * 1- 比较 epoch（zxid 高 32 位）：
     *     如果其他节点的 epoch 比自己的大，选举 epoch 大的节点（理由：epoch 表示年代【投票次数越多，数据越新】，epoch 越大表示数据越新）。
     *     代码：(newEpoch > curEpoch)；
     * 2- 比较 zxid：
     *     如果纪元相同，就比较两个节点的 zxid 的大小，选举 zxid 大的节点（理由：zxid 表示节点所提交事务最大的 id，zxid 越大代表该节点的数据越完整）。
     *     代码：(newEpoch == curEpoch) && (newZxid > curZxid)；
     * 3- 比较 serverId：
     *     如果 epoch 和 zxid 都相等，就比较服务的 serverId，选举 serverId 大的节点（理由：serverId 表示机器性能，它是在配置 ZooKeeper 集群时确定的，因此我们在配置 ZooKeeper 集群时可以将性能更高的服务器的 serverId 设置得大些，让性能好的机器担任 leader 角色）。
     *     代码：(newEpoch == curEpoch) && ((newZxid == curZxid) && (newId > curId))。
     */
    return ((newEpoch > curEpoch)
            || ((newEpoch == curEpoch)
                && ((newZxid > curZxid)
                    || ((newZxid == curZxid)
                        && (newId > curId)))));
}
```

---

### 集群数据读写

---

**读请求**：

*   当 Client 向 ZooKeeper 发出读请求时
    *   无论是 Leader 还是 Follower，都直接返回查询结果

**写请求 - Leader**：

*   Client 向 Leader 发出写请求时
    *   Leader 将数据写入本节点，并将数据发送到所有 Follower 节点，然后等待返回；
    *   当 Leader 收到过半节点（包含自身）返回的写成功信息后，直接向 Client 返回成功。

**写请求 - Follower**：

*   Client 向 Follower 发出写请求时
    *   Follower 将请求转发给 Leader；
    *   Leader 将数据写入本节点，并将数据发送到所有 Follower 节点，然后等待返回；
    *   当 Leader 收到过半节点（包含自身）返回的写成功信息后，向发起转发的 Follower 返回成功；
    *   Follower 收到 Leader 的成功响应后，再向 Client 返回成功。