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
   
   ![image-20220529172141676](https://gitee.com/orange-mint/upload-image/raw/master/202205291721829.png)

2. select
   
   ![](https://gitee.com/orange-mint/upload-image/raw/master/202205291720365.png)

3. update
   
   ![](https://gitee.com/orange-mint/upload-image/raw/master/202205291720808.png)

4. delete
   
   ![](https://gitee.com/orange-mint/upload-image/raw/master/202205291720633.png)

5. insert
   
   ![](https://gitee.com/orange-mint/upload-image/raw/master/202205291720679.png)

6. use
   
   ![](https://gitee.com/orange-mint/upload-image/raw/master/202205291720846.png)

7. create
   
   ![](https://gitee.com/orange-mint/upload-image/raw/master/202205291720250.png)

8. drop
   
   ![](https://gitee.com/orange-mint/upload-image/raw/master/202205291721495.png)

9. desc
   
   ![](https://gitee.com/orange-mint/upload-image/raw/master/202205291721403.png)

10. show
    
    ![](https://gitee.com/orange-mint/upload-image/raw/master/202205291721813.png)

11. exit/quit
    
    ![](https://gitee.com/orange-mint/upload-image/raw/master/202205291721878.png)

12. select version
    
    ![](https://gitee.com/orange-mint/upload-image/raw/master/202205291721875.png)

13. cwd
    
    ![](https://gitee.com/orange-mint/upload-image/raw/master/202205291721439.png)
    
    

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
