---
title: Nginx技巧
author: XUANWEN DING
categories:
  - - Nginx
abbrlink: aca97dde
date: 2024-03-18 11:18:23
---
文章引言
简单汇总 Nginx 使用中常见操作和机技巧
<!-- more -->

## 替换https证书

```nginx
第一步，进入 nginx 安装目录下，找到conf/cert目录，将新的证书文件，key和pem上传上去。

第二步，grep -r -l "旧证书名"，搜索conf目录下配置了证书的配置文件。然后将里面的名称替换为新的证书名称

第三步，nginx -t，测试配置文件是否正确。nginx -s reload 热重启nginx

```