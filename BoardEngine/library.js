const dbmanager = require('./dbmanager.js');

function libraryOnLoad(){
    dbmanager.loadDB(onFinishDBLoad)
}

function onFinishDBLoad(){
    let gameEntryList = $("#game-entry-list")
    let installedGames = dbmanager.getInstalledGameApps()
    for(gameName of installedGames){
        gameEntryList.append(createLibraryEntry(gameName))
    }

    gameEntryList.append(createNewGameBtn())

    updateGameMainPage(installedGames[0])
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
    let entryBtn =$(document.createElement('button'));
    entryBtn.text("+New Game");
    entryBtn.attr('class',"btn btn-dark");
    entryBtn.attr('data-toggle','modal');
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