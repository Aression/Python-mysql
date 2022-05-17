import os
import json
import re
import lib.core.env as env
import lib.core.function as function


def create_db(dbname):
    try:
        if os.path.exists(env.DB_PATH) == False:
            os.mkdir(env.DB_PATH)
        db_tmp = env.DB_PATH + "/" + dbname
        if os.path.exists(db_tmp) == False:
            os.mkdir(db_tmp)
            print("数据库{0}创建成功".format(dbname))
        else:
            print("\033[1;31mERROR : 数据库已存在\033[0m")
    except Exception as e:
        print("\033[1;31mERROR : 数据库创建失败\033[0m")


def select_db(dbname):
    db_tmp = env.DB_PATH + "/" + dbname
    if os.path.exists(db_tmp) == True:
        env.CURRENT_DB = dbname
        env.CURRENT_PATH = db_tmp
        print("成功切换到数据库{0}".format(dbname))
    else:
        print("\033[1;31mERROR : 数据库不存在\033[0m")


def create_table(table_name, columns):
    """
    create table test(id int,name string)
    columns = {'id': 'int', 'name': 'string'}
    """
    for column in columns:
        if columns[column] not in ["string", "int"]:
            print("\033[1;31mERROR : 仅支持的数据类型为 int string\033[0m")
            return 0
    if env.CURRENT_DB == "":
        print("\033[1;31mERROR : 未选择数据库\033[0m")
        return 0

    tmp_table_path = env.CURRENT_PATH + "/" + table_name + ".json"

    try:
        if os.path.exists(tmp_table_path) == False:
            with open(tmp_table_path, "w") as f:
                f.write(json.dumps(columns) + "\n")
                print("表{0}创建成功".format(table_name))
        else:
            print("\033[1;31mERROR : 表{0}已存在\033[0m".format(table_name))
    except Exception as e:
        print("\033[1;31mERROR : 表创建失败，可能原因为data目录没有权限\033[0m")
        print(e)


def show_databases():

    try:
        db_list = os.listdir(env.DB_PATH)
        if len(db_list) == 0:
            print("\033[1;31mERROR : 暂无数据库\033[0m")
            return 0
    except Exception as e:
        print("\033[1;31mERROR : 暂无数据库\033[0m")
        return 0

    res = []
    for x in db_list:
        res.append({"Database": x})

    function.console_print(["Database"], res)


def show_tables():
    """
    查看数据库中表的信息
    """
    if env.CURRENT_DB == "":
        print("\033[1;31mERROR : 未选择数据库\033[0m")
        return 0
    table_list = os.listdir(env.CURRENT_PATH)

    res = []
    for x in table_list:
        res.append({"Tables_in_{0}".format(env.CURRENT_DB): x.split(".")[0]})

    function.console_print(["Tables_in_{0}".format(env.CURRENT_DB)], res)


def select_version():
    """
    查看数据库版本
    """
    if env.VERSION == "":
        print("\033[1;31mERROR : 环境错误\033[0m")

    function.console_print(["version"], [{"version": env.VERSION}])


def drop_db(dbname):
    db_tmp = env.DB_PATH + "/" + dbname + "/"
    try:
        if os.path.isdir(db_tmp) == True:
            os.removedirs(db_tmp)
            print("成功删除库{0}".format(dbname))
        else:
            print("\033[1;31mERROR : 删除库错误 库{0}不存在\033[0m".format(dbname))
    except Exception as e:
        print("\033[1;31mERROR : 删除库错误 原因未知\033[0m")


def drop_table(table_name):
    # 想要删除表的路径
    tmp_table_path = env.CURRENT_PATH + "/" + table_name + ".json"
    if env.CURRENT_DB == "":
        print("\033[1;31mERROR : 未选择数据库\033[0m")
        return 0
    try:
        if os.path.isfile(tmp_table_path) == True:
            os.remove(tmp_table_path)
            print("成功删除表{0}".format(table_name))
        else:
            print("\033[1;31mERROR : 删除表错误 表{0}不存在\033[0m".format(table_name))
    except Exception as e:
        print("\033[1;31mERROR : 删除表错误 原因未知\033[0m")
        print(e)


def insert_into_table(table_name, data):
    """
    data的类型为 [{"name":x,"sex":x},{"name":x,"sex":x}]
    """
    tmp_table_path = env.CURRENT_PATH + "/" + table_name + ".json"

    if os.path.isfile(tmp_table_path) == False:
        print("\033[1;31mERROR : 数据表{0}不存在\033[0m".format(table_name))
        return 0

    # 检查表头是否存在
    table_info = function.get_table_info(tmp_table_path)
    if table_info == False:
        return 0

    # 检查数据是否 符合表的结构
    for x in data:
        if function.check_data_with_table_format(tmp_table_path, x) == False:
            return 0
    # 尝试写入数据
    try:
        if os.path.isfile(tmp_table_path) == True:
            # 监测数据是否存在
            with open(tmp_table_path, "r") as f:
                lines = f.readlines()
                for line in lines:
                    if json.loads(line) in data:
                        print("\033[1;31mERROR : 暂不支持重复数据\033[0m")
                        return 0
            with open(tmp_table_path, "a") as f:
                for x in data:
                    f.write(json.dumps(x) + "\n")
                print("数据插入成功")
        else:
            print("\033[1;31mERROR : 数据表{0}不存在\033[0m".format(table_name))
    except Exception as e:
        raise e
        pass


def delete_from_table(table_name, wheres, relations):
    """
    where 为条件 格式为字典类型 如 {"id":[">","3"],"name":["=","张三"]}
    """
    tmp_table_path = env.CURRENT_PATH + "/" + table_name + ".json"
    # 获取表头信息
    table_info = function.get_table_info(tmp_table_path)
    if table_info == False:
        return False
    table_info = json.loads(table_info)

    # 获取表中所有数据
    data = function.get_all_data_from_table(tmp_table_path)
    if data == False:
        return False

    # 若where 为空则将表清空
    if len(wheres) == 0:
        try:
            with open(tmp_table_path, "w") as f:
                f.write(json.dumps(table_info) + "\n")
                print("成功删除{}条数据".format(len(data)))
                return 0
        except Exception as e:
            print("\033[1;31mERROR : 清空表时异常\033[0m")
            return 0

    # 查询

    tmp_wheres = []
    for where in wheres:
        operation = re.findall("[><=!]+", where)
        if len(operation) == 2:
            operation = str(operation[0]) + str(operation[1])
        else:
            operation = operation[0]
        tmp_column = where.split(operation)[0].replace(" ", "")
        value = where.split(operation)[1].strip()
        tmp_wheres.append({tmp_column: [operation, value]})

    # 转化成最终形式
    # [{"and": {"id":["=",1]}},{"or":{"id":[">",1]}}]
    tmp_where = []
    for x in range(0, len(relations)):
        tmp_where.append({relations[x]: tmp_wheres[x]})

    res = function.data_where(table_info, data, tmp_where)
    if res == False:
        return 0

    # 判断是否于原表数据一样
    if res == data:
        print("\033[1;31mERROR : 无可满足条件的数据\033[0m")
        return 0
    try:
        with open(tmp_table_path, "w") as f:
            f.write(json.dumps(table_info) + "\n")
            for x in data:
                if x not in res:
                    f.write(json.dumps(x) + "\n")
            print("成功删除{0}条数据".format(len(res)))
    except Exception as e:
        raise e


def select_from_table(table_name, columns, where, limit):
    """
    columns 格式为 [column1,column2]
    where 为条件 格式为字典类型 如 {"id":[">","3"],"name":["=","张三"]}
    """
    tmp_table_path = env.CURRENT_PATH + "/" + table_name + ".json"

    # 查询
    res = function.table_where(tmp_table_path, where)
    if res == False:
        return 0

    # 获取表结构
    table_info = function.get_table_info(tmp_table_path)
    if table_info == False:
        return 0
    table_info = json.loads(table_info)

    res_data = function.columns_filter(table_name, table_info, columns, res)
    header_data = res_data[0]
    res_data.remove(header_data)

    # 引入limit 功能
    if len(limit) != 0:
        res_data = function.data_limit(res_data, limit)

    function.console_print(header_data, res_data)


def update_from_table(table_name, set_rule, wheres, relations):
    """
    set格式   set name = xxx ,id = xx  转化为 {"name":"xxxx","id":"xxxx"}
    """
    tmp_table_path = env.CURRENT_PATH + "/" + table_name + ".json"

    if os.path.isfile(tmp_table_path) == False:
        print("\033[1;31mERROR : 数据表{0}不存在\033[0m".format(table_name))
        return 0

    # 检查表头是否存在
    table_info = function.get_table_info(tmp_table_path)
    if table_name == False:
        return 0
    table_info = json.loads(table_info)

    # 获取所有记录
    data = function.get_all_data_from_table(tmp_table_path)
    if data == False:
        return 0

    # 筛选满足条件的记录
    tmp_wheres = []
    for where in wheres:
        operation = re.findall("[><=!]+", where)
        if len(operation) == 2:
            operation = str(operation[0]) + str(operation[1])
        else:
            operation = operation[0]
        tmp_column = where.split(operation)[0].replace(" ", "")
        value = where.split(operation)[1].strip()
        tmp_wheres.append({tmp_column: [operation, value]})

    # 转化成最终形式
    # [{"and": {"id":["=",1]}},{"or":{"id":[">",1]}}]
    tmp_where = []
    for x in range(0, len(relations)):
        tmp_where.append({relations[x]: tmp_wheres[x]})

    #
    res = function.data_where(table_info, data, tmp_where)

    # 记录未被修改的数据
    tmp_dict = []
    for x in data:
        if x not in res:
            tmp_dict.append(x)

    # 对res 的结果按照 set 规则进行修改
    # 检测列是否存在
    for x in set_rule:
        if x not in table_info:
            print("\033[1;31mERROR : set 中列{0}不存在\033[0m".format(x))
            return 0
    # 对·set值进行约束、规范化
    for x in set_rule:
        if '"' in set_rule[x] or "'" in set_rule[x]:
            set_rule[x] = set_rule[x].replace('"', "").replace("'", "")
        else:
            try:
                set_rule[x] = int(set_rule[x])
            except Exception as e:
                print("\033[1;31mERROR : set 中值错误\033[0m")

    # 属性修改
    for x in set_rule:
        column = x
        value = set_rule[x]
        i = 0
        while i < len(res):
            res[i][column] = value
            i = i + 1

    # 将修改结果保存到数据库
    try:
        with open(tmp_table_path, "a") as f:
            f.truncate(0)
            f.write(json.dumps(table_info) + "\n")
            for x in res:
                f.write(json.dumps(x) + "\n")
            for x in tmp_dict:
                f.write(json.dumps(x) + "\n")
            print("数据修改成功")
    except Exception as e:
        raise e


def desc_from_table(table_name):
    """
    打印 表结构
    """
    if env.CURRENT_DB == "":
        print("\033[1;31mERROR : 未选择数据库\033[0m")
        return 0

    tmp_table_path = env.CURRENT_PATH + "/" + table_name + ".json"
    # 获取表结构
    table_info = function.get_table_info(tmp_table_path)
    if table_info == False:
        return 0
    table_info = json.loads(table_info)

    res = []
    for x in table_info:
        res.append({"Field": x, "Type": table_info[x]})

    function.console_print(["Field", "Type"], res)


def select_data_from_table_with_where(table_name, columns, wheres, relations, limit):

    tmp_table_path = env.CURRENT_PATH + "/" + table_name + ".json"

    # 获取表结构
    table_info = function.get_table_info(tmp_table_path)
    if table_info == False:
        return 0
    table_info = json.loads(table_info)

    # 获取表中所有数据
    data = function.get_all_data_from_table(tmp_table_path)
    if data == False:
        return False

    # 将wheres 转化成函数能处理的类型
    # e.g. id = 1 -> {"id":["=",1]}}

    tmp_wheres = []
    for where in wheres:
        operation = re.findall("[><=!]+", where)
        if len(operation) == 2:
            operation = str(operation[0]) + str(operation[1])
        else:
            operation = operation[0]
        tmp_column = where.split(operation)[0].replace(" ", "")
        value = where.split(operation)[1].strip()
        tmp_wheres.append({tmp_column: [operation, value]})

    # 转化成最终形式
    # e.g. [{"and": {"id":["=",1]}},{"or":{"id":[">",1]}}]
    tmp_where = []
    for x in range(0, len(relations)):
        tmp_where.append({relations[x]: tmp_wheres[x]})
    res_data = function.data_where(table_info, data, tmp_where)
    res_data = function.columns_filter(table_name, table_info, columns, res_data)

    # 表头
    header_data = res_data[0]
    res_data.remove(header_data)

    # 引入limit 功能
    if len(limit) != 0:
        res_data = function.data_limit(res_data, limit)

    function.console_print(header_data, res_data)


def table_join(table_names, columns, wheres, limit):

    tmp_table_paths = []
    for table_name in table_names:
        tmp_table_paths.append(env.CURRENT_PATH + "/" + table_name + ".json")

    join_tmp_table = []

    if len(tmp_table_paths) != 2:
        print("\033[1;31mERROR : 不支持多于2的多表查询\033[0m")
        return 0

    # 获取所有表的表头信息
    table_head_arr = []
    for table_path in tmp_table_paths:
        tmp_head = function.get_table_info(table_path)
        if tmp_head == False:
            return 0
        table_head_arr.append(list(json.loads(tmp_head).keys()))

    # 获取所有表的内容
    tables_data_arr = []
    for table_path in tmp_table_paths:
        tmp_data = function.get_all_data_from_table(table_path)
        if tmp_data == False:
            return 0
        tables_data_arr.append(tmp_data)

    # 检查表头是否有重复元素，存在则对第二个表起别名
    # 仅考虑两个表的清框
    repat_columns = list(set(table_head_arr[0]).intersection(set(table_head_arr[1])))
    for x in range(0, len(table_head_arr[1])):
        if table_head_arr[1][x] in repat_columns:
            table_head_arr[1][x] = "_" + table_head_arr[1][x]

    tmp_table_data = []
    for datas in tables_data_arr[1]:
        tmp_dict = {}
        for data in datas:
            if data in repat_columns:
                tmp_dict.update({"_" + data: datas[data]})
            else:
                tmp_dict.update({data: datas[data]})
        tmp_table_data.append(tmp_dict)

    tables_data_arr[1] = tmp_table_data
    # 表头合并
    table_head = table_head_arr[0] + table_head_arr[1]

    # 表的连接 - 笛卡尔积
    dikaer = []
    for x in range(0, len(tables_data_arr[0])):
        for y in range(0, len(tables_data_arr[1])):
            tmp = {**tables_data_arr[0][x], **tables_data_arr[1][y]}
            dikaer.append(tmp)

    # 引入limit 功能
    if len(limit) != 0:
        dikaer = function.data_limit(dikaer, limit)

    function.console_print(table_head, dikaer)

notify = """本数据库按照 MYSQL 为原型进行修改，大致操作同mysql
支持SQL 语句大小写、注释符/**/ #、 || && 、 where 支持比较运算符 > >= < <= = != 
"""

actions = """SQL指令
1. SELECT 列名,列名... FROM 表名 [WHERE 条件 [[AND] [OR]] [LIMIT N 或者 N,M]
2. UPDATE 表名 SET 列名=新值, 列名=新值 [WHERE 条件 [AND [OR]]
3. DELETE FROM 表名 [WHERE  条件 [AND [OR]]
4. INSERT INTO 表名 ( 列名,列名,...)VALUES (值,值,...)
5. USE 数据库名
6. CREATE [DATABASE|TABLE] [库名|表名(列名 类型,列名 类型....)]  # 类型只支持int string两种类型
7. DROP [DATABASE|TABLE] [库名|表名]
8. DESC 表名
9. SHOW [DATABASES|TABLES]
10. SELECT * FROM 表名,表名 [limit N 或者 N,M]

DBMS指令
11. EXIT QUIT
12. SELECT VERSION()
13. CWD"""
def help():
    print(f"\033[1;33m{notify}\033[0m")
    print(f"\033[32m{actions}\033[0m")
