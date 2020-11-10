// for historical reason, the naming styple in db is same to the Python one
// because the database is originnally wrote in Python

const fs = require('fs')
const ncp = require('ncp').ncp
const rimraf = require("rimraf")
const rootPath = require('electron-root-path').rootPath
const config = require('../scripts/config')

const dbRoot = calculateDBRoot()

var manifest = {}
var installedGames = [];
var resourceRoot = "";

function calculateDBRoot(){	
    if(config.isDevMode){
		console.log("set db root in development mode...")
		return config.devDependencies.pythonProject+'\\DATA'
	}
	else{
		console.log("set db root in build mode...")
		return  rootPath+'\\executables\\pyproj\\DATA'
	}
}

function loadDB(onFinishLoad){
    let manifestPath = dbRoot +'/manifest.json';
    fs.readFile(manifestPath, 'utf8', function(err, data){ 
        if (err) throw err;
        manifest = JSON.parse(data);
        installedGames = manifest.installed_app;
        resourceRoot = dbRoot + '\\' + manifest.resource_directory
        onFinishLoad()
    });     
}


function getResourceRoot(){
    return resourceRoot
}

function createNewGame(templateGame,newGameName,onFinishCallback){
    if(!installedGames.includes(templateGame)){
        throw "no template named: " + templateGame
    }

    if(installedGames.includes(newGameName)){
        throw "game named: "+newGameName+" already exists!"
    }

    let templateGameDir = dbRoot + '/' + templateGame
    let newGameDir = dbRoot + '/' + newGameName
    console.log("template: "+templateGameDir+" new: "+newGameDir)
    ncp(templateGameDir, newGameDir, function (err) {
        if (err) {
          throw err
        }
        manifest.installed_app.push(newGameName)
        saveManifest()
        onFinishCallback()
        console.log('done!');
    });
}

function createNewDeckOnCurrentGame(templateDeck,newDeckName){
    let gameName = getCurrentGameName()
    let gameData = loadGameData(gameName)

    if(!templateDeck in gameData.decks){
        throw "no template named: " + templateDeck
    }

    if(newDeckName in gameData.decks){
        throw "game named: "+newDeckName+" already exists!"
    }

    let newDeck = JSON.parse(JSON.stringify(gameData.decks[templateDeck]))  
    let newDeckPath= dbRoot + '\\' + gameName+'\\Decks\\'+ newDeckName +'.json'
    saveObjectToFileAsJSON(newDeck,newDeckPath)
}

function removeGame(gameName,onFinishCallback){
    if(!installedGames.includes(gameName)){
        throw "no such registered game: " + gameName
    }
    if(installedGames.length <= 1){
        throw "error: cannot delete game when there is only on game!"
    }

    let gameDir = dbRoot + '/' + gameName
    console.log("going to remove dir at: "+gameDir)
    rimraf.sync(gameDir)

    manifest.installed_app.splice(manifest.installed_app.indexOf(gameName),1)
    manifest.game_app = manifest.installed_app[0]
    saveManifest()

    onFinishCallback()
}

function saveManifest(){
    fs.writeFileSync(dbRoot +'/manifest.json', JSON.stringify(manifest, null, 4))
}

// return: gameData
function loadGameData(gameName){
    let gameRoot = getGameAppRoot(gameName);
    let gameData = {};
    // load init.json
    gameData.init = loadObjectFromJSONFile(gameRoot+'\\init.json') 

    // load gameData.decks
    gameData.decks = {}
    let deckFileRoot = gameRoot +'\\'+gameData.init.decks_directory;
    // all decks are stored in ../DeckFileRoot/(deckname).json 
    for(deckFile of fs.readdirSync(deckFileRoot,"utf8")){
        gameData.decks[deckFile.split('.')[0]] = loadObjectFromJSONFile(deckFileRoot+'\\'+deckFile) 
    }

    // load gameData.cards
    gameData.cards = {}
    let cardFileRoot = gameRoot +'\\'+gameData.init.cards_directory;
    // all cards are stored in ../cardFileRoot/(cardname).json 
    for(cardFile of fs.readdirSync(cardFileRoot,"utf8")){
        gameData.cards[cardFile.split('.')[0]] = loadObjectFromJSONFile(cardFileRoot+'\\'+cardFile) 
    }

    // load gameData.buffInfo
    gameData.buffInfo = loadObjectFromJSONFile(gameRoot +'\\' + gameData.init.buffs_file) 

    // load gameData.rules
    gameData.rules = loadObjectFromJSONFile(gameRoot +'\\' + gameData.init.rules_file) 
    return gameData
}

// current veilable attr: 
// currentDeck
// ..
function updateGameData(gameName,attr,value,onFinishCallback){
    if(attr == "currentDeck"){
        let gameDataRoot = getGameAppRoot(gameName)
        let ruleObjPath = gameDataRoot+'/rules.json'
        let rulesObj = loadObjectFromJSONFile(ruleObjPath)
        rulesObj.deck = value
        saveObjectToFileAsJSON(rulesObj,ruleObjPath)
    }
    else{
        throw "undefined attribute name  to update: "+attr
    }

    onFinishCallback()
}

function getCurrentGameName(){
    return manifest.game_app
}

function setCurrentGame(gameName){
    if(!installedGames.includes(gameName)){
        throw "no game named: " + templateGame
    }
    manifest.game_app = gameName
    saveManifest()
}

function getInstalledGameApps(){
    return installedGames;
}

function loadObjectFromJSONFile(jsonFilePath){
    let initData = fs.readFileSync(jsonFilePath);
    return JSON.parse(initData);
}

function saveObjectToFileAsJSON(sourceObj,path){
    fs.writeFileSync(path, JSON.stringify(sourceObj, null, 4))
}

function getGameAppRoot(gameName){
    return dbRoot + '/'+gameName
}

function getGameRecordDataRoot(gameName,isPlayerRecord){
    let gameAppRoot = getGameAppRoot(gameName)
    if(isPlayerRecord){
        return gameAppRoot+'\\Record\\Player'
    }
    else{
        return gameAppRoot+'\\Record\\AI'
    }
}

function modifyDeck(deckname,cardname,newCardCopyNumber){
    let gameData = loadGameData(getCurrentGameName())
    let targetDeck = gameData.decks[deckname]
    targetDeck[cardname] = newCardCopyNumber
    
    let deckPath= dbRoot + '\\' + getCurrentGameName()+'\\Decks\\'+ deckname +'.json'
    saveObjectToFileAsJSON(targetDeck,deckPath)
}

module.exports = {
    loadDB,
    getInstalledGameApps,
    loadGameData,
    updateGameData,
    getCurrentGameName,
    setCurrentGame,
    createNewGame,
    createNewDeckOnCurrentGame,
    modifyDeck,
    removeGame,
    getGameAppRoot,
    getResourceRoot,
    getGameRecordDataRoot
}