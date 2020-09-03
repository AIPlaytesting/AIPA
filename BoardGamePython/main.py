import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('127.0.0.1', 9999)
print ('connecting to: ',server_address)
sock.connect(server_address)
print ('connected to: ',server_address)

try:     
    while True:
        # recv data
        data = sock.recv(1024) 
        print('recv:',data.decode())
        # echo back
        sock.send("I received your message!".encode())
finally:
    print ('closing socket') 
    sock.close()