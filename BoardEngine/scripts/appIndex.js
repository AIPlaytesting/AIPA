
const rootPath = require('electron-root-path').rootPath

function openNewWindow(herf){
    win = window.open(herf)
}

function onClickPlay(){
    let child = require('child_process').execFile;
    let executablePath = rootPath + '/executables/unitybuild/AIPA.exe';
    console.log('launch unity at: '+executablePath)
    child(executablePath, function(err, data) {
        if(err){
           console.error(err);
           return;
        }
     
        console.log(data.toString());
    });  
}