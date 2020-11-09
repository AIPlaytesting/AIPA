const fs = require('fs');
const rootPath = require('electron-root-path').rootPath

const isDevMode = loadConfig().isDevMode
const devDependencies = loadConfig().devDependencies
const buildDependencies = loadConfig().buildDependencies

function loadConfig(){
    let configPath = rootPath + '\\config.json'
    let config = loadObjectFromJSONFile(configPath)
    return config
}

function loadObjectFromJSONFile(jsonFilePath){
    let initData = fs.readFileSync(jsonFilePath);
    return JSON.parse(initData);
}


module.exports = {devDependencies,buildDependencies,isDevMode}