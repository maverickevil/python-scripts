# -*- coding: utf-8 -*-
# @File   : client.py
# @Author : PokeyBoa
# @Date   : 2022/04/16 - 04/17
# @Desc   : Cloud Network Pan (client)
"""
Client socket conn: Blocking
Procedure realization: Functional programming + Dict types + Terminal input
"""

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import *
from datetime import datetime
import subprocess
import platform
import socket
import struct
import base64
import json
import time
import sys
import os
import re


# Define client-side global variables.
client = None
delay_sec = 1
form_width = 60
cmd_prompt = "[{%user%}@cloud-pan] $ "
auth_keys = {
    'username': None,
    'auth_token': None
}
err_times = {
    'menu': 1,
    'login': 1
}
title_slogan = {
    'index': ("#" * form_width + "\n#" + " " * (form_width-2) + "#\n#" + "Welcome to the Cloud-Pan System".center(form_width-2) + "#\n#" + " " * (form_width-2) + "#\n" + "#" * form_width),
    'login': ("#" * form_width + "\n#" + " " * (form_width-2) + "#\n#" + "Cloud-Pan System Login Menu".center(form_width-2) + "#\n#" + " " * (form_width-2) + "#\n" + "#" * form_width),
    'register': ("#" * form_width + "\n#" + " " * (form_width-2) + "#\n#" + "Cloud-Pan Account Register Menu".center(form_width-2) + "#\n#" + " " * (form_width-2) + "#\n" + "#" * form_width),
    'onboarding': ("#" * form_width + "\n#" + " " * (form_width-2) + "#\n#" + "Cloud-Pan System Onboarding".center(form_width-2) + "#\n#" + " " * (form_width-2) + "#\n" + "#" * form_width)
}


# Decorator
def cls_terminal(func):
    def inner(*args, **kwargs):
        clear()
        res = func(*args, **kwargs)
        return res
    return inner


def upload_file(source_path: str, port: int) -> bool:
    fclient = None
    try:
        fclient = socket.socket()
        fclient.connect((SERVER_IP, port))
        file_size = os.stat(source_path).st_size
        header = struct.pack('i', file_size)
        fclient.sendall(header)
        has_send_size = 0
        with open(source_path, mode='rb') as f:
            while has_send_size < file_size:
                chunk = f.read(2048)
                fclient.sendall(chunk)
                has_send_size += len(chunk)
        return True
    except:
        return False
    finally:
        fclient.close()


def download_file_progress(port, save_path, mode, chunk_size=1024, seek=0) -> bool:
    fclient = None
    try:
        fclient = socket.socket()
        fclient.connect((SERVER_IP, port))
        fclient.sendall(b' ')
        # 获取头部信息：数据长度
        has_read_size = 0
        bytes_list = []
        while has_read_size < 4:
            chunk = fclient.recv(4 - has_read_size)
            bytes_list.append(chunk)
            has_read_size += len(chunk)
        header = b"".join(bytes_list)
        data_length = struct.unpack('i', header)[0]
        # 获取数据
        file_object = open(save_path, mode=mode)
        file_object.seek(seek)
        has_read_data_size = 0
        while has_read_data_size < data_length:
            size = chunk_size if (data_length - has_read_data_size) > chunk_size else data_length - has_read_data_size
            chunk = fclient.recv(size)
            file_object.write(chunk)
            file_object.flush()
            has_read_data_size += len(chunk)
            percent = "\r{}%".format(int(has_read_data_size * 100 / data_length))
            print(percent, end="")
            time.sleep(0.5)
        print("")
        file_object.close()
        return True
    except:
        return False
    finally:
        fclient.close()


def local_save_path() -> str:
    # Linux OS
    if platform.system() == "Linux":
        home_dir = os.path.expanduser("~")
    # Windows or MacOS
    else:
        home_dir = os.path.join(os.path.expanduser("~"), 'Desktop')
    return home_dir


class SocketTrans(object):
    """
    Perform TCP protocol network transmission, send and receive network packets.
    """
    def __init__(self, conn):
        self.conn = conn

    def send_msg(self, content: str) -> None:
        """
        The data transmitted by the TCP protocol network to the peer.
        """
        data = content.encode('utf-8')
        header = struct.pack('i', len(data))
        self.conn.sendall(header)
        self.conn.sendall(data)

    @property
    def receive_msg(self) -> str:
        """
        The TCP protocol network transmits the data received from the peer.
        """
        # Waiting for callback result, Fixed header length (4 bytes)
        header = self.conn.recv(4)
        # Receive new network packets
        if header:
            # data byte length
            data_length = struct.unpack('i', header)[0]
            has_recv_len = 0
            result = b''
            # receive actual length
            while True:
                length = data_length - has_recv_len
                if length > 1024:
                    lth = 1024
                else:
                    lth = length
                chunk = self.conn.recv(lth)
                result += chunk
                has_recv_len += len(chunk)
                if has_recv_len == data_length:
                    break
            return result.decode('utf-8')
        else:
            return ''


def tcp_trans(content: dict, conn=client) -> dict:
    """
    A wrapper for the SocketTrans Class.
    """
    # get connected
    tcp = SocketTrans(conn)
    # convert dict to json format
    json_data = json.dumps(content)
    # send json data
    tcp.send_msg(json_data)
    # receive json data
    result = tcp.receive_msg
    # convert json to dict format
    data = json.loads(result)
    # return dict data
    return data


def cmdhelp(**kwargs) -> None:
    if kwargs.get('auth_token'):
        print("+--------------+-------------------------------------------+\n" +
              "| Command      |  Description                              |\n" +
              "|--------------+-------------------------------------------|\n" +
              "| ls, ll       |  List files of remote server.             |\n" +
              "| cls          |  Empty the entire terminal screen.        |\n" +
              "| put <lpath>  |  Upload a local file (absolute path).     |\n" +
              "| get <rpath>  |  Download a remote file (absolute path).  |\n" +
              "| help         |  View the command manual.                 |\n" +
              "+--------------+-------------------------------------------+\n" +
              "                                          [exit() / logout] \n")
    else:
        print("The current user is not authorized to view.")


def clear() -> None:
    """Clean screen across platforms"""
    if platform.system() == "Linux":
        subprocess.call("clear", shell=True)
    elif platform.system() == "Darwin":
        subprocess.call("export TERM=xterm-color; clear", shell=True)
    elif platform.system() == "Windows":
        subprocess.call("cls", shell=True)


def filelist(*args, **kwargs) -> list:
    """list files"""
    # assembly of data
    content = {
        'method': sys._getframe().f_code.co_name,
        'data': {
            'cookie': kwargs
        }
    }
    # network transmission and return data
    trans_data = tcp_trans(content, client)
    if trans_data.get('data').get('counts'):
        if args[0] == "ll":
            print(trans_data.get('msg'))
            for file in trans_data.get('data').get('filelist'):
                print("-rw-r--r--" + " " * 25 + file)
            print(f"{trans_data.get('data').get('counts')} rows in total")
        elif args[0] == "ls":
            for file in trans_data.get('data').get('filelist'):
                print(file, end=" ")
            print("", end="\n")
        # this conditional branch for getfile function
        elif args[0] == "__ls-Api-Function":
            return trans_data.get('data').get('f_bsize_list')
        return trans_data.get('data').get('filelist')
    else:
        if args[0] != "__ls-Api-Function":
            print("Home directory is empty.")
        return []


def putfile(*args, **kwargs) -> None:
    """upload files"""
    # basic syntax judgment (default: yes)
    choose = input("Whether to enable overwrite mode, if remote file already exists: [y/n] ")
    overwrite = False if (choose.lower() == 'n') else True
    # assembly of data
    content = {
        'method': sys._getframe().f_code.co_name,
        'data': {
            'cookie': kwargs,
            'upload': args[0],
            'overwrite': overwrite
        }
    }
    # network transmission and return data
    trans_data = tcp_trans(content, client)
    if trans_data['status'] == "success":
        # send_file
        res = upload_file(source_path=args[0], port=int(trans_data['data']['listenport']))
        if res:
            print("Task: upload completed.")
        else:
            print("Task: upload failed.")
    elif trans_data['status'] == "failed":
        print(trans_data['msg'])


def getfile(*args, **kwargs) -> None:
    """download file"""
    # get filename
    if (os.path.basename(args[0]) != args[0]):
        print("Path filling is not supported, only the base filename can be selected from 'ls'.")
        return
    # search file in remote filelist
    remote_fsizelist = filelist('__ls-Api-Function', **kwargs)
    if not remote_fsizelist:
        print("The home space is empty, the getfile method cannot be executed!")
        return
    real_filesize = 0
    # view real file size
    find_counts = 0
    for obj in remote_fsizelist:
        if obj[0] == args[0]:
            real_filesize = obj[1]
        else:
            find_counts += 1
    if len(remote_fsizelist) == find_counts:
        print("The file was not found in the home space!")
        return
    # get local filepath
    local_filepath = os.path.join(local_save_path(), args[0])
    # assembly of data
    content = {
        'method': sys._getframe().f_code.co_name,
        'data': {
            'cookie': kwargs,
            'rfilepath': args[0]
        }
    }
    # judging the size
    if real_filesize:
        if os.path.exists(local_filepath) and os.path.isfile(local_filepath):
            # local size (bytes)
            seek = os.stat(local_filepath).st_size
            if seek == real_filesize:
                print("The file exists locally, no need to download repeatedly.")
                return
            else:
                # basic syntax judgment (default: no)
                val = input("Whether to start the resume upload job: [y/n] ")
                if val.lower() == 'y':
                    # update assembly data
                    content.get('data').update({
                        'lfilesize': seek,
                        'resume': True
                    })
                else:
                    os.remove(local_filepath)
                    # update assembly data
                    content.get('data').update({
                        'lfilesize': 0,
                        'resume': False
                    })
        else:
            # update assembly data
            content.get('data').update({
                'lfilesize': 0,
                'resume': False
            })
    else:
        print("This is an empty file and the download will be pointless.")
        return
    # network transmission and return data
    trans_data = tcp_trans(content, client)
    if trans_data['status'] == "success":
        # recv_file
        res = download_file_progress(
            port=int(trans_data['data']['listenport']),
            save_path=local_filepath,
            mode=trans_data['data']['mode'],
            chunk_size=1024,
            seek=trans_data['data']['seek']
        )
        if res:
            print("\nTask: download completed.")
        else:
            print("\nTask: download failed.")


@cls_terminal
def onboarding(auth) -> None:
    """Cloud Pan System"""
    user = auth['username']
    # command line identifier
    ps1 = "[" + user + "@" + cmd_prompt.split('@')[-1]
    if user == "root":
        ps1 = ps1.replace("$", "#")
    function_dict = {
        "ls": filelist,
        "cls": clear,
        "put": putfile,
        "get": getfile,
        "help": cmdhelp
    }
    for item in auth.values():
        if user == item:
            print(title_slogan.get(sys._getframe().f_code.co_name) + "\n")
            cmdhelp(**auth)
            break
    while True:
        command = input(ps1)
        # exit the program
        if command == "exit()":
            print("\n  Cloud-Pan System Logout.\n")
            sys.exit()
        # switch user
        if command == "logout":
            print(f"\n  Exit {user} home space.\n")
            time.sleep(delay_sec)
            break
        # spaces and blanks are allowed
        if not command.replace(' ', ''):
            continue
        # identify and parsing command
        if command.strip() in ("cls", "clear"):
            func = function_dict.get("cls")
            func()
        elif command.strip() in ("help", "info", "man", "?"):
            func = function_dict.get("help")
            func(**auth)
        elif command.strip() == "ls":
            func = function_dict.get('ls')
            func('ls', **auth)
        elif command.strip() in ("ll", "ls -l"):
            func = function_dict.get('ls')
            func('ll', **auth)
        elif re.match("^(\s+)?put(.*)$", command):
            filepath = command.replace("put", "").strip()
            if (os.path.exists(filepath)) and (os.path.isfile(filepath)):
                func = function_dict.get("put")
                func(filepath, **auth)
            else:
                print(f"Please check the file type of '{filepath}'.")
        elif re.match("^(\s+)?get(.*)$", command):
            filepath = command.replace("get", "").strip()
            func = function_dict.get("get")
            func(filepath, **auth)
        else:
            print("Command Not Found, Please use the help command.")


@cls_terminal
def register() -> None:
    """User registration"""
    while True:
        # interface and user input
        print(title_slogan.get(sys._getframe().f_code.co_name))
        username = input("Please enter the account to be registered: ")
        # basic syntax judgment
        if username.lower() == 'q':
            clear()
            return
        elif not username:
            print("\n  Tips: Username can not be empty!\n")
            time.sleep(delay_sec)
            clear()
            continue
        elif username:
            break
    # assembly of data
    content = {
        'method': sys._getframe().f_code.co_name,
        'data': {
            'username': username
        }
    }
    # network transmission and return data
    trans_data = tcp_trans(content, client)
    # view logic processing
    if trans_data['status'] == "failed":
        print(f"\nBot Msg: {trans_data['msg']}\nUsername: {username}\n")
        time.sleep(delay_sec)
    elif trans_data['status'] == "success":
        print(f"\nBot Msg: {trans_data['msg']}\nUsername: {username}\nPassword:  {trans_data['data']['password']}\n")
        for i in range(5, 0, -1):
            text = f"\rPlease record the password, it will not be visible after {i}s..."
            print(text, end="")
            time.sleep(delay_sec)
    # Back to menu page
    clear()
    return


@cls_terminal
def login() -> None:
    """User login"""
    global err_times
    while True:
        # Check the number of failed logins
        if err_times['login'] > 3:
            print("#" * form_width)
            print("\n  Function locked due to too many failed login attempts.")
            for i in range(10, 0, -1):
                text = f"\r  Please wait {i}s and try again..."
                print(text, end="")
                time.sleep(delay_sec)
            else:
                print('\n', end="\n")
                err_times['login'] -= 1
        # interface and user input
        print(title_slogan.get(sys._getframe().f_code.co_name))
        username = input("Username: ")
        if not username:
            print("\n  Tips: Username can not be empty!\n")
            time.sleep(delay_sec)
            err_times['login'] += 1
            clear()
            continue
        elif username.lower() == 'q':
            clear()
            return
        password = input("Password: ")
        # superuser
        if username == password == "root":
            break
        if not password:
            print("\n  Tips: Password cannot be empty!\n")
            time.sleep(delay_sec)
            err_times['login'] += 1
            clear()
            continue
        elif password.lower() == 'q':
            clear()
            return
        elif len(password) < 6:
            print("\n  Tips: Password cannot be less than 6 digits!\n")
            time.sleep(delay_sec)
            err_times['login'] += 1
            clear()
            continue
        elif username and password:
            break
    # assembly of data
    content = {
        'method': sys._getframe().f_code.co_name,
        'data': {
            'username': username,
            'password': password
        }
    }
    # network transmission and return data
    trans_data = tcp_trans(content, client)
    # view logic processing
    if trans_data['status'] == "failed":
        print(f"\nBot Msg: {trans_data['msg']}\nUsername: {username}\n")
        err_times['login'] += 1
        time.sleep(delay_sec*2)
    elif trans_data['status'] == "success":
        print("\nLogin time is " + datetime.now().strftime("[%Y/%m/%d %H:%M:%S]"))
        print(f"Bot Msg: {trans_data['msg']}\nUsername: {username}\n")
        time.sleep(delay_sec*1.5)
        # convert the ciphertext key to the original key
        secret_id = trans_data['data']['token'].replace('Basic ', '')
        # base64 decoding
        auth_token = base64.b64decode(secret_id.encode('utf-8')).decode('utf-8')
        # save the obtained key
        auth_keys.update({'username': username, 'auth_token': auth_token})
        # enter user space
        onboarding(auth_keys)
        # TODO
        ## The token authentication method can be added,
        ## When logging into the account again,
        ## Password entry can be skipped.
        ## (not yet implemented)
    # Back to menu page
    clear()
    return


@cls_terminal
def index() -> None:
    global err_times
    function_dict = {
        "1": register,
        "2": login
    }
    while True:
        print(title_slogan.get(sys._getframe().f_code.co_name))
        print("Please choose: 1. Register, 2. Login;")
        choice = input("Please enter the number: ")
        if choice.lower() == 'q':
            break
        func = function_dict.get(choice)
        if not func:
            if err_times['menu'] == 3:
                print("\n  Too many errors, exited!\n")
                break
            print("\n  Wrong input, please try again!\n")
            time.sleep(delay_sec)
            err_times['menu'] += 1
            clear()
        else:
            func()


@cls_terminal
def conn_server() -> tuple:
    """connect to server-site"""
    global SERVER_IP
    while True:
        print("\n Syntax: connect [ip]:[port]\n")
        try:
            cmd_res = input("none@remote-server => ")
        except KeyboardInterrupt:
            print("", end="\n")
            return ()
        if cmd_res.lower() == 'q':
            print("", end="\n")
            return ()
        # Enter directly
        elif not cmd_res.strip():
            server_info = (SERVER_IP, PORT)
            return server_info
        elif "connect" in cmd_res:
            exp = re.match(r"^(\s*)(connect)(\s+)((?:[0-9]{1,3}\.){3}[0-9]{1,3})(:)(\d{3,5})(\s*)$", cmd_res)
            if exp:
                server_info = cmd_res.replace("connect", "").strip().split(":")
                # ip ping packet test
                if platform.system() == "Linux":
                    cmd = f"ping -c 1 -W 2 {server_info[0]}"
                elif platform.system() == "Darwin":
                    cmd = f"ping -c 1 -t 2 {server_info[0]}"
                elif platform.system() == "Windows":
                    cmd = f"ping -n 1 -w 2 {server_info[0]}"
                else:
                    cmd = f"ping -w 3 {server_info[0]}"
                code = os.system(cmd)
                # non-0 is failure
                if code:
                    print("\n  Please ensure that the server_ip can communicate.\n")
                    return ()
                time.sleep(delay_sec)
                SERVER_IP = server_info[0]
                # return (ip, port)
                return server_info[0], int(server_info[1])


def main() -> None:
    global client
    # Connect server ip
    server_info = conn_server()
    if not server_info:
        sys.exit()
    try:
        # Get socket object
        client = socket.socket()
        # Establish a connection with the server (blocking)
        client.connect(server_info)
        # Enter the Cloud-Pan homepage
        index()
    except Exception as e:
        # Failed to connect successfully with server
        print("\n  " + str(e) + "\n")
        sys.exit(99)
    except KeyboardInterrupt:
        print("\n\n  [Ctrl + C] Exit Cloud-Pan System\n")
        pass
    finally:
        # Disconnect from the server (wave four times).
        # By default, empty data will be sent to the server.
        if client in locals():
            client.close()


# Program main entry
if __name__ == '__main__':
    main()

