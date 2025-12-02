---
title: CentOS系统命令和操作技巧
author: XUANWEN DING
categories:
  - [Linux,CentOS]
abbrlink: 7d6c437
date: 2024-04-11 10:55:49
---
CentOS系统命令和操作技巧，整和大部分常用命令和操作方式等。

<!-- more -->

---

## 一、系统配置类

### 1.1、防火墙操作命令

```bash
# 查看防火墙状态
firewall-cmd --state

# 启/停用防火墙
systemctl start/stop firewalld

# 禁止/开启firewall开机启动：
systemctl disable/enable  firewalld

# 开放端口
firewall-cmd --zone=public --add-port=80/tcp --permanent

# 关闭端口
firewall-cmd --zone=public --remove-port=80/tcp --permanent
命令含义： --zone #作用域 --add-port=80/tcp #添加端口，格式为：端口/通讯协议 --permanent #永久生效，没有此参数重启后失效

#做完重启防火墙；
[参考连接](https://www.cnblogs.com/Sungeek/p/8257681.html)

# 开启http
firewall-cmd --add-service=http --permanent

# 查看http是否开启
firewall-cmd --query-service http

# 重启防火墙命令：
firewall-cmd --reload

# 查询开放的端口：
firewall-cmd --list-port
```

---

### 1.2、修改系统ip地址等网络配置

```bash
# 路径：/etc/sysconfig/network-scripts/

# 安装ifconfig包：
yum -y install net-tools
#此目录下放置着系统的网络配置文件，修改时需要先确认目前本机使用的是哪个配置再进行修改

# 修改配置固定IP：
BOOTPROTO=static
IPADDR=xxx.xxx.xxx.xxx # 这里填ip
NETMASK=xxx.xxx.xxx.xxx # 这里填网络掩码，如255.255.255.0
GATEWAY=xxx.xxx.xx.xxx # 这里填网关ip

# 添加DNS识别
# 修改/etc/resolv.conf文件，添加DNS识别地址
# 阿里解析
nameserver 223.5.5.5
# 谷歌解析
nameserver 8.8.8.8

# 查看网关配置：
netstat -rn

# 重启网卡，选其一执行即可
service network restart;
systemctl restart network
```

---

### 1.3、更改默认启动模式

```bash
# 获取当前默认模式
# multi-user.target 相当于之前的更改运行级别为3，意思就是命令行。
# graphical.target 相当于之前的更改运行级别为5，意思就是图形界面
systemctl get-default

# 修改启动模式为图形界面，
systemctl set-default graphical.target 

# 修改为命令行
systemctl set-default multi-user.target 
```

---

### 1.4、禁用swap

```bash
# 执行如下命令，关闭所有swap分区：
swapoff -a

# 检查sysctl.conf文件，添加swap权重限制
cat /etc/sysctl.conf |grep swappiness

# 如无输出，root用户执行
echo "vm.swappiness=0" >> /etc/sysctl.conf

# 如无输出，普通用户执行
sudo sh -c "echo "vm.swappiness=0" >> /etc/sysctl.conf"

# 刷新stsctl文件
sysctl -p
```

---

### 1.5、定时任务

```bash
# 查看定时任务是否启动 
service crond status

# 强杀干扰crond任务启动的所有进程
pkill cron

# 再执行命令：
service crond start
```

<https://www.cnblogs.com/han20180705/p/9638992.html>

### 1.6、时间校准

1)、服务器可以通外网

```bash
# 安装NTP同步工具
yum -y install ntpdate
# 手动同步一次时间
# 中国科学院国家授时中心NTP授时服务器地址： ntp.ntsc.ac.cn
ntpdate ntp.ntsc.ac.cn && clock -w

# 录入定时任务，实现自动同步
crontab -e
# 定时每天2点同步时间
0 2 * * * ntpdate ntp.ntsc.ac.cn && clock -w
```

2)、服务器不通外网

```bash
# 手动设置时间并写入时钟
date -s "2021-08-05 10:52:40" && clock -w
```

### 1.7、修改允许打开的最大文件数

```bash
vi /etc/security/limits.conf 
# 所有用户允许打开的文件数量最大为65535
* soft nofile 65536
* hard nofile 65536
# 也可以把 * 换成指定的用户
```

---

## 二、使用和操作技巧

### 2.1、解压和压缩

```bash
# 将目录里所有jpg文件打包并且将其用gzip压缩，生成命名为jpg.tar.gz的压缩包
tar –zcvf jpg.tar.gz *.jpg 

# 解压tar.gz
tar -zxvf file.tar.gz 
```

---

### 2.2、查看目录下文件数量

```bash
# 统计当前文件夹下文件的个数，不包含子文件夹
ls -l |grep "^-"|wc -l

# 在默认的情况下，wc将计算指定文件的行数、字数，以及字节数。
wc testfile 
3 92 598 testfile # testfile文件的行数为3、单词数92、字节数598
```

---

### 2.3、nginx日志切割

```bash
#!/bin/bash
#日志路径
log_path=/data/nginx/log
log_bak=/data/nginx/logbak
#PID路径
pid_path=/run/nginx.pid
#昨天日期
YesterDay=$(date `+%Y-%m-%d`)
#今天日期
today=$(date `+%Y-%m-%d`)
#生成昨天的日志文件
mv ${log_path}/wxds1.towngasvcc.com.access.log ${log_bak}/wxds1.towngasvcc.com.access.log_${YesterDay}.log
# 向 Nginx 主进程发送 USR1 信号。USR1 信号是重新打开日志文件
kill -USR1 `cat ${pid_path}`
```

---

### 2.4、Find命令技巧

```bash
# 列出当前目录下符合条件的文件名
find -name 'tcis3.201912*' -exec basename {} \;

# 找到当前目录下指定开头的文件，并全部使用gzip解压
find -maxdepth 1 -name "trans*" | xargs -i gzip -d {}

# 找到目录下日志大于当前30天的文件并删除
# 替换 username
find /home/{username}/wwyt/db_backfiles -mtime +30 -name "*.sql" -exec rm -f {} ;
```

---

### 2.5、dos文件转unix

vi进入文件后，使用 `set ff?`查看当前文件格式。用`set ff=unix` 来修改为linux可读取格式

---

### 2.6、查询硬件信息

```bash
# 查询线程：
grep 'processor' /proc/cpuinfo | sort -u | wc -l
cat /proc/cpuinfo | grep "processor" |wc -l

# 查询核数
cat /proc/cpuinfo | grep "cores"|uniq

# cpu详细信息
lscpu

# 硬盘信息
lsscsi
# 如不存在该命令，需安装
yum -y install lsscsi

# 磁盘层级信息
lsblk

# 打印硬盘信息
sudo fdisk -l

# 打印硬盘详细信息
sudo lshw -class disk
# 如不存在该命令，需安装
yum -y install lshw

# 固态机械盘判定  （返回值0即为SSD；返回1即为HDD）
cat /sys/block/ 盘名 /queue/rotational
```

---

### 2.7、磁盘读写性能测试

<details>

**<summary> 脚本内容 </summary>**

```python
import sys, os, time, random

#--------------------------------------------------------------------------------------------------

def BytesString(n):
    suffixes = ['B','KB','MB','GB','TB','PB','EB','ZB','YB']
    suffix = 0
    while n % 1024 == 0 and suffix+1 < len(suffixes):
        suffix += 1
        n /= 1024
    return '{0}{1}'.format(n, suffixes[suffix])

def BytesInt(s):
    if all(c in '0123456789' for c in s):
        return int(s)
    suffixes = ['B','KB','MB','GB','TB','PB','EB','ZB','YB']
    for power,suffix in reversed(list(enumerate(suffixes))):
        if s.endswith(suffix):
            return int(s.rstrip(suffix))*1024**power
    raise ValueError('BytesInt requires proper suffix ('+' '.join(suffixes)+').')

def BytesStringFloat(n):
    x = float(n)
    suffixes = ['B','KB','MB','GB','TB','PB','EB','ZB','YB']
    suffix = 0
    while x > 1024.0 and suffix+1 < len(suffixes):
        suffix += 1
        x /= 1024.0
    return '{0:0.2f}{1}'.format(x, suffixes[suffix])


#--------------------------------------------------------------------------------------------------

disk = open('/dev/dm-2', 'r')
disk.seek(0,2)
disksize = disk.tell()
os.system('echo noop | sudo tee /sys/block/sdb/queue/scheduler > /dev/null')

print 'Syntax: progam [-s -sr -t -tr] [-v]:  to run specific modes; for verbose mode.'
print 'Disk name: {0}  Disk size: {1}  Scheduler disabled.'.format(
    disk.name, BytesStringFloat(disksize))

displaytimes = '-v' in sys.argv


#--------------------------------------------------------------------------------------------------

bufsize = 512
bufcount = 100
displaysamplecount = 24

for randomareas in [False,True]:
    print
    print 'Measuring: Random seek time {0}'.format(
        'using random areas of disk.' if randomareas else 'using beginning of disk.')
    print 'Samples: {0}{1}   Sample size: {2}'.format(
        bufcount, ' (displayed {0})'.format(displaysamplecount) if displaytimes else '', bufsize)

    for area in [BytesInt('1MB')*2**i for i in range(0,64)]+[disksize]:
        if area > disksize:
            continue

        os.system('echo 3 | sudo tee /proc/sys/vm/drop_caches > /dev/null')

        times = []
        disk.seek(0)
        disk.read(bufsize)
        for _ in range(bufcount):
            left = random.randint(0, disksize-area) if randomareas else 0
            right = left + random.randint(0, area)
            disk.seek(left)
            disk.read(bufsize)
            start = time.time()
            disk.seek(right)
            disk.read(bufsize)
            finish = time.time()
            times.append(finish-start)

        times = sorted(times)[:bufcount*95/100]
        print 'Area tested: {0:6}   Average: {1:5.2f} ms   Max: {2:5.2f} ms   Total: {3:0.2f} sec'.format(
            BytesString(area) if area < disksize else BytesStringFloat(area),
            sum(times)/len(times)*1000, max(times)*1000, sum(times))
        if displaytimes:
            print 'Read times: {0} ... {1} ms'.format(
                ' '.join(['{0:0.2f}'.format(x*1000) for x in times[:displaysamplecount/2]]),
                ' '.join(['{0:0.2f}'.format(x*1000) for x in times[-displaysamplecount/2:]]))
```

</details>

```bash
sudo python iotestlinux.py
```

---

### 2.8、查看监听的端口

```bash
netstat -lnpt
iptables -L -n
```

---

### 2.9、查看服务器网卡流量

```bash
# 安装
yum install -y sysstat

# 1秒提取一次网络数据 共提取两次数据。
sar -n DEV 1 2

```

---

### 2.10、查看连接/进程流量

```bash
# ss 和 netstat 是查看活动链接/监听端口的常用命令。ss 是 netstat 的上位替代，性能更好
ss/netstat

# ss安装
yum install -y iproute

# netstat安装：
yum install -y net-tools

# iftop是一款实时流量监控工具，可以查看每个连接的实时速率。
# 安装命令
yum install -y epel-release && yum install -y iftop 
# 实时查看eth0网卡的各个连接和网速：
iftop -nN -i eth0

# nethogs是为了查看单个进程流量而设计的工具，按照进程进行带宽分组。
# 安装命令
yum install -y epel-release && yum install -y nethogs
# 每2秒刷新流经eth0网卡的进程流量信息：
nethogs -d 2 eth0 
```

---

### 2.11、清理缓存

```bash
# 非root用户执行
sync
sudo sh -c "echo 3 > /proc/sys/vm/drop_caches" 

# 也可以写成下面的脚本放到服务器里
#!/bin/bash
sync
echo 3 > /proc/sys/vm/drop_caches

# 添加定时任务
*/10 * * * * clean_free.sh

# 保存定时任务并重启
service crond restart 
```

---

### 2.12、磁盘挂载

```bash
# 检查磁盘
fdisk -l

# 找到需要处理的磁盘，例如 /dev/sda 格式化
mkfs.ext4 /dev/sda

# 创建挂载点
mkdir /data

# 挂载磁盘到挂载点
mount /dev/sda /data/

# 修改fstab任务，让系统启动时就自动挂载，防止重启后磁盘未挂载
vi /etc/fstab
/dev/sda /data ext4 defaults 0 0 # 系统启动时自动挂载

# 赋予用户账户使用权限，任选一个就行
sudo chown -R user:user /data # 把挂载点改为指定用户的权限
sudo chmod -R 775 /data # 挂载点服务器全部用户都可以使用的权限。

# 设置开机时自动赋予权限
vi /etc/rc.local

chown -R user:user /data
sudo chmod -R 775 /data

# 设置软连接（如需要）
# 进入到你需要设置软连接的目录下
ln -s /data/xxx 放软连接的目录
```

### 2.13、系统性能监控工具

[点击此处下载文件](nmon-16g-3.el7.x86_64.rpm)

```bash
# 下载文件，然后上传到服务器目录，执行
sudo rpm -ivh nmon-16g-3.el7.x86_64.rpm

# 进入交互页面，按提示按下快捷键，进入具体的硬件性能监控
nmon
```

### 2.14、网络测速

[点击此处下载文件](speedtest.py)

```bash
# 下载文件，然后上传到服务器目录，授予权限
chmod 775 speedtest.py
# 执行,等待结果
./speedtest.py

```

### 2.15、sed命令替换指定内容

```bash
#将新字符串替换旧字符串
sed -i 's/ 旧字符串 / 新字符串 /g' file1 file2 file3 

```

### 2.16、SCP文件传输

```bash
scp [options] [source] [user@]destination
# [options]：是可选参数，比如-r用于递归复制目录，-p用于保留文件属性。
# [source]：指定要复制的源文件或目录的路径。
# [user@]destination：远程系统的用户名和IP地址（或者主机名），以及目的文件或目录的路径。
# 例如 ：
scp file.txt remote_user@10.0.109.19:/home/remote_user/
# 如果需要指定目标文件的名称，可以在远程路径后面加上文件名
scp file.txt remote_user@10.0.109.19:/home/remote_user/file.txt

# 如果想要保留文件的基本属性（如修改时间、访问时间等），可以使用-p选项；
# 如果需要递归复制整个目录及其子目录和文件，则应使用-r选项
```
