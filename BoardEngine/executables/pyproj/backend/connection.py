import socket
import json
from .protocol import RequestMessage, ResponseMessage,PlayerStep

PDU_DIVIDOR = '$'
class Connection:
    def __init__(self,port):
        self.__sock = None
        self.__pdus = []
        self.__port = port

    def connect(self):
        # Create a TCP/IP socket
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect the socket to the port where the server is listening
        server_address = ('127.0.0.1', self.__port)
        print ('connecting to: ',server_address)
        self.__sock.connect(server_address)
        print ('connected to: ',server_address)

    def wait_one_request(self)->RequestMessage:
        if len(self.__pdus) == 0:
            data = self.__sock.recv(16384) 
            stream_str = data.decode()
            # print("[raw stream] ",stream_str)
            for i,pdu in enumerate(stream_str.split(PDU_DIVIDOR)):
                if len(pdu) >= 2:
                    print("[splited pdu]",i,'-',pdu)
                    self.__pdus.append(pdu)

        pdu = self.__pdus[0]
        self.__pdus.pop(0)

        message_json_data =  pdu
        request_dict = json.loads(message_json_data) 
        request_message = RequestMessage.create_request_message_from(request_dict)
        return request_message

    def send_response(self,response:ResponseMessage):
        self.__sock.send(response.to_json().encode())