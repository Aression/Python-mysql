<!--
 * @Descripttion: 
 * @version: 
 * @Author: Lv Di
 * @Date: 2022-05-17 11:04:50
 * @LastEditors: Lv Di
 * @LastEditTime: 2022-05-17 13:22:01
-->

## 程序截图

1. 欢迎界面
2. select
3. update
4. delete
5. insert
6. use
7. create
8. drop
9. desc
10. show
11. exit/quit
12. select version
13. cwd

## 项目结构

1. data: 数据库存储位置
   1. 数据库
      1. 表（json文件）
2. lib：模拟程序代码
   1. core：核心代码
      1. base.py 定义了具体对数据表的操作，与具体的json文件交互
      2. env.py 环境信息
      3. function.py 操作接口代码，与操作语句交互
   2. parse：解析器代码
      1. SqlToCode.py sql语言转具体操作
3. index.py：入口脚本，定义了程序的入口

## 使用

```shell
python index.py
```
