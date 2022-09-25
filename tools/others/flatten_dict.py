
class FlattenDict(object):
    """
    Flatten nested dictionaries, compressing keys
    https://stackoverflow.com/questions/6027558/flatten-nested-dictionaries-compressing-keys/6027615#6027615
    https://www.freecodecamp.org/news/how-to-flatten-a-dictionary-in-python-in-4-different-ways/
    """

    container = []

    def __new__(cls, *args, **kwargs):
        if cls.container:
            cls.container.clear()
        return super(FlattenDict, cls).__new__(cls)

    def __init__(self, d: dict, prefix='top'):
        self.data = d
        self.prefix = prefix
        for k, v in globals().items():
            if v == d:
                self.prefix = k

    def _deepdict(self, value, key=None, sep='.', prefix=''):
        if isinstance(value, dict):
            for k, v in value.items():
                s = f"{prefix}{sep}{k}"
                self._deepdict(v, key=k, prefix=s)

        if isinstance(value, list):
            _exec = lambda line: eval(
                f"{line.split('.')[0]}" + "".join([f".get('{x}')" for x in line.split('.')[1:]]))
            if not _exec(prefix) and type(key):
                self.container.append({prefix: value})
            n = 1
            for y in value:
                if not isinstance(y, dict):
                    self.container.append({prefix: y})
                else:
                    for k, v in y.items():
                        s = f"{prefix}{sep}{n}{sep}{k}"
                        self._deepdict(v, key=k, prefix=s)
                n += 1

        if isinstance(value, (str, int, type(None))):
            # print(f"'{prefix}': '{value}'")
            self.container.append({prefix: value})

    @property
    def generator(self):
        try:
            self._deepdict(self.data, prefix=self.prefix)
            for z in self.container:
                yield z
        except Exception as e:
            raise TypeError(f"Unsupported dictionary type resolution.\n\tReason: {e}")

    @property
    def result(self):
        tuple_data = []
        self._deepdict(self.data, prefix=self.prefix)
        for item in self.container:
            tuple_data.append((".".join(list(item.keys())[0].split('.')[1:]), list(item.values())[0]))
        return tuple_data


if __name__ == '__main__':
    # 原始数据
    json_data = {
        "project": {
            "id": 50,
            "name": "City Central Business District Planning Project",
            "type": "Construction",
            "site": {
                "name": "Shopping Center",
                "code": "CN-xxx-034",
                "count": 30000
            },
            "contact": {
                "Responsible": {
                    "company": "Wanda",
                    "phone": "010-xxxx-xxxx"
                },
                "Delivery": {
                    "name": "Li Ming",
                    "phone": "086-139xxxx1234"
                }
            }
        },
        "detail": {
            "infrastructure": [
                {
                    "system": "personnel, merchant, client"
                },
                {
                    "services": "shopping, entertainment, cinema"
                }
            ]
        }
    }

    # 将多层级字典转换成平铺式key单层字典
    data = FlattenDict(json_data)
    for i in data.generator:
        print(i)

"""
效果如下：
{'json_data.project.id': 50}
{'json_data.project.name': 'City Central Business District Planning Project'}
{'json_data.project.type': 'Construction'}
{'json_data.project.site.name': 'Shopping Center'}
{'json_data.project.site.code': 'CN-xxx-034'}
{'json_data.project.site.count': 30000}
{'json_data.project.contact.Responsible.company': 'Wanda'}
{'json_data.project.contact.Responsible.phone': '010-xxxx-xxxx'}
{'json_data.project.contact.Delivery.name': 'Li Ming'}
{'json_data.project.contact.Delivery.phone': '086-139xxxx1234'}
{'json_data.detail.infrastructure.1.system': 'personnel, merchant, client'}
{'json_data.detail.infrastructure.2.services': 'shopping, entertainment, cinema'}
"""
