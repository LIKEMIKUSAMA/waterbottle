---
title: Linux小练习
author: XUANWEN DING
categories:
  - [Linux,CentOS,CentOS练习题] 
abbrlink: 9e9006f1
date: 2023-12-29 10:42:27
---
问题难度不分先后，实现答案**不唯一**。一个题不会可以先跳去另一个。有思路可以不急着看答案，先百度找找资料尝试一下。如果思路也没有，百度也不会，那建议对着答案和注释找AI一点点分析为毛这么做。
<!-- more -->

## 第一题 TCP链接和进程可打开文件数的检测与配置。

请写出一个脚本
1、可以判断系统是否已配置可将 TIME-WAIT 状态下的 TCP 重新用于新的 TCP 连接。
2、可以判断系统是否已配置单个进程最大可打开文件数为204800。
3、如系统无相关配置，则该脚本需要按上述要求配置。
4、如系统有相关配置但未启用，则该脚本需要将配置修改为允许。
5、设置后需要即时生效
<details>
<summary> 答案 </summary>

```bash
#!/bin/bash
# TCP连接复用
if ! cat /etc/sysctl.conf | grep "net.ipv4.tcp_tw_reuse" ; then
cat << EOF >> /etc/sysctl.conf
net.ipv4.tcp_tw_reuse = 1
EOF
else 
sed -i '/net.ipv4.tcp_tw_reuse/c\net.ipv4.tcp_tw_reuse = 1' /etc/sysctl.conf #调整
echo "已调整配置为 ： $(cat /etc/sysctl.conf | grep "net.ipv4.tcp_tw_reuse")" #输出调整后的结果
fi

# 单个进程最大文件打开数
if ! cat /etc/sysctl.conf | grep "fs.file-max" ; then
cat << EOF >> /etc/sysctl.conf
fs.file-max = 204800
EOF
else 
sed -i 'fs.file-max/c\fs.file-max = 204800' /etc/sysctl.conf #调整
ehco "已调整配置为 ： $(cat /etc/sysctl.conf | grep "fs.file-max")" #输出调整后的结果
fi

# 刷新内核配置
echo "重新加载内核文件...."
/sbin/sysctl -p

```

</details>

## 第二题 tcp链接的检测与清理

写出一个脚本
1、查询并输出出所有状态为 ESTABLISHED 的 ssh 连接
2、清理上述连接
<details>
<summary> 答案 </summary>

```bash
#!/bin/bash
# 查询链接信息
echo "查询链接信息....."
netstat -natp|awk '/ssh/&&/ESTABLISHED/'

# 清理连接 
echo "----------------------"
echo "查询完毕，开始清理。。。"
echo "----------------------"

netstat -natp|awk '/ssh/&&/ESTABLISHED/ {print $7}'|awk -F '/' '{print $1}'|xargs kill

# 验证
echo "----------------------"
echo "清理完毕，请确认剩余连接信息:"
echo "----------------------"
netstat -natp|awk '/ssh/&&/ESTABLISHED/'
```

</details>

## 第三题 文件的移动

解压 root 目录下的 log.tar.gz 文件至 opt 目录下

<details>

<summary> 答案 </summary>

`tar -zxvf /root/log.tar.gz -C /opt/`
</details>

## 第四题 文件内容的快速替换

将 opt 目录下的 log.tar.gz 解压出来的文件内，以 Listen 开头的所有内容替换为 Listen=12123

<details>

<summary> 答案 </summary>

`sed -i 's/^Listen*/Listen=12123/g' log.log`
</details>

## 第五题 日志关键字的快速检索与输出

从文件 info.log 中检索 logics 为关键字的日志，并将其内容输出到 log1.log 文件内
<details>

<summary> 答案 </summary>

`cat info.log |grep logics >> log1.log`
</details>

## 第六题 监控脚本

请写出一个脚本
1、该脚本监视名为 server 的服务进程
2、当服务掉线时，使用 /root/start.sh 脚本启动程序，并输出带有启动时间和服务重启的关键字至 monitor.log
3、如果服务在运行，输出包含当前时间和服务运行正常关键字的日志到 monitor.log
<details>

<summary> 答案 </summary>

```bash
flag=$(ps -ef|grep "server"|grep -v "grep"|wc -l)
    if [ $flag == 0 ]
    then
        /root/start.sh 
        ehco "服务已重启，重启时间为：$(date)" >> /root/monitor.log
    else
        echo "server 运行正常，检测时间：$(date) " >> /root/monitor.log
    fi
```

</details>

## 第七题 Nginx配置理解

请写出下面代码中四行内容分别代表什么配置

```nginx
# nginx配置
    server {
        listen      80 ;
        server_name rabbitmq-dingxuanwen.yovole.com;      
        location  / {       
        proxy_pass http://paas.yovole.com:15672/; 
        }

```

<details>

<summary> 答案 </summary>

```nginx
# nginx配置
    server {
        listen      80 ;   #监听端口
        server_name rabbitmq-dingxuanwen.yovole.com;   #监听地址       
        location  / {       #请求的url过滤，正则匹配，~为区分大小写，~*为不区分大小写。
        proxy_pass http://paas.yovole.com:15672/;  #请求转向定义的服务列表     
        }
```

</details>

## 第八题 文件的复制

将 /root/logs/ 下的所有文件，**复制**到 /home/ 下

<details>

<summary> 答案 </summary>

```bash
cp /root/logs/* /home/
```

</details>

## 第九题 多个组件的检测与安装

写出一个脚本
1、该脚本可以检测多个第三方库是否已安装
2、如果未安装该脚本需要将库安装完。
<details>

<summary> 答案 </summary>

```bash
#!/bin/bash
Bakge=(dos2unix lrzsz telnet mailx net-tools vim)

#遍历包
for i in ${Bakge[@]}; do
    if rpm -qa | grep $i; then
        echo"$i 已安装无需重复安装"
    else
        yum -y install $i
    fi
done

```

</details>






---

<details>

<summary> 千万别点开 </summary>

```txt
未完待续。。。。
```

</details>
