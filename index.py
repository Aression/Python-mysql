import lib.core.base as db
import lib.core.function as function
import lib.parse.SqlToCode as SqlToCode
import json
import os 


welcome = '''
__        __   _                            _        
\ \      / /__| | ___ ___  _ __ ___   ___  | |_ ___  
 \ \ /\ / / _ \ |/ __/ _ \| '_ ` _ \ / _ \ | __/ _ \ 
  \ V  V /  __/ | (_| (_) | | | | | |  __/ | || (_) |
   \_/\_/ \___|_|\___\___/|_| |_| |_|\___|  \__\___/ 
                                                     
 ____  ____  __  __ ____  
|  _ \| __ )|  \/  / ___| 
| | | |  _ \| |\/| \___ \ 
| |_| | |_) | |  | |___) |
|____/|____/|_|  |_|____/    -- version 1.0  help 命令查看帮助
                          
'''

if __name__ == '__main__':

	os.system('')
	print("\033[34m" + welcome + "\033[0m" )
	while True:
		try:
			
			sql = input("\033[32m数据库 >> \033[0m")
			print("")
			if len(sql) != 0:
				SqlToCode.parseSql(sql)
			print("")
		except Exception as e:
			print(e)
		
	