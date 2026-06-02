---
title: "Spring Validation 详解"
date: 2024-08-14
categories: [Java]
description: ""
---

## 校验框架

* * *

SpringBoot 的 Validation：

  * Spring Boot中的验证功能是基于Java Bean Validation（Jakarta Validation）规范的
  * Spring Boot 通过 `spring-boot-starter-validation` 自动配置，实际使用的是 Hibernate Validator 作为其实现



Java Bean Validation：

  * Java Bean Validation 是JSR 303和JSR 380的一个执行标准（早期是JSR303，更新后是JSR380）
  * 定义了一套用于对象属性验证的 API 和注解，这个标准本身不提供具体的实现，只定义了规范
  * 在Java EE技术迁移到 Jakarta EE 之后，Java Bean Validation 变成了 Jakarta Validation



Hibernate Validator：

  * Hibernate Validator 是 Jakarta Validation 规范的参考实现
  * 它提供了该规范的完整实现，并且扩展了部分功能，使得验证更加灵活和强大



综上所述，SpringBoot 的 Validation 实际执行的是 Hibernate Validator，通过 Jakarta Validation API 对其进行了一层封装。

* * *

## 常用注解

* * *

### @Size

* * *

  * **用法** : 用于验证字符串、集合、数组等的长度或大小。

  * 属性：

```java
* `min`: 最小长度或大小（默认值为0）。
* `max`: 最大长度或大小（默认值为Integer.MAX_VALUE）。
```
  * 示例:
```java
    
    @Size(min = 3, max = 10)
    private String name;
```




* * *

### @Min

* * *

  * **用法** : 用于验证数值型字段的值不小于指定的最小值。

  * 属性:

```java
* `value`: 最小值。
```
  * 示例:
```java
    
    @Min(18)
    private int age;
```




* * *

### @Max

* * *

  * **用法** : 用于验证数值型字段的值不大于指定的最大值。

  * 属性:

```java
* `value`: 最大值。
```
  * 示例:
```java
    
    @Max(100)
    private int score;
```




* * *

### @Null

* * *

  * **用法** : 用于验证字段必须为`null`。

  * 示例:
```java
    
    @Null
    private String middleName;
```




* * *

### @NotNull

* * *

  * **用法** : 用于验证字段不能为`null`。

  * 示例:
```java
    
    @NotNull
    private String firstName;
```




* * *

### @NotEmpty

* * *

  * **用法** : 用于验证字符串、集合、数组等不能为`null`且必须有元素（即非空）。

  * 示例:
```java
    
    @NotEmpty
    private List items;
```




* * *

### @NotBlank

  * **用法** : 用于验证字符串不能为`null`，且去除空白字符后长度必须大于0。

  * 示例:
```java
    
    @NotBlank
    private String username;
```




* * *

### @Pattern

* * *

  * **用法** : 用于验证字符串字段必须符合指定的正则表达式。

  * 属性:

```java
* `regexp`: 正则表达式。
* `flags`: 正则表达式的匹配标志（可选）。
```
  * 示例:
```java
    
    @Pattern(regexp = "^[a-zA-Z0-9]+$")
    private String alphanumeric;
```




* * *

### @DecimalMin

  * **用法** : 用于验证数值型字段的值不小于指定的最小值（支持小数）。

  * 属性

:

```java
* `value`: 最小值。
* `inclusive`: 是否包含最小值，默认为`true`（包含）。
```
  * 示例

:
```java
    
    @DecimalMin(value = "0.1", inclusive = false)
    private double price;
```




* * *

### @DecimalMax

  * **用法** : 用于验证数值型字段的值不大于指定的最大值（支持小数）。

  * 属性:

```java
* `value`: 最大值。
* `inclusive`: 是否包含最大值，默认为`true`（包含）。
```
  * 示例:
```java
    
    @DecimalMax(value = "100.0", inclusive = true)
    private double percentage;
```




* * *

### @Digits

  * **用法** : 用于验证数值型字段的整数位数和小数位数。

  * 属性:

```java
* `integer`: 最大整数位数。
* `fraction`: 最大小数位数。
```
  * 示例:
```java
    
    @Digits(integer = 5, fraction = 2)
    private BigDecimal amount;
```




* * *

### @Email

  * **用法** : 用于验证字符串字段是否符合电子邮件地址的格式。

  * 属性:

```java
* `regexp`: 正则表达式，默认是一个简单的电子邮件格式。
* `flags`: 正则表达式的匹配标志（可选）。
```
  * 示例:
```java
    
    @Email
    private String email;
```




* * *

### @Future

  * **用法** : 用于验证日期或时间字段的值必须在将来。

  * 示例:
```java
    
    @Future
    private LocalDate expirationDate;
```




* * *

## 全局异常解析

* * *

当校验异常时，会抛出 `MethodArgumentNotValidException` 异常，可以对其添加全局的异常解析：
```java


@ExceptionHandler(MethodArgumentNotValidException.class)
public Map&lt;String, String&gt; handleValidationExceptions(
  MethodArgumentNotValidException ex) {
    Map&lt;String, String&gt; errors = new HashMap&lt;&gt;();
    ex.getBindingResult().getAllErrors().forEach((error) -> {
        String fieldName = ((FieldError) error).getField();
        String errorMessage = error.getDefaultMessage();
        errors.put(fieldName, errorMessage);
    });
    return errors;
}
```
