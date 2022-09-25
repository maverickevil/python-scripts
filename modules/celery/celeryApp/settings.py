"""
使用Redis作为消息队列（message broker）
"""

# 任务队列的链接地址
# redis没用户，置为空即可
broker_url = 'redis://:@127.0.0.1:6379/0'

# 结果队列的链接地址
# result_backend = 'redis://username:password@host:port/db'
result_backend = 'redis://:@127.0.0.1:6379/1'

