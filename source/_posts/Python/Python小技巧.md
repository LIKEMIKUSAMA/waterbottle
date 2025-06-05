---
title: Python小技巧
author: XUANWEN DING
categories:
  - - Python
    - Python小技巧
abbrlink: 76683f9
date: 2023-12-31 11:54:11
---

## 配置国内pip源

```python
# 阿里云源:https://mirrors.aliyun.com/pypi/simple/
# 中科大:https://pypi.mirrors.ustc.edu.cn/simple/
# 清华大学:https://pypi.tuna.tsinghua.edu.cn/simple/

# 命令换源，最后的 URL 直接替换为上面的链接就行
pip config set global.index-url https://pypi.mirrors.ustc.edu.cn/simple
```

