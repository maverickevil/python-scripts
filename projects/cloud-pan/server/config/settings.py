# -*- coding: utf-8 -*-
import os

# Define Server-side global variables.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Server ip address
SERVER_IP = "172.0.0.1"

# Service port
PORT = 8888

# Number of client connection pools
CONN_COUNTS = 10

