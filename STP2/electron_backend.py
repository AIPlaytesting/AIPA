
from backend.connection import Connection
from backend.protocol import ResponseMessage

def detectEnv():
    version = {}
    import sys
    pyver = sys.version_info
    version['python'] = str(pyver.major) +'.'+str(pyver.minor)+'.'+str(pyver.micro)
    try:
        import tensorflow
        version['tf'] = tensorflow.__version__
    except:
        version['tf'] = 'none'

    return version

# connect to frontend
connection = Connection(10000)
connection.connect()

while True:
    request = connection.wait_one_request()
    print(request.method)
    ver = detectEnv()
    print(ver)
    connection.send_response(ResponseMessage(1,ver))

