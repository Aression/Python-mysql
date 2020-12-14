import lib.core.function as function
import lib.core.base as db
import re

def parseSql(sql):
	
	sql = sql.strip()
	sql = re.sub(" +"," ",sql)
	print(sql)