#!/usr/bin/env bash

#  尝试查杀Gunicorn进程
ps aux | awk '/gunicorn/{if ($0!~/awk/) system("kill -9 "$2)}' && \
  echo -e "\033[31m\n  已停止全部服务！\n\033[0m"


#EOF
