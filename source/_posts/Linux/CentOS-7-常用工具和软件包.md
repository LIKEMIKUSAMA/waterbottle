---
title: CentOS 7 常用工具和软件包
author: XUANWEN DING
categories:
  - [Linux,常用工具和软件包]
date: 2024-01-03 15:19:04
---
CentOS 系统常用于作为服务器，因此多数情况下都需要使用 SSH 方式连接，本文主要介绍常用的 SSH 连接服务器的工具和服务器内一些好用的软件包。

<!-- more -->

## 一、常用工具

### 1.1、WindTerm

一款完全开源，免费，轻量级的工具
优点：
1、支持本地 CMD 和 PowerShell 命令使用。
2、可以远程 SSH 连接服务器进行操作。
3、内置了文件上传下载功能。
4、够轻量化，启动速度够快。
5、命令操作提示和补全

缺点：截至2.5版本
1、文件上传下载需要服务器上装有 rzsz 组件包。（勉强算一个缺点吧。）
2、出现部分服务器密码循环校验错误的情况，使用其他 SSH 登录器可以正常登录。(解决办法是 SSH 密码校验中，关闭除密码外的所有选项)
3、无法直接从 XShell 中导入已有连接


[下载地址](https://github.com/kingToolbox/WindTerm/releases)

作者有自己的博客用来介绍软件详细情况，具体可以看这个[传送门](https://kingtoolbox.github.io/)


## 二、常用软件包

### 2.1、上传下载

```bash
# CentOS 系统里，不依赖第三方软件的话，上传下载主要使用 rz 和 sz 命令
# 但是命令需要额外安装。
# 安装完成后可以使用help命令查看具体用法
yum -y install lrzsz

```