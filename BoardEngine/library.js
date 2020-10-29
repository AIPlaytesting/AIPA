const dbmanager = require('./dbmanager.js');
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
    $('#create-new-game-btn').off()
    $('#create-new-game-btn').click(function(){onClickCreateNewGame()})

    updateGameMainPage()
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

function onSwitchCurrentDeck(deckName){
    console.log("switch to: "+deckName)
    if(deckName != currentGameData.rules.deck){
        dbmanager.updateGameData(dbmanager.getCurrentGameName(),"currentDeck",deckName,refreshLibraryPage)
    }
}

function createLibraryEntry(gameName){
    let entryBtn =$(document.createElement('button'))
    entryBtn.text(gameName)
    entryBtn.attr('class',"btn btn-light")
    entryBtn.click(function(){
        onClickLibraryGameEntry(gameName)})
    return entryBtn
}

function createNewGameBtn(){
    let entryBtn =$(document.createElement('button'))
    entryBtn.text("+New Game")
    entryBtn.attr('class',"btn btn-dark")
    entryBtn.attr('data-toggle','modal')
    entryBtn.attr('data-target','#create-game-modal')
    return entryBtn;
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
    let deckImgView = $('#deck-img-view')
    deckImgView.text("")
    let currentDeckinfo = gameData.decks[gameData.rules.deck]
    // create card info
    let currentImgRow = $(document.createElement('div'))
    currentImgRow.attr('class',"row")
    let currentImgRowCount = 0
    let maxImgRowCount = 4
    for(let cardName in currentDeckinfo){
        // check row change
        if(currentImgRowCount >= maxImgRowCount){
            deckImgView.append(currentImgRow)
            currentImgRow = $(document.createElement('div'))
            currentImgRow.attr('class',"row")
            currentImgRowCount = 0
        }
        currentImgRowCount += 1

        let cardCopies = currentDeckinfo[cardName]
        let cardImgFullPath = "static/defaultcard.png"
        if( "img_relative_path" in gameData.cards[cardName]){
            let cardImgRelativePath = gameData.cards[cardName].img_relative_path
            cardImgFullPath = dbmanager.getResourceRoot()+'\\'+cardImgRelativePath
        }
        let imgDiv = $(document.createElement('div'))
        imgDiv.attr('class','col-3')
        let imgElement = $(document.createElement('img'))
        imgElement.attr('src',cardImgFullPath)
        imgDiv.append(imgElement)
        imgDiv.append(cardName+"*"+cardCopies)
        currentImgRow.append(imgDiv)
    }
    // add the last row 
    deckImgView.append(currentImgRow)

    updateDeckDropdown()
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
