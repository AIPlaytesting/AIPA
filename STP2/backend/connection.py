import socket
import json
from .protocol import RequestMessage, UserInput
class Connection:
    def __init__(self):
        pass

    def connect(self):
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect the socket to the port where the server is listening
        server_address = ('127.0.0.1', 9999)
        print ('connecting to: ',server_address)
        sock.connect(server_address)
        print ('connected to: ',server_address)

    def wait_one_request(self)->RequestMessage:
        data = socket.recv(1024) 
        message_json_data = data.decode()
        print('recv raw json: ',message_json_data)
        request_dict = json.loads(message_json_data) 

        method = request_dict['method']
        if method  == 'UserInput':
            # parse userinput
            user_input_dict = request_dict['userInput']
            user_input = UserInput(
                user_input_dict['type'],
                user_input_dict['cardName'],
                user_input_dict['cardGUID'])
            return RequestMessage(method,user_input,"")
        elif method == 'DBQuery':
            return RequestMessage(method,None,request_dict['dbQuery'])
        else:
            print("undefined method: ",method)
            return None

    def send_response(self,response):
        pass