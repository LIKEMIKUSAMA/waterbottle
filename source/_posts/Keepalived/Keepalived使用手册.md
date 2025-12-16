---
title: Keepalived使用手册
categories:
  - Keepalived
author: 瓶子
tags: Keepalived
abbrlink: '4e75'
date: 2025-12-09 17:47:48
index_img:
banner_img:
---
Keepalived有关的一些使用说明
源码版本：2.3.4
地址：https://gitee.com/LIKEMIKU/keepalived
<!-- more -->
## conf配置文件解析

**该配置文件只能以644权限进行配置**，否则会导致keepalive无法启动
[点击下载keepalived配置](../../file/Keepalived/keepalived.conf)
```shell
# Keepalived监控配置===>》 nginx监控

# 此脚本权限必须为644，否则keepalived无法启动

# 请注意修改 VRRP 中的参数
# 主备节点配置
# state [MASTER|BACKUP]
# 网卡接口配置
# interface <填写网卡名称>
# 本节点IP
# unicast_src_ip
# 备节点IP
# unicast_peer
# VIP地址
# virtual_ipaddress里修改IP，网卡，标签


# 全局配置

global_defs {
    # 本节点名称-集群唯一，配置格式===> <被监控组件名称>_HA_<结点类型>
    # Nginx_HA_Master
    router_id Nginx_HA_Master
    script_user root
    enable_script_security
    

    # 跳过VRRP通告地址检查
    vrrp_skip_check_adv_addr
    # 发送免费ARP报文的间隔
    vrrp_garp_interval 3
    # 发送邻居通告报文的间隔
    vrrp_gna_interval 3
}

# VRRP监控脚本
vrrp_script chk_nginx_status {
    # 执行的脚本路径
    script "/etc/keepalived/tools/check_nginx.sh"
    # 检查间隔（秒）
    interval 3
    # 检查失败时调整优先级的值（可正可负）
    weight -2
    # 失败几次后认为服务不可用
    fall 3
    # 成功几次后认为服务恢复
    rise 1
}

# VRRP实例配置设置
# 备用节点其他参数保持一致，只需修改 state 和 priority 参数即可
vrrp_instance nginx_vrrp_chack {
    # 禁用strict_mode，用来支持认证和单播模式
    strict_mode no
    # 结点状态，可选[MASTER,BACKUP]
    state MASTER
    # 绑定网卡接口
    interface ens18
    # 虚拟路由IP，范围 1-255,同VRRP组内需一致
    virtual_router_id 100
    # 优先级，数值越大优先级越高，MASTER通常比BACKUP更高，约定范围 1-100
    priority 100
    # VRRP通信间隔
    advert_int 1
    # 认证类 Nginx_Vrrp_chack
    authentication {
        # 密码认证：PASS  IPSEC认证：AH
        auth_type PASS
        auth_pass Jhy@Keep
    }

    # VIP地址，该地址会在主备节点浮动，访问该地址等于访问浮动地址后对应的服务器 
    virtual_ipaddress {
        # 格式：IP/掩码 dev 接口 label 标签 （接口和标签可以省略不写）
        # 如 192.168.1.100/24 dev eth0 label eth0:1
        # 如果有VIP地址，则替换为VIP地址和网络接口
        10.8.3.133/24 dev ens18 label ens18:Nginx_HA
    }

    # 使用单播替代多播
    unicast_src_ip 10.8.3.102  # 本节点IP
    unicast_peer {
       10.8.3.205  # 对端IP
    }

    # 监控脚本，与 vrrp_script 定义关联，可添加多个
    track_script {
        chk_nginx_status
    }
    # 四种运行状态变换时触发的命令
    notify_master "/usr/bin/logger -t keepalived 'MASTER state' || echo 'MASTER state' >> /var/log/keepalived/state.log"
    notify_backup "/usr/bin/logger -t keepalived 'BACKUP state' || echo 'BACKUP state' >> /var/log/keepalived/state.log"
    notify_fault "/usr/bin/logger -t keepalived 'FAULT state' || echo 'FAULT state' >> /var/log/keepalived/state.log"
}


```

## 构建可用于docker的纯净镜像
``` shell
# 确保目录结构正确
# ├── Dockerfile
# └── src/ (您的keepalived源码)

# 构建镜像
docker build -t keepalived:2.3.4 .
```
[点击下载Dockerfile](/waterbottle/file/Dockerfile)

```shell
# 构建阶段
FROM ubuntu:22.04 AS builder

# 设置环境变量
ENV DEBIAN_FRONTEND=noninteractive

# 安装编译依赖
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    libnl-3-dev \
    libnl-genl-3-dev \
    libpopt-dev \
    ca-certificates \
    autoconf \
    automake \
    pkg-config \
    git \
    make \
    cmake \
    bison \
    flex && \
    rm -rf /var/lib/apt/lists/*

# 复制本地源码
COPY src /usr/src/keepalived

# 编译安装
WORKDIR /usr/src/keepalived
RUN ./configure --prefix=/usr --sysconfdir=/etc/keepalived --with-init=systemd && \
    make -j$(nproc) && \
    make install

# 最终镜像阶段
FROM ubuntu:22.04

# 设置环境变量
ENV DEBIAN_FRONTEND=noninteractive

# 安装运行时依赖和常用工具
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libssl3 \
    libnl-3-200 \
    libnl-genl-3-200 \
    libpopt0 \
    iproute2 \
    ca-certificates \
    curl \
    wget \
    dnsutils \
    iputils-ping \
    netcat-openbsd \
    telnet \
    tcpdump \
    nmap \
    traceroute \
    mtr-tiny \
    procps \
    htop \
    sysstat \
    iotop \
    iftop \
    lsof \
    net-tools \
    # 文本处理
    less \
    vim-tiny \
    nano \
    # 终端增强
    tmux \
    # 文件工具
    rsync \
    zip \
    unzip \
    # 系统工具
    psmisc \
    util-linux && \
    # 清理缓存和临时文件
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    # 创建必要的目录
    mkdir -p /etc/keepalived

# 从构建阶段复制keepalived主程序
COPY --from=builder /usr/sbin/keepalived /usr/sbin/keepalived

# 暴露VRRP协议端口
EXPOSE 112

# 设置容器启动命令
CMD ["/usr/sbin/keepalived", "--dont-fork", "--log-console", "--vrrp"]
```