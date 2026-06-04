---
title: "Netty 应用与原理"
date: 2024-04-27
categories: [Software Architect, Netty]
description: ""
---

# Java IO 模型

本篇示例代码仓库：[learn-netty](https://github.com/Doge2077/learn-netty)

## 基础概念

在 I/O 操作中有这么两组概念，其中同步/异步要与线程中的同步线程/异步线程区分开，这里指的是同步 IO / 异步 IO。

**阻塞/非阻塞**：

* 没有数据传过来时，读操作会阻塞直到有数据；缓冲区满时，写操作也会阻塞。
* 非阻塞遇到这些情况，都是直接返回。

**同步/异步**：

* 数据就绪后需要程序自己去读，这是同步。
* 数据就绪后由系统直接读好再回调给程序，这是异步。

**常见的 IO 模型**：

* 同步阻塞 IO
* 同步非阻塞 IO
* IO 多路复用
* 信号驱动 IO
* 异步 IO

## Java BIO

BIO 是 Blocking I/O 的简称，它是同步阻塞型 IO，其相关的类和接口在 `java.io` 包下，简单来讲：

* BIO 模型下的服务端为每一个请求都分配一个线程进行处理。
* I/O 操作都是基于流（Stream）的操作。

![Java BIO 模型示意图](https://image.itbaima.cn/images/40/image-20240324096780993.png)

编写一个简单的 BioServer：
```java
public class BioServer {
    public static void main(String[] args) throws IOException {
        // BIO 模型的服务端要为每一个客户端建立一个对应的连接
        ServerSocket serverSocket = new ServerSocket(1145);
        while (true) {
            // 持续接受客户端的连接
            Socket accept = serverSocket.accept();
            // 为每一个客户端连接新开一个线程，执行对应的业务
            new Thread(new ClientService(accept)).start();
        }
    }

    static class ClientService implements Runnable {
        private Socket socket;

        public ClientService(Socket socket) {
            this.socket = socket;
        }

        @Override
        public void run() {
            System.out.println("执行对应的业务操作：" + socket);
        }
    }
}
```

对应编写一个简单的客户端：
```java
public class Client {
    public static void main(String[] args) throws IOException {
        Socket socket = new Socket("127.0.0.1", 1145);
        System.out.println("建立连接：" + socket);
    }
}
```

这种 IO 模型的弊端十分明显：

* 线程开销：客户端的并发数与后端的线程数成1：1的比例，线程的创建、销毁是非常消耗系统资源的，随着并发量增大，服务端性能将显著下降，甚至会发生线程堆栈溢出等错误。
  * 线程阻塞：当连接创建后，如果该线程没有操作时，会进行阻塞操作，这样极大的浪费了服务器资源。

---

## Java NIO

NIO，称之为 New IO 或是 non-blocking IO（非阻塞IO），这两种说法都可以，其实称之为非阻塞 IO 更恰当一些。

NIO的三大核心组件：

* Buffer（缓冲区）
  * Channel（通道）
  * Selector（选择器/多路复用器）

---

### Buffer

在应用层面，数据从网络传递给 Buffer，我们操作 Buffer 中的数据，之后再通过 NIO 的 api 将处理后的 Buffer 中的数据写回到网络中：

* Buffer是一个对象，包含一些要写入或者读出的数据。
  * 原有的 IO 数据读写都是在 Stream 中，而 NIO 则是用 Buffer 预处理。
  * 读数据从缓冲区读，写数据也写入到缓冲区。
  * 缓冲区的本质是一个数组，底层支持多种实现（通常是字节数组实现），还提供了对数据结构化访问以及维护读写位置等操作。

查看一下 java.nio 包下的 Buffer.java 源码中的几个私有属性：
```java
// Invariants: mark &lt;= position &lt;= limit &lt;= capacity
    private int mark = -1;
    private int position = 0;
    private int limit;
    private int capacity;
```

mark &lt;= position &lt;= limit &lt;= capacity 这个大小关系是在写模式下的：

* mark 就是一个标志位，capacity 是总容量。
  * position 是写入起始位置，limit 限制了可操作的最大位置。

当 Buffer 需要读数据时会进行读写模式切换：
```java
public Buffer flip() {
        limit = position;
        position = 0;
        mark = -1;
        return this;
    }
```

* 这里将 limit 值更新为 position 的位置，即可读的区间不会超过已写入的区间。
  * 然后将 position 置 0，即读区间的起始位置。

---

### Channel

Channel是一个通道，管道，网络数据通过 Channel 读取和写入。

Channel 和流 Stream 的不同之处：

![image-20240324104117449](https://image.itbaima.cn/images/40/image-20240324109182233.png)

* Channel 是双向的。
  * 流只在一个方向上移动（InputStream/OutputStream）。
  * 而 Channel 可以用于读写同时进行，即 Channel 是全双工模式。

Java 提供两个网络读写相关的 Channel：

* ServerSocketChannel：用于服务端和客户端建立连接，服务端必备，客户端不需要。
  * SocketChannel：用于客户端和服务端双向通信，服务端建立连接后需要创建该对象和客户端进行通信。

![image-20240324104800899](https://image.itbaima.cn/images/40/image-20240324102738323.png)

这里 SocketChannel 在不同端上所支持的事件是不一样的：

端类型 | Channel 类型 | OP_ACCEPT | OP_CONNECT | OP_WRITE | OP_READ
---|---|---|---|---|---
Client 端 | SocketChannel |  | 支持 | 支持 | 支持
Server 端 | ServerSocketChannel | 支持 |  |  |
Server 端 | SocketChannel |  |  | 支持 | 支持

---

### Selector

Selector（选择器/多路复用器）：

* Selector 会不断轮询注册在其上的 Channel。
  * 如果某个 Channel 上面发生读或者写事件，即该 Channel 处于就绪状态，它就会被 Selector 轮询出来。
  * 通过 selectedKeys 即可获取被轮询出的就绪 Channel 的集合，进行后续的 I/O 操作。

![image-20240324110212214](https://image.itbaima.cn/images/40/image-20240324115893756.png)

基于 NIO 来实现一个服务端：
```java
public class NioServer {
    public static void main(String[] args) {
        try {
            //1、打开ServerSocketChannel,用于监听客户端的连接，它是所有客户端连接的父管道(代表客户端连接的管道都是通过它创建的)
            ServerSocketChannel serverSocketChannel = ServerSocketChannel.open();
            //2、绑定监听端口，设置连接为非阻塞模式
            serverSocketChannel.socket().bind(new InetSocketAddress(1145));
            serverSocketChannel.configureBlocking(false);
            //3、创建多路复用器Selector
            Selector selector = Selector.open();
            //4、将ServerSocketChannel注册到selector上，监听客户端连接事件ACCEPT
            serverSocketChannel.register(selector, SelectionKey.OP_ACCEPT);
            //5、创建 Reactor线程，让多路复用器在 Reactor 线程中执行多路复用程序
            new Thread(new SingleReactor(selector)).start();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}

class SingleReactor implements Runnable {
    private final Selector selector;

    public SingleReactor(Selector selector) {
        this.selector = selector;
    }

    @Override
    public void run() {
        // 6、selector轮询准备就绪的事件
        while (true) {
            try {
                selector.select(1000);
                Set&lt;SelectionKey&gt; selectionKeys = selector.selectedKeys();
                Iterator&lt;SelectionKey&gt; iterator = selectionKeys.iterator();
                while (iterator.hasNext()) {
                    SelectionKey selectionKey = iterator.next();
                    iterator.remove();
                    try {
                        processKey(selectionKey);
                    } catch (IOException e) {
                        e.printStackTrace();
                        if (selectionKey != null) {
                            selectionKey.cancel();
                            SelectableChannel channel = selectionKey.channel();
                            if (channel != null) {
                                channel.close();
                            }
                        }
                    }
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    private void processKey(SelectionKey key) throws IOException {
        if (key.isValid()) {
            //7、根据准备就绪的事件类型分别处理
            if (key.isAcceptable()) {//客户端请求连接事件就绪
                //7.1、接收一个新的客户端连接，创建对应的SocketChannel,
                ServerSocketChannel serverSocketChannel = (ServerSocketChannel) key.channel();
                SocketChannel socketChannel = serverSocketChannel.accept();
                //7.2、设置socketChannel的非阻塞模式，并将其注册到Selector上，监听读事件
                socketChannel.configureBlocking(false);
                socketChannel.register(this.selector, SelectionKey.OP_READ);
            }
            if (key.isReadable()) {//读事件准备就绪
                //7.1、读客户端发送过来的数据
                SocketChannel socketChannel = (SocketChannel) key.channel();
                ByteBuffer readBuffer = ByteBuffer.allocate(1024);
                int readBytes = socketChannel.read(readBuffer);
                //前面设置过socketChannel是非阻塞的，故要通过返回值判断读取到的字节数
                if (readBytes > 0) {
                    readBuffer.flip();//读写模式切换
                    byte[] bytes = new byte[readBuffer.remaining()];
                    readBuffer.get(bytes);
                    String msg = new String(bytes, "utf-8");
                    //进行业务处理
                    String response = doService(msg);
                    //开始给客户端响应数据
                    System.out.println("服务端开始向客户端响应数据");
                    byte[] responseBytes = response.getBytes();
                    ByteBuffer writeBuffer = ByteBuffer.allocate(responseBytes.length);
                    writeBuffer.put(responseBytes);
                    writeBuffer.flip();
                    socketChannel.write(writeBuffer);
                } else if (readBytes &lt; 0) {
                    //值为-1表示链路通道已经关闭
                    key.cancel();
                    socketChannel.close();
                } else {
                    //没读取到数据，忽略
                }
            }
        }
    }

    private String doService(String msg) {
        System.out.println("成功接收客户端数据:" + msg);
        return "hello client, i am server!";
    }
}
```

对应的客户端实现：
```java
public class NioClient {
    public static void main(String[] args) {
        try {
            // 1、打开客户端SocketChannel，绑定客户端本地地址（不选默认随机分配一个可用地址）
            SocketChannel socketChannel = SocketChannel.open();
            // 2、设置非阻塞模式
            socketChannel.configureBlocking(false);
            // 3、创建Selector
            Selector selector = Selector.open();
            // 4、创建Reactor线程
            new Thread(new SingleReactorClient(socketChannel, selector)).start();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}

class SingleReactorClient implements Runnable {
    private final SocketChannel socketChannel;
    private final Selector selector;

    public SingleReactorClient(SocketChannel socketChannel, Selector selector) {
        this.socketChannel = socketChannel;
        this.selector = selector;
    }

    public void run() {
        try {
            // 连接服务端
            doConnect(socketChannel, selector);
            //5、多路复用器执行多路复用程序
            while (true) {
                try {
                    selector.select(1000);
                    Set&lt;SelectionKey&gt; selectionKeys = selector.selectedKeys();
                    Iterator&lt;SelectionKey&gt; iterator = selectionKeys.iterator();
                    while (iterator.hasNext()) {
                        SelectionKey selectionKey = iterator.next();
                        processKey(selectionKey);
                        iterator.remove();
                    }
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
            System.exit(1);
        }
    }

    private void doConnect(SocketChannel sc, Selector selector) throws IOException {
        System.out.println("客户端成功启动,开始连接服务端");
        //3、连接服务端
        boolean connect = sc.connect(new InetSocketAddress("127.0.0.1", 1145));
        //4、将socketChannel注册到selector并判断是否连接成功，连接成功监听读事件，没有继续监听连接事件
        System.out.println("connect=" + connect);
        if (connect) {
            sc.register(selector, SelectionKey.OP_READ);
            System.out.println("客户端成功连上服务端,准备发送数据");
            //开始进行业务处理，向服务端发送数据
            doService(sc);
        } else {
            sc.register(selector, SelectionKey.OP_CONNECT);
        }
    }

    private void processKey(SelectionKey key) throws IOException {
        if (key.isValid()) {
            // 6、根据准备就绪的事件类型分别处理
            if (key.isConnectable()) { // 服务端可连接事件准备就绪
                SocketChannel sc = (SocketChannel) key.channel();
                if (sc.finishConnect()) {
                    // 6.1、向selector注册可读事件(接收来自服务端的数据)
                    sc.register(selector, SelectionKey.OP_READ);
                    // 6.2、处理业务 向服务端发送数据
                    doService(sc);
                } else {
                    // 连接失败，退出
                    System.exit(1);
                }
            }
            if (key.isReadable()) {//读事件准备继续
                //6.1、读服务端返回的数据
                SocketChannel sc = (SocketChannel) key.channel();
                ByteBuffer readBuffer = ByteBuffer.allocate(1024);
                int readBytes = sc.read(readBuffer);
                //前面设置过socketChannel是非阻塞的，故要通过返回值判断读取到的字节数
                if (readBytes > 0) {
                    readBuffer.flip();//读写模式切换
                    byte[] bytes = new byte[readBuffer.remaining()];
                    readBuffer.get(bytes);
                    String msg = new String(bytes, "utf-8");
                    //接收到服务端返回的数据后进行相关操作
                    doService(msg);
                } else if (readBytes &lt; 0) {
                    //值为-1表示链路通道已经关闭
                    key.cancel();
                    sc.close();
                } else {
                    //没读取到数据，忽略
                }
            }
        }
    }

    private static void doService(SocketChannel socketChannel) throws IOException {
        System.out.println("客户端开始向服务端发送数据:");
        //向服务端发送数据
        byte[] bytes = "hello nioServer,i am nioClient !".getBytes();
        ByteBuffer writeBuffer = ByteBuffer.allocate(bytes.length);
        writeBuffer.put(bytes);
        writeBuffer.flip();
        socketChannel.write(writeBuffer);
    }

    private String doService(String msg) {
        System.out.println("成功接收来自服务端响应的数据:" + msg);
        return "";
    }
}
```

在NIO中，Selector多路复用器在没有事件发生时仍会阻塞，可以考虑以下优化方式：
- **使用带超时的`select(long timeout)`方法**：设置超时时间，避免无限期阻塞；
- **使用`wakeup()`方法**：在其他线程中唤醒阻塞的Selector，以便及时响应；
- **采用Epoll替代方案（如Netty的EpollEventLoop）**：利用Linux的Epoll机制，进一步提升性能；
- **合理设置Selector的轮询策略**：结合业务场景调整阻塞与非阻塞的平衡。

这里提到 AIO，它是 Asynchronous I/O 的简称（异步非阻塞 IO），是异步 IO，该异步 IO 需要依赖于操作系统底层的异步 IO 实现。

![image-20240325093142421](https://image.itbaima.cn/images/40/image-20240325098792701.png)

* 用户线程通过系统调用，告知 kernel 内核启动某个 IO 操作，用户线程返回；
  * kernel 内核在整个 IO 操作（包括数据准备、数据复制）完成后，通知用户程序，用户执行后续的业务操作。

目前该技术在 Windows 下实现成熟，但很少作为百万级以上或高并发应用的服务器操作系统来使用。

Linux 系统下，异步 IO 模型在 2.6 版本才引入，目前并不完善。因此 Linux 下实现高并发网络编程时，通常以 NIO 多路复用模型为主。

---

# Reactor 线程模型

## 基础概念

Reactor 线程模型不是 Java 专属，也不是 Netty 专属，它其实是一种并发编程模型，是一种思想，具有指导意义。

Reactor 模型中定义了三种角色：

* Reactor：负责监听和分配事件，将 I/O 事件分派给对应的 Handler。新的事件包含连接建立就绪、读就绪、写就绪等。
  * Acceptor：处理客户端新连接，并分派请求到处理器链中。
  * Handler：将自身与事件绑定，执行非阻塞读/写任务，完成 Channel 的读入，处理业务逻辑后，负责将结果写出 Channel。

---

## 单 Reactor

我们之前在 Java NIO 中实现的代码，其实就是一个类似的 Reactor 单线程模型：

![image-20240324173722934](https://image.itbaima.cn/images/40/image-20240324171733664.png)

在 Reactor 单线程模型中：

* 一个单独的线程运行一个事件循环，负责监听事件的发生（如网络请求），并将对应的处理工作委托给相应的处理器。
  * 一旦事件被 Reactor 检测到，就通知程序中相应的事件处理器（Handler）来相应地处理这些事件。

这样的模型好处是编码简单、实现容易，但所有业务都依赖单线程执行，容易达到性能瓶颈。因此可以将业务抽离出来放到线程池中执行，这就是单 Reactor 多线程模型：

![image-20240324175554772](https://image.itbaima.cn/images/40/image-20240324173263805.png)

---

## 主从 Reactor

在单 Reactor 多线程模型中，虽然我们已经将业务进行了分离，但仍然存在缺陷：

* 假如有多个 Handler 在执行 read 操作，则当前的线程仍然可能被阻塞；
  * 对于其他 Client 发起的连接请求将会阻塞，这就存在丢失连接的风险。

对于服务器来说，接收客户端的连接是比较重要的，因此可以将这部分操作单独用线程去处理。

![image-20240324181304451](https://image.itbaima.cn/images/40/image-20240324188957887.png)
这里的 subReactor 可以有多个，但都只负责对连接建立事件的监听，已建立连接的 SocketChannel 将会注册到 MainReactor 中。

# Netty 概述

Netty 是由 JBOSS 提供的一个 Java 开源框架，现为 GitHub 上的独立项目，[项目地址](https://github.com/netty/netty)。

Netty 提供非阻塞的、事件驱动的网络应用程序框架和工具，用以快速开发高性能、高可靠性的网络服务器和客户端程序：

* 本质：网络应用程序框架
  * 实现：异步、事件驱动
  * 特性：高性能、可维护、快速开发
  * 用途：开发服务器和客户端

## Netty 架构设计

![image-20240325151500031](https://image.itbaima.cn/images/40/image-20240325158390948.png)

**核心：**

* 可扩展的事件模型
* 统一的通信 API，简化了通信编码
* 零拷贝机制与丰富的字节缓冲区

**传输服务：**

* 支持 socket 以及 datagram（数据报）
* HTTP 传输服务
* In-VM Pipe（管道协议，是 JVM 的一种进程）

**协议支持：**

* HTTP 以及 WebSocket
* SSL 安全套接字协议支持
* Google Protobuf（序列化框架）
* 支持 zlib、gzip 压缩，支持大文件的传输
* RTSP（实时流传输协议，是 TCP/IP 协议体系中的一个应用层协议）
* 支持二进制协议并且提供了完整的单元测试

## Netty 核心优势

**API 隔离**：

* JDK 中 NIO 的一些 API 功能薄弱且复杂
* Netty 隔离了 JDK 中 NIO 的实现变化及实现细节
* 譬如：ByteBuffer -&gt; ByteBuf 主要负责从底层的 IO 中读取数据到 ByteBuf
* 然后传递给应用程序，应用程序处理完之后封装为 ByteBuf，写回给 IO

**简化开发**：

* 使用 JDK 原生 API 需要对多线程要很熟悉
* 因为 NIO 涉及到 Reactor 设计模式，得对里面的原理要相当的熟悉

**高可用机制**：

* JDK 原生方式要实现高可用，需要自己实现断路重连、半包读写、粘包处理、失败缓存处理等相关操作
* 而 Netty 则做的更多，它解决了传输的一些问题譬如粘包半包现象，它支持常用的应用层协议，完善的断路重连等异常处理

**缺陷处理**：

* JDK 的 NIO 存在 bug，如经典的 epoll bug，会导致 CPU 100%
* 而 Netty 封装的更完善

## Netty 线程模型

![image-20240325210837433](https://image.itbaima.cn/images/40/image-20240325215461744.png)

Netty 线程模型是基于 Reactor 模型实现的，对 Reactor 的三种模式都有非常好的支持，并做了一定的改进，也非常的灵活，一般情况，在服务端会采用主从架构模型。

对于主从 Reactor 架构：

![image-20240325211729921](https://image.itbaima.cn/images/40/image-20240325212635047.png)

Netty 抽象出两组线程池：

*   BossGroup 和 WorkerGroup，每个线程池中都有 EventLoop 线程（可以是OIO，NIO，AIO）
    *   BossGroup 中的线程专门负责和客户端建立连接
    *   WorkerGroup 中的线程专门负责处理连接上的读写
    *   EventLoopGroup 相当于一个事件循环组，这个组中含有多个事件循环

EventLoop 表示一个不断循环的执行事件处理的线程，每个 EventLoop 都包含一个 Selector，用于监听注册在其上的 Socket 网络连接（Channel）

每个 Boss EventLoop 中循环执行以下三个步骤：

*   select：轮询注册在其上的 ServerSocketChannel 的 accept 事件（OP_ACCEPT 事件）
    *   processSelectedKeys：处理 accept 事件，与客户端建立连接，生成一个 SocketChannel，并将其注册到某个 WorkerEventLoop 上的 Selector 上
    *   runAllTasks：再去依次循环处理任务队列中的其他任务

每个 WorkerEventLoop 中循环执行以下三个步骤：

*   select：轮询注册在其上的 SocketChannel 的 read/write 事件（OP_READ/OP_WRITE 事件）
    *   processSelectedKeys：在对应的 SocketChannel 上处理 read/write 事件
    *   runAllTasks：再去依次循环处理任务队列中的其他任务

在以上两个 processSelectedKeys 步骤中，会使用 Pipeline（管道），Pipeline 中引用了 Channel，即通过 Pipeline 可以获取到对应的 Channel，Pipeline 中维护了很多的处理器（拦截处理器、过滤处理器、自定义处理器等）

## Pipeline 和 Handler

### ChannelPipeline 处理流程

ChannelPipeline 提供了 ChannelHandler 链的容器：

![image-20240325213317524](https://image.itbaima.cn/images/40/image-20240325215557848.png)

以服务端程序为例：

*   客户端发送过来的数据要接收，读取处理，我们称数据是入站的
    *   入站的数据交由各个 Handler 处理，即执行具体的业务逻辑
    *   如果服务器想向客户端写回数据，也需要经过一系列 Handler 处理，我们称数据是出站的

Handler 的头节点和尾节点都是初始化好的，用户无需自己实现，只需要实现中间的 Handler 即可

当一个事件如接收到数据或者异常发生时，这个事件会按照 ChannelPipeline 中的 ChannelHandler 的顺序被处理，每个 ChannelHandler 可以传递给下一个，直到有一个处理器处理它或者 Pipeline 中没有更多的处理器了，这个处理过程是**责任链设计模式** 的体现。

---

### ChannelHandler 体系结构

在 ChannelPipeline 的处理流程中，对于入站和出站的数据，对应的 ChannelHandler 的类型不同：

- **ChannelInboundHandler**：入站事件处理器
- **ChannelOutBoundHandler**：出站事件处理器
- **ChannelHandlerAdapter**：提供了一些方法的默认实现，可减少用户对于 ChannelHandler 的编写
- **ChannelDuplexHandler**：混合型，既能处理入站事件又能处理出站事件

![ChannelHandler 继承关系图](https://image.itbaima.cn/images/40/image-20240325214690468.png)

inbound 入站事件处理顺序（方向）是由链表的头到链表尾，outbound 事件的处理顺序是由链表尾到链表头：

- inbound 入站事件由 Netty 内部触发，最终由 Netty 外部的代码消费
- outbound 事件由 Netty 外部的代码触发，最终由 Netty 内部消费

---

# Quick Start

## 引入依赖

```xml
&lt;dependency&gt;
    &lt;groupId&gt;io.netty&lt;/groupId&gt;
    &lt;artifactId&gt;netty-all&lt;/artifactId&gt;
    &lt;version&gt;4.1.42.Final&lt;/version&gt;
&lt;/dependency&gt;
```

这里为了后续便于演示，添加 slf4j：

```xml
&lt;dependency&gt;
    &lt;groupId&gt;org.slf4j&lt;/groupId&gt;
    &lt;artifactId&gt;slf4j-simple&lt;/artifactId&gt;
    &lt;version&gt;1.7.25&lt;/version&gt;
&lt;/dependency&gt;

&lt;dependency&gt;
    &lt;groupId&gt;org.slf4j&lt;/groupId&gt;
    &lt;artifactId&gt;slf4j-api&lt;/artifactId&gt;
    &lt;version&gt;1.7.25&lt;/version&gt;
&lt;/dependency&gt;
```

---

## 编写 Server

### 配置 Server

```java
public class NettyServer {

    private static final Logger log = LoggerFactory.getLogger(NettyServer.class);

    public static void main(String[] args) {
        NettyServer nettyServer = new NettyServer();
        nettyServer.start(8888);
    }

    public void start(int port) {
        // 创建 bossGroup、workerGroup，分别管理连接建立事件和具体的业务处理事件
        EventLoopGroup boss = new NioEventLoopGroup();
        EventLoopGroup worker = new NioEventLoopGroup();
        try {
            // 创建启动引导类
            ServerBootstrap serverBootstrap = new ServerBootstrap();
            // 配置参数
            serverBootstrap.group(boss, worker)
                    .channel(NioServerSocketChannel.class)        // 指定服务端通道，用于接收并创建新连接
                    .handler(new LoggingHandler(LogLevel.DEBUG))  // 给 boss group 配置 handler
                    .childHandler(new ChannelInitializer&lt;SocketChannel&gt;() {
                        // 每个客户端 channel 初始化时都会执行该方法来配置该 channel 的相关 handler
                        @Override
                        protected void initChannel(SocketChannel ch) throws Exception {
                            // 获取与该 channel 绑定的 pipeline
                            ChannelPipeline pipeline = ch.pipeline();
                            // 向 pipeline 中添加 handler，如果没有注册到这里则不会生效
                            pipeline.addLast(new ServerOutboundHandler1());
                            pipeline.addLast(new ServerInboundHandler1());
                            pipeline.addLast(new ServerInboundHandler2());
                        }
                    }); // 给 worker group 配置 handler
            // 服务端绑定端口启动
            ChannelFuture future = serverBootstrap.bind(port).sync();
            // 服务端监听端口关闭
            future.channel().closeFuture().sync();
        } catch (Exception e) {
            log.error("netty server error, {}", e.getMessage());
        } finally {
            // 优雅关闭 boss 和 worker 线程组
            boss.shutdownGracefully();
            worker.shutdownGracefully();
        }
    }
}
```

这样我们就配置好了服务端，我们需要做的就是完成 worker 的 Pipeline 中各个 Handler 的处理逻辑即可。

---

### 编写 Handler

对于入站处理数据，需要一个 Inbound 类型的 Handler：

```java
public class ServerInboundHandler1 extends ChannelInboundHandlerAdapter {
    private static final Logger log = LoggerFactory.getLogger(ServerInboundHandler1.class);

    /**
     * 通道准备就绪时
     *
     * @param ctx
     * @throws Exception
     */
    @Override
    public void channelActive(ChannelHandlerContext ctx) throws Exception {
        log.info("ServerInboundHandler1 channelActive-----");

        // 将事件向下传递
        ctx.fireChannelActive();
    }

    /**
     * 通道有数据可读时
     *
     * @param ctx
     * @param msg
     * @throws Exception
     */
    @Override
    public void channelRead(ChannelHandlerContext ctx, Object msg) throws Exception {
        log.info("ServerInboundHandler1 channelRead----,remoteAddress={}", ctx.channel().remoteAddress());
        // 处理接收的数据
        ByteBuf buf = (ByteBuf) msg;
        log.info("ServerInboundHandler1:received client data = {}", buf.toString(StandardCharsets.UTF_8));

        // 将事件消息向下传递，如果不传递则 msg 不会到达下一个 handler
        ctx.fireChannelRead(msg);
    }

    /**
     * 数据读取完毕时
     *
     * @param ctx
     * @throws Exception
     */
    @Override
    public void channelReadComplete(ChannelHandlerContext ctx) throws Exception {
        log.info("channelReadComplete----");
        // 数据读取结束后向客户端写回数据
        byte[] data = "hello client, i am server".getBytes(StandardCharsets.UTF_8);
        ByteBuf buffer = Unpooled.buffer(data.length);
        buffer.writeBytes(data); // 以bytebuf为中心，看是写到bytebuf中还是从bytebuf中读
        ByteBuf buf = Unpooled.copiedBuffer("hello client, i am server", StandardCharsets.UTF_8);
        ctx.writeAndFlush(buf); // 通过ctx写，事件会从当前handler向pipeline头部移动
        // ctx.channel().writeAndFlush(buf); // 通过Channel写，事件会从通道尾部向头部移动
    }

    /**
     * 发生异常时
     *
     * @param ctx
     * @param cause
     * @throws Exception
     */
    @Override
    public void exceptionCaught(ChannelHandlerContext ctx, Throwable cause) throws Exception {
        log.info("ServerInboundHandler1 exceptionCaught----, cause={}", cause.getMessage());
    }
}
```

这里要注意，如果该 Handler 需要向下传递数据，即要让他之后的 Handler 也拿到 msg，需要在 channelRead 内通过 ChannelHandlerContext 的 fireChannelRead 方法。

再来一个 ServerInboundHandler2 进行 msg 传递测试：

```java
@ChannelHandler.Sharable
public class ServerInboundHandler2 extends ChannelInboundHandlerAdapter {
    private static final Logger log = LoggerFactory.getLogger(ServerInboundHandler2.class);

    @Override
    public void channelActive(ChannelHandlerContext ctx) throws Exception {
        log.info("ServerInboundHandler2 channelActive-----");
    }

    @Override
    public void channelRead(ChannelHandlerContext ctx, Object msg) throws Exception {
        log.info("ServerInboundHandler2 channelRead----,remoteAddress={}", ctx.channel().remoteAddress());
        // 处理接收的数据
        ByteBuf buf = (ByteBuf) msg;
        log.info("ServerInboundHandler2:received client data = {}", buf.toString(StandardCharsets.UTF_8));
    }

    @Override
    public void channelReadComplete(ChannelHandlerContext ctx) throws Exception {
        log.info("ServerInboundHandler2 channelReadComplete----");
    }

    @Override
    public void exceptionCaught(ChannelHandlerContext ctx, Throwable cause) throws Exception {
    }
}
```

在数据处理完后，会由 tail 节点写回，我们也可以编写 Outbound 类型的 Handler 来添加对出站数据的处理：
```java
public class ServerOutboundHandler1 extends ChannelOutboundHandlerAdapter {
    private static final Logger log = LoggerFactory.getLogger(ServerOutboundHandler1.class);

    /**
     * 通道准备就绪时
     *
     * @param ctx
     * @throws Exception
     */
    @Override
    public void channelActive(ChannelHandlerContext ctx) throws Exception {
        log.info("ServerOutboundHandler1 channelActive-----");

        // 将事件向下传递
        //ctx.fireChannelActive();
        super.channelActive(ctx);
    }

    /**
     * 通道有数据可读时
     *
     * @param ctx
     * @param msg
     * @throws Exception
     */
    @Override
    public void channelRead(ChannelHandlerContext ctx, Object msg) throws Exception {
        log.info("ServerInboundHandler1 channelRead, remoteAddress={}", ctx.channel().remoteAddress());
        // 处理接收的数据
        ByteBuf buf = (ByteBuf) msg;
        log.info("ServerInboundHandler1: received client data = {}", buf.toString(StandardCharsets.UTF_8));

        // 将事件消息向下传递，如果不传递则 msg 不会到达下一个 handler
        ctx.fireChannelRead(msg);
        // super.channelRead(ctx, msg);
    }

    /**
     * 数据读取完毕时
     *
     * @param ctx
     * @throws Exception
     */
    @Override
    public void channelReadComplete(ChannelHandlerContext ctx) throws Exception {
        log.info("channelReadComplete");
        // 数据读取结束后向客户端写回数据
        byte[] data = "hello client, I am server".getBytes(StandardCharsets.UTF_8);
        ByteBuf buffer = Unpooled.buffer(data.length);
        buffer.writeBytes(data); // 以bytebuf为中心，看是写到bytebuf中还是从bytebuf中读
        ByteBuf buf = Unpooled.copiedBuffer("hello client, I am server", StandardCharsets.UTF_8);
        ctx.writeAndFlush(buf); // 通过ctx写，事件会从当前handler向pipeline头部移动
        // ctx.channel().writeAndFlush(buf); // 通过Channel写，事件会从通道尾部向头部移动
    }

    /**
     * 发生异常时的处理
     *
     * @param ctx 上下文
     * @param cause 异常原因
     * @throws Exception 可能抛出的异常
     */
    @Override
    public void exceptionCaught(ChannelHandlerContext ctx, Throwable cause) throws Exception {
        log.info("ServerInboundHandler1 exceptionCaught----, cause={}", cause.getMessage());
    }
}
```

这里注意，在写回数据时：

- 如果调用的是 `ctx.channel().writeAndFlush()`：则会从 tail 节点从后往前寻找 Outbound 类型的 Handler 节点处理。
- 如果调用的是 `ctx.writeAndFlush()`：则会从当前的 Handler 流向 head。

---

## 编写 Client

### 配置 Client

```java
public class NettyClient {

    private static final Logger log = LoggerFactory.getLogger(NettyClient.class);

    public static void main(String[] args) {
        NettyClient client = new NettyClient();
        client.start("127.0.0.1", 8888);
    }

    public void start(String host, int port) {
        EventLoopGroup group = new NioEventLoopGroup();
        try {
            Bootstrap bootstrap = new Bootstrap();
            bootstrap.group(group)
                    .channel(NioSocketChannel.class)
                    .handler(new ChannelInitializer&lt;SocketChannel&gt;() {
                        @Override
                        protected void initChannel(SocketChannel ch) throws Exception {
                            ChannelPipeline pipeline = ch.pipeline();
                            // 添加客户端 channel 对应的 handler
                            pipeline.addLast(new ClientInboundHandler1());
                            pipeline.addLast(new ClientSimpleInboundHandler2());
                        }
                    });
            // 连接远程服务器
            ChannelFuture future = bootstrap.connect(host, port).sync();
            // 监听通道关闭
            future.channel().closeFuture().sync();
        } catch (Exception e) {
            log.error("netty client error, msg={}", e.getMessage());
        } finally {
            // 优雅关闭
            group.shutdownGracefully();
        }
    }
}
```

和服务端一样，只不过客户端不需要 worker，只需要完成当前 Pipeline 中各个 Handler 的处理逻辑即可。

---

### 编写 Handler

```java
public class ClientInboundHandler1 extends ChannelInboundHandlerAdapter {
    private static final Logger log = LoggerFactory.getLogger(ClientInboundHandler1.class);

    /**
     * 通道准备就绪
     *
     * @param ctx
     * @throws Exception
     */
    @Override
    public void channelActive(ChannelHandlerContext ctx) throws Exception {
        log.info("ClientInboundHandler1 channelActive begin send data");
        //通道准备就绪后开始向服务端发送数据
        ByteBuf buf = Unpooled.copiedBuffer("hello server,i am client".getBytes(StandardCharsets.UTF_8));
        ctx.writeAndFlush(buf);
    }

    /**
     * 通道有数据可读（服务端返回了数据）
     *
     * @param ctx
     * @param msg
     * @throws Exception
     */
    @Override
    public void channelRead(ChannelHandlerContext ctx, Object msg) throws Exception {
        log.info("ClientInboundHandler1 channelRead");
        ByteBuf buf = (ByteBuf) msg;
        log.info("ClientInboundHandler1: received server data ={}", buf.toString(StandardCharsets.UTF_8));

        // 接着传递消息给下一个 ChannelInboundHandler
        ctx.fireChannelRead(msg);
    }

    /**
     * 数据读取完毕
     *
     * @param ctx
     * @throws Exception
     */
    @Override
    public void channelReadComplete(ChannelHandlerContext ctx) throws Exception {
        super.channelReadComplete(ctx);
    }

    /**
     * 产生了异常
     *
     * @param ctx
     * @param cause
     * @throws Exception
     */
    @Override
    public void exceptionCaught(ChannelHandlerContext ctx, Throwable cause) throws Exception {
        super.exceptionCaught(ctx, cause);
    }
}
```

同样的，Client 的 ChannelInboundHandler 在 channelRead 也需要 fireChannelRead 才能将 msg 向后传递。

这里继续编写一个 Handler 用于测试 msg 传递：
```java
public class ClientSimpleInboundHandler2 extends SimpleChannelInboundHandler&lt;ByteBuf&gt; {
    private static final Logger log = LoggerFactory.getLogger(ClientSimpleInboundHandler2.class);

    @Override
    protected void channelRead0(ChannelHandlerContext ctx, ByteBuf msg) throws Exception {
        log.info("ClientSimpleInboundHandler2 channelRead");
        log.info("ClientSimpleInboundHandler2: received server data = {}", msg.toString(StandardCharsets.UTF_8));
    }
}
```

---

# Netty 核心组件剖析

这里我们仍然基于上述的 Netty 线程模型来看：

![image-20240325211729921](https://image.itbaima.cn/images/40/image-20240325212635047.png)

---

## Bootstrap

Bootstrap 是引导的意思，它的作用是配置整个 Netty 程序，将各个组件都串起来，最后绑定端口、启动 Netty 服务。

Netty 中提供了两种类型的引导类：

*   用于客户端的 `Bootstrap`
*   用于服务端的 `ServerBootstrap`

`ServerBootstrap` 将绑定到一个端口，因为服务器必须要监听连接，而 `Bootstrap` 则是由想要连接到远程节点的客户端应用程序所使用的。

引导一个客户端只需要一个 `EventLoopGroup`，但是一个 `ServerBootstrap` 则需要两个。

---

## Channel

Netty 中的 `Channel` 是与网络套接字相关的，可以理解为是 socket 连接。

在客户端与服务端连接的时候就会建立一个 `Channel`，它负责基本的 I/O 操作，比如：`bind()`、`connect()`、`read()`、`write()` 等。

主要作用：

*   通过 `Channel` 可获得当前网络连接的通道状态。
*   通过 `Channel` 可获得网络连接的配置参数（缓冲区大小等）。
*   `Channel` 提供异步的网络 I/O 操作，比如连接的建立、数据的读写、端口的绑定等。

不同协议、不同的 I/O 类型的连接都有不同的 `Channel` 类型与之对应。

---

## EventLoopGroup & EventLoop

Netty 是基于事件驱动的，比如：连接注册，连接激活；数据读取；异常事件等等。有了事件，就需要一个组件去监控事件的产生和事件的协调处理——这个组件就是 `EventLoop`（事件循环/EventExecutor）。

在 Netty 中，每个 Channel 都会被分配到一个 EventLoop，一个 EventLoop 可以服务于多个 Channel，每个 EventLoop 会占用一个 Thread，同时这个 Thread 会处理 EventLoop 上面发生的所有 IO 操作和事件。

EventLoopGroup 是用来生成 EventLoop 的，包含了一组 EventLoop，可以初步理解成 Netty 线程池。

在我们之前的示例代码中，EventLoopGroup 是接口，我们采用的实现是 NioEventLoopGroup：
```java
// 主线程，不处理任何业务逻辑，只是接收客户端的连接请求
EventLoopGroup boss = new NioEventLoopGroup();
// 工作线程，处理注册其上 Channel 的 I/O 事件及其他 Task
EventLoopGroup worker = new NioEventLoopGroup();
```

这里查看 NioEventLoopGroup 源码，继承自 MultithreadEventLoopGroup：
```java
private static final int DEFAULT_EVENT_LOOP_THREADS = Math.max(1, SystemPropertyUtil.getInt("io.netty.eventLoopThreads", NettyRuntime.availableProcessors() * 2));
```

其中 `DEFAULT_EVENT_LOOP_THREADS` 表示默认的核心线程数：

* 核心线程数默认为 max(1, CPU 核心数 * 2)
* 核心线程数在创建时可通过构造函数指定

对于 boss组，我们其实也只用到了其中的一个线程，因为服务端一般只会绑定一个端口启动。

---

## ChannelHandler 复用

每个客户端 Channel 创建后初始化时均会向与该 Channel 绑定的 Pipeline 中添加 Handler，此种模式下，每个 Channel 享有的是各自独立的 Handler，例如之前 NettyServer 中的配置初始化：
```java
.childHandler(new ChannelInitializer&lt;SocketChannel&gt;() {
    //每个客户端 channel 初始化时都会执行该方法来配置该 channel 的相关 handler
    @Override
    protected void initChannel(SocketChannel ch) throws Exception {
        //获取与该 channel 绑定的 pipeline
        ChannelPipeline pipeline = ch.pipeline();
        //向 pipeline 中添加 handler，如果没有注册到这里则不会生效
        pipeline.addLast(new ServerOutboundHandler1());
        pipeline.addLast(new ServerInboundHandler1());
        pipeline.addLast(new ServerInboundHandler2());
    }
});
```

原先上述方式会给每次新注册进来的 Channel 初始化新的 Handler，如果我们稍作修改：
```java
public class NettyServer {

    private static final Logger log = LoggerFactory.getLogger(NettyServer.class);

    public static void main(String[] args) {
        NettyServer nettyServer = new NettyServer();
        nettyServer.start(8888);
    }

    public void start(int port) {
        //创建 bossGroup workerGroup 分别管理连接建立事件和具体的业务处理事件
        EventLoopGroup boss = new NioEventLoopGroup();
        EventLoopGroup worker = new NioEventLoopGroup();

        // 只创建一次 serverInboundHandler2 对象
        ServerInboundHandler2 serverInboundHandler2 = new ServerInboundHandler2();
        try {
            // 创建启动引导类
            ServerBootstrap serverBootstrap = new ServerBootstrap();
            // 配置参数
            serverBootstrap.group(boss, worker)
                    .channel(NioServerSocketChannel.class)       // 指定服务端通道，用于接收并创建新连接
                    .handler(new LoggingHandler(LogLevel.DEBUG)) // 给 boss group 配置 handler
                    .childHandler(new ChannelInitializer&lt;SocketChannel&gt;() {
                        // 每个客户端 channel 初始化时都会执行该方法来配置该 channel 的相关 handler
                        @Override
                        protected void initChannel(SocketChannel ch) throws Exception {
                            // 获取与该 channel 绑定的 pipeline
                            ChannelPipeline pipeline = ch.pipeline();
                            // 向 pipeline 中添加 handler，如果没有注册到这里则不会生效
                            pipeline.addLast(new ServerOutboundHandler1());
                            pipeline.addLast(new ServerInboundHandler1());

                            // 在这里对 serverInboundHandler2 进行复用
                            pipeline.addLast(serverInboundHandler2);
                        }
                    }); // 给 worker group 配置 handler
            ChannelFuture future = serverBootstrap.bind(port).sync();
            future.channel().closeFuture().sync();
        } catch (Exception e) {
            log.error("netty server error, {}", e.getMessage());
        } finally {
            // 优雅关闭 boss worker
            boss.shutdownGracefully();
            worker.shutdownGracefully();
        }
    }
}
```

如果我们此时直接运行两个 NettyClient 实例并将其绑定到该 NettyServer，那么第二个运行的实例将会报错：
```
[nioEventLoopGroup-2-1] INFO handler.client.ClientInboundHandler1 - ClientInboundHandler1 channelActive begin send data
[nioEventLoopGroup-2-1] WARN io.netty.channel.DefaultChannelPipeline - An exceptionCaught() event was fired, and it reached the tail of the pipeline. It usually means the last handler in the pipeline did not handle the exception.
java.io.IOException: 你的主机中的软件中止了一个已建立的连接。
    at java.base/sun.nio.ch.SocketDispatcher.read0(Native Method)
    at java.base/sun.nio.ch.SocketDispatcher.read(SocketDispatcher.java:46)
    at java.base/sun.nio.ch.IOUtil.readIntoNativeBuffer(IOUtil.java:330)
    at java.base/sun.nio.ch.IOUtil.read(IOUtil.java:284)
    at java.base/sun.nio.ch.IOUtil.read(IOUtil.java:259)
    at java.base/sun.nio.ch.SocketChannelImpl.read(SocketChannelImpl.java:417)
    at io.netty.buffer.PooledByteBuf.setBytes(PooledByteBuf.java:247)
    at io.netty.buffer.AbstractByteBuf.writeBytes(AbstractByteBuf.java:1147)
    at io.netty.channel.socket.nio.NioSocketChannel.doReadBytes(NioSocketChannel.java:347)
    at io.netty.channel.nio.AbstractNioByteChannel$NioByteUnsafe.read(AbstractNioByteChannel.java:148)
    at io.netty.channel.nio.NioEventLoop.processSelectedKey(NioEventLoop.java:700)
    at io.netty.channel.nio.NioEventLoop.processSelectedKeysOptimized(NioEventLoop.java:635)
    at io.netty.channel.nio.NioEventLoop.processSelectedKeys(NioEventLoop.java:552)
    at io.netty.channel.nio.NioEventLoop.run(NioEventLoop.java:514)
    at io.netty.util.concurrent.SingleThreadEventExecutor$6.run(SingleThreadEventExecutor.java:1044)
    at io.netty.util.internal.ThreadExecutorMap$2.run(ThreadExecutorMap.java:74)
    at io.netty.util.concurrent.FastThreadLocalRunnable.run(FastThreadLocalRunnable.java:30)
    at java.base/java.lang.Thread.run(Thread.java:840)

Process finished with exit code 0
```

如果想要实现 ChannelHandler 复用，则只需要在对应需要复用的 Handler 上添加 @Sharable 注解即可：

![image-20240326162515692](https://image.itbaima.cn/images/40/image-20240326164394421.png)

对 ServerInboundHandler2 添加注解即可：
```java
@ChannelHandler.Sharable
public class ServerInboundHandler2 extends ChannelInboundHandlerAdapter {
    private static final Logger log = LoggerFactory.getLogger(ServerInboundHandler2.class);

    @Override
    public void channelActive(ChannelHandlerContext ctx) throws Exception {
        log.info("ServerInboundHandler2 channelActive-----");
    }

    @Override
    public void channelRead(ChannelHandlerContext ctx, Object msg) throws Exception {
        log.info("ServerInboundHandler2 channelRead----,remoteAddress={}", ctx.channel().remoteAddress());
        //处理接收的数据
        ByteBuf buf = (ByteBuf) msg;
        log.info("ServerInboundHandler2:received client data = {}", buf.toString(StandardCharsets.UTF_8));
    }

    @Override
    public void channelReadComplete(ChannelHandlerContext ctx) throws Exception {
        log.info("ServerInboundHandler2 channelReadComplete----");
    }

    @Override
    public void exceptionCaught(ChannelHandlerContext ctx, Throwable cause) throws Exception {
    }
}
```

---

## SimpleChannelInboundHandler

对于编写 Netty 数据入站处理器，可以选择继承 `ChannelInboundHandlerAdapter`，也可以选择继承 `SimpleChannelInboundHandler&lt;I&gt;`，区别是什么？

对于继承了 ChannelInboundHandlerAdapter 的 channelRead 方法：
```java
@Override
public void channelRead(ChannelHandlerContext ctx, Object msg) throws Exception {
    log.info("ServerInboundHandler1 channelRead ----, remoteAddress={}", ctx.channel().remoteAddress());
    // 处理接收的数据
    ByteBuf buf = (ByteBuf) msg;
    log.info("ServerInboundHandler1: received client data = {}", buf.toString(StandardCharsets.UTF_8));

    // 将事件消息向下传递，如果不传递则 msg 不会到达下一个 handler
    ctx.fireChannelRead(msg);
}
```

其中 `msg` 是 `Object` 类型的，因此在当前 `Handler` 处理时需要判断上一个 `Handler` 处理的 `msg` 是什么类型的。在之前的示例中，我们默认了处理的 `msg` 都是 `ByteBuf` 类型，每次处理都要做强制转换。

对于 `SimpleChannelInboundHandler&lt;I&gt;`，本质上也是继承自 `ChannelInboundHandlerAdapter`，但仅仅对其中的 `channelRead` 方法进行了重写：
```java
public void channelRead(ChannelHandlerContext ctx, Object msg) throws Exception {
    boolean release = true;
    try {
        // 判断是否是接收
        if (this.acceptInboundMessage(msg)) {
            // 调用 channelRead0 方法
            this.channelRead0(ctx, msg);
        } else {
            release = false;
            ctx.fireChannelRead(msg);
        }
    } finally {
        if (this.autoRelease && release) {
            // 对原始资源释放
            ReferenceCountUtil.release(msg);
        }
    }
}
```

继承 `SimpleChannelInboundHandler` 需要重写 `channelRead0` 方法，且可以通过泛型指定 `msg` 类型：
```java
protected abstract void channelRead0(ChannelHandlerContext var1, I var2) throws Exception;
```

这是一个抽象方法，参数将 `var2` 作为泛型指定，因此在使用 `SimpleChannelInboundHandler&lt;I&gt;` 指定的类型后，只需要重写 `channelRead0` 方法就可以帮我们把 `msg` 转换。

**注意**：

* `SimpleChannelInboundHandler` 在接收到数据后会自动释放数据占用的 `ByteBuf` 资源。
  * 服务端异步处理数据，或服务端想把客户端发送来的数据再写回等场景下，最好不要继承 `SimpleChannelInboundHandler`。
  * 客户端推荐使用 `SimpleChannelInboundHandler`，服务端视场景而定。

---

## ByteBuf

### 基础定义

Java NIO 提供了 `ByteBuffer` 作为它的字节容器，但是这个类使用起来过于复杂，而且也有些繁琐。

Netty 使用 `ByteBuf` 来替代 `ByteBuffer`，它是一个强大的实现，既解决了 JDK API 的局限性，又为网络应用程序的开发者提供了更好的 API。

从结构上来说：

* `ByteBuf` 由一串字节数组构成，数组中每个字节用来存放信息。
  * `ByteBuf` 提供了两个索引，一个用于读取数据（`readerIndex`），一个用于写入数据（`writerIndex`）。
  * 这两个索引通过在字节数组中移动，来定位需要读或者写信息的位置。
  * 而 JDK 的 `ByteBuffer` 只有一个索引，因此需要使用 `flip` 方法进行读写切换。

![image-20240401100837338](https://image.itbaima.cn/images/40/image-20240401101659546.png)

* `readerIndex`：
  * 指示读取的起始位置。
  * 每读取一个字节，readerIndex 自增累加 1。
  * 如果 readerIndex 与 writerIndex 相等，ByteBuf 不可读。
* `writerIndex`：
  * 指示写入的起始位置。
  * 每写入一个字节，writerIndex 自增累加 1。
  * 如果增加到 writerIndex 与 capacity() 容量相等，表示 ByteBuf 已经不可写。
* `maxCapacity`：
  * 指示 ByteBuf 可以扩容的最大容量。
  * 如果向 ByteBuf 写入数据时，容量不足，该值表示可以进行扩容的最大容量。

如果 `writerIndex` 与 `capacity()` 容量相等时继续向 `ByteBuf` 中写数据，Netty 会自动扩容 `ByteBuf`，直到扩容到底层的内存大小为 `maxCapacity`。

---

### 三种模式

**堆缓冲区 (HeapByteBuf)**：
* 内存分配在JVM堆，分配和回收速度比较快，可以被JVM自动回收。
* 缺点是：如果进行socket的IO读写，需要额外做一次内存复制，将堆内存对应的缓冲区复制到内核Channel中，性能会有一定程度的下降。
* 由于在堆上被JVM管理，在不被使用时可以快速释放，可以通过ByteBuf.array()来获取byte[]数据。

**直接缓冲区 (DirectByteBuf)**：
* 内存分配的是堆外内存（系统内存），相比堆内存，它的分配和回收速度会慢一些。
* 但是将它写入或从Socket Channel中读取时，由于减少了一次内存拷贝，速度比堆内存快。

**复合缓冲区 (CompositeByteBuf)**：
* 将两个不同的缓冲区从逻辑上合并，让使用更加方便。

Netty默认使用的是DirectByteBuf，如果需要使用HeapByteBuf模式，则需要进行系统参数的设置：
```java
// 设置HeapByteBuf模式，但ByteBuf的分配器ByteBufAllocator要设置为非池化，否则不能切换到堆缓冲区模式。
System.setProperty("io.netty.noUnsafe", "true");
```

---

### ByteBufAllocator

Netty提供了两种ByteBufAllocator的实现，分别是：

**PooledByteBufAllocator**：
* 实现了ByteBuf的对象的池化，提高性能并最大限度地减少内存碎片。
* 池化思想：通过预先申请一块专用内存地址作为内存池进行管理，从而不需要每次都进行分配和释放。

**UnpooledByteBufAllocator**：
* 没有实现对象的池化，每次会生成新的对象实例。

Netty默认使用了PooledByteBufAllocator，但可以通过引导类设置非池化模式。

参考源码DefaultChannelConfig中的`allocator`属性：
```java
// 引导类中设置非池化模式
bootstrap.childOption(ChannelOption.ALLOCATOR, UnpooledByteBufAllocator.DEFAULT);

// 或者通过系统参数设置
System.setProperty("io.netty.allocator.type", "pooled");
System.setProperty("io.netty.allocator.type", "unpooled");
```

对于Pooled类型的ByteBuf：

* 不管是PooledDirectByteBuf还是PooledHeapByteBuf，都只能由Netty内部自己使用（构造是私有和受保护的）。
* 开发者可以使用Unpooled类型的ByteBuf。

Netty提供`Unpooled`工具类创建的ByteBuf都是unpooled类型，默认采用的Allocator是direct类型；当然用户可以自己选择创建`UnpooledDirectByteBuf`和`UnpooledHeapByteBuf`。

---

### ByteBuf 释放机制

**ByteBuf 不同模式下的释放：**

* ByteBuf 如果采用的是堆缓冲区模式，可以由 GC 回收。
  * 但如果是直接缓冲区，则不受 GC 管理，需要手动释放，否则会发生内存泄露。

Netty 自身引入了引用计数，提供了 `ReferenceCounted` 接口。当对象的引用计数 > 0 时，需保证对象不被释放；当为 0 时，则需要被释放。这里分为手动释放和自动释放：

* **手动释放：**
  ```java
  // 在使用完成后，调用 ReferenceCountUtil.release(byteBuf) 进行释放
  // 这种方式的弊端是，一旦忘记释放就可能造成内存泄露
  ```
* **自动释放：**
  ```java
  // 有三种方式：入站的 TailHandler（TailContext）、继承 SimpleChannelInboundHandler，以及 HeadHandler（HeadContext）的出站释放。
  // * TailContext：Inbound 流水线的末端，如果前面的 Handler 都把消息向后传递，最终由 TailContext 释放该消息。需要注意的是，如果没有进行向下传递，则不会进行释放操作。
  // * SimpleChannelInboundHandler：自定义的 InboundHandler 继承自 SimpleChannelInboundHandler，会在该类中自动释放。
  // * HeadContext（outbound）：Outbound 流水线的末端。出站消息一般由应用申请，到达最后一站时，经过一系列调用，在 flush 完成后终将被 release 掉。
  ```

**总结：**

* **对于入站消息：**
  ```java
  // * 对原消息不做处理，依次调用 ctx.fireChannelRead(msg) 往下传。如果能到达 TailContext，则无需手动释放，它会自动释放。
  // * 若将原消息转化为新的消息并调用 ctx.fireChannelRead(newMsg) 往下传，则需手动 release 掉原消息。
  // * 若不再调用 ctx.fireChannelRead(msg) 传递任何消息，则需手动 release 掉原消息。
  ```
* **对于出站消息：**
  ```java
  // * 无需用户关心。
  // * 消息最终都会到达 HeadContext，flush 之后会自动释放。
  ```

---

## Future & Promise

### Netty 的异步编程模型

对于 JDK5 的 Future，在调用后想要获取任务执行的返回值，必须通过 `future.get()` 方法监听 Future 对象中的 result 字段，这会导致线程阻塞。

![image-20240427025809309](https://image.itbaima.cn/images/40/image-20240427025787659.png)

对于 Netty，它的异步模型为 Future/Promise 异步模型：

Future 和 Promise 的设计目的是将值（Future）与其计算方式（Promise）分离，从而允许更灵活地进行计算，特别是通过并行化。  
Future 表示目标计算的返回值，Promise 表示计算的方式。该模型将返回结果与计算逻辑分离，目的是让计算逻辑不影响返回结果，从而抽象出一套异步编程模型。而计算逻辑与结果关联的纽带就是回调（Callback）。  
Netty 中有大量的异步调用，例如客户端/服务器的启动、连接、数据的读写等操作均支持异步。

> 对于 JDK 8，新增了 CompletableFuture 类，它提供了对 Future 强大的扩展功能，最重要的是实现了回调的功能。

---

### Netty Future

Netty 中使用 ChannelFuture 来实现异步操作，其中 ChannelFuture 继承自 `io.netty.util.concurrent.Future` 接口：
```java
public interface Future&lt;V&gt; extends java.util.concurrent.Future&lt;V&gt; {
  // 只有IO操作完成时才返回true
  boolean isSuccess();
  // 只有当cancel(boolean)成功取消时才返回true
  boolean isCancellable();
  // IO操作发生异常时，返回导致IO操作意外的原因，如果没有异常，返回null
  Throwable cause();
  // 向Future添加监听器，future完成时，会执行这些监听器；如果添加时future已经完成，会立即执行监听事件
  Future&lt;V&gt; addListener(GenericFutureListener&lt;? extends Future&lt;? super V&gt;> listener);
  Future&lt;V&gt; addListeners(GenericFutureListener&lt;? extends Future&lt;? super V&gt;>... listeners);
  // 移除监听器，future完成时不会触发
  Future&lt;V&gt; removeListener(GenericFutureListener&lt;? extends Future&lt;? super V&gt;> listener);
  Future&lt;V&gt; removeListeners(GenericFutureListener&lt;? extends Future&lt;? super V&gt;>... listeners);
  // 等待future完成
  Future&lt;V&gt; sync() throws InterruptedException;
  // 等待future完成，不可中断
  Future&lt;V&gt; syncUninterruptibly();
  // 等待future完成
  Future&lt;V&gt; await() throws InterruptedException;
  // 等待future完成，不可中断
  Future&lt;V&gt; awaitUninterruptibly();
  boolean await(long timeout, TimeUnit unit) throws InterruptedException;
  boolean await(long timeoutMillis) throws InterruptedException;
  boolean awaitUninterruptibly(long timeout, TimeUnit unit);
  boolean awaitUninterruptibly(long timeoutMillis);
  // 立即获取结果，如果future未完成，返回null
  V getNow();
  // 如果成功取消，future会失败，抛出CancellationException
  @Override
  boolean cancel(boolean mayInterruptIfRunning);
}
```

Netty 自己实现的 Future 继承了 JDK 的 Future，新增了 `sync()` 和 `await()` 用于阻塞等待，还加了 Listeners，只要任务结束去回调 Listener 就可以了，那么我们就不一定要主动调用 `isDone()` 来获取状态，或通过 `get()` 阻塞方法来获取值。

Netty 的 Future 与 Java 的 Future 虽然类名相同，但功能上略有不同，Netty 中引入了 Promise 机制。

---

### Netty Promise

Netty 的 Future，只是增加了监听器。整个异步的状态，是不能进行设置和修改的，于是 Netty 的 Promise 接口扩展了 Netty 的 Future 接口，可以设置异步执行的结果。在IO操作过程，如果顺利完成、或者发生异常，都可以设置 Promise 的结果，并且通知 Promise 的 Listener 们，示例如下：
```java
package netty;

import io.netty.channel.EventLoopGroup;
import io.netty.channel.nio.NioEventLoopGroup;
import io.netty.util.concurrent.DefaultPromise;
import io.netty.util.concurrent.Future;
import io.netty.util.concurrent.Promise;
import org.junit.Test;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.time.LocalDateTime;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.TimeUnit;

public class NettyFutureTest {
    private static final Logger log = LoggerFactory.getLogger(NettyFutureTest.class);

    @Test
    public void testFuture() throws InterruptedException, ExecutionException {
        EventLoopGroup group = new NioEventLoopGroup();
        Future&lt;String&gt; future = group.submit(() -> {
            log.info("---异步线程执行任务开始----,time={}", LocalDateTime.now().toString());
            try {
                TimeUnit.SECONDS.sleep(3);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            log.info("---异步线程执行任务结束----,time={}", LocalDateTime.now().toString());
            return "hello netty future";
        });
        /*String result = future.get();
        log.info("----主线程阻塞等待异步线程执行结果:{}",result);*/
        // 设置监听
        future.addListener(future1 -> {
            log.info("---收到异步线程执行任务结果通知----执行结果是:{},time={}", future1.get(), LocalDateTime.now().toString());
        });
        log.info("---主线程----");
        TimeUnit.SECONDS.sleep(10);
    }

    @Test
    public void testPromise() throws InterruptedException {
        EventLoopGroup group = new NioEventLoopGroup();
        Promise&lt;String&gt; promise = new DefaultPromise<>(group.next()); // promise绑定到EventLoop上
        group.submit(() -> {
            log.info("---异步线程执行任务开始----, time={}", LocalDateTime.now().toString());
            try {
                int i = 1 / 0;
                TimeUnit.SECONDS.sleep(3);
                promise.setSuccess("hello netty promise");
                TimeUnit.SECONDS.sleep(3);
                log.info("---异步线程执行任务结束----, time={}", LocalDateTime.now().toString());
                return;
            } catch (Exception e) {
                promise.setFailure(e);
            }
        });
        // 设置监听回调
        promise.addListener(future -> {
            log.info("----异步任务执行结果: {}", future.isSuccess());
        });
        promise.addListener(future2 -> {
            log.info("----异步任务执行结果: {}", future2.isSuccess());
        });
        log.info("---主线程----");
        TimeUnit.SECONDS.sleep(10);
    }
}
```

在 Java 的 Future 中，业务逻辑为一个 Callable 或 Runnable 实现类，该类的 `call()` 或 `run()` 执行完毕意味着业务逻辑的结束。在 Promise 机制中，可以在业务逻辑中人工设置业务逻辑的成功与失败，这样更加方便地监控自己的业务逻辑。

---

# Netty 编码器

## TCP 粘包拆包

### Socket 缓冲区与滑动窗口

Netty 底层是基于 TCP 协议来处理网络数据传输，而对于 TCP 协议而言，它传输数据是**基于字节流传输**的。

应用层在传输数据时：

* 实际上会先将数据写入到 TCP 套接字的缓冲区，当缓冲区被写满后，数据才会被发送出去。
  * 每个 TCP Socket 在内核中都有一个发送缓冲区（SO_SNDBUF）和一个接收缓冲区（SO_RCVBUF）。
  * TCP 的全双工工作模式以及 TCP 的滑动窗口机制便是依赖于这两个独立的缓冲区及其填充状态。

**SO_SNDBUF：**

* 进程发送数据时，假设调用了 send 方法，会将数据拷贝进入 Socket 的内核发送缓冲区之中，然后 send 便会在上层返回。
  * 换句话说，send 返回之时，数据不一定会立即发送到对端（和 write 写文件有点类似），send 仅仅是把应用层缓冲区的数据拷贝进 Socket 的内核发送缓冲区中。

**SO_RCVBUF：**

将接收到的数据缓存入内核后，若应用进程一直没有调用 `read` 进行读取，此数据会一直缓存在相应 Socket 的接收缓冲区内。无论进程是否读取 Socket，对端发来的数据都会经由内核接收并缓存到 Socket 的内核接收缓冲区中。  
* `read` 所做的工作，就是把内核缓冲区中的数据拷贝到应用层用户的 buffer 里，仅此而已。

接收缓冲区保存收到的数据，直到应用进程读取为止。对于 TCP，如果应用进程一直没有读取，当 buffer 满了之后，会通知对端 TCP 窗口关闭。这就是滑动窗口的实现机制，确保 TCP 套接口接收缓冲区不会溢出，从而保证 TCP 是可靠传输。因为对方不允许发送超过所通告窗口大小的数据。这就是 TCP 的流量控制——如果对方无视窗口大小而发送了超过窗口大小的数据，接收方 TCP 将丢弃它。

**滑动窗口：**

* TCP 连接在三次握手时，会将自己的窗口大小（window size）发送给对方，该值实际为 `SO_RCVBUF` 指定的值。之后在发送数据时，发送方必须先确认接收方的窗口未被填满，若未填满，则可发送数据。
  * 每次发送数据后，发送方会减小自己维护的对方 window size，表示对方的 `SO_RCVBUF` 可用空间减小。
  * 当接收方开始处理 `SO_RCVBUF` 中的数据时，会将数据从 Socket 在内核中的接收缓冲区读出，此时接收方的 `SO_RCVBUF` 可用空间变大，即 window size 增大。接收方会通过 ACK 消息将自己最新的 window size 返回给发送方，发送方随即将自己维护的接收方 window size 设置为 ACK 消息中返回的值。
  * 此外，发送方可以连续向接收方发送消息，只要对方的 `SO_RCVBUF` 空间能够缓存数据即可，即 window size > 0。当接收方的 `SO_RCVBUF` 被填满时，此时 window size = 0，发送方不能再继续发送数据，需等待接收方的 ACK 消息，以获取最新的可用 window size。

---

### MSS / MTU 分片

MTU（Maximum Transmission Unit，最大传输单元）是链路层对一次可发送的最大数据的限制。MSS（Maximum Segment Size，最大分段大小）是 TCP 报文中 data 部分的最大长度，是传输层对一次可发送的最大数据的限制。

数据在传输过程中，每经过一层，都会加上一些额外的信息：

应用层：只关心发送的数据 data，将数据写入 Socket 在内核中的缓冲区 SO_SNDBUF 即返回，操作系统会将 SO_SNDBUF 中的数据取出来进行发送；
* 传输层：会在 data 前面加上 TCP Header（20字节）；
* 网络层：会在 TCP 报文的基础上再添加一个 IP Header，也就是将自己的网络地址加入到报文中。IPv4 中 IP Header 长度是 20 字节，IPv6 中 IP Header 长度是 40 字节；
* 链路层：加上 Datalink Header 和 CRC。会将 SMAC（Source Machine，数据发送方的MAC地址）、DMAC（Destination Machine，数据接收方的MAC地址）和 Type 域加入。SMAC + DMAC + Type + CRC 总长度为 18 字节；
* 物理层：进行传输。

MTU 是以太网传输数据方面的限制，每个以太网帧最大不能超过 1518 Bytes。刨去以太网帧的帧