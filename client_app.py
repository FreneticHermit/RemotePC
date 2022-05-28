import socket
import wakeonlan
import sys
from commons import *

ip=""
Builder.load_string('''
<MainScreen>:
    BoxLayout:
        orientation:'vertical'
        TextInput:
            hint_text:"IP shown on PC"
            id:ip_input
            text:"192.168.1.65"
        Button:
            text:"Open Link"
            on_press:root.redirect("link")
        Button:
            text:"Execute Programs"
            on_press:root.redirect("execute")
        Button:
            text:"Power Control"
            on_press:root.redirect("power")
        Button:
            text:"Special commands"
            on_press:root.redirect("special")
        Button:
            text:"Connect (reconnect)"
            on_press:root.get_ip()
        Button:
            text:"Exit"
            on_press:app.exit_program()
<LinkScreen>:
    BoxLayout:
        orientation:'vertical'
        TextInput:
            hint_text:"Type URL here"
            id:url
        Button:
            text:"Open URL"
            on_press:root.send_data()
        Button:
            text:"To Main Menu"
            on_press:root.to_main()
<ExecuteScreen>:
    BoxLayout:
        orientation:'vertical'
        TextInput:
            hint_text:"Type full path to file here"
            id:path
        Button:
            text:"Open file"
            on_press:root.send_data()
        Button:
            text:"To Main Menu"
            on_press:root.to_main()
<PowerScreen>:
    BoxLayout:
        orientation:'vertical'
        Button:
            text:"Wake On Lan"
            on_press:root.wol()
        Button:
            text:"To Main Menu"
            on_press:root.to_main()
<SpecialScreen>:
    BoxLayout:
        orientation:'vertical'
        Button:
            text:"To Main Menu"
            on_press:root.to_main()
''')
class LinkScreen(Screen):
    def send_data(self):
        app.send_processed_data("link",self.ids.url.text)
    def to_main(self):
        self.manager.current="main"
class ExecuteScreen(Screen):
    def send_data(self):
        app.send_processed_data("execute",self.ids.path.text)
    def to_main(self):
        self.manager.current="main"
class PowerScreen(Screen):
    def wol(self):
        app.wol(app.mac)
    def send_data(self,data):
        app.send_processed_data("power",data)
    def to_main(self):
        self.manager.current="main"
class SpecialScreen(Screen):
    def send_data(self,data):
        app.send_processed_data("special",data)
    def to_main(self):
        self.manager.current="main"
class MainScreen(Screen):
    def get_ip(self):
        global ip
        ip=self.ids.ip_input.text
        app.start_new_session()
    def redirect(self,id):
        self.manager.current=id

class FirstKivy(App):
    def __init__(self):
        super(FirstKivy,self).__init__()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.screen = 0
    def exit_program(self):
        self.send_server("4::disconnect")
        self.client_socket.close()
        sys.exit()
    def send_processed_data(self,name,data):
        index=variables().function_index.get(name)
        self.send_server(f'{index}::{data}')

    def return_to_ms(self,data):
        if data == "q":
            self.screen = "0"
            return True
    def start_server(self,ip):
        try:
            self.client_socket.connect((ip, variables().port))
            print(f'Successfully connected')
            self.mac=self.client_socket.recv(4096).decode()
        except:
            pass
    def listen_server(self):
        self.data = self.client_socket.recv(4096).decode()
        print(self.data)
    def wol(self,mac):
        wakeonlan.send_magic_packet(mac)
    def send_server(self,text):
        self.client_socket.send(text.encode())
    def start_new_session(self):
        self.start_server(ip)
    def build(self):
        SM=ScreenManager()
        SM.add_widget(MainScreen(name="main"))
        SM.add_widget(LinkScreen(name="link"))
        SM.add_widget(ExecuteScreen(name="execute"))
        SM.add_widget(PowerScreen(name="power"))
        SM.add_widget(SpecialScreen(name="special"))
        return SM
if __name__=="__main__":
    app = FirstKivy()
    app.run()