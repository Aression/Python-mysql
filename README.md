<!--
 * @Descripttion: 
 * @version: 
 * @Author: Lv Di
 * @Date: 2022-05-17 11:04:50
 * @LastEditors: Lv Di
 * @LastEditTime: 2022-05-17 13:28:44
-->

## 程序截图

1. 欢迎界面
   
   ![](C:\Users\hanyi\AppData\Roaming\marktext\images\2022-05-29-15-49-18-E951FAA70C8C4B2F9D534A4227AF4C4D.png)
   
   

2. select
   
   ![](C:\Users\hanyi\AppData\Roaming\marktext\images\2022-05-29-14-45-09-image.png)

3. update
   
   ![](C:\Users\hanyi\AppData\Roaming\marktext\images\2022-05-29-15-03-54-image.png)

4. delete
   
   ![](C:\Users\hanyi\AppData\Roaming\marktext\images\2022-05-29-14-58-21-image.png)

5. insert
   
   ![](C:\Users\hanyi\AppData\Roaming\marktext\images\2022-05-29-14-51-28-image.png)

6. use
   
   ![](C:\Users\hanyi\AppData\Roaming\marktext\images\2022-05-29-14-24-19-image.png)

7. create
   
   ![](C:\Users\hanyi\AppData\Roaming\marktext\images\2022-05-29-14-49-10-image.png)

8. drop
   
   ![](C:\Users\hanyi\AppData\Roaming\marktext\images\2022-05-29-14-49-29-image.png)

9. desc
   
   ![](C:\Users\hanyi\AppData\Roaming\marktext\images\2022-05-29-14-31-08-image.png)

10. show
    
    ![](C:\Users\hanyi\AppData\Roaming\marktext\images\2022-05-29-14-30-26-image.png)

11. exit/quit
    
    ![](C:\Users\hanyi\AppData\Roaming\marktext\images\2022-05-29-14-06-27-image.png)

12. select version
    
    ![](C:\Users\hanyi\AppData\Roaming\marktext\images\2022-05-29-14-06-04-image.png)

13. cwd
    
    ![](C:\Users\hanyi\AppData\Roaming\marktext\images\2022-05-29-14-05-37-image.png)

## 原理

1. DBMS架构

2. 数据存储的实现

3. 事务管理

4. 进程管理与冲突解决

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
