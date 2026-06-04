---
title: "Java 算竞操作"
date: 2024-06-01
categories: [ALGORITHM, Basic Algorithm, Java]
description: ""
---

## 输入输出

---

### 简单写法

---

数据量不大：
```java
Scanner sc = new Scanner(System.in);
int a = sc.nextInt();
char op = sc.nextLine().charAt(0);
```

如果比较大可以换：
```java
Scanner sc = new Scanner(new BufferedInputStream(System.in));
```

不嫌麻烦可以写：
```java
import java.io.*;

public class Main {
    static BufferedReader cin = new BufferedReader(new InputStreamReader(System.in));
    static PrintWriter cout = new PrintWriter(new OutputStreamWriter(System.out));

    public static void main(String[] args) throws IOException {
        int a = Integer.parseInt(cin.readLine());
        cout.println(a);
        cout.flush();
        cout.println(a);
        cout.flush();
        cin.close();
    }
}
```

---

### 快读板子

---
```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.util.StringTokenizer;

public class Main {
    static Cin cin = new Cin();
    static PrintWriter cout = new PrintWriter(System.out);

    static void solve() {
        int n = cin.nextInt();
        for (int i = 0; i < n; i++) {
            char op = cin.nextChar();
            cout.println(op);
        }
    }

    public static void main(String[] args) {
        int t = 1;
//        t = cin.nextInt();
        for (int i = 0; i < t; i++) {
            solve();
        }
        cout.flush();
    }

    static class Cin {
        static BufferedReader br;
        static StringTokenizer st;
    }
}
```java
import java.io.*;
import java.util.StringTokenizer;

public class Cin {
    private BufferedReader br;
    private StringTokenizer st;

    public Cin() {
        br = new BufferedReader(new InputStreamReader(System.in));
    }

    public String next() {
        String s = "";
        while (st == null || !st.hasMoreElements()) {
            try {
                s = br.readLine();
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
            st = new StringTokenizer(s);
        }
        return st.nextToken();
    }

    public int nextInt() {
        return Integer.parseInt(next());
    }

    public double nextDouble() {
        return Double.parseDouble(next());
    }

    public long nextLong() {
        return Long.parseLong(next());
    }

    public char nextChar() {
        return next().charAt(0);
    }
}
```

---

### 多实例输入

---
```java
import java.io.BufferedInputStream;
import java.util.Scanner;

public class Main {
    static Scanner sc = new Scanner(new BufferedInputStream(System.in));

    public static void main(String[] args) {
        while (sc.hasNext()) {
            int a = sc.nextInt();
            System.out.println(a);
        }
    }
}
```

---

##