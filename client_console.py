import socket
import wakeonlan
from commons import *
class logic():
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.screen=0
        self.define_functions()
    def define_functions(self):
        self.link_class=menu_function(name="link",index=1,command=lambda: self.link_func())
        self.execute_class=menu_function(name="execute",index=2,command=lambda:self.execute_func())
        self.power_class=menu_function(name="power",index=3,command=lambda : self.power_func())
        self.special_class=menu_function(name="special",index=4,command=lambda: self.special_func())
    def link_func(self):
        in_input = input("Link to open: ").lower()
        if not self.return_to_ms(in_input):
            self.send_server(f"1::{in_input}")
    def execute_func(self):
        in_input = input("Full path to file: ").lower()
        if not self.return_to_ms(in_input):
            self.send_server(f"2::{in_input}")
    def power_func(self):
        in_input = input("Power command: ").lower()
        if not self.return_to_ms(in_input):
            if in_input == "wol":
                self.wol(self.mac)
            else:
                self.send_server(f"3::{in_input}")
    def special_func(self):
        in_input = input("Special command: ").lower()
        if not self.return_to_ms(in_input):
            if in_input.lower() == "disconnect":
                self.send_server(f"4::{in_input}")
                self.start_new_session()
    def return_to_ms(self,data):
        if data == "q":
            self.screen = "0"
            return True
    def start_server(self,ip):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((ip, variables.port))
            print(f'Successfully connected')
            self.mac=self.client_socket.recv(4096).decode()
        except:
            self.start_new_session()
    def listen_server(self):
        self.data = self.client_socket.recv(4096).decode()
        print(self.data)
    def wol(self,mac):
        wakeonlan.send_magic_packet(mac)
    def send_server(self,text):
        self.client_socket.send(text.encode())
    def start_new_session(self):
        self.ip = input("IP on PC: ")
        self.start_server(self.ip)
        self.screen = "0"
    def manager(self):
        self.start_new_session()
        print("q to return to main screen")
        while True:
            try:
                if self.screen=="0":
                    screen_input=input("MENU (1-Link, 2-ExecuteFile, 3-Power, 4-Special): ")
                    self.screen=screen_input
                elif self.screen==str(self.link_class.kwargs_dict.get("index")):
                    self.link_class.execute_command()
                elif self.screen==str(self.execute_class.kwargs_dict.get("index")):
                    self.execute_class.execute_command()
                elif self.screen==str(self.power_class.kwargs_dict.get("index")):
                    self.power_class.execute_command()
                elif self.screen==str(self.special_class.kwargs_dict.get("index")):
                    self.special_class.execute_command()
                else:
                    print("Incorrect menu function")
                    self.screen="0"
            except:
                self.start_new_session()
if __name__=="__main__":
    logic=logic()
    logic.manager()