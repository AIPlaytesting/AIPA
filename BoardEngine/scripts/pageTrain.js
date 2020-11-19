const dbmanager = require('../scripts/dbmanager')
var trainingQueue = []

class TrainSession{
    constructor(trainInfo){
        this.trainInfo = trainInfo
    }

    getSessionID(){
        return this.trainInfo.gameName+this.trainInfo.deckName
    }

    startTrain(){
        setTrainHeadPannel(true)

        let gameName = this.trainInfo.gameName
        let deckName = this.trainInfo.deckName

        // lock the deck before training
        dbmanager.updateGameData(gameName,'lockedDeck',deckName,refreshLibraryPage)

        let sessionID = this.getSessionID()
        let pyProcess = new PythonProcess(
            11,
            {'game_id':gameName,
            'deck_id':deckName,
            'iterations':this.trainInfo.iterations},
            function () { console.log('success!') },
            function (data) {onReceiveTrainMesssage(sessionID,data) },
            function(err){popupWarning(err)})
    }
    
    createView(){
        let sessionID = this.getSessionID()
        let trainSessionDiv = $(document.createElement('div'))
        .attr('class','row')
        .attr('id',sessionID+'-train-session')
        .addClass('inner-section')
        .append(createProgressBarElement())
        .append(createStatusElement())
        console.log(trainSessionDiv)
        return trainSessionDiv

        function createProgressBarElement(){
            let root = $(document.createElement('div')).addClass('col-3')
            let progressRoot = $(document.createElement('div')).attr('class',"clearfix text-center")
            let progressBar = $(document.createElement('div'))
            .attr('id',sessionID+'-train-progress-bar')
            .attr('class',"c100 p0")
            .append($(document.createElement('span')).attr('id',sessionID+'-train-progress-text'))
            .append("<div class='slice'><div class='bar'></div><div class='fill'></div></div>")
            root.append(progressRoot.append(progressBar))
            return root
        }

        function createStatusElement(){
            let root = $(document.createElement('div')).addClass("col-8")
            let initIndicator = $(document.createElement('div'))
            .append("<span class='spinner-border text-dark' role='status'></span>")
            .append("initializing...")
            let statusText = $(document.createElement('h1'))
            .attr('id',sessionID + '-train-status')
            .attr('class','text-center')
            .append(initIndicator)
            
            return root.append(statusText)
        }
    }
}

function startTrain(gameName,deckName){
    let trainInfo = collectTrainInfo()
    let trainSession = new TrainSession(trainInfo)
    trainSession.startTrain()
    trainingQueue.push(trainSession)
    updateTrainingQueueView()

    function collectTrainInfo(){
        let trainInfo = {
            'gameName':gameName,
            'deckName':deckName,
            'iterations':$('#train-iter-config').val()
        }
        return trainInfo
    }
}

function updateTrainPage(){
    updateTrainingQueueView()
}


function onReceiveTrainMesssage(sessionID,data){
    let trainInfo = JSON.parse(data).content
    let curprogress =  trainInfo.curprogress
    let maxprogress = trainInfo.maxprogress
    let percentage = Math.ceil(100*curprogress/maxprogress)

    $('#'+sessionID+'-train-progress-bar').attr("class","c100 p"+percentage)
    $('#'+sessionID+'-train-progress-text').text(curprogress + "/" + maxprogress)
    if(trainInfo.is_finished){
        onTrainFinish(sessionID)
    }
    else{
        $('#'+sessionID+'-train-status').text('Remaining Time :  ' + trainInfo.remaining_hours + ' Hrs ' + trainInfo.remaining_minutes + ' Min.')
    }
}

function updateTrainingQueueView(){
    let rootDiv = $('#training-queue').text("")
    for(let trainSession of trainingQueue){
        rootDiv.append(trainSession.createView())
    }
}

function setTrainHeadPannel(isTrainScheduled){
    if(isTrainScheduled){
        $('#train-btn').addClass('d-none')
        $('#train-config').addClass('d-none')
    
        $('#train-status').removeClass('d-none')
        $('#train-status').text('The train has been scheduled :-)')
    }
    else{
        $('#train-btn').removeClass('d-none')
        $('#train-config').removeClass('d-none')

        $('#train-status').addClass('d-none')
    }
}

// TO-DO: now it use extranl func in library.js!
function onTrainFinish(sessionID){
    $('#'+sessionID+'-train-status').text('training is over')
    setTrainHeadPannel(false)
    // TO-DO: now it use extranl func in library.js!
    updatePlaytestPage()

    // remove from the queue
    for(let s of trainingQueue){
        if(s.getSessionID() == sessionID){
            let index = trainingQueue.indexOf(s)
            trainingQueue.splice(index, 1)
            console.log(sessionID+ "removed from the queue")
        }
    }
}
module.exports ={startTrain,updateTrainPage}