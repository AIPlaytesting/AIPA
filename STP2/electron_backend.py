
from backend.connection import Connection
from backend.protocol import ResponseMessage

# electron method code 
ELECTRON_DETECT_ENV = 10
ELECTRON_TRAIN = 11
ELECTRON_SIMULATE = 12

# connect to frontend
connection = Connection(10000)
connection.connect()

def detect_env_mainloop():
    def detectEnv():
        version = {}
        import sys
        pyver = sys.version_info
        version['py'] = str(pyver.major) +'.'+str(pyver.minor)+'.'+str(pyver.micro)
        try:
            import tensorflow
            version['tf'] = tensorflow.__version__
        except:
            version['tf'] = 'none'

        return version
    ver = detectEnv()
    connection.send_response(ResponseMessage("electron",ver))
    print("detect env mainloop done: ",ver)

def train_mainloop():
    connection.send_response(ResponseMessage("electron","train"))

def simulate_mainloop():
    connection.send_response(ResponseMessage("electron","simulate"))


# wait method
request = connection.wait_one_request()
if request.method == ELECTRON_DETECT_ENV:
    detect_env_mainloop()
elif request.method == ELECTRON_TRAIN:
    train_mainloop()
elif request.method == ELECTRON_SIMULATE:
    simulate_mainloop()
else:
    print("undefined method: ",request.method)