import socket
import json
from .protocol import RequestMessage, ResponseMessage,PlayerStep
class Connection:
    def __init__(self):
        self.__sock = None

    def connect(self):
        # Create a TCP/IP socket
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect the socket to the port where the server is listening
        server_address = ('127.0.0.1', 9999)
        print ('connecting to: ',server_address)
        self.__sock.connect(server_address)
        print ('connected to: ',server_address)

    def wait_one_request(self)->RequestMessage:
        data = self.__sock.recv(1024) 
        message_json_data = data.decode()
        print('recv raw json: ',message_json_data)
        request_dict = json.loads(message_json_data) 
        request_message = RequestMessage.create_request_message_from(request_dict)
        return request_message

    def send_response(self,response:ResponseMessage):
        self.__sock.send(response.to_json().encode())