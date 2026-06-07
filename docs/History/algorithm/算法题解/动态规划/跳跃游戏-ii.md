---
title: "跳跃游戏 II"
date: 2023-04-29
categories: [Q&A, 贪心]
description: ""
---

# 跳跃游戏-ii


[Original link](https://leetcode.cn/problems/jump-game-ii/)

**思想**：

* 贪心；
  * 对于当前所处的位置 `i`，当 `i + nums[i] >= n - 1` 时可以直接返回结果；
  * 否则，从 `j = i + 1` 遍历到 `j = i + nums[i]`，设下一步的位置为 `res`，以 `res` 能到达的最远位置为 `idx`；
  * 显然， `j + nums[j]` 即为下一步可以到达的最远位置 `idx`；
  * 则只需找到 `j + nums[j]` 的最大值，并用 `res` 维护下一步的坐标 `j` 即可。

**代码**：

```java
class Solution {
    public int jump(int[] nums) {
        int ans = 0, n = nums.length;
        if (n <= 1) return 0;  // 当长度只有 1 时无需操作
        for (int i = 0; i < n; i++) {
            int res = 0, idx = 0;
            if (i + nums[i] >= n - 1) return ans + 1;  // 下一步的最远距离正好到达终点
            for (int j = i + 1; j <= i + nums[i]; j++) {  // 遍历找到能到达最远距离的方案
                if (j + nums[j] >= idx) {
                    idx = j + nums[j];
                    res = j;
                }
            }
            i = res - 1; ans++;  // 更新 i 和 ans
        }
        return ans;
    }
}
```

