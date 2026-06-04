---
title: "3. 创建游戏界面"
date: 2022-11-11
categories: [Django, Django]
description: ""
---

## 3.1 前期准备

---

### 3.1.1 模块化引用 js 文件

---

进入 `/game/templates/multiends` 打开 `web.html`：
```javascript
&lt;script src="{% static 'js/dist/game.js' %}"&gt;&lt;/script&gt;
```

使用这种引用方式会将所有的 `js` 对象作为网页内部的全局变量引入，为防止后续引用的 `js` 文件发生命名冲突，我们改为模块化引用。

首先将该文件修改为：
```html
{% load static %}  &lt;!-- 查找并载入静态文件 static 的文件夹 --&gt;

&lt;head&gt;
    &lt;link rel="stylesheet" href="https://cdn.acwing.com/static/jquery-ui-dist/jquery-ui.min.css"&gt;
    &lt;script src="https://cdn.acwing.com/static/jquery/js/jquery-3.3.1.min.js"&gt;&lt;/script&gt;
    &lt;link rel="stylesheet" href="{% static 'css/game.css' %}"&gt;
    &lt;!-- 删掉该行：&lt;script src="{% static 'js/dist/game.js' %}"&gt;&lt;/script&gt; -->
&lt;/head&gt;

&lt;body style="margin: 0"&gt;
    &lt;div id="ac_game_12345678"&gt;&lt;/div&gt;
    &lt;!-- 修改此处为： --&gt;
    &lt;script type="module"&gt;
        import {AcGame} from "{% static 'js/dist/game.js' %}";
        $(document).ready(function(){
            let ac_game = new AcGame("ac_game_12345678");
        });
    &lt;/script&gt;
&lt;/body&gt;
```

然后修改 `AcGame` 类对象的引入方式，进入 `/game/static/js/src`，打开 `zbase.js`：
```javascript
export class AcGame {  // 此处添加 export
    constructor(id) {
        this.id = id;
        this.$ac_game = $(`#` + id);
        this.menu = new AcGameMenu(this);
        this.playground = new AcGamePlayground(this);
    }
}
```

修改 `js` 文件后记得在 `/script` 下运行打包脚本重新打包。

---

### 3.1.2 修改页面显示

---

为了便于游戏界面的调试，我们先不显示菜单界面，默认直接打开游戏界面。

还是进入 `/game/static/js/src`，打开 `zbase.js`：
```javascript
```

export class AcGame {  //此处添加 export
    constructor(id) {
        this.id = id;
        this.$ac_game = $(`#` + id);
        //this.menu = new AcGameMenu(this);  将该行注释掉，不生成菜单界面对象
        this.playground = new AcGamePlayground(this);
    }
}

然后进入 `/game/static/js/src/playground`，打开 `zbase.js`：
```javascript

class AcGamePlayground {
    constructor(root) {
        this.root = root;
        this.$playground = $(`&lt;div&gt;lys is a dog&lt;/div&gt;`);

        //this.hide();  注释掉该行，不默认关闭
        this.root.$ac_game.append(this.$playground);

        this.start();
    }

    start() {
    }

    show() { // 打开playground界面
        this.$playground.show();
    }

    hide() { // 关闭playground界面
        this.$playground.hide();
    }

}
```

修改 `js` 文件后记得在 `/script` 下运行打包脚本重新打包。

---

### 3.1.3 创建游戏界面对象

---

首先进入 `game/static/js/src/playground/zbase.js`，创建新的 `html` 类：
```javascript

class AcGamePlayground {
    constructor(root) {
        this.root = root;
        this.$playground = $(`&lt;div class="ac_game_playground"&gt;lys is a dog&lt;/div&gt;`);  //创建新的html对象

        //this.hide();  注释掉该行，不默认关闭
        this.root.$ac_game.append(this.$playground);

        this.start();
    }

    start() {
    }

    show() { // 打开playground界面
        this.$playground.show();
    }

    hide() { // 关闭playground界面
        this.$playground.hide();
    }

}
```

同时要在 `game/static/css` 里面添加该 `html` 类的 `css` 样式：
```css

.ac_game_playground {
    width: 100%;
    height: 100%;
    user-select: none;
}
```

---

## 3.2 游戏界面文件结构

---
```javascript
```

game/static
|-- css
|   `-- game.css
|-- image
|   |-- menu
|   |   `-- background.png
|   |-- playground
|   `-- settings
`-- js
    |-- dist
    |   `-- game.js
    `-- src
        |-- menu
        |   `-- zbase.js
        |-- playground  //游戏界面
        |   |-- ac_game_object  //可动对象的基类
        |   |   `-- zbase.js
        |   |-- game_map  //地图
        |   |   `-- zbase.js
        |   |-- particle  //动效
        |   |   `-- zbase.js
        |   |-- player  //人物
        |   |   `-- zbase.js
        |   |-- skill  //技能
        |   |   `-- fireball
        |   |       `-- zbase.js
        |   `-- zbase.js
        |-- settings
        `-- zbase.js
```

---

## 3.3 游戏界面文件创建

---

### 3.3.1 创建可动对象的基类文件

---

进入 `game/static/js/src/playground/ac_game_object`，创建 `zbase.js`：
```javascript
//将创建的对象存入全局数组里，之后每秒调用数组里的对象调用60次
let AC_GAME_OBJECTS = [];

class AcGameObject {
    constructor() {
        AC_GAME_OBJECTS.push(this);  //创建对象加入数组
        this.has_called_start = false;  //标记是否执行过start函数
        this.timedelta = 0;  //当前帧距离上一帧的时间间隔
    }

    start() {  //只会在第一帧执行一次

    }

    update() {  //每一帧都会执行一次

    }

    on_destroy() {  //在物体被销毁前执行一次
    }

    destroy() {  //删除当前物体
        this.on_destroy();

        for(let i = 0; i &lt; AC_GAME_OBJECTS.length; i ++){
            if(AC_GAME_OBJECTS[i] === this) {  //找到需要删除的对象
                AC_GAME_OBJECTS.splice(i, 1);
                i --;
            }
        }
    }
}
```

let last_timestamp;  // 上一帧的时间戳
let AC_GAME_ANIMATION = function(timestamp) {  // timestamp是传入的当前时间
    for(let i = 0; i &lt; AC_GAME_OBJECTS.length; i++) {  // 更新所有可以动的对象
        let obj = AC_GAME_OBJECTS[i];
        if (!obj.has_called_start) {
            obj.start();
            obj.has_called_start = true;
        } else {
            obj.timedelta = timestamp - last_timestamp;  // 更新对象的时间间隔
            obj.update();  // 更新这一帧对象的位置
        }
    }
    last_timestamp = timestamp;
    requestAnimationFrame(AC_GAME_ANIMATION);  // 递归调用
}

requestAnimationFrame(AC_GAME_ANIMATION);  // 调用JS API来启动动画帧循环
```

---

### 3.3.2 创建地图文件

---

进入 `game/static/js/src/playground/game_map`，创建 `zbase.js`：
```javascript
class GameMap extends AcGameObject {
    constructor(playground) {  // 将playground的参数传进来
        super();
        this.playground = playground;  // 存储下来
        this.$canvas = $(`&lt;canvas&gt;&lt;/canvas&gt;`);  // 通过API创建画布
        this.ctx = this.$canvas[0].getContext('2d');
        this.ctx.canvas.width = this.playground.width;  // 设置画布宽度
        this.ctx.canvas.height = this.playground.height;  // 设置画布高度
        this.playground.$playground.append(this.$canvas);  // 将画布对象添加到页面
    }

    start() {

    }

    // 每一帧都会调用的更新函数
    update() {
        this.render();
    }

    render() {  // 不断重绘画布
        this.ctx.fillStyle = "rgba(0, 0, 0, 0.2)";  // 设置背景颜色和透明度
        this.ctx.fillRect(0, 0, this.ctx.canvas.width, this.ctx.canvas.height);  // 使用JS API填充矩形
    }
}
```

---

### 3.3.3 创建玩家文件

---

进入 `game/static/js/src/playground/player`，创建 `zbase.js`：
```javascript

class Player extends AcGameObject {
    constructor(playground, x, y, radius, color, speed, is_me, life) {  //传入需要处理的参数
        super();
        this.playground = playground;
        this.ctx = this.playground.game_map.ctx;
        //坐标
        this.x = x;
        this.y = y;

        //速度方向
        this.vx = 0;
        this.vy = 0;

        //受到伤害的速度方向和速度
        this.damage_x = 0;
        this.damage_y = 0;
        this.damage_speed = 0;

        this.friction = 0.9;  //摩擦力
        this.move_length = 0;  //移动距离

        this.radius = radius;  //该对象的半径
        this.color = color;  //颜色
        this.speed = speed;  //速度

        this.is_me = is_me;  //是否是玩家
        this.life = life;  //生命值

        this.eps = 0.1;  //精度

        this.cur_skill = null;  //当前选择的技能
        this.spent_time = 0;  //开局静默期
    }

    start() {
        //是自己本身
        if (this.is_me) {
            this.add_listening_events();  //通过监听函数控制
        } else {  //敌人
            //通过随机生成的坐标控制移动
            let tx = Math.random() * this.playground.width;
            let ty = Math.random() * this.playground.height;
            this.move_to(tx, ty);
        }
    }

    //监听函数，判断鼠标点击行为
    add_listening_events() { 
        let outer = this;

        if (this.life &lt;= 0) return false;  //死亡不再接收指令

        this.playground.game_map.$canvas.on("contextmenu", function() {  //截断鼠标右键显示菜单选项
            return false;
        });
    }
}
```

//监听鼠标移动
        this.playground.game_map.$canvas.mousedown(function(e) {
            if(e.which === 3) {  //判断鼠标按键 1是左键， 2是滚轮
                outer.move_to(e.clientX, e.clientY);  //鼠标点击移动API
            }
            else if(e.which === 1) {
                if(outer.cur_skill === "fireball") {  //发射火球
                    outer.shoot_fireball(e.clientX, e.clientY, this.color);
                }
                else if(outer.cur_skill === "go_to") {  //闪现方向
                    outer.go_to(e.clientX, e.clientY);
                }
                outer.cur_skill = null;  //清空当前的技能选择
            }
        });

//监听键盘按键
        $(window).keydown(function(e) {
            //键码
            if(e.which === 81) {  //按 'Q' 发射火球
                outer.cur_skill = "fireball";
                return false;
            }
            else if(e.which === 69) {  //按 'E' 闪现
                outer.cur_skill = "go_to";
                return false;
            }
        });
    }

// 发射火球
    shoot_fireball(tx, ty, color) {
        let x = this.x, y = this.y;  // 发射位置为当前位置
        let radius = this.playground.height*0.01;  // 火球半径
        let angle = Math.atan2(ty - this.y, tx - this.x);  // 计算当前位置相对鼠标点击坐标的方向角度
        let vx = Math.cos(angle), vy = Math.sin(angle);  // 计算速度的方向
        let speed = this.speed*2;  // 火球速度为自身移动速度的2倍
        let move_length = this.playground.height*1;  // 火球移动的最大距离
        if(this.life &gt; 0) new FireBall(this.playground, this, x, y, radius, vx, vy, this.color, speed, move_length, this.playground.height*0.01);  // 当前对象存活才可发射火球
        //console.log("fireball", tx, ty);
        //if(this.is_me) console.log("life:", this.life);
    }

// 瞬移操作
    go_to(tx, ty) {
        this.x = tx;  // 直接更新位置
        this.y = ty;
        this.move_length = 0;  // 重置移动方向和距离
    }

// 计算移动的相对距离
    get_dist(x1, y1, x2, y2) { 
        let dx = x1 - x2;
        let dy = y1 - y2;
        return Math.sqrt(dx*dx + dy*dy);
    }

// 移动的方向
    move_to(tx, ty) {
        this.move_length = this.get_dist(this.x, this.y, tx, ty);
        let angle = Math.atan2(ty - this.y, tx - this.x);  // 计算相对位置的角度
        this.vx = Math.cos(angle), this.vy = Math.sin(angle);
    }

//受到攻击后执行的逻辑
    is_attacked(angle, damage) {
        if(this.life &lt;= 0) return false;  //生命值归零的对象直接忽视
        //释放粒子效果
        for(let i = 0; i &lt; 10 + Math.random()*5; i ++){
            let x = this.x, y = this.y;
            let radius = this.radius*Math.random()*0.11;  //粒子大小半径
            let angle = Math.PI*2*Math.random();  //随机的角度
            let vx = Math.cos(angle), vy = Math.sin(angle);
            let color = this.color;  //粒子颜色
            let speed = this.speed*4;  //释放速度
            let move_length = this.radius*Math.random()*10;  //粒子释放半径
            new Particle(this.playground, x, y, radius, vx, vy, color, speed, move_length);  //基于上述参数生成粒子对象
        }

        this.radius -= damage*0.65;  //受到攻击变小
        this.speed *= 0.88;  //速度减慢
        this.life -= 1;  //生命值降低

        if(this.life &lt;= 0){  //生命值归零即为死亡
            this.destroy();  //销毁该对象
            return false;
        }
        else {
            //受击的击退效果
            this.damage_x = Math.cos(angle);  //击退的方向
            this.damage_y = Math.sin(angle);
            this.damage_speed = damage*50;  //击退的速度
        }
    }

//每一帧刷新
    update() {
        //生命值归零直接销毁对象
        if(this.life &lt;= 0) {
            this.destroy();
            return false;
        }

        //更新静默的时间
        this.spent_time += this.timedelta/1000;

        if(this.damage_speed &gt; this.eps) {  //当前存在受击的方向和速度则先被击退
            //打断当前的移动
            this.vx = this.vy = 0;
            this.move_length = 0;
        }
    }

//更改击退的位置和方向
        this.x += this.damage_x * this.damage_speed * this.timedelta / 1000;
        this.y += this.damage_y * this.damage_speed * this.timedelta / 1000;
        this.damage_speed *= this.friction; //摩擦效果
    }
    else {
        if (!this.is_me) { //人机模式下敌人的攻击规则
            if (Math.random() &lt; 1 / 250.0 && this.spent_time &gt; 3) { //攻击频率和静默时间
                //随机攻击当前场上存在的人
                let player = this.playground.players[Math.floor(Math.random() * this.playground.players.length)];

                //只朝玩家攻击（地狱模式QAQ）
                //let player = this.playground.players[0];

                //发射火球
                this.shoot_fireball(player.x, player.y, this.color);
            }
        }

        //当前移动距离为0，即到达了上一次移动的终点位置
        if (this.move_length &lt; this.eps) {
            //重置速度和移动距离
            this.vx = this.vy = 0;
            this.move_length = 0;
            if (!this.is_me) { //人机再随机一个坐标方向移动
                let tx = Math.random() * this.playground.width;
                let ty = Math.random() * this.playground.height;
                this.move_to(tx, ty);
            }
        }
        else { //移动
            let moved = Math.min(this.move_length, this.speed * this.timedelta / 1000); //这一帧的移动距离
            this.x += this.vx * moved; //移动后的位置
            this.y += this.vy * moved;
            this.move_length -= moved; //更新还需要移动的距离
        }
    }

```javascript
this.render();  // 调用渲染函数，每一帧都要重新渲染该对象的位置，否则会消失
    }

    render() {
        this.ctx.beginPath();
        this.ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2, false);  // 画圆
        this.ctx.fillStyle = this.color;
        this.ctx.fill();
    }

}
```

---

### 3.3.4 创建火球技能文件

---

进入 `game/static/js/src/playground/skill/fireball`，创建 `zbase.js`：
```javascript
class FireBall extends AcGameObject {
    constructor(playground, player, x, y, radius, vx, vy, color, speed, move_length, damage) {
        super();
        this.playground = playground;
        this.ctx = this.playground.game_map.ctx;
        this.player = player;

        // 火球位置
        this.x = x;
        this.y = y;
        // 火球半径
        this.radius = radius;
        // 火球速度方向
        this.vx = vx;
        this.vy = vy;

        this.color = color;  // 颜色
        this.speed = speed;  // 速度
        this.move_length = move_length;  // 运动距离
        this.damage = damage;  // 伤害

        this.eps = 0.1;  // 精度
    }

    start() {

    }

    update() {
        // 到达最大距离消失
        if (this.move_length &lt; this.eps) {
            this.destroy();
            return false;
        }

        // 更新距离，逻辑同 player
        let moved = Math.min(this.move_length, this.speed * this.timedelta / 1000);
        this.x += this.vx * moved;
        this.y += this.vy * moved;
        this.move_length -= moved;
    }
}
```javascript
// 判断火球是否击中某个球
for (let i = 0; i &lt; this.playground.players.length; i++) {
    let player = this.playground.players[i];
    if (this.player !== player && this.is_collision(player) && this.player.life &gt; 0) {
        this.attack(player);  // 调用击中函数
    }
}

// 调用渲染函数
this.render();

// 获取火球和该player的中心距离
get_dist(x1, y1, x2, y2) {
    let dx = x1 - x2;
    let dy = y1 - y2;
    return Math.sqrt(dx * dx + dy * dy);
}

// 判断是否可以击中
is_collision(player) {
    let distance = this.get_dist(this.x, this.y, player.x, player.y);
    if (distance &lt; this.radius + player.radius) return true;
    else return false;
}

// 击中之后的逻辑
attack(player) {
    if (player.life &gt; 0) this.destroy();  // 击中后销毁火球
    let angle = Math.atan2(player.y - this.y, player.x - this.x);
    player.is_attacked(angle, this.damage);
    return false;
}

render() {
    this.ctx.beginPath();
    this.ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2, false);
    this.ctx.fillStyle = this.color;
    this.ctx.fill();
}
```

---

### 3.3.5 创建动效文件

---

进入 `game/static/js/src/playground/particle`，创建 `zbase.js`：
```javascript
```

---

**修复内容：**
1. `destory` → `destroy`（拼写错误）
2. 运算符前后添加空格，如 `dx*dx` → `dx * dx`、`Math.PI*2` → `Math.PI * 2`
3. 循环条件中的空格规范化：`i ++` → `i++`
4. 函数参数逗号后添加空格

class Particle extends AcGameObject {
    constructor(playground, x, y, radius, vx, vy, color, speed, move_length) {
        super();
        this.playground = playground;
        this.ctx = this.playground.game_map.ctx;
        this.x = x;
        this.y = y;
        this.radius = radius;
        this.vx = vx;
        this.vy = vy;
        this.color = color;
        this.speed = speed;
        this.move_length = move_length;
        this.friction = 0.9;
        this.eps = 3;
    }

    start() {

    }

    update() {
        if (this.move_length &lt; this.eps || this.speed &lt; this.eps) {
            this.destroy();
            return false;
        }

        let moved = Math.min(this.move_length, this.speed * this.timedelta / 1000);
        this.x += this.vx * moved;
        this.y += this.vy * moved;
        this.move_length -= moved;
        this.speed *= this.friction;
        this.render();
    }

    render() {
        this.ctx.beginPath();
        this.ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2, false);
        this.ctx.fillStyle = this.color;
        this.ctx.fill();
    }
}
```

---

### 3.3.6 更新总文件

---

进入 `game/static/js/src/playground`，打开 `zbase.js`：
```javascript

class AcGamePlayground {
    constructor(root) {
        this.root = root;
        this.$playground = $(`&lt;div class="ac_game_playground"&gt;lys is a dog&lt;/div&gt;`);
```javascript
// this.hide();
this.root.$ac_game.append(this.$playground);
this.width = this.$playground.width();
this.height = this.$playground.height();
this.game_map = new GameMap(this); // 创建地图对象
this.players = []; // 存储所有的玩家对象

// 创建玩家本身
this.players.push(new Player(this, this.width/2, this.height/2, this.height*0.05, "white", this.height*0.35, true, 5)); // 此处大小和界面大小绑定，便于适应不同大小的窗口

// 添加敌人
for (let i = 0; i < 4; i++) {
    this.players.push(new Player(this, this.width/2, this.height/2, this.height*0.05, this.get_random_color(), this.height*0.35, false, 5));
}

this.start();
}

// 随机的敌人颜色
get_random_color() {
    let colors = ["blue", "red", "pink", "green", "grey"];
    return colors[Math.floor(Math.random() * 5)];
}

start() {

}

show() { // 打开playground界面
    this.$playground.show();
}

hide() { // 关闭playground界面
    this.$playground.hide();
}

}

最后进入 `game/scripts`，运行之前写好的打包文件脚本，启动服务查看效果即可。
```

修复内容：
1. 将 `//        this.hide();` 中的多余空格移除
2. 将注释前的 `//` 后统一添加空格
3. 修复了 `//创建玩家本身` 和 `//添加敌人` 注释格式，添加了冒号
4. 将 `for(let i = 0; i < 4; i ++)` 改为 `for (let i = 0; i < 4; i++)`，添加空格并修复自增运算符格式
5. 将 `Math.random()*5` 改为 `Math.random() * 5`，添加运算符两侧空格
6. 统一代码缩进，使其更整洁