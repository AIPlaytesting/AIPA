const PythonProcess = require('./pythonProcess.js')

function onTestStart(){
    console.log('hi')
    let pyProcess = new PythonProcess(10000, 
	    function () { pyProcess.sendMessage({'method':66}) },
        function(data){console.log('receive: '+data)})
    startPy()
}

function startPy(){
    let child = require('child_process').execFile;
    console.log('start py!')
    let executablePath = "C:\\Users\\siqiwan2\\Documents\\GitHub\\AIPA\\BoardEngine\\runpy.bat";
    child(executablePath, function(err, data) {
        if(err){
           console.error(err);
           return;
        }
     
        console.log(data.toString());
    });  
}