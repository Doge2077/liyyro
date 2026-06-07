---
title: "Java-Agent 实现字节码热替换"
date: 2024-07-23
categories: [Java, Tips]
description: ""
---

# java-agent-实现字节码热替换


## 问题背景

正在运行中的 SpringBoot 项目需要在不停机的情况下，针对某个 Aop 切面的方法体内容进行修改，需要执行字节码替换的类为：

```java
package com.test.agent.aop;

@Aspect
@Component
public class TestAgentAop {

    @Before("execution(* com.test.agent.controller..*(..))")
    public void logBefore(JoinPoint joinPoint) {
    }

}
```

我们的目标是将其中的 `logBefore` 方法进行修改，这里用一个简单的示例，可以通过其获取到 controller 入参的所有参数：

```java
package com.test.agent.aop;

@Aspect
@Component
public class TestAgentAop {

    @Before("execution(* com.test.agent.controller..*(..))")
    public void logBefore(JoinPoint joinPoint) {
        // 输出入参的方法
        System.out.println("Method Name: " + joinPoint.getSignature().getName());
        // 输出该方法下的所有入参
        Object[] args = joinPoint.getArgs();
        for (int i = 0; i < args.length; i++) {
            System.out.println("Argument: " + args[i]);
        }
    }

}
```

## 问题分析

* 该 SpringBoot 项目处于运行中，需要针对运行中的类代码进行修改
    * 即对这个方法的字节码进行热替换
    * 考虑字节码增强技术，利用 Javassist 修改字节码，Java Agent 实现字节码热替换

## 解决方案

### 编写字节码修改探针类

创建 Maven 工程，引入 Javassist 依赖：

```xml
<dependencies>
    <dependency>
        <groupId>org.javassist</groupId>
        <artifactId>javassist</artifactId>
        <version>3.20.0-GA</version>
    </dependency>
</dependencies>
```

这里使用 Javassist 操作字节码是因为这种方式比 ASM 直接操作更为容易上手。

添加 `src/main/resources/META-INF/MANIFEST.MF` 探针配置文件：

```
Manifest-Version: 1.0
Agent-Class: MyAgent
Can-Redefine-Classes: true
Can-Retransform-Classes: true
```

编写探针类 `MyAgent`：

```java
import javassist.ClassPool;
import javassist.CtClass;
import javassist.CtMethod;

import java.lang.instrument.ClassFileTransformer;
import java.lang.instrument.Instrumentation;
import java.security.ProtectionDomain;

public class MyAgent {
    static String methodName = "logBefore";                           // 需要替换的方法名称
    static String classPath = "com.test.agent.aop.TestAgentAop";      // 需要替换的方法所在的类
    static String replaceName = "com/test/agent/aop/TestAgentAop";    // 底层类名是以 '/' 区分的

    public static void agentmain(String agentArgs, Instrumentation inst) {
        System.out.println("Agent loading");
        try {
            inst.addTransformer(new ClassFileTransformer() {
                @Override
                public byte[] transform(ClassLoader loader, String className, Class<?> classBeingRedefined,
                                        ProtectionDomain protectionDomain, byte[] classfileBuffer) {
                    if (className.equals(replaceName)) {
                        try {
                            ClassPool cp = ClassPool.getDefault();
                            CtClass cc = cp.get(classPath);
                            CtMethod m = cc.getDeclaredMethod(methodName);
                            m.setBody("{ "
                                    + "org.aspectj.lang.JoinPoint jp = $1;"
                                    + "System.out.println(\"Method Name: \" + jp.getSignature().getName()); "
                                    + "java.lang.Object[] args = jp.getArgs(); "
                                    + "for (int i = 0; i < args.length; i++) { System.out.println(\"Argument: \" + args[i]); }"
                                    + "}");
                            return cc.toBytecode();
                        } catch (Exception e) {
                            e.printStackTrace();
                        }
                    }
                    return null;
                }
            }, true);
            Class<?> targetClass = Class.forName(classPath);
            inst.retransformClasses(targetClass);
            System.out.println("Agent load successfully!");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

### 编写字节码热替换类

这里通过 Attach API 的 `loadAgent()` 方法，将预先打包好的探针动态 Attach 到目标 JVM 上，编写该工具类：

```java
import com.sun.tools.attach.VirtualMachine;

public class AttachAgent {
    static String pid = "114514";               // 替换为目标虚拟机进程 pid
    static String agentPath = "MyAgent.jar"; // 替换为打包好的 MyAgent.jar 路径

    public static void main(String[] args) {
        try {
            System.out.println("Attaching to JVM with PID: " + pid);
            VirtualMachine vm = VirtualMachine.attach(pid);
            System.out.println("Successfully attached to JVM with PID: " + pid);

            System.out.println("Loading agent from path: " + agentPath);
            vm.loadAgent(agentPath);   // 执行替换
            System.out.println("Agent loaded successfully.");

            vm.detach();
            System.out.println("Detached from JVM.");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

### 执行替换操作

首先将编写好的探针类与其 MANIFEST.MF 配置一起打包，因此需要在 Maven 中引入：

```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-jar-plugin</artifactId>
            <version>3.1.0</version>
            <configuration>
                <archive>
                    <manifestFile>src/main/resources/META-INF/MANIFEST.MF</manifestFile>
                </archive>
            </configuration>
        </plugin>
    </plugins>
</build>
```

然后填写 AttachAgent 中的配置信息：

* pid：使用 `jps -l` 或者 `ps -aux|grep java` 找到对应的 `XXXApplication` JVM 进程 pid
* agentPath：打包好的 MyAgent.jar 路径

然后运行 AttachAgent 即可完成替换。

## 注意事项

* 替换的 JavaAgent 需要和目标项目使用的 JDK 保持一致
* Javassist 需要引用的类型需要附加其所在的包，例如，使用 `Object` 应指定 `java.lang.Object`
* 不能使用增强 for 循环、lambda、方法引用等高级语法，如果需要应考虑 ASM 实现

