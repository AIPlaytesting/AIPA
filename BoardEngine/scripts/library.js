const dbmanager = require('../scripts/dbmanager')
const rootPath = require('electron-root-path').rootPath
const dataVisualizer = require('../scripts/dataVisualizer')
const cardRenderer = require('../scripts/cardRenderer')
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

    updateGameMainPage()

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
    $('#game-edit-section-overlay').removeClass('d-none')
    $('#train-btn').addClass('d-none')
    $('#train-spinner').removeClass('d-none')
    $('#train-status').text('load AI...')
    let pyProcess = new PythonProcess(11,
	    function () { console.log('success!') },
        onReceiveTrainMesssage)
}

function onReceiveTrainMesssage(data){
    trainInfo = JSON.parse(data).content
    let curprogress =  trainInfo.curprogress
    let maxprogress = trainInfo.maxprogress
    console.log('recevice!')
    $('#train-progress').attr("style","width:"+(curprogress*100/maxprogress)+"%")
    $('#train-progress-text').text(curprogress + "/" + maxprogress)
    $('#train-status').text('Remaining Time :  ' + trainInfo.remaining_hours + ' Hrs ' + trainInfo.remaining_minutes + ' Min.')
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
    let deckname = currentGameData.rules.deck
    let cardname =  $('#newcard-name-dropdown').text()
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
    updateGameMainPage()
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
    $('#playtest-btn').addClass('d-none')
    $('#playtest-spinner').removeClass('d-none')
    $('#data-status').removeClass('d-none')
    $('#data-display-root').addClass('d-none')
    let pyProcess = new PythonProcess(12,
	    function () { console.log('success!') },
        onReceivePlaytestMesssage)
    $('#data-status').text('Is playtesting...')
}

function onReceivePlaytestMesssage(data){
    simulateInfo = JSON.parse(data).content
    let curprogress =   simulateInfo.curprogress
    let maxprogress =  simulateInfo.maxprogress
    $('#playtest-progress-bar').attr("style","width:"+(curprogress*100/maxprogress)+"%")
    $('#playtest-progress-text').text(curprogress+'/'+maxprogress)
    if(simulateInfo.curprogress >= simulateInfo.maxprogress){
        onFinishPlaytest()
    }
}

function onFinishPlaytest(){
    $('#playtest-btn').removeClass('d-none')
    $('#playtest-spinner').addClass('d-none')
    $('#data-status').addClass('d-none')
    $('#data-display-root').removeClass('d-none')
    // draw data
    let data = [
        [
          {"area": "winrate ", "value": 100*Math.random()},
          {"area": "player HP", "value": 100*Math.random()},
          {"area": "boss HP", "value": 100*Math.random()},
          {"area": "average turns", "value": 100*Math.random()},
          ]
      ]
    let radarColors= ["#69257F", "#CA0D59", "#CA0D19", "#CA1D52"]
    dataVisualizer.drawRadarChart('playtest-radar-chart',data,radarColors)
    dataVisualizer.drawRankChart("../static/card.csv",'card-data-rankChart')
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
    entryBtn.text("+")
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
function updateGameMainPage(){
    let gameName = dbmanager.getCurrentGameName()
    currentGameData = dbmanager.loadGameData(gameName)
    let gameData = currentGameData
    //console.log(gameData)
    $('#game-title').text(gameName)
    $('#deck-count').text(Object.keys(gameData.decks).length)
    $('#card-count').text(Object.keys(gameData.cards).length)
    $('#buff-count').text(gameData.buffInfo.registered_buffnames.length)

    updateDropdownList('newcard-name-list','newcard-name-dropdown',Object.keys(gameData.cards))
    updateDeckDropdown()
    updateDeckTemplateList()

    renderCardGrid()

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
        let rootDiv = $(document.createElement('div')).attr('class','col-2')
        let addCardBtn = $(document.createElement('button'))
        .text('+new card')
        .attr('class','btn btn-dark div-center')
        .css('width','100px')
        .css('height','150px')
        .attr('data-toggle','modal')
        .attr('data-target','#add-card-modal')
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

    function updateDeckTemplateList(){
        let deckTemplateList = $("#deck-template-list");
        deckTemplateList.text("");
        $('#deck-template-dropdown').text("please select a template")
        for(deckName in currentGameData.decks){
            // create deck template option button
            let templateOptionBtn =$(document.createElement('button'))
            templateOptionBtn.attr('class','dropdown-item')
            templateOptionBtn.text(deckName)
            templateOptionBtn.click(function(){
                $('#deck-template-dropdown').text($(this).text())
            })
            deckTemplateList.append(templateOptionBtn)
        }
    }

    function updateDropdownList(dropdownMenuID,dropwdownBtnID,options){
        let dropdownMenu = $("#"+dropdownMenuID);
        dropdownMenu .text("");
        $('#'+dropwdownBtnID).text("please select")
        for(option of options){
            let optionBtn =$(document.createElement('button'))
            .attr('class','dropdown-item')
            .text(option)
            .click(function(){
                $('#'+dropwdownBtnID).text($(this).text())
            })
            dropdownMenu .append(optionBtn)
        }
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