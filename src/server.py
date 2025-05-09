# imports
import socket
import threading

# functions
# convert string to int
def str_to_int(str):
    try:
        return int(str)
    except (ValueError, TypeError):
        return None

# server class
class Server:
    # get info about server
    def __init__(self):
        print("welcome, please type information to initialize server")
        
        # get ip address
        self.address = None
        while not self.address:
            self.address = input("type server address: ")
        
        # get port (can be any)
        self.port = None
        while not self.port:
            self.port = str_to_int(input("type server port: "))
        
        # connected ips
        self.connected = []
    
    # host server
    def host(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.address, self.port))
        
        print(f"server initizialized on {self.address}:{self.port}")
    
    # manage server
    def manage(self):
        while True:
            # managing by commands
            cmd = input("/")
            
            if cmd.lower() == "activate":
                # server.activate()
                threading.Thread(target=self.activate).start()
            elif cmd.lower() == "disable":
                # server.disable()
                self.disable()
            elif cmd.lower() == "close":
                # server.close()
                self.socket.close()
                break
    
    # activate to forward messages to all connected ips
    def activate(self):
        self.active = True
        
        while self.active:
            try:
                # attempt to get send data
                data, sndr = self.socket.recvfrom(1024)
                print(f"({sndr[0]}) {data.decode()}")
                
                # check if sender in ip list
                try:
                    self.connected.index(sndr)
                except ValueError:
                    self.connected.append(sndr)

                # forward new message to every ip
                for ip in self.connected:
                    self.socket.sendto(data, ip)
            except BlockingIOError:
                pass
    
    # deactivate message forwarding
    def disable(self):
        self.active = False
            
# server initilization
def main():
    server = Server()
    server.host()
    server.manage()

if __name__ == "__main__":
    main()