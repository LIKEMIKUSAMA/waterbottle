---
title: Mysql8.0启用组复制（集群）的配置过程
tags:
  - Mysql
  - 数据库集群
categories:
  - - Mysql
    - 集群
author: 瓶子
abbrlink: 34a8
date: 2026-04-07 15:06:53
index_img:
banner_img:
---
Mysql8.0启用组复制（集群）的配置过程和踩过的坑，基于Mysql8.0.45和docker容器化配置模式，参考节点为三节点冗余服务器，mysql-route负责统一管理数据库入口

<!-- more -->

## 初始化注意事项
新的数据库要开启集群，需要先初始化默认的mysql数据库，然后在my.cnf文件中添加集群相关的配置参数，参考配置文件如下
新数据库初始化需要删除集群配置里的内容，等初始化结束后再写入my.cnf，否则数据库会初始化失败！
### my.cnf文件
```editorconfig
[client]
default-character-set=utf8mb4

[mysql]
default-character-set=utf8mb4

[mysqld]
# 基础字符集配置
init_connect="SET collation_connection = utf8mb4_unicode_ci"
init_connect="SET NAMES utf8mb4"
character-set-server=utf8mb4
collation-server=utf8mb4_unicode_ci
lower_case_table_names=1
# 通用日志（按需保留）
general_log=ON
general_log_file=/var/log/mysql/mysql_general.log

# binlog
log_bin=/var/log/mysql/mysql-binlog
# 日志完整性校验
binlog_checksum=CRC32
# 轮转大小500M
max_binlog_size=524288000
# 保留天数30，单位秒
binlog_expire_logs_seconds=2592000

bind-address=0.0.0.0

# ---------------------------
# 以下为 Group Replication 集群必备配置
# ---------------------------

# 启动时自动加入组（设置为 OFF，手动控制，待集群稳定后再改回ON，或手动启动后执行START GROUP_REPLICATION;）
plugin-load-add=group_replication.so
group_replication_start_on_boot=OFF

# Group Replication 通信地址（用于节点间内部通信）
# 格式：宿主机IP:组内通信端口（映射到容器的该端口）
group_replication_local_address="10.8.3.130:13306"
group_replication_group_seeds="10.8.3.130:13306,10.8.3.131:13306,10.8.1.10:13306"

# 节点在集群中的标识（用于 MySQL 客户端连接）
# 因为容器使用桥接网络，需设置 report_host 为宿主机 IP
report_host=10.8.3.130
report_port=3306

# 服务器 ID，集群内唯一
server_id=1

# 启动时自动引导组（仅用于初始化第一个节点，保持OFF即可）
group_replication_bootstrap_group=OFF

# 组复制模式（单主模式）
group_replication_single_primary_mode=ON

# 组名称（UUID，可任意生成，集群内一致）
group_replication_group_name="1c2ad992-3242-11f1-a2e0-0242ac120002"

# 开启 GTID
gtid_mode=ON
enforce_gtid_consistency=ON

# 复制元数据存储方式
master_info_repository=TABLE
relay_log_info_repository=TABLE

# 是否将主库传入变更写入从库binlog
log_replica_updates=ON

# 写集合提取方式（Group Replication 需要）
transaction_write_set_extraction=XXHASH64

# 禁用多主更新中严格的一致性检查，单主模式必须全体禁用
group_replication_enforce_update_everywhere_checks=OFF
```
### 环境变量
Mysql还有部分环境变量可供快速初始化，可参考如下
```dotenv
# 新建一个指定密码允许从其他服务器远程登录的root账号
MYSQL_ROOT_PASSWORD=
MYSQL_ROOT_HOST=%
# 新建一个指定用户和密码的账户，但是没有权限。
MYSQL_USER=
MYSQL_PASSWORD=
```


## docker容器化部署

### compose文件
```yaml
version: '3'
services:
  mysql: # 服务名称
    image: mysql:8.0.45 
    container_name: mysql8.0 # 容器名称
    env_file:
      - ../system.env
    
    volumes:
      - ./log:/var/log/mysql # 映射日志目录，宿主机:容器
      - ./data:/var/lib/mysql # 映射数据目录，宿主机:容器
      - ./conf:/etc/mysql/conf.d # 映射配置目录，宿主机:容器
      - /etc/localtime:/etc/localtime:ro # 让容器的时钟与宿主机时钟同步，避免时间的问题，ro是read only的意思，就是只读。
      - ./run:/var/run/mysqld
    
    network_mode: host
    ports:
      - 3306:3306 # 指定宿主机端口与容器端口映射关系，宿主机:容器
      - 13306:13306 # 集群端口
    restart: always # 容器随docker启动自启
```




## 坑点合集
1.所有数据库的配置须保持一致，如出现不一致的配置会导致集群配置冲突然后全体掉线。
2.不同的硬件架构下的系统，即使使用同一版本的数据库，也无法搭建集群。集群所有节点必须处于同一建构下，如全为`arm`或全为`amd_x86`
3.引导集群创建时，只有第一个引导节点需要配置账户权限和修改节点初始化引导开关，其余节点直接配置同步用户后加入节点即可。
4.数据库必须先初始化，然后再加载插件并修改添加相关配置。不能在初始化时就加载插件，插件会因为相关表不存在而报错，然后打断整个数据库的初始化过程。
5.Mysql8.0默认使用的密码插件`caching_sha2_password` 要求集群连接时使用SSL方式或者要求基于RSA密钥进行密码交换(需要客户端指定 `GET_MASTER_PUBLIC_KEY=1`)，最简单的办法就是直接修改密码插件为`mysql_native_password`。
6.mysql集群需要绑定本机IP，容器化部署会导致容器IP和宿主机IP不一致，随后集群绑定IP失败，解决办法为：将mysql的网络设置为host，直接使用宿主机IP。