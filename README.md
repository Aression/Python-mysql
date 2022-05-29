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

   ![2-tier dbms architecture](https://gitee.com/orange-mint/upload-image/raw/master/202205291728288.png)

   在用户和DBMS之间包含一个应用程层，该层负责将用户的请求传达给数据库管理系统，然后将响应从DBMS发送给用户。

   这样的架构为DBMS提供了额外的安全性，因为它不会直接暴露给最终用户。同样，可以通过在应用程序层中添加安全性和身份验证检查来提高安全性。

2. 数据存储的实现

   使用关系数据库，采用二维表格来存储数据，按行与列排列的具有相关信息的逻辑组。一个数据库可以包含任意多个数据表。

3. 事务管理

   数据库锁：通过给数据库中被操作的数据加锁来实现，分为共享锁【读锁】，互斥锁【写锁】

   版本号于时间戳：在更新数据前，需要检查版本号是否发生了变化，变化了则取消更新，否则成功更新数据。

4. 进程管理与冲突解决

   IGNORE：当使用INSERT语句向表中添加一些行数据并且在处理期间发生错误时，INSERT语句将被中止，并返回错误消息。因此，可能不会向表中插入任何行。但是，如果使用INSERT INGORE语句，则会忽略导致错误的行，并将其余行插入到表中。
   
   REPLACE INTO：如果发现表中已经有此行数据（根据主键或者唯一索引判断）则先删除此行数据，然后插入新的数据。
   否则，直接插入新数据。要注意的是：插入数据的表必须有主键或者是唯一索引！否则的话，replace into 会直接插入数据，这将导致表中出现重复的数据。 
   
   

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
