from gevent import monkey
monkey.patch_all()
import multiprocessing

## 详细参考 https://docs.gunicorn.org/en/latest/configure.html

# debug = True               # 开发者调试模式，生产关闭

# 日志级别
loglevel = 'debug'

# 绑定ip和监听端口
bind = '127.0.0.1:8000'      # 绑定与Nginx通信的端口

# 设置pid文件
pidfile = 'logs/gunicorn.pid'

# 设置日志路径
accesslog = 'logs/access.log'
errorlog = 'logs/error.log'

# 设置守护进程
daemon = True                # 若直接使用Gunicorn来管理，需启用该选项; 若使用Supervisor来管理的话，需要注释该选项

# 并行工作进程数
workers = multiprocessing.cpu_count() * 2 + 1

# 设置工作模式为协程
worker_class = 'gevent'      # 默认为阻塞模式，最好选择Gevent模式（三方模块）

# 设置超时时间
timeout = 60                 # 默认30s

