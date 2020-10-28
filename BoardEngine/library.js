const dbmanager = require('./dbmanager.js');

function refreshLibraryPage(){
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
    $('#create-new-game-btn').click(function(){onClickCreateNewGame()})
    updateGameMainPage(installedGames[0])
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

function createLibraryEntry(gameName){
    let entryBtn =$(document.createElement('button'))
    entryBtn.text(gameName)
    entryBtn.attr('class',"btn btn-light")
    entryBtn.click(function(){
        updateGameMainPage(gameName);})
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

function updateGameMainPage(gameName){
    let gameData = dbmanager.loadGameData(gameName)
    console.log(gameData)
    $('#game-title').text(gameName)
    $('#current-deck').text(gameData.rules.deck)
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
}

function popupWarning(message){
    $('#warning-modal').modal()
    $('#warning-modal-body').text(message)
}