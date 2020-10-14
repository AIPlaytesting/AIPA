from .connection import Connection
from .gameplay_kernel import GameplayKernel
from .db_accessor import DBAccessor
from .protocol import RequestMessage
class BackendMainloop:
    def __init__(self,connection:Connection,gameplay_kernal:GameplayKernel,db_accessor:DBAccessor):
        self.__connection  = connection
        self.__gameplay_kernal = gameplay_kernal
        self.__db_accessor = db_accessor

    def run(self):
        print("back end running....")
        while True:
            request = self.__connection.wait_one_request()
            print("method:",request.method )