const fs = require('fs');

var dbRoot = '../STP2/DATA';
var installedGames = [];

function loadDB(onFinishLoad){
    let manifestPath = dbRoot +'\\manifest.json';
    fs.readFile(manifestPath, 'utf8', function(err, data){ 
        if (err) throw err;
        let manifest = JSON.parse(data);
        installedGames = manifest.installed_app;
        console.log(manifest.installed_app)
        console.log(installedGames)
        onFinishLoad()
    });     
}

// return: gameData
function loadGameData(gameName){
    let gameRoot = dbRoot +'\\'+gameName;
    let gameData = {}
    initData = fs.readFileSync(gameRoot+'\\init.json','utf8')
    gameData.init = JSON.parse(initData)
    return gameData
}

function getInstalledGameApps(){
    console.log("get called")
    console.log(installedGames)
    return installedGames;
}

module.exports = {
    getInstalledGameApps,loadDB,loadGameData
}
