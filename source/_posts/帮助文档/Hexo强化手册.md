---
title: Hexo强化手册
author: XUANWEN DING
categories:
  - - Hexo帮助
abbrlink: b4c91620
date: 2024-07-12 11:30:23
---
Hexo使用帮助文件，汇集总结使用中常见的各类配置和常见调整

<!-- more -->

## 1、在博客中添加文件

  在博客的根目录的配置文件_config.yml中，找到 post_asset_folder项，设置为true ，这样在创建文章时会自动在文章.md所在目录/source/_posts文件夹内生成一个与文章同名的文件夹。例如新建文章hexo new post example则会生成一个example.md文件与一个名为example的文件夹。
  例如 `hexo new "Hexo强化手册" -p 帮助文件/Hexo强化手册1`
这样就可以在 `帮助文件` 这个目录下，创建一个title叫`Hexo强化手册`，文件名称叫`Hexo强化手册1`的文件和与其同名的目录。

把example这个博文需要展示的图片放在example文件夹目录下；

文章内使用` [title](file_name) ` 的形式就可以创建一个跳转连接

---
## 更新hexo版本和依赖

```shell
# 先更新hexo-cli
npm install -g hexo-cli@latest
# 在博客根目录升级hexo核心
npm install hexo@latest --save
# 查看过时的包
npm outdated
# 升级所有依赖
npm update
# 清理缓存
hexo clean
# 生成静态文件
hexo generate
# 本地预览
hexo server
# 检查所有页面、功能是否正常
```

## 添加图片和文件
添加图片和文件，需要将图片和文件放在source文件夹下的file目录或img目录，例如 `source/img/example.png`
添加图片使用：`![title](/waterbottle/img/ptah/to/example.png`
添加文件可下载链接：`[title](/waterbottle/file/ptah/to/file`
注意文件下载链接前面没有感叹号 `!`