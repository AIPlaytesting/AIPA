const dataVisualizer = require('../scripts/dataVisualizer')
const dbmanager = require('../scripts/dbmanager')
const utils = require('../scripts/utils')
const cardRenderer = require('./cardRenderer')

function updatePlaytestPage() {
    utils.setupDropdown(
        'AI-dropdown-list',
        'AI-dropdown-btn',
        dbmanager.getAllTrainedVersion(dbmanager.getCurrentGameName(), currentGameData.rules.deck))
    updatePlaytestHistory()

    function updatePlaytestHistory() {
        $('#playtest-history-list').text("").append(createInfoEntry())
        for (let history of dbmanager.getPlaytestHistory(dbmanager.getCurrentGameName(), currentGameData.rules.deck)) {
            $('#playtest-history-list').append(createHistoryEntry(history))
        }
    }

    function createInfoEntry() {
        let entryRoot = $(document.createElement('div'))
            .attr('class', 'row playtest-history-entry')
            .css('border-radius', '10px;')
        let space = $(document.createElement('span')).attr('class', 'col-1')
        let trainVersionText = $(document.createElement('span'))
            .attr('class', 'col-3')
            .text("AI version")
            .css('font-weight', 'bold')
        let winrateText = $(document.createElement('span'))
            .attr('class', 'col-2')
            .text("winrate")
            .css('font-weight', 'bold')
        let gameNumText = $(document.createElement('span'))
            .attr('class', 'col-2')
            .text("number of games")
            .css('font-weight', 'bold')
        entryRoot.append(space, trainVersionText, winrateText, gameNumText)
        return entryRoot
    }

    function createHistoryEntry(historyInfo) {
        let entryRoot = $(document.createElement('div'))
            .attr('class', 'row playtest-history-entry')
            .css('border-radius', '10px;')
        let space = $(document.createElement('span')).attr('class', 'col-1')
        let trainVersionText = $(document.createElement('span')).attr('class', 'col-3').text(historyInfo.trainVersion)
        let playtestData = dbmanager.loadPlaytestData(historyInfo.gameName, historyInfo.deckName, historyInfo.trainVersion)
        let winrateStr = (playtestData.basicStats.win_rate * 100).toFixed(2) + '%'
        let winrateText = $(document.createElement('span')).attr('class', 'col-2').text(winrateStr)
        let gameNumText = $(document.createElement('span')).attr('class', 'col-2').text(historyInfo.gameNums)
        let viewResBtn = $(document.createElement('button'))
            .attr('class', 'col-2 btn btn-primary')
            .text('View Result')
            .click(function () {
                viewPlaytestData(historyInfo.gameName, history.deckName, trainVersionText.text())
                $('.playtest-history-entry')
                    .css('color', '')
                    .css('font-weight', '')
                    .css('font-size', '')
                $(this).parent()
                    .css('color', 'red')
                    .css('font-weight', 'bold')
                    .css('font-size', 'large')
            })
        //let delBtn = $(document.createElement('button')).attr('class','col-2 btn btn-danger').text('Retest')
        entryRoot.append(space, trainVersionText, winrateText, gameNumText, viewResBtn)
        return entryRoot
    }
}

function onClickPlaytest() {
    let gameNums = $('#playtest-game-num').val()
    let gameName = dbmanager.getCurrentGameName()
    let deckName = currentGameData.rules.deck
    let trainVersion = $('#AI-dropdown-btn').text()

    if (!dbmanager.getAllTrainedVersion(gameName, deckName).includes(trainVersion)) {
        popupWarning("must select correct AI to playtest!")
        return
    }
    $('#playtest-btn').addClass('d-none')
    $('#playtest-config-div').addClass('d-none')
    $('#playtest-history-div').addClass('d-none')
    $('#data-display-root').addClass('d-none')

    $('#playtest-progress').removeClass('d-none')
    $('#playtest-status').removeClass('d-none')

    console.log('Playtst: [train ver]-' + trainVersion)
    let pyProcess = new PythonProcess(
        12,
        { 'train_version': trainVersion, 'game_nums': gameNums },
        function () { console.log('success!') },
        onReceivePlaytestMesssage,
        function (err) { popupWarning(err) })
    $('#playtest-status').text('Loading...')
}

function onReceivePlaytestMesssage(data) {
    simulateInfo = JSON.parse(data).content
    let curprogress = simulateInfo.curprogress
    let maxprogress = simulateInfo.maxprogress
    let percentage = Math.ceil(100 * curprogress / maxprogress)
    $('#playtest-status').text('Playtesting...')
    $('#playtest-progress-bar').attr("class", "c100 p" + percentage)
    $('#playtest-progress-text').text(curprogress + '/' + maxprogress)
    if (simulateInfo.is_finished) {
        let gamename = dbmanager.getCurrentGameName()
        let deckname = currentGameData.rules.deck
        let trainVersion = $('#AI-dropdown-btn').text()
        dbmanager.recordPlaytestHistory(gamename, deckname, maxprogress, trainVersion)
        updatePlaytestPage()
        viewPlaytestData(gamename, deckname, trainVersion)
    }
}

function viewPlaytestData(gamename, deckname, trainVersion) {
    let playtestData = dbmanager.loadPlaytestData(gamename, deckname, trainVersion)
    console.log(playtestData)
    $('#playtest-btn').removeClass('d-none')
    $('#playtest-config-div').removeClass('d-none')
    $('#playtest-history-div').removeClass('d-none')
    $('#data-display-root').removeClass('d-none')

    $('#playtest-progress').addClass('d-none')
    $('#playtest-status').addClass('d-none')

    let basicStats = playtestData.basicStats
    // set wintrate graph
    $('#win-rate-text').text((basicStats.win_rate * 100).toFixed(2) + '%')
    let percentage = Math.ceil(basicStats.win_rate * 100)
    $('#win-rate-progress').attr("class", "green c100 p" + percentage)

    // draw distributions
    dataVisualizer.drawDistribution(playtestData.game_len_distribution_csv_url, "v-pills-game-len")
    dataVisualizer.drawDualDistribution(playtestData.hp_distribution_csv_url, "v-pills-ending-hp")

    // card analysis
    drawCardAnalysisSection(playtestData)

    // relationship heat map
    dataVisualizer.drawRelationshipTable(playtestData.card_relationship_csv_url, 'card-relationship-table', gamename)

    // top combos
    drawTopCombosSection('top-combo', gamename, playtestData.comboInfo)

    // nomalies
    DrawAnomiliesSection(playtestData)
}

function drawTopCombosSection(divID, gameName, comboInfo) {
    let rootDiv = $('#' + divID)
    rootDiv.text("").append(createComboAnnoatationRow())
    let topNum = 5
    let rankedCombos = []
    for (let combo in comboInfo.trios) {
        rankedCombos.push(combo)
    }
    for (let i = rankedCombos.length - 1; i >= 0 && i > rankedCombos.length - topNum - 1; i--) {
        let combo = rankedCombos[i]
        let names = parseCardNamesFromComboName(combo)
        let comboElement = createComboElement(names[0], names[1], names[2], comboInfo.trios[combo])
        rootDiv.append(comboElement)
    }
    // for(let combo in comboInfo.trios){
    //     if(curNum >= topNum){
    //         break;
    //     }
    //     curNum++
    //     let names = parseCardNamesFromComboName(combo)
    //     let comboElement = createComboElement(names[0],names[1],names[2],comboInfo.trios[combo])
    //     rootDiv.append(comboElement)
    // }

    function parseCardNamesFromComboName(comboName) {
        return comboName.split('-')
    }

    function createComboAnnoatationRow() {
        let comboDiv = $(document.createElement('div'))
            .attr('class', 'row')

        let space = $(document.createElement('div')).attr('class', 'col-1')
        let occurNumber = $(document.createElement('div'))
            .attr('class', 'col-2')
            .append($(document.createElement('h1')).text("Occur Times"))

        comboDiv.append(space)
            .append(occurNumber)
            .append($(document.createElement('h1')).text("1st Card").attr('class', 'col-2'))
            .append($(document.createElement('div')).attr('class', 'col-1'))
            .append($(document.createElement('h1')).text("2nd Card").attr('class', 'col-2'))
            .append($(document.createElement('div')).attr('class', 'col-1'))
            .append($(document.createElement('h1')).text("3rd Card").attr('class', 'col-2'))

        return comboDiv
    }

    function createComboElement(card1, card2, card3, occurTimes) {
        let comboDiv = $(document.createElement('div'))
            .attr('class', 'row')
            .css('border-radius', '20px')
            .css('margin-top', '10px')
            .css('margin-bottom', '10px')
            .css('margin-left', '15px')
            .css('margin-right', '15px')
            .css('background-color', 'white')

        let space = $(document.createElement('div')).attr('class', 'col-1')
        let occurNumber = $(document.createElement('div'))
            .attr('class', 'col-2')
            .append($(document.createElement('h1')).text(occurTimes).attr('class', 'div-center'))
        comboDiv.append(space)
            .append(occurNumber)
            .append(cardRenderer.createCardElementByName(gameName, card1))
            .append($(document.createElement('div')).attr('class', 'col-1'))
            .append(cardRenderer.createCardElementByName(gameName, card2))
            .append($(document.createElement('div')).attr('class', 'col-1'))
            .append(cardRenderer.createCardElementByName(gameName, card3))
        return comboDiv
    }
}

function drawCardAnalysisSection(playtestData) {
    dataVisualizer.drawHistorgram(playtestData.card_perfromance_csv_url, 'Card Name', 'Card Utilization', 'card-utilization-histogram', 'red')
    dataVisualizer.drawHistorgram(playtestData.card_perfromance_csv_url, 'Card Name', 'Avg Play Position', 'card-playpos-histogram', 'green')
    dataVisualizer.drawHistorgram(playtestData.card_perfromance_csv_url, 'Card Name', 'Card Play Count', 'card-playcount-histogram', 'blue')

    let sectionRoot = $('#card-analysis-list').text("")
    for (let analysis of createCardAnalysises(playtestData)) {
        sectionRoot.append(createCardAnalysisElement(analysis))
    }

    function createCardAnalysises(playtestData) {
        let res = []
        for (let cardName in playtestData.cardAnalysis) {
            let cardAnalysis = {
                "gameName": playtestData.gameName,
                "cardName": cardName,
                "cardUtilization": playtestData.cardAnalysis[cardName].card_utilization,
                "playPos": playtestData.cardAnalysis[cardName].avg_play_pos,
                "playCount": playtestData.cardAnalysis[cardName].card_play_count,
            }
            res.push(cardAnalysis)
        }
        return res
    }
}

function DrawAnomiliesSection(playtestData) {
    $('#anomalies').text("")
    for (let anomalyName in playtestData.anomalies) {
        $('#anomalies').append(createAnomalyElement(playtestData.gameName, anomalyName, playtestData.anomalies[anomalyName]))
    }
}

function createAnomalyElement(gameName, anomalyName, anomalyData) {
    cardRenderer.setCachedGameData(gameName)

    console.log(anomalyData)
    let rootDiv = $(document.createElement('div'))
    let collapseHead =$( document.createElement('div')).addClass('row')
    let collapseBtn = $(document.createElement('button'))
        .text(anomalyName)
        .addClass('btn')
        .addClass('inner-section')
        .addClass('col-12')
        .attr('data-toggle', 'collapse')
        .attr('data-target', '#' + anomalyName + '-collapse')

    let collapseDiv = $(document.createElement('div'))
        .attr('id', anomalyName + '-collapse')
        .addClass('collapse')
    collapseHead.append(collapseBtn)
    rootDiv.append(collapseHead, collapseDiv)
    for (let turnName in anomalyData.game_states) {
        collapseDiv.append(createTurnElement(turnName, anomalyData.game_states[turnName]))
        collapseDiv.append($(document.createElement('hr')))
    }
    return rootDiv

    function createTurnElement(turnName, turnData) {
        let rootDiv = $(document.createElement('div')).addClass("row")
        let turnTitle = $(document.createElement('h1')).text(turnName)
            .addClass('col-1')
            .css('border-right', '5px solid grey')
        rootDiv.append(turnTitle)
        for (let step in turnData) {
            let stepDiv = $(document.createElement('div'))
                //.css('border-style','dotted')
                .attr('class', 'col-3 row')

            // create elements for this step
            let stepData = turnData[step]
            let cardName = stepData.card_played
            if (cardName != 'End Turn') {
                let cardImg = cardRenderer.createCardElementByCaching(stepData.card_played)
                    .attr("class", "col-3")

                let detailInfo = createStepDetailInfoElement2(stepData)

                // create arrow
                // let arrow = $(document.createElement('img'))
                // .attr('class','col-1')
                // .attr('src','../static/right-arrow.png')
                // .css('height','20px')
                // .css('width','100px')
                // .css('margin-top','80px')

                stepDiv.append(cardImg, detailInfo)
                rootDiv.append(stepDiv)
            }
            else {
                let endTurnSign = $(document.createElement('div'))
                    .text('End Turn')
                    .attr('class', 'col-1')
                rootDiv.append(endTurnSign)
            }
        }
        return rootDiv
    }

    function createStepDetailInfoElement2(stepData) {
        let rootDiv = $(document.createElement('div'))
            .attr('class', 'overflow-auto col-6')
            .css('height', '200px')
            .css('margin-left', '50px')

        let page1 = $(document.createElement('div'))
            .css('height', '200px')
            .addClass('inner-section')

        let playerHPbar = utils.createProgressBar(stepData.player_health,100)
        let bossHPbar = utils.createProgressBar(stepData.boss_health,240)

        page1.append($(document.createElement('h4')).text("Player HP: " + stepData.player_health))
            .append(playerHPbar)
            .append($(document.createElement('h4')).text("Boss HP: " + stepData.boss_health))
            .append(bossHPbar)
            .append($(document.createElement('h4')).text("Boss Intent: " + stepData.boss_intent))

        // fill page 2: card name list
        let page2 = $(document.createElement('div'))
            .addClass('inner-section')
            .append($(document.createElement('h4')).text("Available Cards: "))
        let cardNameList = $(document.createElement('ul'))
        for (let cardName of stepData.available_cards) {
            cardNameList.append($(document.createElement('li')).text(cardName))
        }
        page2.append(cardNameList)

        let page3 = $(document.createElement('div'))
            .addClass('inner-section')
        page3.append($(document.createElement('h4')).text("Player Buffs"))
        for (let buffName of stepData.player_buffs) {
            page3.append($(document.createElement('p')).text(buffName))
        }
        page3.append($(document.createElement('h4')).text("Boss Buffs"))
        for (let buffName of stepData.boss_buffs) {
            page3.append($(document.createElement('p')).text(buffName))
        }

        return rootDiv.append(page1, page2, page3)
    }
    function createStepDetailInfoElement(stepData) {
        let rootDiv = $(document.createElement('div')).addClass('col-2')
        let page1 = $(document.createElement('div'))
            .css('height', '200px')
            .text('page1')
        let page2 = $(document.createElement('div'))
            .css('height', '200px')
            .addClass('d-none')
            .text('page2')
        let page3 = $(document.createElement('div'))
            .css('height', '200px')
            .addClass('d-none')
            .text('page3')

        let buttonList = $(document.createElement('div')).addClass('row')
        // create turn page btn
        let pageBtn1 = $(document.createElement('button'))
            .append($(document.createElement('span')).addClass('bs-stepper-circle').text(1))
            .addClass('col-4')
            .addClass('btn')
            .click(function () {
                page1.removeClass('d-none')
                page2.addClass('d-none')
                page3.addClass('d-none')
            })
        let pageBtn2 = $(document.createElement('button'))
            .append($(document.createElement('span')).addClass('bs-stepper-circle').text(2))
            .addClass('col-4')
            .addClass('btn')
            .click(function () {
                page2.removeClass('d-none')
                page1.addClass('d-none')
                page3.addClass('d-none')
            })
        let pageBtn3 = $(document.createElement('button'))
            .append($(document.createElement('span')).addClass('bs-stepper-circle').text(3))
            .addClass('col-4')
            .addClass('btn')
            .click(function () {
                page3.removeClass('d-none')
                page2.addClass('d-none')
                page1.addClass('d-none')
            })

        buttonList.append(pageBtn1, pageBtn2, pageBtn3)

        rootDiv.append(page1, page2, page3, buttonList)
        return rootDiv
    }
}

function createCardAnalysisElement(cardAnalysis) {
    // create card elements
    let cardEle = cardRenderer.createCardElementByName(cardAnalysis.gameName, cardAnalysis.cardName)
    cardEle.attr('class', 'col-6')
    // creatte card attrs
    let cardAttrs = $(document.createElement('div')).addClass('col-6')
    let opportunityAttr = createCardAttrElement('Opportunity Utilize', cardAnalysis.cardUtilization * 100, 'blue', true)
    let playPos = createCardAttrElement('Card Play Position', 100 * (cardAnalysis.playPos / 3), 'red', true)
    let playCount = createCardAttrElement('PlayCount', cardAnalysis.playCount, 'black')
    cardAttrs.append(opportunityAttr, playPos, playCount)
    // build final div
    let analysisDiv = $(document.createElement('div'))
        .addClass('row')
        .addClass('col-3')
        .css('border-radius', '20px')
        .css('margin-top', '10px')
        .css('margin-bottom', '10px')
        .css('margin-left', '30px')
        .css('background-color', 'white')
        .append(cardEle, cardAttrs)

    return analysisDiv

    function createCardAttrElement(attrName, attrValue, color, useBar = false) {
        let nameTitle = $(document.createElement('h4')).text(attrName)
        let valueIndicator
        if (useBar) {
            attrValue = parseInt(attrValue)
            let progressbar = $(document.createElement('div'))
                .attr('class', 'progress-bar')
                .attr('role', 'progressbar')
                .css('width', attrValue + '%')
                .css('background-color', color)
            valueIndicator = $(document.createElement('div'))
                .css('height', '6px')
                .attr('class', 'progress md-progress')
                .append(progressbar)
        }
        else {
            valueIndicator = $(document.createElement('h3')).text(attrValue).css('color', color)
        }
        let rootDiv = $(document.createElement('div'))
            .append(nameTitle, valueIndicator)
        return rootDiv
    }
}


module.exports = { onClickPlaytest, viewPlaytestData, updatePlaytestPage }