## celeryApp

### Celery 布式异步任务队列框架


### 运行
- 守护服务
``` Bash
[admin@localhost ~]$ ./run.sh
##############################
	Please choose:
	 1. start app
	 2. stop app
##############################
1
celery multi v5.2.7 (dawn-chorus)
> Starting nodes...
	> worker@worker1: OK
celery multi v5.2.7 (dawn-chorus)
> Starting nodes...
	> worker@worker2: OK
celery multi v5.2.7 (dawn-chorus)
> Starting nodes...
	> worker@worker3: OK
celery multi v5.2.7 (dawn-chorus)
> Starting nodes...
	> worker@worker4: OK
celery multi v5.2.7 (dawn-chorus)
> Starting nodes...
	> worker@worker5: OK

5 asynchronous celery worker process tasks started.

[ command ]
  ps aux | grep -i 'celery' | grep -v 'grep'

[ monitor ]
  tail -f logs/celery.log

[ async ]
  python3 ./call.py
```

- 异步任务
``` Bash
[admin@localhost ~]$ python3 call.py
b172d286-74d4-41bd-b9b0-1931896be148
986ff699-5460-4153-81bc-1249c67b12fb
f2200ede-f336-4f39-a173-d2d449cb292b
26b82e06-dc04-40b8-8e02-1f19f80cd431
f8d170e6-7d51-4aa8-b4b8-290a7d9f3798
f8d170e6-7d51-4aa8-b4b8-290a7d9f3798
PENDING
等待任务，阻塞中...
True
all done!
```

### 使用 redis 作为消息队列
![image](https://user-images.githubusercontent.com/58482090/191494049-77b64196-a3f7-4129-97f8-cf19d986b85d.png)
