## 程序截图

![](https://blog-1300884845.cos.ap-shanghai.myqcloud.com/wenzhang/20201217204933.png)





![](https://blog-1300884845.cos.ap-shanghai.myqcloud.com/wenzhang/20201217204958.png)





![](https://blog-1300884845.cos.ap-shanghai.myqcloud.com/wenzhang/20201217205522.png)



![](https://blog-1300884845.cos.ap-shanghai.myqcloud.com/wenzhang/20201217205543.png)





## 项目结构

```
G:.
│  index.py
│  index.spec
│  README.md
│  requirements.txt
│
├─build  # 生成exe 需要的文件（自动生成的
│  └─index
│          Analysis-00.toc
│          base_library.zip
│          EXE-00.toc
│          index.exe.manifest
│          PKG-00.pkg
│          PKG-00.toc
│          PYZ-00.pyz
│          PYZ-00.toc
│          warn-index.txt
│          xref-index.html
│
├─data  #数据库存在位置
│  ├─diego
│  │      ttt.json
│  │      user1.json
│  │      users.json
│  │
│  ├─test
│  └─test1
│          bbb.json
│
├─dist  #生成的exe位置
│      index.exe
│
├─lib  # 代码
│  │  __init__.py
│  │
│  ├─core  #核心代码 用来实现基本功能
│  │  │  base.py
│  │  │  env.py
│  │  │  function.py
│  │  │  __init__.py
│  │  │
│  │  └─__pycache__
│  │          base.cpython-37.pyc
│  │          env.cpython-37.pyc
│  │          function.cpython-37.pyc
│  │          __init__.cpython-37.pyc
│  │
│  ├─parse  # sql 解析器  sql语言转 操作
│  │  │  SqlToCode.py
│  │  │  __init__.py
│  │  │
│  │  └─__pycache__
│  │          SqlToCode.cpython-37.pyc
│  │          __init__.cpython-37.pyc
│  │
│  └─__pycache__
│          __init__.cpython-37.pyc
│
└─__pycache__
        index.cpython-37.pyc
```





## 项目打包

生成exe

```bash
pyinstaller -F .\index.py
```



生成python 所需要的库(requirements.txt)

```bash
pipreqs --encoding utf8 ./
```

