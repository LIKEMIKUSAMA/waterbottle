---
title: 认识Lambda表达式
author: 瓶子
categories:
  - - Java
    - Java快速入门学习手册
abbrlink: 58ce
date: 2025-06-26 14:58:37
tags:
index_img:
banner_img:
---
本章主要介绍Java中Lambda表达式并介绍表达式的作用和使用场景。

<!-- more -->
## 一、Lambda表达式
> Lambda表达式是Java 8新增的语法，**只适用于**简化使用了函数式接口的匿名内部类。

函数式接口:
* 函数式接口是**有且仅只有一个抽象方法**的接口。
```java
// 函数式接口
@FunctionalInterface  // 声明函数式接口的注解，加上后，接口的抽象方法只能有一个
interface Animal{
    void eat();
}
```

## 二、表达式如何替换匿名函数
替换格式
```textmate
(被重写方法的形参列表) -> {
    被重写方法的方法体代码。
}
```

```java
public class LambdaDemo {
    public static void main( String[] args ) {
        // 使用匿名函数
        Animal cat = new Animal() {
            @Override
            public void eat() {
                System.out.println("猫吃鱼");
            }
        }; 
        cat.eat();
        
        // 使用Lambda表达式简化匿名函数
        Animal lambdacat = () -> {
            System.out.println("使用Lambda表达式简化匿名函数");
        };
        lambdacat.eat();
    }
}

// 函数式接口
@FunctionalInterface
interface Animal {
    void eat();
}
```

## 三、Lambda表达式的优点
* 语法简洁，代码量少，可读性高。
这是Lambda函数最重要的优点。

## 四、Lambda表达式使用场景和简化规则

**Lambda表达式简化有以下规则**
* 参数类型全部可以省略不写。
* 如果只有一个参数，参数类型省略的同时“()”也可以省略，但多个参数不能省略“()”
* 如果Lambda表达式中只有一行代码，大括号可以不写，同时要省略分号“:” 如果这行代码是return语句，也必须去掉return。

代码演示，我们使用之前介绍内部类的代码来示范使用场景和简化规则
```java
/**
 * 匿名内部类实现接口。采用Arrays.sort方法实现排序作为例子。（使用Lambda表达式简化后）
 *
 * Version: 1.1
 * Author: 瓶子
 */
// 父类
public class Test {
    public static void main( String[] args ) {
        Student[] students = new Student[3];
        students[0] = new Student("张三", 19, 170.0, '男');
        students[1] = new Student("李四", 21, 160.0, '女');
        students[2] = new Student("王五", 18, 180.0, '男');

        //  public static void sort(T[] a, Comparator<T> c)
        //  参数一：需要排序的数组。
        //  参数二：给sort方法传递比较器对象Comparator，Comparator中制定排序规则。

        // 对student数组进行排序
        // 使用匿名内部类来满足Array.sort方法所需的参数。
//        Arrays.sort(students, new Comparator< Student >() {  // 创建匿名内部类对象
//            @Override
//            public int compare( Student o1, Student o2 ) {  // 比较规则
//                // 年龄升序
//                return o1.getAge() - o2.getAge();
//            }
//        });

//        // 上述方法使用Lambda表达式简化
//        Arrays.sort(students, (Student o1, Student o2) -> {
//            return o1.getAge() - o2.getAge();
//        });

//        // 按规则二次简化，去除o1和o2前面的参数类型名称
//        Arrays.sort(students, ( o1,  o2) -> {
//            return o1.getAge() - o2.getAge();
//        });
        
        // 按规则最终简化，去除return关键字，去除大括号。
        Arrays.sort( students, ( o1,  o2) ->  o1.getAge() - o2.getAge() );
        
        // 输出排序后的数组
        for ( int i = 0; i < students.length; i++ ) {
            Student student = students[i];
            System.out.println(student);
        }
    }
}

class Student {
    // 姓名，年龄，身高，性别。
    private String name;
    private int age;
    private double height;
    private char sex;

    // 篇幅有限，省略构造器和getter和setter方法。
    // ...
}    
```

