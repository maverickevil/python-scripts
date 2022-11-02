#!/usr/bin/env bash
set -u
export LANG=en_US.UTF-8
curdir=`dirname $(readlink -f $0)`
basedir=`dirname $curdir`"/"

#############################
##                         ##
##  ���������WEB������Ŀ  ##
##                         ##
#############################


# ������pyc�����ļ�
export PYTHONDONTWRITEBYTECODE=1


# ����������
config_file="gunicorn.config.py"
module_name="app"
instance_name="app"


# ��������
which gunicorn &> /dev/null
if [ $? -eq 0 ]; then
    # �鿴��ǰGunicorn���ڵĽ�����
    p_count=$(ps -ef | grep -c "gunicorn")
    if [ ${p_count} -gt 1 ]; then
        # �����ڲ�����̣���ɱ��
        ps aux | grep "gunicorn" | grep -v "grep" | awk '{print $2}' | xargs kill -9
    fi
    # �Һ�̨��������nohup.out��־
    cd ${basedir} && \
      nohup gunicorn ${module_name}:${instance_name} -c ${config_file} 1>/dev/null 2>&1 &
    echo -e "\033[32m\n  �ѳɹ���������\n\033[0m"
else
    echo -e "\033[33m\n  δ�ҵ���ģ�����\n\033[0m"
fi


#EOF
