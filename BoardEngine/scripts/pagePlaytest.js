const dataVisualizer = require('../scripts/dataVisualizer')
const dbmanager = require('../scripts/dbmanager')
const utils = require('../scripts/utils')

function updatePlaytestPage(){
    utils.setupDropdown(
        'AI-dropdown-list',
        'AI-dropdown-btn',
        dbmanager.getAllTrainedVersion(dbmanager.getCurrentGameName(),currentGameData.rules.deck))
    updatePlaytestHistory()

    function updatePlaytestHistory(){
        $('#playtest-history-list').text("").append(createInfoEntry())
        for(let history of dbmanager.getPlaytestHistory(dbmanager.getCurrentGameName(),currentGameData.rules.deck)){
            $('#playtest-history-list').append(createHistoryEntry(history))
        }
    }

    function createInfoEntry(){
        let entryRoot = $(document.createElement('div'))
            .attr('class','row playtest-history-entry')
            .css('border-radius','10px;')
        let space = $(document.createElement('span')).attr('class','col-1')
        let trainVersionText = $(document.createElement('span'))
        .attr('class','col-3')
        .text("AI version")
        .css('font-weight','bold')
        let winrateText = $(document.createElement('span'))
        .attr('class','col-2')
        .text("winrate")
        .css('font-weight','bold')
        let gameNumText = $(document.createElement('span'))
        .attr('class','col-2')
        .text("number of games")
        .css('font-weight','bold')
        entryRoot.append(space, trainVersionText,winrateText, gameNumText)
        return entryRoot
    }

    function createHistoryEntry(historyInfo){
        let entryRoot = $(document.createElement('div'))
            .attr('class','row playtest-history-entry')
            .css('border-radius','10px;')
        let space = $(document.createElement('span')).attr('class','col-1')
        let trainVersionText = $(document.createElement('span')).attr('class','col-3').text(historyInfo.trainVersion)
        let playtestData = dbmanager.loadPlaytestData(historyInfo.gameName,historyInfo.deckName,historyInfo.trainVersion)
        let winrateStr = (playtestData.basicStats.win_rate*100).toFixed(2) +'%'
        let winrateText = $(document.createElement('span')).attr('class','col-2').text(winrateStr)
        let gameNumText = $(document.createElement('span')).attr('class','col-2').text(historyInfo.gameNums)
        let viewResBtn = $(document.createElement('button'))
            .attr('class','col-2 btn btn-primary')
            .text('View Result')
            .click(function(){
                viewPlaytestData(historyInfo.gameName,history.deckName,trainVersionText.text())
                $('.playtest-history-entry')
                    .css('color','')
                    .css('font-weight','')
                    .css('font-size','')
                $(this).parent()
                    .css('color','red')
                    .css('font-weight','bold')
                    .css('font-size','large')
            })
        //let delBtn = $(document.createElement('button')).attr('class','col-2 btn btn-danger').text('Retest')
        entryRoot.append(space,trainVersionText,winrateText, gameNumText,viewResBtn)
        return entryRoot
    }
}

function onClickPlaytest(){
    let gameNums = $('#playtest-game-num').val()
    let gameName = dbmanager.getCurrentGameName()
    let deckName = currentGameData.rules.deck
    let trainVersion = $('#AI-dropdown-btn').text()

    if(!dbmanager.getAllTrainedVersion(gameName,deckName).includes(trainVersion)){
        popupWarning("must select correct AI to playtest!")
        return 
    }
    $('#playtest-btn').addClass('d-none')
    $('#playtest-config-div').addClass('d-none')
    $('#playtest-history-div').addClass('d-none')
    $('#data-display-root').addClass('d-none')

    $('#playtest-progress').removeClass('d-none')
    $('#playtest-status').removeClass('d-none')

    console.log('Playtst: [train ver]-'+trainVersion)
    let pyProcess = new PythonProcess(
        12,
        {'train_version': trainVersion,'game_nums':gameNums},
	    function () { console.log('success!') },
        onReceivePlaytestMesssage,
        function(err){popupWarning(err)})
    $('#playtest-status').text('load trained AI modal...')
}

function onReceivePlaytestMesssage(data){
    simulateInfo = JSON.parse(data).content
    let curprogress =   simulateInfo.curprogress
    let maxprogress =  simulateInfo.maxprogress
    let percentage = Math.ceil(100*curprogress/maxprogress)
    $('#playtest-status').text('Is playtesting...')
    $('#playtest-progress-bar').attr("class","c100 p"+percentage)
    $('#playtest-progress-text').text(curprogress+'/'+maxprogress)
    if(simulateInfo.is_finished){
        let gamename= dbmanager.getCurrentGameName()
        let deckname = currentGameData.rules.deck
        let trainVersion = $('#AI-dropdown-btn').text()
        dbmanager.recordPlaytestHistory(gamename,deckname,maxprogress,trainVersion)
        updatePlaytestPage()
        viewPlaytestData(gamename,deckname, trainVersion)
    }
}

function viewPlaytestData(gamename,deckname,trainVersion){
    let playtestData = dbmanager.loadPlaytestData(gamename,deckname,trainVersion)
    console.log(playtestData)
    $('#playtest-btn').removeClass('d-none')
    $('#playtest-config-div').removeClass('d-none')
    $('#playtest-history-div').removeClass('d-none')
    $('#data-display-root').removeClass('d-none')
    
    $('#playtest-progress').addClass('d-none')
    $('#playtest-status').addClass('d-none')

    let basicStats = playtestData.basicStats
    // set wintrate graph
    $('#win-rate-text').text((basicStats.win_rate*100).toFixed(2)+'%')
    let percentage = Math.ceil(basicStats.win_rate*100)
    $('#win-rate-progress').attr("class","green c100 p"+percentage)

    // draw distributions
    drawDistribution("v-pills-game-len")
    // $('#avg-game-len').text("average game length: "+basicStats.avg_game_length)
    $('#avg-boss-hp').text("average boss hp: "+basicStats.avg_boss_hp)
    $('#avg-player-hp').text("average player hp: "+basicStats.avg_player_hp)

    // relationship heat map
    dataVisualizer.drawRelationshipTable(playtestData.card_relationship_csv_url,'card-relationship-table',gamename)
    
    //dataVisualizer.drawRankChart( playtestData.card_perfromance_csv_url,'Card Name','card-data-rankChart')
}

function drawDistribution(rootID){
    dataVisualizer.drawDistribution("../static/tempdistribution.csv",rootID)
}


module.exports ={onClickPlaytest,viewPlaytestData,updatePlaytestPage}