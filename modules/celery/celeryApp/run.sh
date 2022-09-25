#!/usr/bin/env bash
# shellcheck disable=SC2009,SC2039,SC2046,SC2126,SC2155

set -o nounset
export LANG=en_US.UTF-8

declare symbols=$(perl -e "print '#' x 30;")
declare cur_dir=$(dirname $(readlink -f "$0"))
declare base_dir=$(dirname "${cur_dir}")

# 启动worker的进程数
declare forks=5

cd "${base_dir}" || exit 0

function check_clean() {
    # 检查当前进程状态
    process=$(ps -ef | grep -i 'celery' | grep -v 'grep' | wc -l)
    if [ "${process}" -gt 0 ]; then
        ps -ef | grep -i 'celery' | grep -v 'grep' | awk '{print $2}' | xargs kill -9
    fi

    # 清除残余文件目录
    rm -rf "${cur_dir}"/{__pycache__,logs}
}

function start_app() {
    # 检查清除残余进程
    check_clean

    # 启动多工作进程，以守护进程的模式运行
    # 注意：pidfile和logfile必须以绝对路径来声明
    clear
    test -d "${cur_dir}"/logs/ || mkdir -p "${cur_dir}"/logs/
    for n in $(seq 1 ${forks});
    do
        "${cur_dir}"/.venv/bin/celery multi start worker -A celeryApp.main -E \
        --pidfile="${cur_dir}/logs/worker${n}.pid" \
        --logfile="${cur_dir}/logs/celery.log" -l info -n "worker${n}"
    done

    # 打印输出结果
    echo -e "\n${forks} asynchronous celery worker process tasks started.\n"
    echo -e "[ command ]\n  ps aux | grep -i 'celery' | grep -v 'grep'\n"
    echo -e "[ monitor ]\n  tail -f logs/celery.log\n"
    echo -e "[ async ]\n  python3 ./call.py\n"
    exit 0
}

function stop_app() {
    # 停止多工作进程（与子线程）
    clear
    for n in $(seq 1 ${forks});
    do
        "${cur_dir}"/.venv/bin/celery multi stop worker -A celeryApp.main \
        --pidfile="${cur_dir}/logs/worker${n}.pid" \
        --logfile="${cur_dir}/logs/celery.log"
    done

    # 检查清除残余进程
    check_clean

    # 打印输出结果
    echo -e "\nAll celery worker process tasks have ended.\n"
    exit 0
}

function main() {
    while true
    do
        clear
        echo -e "${symbols}\n\tPlease choose:\n\t 1. start app\n\t 2. stop app\n${symbols}"
        read -r select
        case ${select} in
            1)
                start_app
            ;;
            2)
                stop_app
            ;;
            *)
                echo -e "\nInput error !\n"
                sleep 1
            ;;
        esac
    done
}
main

#EOF