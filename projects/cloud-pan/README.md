## cloud-pan

> Project :  A simple personal network cloud disk system based on TCP protocol.

### 1. Client Demo

#### 1-1. preparations
* view the directory structure of the client: 
![image](https://user-images.githubusercontent.com/58482090/164915007-d1e97807-bddc-4d9a-9388-07426b9118d7.png)
* modify the configuration file: 
![image](https://user-images.githubusercontent.com/58482090/164915015-7a73c68c-314d-4d91-bbd7-c5e299d863ad.png)

#### 1-2. Running Client
* server connectivity verification: 
    + if modified settings.py file. Press enter to skip this step; 
    + or enter connect ip:port command; 
![image](https://user-images.githubusercontent.com/58482090/164915110-84f69977-77dc-4786-a3b6-567725328c0c.png)
* go to the homepage menu: 
    + 1-register; 
    + 2-login;
![image](https://user-images.githubusercontent.com/58482090/164915156-5534a914-ca22-473f-9402-8b8aa2fb7e65.png)
* register an account: 
    + the server returns the 10-digit random password of the account; 
    + initialize the user's home directory on the server;
![image](https://user-images.githubusercontent.com/58482090/164915175-bba4ce41-f6c2-49a5-842b-02e9380e1924.png)
* logon account: 
    + if the input is incorrect for more than three times, the account will be locked for 10 seconds;
![image](https://user-images.githubusercontent.com/58482090/164915191-570e82e5-6206-43e9-98c9-855020676236.png)
* log on to the cloud disk system: 
    + internal Implementation: C/S interacts data through Json, and Auth carries the authentication Token;
![image](https://user-images.githubusercontent.com/58482090/164915214-ce90acff-3ba2-4b07-8c73-b74d8ec8c4c4.png)


### 2. Client Commands
* the following commands are supported: 
  | **Commands**                         | **Description**        |
  | ------------------------------------ | ---------------------- |
  | `ls`, `ll`, `ls -l`                  | List objects (Details) |
  | `cls`, `clear`                       | Clear the screen       |
  | `put {local_file} `                  | Upload file            |
  | `get {remote_file}`                  | Download file          |
  | `help`, `man`, `info`, `?`           | Get help               |
  | `logout`                             | Exit account           |
  | `exit()`                             | Exit program           |


### 3. API Design Documentation

#### 3-1. Register module

* Client Request Data

```json
{
    "method": "register",
    "data": {
        "username": "admin"
    }
}
```

* Server Response Return

```json
// Example 1
{
    "status": "success",
    "msg": "User registration is successful.",
    "data": {
        "username": "admin",
        "password": "123456"
    }
}
// Example 2
{
    "status": "failed",
    "msg": "The username is already occupied, registration failed.",
    "data": {}
}
```

#### 3-2. Login module

* Client Request Data

```json
{
    "method": "login",
    "data": {
        "username": "admin",
        "password": "123456"
    }
}
```

* Server Response Return

```json
// Example 1
{
    "status": "success",
    "msg": "Successfully logged in to the system ~",
    "data": {
        "username": "admin",
        "token": ".W!f1_xpXzA3-gRsodNSBc?$Ll@5mH=="
    }
}
// Example 2
{
    "status": "failed",
    "msg": "Account or password do not match!",
    "data": {}
}
```

#### 3-3. Filelist module

* Client Request Data

```json
{
    "method": "filelist",
    "data": {
        "cookie": {
            "username": "admin",
            "token": ".W!f1_xpXzA3-gRsodNSBc?$Ll@5mH=="
        }
    }
}
```

* Server Response Return

```json
// Example 1
{
    "status": "success",
    "msg": "List files in admin space.",
    "data": {
        "filelist": ['createdb.sql', 'demo.txt', 'hello.go', 'idrac.sh', 'index.html', 'pip-22.0.4.tar.gz'],
        "counts": 6,
        "f_bsize_list": [['createdb.sql', 1556], ['demo.txt', 40], ['hello.go', 16630], ['idrac.sh', 43484], ['index.html', 42406], ['pip-22.0.4.tar.gz', 5118513]]
    }
}
// Example 2
{
    "status": "success",
    "msg": "List files in admin space.",
    "data": {
        "filelist": "[]",
        "counts": 0
    }
}
// Example 3
{
    "status": "failed",
    "msg": "This is an illegal login.",
    "data": {}
}
```

#### 3-4. Upload module

* Client Request Data

```json
{
    "method": "putfile",
    "data": {
        "cookie": {
            "username": "admin",
            "token": ".W!f1_xpXzA3-gRsodNSBc?$Ll@5mH=="
        },
        "upload": "C:\Users\ever\Desktop\demo.py",
        "overwrite": True
    }
}
```

* Server Response Return

```json
// Example 1
{
    "status": "success",
    "msg": "The uploader task is ready.",
    "data": {
        "listenport": 14398,
        "savepath": "/opt/project/cloud-pan/server/space/admin/demo.py"
    }
}
// Example 2
{
    "status": "failed",
    "msg": "The file already exists.",
    "data": {}
}
```

#### 3-5. Download module

* Client Request Data

```json
{
    "method": "getfile",
    "data": {
        "cookie": {
            "username": "admin",
            "token": ".W!f1_xpXzA3-gRsodNSBc?$Ll@5mH=="
        },
        "rfilepath": "hello.go",
        "lfilesize": 16630,
        "resume": True
    }
}
```

* Server Response Return

```json
// Example 1
{
    "status": "success",
    "msg": "The downloader task is ready.",
    "data": {
        "listenport": 13268,
        "mode": "ab",
        "seek": 3660
    }
}
// Example 2
{
    "status": "failed",
    "msg": "The file is not exists.",
    "data": {}
}
```

