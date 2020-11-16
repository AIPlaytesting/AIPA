const dbmanager = require('../scripts/dbmanager')
const rootPath = require('electron-root-path').rootPath
const dataVisualizer = require('../scripts/dataVisualizer')
const cardRenderer = require('../scripts/cardRenderer')
const utils = require('../scripts/utils')
const PythonProcess = require('../Scripts/pythonProcess.js')

var currentGameData = {}

function refreshLibraryPage(){
    console.log("refresh!")
    dbmanager.loadDB(onFinishDBLoad)
}

function onFinishDBLoad(){
    let installedGames = dbmanager.getInstalledGameApps()
    // fill game lib list
    let gameEntryList = $("#game-entry-list")
    gameEntryList.text("")
    for(gameName of installedGames){
        gameEntryList.append(createLibraryEntry(gameName))
    }
    // set game create button
    gameEntryList.append(createNewGameBtn())
    
    updateGameTemplateList()

    $('#create-new-game-btn').off()
    $('#create-new-game-btn').click(function(){onClickCreateNewGame()})

    // refresh design page
    updateDesignPage()
    // also update playtest
    updatePlaytestPage()

    function updateGameTemplateList(){
        let gameTemplateList = $("#game-template-list");
        gameTemplateList.text("");
        $('#game-template-dropdown').text("please select a template")
        for(gameName of installedGames){
            // create game template option button
            let templateOptionBtn =$(document.createElement('button'))
            templateOptionBtn.attr('class','dropdown-item')
            templateOptionBtn.text(gameName)
            templateOptionBtn.click(function(){
                $('#game-template-dropdown').text($(this).text())
            })
            gameTemplateList.append(templateOptionBtn)
        }
    }
}

function onClickPlay(){
    let child = require('child_process').execFile;
    let executablePath = rootPath + '/executables/unitybuild/AIPA.exe';
    console.log('launch unity at: '+executablePath)
    child(executablePath, function(err, data) {
        if(err){
           console.error(err);
           return;
        }
     
        console.log(data.toString());
    });  
}

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

function onClickCreateNewGame(){
    let templateName = $('#game-template-dropdown').text()
    let newGameName  = $('#new-game-name-input').val()
    if(newGameName  == ""){
        popupWarning("game name cannot be empty!")
        return
    }

    try {
        dbmanager.createNewGame(templateName, newGameName,refreshLibraryPage)
    } catch (error) {
        popupWarning(error)
    }
}

function onClickCreateNewDeck(){
    let templateName = $('#deck-template-dropdown').text()
    let newDeckName = $('#new-deck-name-input').val()
    if(newDeckName  == ""){
        popupWarning("deck name cannot be empty!")
        return
    }

    try {
        dbmanager.createNewDeckOnCurrentGame(templateName, newDeckName)
        refreshLibraryPage()
        onSwitchCurrentDeck(newDeckName)
    } catch (error) {
        popupWarning(error)
    }
}

function onClickAddNewCard(){
    const defaultText = 'please select'
    let deckname = currentGameData.rules.deck
    let cardname =  $('#newcard-name-dropdown').text()
    if(cardname ==defaultText){
        popupWarning('need to select a card to add!')
        return 
    }
    let newCardCopies = 1
    if(cardname in currentGameData.decks[deckname]){
        newCardCopies =  currentGameData.decks[deckname][cardname]+1
    }
    dbmanager.modifyDeck(deckname,cardname,newCardCopies)
    refreshLibraryPage()
}

function onClickRemoveCard(cardname){
    let deckname = currentGameData.rules.deck
    let newCardCopies = 1
    if(cardname in currentGameData.decks[deckname]){
        newCardCopies =  currentGameData.decks[deckname][cardname] - 1
        if(newCardCopies < 0){
            newCardCopies = 0
        }
        dbmanager.modifyDeck(deckname,cardname,newCardCopies)
        refreshLibraryPage()
    }
    else{
        console.log(cardname+'doesnt exist!')
    }
}

function onClickLibraryGameEntry(gameName){
    dbmanager.setCurrentGame(gameName)
    refreshLibraryPage()
}

function onClickRemoveGame(){
    let currentGameName = dbmanager.getCurrentGameName()
    console.log("game to delete: "+currentGameName)
    popupConfirmDialog("Calm down",
    "are you sure to delete: "+currentGameName,
    function(){
        try{
            dbmanager.removeGame(currentGameName,refreshLibraryPage)
        }
        catch(error){
            popupWarning(error)
        }
    }
    )
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
    $('#playtest-progress').removeClass('d-none')
    $('#playtest-status').removeClass('d-none')
    $('#data-display-root').addClass('d-none')
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
        viewPlaytestData(gamename,deckname, trainVersion)
    }
}

function viewPlaytestData(gamename,deckname,trainVersion){
    let playtestData = dbmanager.loadPlaytestData(gamename,deckname,trainVersion)
    console.log(playtestData)
    $('#playtest-btn').removeClass('d-none')
    $('#playtest-config-div').removeClass('d-none')
    $('#playtest-progress').addClass('d-none')
    $('#playtest-status').addClass('d-none')
    $('#data-display-root').removeClass('d-none')

    let basicStats = playtestData.basicStats
    // set wintrate graph
    $('#win-rate-text').text(basicStats.win_rate*100+'%')
    let percentage = Math.ceil(basicStats.win_rate*100)
    $('#win-rate-progress').attr("class","green c100 p"+percentage)
    $('#avg-game-len').text("average game length: "+basicStats.avg_game_length)
    $('#avg-boss-hp').text("average boss hp: "+basicStats.avg_boss_hp)
    $('#avg-player-hp').text("average player hp: "+basicStats.avg_player_hp)

    // relationship heat map
    dataVisualizer.drawRelationshipTable(playtestData.card_relationship_csv_url,'card-relationship-table')
    dataVisualizer.drawRankChart( playtestData.card_perfromance_csv_url,'Card Name','card-data-rankChart')
}

function onSwitchCurrentDeck(deckName){
    console.log("switch to: "+deckName)
    if(deckName != currentGameData.rules.deck){
        dbmanager.updateGameData(dbmanager.getCurrentGameName(),"currentDeck",deckName,refreshLibraryPage)
    }
}

function createLibraryEntry(gameName){
    let entryBtn =$(document.createElement('button'))
    entryBtn.text(gameName)
    entryBtn.attr('class',"btn btn-light tab-v")
    entryBtn.click(function(){
        $(".tab-v").removeClass('active')
        $(this).addClass('active')
        onClickLibraryGameEntry(gameName)})
    return entryBtn
}

function createNewGameBtn(){
    let container = $(document.createElement('div'))
    let entryBtn =$(document.createElement('button'))
        .text("+")
        .attr('class',"btn btn-dark")
        .attr('data-toggle','modal')
        .attr('data-target','#create-game-modal')
        .css('width','50px')
        .css('position','absolute')
        .css('right','0px')
        .addClass('text-center')
    container.append(entryBtn)
    return container;
}

// update main page based on current game in manifest
function updateDesignPage(){
    let gameName = dbmanager.getCurrentGameName()
    currentGameData = dbmanager.loadGameData(gameName)
    let gameData = currentGameData
    // lock the deck edit if it is locked 
    if(gameData.rules.locked_decks.includes(gameData.rules.deck)){
        $('#game-edit-section-overlay').removeClass('d-none')
    }
    else{
        $('#game-edit-section-overlay').addClass('d-none')
    }
    $('#game-title').text(gameName)
    updateGameSettingSection()

    utils.setupDropdown('newcard-name-list','newcard-name-dropdown',Object.keys(gameData.cards))
    utils.setupDropdown('deck-template-list','deck-template-dropdown',Object.keys(gameData.decks))

    updateDeckDropdown()

    renderCardGrid()

    function updateGameSettingSection(){
        $('#deck-count').text(Object.keys(gameData.decks).length)
        $('#card-count').text(Object.keys(gameData.cards).length)
        $('#buff-count').text(gameData.buffInfo.registered_buffnames.length)
        utils.setupSlider('player-hp-slider','player-hp-slider-value',30,100)
        utils.setupSlider('boss-hp-slider','boss-hp-slider-value',100,400)
    }

    function renderCardGrid(){
        let deckImgView = $('#deck-img-view')
        deckImgView.text("")
        let currentDeckinfo = gameData.decks[gameData.rules.deck]
        // create card info
        let currentImgRow = $(document.createElement('div'))
        currentImgRow.attr('class',"row")
        let currentImgRowCount = 0
        let maxImgRowCount = 6
        for(let cardName in currentDeckinfo){
            if(gameData.cards[cardName] == undefined){
                console.error(cardName+' is undefined in cards')
                continue
            }

            let cardCopies = currentDeckinfo[cardName]
            let cardImgFullPath = "../static/defaultcard.png"
            if( "img_relative_path" in gameData.cards[cardName]){
                let cardImgRelativePath = gameData.cards[cardName].img_relative_path
                cardImgFullPath = dbmanager.getResourceRoot()+'\\'+cardImgRelativePath
            }
    
            for(i = 0; i <cardCopies; i++){
                // check row change
                if(currentImgRowCount >= maxImgRowCount){
                    deckImgView.append(currentImgRow)
                    currentImgRow = $(document.createElement('div'))
                    currentImgRow.attr('class',"row")
                    currentImgRowCount = 0
                }
                currentImgRowCount += 1
                // render card
                let cardObj = gameData.cards[cardName]
                let imgDiv = cardRenderer.createCardElement(
                    cardImgFullPath,
                    cardName,
                    cardObj.description,
                    cardObj.energy_cost,
                    function(){onClickRemoveCard(cardName)})
                currentImgRow.append(imgDiv)   
            }
        }
        // add create new card buttons

        // check row change
        if(currentImgRowCount >= maxImgRowCount){
            deckImgView.append(currentImgRow)
            currentImgRow = $(document.createElement('div'))
            currentImgRow.attr('class',"row")
            currentImgRowCount = 0
        }
        currentImgRow.append(createAddNewCardDiv())   

        // add the last row 
        deckImgView.append(currentImgRow)
    }

    function createAddNewCardDiv(){
        let rootDiv = $(document.createElement('div'))
            .attr('class','col-2')
        let addCardImg = $(document.createElement('img'))
            .attr('src','../static/add.png')
            .css('width','100%')
            .css('height','70%')
        let addCardBtn = $(document.createElement('button'))
            .attr('class','btn')
            .css('width','160px')
            .css('height','220px')
            .attr('data-toggle','modal')
            .attr('data-target','#add-card-modal')
            .append(addCardImg)
        rootDiv.append(addCardBtn)   
        return rootDiv
    }

    function updateDeckDropdown(){
        $('#current-deck-dropdown-btn').text(currentGameData.rules.deck)
        let deckList = $('#current-deck-dropdown-list')
        deckList.text("")
        for(let deckName in currentGameData.decks){
            let deckSwitchBtn = $(document.createElement('button'))
            deckSwitchBtn.text(deckName)
            deckSwitchBtn.click(function(){onSwitchCurrentDeck(deckName)})
            deckSwitchBtn.attr('class','dropdown-item')
            deckList.append(deckSwitchBtn)
        }
    }
}

function updatePlaytestPage(){
    utils.setupDropdown(
        'AI-dropdown-list',
        'AI-dropdown-btn',
        dbmanager.getAllTrainedVersion(dbmanager.getCurrentGameName(),currentGameData.rules.deck))
    updatePlaytestHistory()

    function updatePlaytestHistory(){
        $('#playtest-history-list').text("")
        for(i = 0; i <5;i++){
            $('#playtest-history-list').append(createHistoryEntry())
        }
    }

    function createHistoryEntry(){
        let entryRoot = $(document.createElement('div'))
            .attr('class','row playtest-history-entry')
            .css('border-radius','10px;')
        let deckText = $(document.createElement('span')).attr('class','col-3 text-center').text("Deck 1")
        let timeText = $(document.createElement('span')).attr('class','col-3').text("11-Oct-10-23")
        let viewResBtn = $(document.createElement('button'))
            .attr('class','col-2 btn btn-primary')
            .text('View Result')
            .click(function(){
                viewPlaytestData('TestApp','deck1')
                $('.playtest-history-entry')
                    .css('color','')
                    .css('font-weight','')
                    .css('font-size','')
                $(this).parent()
                    .css('color','red')
                    .css('font-weight','bold')
                    .css('font-size','large')
            })
        let delBtn = $(document.createElement('button')).attr('class','col-2 btn btn-danger').text('Delete')
        entryRoot.append(deckText,timeText,viewResBtn,delBtn)
        return entryRoot
    }
}

function popupWarning(message){
    $('#warning-modal').modal()
    $('#warning-modal-body').text(message)
}

function popupConfirmDialog(title, message,onConfirmCallback){
    $('#confirm-modal').modal()
    $('#confirm-modal-title').text(title)
    $('#confirm-modal-body').text(message)
    $('#confirm-model-confirm-btn').off()
    $('#confirm-model-confirm-btn').click(function(){
        console.log("call back!")
        onConfirmCallback()})
}