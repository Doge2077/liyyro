---
title: "双 Token 三验证解决方案"
date: 2024-08-01
categories: [Software Architect]
description: ""
---

## 问题分析

* * *

以往的项目大部分解决方案为单 token：

  * 用户登录后，服务端颁发 jwt 令牌作为 token 返回
  * 每次请求，前端携带 token 访问，服务端解析 token 进行校验和鉴权



存在的问题：

  * 有效期设置问题：有效期设置需要对时间做平衡，不能太短也不能太长
  * 续期问题：一旦过期，用户必须重新登录，很难做无感刷新
  * 无状态问题：token 是无状态的，单 token 颁发后服务端无法主动使其失效



* * *

## 原理解析

* * *

这里引入双 token 机制：

  * accessToken：时间较短，一般为 5 分钟或者更短
  * refreshToken：时间较长，一般为 1 到 3 天



登录过程：

  * 用户携带用户名和密码登录
  * 服务端为其颁发 accessToken 和 refreshToken



三验证环节：

  * 一验证：前端请求携带 accessToken，验证是否过期，不过期放行，过期则进入第二个验证环节
  * 二验证：前端请求携带 refreshToken，验证是否过期，不过期进入第三个验证环节，过期则要求用户重新登录
  * 三验证：在 redis 种验证 refreshToken 是否存在，存在则颁发新的 accessToken 和 refreshToken 返回前端更新，将原来的 refreshToken 删除，再把新的 refreshToken 存入 redis



该机制的 UML 图如下：

![](https://cdn.jsdelivr.net/gh/Doge2077/liyyro-photo@main/images/2024/08/双token三验证.png)

* * *

## 最佳实践

* * *

### 生成 Token

* * *

基于 SpringCache 来操作 redis，利用 MD5 算法对 token 进行加密，防止其作为键的后缀存入时过长，导致”大KEY“的问题出现
    
    
    public class CommonRedisConstants {
        public static class RedisKey {
            /**
             * refreshToken 前缀
             */
            public static final String REFRESH_TOKEN_PREFIX = "REFRESH_TOKEN_PREFIX_%s";
        }
    }
    
    
    @Resource
    private StringRedisTemplate stringRedisTemplate;
    
    // 生成 accessToken
    private String createAccessToken(Map&lt;String, Object&gt; claims) {
        // 这里是利用 jjwt 编写的工具类方法，读者可以自行实现相关工具类
        return JwtUtils.generateAccessToken(claims);
    }
    
    // 生成 refreshToken 并存入 redis
    private String createRefreshToken(Map&lt;String, Object&gt; claims) {
        String refreshToken = JwtUtils.generateRefreshToken(claims);
        // redisKey 的形式为固定前缀+md5转换的token
        String redisKey = String.format(CommonRedisConstants.RedisKey.REFRESH_TOKEN_PREFIX, MD5Util.generateMd5Str(refreshToken));
        // 设置有效期为 3 days
        this.stringRedisTemplate.opsForValue().set(redisKey, refreshToken, Duration.ofDays(3L));
        return refreshToken;
    }

* * *

### 校验 Token

* * *

基于自定义注解和 Spring AOP 实现校验 token，并将解析后的信息存储到上下文

自定义的注解：
    
    
    @Target(ElementType.METHOD)
    @Retention(RetentionPolicy.RUNTIME)
    @Documented
    public @interface CurrentUser {
    }

AOP 切面：
    
    
    @Aspect
    @Component
    @Slf4j
    public class CurrentUserAspect {
    
        private final HttpServletRequest request;
    
        public CurrentUserAspect(HttpServletRequest request) {
            this.request = request;
        }
    
        @Before("@annotation(currentUser)")
        public void setUserContext(CurrentUser currentUser) {
            String token = request.getHeader("Authorization");
            if (token != null) {
                try {
                    // 这里是利用 jjwt 编写的工具类方法，读者可以自行实现相关工具类
                    Claims claims = JwtUtils.parseToken(token);
                    // 这里是利用 ThreadLocal 存储用户信息到上下文，读者可以自行实现相关工具类
                    UserContextUtil.set(claims);
                } catch (Exception e) {
                    // token 解析失败后的逻辑
                }
            } else {
                // 请求头未携带 token 的逻辑
            }
        }
    
        // 方法执行完后释放资源，防止内存泄漏
        @After("@annotation(currentUser)")
        public void clearUserContext(CurrentUser currentUser) {
            UserContextUtil.clear();
        }
    
    }

* * *

### 刷新 Token

* * *

前端调用刷新 token 后，服务端返回新的 accessToken 和 refreshToken：
    
    
    @Data
    @AllArgsConstructor
    public class AdminLoginVO {
        private String accessToken;
        private String refreshToken;
    }
    
    
    public AdminLoginVO refreshLogin(String refreshToken) {
            // 校验 token 是否有效
            boolean isValidated = JwtUtils.validateToken(refreshToken);
            if (!isValidated) {
                // token 
            }
    
            /**
             * 校验 redis 里的 refreshToken 是否失效
             * 未失效：将 redis 里的 refreshToken 删除，重新颁发新的 accessToken 和 refreshToken
             * 已失效：重新登录
             */
            String redisKey = String.format(CommonRedisConstants.RedisKey.REFRESH_TOKEN_PREFIX, MD5Util.generateMd5Str(JwtUtils.preDecodeToken(refreshToken)));
            Boolean hasKey = this.stringRedisTemplate.hasKey(redisKey);
            if (ObjectUtil.notEqual(hasKey, Boolean.TRUE)) {
                // 原 token 过期或已经使用过的逻辑
            }
            // 删除原 token
            this.stringRedisTemplate.delete(redisKey);
            // 颁发新的 accessToken 和 refreshToken
            Claims claims = JwtUtils.parseToken(refreshToken);
            String accessToken = createAccessToken(claims);
            refreshToken = createRefreshToken(claims);
            return new AdminLoginVO(accessToken, refreshToken);
        }
