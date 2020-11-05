const PythonProcess = require('../scripts/pythonProcess.js')

function onTestEnv(){
    console.log('env')
    let pyProcess = new PythonProcess(10,
	    function () { console.log('success!') },
        function(data){console.log('receive: '+data)})
}

function onTestTrain(){
    console.log('train')
    let pyProcess = new PythonProcess(11,
	    function () { console.log('success!') },
        function(data){console.log('receive: '+data)})
}



function onTestSimulate(){
    console.log('simulate')
    let pyProcess = new PythonProcess(12,
	    function () { console.log('success!') },
        function(data){console.log('receive: '+data)})
}

