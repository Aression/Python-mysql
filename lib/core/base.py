import os
import json
import lib.core.env as env
import lib.core.function as function

def create_db(dbname):
	try:
		if os.path.exists(env.DB_PATH) == False :
			os.mkdir(env.DB_PATH)
		db_tmp = env.DB_PATH + "/" + dbname
		if os.path.exists(db_tmp) == False :
			os.mkdir(db_tmp)
			print("数据库{0}创建成功".format(dbname))
		else :
			print("ERROR : 数据库已存在")
	except Exception as e:
		print("ERROR : 数据库创建失败")

def select_db(dbname):
	db_tmp = env.DB_PATH + "/" + dbname
	if os.path.exists(db_tmp) == True :
		env.CURRENT_DB = dbname
		env.CURRENT_PATH = db_tmp
		print("成功切换到数据库{0}".format(dbname))
	else:
		print("ERROR : 数据库不存在")

def create_table(table_name,columns):
	'''
	create table test(id int,name string)
	columns = {'id': 'int', 'name': 'string'}
	'''
	if env.CURRENT_DB == "":
		print("ERROR : 未选择数据库")
		return 0

	tmp_table_path = env.CURRENT_PATH + "/" + table_name + ".json"

	try:
		if os.path.exists(tmp_table_path) == False :
			with open(tmp_table_path,"w") as f :
				f.write(json.dumps(columns) + "\n")
				print("表{0}创建成功".format(table_name))
		else:
			print("ERROR : 表{0}已存在".format(table_name))
	except Exception as e:
		print("ERROR : 表创建失败，可能原因为data目录没有权限")
		print(e)

def drop_db(dbname):
	db_tmp = env.DB_PATH + "/" + dbname + "/"
	print(db_tmp)
	try:
		if os.path.isdir(db_tmp) == True:
			os.removedirs(db_tmp)
			print("成功删除库{0}".format(dbname))
		else:
			print("ERROR : 删除库错误 库{0}不存在".format(dbname))
	except Exception as e:
		print("ERROR : 删除库错误 原因未知")

def drop_table(table_name):
	# 想要删除表的路径
	tmp_table_path = env.CURRENT_PATH + "/" + table_name + ".json"
	if env.CURRENT_DB == "":
		print("ERROR : 未选择数据库")
		return 0
	try:
		if os.path.isfile(tmp_table_path) == True :
			os.remove(tmp_table_path)
			print("成功删除表{0}".format(table_name))
		else:
			print("ERROR : 删除表错误 表{0}不存在".format(table_name))
	except Exception as e:
		print("ERROR : 删除表错误 原因未知")
		print(e)

def insert_into_table(table_name,data):
	'''
	data的类型为 [{"name":x,"sex":x},{"name":x,"sex":x}]
	'''
	tmp_table_path = env.CURRENT_PATH + "/" + table_name + ".json"

	if os.path.isfile(tmp_table_path) == False :
		print("ERROR : 数据表{0}不存在".format(table_name))
		return 0

	# 检查表头是否存在
	table_info = function.get_table_info(tmp_table_path)
	if table_info == False :
		return 0

	# 检查数据是否 符合表的结构
	for x in data : 
		if function.check_data_with_table_format(tmp_table_path,x) == False:
			return 0
	# 尝试写入数据
	try:
		if os.path.isfile(tmp_table_path) == True :
			with open(tmp_table_path,"a") as f :
				for x in data:
					f.write(json.dumps(x) + "\n")
				print("数据插入成功")
		else:
			print("ERROR : 数据表{0}不存在".format(table_name))
	except Exception as e:
		print("ERROR : " + e)
		pass

def delete_from_table(table_name,where):
	'''
	where 为条件 格式为字典类型 如 {"id":[">","3"],"name":["=","张三"]}
	'''
	tmp_table_path = env.CURRENT_PATH + "/" + table_name + ".json"
	# 获取表头信息
	table_info = function.get_table_info(tmp_table_path)
	if table_info == False:
		return False
	table_info = json.loads(table_info)

	# 查询
	res = function.table_where(tmp_table_path,where)
	if res == False:
		return 0

	# 获取表中所有数据
	data = function.get_all_data_from_table(tmp_table_path)
	if data == False :
		return False

	# 判断是否于原表数据一样
	if res == data:
		print("ERROR : 无可满足条件的数据")
		return 0
	try:
		with open(tmp_table_path,"w") as f:
			f.write(json.dumps(table_info) + "\n")
			for x in data:
				if x not in res: 
					f.write(json.dumps(x) + "\n")
			print("删除成功")
	except Exception as e:
		raise e

def select_from_table(table_name,columns,where):
	'''
	columns 格式为 [column1,column2]
	where 为条件 格式为字典类型 如 {"id":[">","3"],"name":["=","张三"]}
	'''
	tmp_table_path = env.CURRENT_PATH + "/" + table_name + ".json"

	# 查询
	res = function.table_where(tmp_table_path,where)
	if res == False:
		return 0

	# 获取表结构
	table_info = function.get_table_info(tmp_table_path)
	if table_info == False :
		return 0
	table_info = json.loads(table_info)

	header_data = []
	res_tmp = []
	# 按列筛选
	if "*" == columns[0]:
		for x in table_info:
			header_data.append(x)
	else:
		# 过滤表头
		for x in table_info:
			if x in columns :
				header_data.append(x)
		# 过滤数据
		for x in res:
			tmp_dict = {}
			for column in  x :
				if column in columns :
					tmp_dict.update({column : x[column]})
			res_tmp.append(tmp_dict)

		res = res_tmp

	function.console_print(header_data,res)

def update_from_table(table_name,set_rule,where):
	'''
	set格式   set name = xxx ,id = xx  转化为 {"name":"xxxx","id":"xxxx"}
	'''
	tmp_table_path = env.CURRENT_PATH + "/" + table_name + ".json"

	if os.path.isfile(tmp_table_path) == False :
		print("ERROR : 数据表{0}不存在".format(table_name))
		return 0

	# 检查表头是否存在
	table_info = function.get_table_info(tmp_table_path)
	if table_name == False :
		return 0
	table_info = json.loads(table_info)

	# 筛选满足条件的记录
	res = function.table_where(tmp_table_path,where)
	if res == False :
		return 0

	# 获取所有记录
	data = function.get_all_data_from_table(tmp_table_path)
	if data == False :
		return 0

	# 记录未被修改的数据
	tmp_dict = []
	for x in data :
		if x not in res :
			tmp_dict.append(x)

	
	# 对res 的结果按照 set 规则进行修改
	# 检测列是否存在
	for x in set_rule:
		if x not in table_info:
			print("ERROR : set 中列{0}不存在".format(x))
			return 0

	# 属性修改
	for x in set_rule :
		column = x
		value = set_rule[x]
		i = 0
		while i< len(res) :
			res[i][column] = value
			i = i + 1

	# 将修改结果保存到数据库
	try:
		with open(tmp_table_path,"a") as f :
			f.truncate(0)
			f.write(json.dumps(table_info) + "\n")
			for x in res :
				f.write(json.dumps(x) + "\n")
			for x in tmp_dict:
				f.write(json.dumps(x) + "\n")
			print("数据修改成功")
	except Exception as e:
		raise e

def desc_from_table(table_name):
	'''
	打印 表结构
	'''
	if env.CURRENT_DB == "":
		print("ERROR : 未选择数据库")
		return 0

	tmp_table_path = env.CURRENT_PATH + "/" + table_name + ".json"
	# 获取表结构
	table_info = function.get_table_info(tmp_table_path)
	if table_info == False :
		return 0
	table_info = json.loads(table_info)

	res = []
	for x in table_info:
		res.append({"Field":x,"Type":table_info[x]})

	function.console_print(["Field","Type"] ,res)

def show_databases():

	try:
		db_list = os.listdir(env.DB_PATH)
		if len(db_list) == 0 :
			print("ERROR : 暂无数据库")
			return 0
	except Exception as e:
		print("ERROR : 暂无数据库")
	
	res = []
	for x in db_list:
		res.append({"Database":x})

	function.console_print(["Database"] ,res)

def show_tables():
	'''
	查看数据库中表的信息
	'''
	if env.CURRENT_DB == "":
		print("ERROR : 未选择数据库")
		return 0
	table_list = os.listdir(env.CURRENT_PATH)

	res = []
	for x in table_list :
		res.append({"Tables_in_{0}".format(env.CURRENT_DB) : x.split(".")[0]})
	
	function.console_print(["Tables_in_{0}".format(env.CURRENT_DB)],res)


def select_version():
	'''
	查看数据库版本
	'''
	if env.VERSION == "" :
		print("ERROR : 环境错误")

	function.console_print(["version"],[{"version":env.VERSION}])
