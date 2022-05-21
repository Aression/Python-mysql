import json, os
from logging import exception
import env

index_base = "indexs"


"""原功能：
def reset_index(table_name):
    tmp_table_path = env.CURRENT_PATH + "/" + table_name + ".json"

    # 预检查
    if os.path.isfile(tmp_table_path) == False:
        print("\033[1;31mERROR : 数据表{0}不存在\033[0m".format(table_name))
        return 0

    # 检查表头是否存在
    table_info = function.get_table_info(tmp_table_path)
    if table_info == False:
        return 0

    try:
        if os.path.isfile(tmp_table_path) == True:
            # 重设index 貌似没用？
            lines = None
            with open(tmp_table_path, "r+") as f:
                lines = f.readlines()
            with open(tmp_table_path, "w+") as f:
                if len(lines) > 1:
                    f.truncate()
                    f.write(lines[0])
                    ind = 0
                    for line in lines[1:]:
                        print(line)
                        tmp = json.loads(line)
                        tmp["_index"] = ind
                        f.write(json.dumps(tmp) + "\n")
                        ind += 1
                    print("索引重设成功")
                else:
                    print("无需重设索引,没有足够的元素")

    except Exception as e:
        print(f"无法重设索引：{e}")
"""


class Index:
    def __init__(self, col=0, table_lst: dict = None, table_name: str = None) -> None:
        # 默认为第一列创建索引, 并存储在_index.json中。
        index_file_path = f"{env.CURRENT_PATH}/{index_base}"
        key = list(table_lst[0].keys())[col]

        # 第一次创建索引
        if not os.path.ispath(index_file_path):
            os.mkdir(index_file_path)
        with open(f"{index_file_path}/{table_name}.json", "w+") as f:
            for line in table_lst[1:]:
                f.write(str(line[key]) + "\n")
        pass

    def update():
        pass

    def load(path):
        pass

    def binary_search(conditions):
        pass


if __name__ == "__main__":
    """
    Usage
    """
    dbname = "diego"
    env.CURRENT_PATH = env.DB_PATH + "/" + dbname
    table_name = "user1"
    try:
        dict_lst = []
        with open(f"{env.CURRENT_PATH}/{table_name}.json", "r") as f:
            lines = f.readlines()
            for line in lines:
                dict_lst.append(json.loads(line))
        index = Index(0, dict_lst, table_name)

    except Exception as e:
        print(f"Error occured: {e}")
