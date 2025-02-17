import os
import json


def get_table_info(table_path):
    # 存在返回值，返回值为文件的第一行
    # 需要表的路径
    # 如 data/test/test.json  /// get_table_info(env.CURRENT_PATH + "/" + table_name + ".json")

    try:
        if os.path.isfile(table_path) == True:
            with open(table_path, "r") as f:
                info = f.readline()
                return info
        else:
            print("\033[1;31mERROR : 数据表{0}不存在\033[0m".format(table_path))
            return False
    except Exception as e:
        print("\033[1;31mERROR : 获取表信息失败\033[0m")
        return False


def check_data_with_table_format(table_name, data):
    # 检查信息是否与表的格式一致
    # 用在 insert 语句

    # 获取table结构
    tmp_info = get_table_info(table_name)
    if tmp_info == False:
        return False

    # 删除内置索引
    table_info = json.loads(tmp_info)
    table_info.pop('_index')

    try:
        # 长度检查
        if len(table_info) != len(data):
            print("\033[1;31mERROR : 数据与信息表结构不符\033[0m")
            return False
        # 字段检查
        for columns in data:
            if columns not in table_info:
                print("\033[1;31mERROR : 列{0}不存在\033[0m".format(columns))
                return False
        return True

    except Exception as e:
        print(e)
        print("\033[1;31mERROR : 发生异常\033[0m")
        return False


def get_all_data_from_table(table_path):
    """
    以json 格式进行返回 [data1,data2...]
    """
    if os.path.isfile(table_path) == False:
        print("\033[1;31mERROR : 表不存在\033[0m")
        return False

    try:
        with open(table_path, "r") as f:
            tmp_data = f.readlines()
            del tmp_data[0]
            data = []

            for x in tmp_data:
                data.append(json.loads(x))
            return data
    except Exception as e:
        raise e


def table_where(table_path, where):
    """
    where 格式 {"id":["=",1]} 键值为字段
    """
    # 获取表头信息
    table_info = get_table_info(table_path)
    if table_info == False:
        return False

    table_info = json.loads(table_info)

    # 检查字段是否存在于表中
    for columns in where:
        if columns not in table_info:
            print(
                "\033[1;31mERROR : 字段{0} 不存在于表{1}中\033[0m".format(columns, table_path)
            )
            return False

    # 获取表中所有数据
    data = get_all_data_from_table(table_path)
    if data == False:
        return False

    # 将表头写入首元素
    res = []

    # 没有条件则全部返回
    if where == None or where == [] or where == "":
        return data
    # 将取出where 中的元素
    # 如 {"id":["=",2]}  operation 为 = ，condition为2
    # eval 构造的为 id=2
    # 即判断data 中id=2的 记录

    res = select_data(table_info, data, where)
    del res[0]
    return res


def select_data(table_info, data, wheres):
    res = []
    for sub_where in wheres:
        operation = wheres[sub_where][0]
        condition = wheres[sub_where][1]
        if operation == "=":
            operation += "="

        for x in data:
            column = str(table_info[sub_where])
            # 对列类型进行判断
            if column == "string":
                column1 = '"' + x[sub_where] + '"'
                # condition1 = "\"" + condition + "\""

                if eval(column1 + str(operation) + str(condition)) == True:
                    # 做交并运算时不支持dict 先转成json string
                    res.append(json.dumps(x))

            if column == "int":
                if eval(str(x[sub_where]) + str(operation) + str(condition)) == True:
                    res.append(json.dumps(x))
    return res


def data_where(table_info, data, wheres):
    """
    从数据中筛选合适的数据 支持 and or
    wheres 格式为 [{"and": {"id":["=",1]}},{"or":{"id":[">",1]}}]
    键值为 or and
    data 格式为 [{表头信息},{data},{data}]
    """

    if len(data) == 0:
        # 无数据返回
        print("\033[1;31mERROR : 无可反回数据\033[0m")
        return 0

    # 条件为空则全返回
    if len(wheres) == 0:
        return data

    res = []
    count = 0
    for where in wheres:
        relation = list(where.keys())[0]
        res_tmp = select_data(table_info, data, where[relation])
        if count == 0:
            if relation == "and":
                res = res_tmp
        else:
            if relation == "and":
                # 交集运算
                res = list(set(res).intersection(set(res_tmp)))
            elif relation == "or":
                # 并集运算
                res = list(set(res).union(set(res_tmp)))
        count += 1

    # 将经过交并运算的json-string转化为原格式
    result = []
    for x in res:
        result.append(json.loads(x))

    return result
    # console_print(table_info,result)


def console_print(header_data, json_data):
    """
    header_data 格式为 ["column1","column2"]
    json_data 格式为 [{"column1":"xx","column2":"xx"}]
    """
    if len(header_data) == 0:
        print("暂无数据")
        return 0

    column_len = len(header_data)
    # 记录每列最长的长度
    column_max_len_array = [0 for x in range(0, column_len)]

    # 对头进行长度统计
    count = 0
    for x in header_data:
        if len(x) > column_max_len_array[count]:
            column_max_len_array[count] = len(x)
        count += 1

    # 对元素进行长度统计
    for x in json_data:
        count = 0
        for y in x:
            if len(str(x[y])) > column_max_len_array[count]:
                column_max_len_array[count] = len(str(x[y]))
            count += 1

    # 打印开始
    sum_tmp = 0
    for x in column_max_len_array:
        sum_tmp += x

    # 行首
    print("+".ljust(sum_tmp + len(column_max_len_array) * 10, "-") + "+")

    # 打印表头
    count = 0
    tmp_str = ""
    for head in header_data:
        tmp_str += ("| " + head).ljust(column_max_len_array[count] + 10, " ")
        count += 1

    print(tmp_str + "|")
    print("+".ljust(sum_tmp + len(column_max_len_array) * 10, "-") + "+")

    # 打印数据
    for data in json_data:
        tmp_str = ""
        count = 0
        for column in data:
            tmp_str += ("| " + str(data[column])).ljust(
                column_max_len_array[count] + 10, " "
            )
            count += 1
        print(tmp_str + "|")

    if len(json_data) == 0:
        print("|暂无数据".ljust(sum_tmp + len(column_max_len_array) * 10 - 4, " ") + "|")

    # 打印行尾
    print("+".ljust(sum_tmp + len(column_max_len_array) * 10, "-") + "+")


def columns_filter(table_name, table_info, columns_filter, data):
    # 对列进行过滤
    # 按列 筛选
    # 检测字段是否位于表中
    for column in columns_filter:
        if column == "*":
            continue
        if column not in table_info:
            print("\033[1;31mERROR : {0}表中没有字段{1}\033[0m".format(table_name, column))
            return 0

    header_data = []
    res_tmp = []
    # 按列筛选
    if "*" == columns_filter[0]:
        for x in table_info:
            header_data.append(x)
    else:
        # 过滤表头
        for x in table_info:
            if x in columns_filter:
                header_data.append(x)
        # 过滤数据
        for x in data:
            tmp_dict = {}
            for column in x:
                if column in columns_filter:
                    tmp_dict.update({column: x[column]})
            res_tmp.append(tmp_dict)

        data = res_tmp

    # header_data 加入data 头部
    return [header_data] + data


def data_limit(data, limit):
    """
    limit 格式 [n,y]
    """

    tmp_data = []
    tmp1_data = []
    if len(data) == 0:
        return []

    if len(limit) == 1:
        for x in range(0, limit[0]):
            # limit 超长处理
            if x < len(data):
                tmp_data.append(data[x])
    else:
        for x in range(limit[0], limit[0] + limit[1]):
            if x < len(data):
                tmp_data.append(data[x])

    return tmp_data
