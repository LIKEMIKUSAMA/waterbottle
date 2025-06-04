---
title: 基于hexo和gitee从零创建个人博客（二）
author: XUANWEN DING
categories:
  - [从零搭建博客]
date: 2023-12-27 16:12:04
updated: 
---
这一部分主要介绍如何将博客托管到Gitee
本文主要介绍基于 Hexo 和 Gitee Pages 功能来实现个人页面的创建和托管
网页页面是基于 Markdown 文件来生成的。
代码托管基于 Gitee 实现。
所以如果你想要使用同样的方法来操作，你需要学会 Markdown 格式下的文本写法。Git代码管理工具的使用。

<!-- more -->
## 一、在 Gitee 上新建一个仓库

在 Gitee 上新建一个仓库，注意仓库必须是公开开源的，仓库名称和路径尽量使用方便记忆的名称，你最终访问的地址和这个有关。
**注意**仓库语言必须选择为 `JavaScript`
当然你也可以给这个仓库配置上SSH公钥实现免密登录。（不是必须的）
如果你不清楚如何创建一个仓库并配置SSH，可以参考 {% post_link Gitee仓库操作指南 %} 中 **仓库设置SSH，生成/添加SSH公钥** 段落


## 二、安装 Hexo 的部署插件

```bash
#切换到项目根目录，安装插件
npm install hexo-deployer-git --save
```

安装成功后，在项目根目录下找到 `_config.yml` 文件，该文件为默认配置文件。
在文件中找到类似下方结构的配置，并进行修改
如果你不知道如何找到仓库地址，参考 [gitee帮助手册](https://help.gitee.com/enterprise/code-manage/%E4%BB%A3%E7%A0%81%E6%89%98%E7%AE%A1/%E4%BB%A3%E7%A0%81%E4%BB%93%E5%BA%93/git%20clone%E6%88%96%E4%B8%8B%E8%BD%BD%E4%BB%A3%E7%A0%81)

```bash
# Deployment
## Docs: https://hexo.io/docs/one-command-deployment
deploy:
  type: git
  repo:  仓库URL地址 #https://gitee.com/gitee/HelloGitee.git
  branch: master #这里填写仓库分支，一般默认是master，如果和你的不一致，你也可以进行修改
```

## 三、将项目文件推送到远程仓库

在推送文件之前，我们需要先去 Git 内配置一些配置

```bash
git config --global user.name "XXX" #码云用户名
git config --global user.email "XXX@xx.com" #码云的关联邮箱
```

在项目根目录打开 Git bash 窗口，然后输入 `hexo d`，然后等待文件被推送到仓库即可，如果你没有配置SSH公钥，那会出现弹窗让你输入远程仓库的账号密码用来验证。

## 四、开启 Gitee Pages 静态网页托管服务

检查项目文件已经全部上传完毕后，我们需要去仓库主页面内，找到服务按钮，点击其中的 Gitee Pages，选择好分支后，启动服务。进入生成的网址即可访问博客。
**注意** 每次代码上传后都需要回到此页面内点击**更新**按钮重启 Pages 服务。
