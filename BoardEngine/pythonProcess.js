const net = require('net')
const SERVER_PORT = 10000

// methodCode: 
// env = 10
// train = 11
// simulate = 12
class PythonProcess {
	constructor(methodCode, onSuccessListenter, onReceiveDataListener) {
		this.socket = undefined
		let curPythonProcess = this
		launchProcessByBat()
		net.createServer(function (socket) {
			curPythonProcess.socket = socket
			curPythonProcess.socket.on('data',onReceiveDataListener)
			curPythonProcess.sendMessage(createMessage(methodCode,""))
			console.log("connected...")
			onSuccessListenter()
			console.log("about to close listen server...")
			this.close()
			console.log("server closed!")
		})
			.listen(SERVER_PORT, '127.0.0.1')
	}

	sendMessage(messageObj) {
		this.socket.write(JSON.stringify(messageObj))
	}
}

function createMessage(methodCode,content){
	messageObj = {};
	messageObj.method = methodCode
	messageObj.content = content
	return messageObj
}

function launchProcessByBat(){
    let child = require('child_process').execFile;
    let executablePath = "C:\\Users\\siqiwan2\\Documents\\GitHub\\AIPA\\BoardEngine\\runpy.bat";
	console.log('start bat at: '+executablePath)
	child(executablePath, function(err, data) {
        if(err){
           console.error(err);
           return;
        }
     
        console.log(data.toString());
    });  
}

module.exports = PythonProcess