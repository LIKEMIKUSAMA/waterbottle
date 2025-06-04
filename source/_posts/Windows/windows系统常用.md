---
title: windows系统常用命令
author: XUANWEN DING
categories:
  - [windows系统]
date: 2023-12-29 10:34:03
updated: 2023-12-29 10:34:03
---

## 如何开启win10远程桌面：

<https://blog.csdn.net/jianglg2008/article/details/52839340>
<https://github.com/stascorp/rdpwrap/issues/744>

远程桌面服务启停：
`net stop/start termservice`

---

## 使用powershell做端口联通性测试

`test-netconnection 112.33.11.113 -port 8889`

---

## 网络联通性测试（此命令CMD也可以使用）

`tracert ip`
可以用来追踪机器链接到服务器的跳点，可以来判断网络是否通畅
也可以用 ping 获取对应 ip 然后使用 tracert 命令

---

## 重新初始化网络环境

`netsh winsock reset`
可以用以解决由于软件冲突、病毒原因造成的系统参数错误问题。


