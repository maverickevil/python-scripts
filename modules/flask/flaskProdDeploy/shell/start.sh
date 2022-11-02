#!/usr/bin/env bash
set -u
export LANG=en_US.UTF-8
curdir=`dirname $(readlink -f $0)`
basedir=`dirname $curdir`"/"

#############################
##                         ##
##  部署独角兽WEB服务项目  ##
##                         ##
#############################


# 不生成pyc编译文件
export PYTHONDONTWRITEBYTECODE=1


# 启动配置项
config_file="gunicorn.config.py"
module_name="app"
instance_name="app"


# 启动服务
which gunicorn &> /dev/null
if [ $? -eq 0 ]; then
    # 查看当前Gunicorn存在的进程数
    p_count=$(ps -ef | grep -c "gunicorn")
    if [ ${p_count} -gt 1 ]; then
        # 若存在残余进程，先杀掉
        ps aux | grep "gunicorn" | grep -v "grep" | awk '{print $2}' | xargs kill -9
    fi
    # 挂后台，不产生nohup.out日志
    cd ${basedir} && \
      nohup gunicorn ${module_name}:${instance_name} -c ${config_file} 1>/dev/null 2>&1 &
    echo -e "\033[32m\n  已成功启动服务！\n\033[0m"
else
    echo -e "\033[33m\n  未找到该模块命令！\n\033[0m"
fi


#EOF
