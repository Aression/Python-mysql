import lib.core.function as function
import lib.core.base as db
import re
import os

bye = '''
____             
| __ ) _   _  ___ 
|  _ \| | | |/ _ \

| |_) | |_| |  __/
|____/ \__, |\___|
       |___/        
'''

def parseSql(sql):

    # sql 规范化 去首尾空格  将多个连续空格转一个
    sql = sql.lower()
    sql = sql.split(";")[0]
    sql = sql.split("#")[0]
    sql = sql.replace("||","or")
    sql = sql.replace("&&","and")
    sql = sql.strip()
    sql = re.sub("\/\*.*\*\/"," ",sql) # 替换注释符
    sql = re.sub(" +", " ", sql) 
    
    # 检测括号配对
    if sql.count("(") != sql.count(")"):
        if sql.count("(")>sql.count(")"):
            print("\033[1;31mERROR : 意外符号(\033[0m")
        else:
            print("\033[1;31mERROR : 意外符号)\033[0m")
        return 0
    # 单双引号检测
    if sql.count("'") % 2 != 0 :
        print("\033[1;31mERROR : 意外符号'\033[0m")
        return 0
    if sql.count('"') % 2 != 0 :
        print("\033[1;31mERROR : 意外符号\"\033[0m")
        return 0

    sql_arr = sql.split(" ")
    operation = sql_arr[0]

    try:
        # show 命令操作
        if operation == "show":
            operation1 = sql_arr[1]
            if operation1 == "databases":
                db.show_databases()
            elif operation1 == "tables":
                db.show_tables()
            else:
                print("\033[1;31mERROR : 未知操作 {0}\033[0m".format(operation1))
        # use 命令
        elif operation == "use":
            operation1 = sql_arr[1]
            db.select_db(operation1)

        # desc 查看表结构
        elif operation == "desc":
            operation1 = sql_arr[1]
            db.desc_from_table(operation1)

        # 退出
        elif operation == "exit" or operation == "quit":
            print("\033[32m" + bye + "\033[0m")
            os._exit(0)

        elif operation == "drop":

            operation1 = sql_arr[1]
            if operation1 == "table":
                table_name = sql_arr[2]
                db.drop_table(table_name)
            elif operation1 == "database":
                dbname = sql_arr[2]
            else:
                print("\033[1;31mERROR : 未知操作 {0}\033[0m".format(operation1))

        # 创建表 或者 库
        elif operation == "create":
            operation1 = sql_arr[1]
            if operation1 == "database":
                db.create_db(sql_arr[2])
            elif operation1 == "table":
                try:
                    # 将字符串分割成 表名 和 列名+type
                    table_name = sql_arr[2].split("(")[0]
                    key_value = sql.split("(")[1].split(")")[0]
                    # 将 列名与type 转化成json格式并放入 columns
                    columns = {}
                    for x in key_value.split(","):
                        tmp = x.strip()
                        column = tmp.split(" ")[0]
                        column_type = tmp.split(" ")[1]
                        columns.update({column: column_type})

                    if table_name != None or len(columns):
                        db.create_table(table_name, columns)
                    else:
                        print("\033[1;31mERROR : create 格式错误\033[0m")

                except Exception as e:
                    raise e

        # 查询操作
        elif operation == "select" :

            try:
                # 从表中查询数据
                if "from" in sql:
                    # limit 检测
                    limit = []
                    if "limit" in sql :
                        tmp_limit = sql.split("limit")[1]
                        sql = sql.split("limit")[0]
                        if "," in tmp_limit :
                            limit.append(int(tmp_limit.replace(" ","").split(",")[0]))
                            limit.append(int(tmp_limit.replace(" ","").split(",")[1]))
                        else:
                            limit.append(int(tmp_limit.replace(" ","")))

                    column = sql.split("select")[1].split("from")[0].replace(" ","")
                    table = sql.split("from")[1].split(" ")[1].strip()
                    # 多字段检测
                    columns = []
                    if "," in column :
                        columns = column.split(",")
                    else:
                        columns = [column]
                    # 多表检测
                    if "," in table:
                        tables = table.split(",")
                        wheres = []
                        if "where" in sql.split("from")[1]:
                            # 对条件进行匹配
                            tmp_where = sql.split("where")[1] 
                            tmp_wheres = re.findall("([a-zA-Z0-9]+[\ ]*[><=!]+[\ ]*[a-zA-Z0-9'\"]+)",tmp_where)    
                            
                            # 将所以有的关系词放入relations 默认第一个为and
                            relations = ["and"]
                            relations += re.findall("(or|and)",tmp_where)    
                            
                            # 将所有的条件放入一个数组
                            
                            for where in tmp_wheres :
                                wheres.append(where.strip())  
    
                            if len(wheres) != len(relations) :
                                print("\033[1;31mERROR : where语句解析错误0\033[0m")

                        db.table_join(tables,columns,wheres,limit)
                        return 0  
                    
                    if "where" not in sql :
                        # 多列的情况
                        if "," in column :
                            columns = column.split(",")
                            db.select_from_table(table,columns,[],limit)
                        elif len(column) != 0 :
                            db.select_from_table(table,[column],[],limit)
                    else:
                        
                        try:
                            # 对条件进行匹配
                            tmp_where = sql.split("where")[1] 
                            tmp_wheres = re.findall("([a-zA-Z0-9]+[\ ]*[><=!]+[\ ]*[a-zA-Z0-9'\"]+)",tmp_where)
    
                            # 将所以有的关系词放入relations 默认第一个为and
                            relations = ["and"]
                            relations += re.findall("(or|and)",tmp_where)
    
                            # 将所有的条件放入一个数组
                            wheres = []
                            for where in tmp_wheres :
                                wheres.append(where.strip())
                            
                            if len(wheres) != len(relations) :
                                print("\033[1;31mERROR : where语句解析错误0\033[0m")
                            db.select_data_from_table_with_where(table,columns,wheres,relations,limit)

                        except Exception as e:
                            print(e)
                            print("\033[1;31mERROR : where语句解析错误1\033[0m")
                        
                # 版本查询
                elif "version()" in sql:

                    if len(sql.split(" ")) == 2:
                           db.select_version()
                    else:
                        print("\033[1;31mERROR : SQL 解析错误\033[0m")

            except Exception as e:
                print("\033[1;31mERROR : select 格式错误\033[0m")
                raise e

        #  insert 语句处理
        #  insert into table (id,name) values ('1','2') , ('1','2');
        elif operation == "insert":
            if sql_arr[1] == "into" and "values" in sql :
                try:
                    table = sql_arr[2].split("(")[0]
                    #取第一个括号的内容为插入的列名，并按照逗号分隔
                    columns = sql.split(")")[0].split("(")[1].replace(" ","").split(",")
                    # 获取插入的数据 按照values 进行分割,再按照) 进行分割
                    tmp_value = sql.split("values")[1].strip()
                    values = re.findall("\((.*?)\)",tmp_value)

                    # 将括号的内容转化为 列表 最终形式为 [[1,2],[1,2]] 并进行相应的类型转化
                    for x in range(0,len(values)):
                        values[x] = values[x].split(",")

                        # 对插入的数据进行类型处理
                        for y in range(0,len(values[x])):
                            if "'" in values[x][y] or "\"" in values[x][y]:
                                values[x][y] = values[x][y].replace("'","").replace("\"","")
                            else:
                                try:
                                    values[x][y] = int(values[x][y])
                                except Exception as e:
                                    print("\033[1;31mERROR : 类型转化错误 检查字符串是否被引号包裹\033[0m")

                    # 检测 列与 value 的列是否相等
                    for x in values:
                        if len(columns) != len(x):
                            print("\033[1;31mERROR : 输入的列数不符\033[0m")
                    # 转化为接口能处理的形式
                    res_dict = []
                    for value in values:
                        tmp = {}
                        count = 0 
                        for column in value:
                            tmp.update({columns[count] : column})
                            count += 1
                        res_dict.append(tmp)
                    # 插入数据库
                    db.insert_into_table(table,res_dict)
                    
                except Exception as e:
                    raise e

            else:
                print("\033[1;31mERROR : SQL 解析错误\033[0m")
        # delete 语句处理
        # delete from users where id = 1
        elif operation == "delete":
            if sql_arr[1] == "from":
                table = sql_arr[2]
                # 如果没有where 则直接清空表中数据
                if "where" not in sql  and len(sql_arr)==3:
                    db.delete_from_table(table,[],[])
                else:
                    tmp_wheres = re.findall("[a-zA-Z0-9]+[\ ]*[><=!]+[\ ]*[a-zA-Z0-9'\"]+",sql.split("where")[1])
                    wheres = []
                    for where in tmp_wheres:
                        wheres.append(where.strip())

                    relations = ["and"]
                    relations += re.findall("(or|and)",sql.split("where")[1])
                    db.delete_from_table(table,wheres,relations)

            else:
                print("\033[1;31mERROR : delete 格式错误\033[0m")
        # 更新操作 
        # update table set a=1  where id = 1
        # 转化为 db.update_from_table("table",{"a":1},{"id":["=",2]})
        elif operation == "update":
            table = sql_arr[1]
            if "where" in sql :
                tmp_sets = sql.split("set")[1].split("where")[0].strip()
                if "," in tmp_sets:
                    tmp_sets = tmp_sets.split(",")
                else:
                    tmp_sets = [tmp_sets]

                # 匹配set 并放入sets
                sets = {}
                for _set in tmp_sets:
                    sets.update({_set.split("=")[0].strip():_set.split("=")[1].strip()})
                tmp_wheres = re.findall("[a-zA-Z0-9]+[\ ]*[><=!]+[\ ]*[a-zA-Z0-9'\"]+",sql.split("where")[1])
                
                # where子句匹配
                wheres = []
                for where in tmp_wheres:
                    wheres.append(where.strip())

                relations = ["and"]
                relations += re.findall("(or|and)",sql.split("where")[1])

                db.update_from_table(table,sets,wheres,relations)
            else:
                print("\033[1;31mERROR : update解析错误\033[0m")

        elif operation == "help":
            db.help()
        else:
            print("\033[1;31mERROR : 未知语句\033[0m")

    except Exception as e:
        raise e
        print("\033[1;31mERROR : SQL 解析错误\033[0m")
