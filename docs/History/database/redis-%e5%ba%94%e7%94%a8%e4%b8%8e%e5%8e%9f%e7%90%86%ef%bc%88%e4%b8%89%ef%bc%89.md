---
title: "Redis 应用与原理（三）"
date: 2024-03-20
categories: [DataBase System, Software Architect, Redis]
description: ""
---

# Redis Cluster 解决方案

* * *

## 基础概念

* * *

首先，分析一下主从+哨兵模式带来的问题：

![image-20240318202940569](https://image.itbaima.cn/images/40/image-20240318202378518.png)

  * 在主从 + 哨兵的模式下，仍然只有一个 Master 节点，当并发请求较大时，哨兵模式不能缓解写压力
  * 在 Sentinel 模式下，每个节点需要保存全量数据，无法进行海量数据存储



因此，在 Redis 3.0 之后，提供了 Cluster 的解决方案，核心原理是对数据做分片：

![image-20240318203511203](https://image.itbaima.cn/images/40/image-20240318202255799.png)

  * 采用无中心结构
  * 每个 master 可以有多个 slave 节点
  * 整个集群分片共有 16384 个哈希槽
  * 每个 key 通过 CRC16 校验后对 16384 取模来决定放置哪个槽，集群的每个节点负责一部分hash 槽
  * 当主节点不可用时，从节点会升级为主节点，原有主节点恢复后会降级为从节点



* * *

## Redis Cluster 集群策略

* * *

### 故障转移策略

* * *

![image-20240318204921709](https://image.itbaima.cn/images/40/image-20240318201010339.png)

和 Sentinel 类似，Cluster 也存在服务监控和选举规则：

  * 主观下线：和 Sentinel 一样采用心跳包检测，当一个节点不能从另一个节点接收到心跳信息，该节点会将它标记为“主观下线”状态
  * 客观下线：当半数以上的主节点都将某个节点标记为“主观下线”，那么这个节点会被标记为“客观下线”



当某个节点被标记为客观下线后，会从该主节点的从节点中选举一个从节点作为新的主节点：

  * 选举过程主要看从节点的复制偏移量（replica offset）和 runid
  * 优先选择复制偏移量最大的节点，如果复制偏移量相同，则选择 runid 最小的节点



**注意** ：

  * 若某一主节点及其从节点都不可用，则会导致整个 Redis Cluster 集群不可用



* * *

### 数据分片策略

* * *

#### 常见的数据分布策略

* * *

**顺序分布** ：

  * 根据数据的某些属性进行排序，将数据均匀地分配到不同的存储节点
  * 例如，将用户 ID 排序，分区间存入不同的节点



**一致性哈希** ：

  * 将整个哈希值空间组成一个虚拟的圆环，然后根据某种哈希算法将数据项映射到该圆环上
  * 例如对于 Redis，对节点 id 进行 hash，将其值分布在圆环上
  * 发生读写的 key 经过 hash 后，顺时针查圆环上的节点，若未找到，则默认为 0 位置后的第一个节点



如果采用一致性哈希算法，若某个节点挂了，受影响的数据仅仅是此节点到环空间前一个节点（沿着逆时针方向行走遇到的第一个节点）之间的数据，其它不受影响。增加一个节点也同理。

但是当删除节点时，数据再分配会把当前节点所有数据加到它的下一个节点上（缓存抖动）。这样会导致下一个节点使用率暴增，可能会导致挂掉，如果下一个节点挂掉，下下个节点将会承受更大的压力，最终导致集群雪崩。

* * *

#### Redis 哈希槽策略

* * *

Redis 并没有使用一致性哈希，而是采用哈希槽的方式进行分片

Redis 集群有16384个哈希槽，每个key通过CRC16校验后对16384取模来决定放置哪个槽：

![image-20240318215405104](https://image.itbaima.cn/images/40/image-20240318218022338.png)

> 理论上 CRC16 算法可以得到 $2^{16}$ 个数值，其数值范围在 0-65535 之间，取模运算 key 的时候，应该是CRC16(key)%65535，但是却设计为CRC16(key)%16384，原因是作者在设计的时候做了空间上的权衡，觉得节点最多不可能超过1000个，同时为了保证节点之间通信效率，所以采用了 $2^{14}$。

具体分片方式如下：

  * 把16384槽按照节点数量进行平均分配，由节点进行管理
  * 对每个key按照 CRC16规则进行 hash 运算
  * 把hash结果对 16383 进行取余
  * 把余数发送给 Redis 节点
  * 节点接收到数据，验证是否在自己管理的槽编号的范围 
    * 如果在自己的编号范围内，会把数据存储到数据槽中，返回执行结果
    * 否则，会把数据发送给正确的节点，由正确的节点来处理



**使用哈希槽的优势** ：

  * 由于一致性哈希会造成缓存抖动和集群雪崩，因此要在原有基础上进行扩容和删减节点变得极为困难
  * 使用哈希槽在新增节点时，只需要将其他节点的哈希槽分出一部分给新节点
  * 删除节点时，则将该节点的哈希槽再分配给别的节点，之后再删除节点即可



**注意** ：

  * Redis Cluster 节点之间共享消息，每个节点会知道哪个节点负责哪个数据槽
  * 添加节点后，需要手动给新节点分配哈希槽，从其他节点的哈希槽分来一部分，并且支持哈希槽均衡



* * *

# 分布式锁

* * *

本章节的 demo 代码示例，免搭建即开即用：**[learn-redis-demo](https://github.com/Doge2077/learn-redis-demo)**

* * *

## 基于 Redis 实现分布式锁

* * *

### 基础实现

* * *

基于 Redis 实现分布式锁主要依赖于 `SETNX` 命令：

  * `SETNX key value`：若不存在 key 则设置 key 值为 value，返回 1
  * 若 key 已存在，则不做任何操作，返回 0



为了防止某个线程获取锁之后异常结束没有释放锁，导致其他线程调用 `SETNX` 命令返回 0 而进入死锁，因此加锁后需要设置超时时间

以下是一个简单的 SpringBoot demo：
    
    
    @RestController
    @RequestMapping("/sell")
    public class AppController {
        @Resource
        StringRedisTemplate stringRedisTemplate;
    
        String LOCK = "TICKETSELLER";
        String KEY = "TICKET";
    
        @GetMapping("/ticket")
        public void sellTicket() {
            Boolean isLocked = stringRedisTemplate.opsForValue().setIfAbsent(LOCK, "1");
            if (Boolean.TRUE.equals(isLocked)) {
                // 设置过期时间 5s
                stringRedisTemplate.expire(LOCK, 5, TimeUnit.SECONDS);
                try {
                    // 拿到 ticket 的数量
                    int ticketCount = Integer.parseInt((String) stringRedisTemplate.opsForValue().get(KEY));
                    if (ticketCount > 0) {
                        // 扣减库存
                        stringRedisTemplate.opsForValue().set(KEY, String.valueOf(ticketCount - 1));
                        System.out.println("I get a ticket!");
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                } finally {
                    // 释放锁
                    stringRedisTemplate.delete(LOCK);
                }
            } else {
                System.out.println("Field");
            }
        }
    
    }

* * *

### 缺陷分析

* * *

#### 加锁和设置过期时间非原子操作

* * *

  * 我们先是用 `SETNX` 创建了锁，假如这个服务在创建锁之后由于事故导致直接停机，那么这个锁就是一个永不过期的锁
  * 这将导致其他服务无法获取到锁，影响业务的正常进行



解决方案：

  * 使用 LUA 脚本来进行加锁和设置过期时间的操作
  * 这样可以使得加锁和设置过期时间是一个原子操作


    
    
    @RestController
    @RequestMapping("/sell")
    public class AppController {
        @Resource
        StringRedisTemplate stringRedisTemplate;
    
        String LOCK = "TICKETSELLER";
        String KEY = "TICKET";
    
        @GetMapping("/ticket")
        public void sellTicket() {
            // LUA  脚本
            String LUA Script =
                    "if redis.call('setnx',KEYS[1],ARGV[1]) == 1 " +
                            "then redis.call('expire',KEYS[1],ARGV[2]) ;" +
                            "return true " +
                    "else return false " +
                    "end";
    
            // 回调函数返回加锁状态
            Boolean isLocked = stringRedisTemplate.execute(new RedisCallback&lt;Boolean&gt;() {
                @Override
                public Boolean doInRedis(RedisConnection connection) throws DataAccessException {
                   return connection.eval(LUA Script.getBytes(),
                            ReturnType.BOOLEAN,
                            1,
                            LOCK.getBytes(),
                            "1".getBytes(),
                            "5".getBytes());
                }
            });
            if (Boolean.TRUE.equals(isLocked)) {
                try {
                    int ticketCount = Integer.parseInt((String) stringRedisTemplate.opsForValue().get(KEY));
                    if (ticketCount > 0) {
                        stringRedisTemplate.opsForValue().set(KEY, String.valueOf(ticketCount - 1));
                        System.out.println("I get a ticket!");
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                } finally {
                    stringRedisTemplate.delete(LOCK);
                }
            } else {
                System.out.println("Field");
            }
        }
    
    }

* * *

#### 锁的过期时间设置是否合理

* * *

![](https://image.itbaima.cn/images/40/image-20240319003866632.png)

假设现有服务 A 和服务 B，A 先拿到锁执行业务，但是由于业务过长导致 A 的锁到期后超时释放：

  * 如果 B 的业务还没结束，A 的业务结束进行释放锁的操作，A 就会错误的删除掉 B 加的锁，那 B 的业务执行完就无锁可释了
  * 如果 B 服务可以获取到锁了，B 加锁并执行他的业务，由于此时 A 也在执行业务，两个服务共享内存就容易造成超卖问题



针对第一种问题的出现，解决方案很简单，只需要对锁的值做出限制即可：

  * 设置加锁 key 的值为唯一，如利用 uid + threadid
  * 在释放锁时判断是否是自己的锁，如果是则释放
  * 这个释放锁的操作也要保证原子性，因此也需要用 LUA 脚本来实现


    
    
    @RestController
    @RequestMapping("/sell")
    public class AppController {
        @Resource
        StringRedisTemplate stringRedisTemplate;
    
        String LOCK = "TICKETSELLER";
        String KEY = "TICKET";       // 记得在 redis 里面设置好 TICKET 的数量
    
        @GetMapping("/ticket")
        public void sellTicket() {
            String lockLuaScript =
                    "if redis.call('setnx',KEYS[1],ARGV[1]) == 1 " +
                            "then redis.call('expire',KEYS[1],ARGV[2]) ;" +
                            "return true " +
                            "else return false " +
                            "end";
    
            // 生产环境替换为 uuid + 线程 id
            String VALUE = String.valueOf(Thread.currentThread().getId());
            Boolean isLocked = stringRedisTemplate.execute(new RedisCallback&lt;Boolean&gt;() {
                @Override
                public Boolean doInRedis(RedisConnection connection) throws DataAccessException {
                    return connection.eval(lockLuaScript.getBytes(),
                            ReturnType.BOOLEAN,
                            1,
                            LOCK.getBytes(),
                            VALUE.getBytes(),  // 用于判断是否为当前线程加的锁
                            "5".getBytes()
                    );
                }
            });
            if (Boolean.TRUE.equals(isLocked)) {
                try {
                    int ticketCount = Integer.parseInt((String) stringRedisTemplate.opsForValue().get(KEY));
                    if (ticketCount > 0) {
                        stringRedisTemplate.opsForValue().set(KEY, String.valueOf(ticketCount - 1));
                        System.out.println("I get a ticket!");
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                } finally {
    //                // 判断是否是自己加的锁，如果是则释放 缺点：非原子操作
    //                String LOCK_ID = stringRedisTemplate.opsForValue().get(LOCK);
    //                if (LOCK_ID != null && LOCK_ID.equals(VALUE)) {
    //                    stringRedisTemplate.delete(LOCK);
    //                }
                    String unlockLuaScript =
                            "if redis.call('get',KEYS[1]) == ARGV[1] " +
                                    "then redis.call('del',KEYS[1]); " +
                                    "return true " +
                                    "else return false " +
                                    "end";
                    stringRedisTemplate.execute(new RedisCallback&lt;Object&gt;() {
                        @Override
                        public Object doInRedis(RedisConnection connection) throws DataAccessException {
                            return connection.eval(unlockLuaScript.getBytes(),
                                    ReturnType.BOOLEAN,
                                    1,
                                    LOCK.getBytes(),
                                    VALUE.getBytes()
                            );
                        }
                    });
                }
            } else {
                System.out.println("Field");
            }
        }
    
    }

针对第二种问题，我们可以利用看门狗机制实现：

  * 开一个守护线程，每隔一段时间就获取一次锁的状态
  * 如果仍然持有锁，则对其续期，此过程仍然利用 LUA 脚本实现
  * 当业务结束后终止该线程


    
    
    @RestController
    @RequestMapping("/sell")
    public class AppController {
        @Resource
        StringRedisTemplate stringRedisTemplate;
    
        String LOCK = "TICKETSELLER";
        String KEY = "TICKET";       // 记得在 redis 里面设置好 TICKET 的数量
    
        @GetMapping("/ticket")
        public void sellTicket() {
            String lockLuaScript =
                    "if redis.call('setnx',KEYS[1],ARGV[1]) == 1 " +
                            "then redis.call('expire',KEYS[1],ARGV[2]) ;" +
                            "return true " +
                            "else return false " +
                            "end";
            // 生产环境替换为 uuid + 线程 id
            String VALUE = String.valueOf(Thread.currentThread().getId());
            Boolean isLocked = stringRedisTemplate.execute(new RedisCallback&lt;Boolean&gt;() {
                @Override
                public Boolean doInRedis(RedisConnection connection) throws DataAccessException {
                    return connection.eval(lockLuaScript.getBytes(),
                            ReturnType.BOOLEAN,
                            1,
                            LOCK.getBytes(),
                            VALUE.getBytes(),  // 用于判断是否为当前线程加的锁
                            "5".getBytes()
                    );
                }
            });
            if (Boolean.TRUE.equals(isLocked)) {
                // 判断是否是自己加的锁，如果是则续期
                String addlockLuaScript =
                        "if redis.call('get',KEYS[1]) == ARGV[1] " +
                                "then redis.call('expire',KEYS[1], ARGV[2]) ; " +
                                "return true " +
                                "else return false " +
                                "end";
                Thread watchDoge = new Thread(() -> {
                    while (Boolean.TRUE.equals(stringRedisTemplate.execute(new RedisCallback&lt;Boolean&gt;() {
                        @Override
                        public Boolean doInRedis(RedisConnection connection) throws DataAccessException {
                            return connection.eval(addlockLuaScript.getBytes(),
                                    ReturnType.BOOLEAN,
                                    1,
                                    LOCK.getBytes(),
                                    VALUE.getBytes(),
                                    "5".getBytes());
                        }
                    })) && !Thread.currentThread().isInterrupted()) {
                        try {
                            System.out.println(Thread.currentThread().isInterrupted());
                            Thread.sleep(4000);
                        } catch (Exception e) {
                            break;
                        }
                    }
                });
                watchDoge.setDaemon(true);
                watchDoge.start();
                try {
                    int ticketCount = Integer.parseInt((String) stringRedisTemplate.opsForValue().get(KEY));
                    if (ticketCount > 0) {
                        stringRedisTemplate.opsForValue().set(KEY, String.valueOf(ticketCount - 1));
    //                    Thread.sleep(10000000);  // 在这里睡一下，可以到 redis 里面 TTL TICKETSELLER 查看锁是否被续期
                        watchDoge.interrupt();
                        System.out.println("I get a ticket!");
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                } finally {
                    String unlockLuaScript =
                            "if redis.call('get',KEYS[1]) == ARGV[1] " +
                                    "then redis.call('del',KEYS[1]); " +
                                    "return true " +
                                    "else return false " +
                                    "end";
                    stringRedisTemplate.execute(new RedisCallback&lt;Object&gt;() {
                        @Override
                        public Object doInRedis(RedisConnection connection) throws DataAccessException {
                            return connection.eval(unlockLuaScript.getBytes(),
                                    ReturnType.BOOLEAN,
                                    1,
                                    LOCK.getBytes(),
                                    VALUE.getBytes()
                            );
                        }
                    });
                }
            } else {
                System.out.println("Field");
            }
        }
    
    }

* * *

#### 其他缺陷

* * *

对于上面的看门狗机制，其实是一个极其朴素的实现，实际上需要考虑到的东西还有很多。

另外上述的实现仍缺少一些高级应用场景的功能：

  * 如何实现锁的可重入：增加重入次数的参数，实现锁的成对加锁和释放。
  * 如何实现阻塞的锁：客户端轮询（性能开销大）或者发布订阅



而这些功能想要自己去实现是非常麻烦的，因此一般利用 Redisson 实现分布式锁。

* * *

## 基于 Redisson 实现分布式锁

* * *

### 基础操作

* * *

Redisson 内置了一系列的分布式对象，分式集合，分布式锁，分布式服务等诸多功能特性，是一款基于 Redis 实现，拥有一系列分布式 系统功能特性的工具包，是实现分布式系统架构中缓存中间件的最佳选择。

引入依赖：
    
    
```xml
```xml
    &lt;dependency&gt;
        &lt;groupId&gt;org.redisson&lt;/groupId&gt;
        &lt;artifactId&gt;redisson</artifactId>
        &lt;version&gt;3.27.2&lt;/version&gt;
    </dependency>
```
```

编写 Redisson 配置类：
    
    
    @Configuration
    public class RedissonConfig {
        // 构建 Redisson 客户端配置
        @Bean
        public RedissonClient redissonClient() {
            Config config = new Config();
            config.useSingleServer().setAddress("redis://127.0.0.1:6379");
            return Redisson.create(config);
        }
    }

注入到 Controller：
    
    
    @RestController
    @RequestMapping("/redisson")
    public class RedissonAppController {
    
        String LOCK = "REIDSSON:TICKETSELLER";
        String KEY = "TICKET";
    
        // 注入
        @Resource
        RedissonClient redissonClient;
    
        @Resource
        StringRedisTemplate stringRedisTemplate;
    
        @GetMapping("/sell/ticket")
        public void redissonSellTicket() {
            // 加锁
            RLock rLock = redissonClient.getLock(LOCK);
            rLock.lock();
            try {
                int count = Integer.parseInt((String) stringRedisTemplate.opsForValue().get(KEY));
                if (count > 0) {
                    stringRedisTemplate.opsForValue().set(KEY, String.valueOf(count - 1));
                    System.out.println("Reidsson get ticket");
                } else {
                    System.out.println("Field");
                }
            } catch (Exception e) {
                e.printStackTrace();
            } finally {
                // 释放锁
                rLock.unlock();
            }
        }
    
    }

* * *

### 源码剖析

* * *

#### 加锁原理

* * *

首先来看 `package org.redisson` 包下的 `lock` 方法的具体实现：
    
    
    private void lock(long leaseTime, TimeUnit unit, boolean interruptibly) throws InterruptedException {
        long threadId = Thread.currentThread().getId();
        /*
         * 这里调用 tryAcquire 尝试获取锁
         *    如果为 null 说明获取到了锁
         *    如果不是 null 说明其他线程持有锁
         * 这个方法最底层的实现其实也是 LUA 脚本
         */
        Long ttl = this.tryAcquire(-1L, leaseTime, unit, threadId);
        if (ttl != null) {
            // 发布订阅，非阻塞锁
            CompletableFuture&lt;RedissonLockEntry&gt; future = this.subscribe(threadId);
            this.pubSub.timeout(future);
            RedissonLockEntry entry;
            if (interruptibly) {
                entry = (RedissonLockEntry)this.commandExecutor.getInterrupted(future);
            } else {
                entry = (RedissonLockEntry)this.commandExecutor.get(future);
            }
    
            try {
                while(true) {
                    // 仍然尝试获取锁
                    ttl = this.tryAcquire(-1L, leaseTime, unit, threadId);
                    if (ttl == null) {
                        return;
                    }
    
                    if (ttl >= 0L) {
                        try {
                            entry.getLatch().tryAcquire(ttl, TimeUnit.MILLISECONDS);
                        } catch (InterruptedException var14) {
                            if (interruptibly) {
                                throw var14;
                            }
    
                            entry.getLatch().tryAcquire(ttl, TimeUnit.MILLISECONDS);
                        }
                    } else if (interruptibly) {
                        entry.getLatch().acquire();
                    } else {
                        entry.getLatch().acquireUninterruptibly();
                    }
                }
            } finally {
                // 取消订阅频道
                this.unsubscribe(entry, threadId);
            }
        }
    }

接下来我们看 `tryAcquire` 尝试获取锁的方法 `tryAcquireOnceAsync`：
    
    
    private RFuture&lt;Boolean&gt; tryAcquireOnceAsync(long waitTime, long leaseTime, TimeUnit unit, long threadId) {
            RFuture acquiredFuture;
            if (leaseTime > 0L) {
                acquiredFuture = this.tryLockInnerAsync(waitTime, leaseTime, unit, threadId, RedisCommands.EVAL_NULL_BOOLEAN);
            } else {
                // 未设定过期时间走这个默认的
                acquiredFuture = this.tryLockInnerAsync(waitTime, this.internalLockLeaseTime, TimeUnit.MILLISECONDS, threadId, RedisCommands.EVAL_NULL_BOOLEAN);
            }
    
            CompletionStage&lt;Boolean&gt; acquiredFuture = this.handleNoSync(threadId, acquiredFuture);
            CompletionStage&lt;Boolean&gt; f = acquiredFuture.thenApply((acquired) -&gt; {
                if (acquired) {
                    if (leaseTime > 0L) {
                        this.internalLockLeaseTime = unit.toMillis(leaseTime);
                    } else {
                        this.scheduleExpirationRenewal(threadId);
                    }
                }
    
                return acquired;
            });
            return new CompletableFutureWrapper(f);
        }

可以看到 `tryLockInnerAsync` 传参中多了一个参数 `this.internalLockLeaseTime`，这个东西的初始化在：
    
    
    public RedissonLock(CommandAsyncExecutor commandExecutor, String name) {
            super(commandExecutor, name);
            this.commandExecutor = commandExecutor;
            // 看门狗机制的续期时间
            this.internalLockLeaseTime = this.getServiceManager().getCfg().getLockWatchdogTimeout();
            this.pubSub = commandExecutor.getConnectionManager().getSubscribeService().getLockPubSub();
    }

这个续期时间的默认值可以在 Config 里面找到：
    
    
        public Config() {
            this.transportMode = TransportMode.NIO;
            // 默认是 30s
            this.lockWatchdogTimeout = 30000L;
            this.checkLockSyncedSlaves = true;
            this.slavesSyncTimeout = 1000L;
            this.reliableTopicWatchdogTimeout = TimeUnit.MINUTES.toMillis(10L);
            this.keepPubSubOrder = true;
            this.useScriptCache = false;
            this.minCleanUpDelay = 5;
            this.maxCleanUpDelay = 1800;
            this.cleanUpKeysAmount = 100;
            this.nettyHook = new DefaultNettyHook();
            this.useThreadClassLoader = true;
            this.addressResolverGroupFactory = new SequentialDnsAddressResolverFactory();
            this.protocol = Protocol.RESP2;
        }

最后我们回到最底层的 `tryLockInnerAsync` 方法：
    
    
    &lt;T&gt; RFuture&lt;T&gt; tryLockInnerAsync(long waitTime, long leaseTime, TimeUnit unit, long threadId, RedisStrictCommand&lt;T&gt; command) {
            return this.evalWriteSyncedAsync(this.getRawName(), LongCodec.INSTANCE, command, "if ((redis.call('exists', KEYS[1]) == 0) or (redis.call('hexists', KEYS[1], ARGV[2]) == 1)) then redis.call('hincrby', KEYS[1], ARGV[2], 1); redis.call('pexpire', KEYS[1], ARGV[1]); return nil; end; return redis.call('pttl', KEYS[1]);", Collections.singletonList(this.getRawName()), new Object[]{unit.toMillis(leaseTime), this.getLockName(threadId)});
    }

这里实际执行的是一个 LUA 脚本：
    
    
    -- 判断是否存在 KEY，不存在则加锁
    if (redis.call('exists', KEYS[1]) == 0) or (redis.call('hexists', KEYS[1], ARGV[2]) == 1) then
        redis.call('hincrby', KEYS[1], ARGV[2], 1);  -- 对 hash 的字段加一
        redis.call('pexpire', KEYS[1], ARGV[1]);     -- 设置过期时间
        return nil;
    else
        return redis.call('pttl', KEYS[1]); -- 存在锁说明其他线程占有，返回过期时间
    end;

这里新版的 Redisson 加锁的逻辑简化了，以前是区分了加锁和可重入，现在进行了合并。

* * *

#### 看门狗机制原理

* * *

继续看 `tryAcquireAsync` 方法，在获取到锁后，走 `scheduleExpirationRenewal` 的逻辑：
    
    
    private RFuture&lt;Long&gt; tryAcquireAsync(long waitTime, long leaseTime, TimeUnit unit, long threadId) {
        RFuture ttlRemainingFuture;
        if (leaseTime > 0L) {
            ttlRemainingFuture = this.tryLockInnerAsync(waitTime, leaseTime, unit, threadId, RedisCommands.EVAL_LONG);
        } else {
            ttlRemainingFuture = this.tryLockInnerAsync(waitTime, this.internalLockLeaseTime, TimeUnit.MILLISECONDS, threadId, RedisCommands.EVAL_LONG);
        }
    
        CompletionStage&lt;Long&gt; s = this.handleNoSync(threadId, ttlRemainingFuture);
        RFuture&lt;Long&gt; ttlRemainingFuture = new CompletableFutureWrapper(s);
        CompletionStage&lt;Long&gt; f = ttlRemainingFuture.thenApply((ttlRemaining) -&gt; {
            if (ttlRemaining == null) {
                if (leaseTime > 0L) {
                    this.internalLockLeaseTime = unit.toMillis(leaseTime);
                } else {
                    this.scheduleExpirationRenewal(threadId);  // 锁续期
                }
            }
    
            return ttlRemaining;
        });
        return new CompletableFutureWrapper(f);
    }

点进去看 `scheduleExpirationRenewal` 方法：
    
    
    protected void scheduleExpirationRenewal(long threadId) {
            ExpirationEntry entry = new ExpirationEntry();
            ExpirationEntry oldEntry = (ExpirationEntry)EXPIRATION_RENEWAL_MAP.putIfAbsent(this.getEntryName(), entry);
            if (oldEntry != null) {
                oldEntry.addThreadId(threadId);
            } else {
                entry.addThreadId(threadId);
    
                try {
                    this.renewExpiration();  // 创建定时任务
                } finally {
                    if (Thread.currentThread().isInterrupted()) {
                        this.cancelExpirationRenewal(threadId, (Boolean)null);
                    }
    
                }
            }
    
        }

创建定时任务的逻辑：
    
    
    private void renewExpiration() {
            ExpirationEntry ee = (ExpirationEntry)EXPIRATION_RENEWAL_MAP.get(this.getEntryName());
            if (ee != null) {
                Timeout task = this.getServiceManager().newTimeout(new TimerTask() {
                    public void run(Timeout timeout) throws Exception {
                        ExpirationEntry ent = (ExpirationEntry)RedissonBaseLock.EXPIRATION_RENEWAL_MAP.get(RedissonBaseLock.this.getEntryName());
                        if (ent != null) {
                            Long threadId = ent.getFirstThreadId();
                            if (threadId != null) {
                                CompletionStage&lt;Boolean&gt; future = RedissonBaseLock.this.renewExpirationAsync(threadId);
                                future.whenComplete((res, e) -> {
                                    if (e != null) {
                                        RedissonBaseLock.log.error("Can't update lock {} expiration", RedissonBaseLock.this.getRawName(), e);
                                        RedissonBaseLock.EXPIRATION_RENEWAL_MAP.remove(RedissonBaseLock.this.getEntryName());
                                    } else {
                                        if (res) {
                                            RedissonBaseLock.this.renewExpiration();
                                        } else {
                                            RedissonBaseLock.this.cancelExpirationRenewal((Long)null, (Boolean)null);
                                        }
    
                                    }
                                });
                            }
                        }
                    }
                }, this.internalLockLeaseTime / 3L, TimeUnit.MILLISECONDS);  // 这个值在之前讲过，续期用的，默认为 30s，因此这个任务默认每隔 10s 执行一次
                ee.setTimeout(task);
            }
        }

每次定时任务触发，会执行 `renewExpirationAsync` 方法：
    
    
    protected CompletionStage&lt;Boolean&gt; renewExpirationAsync(long threadId) {
            return this.evalWriteSyncedAsync(this.getRawName(), LongCodec.INSTANCE, RedisCommands.EVAL_BOOLEAN, "if (redis.call('hexists', KEYS[1], ARGV[2]) == 1) then redis.call('pexpire', KEYS[1], ARGV[1]); return 1; end; return 0;", Collections.singletonList(this.getRawName()), this.internalLockLeaseTime, this.getLockName(threadId));
    }

可以看到，本质仍然是一个 LUA 脚本：
    
    
    -- 检查 KEY 是否存在
    if (redis.call('hexists', KEYS[1], ARGV[2]) == 1) then 
        redis.call('pexpire', KEYS[1], ARGV[1]);  -- 存在则更新过期时间为 this.internalLockLeaseTime，就是默认那 30s
        return 1; -- 成功返回
    end; 
    return 0;

* * *

#### 解锁原理

* * *

首先来看 `package org.redisson` 包下的 `unlock` 方法的具体实现：
    
    
    public void unlock() {
            try {
                this.get(this.unlockAsync(Thread.currentThread().getId()));
            } catch (RedisException var2) {
                if (var2.getCause() instanceof IllegalMonitorStateException) {
                    throw (IllegalMonitorStateException)var2.getCause();
                } else {
                    throw var2;
                }
            }
        }

调用了方法 `unlockAsync`：
    
    
    public RFuture&lt;Void&gt; unlockAsync(long threadId) {
            return this.getServiceManager().execute(() -> {
                return this.unlockAsync0(threadId);
            });
        }
    
    // 又调用了这段
    private RFuture&lt;Void&gt; unlockAsync0(long threadId) {
            CompletionStage&lt;Boolean&gt; future = this.unlockInnerAsync(threadId);
            CompletionStage&lt;Void&gt; f = future.handle((res, e) -&gt; {
                this.cancelExpirationRenewal(threadId, res);
                if (e != null) {
                    if (e instanceof CompletionException) {
                        throw (CompletionException)e;
                    } else {
                        throw new CompletionException(e);
                    }
                } else if (res == null) {
                    IllegalMonitorStateException cause = new IllegalMonitorStateException("attempt to unlock lock, not locked by current thread by node id: " + this.id + " thread-id: " + threadId);
                    throw new CompletionException(cause);
                } else {
                    return null;
                }
            });
            return new CompletableFutureWrapper(f);
        }

接下来走 `unlockInnerAsync` 的逻辑：
    
    
    protected final RFuture&lt;Boolean&gt; unlockInnerAsync(long threadId) {
        // 生成一个会话ID用于锁的释放
        String id = this.getServiceManager().generateId();
    
        // 获取Redisson的配置对象
        MasterSlaveServersConfig config = this.getServiceManager().getConfig();
    
        // 计算超时的时间，这是基于配置中的超时时间、重试间隔和重试次数计算出的总时间
        int timeout = (config.getTimeout() + config.getRetryInterval()) * config.getRetryAttempts();
        timeout = Math.max(timeout, 1);
    
        // 执行异步任务以释放锁
        RFuture&lt;Boolean&gt; r = this.unlockInnerAsync(threadId, id, timeout);
    
        // 使用CompletionStage处理异步操作的结果
        CompletionStage&lt;Boolean&gt; ff = r.thenApply((v) -&gt; {
            CommandAsyncExecutor ce = this.commandExecutor;
    
            // 判断commandExecutor是否是CommandBatchService的一个实例
            if (ce instanceof CommandBatchService) {
                // 如果是，创建一个新的CommandBatchService实例
                ce = new CommandBatchService(this.commandExecutor);
            }
    
            // 执行DEL命令以删除锁相关的数据
            ((CommandAsyncExecutor)ce).writeAsync(this.getRawName(), 
                                                  LongCodec.INSTANCE, 
                                                  RedisCommands.DEL, 
                                                  new Object[]{this.getUnlockLatchName(id)});
    
            // 如果为CommandBatchService实例，则执行异步批量提交操作
            if (ce instanceof CommandBatchService) {
                ((CommandBatchService)ce).executeAsync();
            }
    
            // 返回之前的异步任务的结果
            return v;
        });
    
        // 将CompletionStage的执行结果包装为RFuture返回
        return new CompletableFutureWrapper(ff);
    }

重点在于执行异步任务释放锁的过程：
    
    
    protected RFuture&lt;Boolean&gt; unlockInnerAsync(long threadId, String requestId, int timeout) {
            return this.evalWriteSyncedAsync(this.getRawName(), LongCodec.INSTANCE, RedisCommands.EVAL_BOOLEAN, "local val = redis.call('get', KEYS[3]); if val ~= false then return tonumber(val);end; if (redis.call('hexists', KEYS[1], ARGV[3]) == 0) then return nil;end; local counter = redis.call('hincrby', KEYS[1], ARGV[3], -1); if (counter > 0) then redis.call('pexpire', KEYS[1], ARGV[2]); redis.call('set', KEYS[3], 0, 'px', ARGV[5]); return 0; else redis.call('del', KEYS[1]); redis.call(ARGV[4], KEYS[2], ARGV[1]); redis.call('set', KEYS[3], 1, 'px', ARGV[5]); return 1; end; ", Arrays.asList(this.getRawName(), this.getChannelName(), this.getUnlockLatchName(requestId)), new Object[]{LockPubSub.UNLOCK_MESSAGE, this.internalLockLeaseTime, this.getLockName(threadId), this.getSubscribeService().getPublishCommand(), timeout});
    }

可以看到，本质还是一个 LUA 脚本：
    
    
    -- 尝试从KEYS[3]获取值
    local val = redis.call('get', KEYS[3])
    -- 如果val不为false，则返回它的数字表示
    if val ~= false then
        return tonumber(val)
    end
    -- 检查hash KEYS[1]中是否存在字段ARGV[3]
    if (redis.call('hexists', KEYS[1], ARGV[3]) == 0) then
        -- 如果不存在，则返回nil
        return nil
    end
    -- 在hash KEYS[1]里将字段ARGV[3]的值减1，并将结果保存在counter中
    local counter = redis.call('hincrby', KEYS[1], ARGV[3], -1)
    -- 如果计数器仍然大于0
    if (counter > 0) then
        -- 设置hash KEYS[1]的过期时间为ARGV[2]毫秒
        redis.call('pexpire', KEYS[1], ARGV[2])
        -- 设置KEYS[3]的值为0，并设置过期时间为ARGV[5]毫秒
        redis.call('set', KEYS[3], 0, 'px', ARGV[5])
        return 0
    else
        -- 如果计数器不大于0，则删除hash KEYS[1]
        redis.call('del', KEYS[1])
        -- 执行ARGV[4]（可能是发布某些消息）到KEYS[2]
        redis.call(ARGV[4], KEYS[2], ARGV[1])
        -- 设置KEYS[3]的值为1，并设置过期时间为ARGV[5]毫秒
        redis.call('set', KEYS[3], 1, 'px', ARGV[5])
        return 1
    end

* * *

# 三大使用陷阱

* * *

## 缓存穿透

* * *

### 原因分析

* * *

  * 查询到的 key 不存在导致查询结果没有写入缓存
  * 后续大量这样的请求直接打到数据库压力很大



这里主要是很多这种的请求打过来，查到的 key 不存在的次数较多，导致数据库压力倍增

* * *

### 解决方案

* * *

较为简单的解决方案是将这种查询不到的 key 设置为空值缓存并返回，缺点是占内存，实际上可以采用更加优雅的解决方案——添加布隆过滤器：

  * 一个 bitmap，多个 hash 函数
  * 对于已经缓存的 key，经过多次 hash 在 bitmap 中做映射
  * 如果请求的 key 多次映射后全部命中，则说明在 Redis 中**可能** 存在，放行请求
  * 否则拒绝请求



![image-20240320175505310](https://image.itbaima.cn/images/40/image-20240320174074053.png)

这里全部命中后的“可能”存在是因为存在哈希冲突的可能性：

  * 假设已经存在缓存中的 x, y, z 这三个 key 做 hash 后命中的 bitmap 如上图所示
  * 现在有 w 这个 key 请求打过来，多次 hash 后发现全部命中，这就造成了误判



技术上实现：

  * 本地缓存：Caffine 或者 Guava
  * 基于 Redisson 实现



* * *

## 缓存击穿

* * *

### 原因分析

* * *

  * 对于设置了过期时间的 key，缓存在某个时间点过期的时出现大量高并发请求
  * 请求发现缓存过期会从后端 DB 加载数据并写回到缓存，这个时候大并发的请求可能会瞬间把 DB 压垮



这里主要是针对某个 key 的，某个 key 恰好过期恰好大量请求打到这个 key 上

* * *

### 解决方案

* * *

![image-20240320181549116](https://image.itbaima.cn/images/40/image-20240320182318621.png)

  * 使用互斥锁： 
    * 缓存失效时不立即查询 DB
    * 先用 redis 的 setnx 设置互斥锁
    * 成功返回再查询 DB 并写回缓存，否则重试 get 缓存方法
    * 能保证强一致性，但线程需要等待有死锁风险
  * 设置 key 逻辑过期： 
    * 设置 key 时添加一个字段表示过期时间，然后设置永不过期
    * 查询到该 key 比对过期时间判断是否过期
    * 如果过期新开线程进行数据同步，当前线程正常返回数据，但数据不是最新的
    * 不能保证一致性，但线程无需等待



* * *

## 缓存雪崩

* * *

### 原因分析

* * *

  * 大量设置缓存时间相同的 key 在同一时间大量失效
  * 导致很多失效的 key 全部查询 DB



这里算是缓存击穿的升级版，大量的同一过期时间的 key 失效，结果大量请求过来，虽然查询的不是同一个 key，但未命中的流量占大部分

* * *

### 解决方案

* * *

  * 将缓存失效时间分散，在原有时间上设置随机数错开失效时间
  * 采用加锁计数，或者使用合理的队列数量来避免缓存失效时对数据库造成太大的压力，但是会降低系统的吞吐量
  * 分析用户行为，尽量让失效时间点均匀分布，尽量避免缓存雪崩的出现



* * *
