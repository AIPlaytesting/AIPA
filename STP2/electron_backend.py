
from backend.connection import Connection
from backend.protocol import ResponseMessage

# connect to frontend
connection = Connection(10000)
connection.connect()

while True:
    request = connection.wait_one_request()
    print(request.method)
    connection.send_response(ResponseMessage(1,"hi"))