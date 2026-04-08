---
title: Linux通用命令操作
categories:
    - Linux
author: 瓶子
abbrlink: 52cd
date: 2025-12-16 14:31:38
tags: [通用,linux]
index_img:
banner_img:
---
一些Linux通用命令操作的记录

<!-- more -->

## 磁盘扩容
例：服务器根目录空间不足，新加一块硬盘，现在需要无损扩容给根目录。
`lsblk` 检查当前磁盘空间与分布，确认新磁盘已识别
![lsblk和fdisk-l确认磁盘](/waterbottle/img/Linux通用命令操作/lsblk和fdisk-l确认磁盘.png)

执行：`vgdisplay` 确认当前磁盘组
![vgdisplay](/waterbottle/img/Linux通用命令操作/vgdisplay.png)

执行：`lvdisplay` 确认需要扩容的逻辑卷，重点记住红框内的 **路径**
![lvdisplay](/waterbottle/img/Linux通用命令操作/lvdisplay.png)

到这一步，如果你使用的硬盘里有数据且已经挂载在服务器上，你需要先备份磁盘内的数据，然后卸载挂载的磁盘
因为接下来的操作会格式化磁盘导致数据清空。

使用：`fdisk` 进入磁盘管理功能，删除原有分区并创建新的LVM分区。如果是一个新磁盘，可以跳过这一步。
我们这次处理的磁盘是 `/dev/sdb` ，所以执行：`fdisk /dev/sdb`。然后在交互界面分别执行 `d` 和 `w`执行。删除分区并将配置写入磁盘，如果有多个分区都要删除。
操作完成后，执行 `partprobe /dev/sdb` 刷新分区信息。记得把 `/dev/sdb` 换成实际的磁盘路径
![删除和刷新分区](/waterbottle/img/Linux通用命令操作/删除和刷新分区.png)

接下来格式化磁盘为linux通用格式`ext4`，执行：`mkfs.ext4 /dev/sdb` 你也可以格式化为 `xfs`，执行：`mkfs.xfs /dev/sdb`。一般建议保持新旧磁盘一致。
如果提示设备有旧的文件系统签名，先执行：`wipefs -a /dev/sdb` 删除文件系统签名再执行格式化。
![格式化](/waterbottle/img/Linux通用命令操作/格式化.png)

创建LVM卷片组并将片组加入VG组中，执行：`pvcreate /dev/sdb`。然后执行 `pvs` 查看创建结果
![创建新的pv](/waterbottle/img/Linux通用命令操作/创建新的pv.png)

将新建的片组加入原先的VG组中，执行：vgextend klas /dev/sdb。执行完毕验证vg `vgs`或`vgdisplay`都可以。
重点验证 **VG Size** 是否已加载新的容量。
![vgextend](/waterbottle/img/Linux通用命令操作/vgextend.png)

扩容逻辑卷，根据开头执行 `lvdisplay`查询到的路径进行扩容
lvextend -L +300G /dev/klas/root
![lvextend.png](/waterbottle/img/Linux通用命令操作/lvextend.png)

根据被扩容磁盘格式，选择对应的刷新命令进行磁盘信息刷新
XFS格式使用：`xfs_growfs /`
ext4格式使用：`resize2fs /`

验证磁盘扩容成功，执行 `df -h` 查看磁盘空间
![验证扩容.png](/waterbottle/img/Linux通用命令操作/验证扩容.png)

如果需要再新建分区进行挂载，
执行：`lvcreate -L 400G -n data klas`
命令格式含义为：`lvcreate -L 容量 -n 新建的磁盘名称 所属VG组`
创建磁盘成功后，执行格式化命令：
ext4格式：`mkfs.ext4 /dev/klas/data`
xfs格式：`mkfs.xfs /dev/klas/data`

创建磁盘成功后，执行挂载命令：
`mount /dev/klas/data /data`
验证磁盘挂载成功，执行 `df -h` 或 `lsblk` 查看磁盘空间和挂载点。

确认扩容完成后，添加开机自动挂载
`vi /etc/fstab`
添加磁盘信息
`/dev/klas/data /data ext4 defaults 0 0`






