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
