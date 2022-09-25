"""
# 比较数字的范围
### 方式一 ###
if 0 < num < 1000:
    size = "小"
elif 1000 < num < 5000:
    size = "中"
else:
    size = "大"
print(num, size)

### 方式二 ###
import interval

class ProInterval(interval.Interval):
    def __init__(self, start=-interval.Inf, end=interval.Inf, alias=None, **kwargs):
        self.alias = alias
        super(ProInterval, self).__init__(lower_bound=start, upper_bound=end, **kwargs)

bound = [
    ProInterval(0, 1000, alias='小'),
    ProInterval(1000, 5000, alias='中'),
    ProInterval(5000, 10000, alias='大'),
]

for item in bound:
    if num in item:
        print(num, item, item.alias)
        break
"""

import pandas as pd


class ProInterval(pd.Interval):
    """
    https://pandas.pydata.org/docs/reference/api/pandas.Interval.html
    """

    qualifiers = ('left', 'right', 'both', 'neither')

    def __init__(self, start=0, end=5, closed='right', alias=None, **kwargs):
        self.alias = alias

        import inspect
        arg_spec = inspect.getfullargspec(self.__class__)
        params = arg_spec.args
        params.pop(0)
        endpoints = params[0:2]
        for arg in endpoints:
            ep = eval(arg)
            if not isinstance(ep, int):
                raise TypeError("Only numeric (integer) is allowed when constructing an Interval.")

        bound = params[2]
        side = eval(bound)
        if side not in self.qualifiers:
            raise ValueError(f"invalid option for '{bound}': {side}")

        super(ProInterval, self).__init__(left=start, right=end, closed=closed, **kwargs)


def interval(number: int) -> tuple:
    scope = [
        ProInterval(start=0, end=300, closed='neither', alias='small'),
        ProInterval(start=300, end=3000, closed='left', alias='medium'),
        ProInterval(start=3000, end=50000, closed='both', alias='large'),
    ]
    for item in scope:
        if number in item:
            return number, item.alias
    return number, None


if __name__ == '__main__':
    """
      size [enum]
      1: small  < 300
      2: medium 300 - 3000
      3: large  > 3000
    """
    counts = 4096
    n1, v1 = interval(number=counts)
    print(n1, v1)           # 4096 large

    counts = 365
    n2, v2 = interval(number=counts)
    print(n2, v2)           # 365 medium
