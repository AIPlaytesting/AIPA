const dbmanager = require('./dbmanager.js');

function libraryOnLoad(){
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
    entryBtn.click(function(){updateGameMainPage(gameName)})
    return entryBtn
}

function createNewGameBtn(){
    let entryBtn =$(document.createElement('button'))
    entryBtn.text("+New Game")
    entryBtn.attr('class',"btn btn-dark")
    return entryBtn
}

function updateGameMainPage(gameName){
    $('#game-title').text(gameName)
}