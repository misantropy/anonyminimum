import socket
import threading
import sys
import os

def str_to_int(str):
    try:
        return int(str)
    except (ValueError, TypeError):
        return None

class Client: 
    def __init__(self):
        print("Welcome, please enter some information before chatting")
        
        self.address = None
        while not self.address:
            self.address = input("Type server address: ")
        
        self.port = None
        while not self.port:
            self.port = str_to_int(input("Type server port: "))
            
        self.username = input("Type your username (optional): ")
        if not self.username:
            self.username = self.address
            
    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setblocking(False)
        
    def receive(self):
        while True:
            self.socket.settimeout(1)
            
            try:
                resp, srvr = self.socket.recvfrom(1024)
                sys.stdout.write(f"\033[s\033[1E{resp.decode()}\033[1L\033[1F\033[u")
                sys.stdout.flush()
            except socket.timeout:
                pass
        
    def message(self):
        sys.stdout.write("\033[1A\033[K> ")
        sys.stdout.flush()
        message = input()
        
        if message.lower() != "/pass":
            data = f"{self.username}: {message}"
            self.socket.sendto(data.encode(), (self.address, self.port))
        
    def close(self):
        self.socket.close()
        
def main():
    client = Client()
    client.connect()
    
    os.system("")
    os.system('cls' if os.name == 'nt' else 'clear')
    
    threading.Thread(target=client.receive).start()
    
    while True:
        client.message()

if __name__ == "__main__":
    main()