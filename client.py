# imports
import socket
import threading
import sys
import os

# functions
# convert string to int
def str_to_int(str):
    try:
        return int(str)
    except (ValueError, TypeError):
        return None

# client class
class Client:
    # collect client info and what server he want
    def __init__(self):
        print("Welcome, please enter some information before chatting")
        
        # get server address to connect
        self.address = None
        while not self.address:
            self.address = input("Type server address: ")
        
        # get server port
        self.port = None
        while not self.port:
            self.port = str_to_int(input("Type server port: "))
        
        # get optional username
        self.username = input("Type your username (optional): ")
        if not self.username:
            self.username = self.address
    
    # "connect" to server (setting up socket to future communications)
    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # get any new messages without a big delay
    def receive(self):
        while True:
            # 1 seconds timeout to message get
            self.socket.settimeout(1)
            
            try:
                # get new message if possible
                resp, srvr = self.socket.recvfrom(1024)
                
                # beatifull message display and cursor position
                sys.stdout.write(f"\033[s\033[1E{resp.decode()}\033[1L\033[1F\033[u")
                sys.stdout.flush()
            except socket.timeout:
                pass
    
    # send message to server
    def message(self):
        # setup cursor
        sys.stdout.write("\033[1A\033[K> ")
        sys.stdout.flush()
        
        # get message
        message = input()
        
        # commands
        if message.lower() == "/dconnect":
            # dissconect
            self.close()
        elif message.lower() == "/announce":
            # make sound on message
            message = message + "\a"
        else: # default message
            data = f"{self.username}: {message}"
            self.socket.sendto(data.encode(), (self.address, self.port))
    
    # close connection
    def close(self):
        self.socket.close()

# client and terminal setup
def main():
    # setup client
    client = Client()
    client.connect()
    
    # setup terminal
    os.system("")
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # start thread for receiving messages
    threading.Thread(target=client.receive).start()
    
    # loop for messaging
    while True:
        client.message()

if __name__ == "__main__":
    main()