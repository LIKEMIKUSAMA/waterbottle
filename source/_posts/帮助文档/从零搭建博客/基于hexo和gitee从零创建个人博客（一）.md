---
title: 基于hexo和gitee从零创建个人博客（一）
author: XUANWEN DING
categories:
  - - 从零搭建博客
abbrlink: 8f01206d
date: 2023-12-27 16:12:04
updated: 2023-12-27 16:12:04
---

这一部分主要介绍如何先在本地搭建Hexo。
本文主要介绍基于 Hexo 和 Gitee Pages 功能来实现个人页面的创建和托管
网页页面是基于 Markdown 文件来生成的。
代码托管基于 Gitee 实现。
所以如果你想要使用同样的方法来操作，你需要学会 Markdown 格式下的文本写法。Git代码管理工具的使用。

## 一、安装Git

Windows：你需要点击[这里](https://git-scm.com/download)去下载 window 版的客户端，以管理员身份运行后，一直选择下一步安装即可，请注意，如果你不熟悉每个选项的意思，请保持默认的选项。
虽然Git的使用网上有很多介绍，但是如果你需要Git的官方帮助文档，可以点击[这里](https://git-scm.com/book/zh/v2)
安装好之后，使用 **`git --version`** 来确认安装是否成功。

## 二、安装NodeJS

Hexo 是基于 NodeJS 编写的，所以需要安装一下 NodeJS 和里面的 npm 工具。
Windows：点击[这里](https://nodejs.org/en/download/)下载，直接下载LTS下的安装包就可以了。
下载完成后，命令行工具验证一下是否安装成功。

``` bash
node -v
npm -v
#由于npm默认的下载源地址在国外，所以这里建议将源切换为淘宝的源
npm config set registry https://registry.npmmirror.com

#然后确认一下当前设置的源
npm config get registry

#如果你需要默认源
npm config set registry https://registry.npmjs.org
```

## 三、安装并初始化Hexo

前面两部安装完成后我们就可以开始安装 Hexo 了。你可以先创建一个文件夹(例如MyBlog)，然后在这个文件夹内右键，使用 Git bash 打开(Open Git Bash here)。如果你Git安装成功的话，这一步应该难不倒你。
输入命令
**`npm install -g hexo-cli`**
执行完成后还是使用 **`hexo -v`** 查看版本来确认是否安装成功、
接下来，初始化一下Hexo

```bash
# YourBlogName请替换成你自己取得名字，这个目录将成为存放你blog文件的目录。
hexo init YourBlogName

# 然后cd进入这个目录
cd YourBlogName

#执行
npm install
```

执行成功后，目录内将会出现存放博客运行所需要的依赖和 Hexo 的文章模板以及自带的默认主题的目录。
接下来，启动 Hexo

```bash
hexo g
hexo s
```

浏览器输入[http://localhost:4000/](http://localhost:4000/)就可以看到你的博客主页了

***注意！！！***
如果你现在关闭了 bash 页面，那 Hexo 也会停止运行。所以如果你想一直保持 Hexo 运行的话有两种选择
1、不关闭打开的这个 bash 页面（**不推荐**）
2、安装 pm2 ,使用 pm2 来执行脚本保证 Hexo 的运行（**推荐**）
第一步：**安装 pm2**
`npm  install -g pm2`
第二步：在根目录下创建一个文件，命名为 hexo_run.js 然后把下面的命令复制进去

```js
//run
const { exec } = require('child_process')
exec('hexo server',(error, stdout, stderr) => {
        if(error){
                console.log('exec error: ${error}')
                return
        }
        console.log('stdout: ${stdout}');
        console.log('stderr: ${stderr}');
})
```

第三步：在根目录下执行
`pm2 start hexo_run.js`
如果需要停止，只要把 start 替换成 stop 即可
参考：[hexo后台运行](https://blog.csdn.net/tangcuyuha/article/details/80331169)

到现在为止，你已经可以在本机和内网网络上访问你的博客了。当然请记得将作为服务器的电脑设置为固定ip或保持开机哦。
