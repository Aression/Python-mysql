import lib.core.function as function
import lib.core.base as db
import re

def parseSql(sql):
	
	# sql 规范化 去首尾空格  将多个连续空格转一个
	sql = sql.split(";")[0]
	sql = sql.split("#")[0]
	sql = sql.strip()
	sql = re.sub(" +"," ",sql)

	sql_arr = sql.split(" ")
	operation =  sql_arr[0].lower()

	try:
		# show 命令操作
		if operation == "show" :
			operation1 = sql_arr[1].lower()
			if  operation1 == "databases" :
				db.show_databases()
			elif operation1 == "tables" :
				db.show_tables()
			else: 
				print("ERROR : 未知操作 {0}".format(operation1))
		# use 命令
		elif operation == "use" :
			operation1 = sql_arr[1].lower()
			db.select_db(operation1)
	
		# desc 查看表结构 
		elif operation == "desc" :
			operation1 = sql_arr[1].lower()
			db.desc_from_table(operation1)
	
		# 退出
		elif operation == "exit" or operation == "quit" :
			exit("bye~ \n")
	
		elif operation == "drop" :
	
			operation1 = sql_arr[1].lower()
			if operation1 == "table" :
				table_name = sql_arr[2].lower()
				db.drop_table(table_name)
			elif operation1 == "database":
				dbname = sql_arr[2].lower()
			else:
				print("ERROR : 未知操作 {0}".format(operation1))
	
		# 创建表 或者 库
		elif operation == "create":
			operation1 = sql_arr[1].lower()
			if operation1 == "database":
				db.create_db(sql_arr[2].lower())
			elif operation1 == "table":
				try:
					# 将字符串分割成 表名 和 列名+type
					table_name = sql_arr[2].split("(")[0]
					key_value = sql.split("(")[1].split(")")[0]
					# 将 列名与type 转化成json格式并放入 columns
					columns = {}
					for x in key_value.split(","):
						column = x.split(" ")[0]
						column_type = x.split(" ")[1]
						columns.update({column:column_type})
	
					if table_name != None or len(columns) :
						db.create_table(table_name,columns)
					else:
						print("ERROR : create 格式错误")
	
				except Exception as e:
					raise e
	except Exception as e:
		print("ERROR : SQL 解析错误")		
				