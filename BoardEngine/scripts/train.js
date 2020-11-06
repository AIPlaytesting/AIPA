const PythonProcess = require('../Scripts/pythonProcess.js')
function train(){
    let pyProcess = new PythonProcess(11,
	    function () { console.log('success!') },
        onReceiveTrainMesssage)
}

function onReceiveTrainMesssage(data){
    trainInfo = JSON.parse(data).content
    let curprogress =  trainInfo.curprogress
    let maxprogress = trainInfo.maxprogress
    $('#train-progress').attr("style","width:"+(curprogress*100/maxprogress)+"%")
    $('#train-progress').text(curprogress+'/'+maxprogress)
    $('#train-cur-winrate').text("winrate: " + trainInfo.curwinrate)
}