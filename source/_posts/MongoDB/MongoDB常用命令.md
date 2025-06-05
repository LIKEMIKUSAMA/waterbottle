---
title: MongoDB常用命令
author: XUANWEN DING
categories:
  - - MongoDB
    - 常用命令
abbrlink: c08448a5
date: 2024-04-03 16:54:50
---
MongoDB常用命令和操作方案

<!-- more -->

## 重启和启动

```bash
# 关闭命令
cd "path to"/mongodb/bin/
./mongod --dbpath=**** --shutdown

# 启动命令
cd "path to"/mongodb/bin/
./mongod -f mongodb.conf
```

## 运行内存使用限制

```bash
vi mongodb.conf
# 添加然后重启生效
wiredTigerCacheSizeGB=2

```