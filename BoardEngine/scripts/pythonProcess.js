const net = require('net')
const SERVER_PORT = 10000
const rootPath = require('electron-root-path').rootPath
const config = require('../scripts/config')
// methodCode: 
// env = 10
// train = 11
// simulate = 12
class PythonProcess {
	constructor(methodCode,params, onSuccessListenter, onReceiveDataListener, onFailListenter = null) {
		this.socket = undefined
		let curPythonProcess = this
		try{
			launchProcessByBat(onFailListenter)
		}
		catch(e){
			console.log(e)
			throw e
		}
		net.createServer(function (socket) {
			curPythonProcess.socket = socket
			curPythonProcess.socket.on('data',onReceiveDataListener)
			curPythonProcess.sendMessage(createMessage(methodCode,params))
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

function launchProcessByBat(onFailListenter){
	let child = require('child_process').execFile;
	let executablePath = ''
	if(config.isDevMode){
		console.log("launch python in development mode...")
		executablePath  = rootPath+'\\'+config.devDependencies.pyLauncher
	}
	else{
		console.log("launch python in build mode...")
		executablePath  = rootPath+'\\'+config.buildDependencies.pyLauncher
	}


	console.log('start bat at: '+executablePath)
	child(executablePath, function(err, data) {
		if(err){
			console.error(err);
			if(onFailListenter!=null){
				onFailListenter()
			}
		}
	}) 
}

module.exports = PythonProcess