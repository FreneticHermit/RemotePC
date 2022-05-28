import os
import socket
import uuid
from select import select
from commons import *
import webbrowser

class Server:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.monitor=[]
        self.clients=[]
        self.client_socket=None
        self.addr=None
        self.disconnected=False
    def start_server(self):
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((get_ip(), variables().port))
        self.server_socket.listen()
        self.monitor.append(self.server_socket)
    def wait_for_users(self):
        self.clients.clear()
        self.client_socket, self.addr = self.server_socket.accept()
        print('Connected', self.addr)
        self.clients.append(self.client_socket)
        self.monitor.append(self.client_socket)
        self.client_socket.send(self.separate_mac(hex(uuid.getnode())).encode())
    def separate_mac(self,mac):
        format_mac = ''
        mac = mac[2:]
        while mac:
            format_mac += mac[:2]
            if len(mac) > 2:
                format_mac += '.'
            mac = mac[2:]
        return format_mac
    def link_func(self,data):
        if len(data.split(":")) > 1:
            webbrowser.open(data)
        else:
            webbrowser.open(f'https:{data}')
    def execute_func(self,data):
        os.system(f'"{data.upper()}"')
    def power_func(self,data):
        pass
    def special_func(self,data):
        if data=="disconnect":
            self.disconnected=True
    def check_data(self,data):
        data=data.lower()
        type=int(data.split("::")[0])
        command=data.split("::")[1]
        if type==variables().function_index.get("link"):
            self.link_func(command)
        if type==variables().function_index.get("execute"):
            self.execute_func(command)
        if type==variables().function_index.get("power"):
            self.power_func(command)
        if type==variables().function_index.get("special"):
            self.special_func(command)
    def send_data(self,data):
        for client in self.clients:
            client.send(data.encode())
    def listen_user(self):
        data = self.client_socket.recv(4096).decode()
        self.check_data(data)
    def event(self):
        self.start_server()
        while True:
            try:
                ready_to_read,_,_=select(self.monitor,[],[])
                for sock in ready_to_read:
                    if sock is self.server_socket:
                        self.wait_for_users()
                    else:
                        self.listen_user()
                if self.disconnected==True:
                    print("Disconnected", self.addr)
                    self.monitor.clear()
                    self.monitor.append(self.server_socket)
                    self.disconnected = False
                    continue
            except:
                self.disconnected=True
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP
if __name__ == '__main__':
    print(f"IP: {get_ip()}\nWaiting for device to connect...")
    server_class=Server()
    server_class.event()