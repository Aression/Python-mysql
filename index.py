"""
Descripttion: 
version: 
Author: Lv Di
Date: 2022-05-17 11:04:50
LastEditors: Lv Di
LastEditTime: 2022-05-17 13:04:09
"""
import libary.core.base as db
import libary.core.function as function
import libary.parse.SqlToCode as SqlToCode
import os
import getpass
from libary.core.env import *

welcome = f"""welcome to python DBMS simuator"""
notify = f"""
-- 环境信息: 版本={VERSION}, 数据存储目录={os.getcwd()}\{DB_PATH}
-- 键入help 命令查看帮助"""

if __name__ == "__main__":
    os.system("cls")
    print("\033[1;34m" + welcome + "\033[0m")
    print("\033[0;34m" + notify + "\033[0m")
    while True:
        try:
            sql = input(
                f"\n\033[36m[{getpass.getuser()} at {os.getcwd()}] # DBMS>> \033[0m"
            )
            if len(sql) != 0:
                SqlToCode.parseSql(sql)
        except Exception as e:
            print("出现了如下错误: \n")
            print(e)
