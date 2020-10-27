// for historical reason, the naming styple in db is same to the Python one
// because the database is originnally wrote in Python

const fs = require('fs');

var dbRoot = '../STP2/DATA';
var installedGames = [];

function loadDB(onFinishLoad){
    let manifestPath = dbRoot +'\\manifest.json';
    fs.readFile(manifestPath, 'utf8', function(err, data){ 
        if (err) throw err;
        let manifest = JSON.parse(data);
        installedGames = manifest.installed_app;
        onFinishLoad()
    });     
}

// return: gameData
function loadGameData(gameName){
    let gameRoot = dbRoot +'\\'+gameName;
    let gameData = {};
    // load init.json
    initData = fs.readFileSync(gameRoot+'\\init.json','utf8');
    gameData.init = JSON.parse(initData);

    // load all decks
    gameData.decks = {}
    let deckFileRoot = gameRoot +'\\'+gameData.init.decks_directory;
    // all decks are stored in ../DeckFileRoot/(deckname).json 
    for(deckFile of fs.readdirSync(deckFileRoot,"utf8")){
        deckData = fs.readFileSync(deckFileRoot+'\\'+deckFile,'utf8');
        gameData.decks[deckFile] = JSON.parse(deckData)
    }

    // load all cards
    gameData.cards = {}
    let cardFileRoot = gameRoot +'\\'+gameData.init.cards_directory;
    // all cards are stored in ../cardFileRoot/(cardname).json 
    for(cardFile of fs.readdirSync(cardFileRoot,"utf8")){
        cardData = fs.readFileSync(cardFileRoot+'\\'+cardFile,'utf8');
        gameData.cards[cardFile] = JSON.parse(cardData)
    }

    // load gameData.buffInfo
    let buffFilePath = gameRoot +'\\' + gameData.init.buffs_file;
    gameData.buffInfo =JSON.parse(fs.readFileSync(buffFilePath))

    // load gameData.rules
    let ruleFilePath = gameRoot +'\\' + gameData.init.rules_file
    gameData.rules = JSON.parse(fs.readFileSync(ruleFilePath))
    return gameData
}

function getInstalledGameApps(){
    return installedGames;
}

module.exports = {
    getInstalledGameApps,loadDB,loadGameData
}
