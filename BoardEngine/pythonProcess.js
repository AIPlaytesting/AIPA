const net = require('net')

class PythonProcess {
	constructor(port, onSuccessListenter, onReceiveDataListener) {
		this.socket = undefined
		let curPythonProcess = this
		net.createServer(function (socket) {
			curPythonProcess.socket = socket
			console.log("connected")
			curPythonProcess.socket.on('data',onReceiveDataListener)
			onSuccessListenter()
		})
			.listen(port, '127.0.0.1')
	}

	sendMessage(messageObj) {
		this.socket.write(JSON.stringify(messageObj))
	}
}

module.exports = PythonProcess