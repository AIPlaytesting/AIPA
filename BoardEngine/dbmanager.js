// for historical reason, the naming styple in db is same to the Python one
// because the database is originnally wrote in Python

const fs = require('fs');
const ncp = require('ncp').ncp;
const rimraf = require("rimraf");

var dbRoot = '../STP2/DATA';
var manifest = {}
var installedGames = [];
var resourceRoot = "";

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

function removeGame(gameName,onFinishCallback){
    if(!installedGames.includes(gameName)){
        throw "no such registered game: " + gameName
    }

    let gameDir = dbRoot + '/' + gameName
    console.log("going to remove dir at: "+gameDir)
    rimraf.sync(gameDir)

    manifest.installed_app.splice(manifest.installed_app.indexOf(gameName),1)
    saveManifest()

    onFinishCallback()
}

function saveManifest(){
    fs.writeFileSync(dbRoot +'/manifest.json', JSON.stringify(manifest, null, 4))
}

// return: gameData
// TODO: refactor, use API to load JSON file
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

module.exports = {
    getInstalledGameApps,
    getResourceRoot,
    loadDB,
    loadGameData,
    updateGameData,
    getCurrentGameName,
    setCurrentGame,
    createNewGame,
    removeGame
}