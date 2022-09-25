from pymongo import MongoClient


class MongoOperation(object):

    """ mongodb basic curd operation tool class """

    def __init__(self, host=None, port=27017, username=None, password=None, db_name=None):
        self.collection = None
        self.host = host
        self.port = int(port)
        self.username = username
        self.password = password
        self.db_name = db_name
        self.handle, self.client = self.get_db_handle

    @property
    def get_db_handle(self):
        # 数据库建连
        client_obj = MongoClient(
            username=self.username,
            password=self.password,
            host=self.host,
            port=self.port
        )
        db_handle = client_obj[self.db_name]
        return db_handle, client_obj

    @property
    def list_all_collection(self):
        # 列出所有集合
        res = [item.get('name') for item in self.handle.list_collections()]
        return res or None

    def exist_collection(self, collection_name=None):
        # 集合是否存在
        res = self.list_all_collection
        return True if res is not None and collection_name in res else False

    def _get_collection(self, collection_name=None):
        # 进入或创建一个集合
        self.collection = self.handle[collection_name]
        return self.collection

    def del_collection(self, collection_name=None):
        # 销毁一个集合
        self._get_collection(collection_name)
        self.collection.drop()
        return True

    def insert_data(self, collection_name=None, data=None):
        self._get_collection(collection_name)
        if isinstance(data, dict):
            self.collection.insert_one(data)
            return True
        if isinstance(data, list) and len(data) > 1:
            for el in data:
                if not isinstance(el, dict):
                    raise TypeError('Check data type')
            self.collection.insert_many(data, ordered=True)
            return True
        raise TypeError('Check data type')

    def select_all(self, collection_name=None):
        self._get_collection(collection_name)
        res = [item for item in self.collection.find()]
        return res or None

    def select_one(self, collection_name=None, filter=None):
        self._get_collection(collection_name)
        if filter is None:
            return self.collection.find_one()
        if isinstance(filter, dict):
            return self.collection.find_one(filter)
        if isinstance(filter, str):
            from bson.objectid import ObjectId
            return self.collection.find_one({'_id': ObjectId(filter)})


def unit_test():
    db = MongoOperation(
        db_name="dev-mongo",
        host="10.0.71.101",
        username="dev-mongo",
        password="OyesmRmyQTxI2NolXyxIgMR0"
    )

    print(db.list_all_collection)

    exist = db.exist_collection("userinfo")
    print(exist)

    d1 = [
        {
            '_id': 'U1006001',
            'name': 'LiMing',
            'age': 18,
            'sex': 'Male'
        }, {
            '_id': 'U1006002',
            'name': 'LinHong',
            'age': 16,
            'sex': 'Female',
            'study': {
                'IT': {
                    'subjects': ['os', 'net', 'vm'],
                }
            }
        }
    ]

    d2 = {
        'name': 'Mary',
        'age': 16,
        'sex': 'Female'
    }

    db.del_collection("userinfo")

    db.insert_data(collection_name="userinfo", data=d1)
    db.insert_data(collection_name="userinfo", data=d2)

    s0 = db.select_all("userinfo")
    print(s0)

    s1 = db.select_one("userinfo")
    print(s1)

    s2 = db.select_one("userinfo", {"age": 16})
    print(s2)

    s3 = db.select_one("userinfo", "6310d89828123c31e7b6c9d6")
    print(s3)


if __name__ == '__main__':
    unit_test()

"""
Demo运行结果: 
['userinfo']
True
[{'_id': 'U1006001', 'name': 'LiMing', 'age': 18, 'sex': 'Male'}, {'_id': 'U1006002', 'name': 'LinHong', 'age': 16, 'sex': 'Female', 'study': {'IT': {'subjects': ['os', 'net', 'vm']}}}, {'_id': ObjectId('6310d89828123c31e7b6c9d6'), 'name': 'Mary', 'age': 16, 'sex': 'Female'}]
{'_id': 'U1006001', 'name': 'LiMing', 'age': 18, 'sex': 'Male'}
{'_id': 'U1006002', 'name': 'LinHong', 'age': 16, 'sex': 'Female', 'study': {'IT': {'subjects': ['os', 'net', 'vm']}}}
{'_id': ObjectId('6310d89828123c31e7b6c9d6'), 'name': 'Mary', 'age': 16, 'sex': 'Female'}
"""
