#!/usr/bin/env bash

#  ���Բ�ɱGunicorn����
ps aux | awk '/gunicorn/{if ($0!~/awk/) system("kill -9 "$2)}' && \
  echo -e "\033[31m\n  ��ֹͣȫ������\n\033[0m"


#EOF
