---
title: Docker操作命令与技巧
categories:
  - Docker
author: 瓶子
abbrlink: 6e0f
date: 2025-12-02 11:08:45
tags: Docker
index_img:
banner_img:
---
Docker的操作命令和配置技巧

<!-- more -->

## 修改docker仓库目录
1、毫秒镜像：https://docker.1ms.run               # 仅有部分常见镜像
2、daocloud：https://docker.m.daocloud.io        # 较慢
放于：`/etc/docker/daemon.json`
修改该文件后，需要操作重载配置并重启docker
```shell
systemctl daemon-reload
systemctl restart docker
# 部分服务器可能没有systemctl，需要使用service
service docker restart
```
```json
{
  "registry-mirrors": [
    "https://docker.1ms.run"
  ],

  "dns": ["223.5.5.5", "114.114.114.114"],

  "dns-search": ["local"]
}
```


## docker.service文件解析

```shell
# 在文件中添加以下内容（根据实际需要调整）：
[Unit]
# 描述
Description=Docker Application Container Engine
# 官方文档地址
Documentation=https://docs.docker.com
# 启动顺序，Docker将在network，firewall，containerd服务启动后启动。
After=network-online.target firewalld.service containerd.service
# 启动依赖，但不是严格依赖，如果network未启动，不影响docker
Wants=network-online.target

# 服务部分
[Service]
# 通知，服务启动后通知systemd
Type=notify
# 指定启动docker进程的文件路径，压缩包安装必须把文件放入该路径
ExecStart=/usr/local/bin/dockerd
# 重新加载配置时，发送HUP信号
ExecReload=/bin/kill -s HUP
# 启动超时时间，0为无限制 
TimeoutStartSec=0
# 启动失败后等待2秒重启
RestartSec=2
# 无论退出状态是什么，总是重启服务
Restart=always
# 资源限制
# LimitNPROC：无进程数限制
# LimitCORE：无核心转储文件大小限制
# TasksMax：无任务（线程）数量限制
LimitNPROC=infinity
LimitCORE=infinity
TasksMax=infinity
# 将cgroups管理托管给服务
Delegate=yes
# 停止服务时只终止主进程，而不是整个进程组
KillMode=process
# 降低被OOM清理终止的优先级，负数表示更受保护
OOMScoreAdjust=-500

# 安装部分
[Install]
# 指定该服务在多用户模式下启动
WantedBy=multi-user.target
```

## 容器操作
```shell
# 列出所有容器，不带a只列出运行中的容器
docker ps -a
# 删除一个容器
docker rm <容器名称>
# 删除所有未使用的镜像和容器
docker system prune
# 删除所有未使用的容器
docker container prune


# 下面是高危操作，谨慎使用
# 停止所有容器
docker stop $(docker ps -a -q)
# 删除所有容器
docker rm $(docker ps -a -q)
```

## 镜像操作
```shell
# 列出所有镜像
docker images
# 下载镜像到本地
# docker pull mysql:5.7 添加--verbose 参数可以看到拉取的详细过程
docker pull <镜像名称>:<版本号>
# 加载镜像文件到docker
docker load -i <镜像文件>
# 从本地镜像导出docker可识别的tar包
# docker save -o mysql-5.7.tar mysql:5.7
docker save -o <文件名>.tar <镜像名称>:<指定版本>

# 下面是高危操作，谨慎使用
# 删除镜像
docker rmi <镜像ID>
# 删除所有未使用的镜像
docker image prune
```

## 运行容器