function onClickTrain(){
    $('#train-btn').addClass('d-none')
    $('#train-config').addClass('d-none')
    $('#train-progress').removeClass('d-none')
    $('#train-status').removeClass('d-none')
    $('#train-status').text('load AI...')
    let gameID = dbmanager.getCurrentGameName()
    let deckID = currentGameData.rules.deck
    let iterationNums = $('#train-iter-config').val()
    // lock the deck before training
    dbmanager.updateGameData(gameID,'lockedDeck',deckID,refreshLibraryPage)
    let pyProcess = new PythonProcess(
        11,
        {'game_id':gameID,'deck_id':deckID,'iterations':iterationNums},
	    function () { console.log('success!') },
        onReceiveTrainMesssage,
        function(err){popupWarning(err)})
}

function onReceiveTrainMesssage(data){
    trainInfo = JSON.parse(data).content
    let curprogress =  trainInfo.curprogress
    let maxprogress = trainInfo.maxprogress
    let percentage = Math.ceil(100*curprogress/maxprogress)
    $('#train-progress').attr("class","c100 p"+percentage)
    $('#train-progress-text').text(curprogress + "/" + maxprogress)
    if(trainInfo.is_finished){
        $('#train-status').text('training is over')
        // also update playtest
        updatePlaytestPage()
    }
    else{
        $('#train-status').text('Remaining Time :  ' + trainInfo.remaining_hours + ' Hrs ' + trainInfo.remaining_minutes + ' Min.')
    }
}

module.exports ={onClickTrain}