"""
[Celery]
布式异步任务队列框架

[运行架构]
Celery 的运行架构由三部分组成，消息队列（message broker），任务执行单元（worker）和任务执行结果存储（task result store）组成。
一个 Celery 系统中可以包含多个 worker 和 broker。
Celery 本身不提供消息队列功能，但是可以很方便地和第三方提供的消息中间件进行集成，包括 Redis, RabbitMQ, RocketMQ, Kafka 等。

Tips：消息队列的数据结构（FIFO 先进先出）。
"""

import sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, f'{BASE_DIR}')

from celeryApp.worker.tasks import (
    no_args_no_ret,
    has_args_no_ret,
    no_args_has_ret,
    has_args_has_ret
)


"""
通过 delay() 进行异步调用任务，在 celery 的 worker 工作进程，只要有空闲的就会立刻执行。
使用 tailf 进行 log 查看
"""

# 例1. 无参数/无返回值的情况
res1 = no_args_no_ret.delay()
print(res1)

# 例2. 有参数/无返回值的情况
res2 = has_args_no_ret.delay(arg1='hello', arg2='world')
print(res2)

# 例3. 无参数/有返回值的情况
res3 = no_args_has_ret.delay()
print(res3)

# 例4. 有参数/有返回值的情况
res4 = has_args_has_ret.delay('你好', '👋👋👋')
print(res4)


"""
通过 apply_async() 让任务在后面指定时间后执行，时间单位：秒/s
任务名.apply_async(args=(参数1, 参数2), countdown=定时时间)
"""

# 例5. 延迟多长时间后再执行
result = has_args_has_ret.apply_async(kwargs={'arg1': 'Hello', 'arg2': 'Celery'}, countdown=5)
print(result)


"""
根据返回结果，不管delay，还是apply_async的返回结果都一样的，都是一串uuid类型。

[其他方法属性]
1. 查看任务的编码（实际是一串uuid）
obj.id

2. 查看任务的状态（枚举值：SUCCESS/PENDING）
obj.status

3. 查看任务执行结果（如果任务函数中没有return，则没有结果，如果结果未出现，则会导致阻塞）
obj.get()
"""

print(result.id)
print(result.status)
if result.status == "SUCCESS":
    print(f"成功：{result.get()}")

if result.status == "PENDING":
    print("等待任务，阻塞中...")
    print(result.get())

print("all done!")
