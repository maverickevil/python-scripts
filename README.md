# Scripts

## Table of contents

1. [`modules`](https://github.com/PokeyBoa/python-scripts/tree/master/modules)
2. [`projects`](https://github.com/PokeyBoa/python-scripts/tree/master/projects)
3. [`tools`](https://github.com/PokeyBoa/python-scripts/tree/master/tools)


## Store some daily scripts (utils class)

| 文件名 | 功能描述 | 实现概述 |
| --- | --- | --- |
| [`mongo_ops.py`](https://github.com/PokeyBoa/python-scripts/blob/master/tools/database/mongo_ops.py) | 非关系型数据库工具类 | 针对MongoDB的CURD基本操作封装 |
| [`mysql_context.py`](https://github.com/PokeyBoa/python-scripts/blob/master/tools/database/mysql_context.py) | Ⅰ. 数据库连接池SQL操作类 | 通过类的__enter__, __exit__方法实现with上下文管理 |
| [`mysql_singleton.py`](https://github.com/PokeyBoa/python-scripts/blob/master/tools/database/mysql_singleton.py) | Ⅱ. 数据库连接池SQL操作类 | 通过类的单例模式和装饰器实现 |
| [`app_generator.py`](https://github.com/PokeyBoa/python-scripts/blob/master/tools/common/app_generator.py) | 生成随机字符串 | 实现了类的__str__, __dict__和__call__的魔法方法 |
| [`requests_auth.py`](https://github.com/PokeyBoa/python-scripts/blob/master/tools/common/requests_auth.py) | 生成Basic/Bearer的认证令牌 | 新增requests.auth的相应实例方法 |
| [`interval.py`](https://github.com/PokeyBoa/python-scripts/blob/master/tools/others/interval.py) | 比较数字的范围, 并为区间定义一个别名 | 重载pandas.Interval模块的__init__初始化方法 |
| [`dell_assets.py`](https://github.com/PokeyBoa/python-scripts/blob/master/tools/others/dell_assets.py) | 查询Dell PowerEdge服务器维保信息 | 使用单例模式实例化类, 以及单例的类方法 |
| [`orm_stract.py`](https://github.com/PokeyBoa/python-scripts/blob/master/modules/django/models/orm_stract.py) | Django ORM的通用基类模型 | 重写query_set查询集对象的update方法 |
| [`flatten_dict.py`](https://github.com/PokeyBoa/python-scripts/blob/master/tools/others/flatten_dict.py) | 转化为平铺展开的字典格式 | 通过Recursive函数与Generators将多层级Dict转为Flatten Dict |


