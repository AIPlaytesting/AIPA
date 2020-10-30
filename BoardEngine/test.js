const PythonProcess = require('./pythonProcess.js')
function onTestStart(){
    console.log('hi')
    let pyProcess = new PythonProcess(10000, 
	    function () { pyProcess.sendMessage({'method':66}) },
	    function(data){console.log('receive: '+data)})
}