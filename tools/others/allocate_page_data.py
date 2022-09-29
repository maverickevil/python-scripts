# -*- coding: utf-8 -*-
import logging

# 终端输出DEBUG级别+
logging.getLogger().setLevel(logging.DEBUG)


def pagination(data: list, page=1, limit=20):
    is_last_page = False

    # 判断类型
    if not isinstance(data, list):
        logging.warning("[说明] data 类型错误")
        return None
    if not isinstance(page, int):
        logging.warning("[说明] page 类型错误")
        return None
    if not isinstance(limit, int):
        logging.warning("[说明] limit 类型错误")
        return None

    # 判断limit值是否有效
    length = len(data)
    if limit < 1 or limit > length:
        logging.warning("[说明] limit 值无效")
        return None

    # 判断page值是否有效
    count = length // limit
    if page < 1 or page > count:
        if (count + 1 == page) and ((page - 1) * limit < length):
            is_last_page = True
        else:
            logging.warning("[说明] page 值无效")
            return None

    logging.debug(f"[提示] page: {page} | limit: {limit}")

    # 取值
    start = (page - 1) * limit
    if is_last_page:
        result = data[start:]
    else:
        end = page * limit
        result = data[start:end]
    logging.info(f"[分页] {result}")
    return result


if __name__ == '__main__':
    # 模拟1-50的数据
    directory = list(range(1, 51))

    # 第1页（整页数据）
    p1 = pagination(directory, 1, 20)
    # 第2页（整页数据）
    p2 = pagination(directory, 2, 20)
    # 第3页（不足整页）
    p3 = pagination(directory, 3, 20)
    # 第4页（超出页码）
    p4 = pagination(directory, 4, 20)

    print(p1)
    print(p2)
    print(p3)

"""
DEBUG:root:[提示] page: 1 | limit: 20
INFO:root:[分页] [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
DEBUG:root:[提示] page: 2 | limit: 20
INFO:root:[分页] [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]
DEBUG:root:[提示] page: 3 | limit: 20
INFO:root:[分页] [41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
WARNING:root:[说明] page 值无效
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
[21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]
[41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
"""
