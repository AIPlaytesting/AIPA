const dbmanager = require('./dbmanager.js');

function libraryOnLoad(){
    let gameEntryList = $("#game-entry-list")
    let installedGames = dbmanager.getInstalledGameApps()
    for(game of installedGames){
        gameEntryList.append(createLibraryEntry(game))
    }
    gameEntryList.append(createNewGameBtn())
}

function createLibraryEntry(gameName){
    let entryBtn =$(document.createElement('button'))
    entryBtn.text(gameName)
    entryBtn.attr('class',"btn btn-light")
    return entryBtn
}

function createNewGameBtn(){
    let entryBtn =$(document.createElement('button'))
    entryBtn.text("+New Game")
    entryBtn.attr('class',"btn btn-dark")
    return entryBtn
}
