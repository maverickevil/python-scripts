# Serve

> 使用 `flask_restful` 库风格快速编写轻量级后端 `WEB` 项目，下面提供三种部署 `WSGI` 项目的方案

## 运行方式

### 开发/测试：Develop 模式

![image](https://user-images.githubusercontent.com/58482090/199562435-5ff456ab-dce8-4591-addb-167a533f729e.png)

```shell
# 开发者模式运行，不产生pyc缓存文件
root@web-server:/serve# python3 -B app.py

# 安装命令
root@web-server:/serve# apt-get install curl jq

# 测试请求
root@web-server:/serve# curl -s http://127.0.0.1/api/test | jq .
```

### 预发布：Gunicorn 启动

![image](https://user-images.githubusercontent.com/58482090/199562838-8bc81c39-29c5-451d-9570-fcf3bbef0f64.png)

```shell
root@web-server:/serve# shell/start.sh 

  已成功启动服务！

root@web-server:/serve# shell/stop.sh 

  已停止全部服务！
```

### 生产: Supervisor 托管

`Flask` + `Gunicorn` + `Supervisor` + `Nginx` 部署 `Prod` 环境


