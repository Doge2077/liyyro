---
title: "LeetCode 第 342 场周赛"
date: 2023-04-26
categories: [Q&amp;A, LeetCode, 最大公约数, 滑动窗口]
description: ""
---

## [2651\. 计算列车到站时间](&lt;https://leetcode.cn/problems/calculate-delayed-arrival-time/&gt;)

* * *

**题目大意** ：

  * 给你一个正整数 `arrivalTime` 表示列车正点到站的时间（单位：小时），另给你一个正整数 `delayedTime` 表示列车延误的小时数。
  * 返回列车实际到站的时间。
  * 注意，该问题中的时间采用 24 小时制。



* * *

**思想** ：

  * 签到题
  * 返回 `(arrivalTime + delayedTime) % 24`



* * *

**代码** ：
    
    
    class Solution {
        public int findDelayedArrivalTime(int arrivalTime, int delayedTime) {
            return (arrivalTime + delayedTime) % 24;
        }
    }

* * *

## [2652\. 倍数求和](&lt;https://leetcode.cn/problems/sum-multiples/&gt;)

* * *

**题目大意** ：

  * 给你一个正整数 n ，请你计算在 [1，n] 范围内能被 3、5、7 整除的所有整数之和。
  * 返回一个整数，用于表示给定范围内所有满足约束条件的数字之和。



* * *

**思想** ：

  * 签到题
  * `i` 从 `1` 遍历到 `n`，将所有满足 `i % k == 0,k = 3, 5, 7` 条件的 `i` 累加即可。



* * *

**代码** ：
    
    
    class Solution {
        public int sumOfMultiples(int n) {
            int sum = 0;
            for(int i = 1; i <= n; i ++){
                if(i % 3 == 0 || i % 5 == 0 || i % 7 == 0) sum += i;
            }
            return sum;
        }
    }

* * *

## [2653\. 滑动子数组的美丽值](&lt;https://leetcode.cn/problems/sliding-subarray-beauty/&gt;)

* * *

**题目大意** ：

  * 给你一个长度为 n 的整数数组 nums ，请你求出每个长度为 k 的子数组的 美丽值 。
  * 一个子数组的 美丽值 定义为：如果子数组中第 x 小整数 是 负数 ，那么美丽值为第 x 小的数，否则美丽值为 0 。
  * 请你返回一个包含 n - k + 1 个整数的数组，依次 表示数组中从第一个下标开始，每个长度为 k 的子数组的 美丽值 。



* * *

**思想** ：

  * 滑动窗口
  * 将所有的数添加偏移量 `base = 50`，以使得所有当前窗口中出现过的数 `i` 可以利用 `vis[i]` 记录其数量；
  * 先将前 `k - 1` 个数加入 `vis[]`；
  * 从 `i = k - 1` 开始，每次循环将 `nums[i]` 统计到 `vis` 中，即 `vis[nums[i] + base] ++`；
  * 由于 `nums[i]` 的范围很小，遍历 `vis[]` 累加窗口中出现的数的数量，保存在 `cnt` 中；
  * 当 `cnt >= x` 时，说明当前遍历到的数即为排序中第 `x` 小的数；
  * 判断减去偏移量 `base` 后将对应美丽值返回。
  * 窗口向后移动，将左边界的 `nums[i - k + 1]` 移出窗口，即 `vis[nums[i - k + 1] + base] --`。



* * *

**代码** ：
    
    
    class Solution {
        public int[] getSubarrayBeauty(int[] nums, int k, int x) {
            int n = nums.length;
            int[] res = new int[n - k + 1];  // 答案数组
            int[] vis = new int[1010];       // 记录窗口中存在数的数量
            final int base = 50;             // 偏移量
            for(int i = 0; i < k - 1; i ++) vis[nums[i] + base] ++;  // 初始化窗口
            for(int i = k - 1; i < n; i ++){
                int cnt = 0;  // 记录数量
                vis[nums[i] + base] ++;          // 移入右边界
                for(int j = 0; j < 110; j ++){
                    cnt += vis[j];   
                    if(cnt >= x){
                        res[i - k + 1] = j - base < 0 ? j - base : 0;
                        break;
                    }
                }
                vis[nums[i - k + 1] + base] --;  // 移出左边界
            }
            return res;  // 返回答案
        }
    }

* * *

## [2654\. 使数组所有元素变成 1 的最少操作次数](&lt;https://leetcode.cn/problems/minimum-number-of-operations-to-make-all-array-elements-equal-to-1/&gt;)

* * *

**题目大意** ：

  * 给你一个下标从 0 开始的 正 整数数组 nums 。你可以对数组执行以下操作 任意 次：
  * 选择一个满足 0 <= i < n - 1 的下标 i ，将 `nums[i]` 或者 `nums[i+1]` 两者之一替换成它们的最大公约数。
  * 请你返回使数组 `nums` 中所有元素都等于 1 的 最少 操作次数。如果无法让数组全部变成 1 ，请你返回 -1 。



* * *

**思想** ：

  * 最大公约数及其性质；
  * 如果一个数列中所有数的最大公约数为 $g$，那么无论如替换数列中任意的两个数为其最大公约数，都无法操作出 $h$ 使得 $h < g$。
  * 证明如下： 
    * 设原数列为 $a_1, a_2, ..., a_n$，最大公约数为 $g$，操作后得到的数列为 $b_1, b_2, ..., b_n$，最大公约数为 $h$，其中 $h < g$。
    * 不妨设 $b_1 = h \times k_1$，其中 $k_1$ 为一个整数。则可以将 $b_1 = \gcd(a_1, a_2) \times (a_1 \div \gcd(a_1, a_2))$。
    * 其中 $a_1 / \gcd(a_1, a_2)$ 是一个整数，故 $h$ 一定整除 $b_1$，即 $h$ 是 $a_1$ 和 $a_2$ 的公约数。
    * 同理，根据操作规则，$a_2$ 和 $a_3$ 的公约数也是 $h$，以此类推，即 $a[i]$ 和 $a[i + 1]$ 的公约数都是 $h$。
    * 由于 $h < g$，所以 $h$ 一定不能整除 $a_1$，即将 $a_1$ 和 $a_2$ 替换为 $h$ 的操作一定不能得到最大公约数为 $h$ 且小于 $g$ 的数列 $b_n$。
  * 若可以通过操作得到： 
    * 当数列存在 $1$ 时，需要操作所有非 $1$ 的元素；
    * 当不存在 $1$ 时，需要找到一个最短的连续的子数组，使得通过操作得到 $1$。 



* * *

**代码** ：
    
    
    class Solution {
        public int minOperations(int[] nums) {
            int n = nums.length;
            int t = nums[0];
            int cnt = t == 1 ? 1 : 0;  // 判断第一个是否为 1
            for(int i = 1; i < n; i ++){
                t = gcd(t, nums[i]);
                if(nums[i] == 1) cnt ++;  // 记录 1 的元素个数
            }
            if(t != 1) return -1;  // t != 1 说明不成立
            if(cnt != 0) return n - cnt;  // 存在 1，最少操作 n - cnt 次
            int res = n;  // 连续的子数组的长度
            for (int i = 0; i < n; i ++) {
                int tt = nums[i];
                for (int j = i + 1; j < n; j ++) {  // 遍历查找
                    tt = gcd(tt, nums[j]);
                    if (tt == 1) {  // 通过操作找到了可以变为 1 的连续子数组
                        res = Math.min(res, j - i + 1);  // 更新最短长度
                        break;
                    }
                }
            }
            return res + n - 2;  // 去除掉连续子数组的两个边界操作
        }
    
        private int gcd(int n, int m){
            return n % m == 0 ? m : gcd(m, n % m);
        }
    
    }
