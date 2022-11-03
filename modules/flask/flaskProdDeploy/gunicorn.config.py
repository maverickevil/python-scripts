from gevent import monkey
monkey.patch_all()
import multiprocessing

## ��ϸ�ο� https://docs.gunicorn.org/en/latest/configure.html

# debug = True               # �����ߵ���ģʽ�������ر�

# ��־����
loglevel = 'debug'

# ��ip�ͼ����˿�
bind = '127.0.0.1:8000'      # ����Nginxͨ�ŵĶ˿�

# ����pid�ļ�
pidfile = 'logs/gunicorn.pid'

# ������־·��
accesslog = 'logs/access.log'
errorlog = 'logs/error.log'

# �����ػ�����
daemon = True                # ��ֱ��ʹ��Gunicorn�����������ø�ѡ��; ��ʹ��Supervisor������Ļ�����Ҫע�͸�ѡ��

# ���й���������
workers = multiprocessing.cpu_count() * 2 + 1

# ���ù���ģʽΪЭ��
worker_class = 'gevent'      # Ĭ��Ϊ����ģʽ�����ѡ��Geventģʽ������ģ�飩

# ���ó�ʱʱ��
timeout = 60                 # Ĭ��30s

