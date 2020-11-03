const PythonProcess = require('./pythonProcess.js')
const rootPath = require('electron-root-path').rootPath

function onStart(){
    detectEnv()
    console.log(rootPath)
}

function detectEnv(){
    let pyProcess = new PythonProcess(10,
	    function () { console.log('success!') },
        onReceiveEnvMesssage)
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

function modifyTensorflow(isInstall){
    let child = require('child_process').execFile;
    let executablePath 
    if(isInstall){
        executablePath  = rootPath+'\\executables\\tfinstall.bat'
    }
    else{
        executablePath  = rootPath+'\\executables\\tfuninstall.bat'      
    }

	console.log('start bat at: '+executablePath)
	let ch = child(executablePath, function(err, data) {

        if(err){
           console.error(err);
           return;
        }
     
        console.log(data.toString())
        console.log("reload the window")
        location.href='index.html'
    })

    ch.stdin.write('y');
    ch.stdin.end();
}

function onReceiveEnvMesssage(data){
    let tfversion  = '2.3.1'
    let pyMainVersion = '2'
    let pass = true
    env = JSON.parse(data).content
    $('#py-env-version').text("Python: "+env.py)
    if(env.py[0]!= pyMainVersion){
        pass = false
        let installBtn = $(document.createElement('button'))
        .text("install")
        .click(onClickInstallPython)
        $('#py-env-version').attr('style','color:red').append(installBtn)
    }


    $('#tf-env-version').text("Tensorflow: "+env.tf)
    if(env.tf != tfversion){
        pass = false
        let installBtn = $(document.createElement('button'))
        .text("install")
        .click(function(){
            modifyTensorflow(true)
            $(this).remove()
            let spining = $(document.createElement('span'))
            .attr('class','spinner-border text-light')
            .attr('role','status')
            .attr('id','tf-install-spining')
            $('#tf-env-version').append(spining)
        })
        $('#tf-env-version').attr('style','color:red').append(installBtn)
    }
    else{
        let uninstallBtn = $(document.createElement('button'))
        .text("uninstall")
        .click(function(){
            modifyTensorflow(false)
            $(this).remove()
            let spining = $(document.createElement('span'))
            .attr('class','spinner-border text-light')
            .attr('role','status')
            .attr('id','tf-install-spining')
            $('#tf-env-version').append(spining)
        })
        $('#tf-env-version').append(uninstallBtn)
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