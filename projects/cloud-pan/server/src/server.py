# -*- coding: utf-8 -*-
# @File   : server.py
# @Author : PokeyBoa
# @Date   : 2022/04/17 - 04/19
# @Desc   : Cloud Network Pan (server)
"""
Server socket conn: Non-blocking + I/O multiplexing
Procedure realization: Object Oriented programming + Reflection
Upload and download: Asynchronous multithreading
"""

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import *
from datetime import datetime
import ipaddress
import threading
import random
import select
import socket
import struct
import base64
import time
import json

lock_object = threading.RLock()

class SocketTrans(object):
    """
    Perform TCP protocol network transmission, send and receive network packets.
    """
    def __init__(self, conn):
        self.conn = conn

    def send_msg(self, content: str):
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


def tcp_trans(conn) -> bool:
    """
    A wrapper for the SocketTrans Class.
    """
    # get connected
    tcp = SocketTrans(conn)
    # receive json data
    result = tcp.receive_msg
    # convert json to dict format
    trans_data = json.loads(result)
    if trans_data:
        # Business logic data processing
        callback = run_task(trans_data)
        json_data = json.dumps(callback)
        # send json data to client
        tcp.send_msg(json_data)
        return True
    return False


def get_host_ip() -> str:
    """
    Get the local ip.
    """
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        res = str(ipaddress.ip_address(ip))
    except:
        res = "127.0.0.1"
    finally:
        if s:
            s.close()
    return res


def check_port_in_use(host, port) -> bool:
    """
    Check if the port is occupied.
    """
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((host, int(port)))
        s.close()
        # print("This port is already in use, please replace.")
        return True
    except socket.error:
        # print("This port is not in use.")
        return False
    finally:
        if s:
            s.close()


def recv_save_file(target_path: str, port: int) -> None:
    """
    Block receiving and save files.
    """
    with lock_object:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((SERVER_IP, port))
        sock.listen(CONN_COUNTS)
        # print("waiting for file")
        conn, addr = sock.accept()
        # Get header information: data length
        chunk_size = 1024
        has_read_size = 0
        bytes_list = []
        while has_read_size < 4:
            chunk = conn.recv(4 - has_read_size)
            bytes_list.append(chunk)
            has_read_size += len(chunk)
        header = b"".join(bytes_list)
        data_length = struct.unpack('i', header)[0]
        # Retrieve data
        with open(target_path, mode='wb') as f:
            has_read_data_size = 0
            while has_read_data_size < data_length:
                size = chunk_size if (data_length - has_read_data_size) > chunk_size else data_length - has_read_data_size
                chunk = conn.recv(size)
                f.write(chunk)
                f.flush()
                has_read_data_size += len(chunk)
        # print("file received")
        conn.close()
        sock.close()


def send_file_by_seek(port, file_size, file_path, seek=0) -> None:
    """
    Read and send the file (supports reading from the specified byte position).
    """
    with lock_object:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((SERVER_IP, port))
        sock.listen(CONN_COUNTS)
        conn, addr = sock.accept()
        while True:
            time.sleep(0.05)
            data = conn.recv(1)
            if data:
                break
        header = struct.pack('i', file_size)
        conn.sendall(header)
        has_send_size = 0
        with open(file_path, mode='rb') as f:
            if seek:
                f.seek(seek)
            while has_send_size < file_size:
                chunk = f.read(2048)
                conn.sendall(chunk)
                has_send_size += len(chunk)
        conn.close()
        sock.close()


class NetPanSystem(object):
    # key: user, value: token
    LoginSessions = {}

    def __init__(self, **kwargs):
        self.data = kwargs
        self.dbdir = os.path.join(BASE_DIR, "db")
        if not os.path.exists(self.dbdir):
            os.makedirs(self.dbdir)
        self.dbfile = os.path.join(self.dbdir, "users.csv")
        if not os.path.exists(self.dbfile):
            with open(self.dbfile, mode='a', encoding='utf-8') as f:
                f.write("username,password")
                f.write("\nroot,root")
        self.home = os.path.join(BASE_DIR, "space")
        if not os.path.exists(self.home):
            os.makedirs(self.home)
        if not os.path.exists(self.home + os.sep + "root"):
            os.makedirs(self.home + os.sep + "root")

    @staticmethod
    def get_random_password(total=16) -> str:
        constant_str = 'abcdefghijklmnopqrstuvwxyz!@#$%+=-_^&*.?ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
        random_str = ''.join(random.sample(constant_str, total))
        return random_str

    def login(self) -> dict:
        """
        Enter the correct account and password, the login is successful,
        otherwise it will fail.
        """
        # print(f"This is the '{sys._getframe().f_code.co_name}' method.")
        this_name = self.data.get('username')
        this_pwd = self.data.get('password')
        with open(file=self.dbfile, mode='rt', encoding='utf-8') as f:
            # Filter out the header and move the cursor one line
            f.readline()
            for line in f:
                user, pwd = line.strip().split(',')
                if (user == this_name) and (pwd == this_pwd):
                    # Generate 30 digit random numbers
                    auth_token = self.get_random_password(30)
                    # Base64 encoding
                    secret_id = base64.b64encode(auth_token.encode('utf-8')).decode('utf-8')
                    # A record for storing the original key
                    self.LoginSessions.update({this_name: auth_token})
                    return {
                        "status": "success",
                        "msg": "Successfully logged in to the system ~",
                        "data": {
                            "username": this_name,
                            "token": "Basic " + secret_id
                        }
                    }
        return {
            "status": "failed",
            "msg": "Account or password do not match!",
            "data": {}
        }

    def register(self) -> dict:
        """
        If the user is queried in the database, the server will return
        a failed result. If not, the server returns the registration
        success and randomly generates a 6-digit password for the user.
        """
        # print(f"This is the '{sys._getframe().f_code.co_name}' method.")
        this_name = self.data.get('username')
        with open(file=self.dbfile, mode='rt', encoding='utf-8') as f:
            # Filter out the header and move the cursor one line
            f.readline()
            for line in f:
                user, _ = line.strip().split(',')
                if user == this_name:
                    return {
                        "status": "failed",
                        "msg": "The username is already occupied, registration failed.",
                        "data": {}
                    }
        # Generate 10-digit password
        random_password = self.get_random_password(10)
        # Account information writing database
        with open(file=self.dbfile, mode='at', encoding='utf-8') as f:
            f.write(f"\n{this_name},{random_password}")
            f.flush()
        # Create user home directory
        folder_path = os.path.join(self.home, this_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        return {
            "status": "success",
            "msg": "User registration is successful.",
            "data": {
                "username": this_name,
                "password": random_password
            }
        }

    def filelist(self) -> dict:
        # print(f"This is the '{sys._getframe().f_code.co_name}' method.")
        for user, token in self.LoginSessions.items():
            # token verification passed
            if (self.data.get('cookie').get('username') == user) and (self.data.get('cookie').get('auth_token') == token):
                house = os.path.join(self.home, user)
                flist = sorted([f for f in os.listdir(house) if not os.path.isdir(house + os.sep + f)])
                fcount = len(flist)
                fabslist = [os.path.join(house, f) for f in flist]
                f_bsize_list = [(os.path.basename(i), os.stat(i).st_size) for i in fabslist]
                return {
                    "status": "success",
                    "msg": f"List files in {user} space.",
                    "data": {
                        "filelist": flist,
                        "counts": fcount,
                        "f_bsize_list": f_bsize_list
                    }
                }
        return {
            "status": "failed",
            "msg": "This is an illegal login.",
            "data": {}
        }

    def putfile(self) -> dict:
        # print(f"This is the '{sys._getframe().f_code.co_name}' method.")
        for user, token in self.LoginSessions.items():
            # token verification passed
            if (self.data.get('cookie').get('username') == user) and (self.data.get('cookie').get('auth_token') == token):
                house = os.path.join(self.home, user)
                file = os.path.basename(self.data.get('upload'))
                filepath = house + os.sep + file
                if os.path.exists(filepath) and os.path.isfile(filepath):
                    if self.data.get('overwrite'):
                        # delete the original file
                        os.remove(filepath)
                    else:
                        return {
                            "status": "failed",
                            "msg": "The file already exists.",
                            "data": {}
                        }
                # Test assigning new ports
                while True:
                    port_num = random.randint(13000, 15000)
                    port_inuse = check_port_in_use(SERVER_IP, port_num)
                    if not port_inuse:
                        break
                # Multi-threaded asynchronous processing blocking
                task = threading.Thread(target=recv_save_file, args=(filepath, port_num))
                task.start()
                return {
                    "status": "success",
                    "msg": "The uploader task is ready.",
                    "data": {
                        "listenport": port_num,
                        "savepath": filepath
                    }
                }


    def getfile(self) -> dict:
        # print(f"This is the '{sys._getframe().f_code.co_name}' method.")
        for user, token in self.LoginSessions.items():
            # token verification passed
            if (self.data.get('cookie').get('username') == user) and (self.data.get('cookie').get('auth_token') == token):
                house = os.path.join(self.home, user)
                file = os.path.basename(self.data.get('rfilepath'))
                filepath = house + os.sep + file
                filesize = os.stat(filepath).st_size
                lfilesize = int(self.data.get('lfilesize'))
                if os.path.exists(filepath) and os.path.isfile(filepath):
                    if self.data.get('resume'):
                        # Resume from a breakpoint
                        download_seek = filesize - lfilesize
                        mode = "ab"
                    else:
                        # Download from scratch
                        download_seek = 0
                        mode = "wb"
                else:
                    return {
                            "status": "failed",
                            "msg": "The file is not exists.",
                            "data": {}
                    }
                # Test assigning new ports
                while True:
                    port_num = random.randint(13000, 15000)
                    port_inuse = check_port_in_use(SERVER_IP, port_num)
                    if not port_inuse:
                        break
                # Multi-threaded asynchronous processing blocking
                task = threading.Thread(target=send_file_by_seek, args=(port_num, filesize, filepath, download_seek))
                task.start()
                return {
                    "status": "success",
                    "msg": "The downloader task is ready.",
                    "data": {
                        "listenport": port_num,
                        "mode": mode,
                        "seek": download_seek
                    }
                }


def run_task(request: dict) -> dict:
    data = request.get('data')
    method = request.get('method')
    cls = NetPanSystem(**data)
    func = getattr(cls, method, None)
    if not func:
        print("wrong method name.")
        return {}
    return func()


def do_somethings(socket_list: list) -> None:
    """
    waiting or processing other transactions.
    """
    now = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    conn_nums = f"[{len(socket_list) - 1} Client Connections".ljust(24) + "]"
    print(f"{now} [INFO] {conn_nums} | Listening & Waiting ...")
    time.sleep(1)


def litsen() -> None:
    global SERVER_IP
    SERVER_IP = get_host_ip()
    try:
        # socket object list
        socket_objs = []
        # create socket obj
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # enable non-blocking
        server.setblocking(False)
        # Bind IP and Port
        server.bind((SERVER_IP, PORT))
        # number of monitors
        server.listen(CONN_COUNTS)
        # Add the server object to the socket list
        socket_objs.append(server)
        while True:
            rlist, wlist, _ = select.select(socket_objs, [], [], 0.05)
            # Monitor socket request status changes
            for sock in rlist:
                # Monitor for new connections
                if sock == server:
                    # Receive new connections
                    conn, addr = sock.accept()
                    now = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
                    raddr = f"[IP Addr: {addr[0]}".ljust(24) + "]"
                    print(f"{now} [INFO] {raddr} | DiDiDi, Client {id(conn)} is online~")
                    socket_objs.append(conn)
                # Monitor if new data arrives
                else:
                    res = None
                    try:
                        res = tcp_trans(conn=sock)
                    except:
                        # If it is an empty packet, wave four times to disconnect
                        if not res:
                            now = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
                            raddr = f"[IP Addr: {sock.getsockname()[0]}".ljust(24) + "]"
                            print(f"{now} [INFO] {raddr} | ByeBye, Client {id(sock)} is offline~")
                            sock.close()
                            socket_objs.remove(sock)
            # handle other things
            do_somethings(socket_objs)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    litsen()

