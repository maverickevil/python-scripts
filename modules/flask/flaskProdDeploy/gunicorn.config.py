## ��ϸ�ο� https://docs.gunicorn.org/en/latest/configure.html

# ��־����
glevel = "debug"

# ���÷�����־�ʹ�����Ϣ��־·��
accesslog = './logs/access.log'
errorlog = './logs/error.log'

# ���й���������
workers = 4

# ���ó�ʱʱ�䣨Ĭ��30s��
timeout=60

# �����ػ�����
daemon = True

# ���ù���ģʽΪЭ�̣���������ģ�飩
worker_class = "gevent"

# ��ip�ͼ����˿�
bind = "0.0.0.0:8000"

