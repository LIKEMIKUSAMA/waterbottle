---
title: Gitee仓库操作指南
author: XUANWEN DING
categories:
  - [Gitee指南]
date: 2024-04-16 17:50:46
---
Gitee仓库操作指南合集，如果需要详细指南可以参考[Gitee帮助中心](https://gitee.com/help)

<!-- more -->

## 仓库设置SSH，生成/添加SSH公钥

按如下命令来生成 sshkey
`ssh-keygen -t ed25519 -C "xxxxx@xxxxx.com"`
这里的-t 指定密钥类型，默认是 rsa ，可以省略。

**注意：这里的 xxxxx@xxxxx.com 只是生成的 sshkey 的名称，并不约束或要求具体命名为某个邮箱。**
**现网的大部分教程均讲解的使用邮箱生成，其一开始的初衷仅仅是为了便于辨识所以使用了邮箱。**

按照提示完成三次回车，即可生成 ssh key。通过查看 ~/.ssh/id_ed25519.pub 文件内容，获取到你的 public key
`cat ~/.ssh/id_ed25519.pub`

复制生成后的 ssh key，通过仓库主页 「管理」->「部署公钥管理」->「添加部署公钥」 ，添加生成的 public key 添加到仓库中。

`ssh -T git@gitee.com`
首次使用需要确认并添加主机到本机SSH可信列表。若返回 Hi XXX! You've successfully authenticated, but Gitee.com does not provide shell access. 内容，则证明添加成功。