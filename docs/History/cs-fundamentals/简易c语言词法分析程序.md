---
title: "简易C语言词法分析程序"
date: 2024-03-21
categories: [Compilation Principle]
description: ""
---

## 问题

---

**词法规则**：
```cpp
&lt;标识符&gt;::=&lt;字母&gt;
&lt;标识符&gt;::=&lt;标识符&gt;&lt;字母&gt;
&lt;标识符&gt;::=&lt;标识符&gt;&lt;数字&gt;
&lt;常量&gt;::=&lt;无符号整数&gt;
&lt;无符号整数&gt;::=&lt;数字序列&gt;
&lt;数字序列&gt;::=&lt;数字序列&gt;&lt;数字&gt;
&lt;数字序列&gt;::=&lt;数字&gt;
&lt;字母&gt;::=a|b|c|……|x|y|z
&lt;数字&gt;::=0|1|2|3|4|5|6|7|8|9
&lt;加法运算符&gt;::=+|-
&lt;乘法运算符&gt;::=*|／
&lt;关系运算符&gt;::=&lt;|&gt;|!=|>=|&lt;=|==
&lt;分界符&gt;::=,|;|(|)|{|}
&lt;保留字&gt;::=main|int|if|else|while|do
```

**符号表**：

| 单词符号 | 种类码 | 单词符号 | 种类码 |
|---------|--------|---------|--------|
| 标识符   | 0      | 整数    | 24     |
| main    | 1      | >=      | 10     |
| int     | 2      | &lt;=      | 11     |
| if      | 3      | ==      | 12     |
| else    | 4      | ,       | 13     |
| while   | 5      | ;       | 14     |
| do      | 6      | )       | 15     |
| &lt;       | 7      | (       | 16     |
| &gt;       | 8      | {       | 17     |
| !=      | 9      | }       | 18     |
| +       | 19     | -       | 20     |
| *       | 21     | /       | 22     |
| =       | 23     |         |        |

根据词法规则和符号表，制作词法分析器

---

## 思路

---

* 利用两个 `unordered_map` 分别存储关键字和其他符号的映射规则
  * 对于原程序中的空格符需要忽略
  * 利用 `std::ifstream` 读入文件，`std::istreambuf_iterator` 来遍历
  * 将字符拼接识别，判断即可

---

## 代码

---
```cpp
#include &lt;iostream&gt;
#include &lt;fstream&gt;
#include &lt;string&gt;
#include &lt;unordered_map&gt;
#include &lt;cctype&gt;

// 关键字和对应的种别码
std::unordered_map&lt;std::string, int&gt; keywords = {
    {"main", 1}, {"int", 2}, {"if", 3}, {"else", 4}, {"while", 5}, {"do", 6}
};

// 运算符和界符及其种别码
std::unordered_map&lt;std::string, int&gt; symbols = {
    {"&lt;", 7}, {"&gt;", 8}, {"!=", 9}, {">=", 10}, {"&lt;=", 11}, {"==", 12}, {",", 13}, 
    {";", 14}, {"(", 15}, {")", 16}, {"{", 17}, {"}", 18}, {"+", 19}, {"-", 20}, 
    {"*", 21}, {"/", 22}, {"=", 23}
};
```

// 检查是否是关键字或者符号，是的话返回种别码，否则返回0
int isKeywordOrSymbol(const std::string& str) {
    if (keywords.find(str) != keywords.end()) return keywords[str];
    if (symbols.find(str) != symbols.end()) return symbols[str];
    return 0;
}

// 检查字符是否是字母或数字
bool isLetterOrDigit(char ch) {
    return isalpha(static_cast&lt;unsigned char&gt;(ch)) || isdigit(static_cast&lt;unsigned char&gt;(ch));
}

void tokenize(const std::string& code, std::ostream &out) {
    std::string token;
    for (size_t i = 0; i &lt; code.length(); ++i) {
        if (isspace(static_cast&lt;unsigned char&gt;(code[i]))) {
            continue; // 忽略空格
        } else if (isLetterOrDigit(code[i])) {
            // 处理标识符和关键字
            token.clear();
            while (i &lt; code.length() && isLetterOrDigit(code[i])) {
                token += code[i++];
            }
            --i; // 回退到上一个字符
            int tokenCode = isKeywordOrSymbol(token);
            out &lt;&lt; "(" &lt;&lt; token &lt;&lt; "," &lt;&lt; (tokenCode ? tokenCode : 24) &lt;&lt; ")" &lt;&lt; std::endl;
        } else {
            // 处理符号
            token = code[i];
            if (i + 1 &lt; code.length() && symbols.count(token + code[i + 1])) {
                token += code[++i];
            }
            out &lt;&lt; "(" &lt;&lt; token &lt;&lt; "," &lt;&lt; symbols[token] &lt;&lt; ")" &lt;&lt; std::endl;
        }
    }
}

int main() {
    std::string inputPath = "C:\\Users\\LYS\\Downloads\\s.c";  // 输入文件路径
    std::string outputPath = "C:\\Users\\LYS\\Desktop\\result.txt";  // 输出文件路径
    // 其他代码应在此处添加，但用户未提供完整main函数体，因此保持原样
}

```
    std::ifstream fileIn(inputPath);
    std::ofstream fileOut(outputPath);

    if (!fileIn.is_open() || !fileOut.is_open()) {
        std::cerr &lt;&lt; "文件路径或权限错误" &lt;&lt; std::endl;
        return -1;
    }

    std::string content((std::istreambuf_iterator&lt;char&gt;(fileIn)), (std::istreambuf_iterator&lt;char&gt;()));

    // 执行词法分析，并将结果重定向输出到文件
    tokenize(content, fileOut);

    // 关闭文件流
    fileIn.close();
    fileOut.close();

    return 0;
}
```