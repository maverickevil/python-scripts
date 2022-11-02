## 详细参考 https://docs.gunicorn.org/en/latest/configure.html

# 日志级别
glevel = "debug"

# 设置访问日志和错误信息日志路径
accesslog = './logs/access.log'
errorlog = './logs/error.log'

# 并行工作进程数
workers = 4

# 设置超时时间（默认30s）
timeout=60

# 设置守护进程
daemon = True

# 设置工作模式为协程（依赖三方模块）
worker_class = "gevent"

# 绑定ip和监听端口
bind = "0.0.0.0:8000"

