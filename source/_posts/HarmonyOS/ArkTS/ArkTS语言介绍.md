---
title: ArkTS语言介绍
author: XUANWEN DING
categories:
  - - HarmonyOS
    - ArkTS
abbrlink: b501a5f5
date: 2024-01-21 00:49:23
---
ArkTS语言基础语法和介绍

<!-- more -->

```ts
// 被此装饰器装饰的组件，代表用作页面的默认入口组件。
// 加载页面时，将首先创建并呈现 @Entry 装饰自定义组件。
@Entry
// 表示自定义组件，用来装饰下面的 struct ListItemComponent
@Component 
// 被 @Component 装饰，代表一个自定义的结构体，是可重用的UI单元，可以和其他组件组合。
// export 关键字可以导出 ListItemComponent 组件
// 在其他地方调用时，须先使用 import 导入子组件。
export struct ListItemComponent { 
    // 使用 @State 装饰的变量 isChange。
    // 含义是当 isChange 发生变化时，会触发该变量所对应的自定义组件 ListItemComponent 的UI界面进行自动刷新
    @State isChange: boolean = false; 
// 上述结构为装饰器内容，装饰器主要是用来装饰类、结构、方法和变量，赋予其特殊的含义。
// UI描述：指 build 方法中的代码块，以声明式的方式描述该自定义组件 ListItemComponent 的UI结构
    build() {
        // 内置组件：系统提供的基础组件和容器组件，可以直接调用
        // 内置组件 Row 指水平方向布局的容器组件
        Row() {
            // 内置组件 Text 文本组件，用来展示文件。
            Text(this.name)
              // 属性方法：设置组件属性，使用 “.” 运算符来进行链接
              .width(ItemStyle.LAYOUT_WEIGHT_CENTER)
              .fontSize(FontSize.MIDDLE)
            Text(this.vote)
              // 属性方法：设置组件属性，使用 “.” 运算符来进行链接
              .width(ItemStyle.LAYOUT_WEIGHT_CENTER)
              .fontSize(FontSize.SMALL)
            ...
        }
    }
    .height(ItemStyle.BAR_HEIGHT)
    .width(WEIGHT)
    // 事件方法：设置组件对事件的响应逻辑
    // 此为 Row 组件的 onClick 方法，点击组件可以触发该方法的调用，并在其中进行响应处理。
    .onClick(() => {
        this.isChange = !this.isChange;
    })
}
...
```

## 自定义组件生命周期回调函数

```ts
// 生命周期回调函数用于通知开发者组件所属的生命周期阶段
// 这两个函数是私有的，系统会在合适的时间自动调用，是无法手动调用这些函数的

aboutToAppear
在创建自定义组件实例后，到执行其 build 函数前执行。
可以在该函数中对 UI 需要展示的数据进行初始化，或申请定时器资源等。
便于在 build 函数中使用这些数据展示。

aboutToDisappear
自定义组件实例被销毁时调用，可以在其中释放不再使用的资源，避免资源泄露。
比如释放 aboutToAppear 中申请的定时器。


```

## @Entry 修饰的页面入口组件生命周期回调函数

```ts

```
