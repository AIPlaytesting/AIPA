const PythonProcess = require('../scripts/pythonProcess.js')
const rootPath = require('electron-root-path').rootPath

function onStart(){
    detectEnv()
    console.log(rootPath)
}

function detectEnv(){
    try{
        let pyProcess = new PythonProcess(
            10,
            {},
            function () { console.log('success!') },
            onReceiveEnvMesssage,
            function(err){onEnvDetectResult("none","none")})
    }
    catch(e){
        console.log('fail to launch py when detect env')
    }
}

function onClickInstallPython(){
    let child = require('child_process').execFile
    let installerPath = rootPath+'\\executables\\pyinstaller.exe'
    child(installerPath, function(err, data) {
        if(err){
           console.error(err);
           return;
        } 
        console.log(data.toString());
    })  
}

function onReceiveEnvMesssage(data){
    env = JSON.parse(data).content
    onEnvDetectResult(env.py,env.tf)
}

function onEnvDetectResult(pyVersion,tfVersion){
    let tfRequiredVersion  = '2.3.1'
    let pyRequiredVersion = '3.8.6'
    let pass = true

    $('#py-env-version').text("Python: "+pyVersion)
    if(pyVersion!= pyRequiredVersion){
        pass = false
        $('#py-env-version').attr('style','color:red')
    }

    // if python is not required, no need to check/install tf
    if(pass){
        $('#tf-env-version').text("Tensorflow: "+ tfVersion)
        if(tfVersion != tfRequiredVersion){
            pass = false
            $('#tf-env-version').attr('style','color:red')
        }
    }

   

    if(pass){
        $('#env-loading').text("Environment Pass")
        $('#env-loading').attr('style','color:green')
    }
    else{
        $('#env-loading').text("Environment Fail")
        $('#env-loading').attr('style','color:red')
    }
}