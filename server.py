# imports
import socket

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
        print("Welcome, please enter information to initialize server")
        
        # get ip address
        self.address = None
        while not self.address:
            self.address = input("Type server address: ")
        
        # get port (can be any)
        self.port = None
        while not self.port:
            self.port = str_to_int(input("Type server port: "))
        
        # connected ips
        self.connected = []
    
    # host server
    def host(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.address, self.port))
        self.socket.setblocking(False)
        
        print(f"Server initizialized on {self.address}:{self.port}")
        
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
    def deactivate(self):
        self.active = False
    
    # close server
    def close(self):
        self.socket.close()
            
# server initilization
def main():
    server = Server()
    server.host()
    server.activate()

if __name__ == "__main__":
    main()