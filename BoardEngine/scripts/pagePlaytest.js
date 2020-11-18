const dataVisualizer = require('../scripts/dataVisualizer')
const dbmanager = require('../scripts/dbmanager')
const utils = require('../scripts/utils')
const cardRenderer = require('./cardRenderer')

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
    dataVisualizer.drawDistribution("../static/tempdistribution.csv","v-pills-game-len")
    dataVisualizer.drawDualDistribution("../static/tempdualdistribution.csv","v-pills-ending-hp")

    // card analysis
    drawCardAnalysisSection('card-analysis',playtestData)

    // relationship heat map
    dataVisualizer.drawRelationshipTable(playtestData.card_relationship_csv_url,'card-relationship-table',gamename)
    
    // top combos
    drawTopCombosSection('top-combo',gamename, playtestData.comboInfo)

    //dataVisualizer.drawRankChart( playtestData.card_perfromance_csv_url,'Card Name','card-data-rankChart')
}

function drawTopCombosSection(divID,gameName,comboInfo){
    let rootDiv = $('#'+divID)
    rootDiv.text("").append(createComboAnnoatationRow())
    let topNum = 5
    let curNum = 0
    for(let combo in comboInfo.trios){
        if(curNum >= topNum){
            break;
        }
        curNum++
        let names = parseCardNamesFromComboName(combo)
        let comboElement = createComboElement(names[0],names[1],names[2],comboInfo.trios[combo])
        rootDiv.append(comboElement)
    }

    function parseCardNamesFromComboName(comboName){
        return comboName.split('-')
    }

    function createComboAnnoatationRow(){
        let comboDiv = $(document.createElement('div'))
        .attr('class','row')

        let space = $(document.createElement('div')).attr('class','col-1')
        let occurNumber = $(document.createElement('div'))
            .attr('class','col-2')
            .append($(document.createElement('h1')).text("occurTimes"))
        
        comboDiv.append(space)
        .append(occurNumber)
        .append($(document.createElement('h1')).text("firstCard").attr('class','col-2'))
        .append($(document.createElement('div')).attr('class','col-1'))
        .append($(document.createElement('h1')).text("secondCard").attr('class','col-2'))
        .append($(document.createElement('div')).attr('class','col-1'))
        .append($(document.createElement('h1')).text("thirdCard").attr('class','col-2'))
        
        return comboDiv
    }

    function createComboElement(card1,card2,card3,occurTimes){
        let comboDiv = $(document.createElement('div'))
        .attr('class','row')
        .css('border-radius','20px')
        .css('margin-top','10px')
        .css('margin-bottom','10px')
        .css('margin-left','15px')
        .css('margin-right','15px')
        .css('background-color','white')

        let space = $(document.createElement('div')).attr('class','col-1')
        let occurNumber = $(document.createElement('div'))
            .attr('class','col-2')
            .append( $(document.createElement('h1')).text(occurTimes).attr('class','div-center'))
        comboDiv.append(space)
        .append(occurNumber)
        .append(cardRenderer.createCardElementByName(gameName,card1))
        .append($(document.createElement('div')).attr('class','col-1'))
        .append(cardRenderer.createCardElementByName(gameName,card2))
        .append($(document.createElement('div')).attr('class','col-1'))
        .append(cardRenderer.createCardElementByName(gameName,card3))
        return comboDiv
    }
}

function drawCardAnalysisSection(divID,playtestData){
    let sectionRoot = $('#'+divID).text("")
    for(let analysis of createCardAnalysises(playtestData)){
        sectionRoot.append(createCardAnalysisElement(analysis))
    }

    function createCardAnalysises(playtestData){
        let res  = []
        for(let i = 0; i <5;i++){
            res.push({"gameName":'Demo',"cardName":'Bash',"opportunity":0.2,"reward":2.3})
        }
        return res
    }
}

function createCardAnalysisElement(cardAnalysis){
    // create card elements
    let cardEle = cardRenderer.createCardElementByName(cardAnalysis.gameName,cardAnalysis.cardName)
    cardEle.attr('class','col-6')
    // creatte card attrs
    let cardAttrs = $(document.createElement('div')).addClass('col-6')
    let opportunityAttr = createCardAttrElement('Opportunity Utilize',23,'blue')
    let playPos = createCardAttrElement('Card Play Position',44,'red')
    let rewardAttr = createCardAttrElement('Average Reward',77,'yellow')
    let playCount = createCardAttrElement('PlayCount',22,'pink')
    cardAttrs.append(opportunityAttr,playPos, rewardAttr,playCount)
    // build final div
    let analysisDiv = $(document.createElement('div'))
    .addClass('row')
    .addClass('col-3')
    .css('border-radius','20px')
    .css('margin-top','10px')
    .css('margin-bottom','10px')
    .css('margin-left','30px')
    .css('background-color','white')
    .append(cardEle,cardAttrs)

    return analysisDiv

    function createCardAttrElement(attrName,attrValue,color){
        let nameTitle = $(document.createElement('h4')).text(attrName)
        let progressbar = $(document.createElement('div'))
        .attr('class','progress-bar')
        .attr('role','progressbar')
        .css('width',attrValue+'%')
        .css('background-color',color)
        let valueIndicator = $(document.createElement('div'))
        .css('height','6px')
        .attr('class','progress md-progress')
        .append(progressbar)

        let rootDiv = $(document.createElement('div'))
        .append(nameTitle,valueIndicator)
        return rootDiv
    }
}


module.exports ={onClickPlaytest,viewPlaytestData,updatePlaytestPage}