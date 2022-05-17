"""
Descripttion: 
version: 
Author: Lv Di
Date: 2022-05-17 11:04:50
LastEditors: Lv Di
LastEditTime: 2022-05-17 13:04:09
"""
"""
Descripttion: 
version: 
Author: Lv Di
Date: 2022-05-17 11:04:50
LastEditors: Lv Di
LastEditTime: 2022-05-17 11:25:58
"""
import lib.core.base as db
import lib.core.function as function
import lib.parse.SqlToCode as SqlToCode
import json
import os
import sys
import getpass

version = 1.0
welcome = f"""                                                                                                                                                                                                                                                                                                             
welcome to python DBMS simuator \n
-- 键入help 命令查看帮助
-- 当前版本: {version}
"""

if __name__ == "__main__":
    os.system("cls")
    print("\033[34m" + welcome + "\033[0m")
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
