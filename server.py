import socket

def str_to_int(str):
    try:
        return int(str)
    except (ValueError, TypeError):
        return None

class Server:
    def __init__(self):
        print("Welcome, please enter information to initialize server")
        
        self.address = None
        while not self.address:
            self.address = input("Type server address: ")
        
        self.port = None
        while not self.port:
            self.port = str_to_int(input("Type server port: "))
            
        self.connected = []
    
    def host(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.address, self.port))
        self.socket.setblocking(False)
        
        print(f"Server initizialized on {self.address}:{self.port}")
        
    def activate(self):
        self.active = True
        while self.active:
            try:
                data, sndr = self.socket.recvfrom(1024)
                print(f"({sndr[0]}) {data.decode()}")
                
                try:
                    self.connected.index(sndr)
                except ValueError:
                    self.connected.append(sndr)

                for ip in self.connected:
                    self.socket.sendto(data, ip)
            except BlockingIOError:
                pass
            
    def deactivate(self):
        self.active = False
        
    def close(self):
        self.socket.close()
            
def main():
    server = Server()
    server.host()
    server.activate()

if __name__ == "__main__":
    main()