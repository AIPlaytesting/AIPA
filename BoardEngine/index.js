const PythonProcess = require('./pythonProcess.js')
const rootPath = require('electron-root-path').rootPath

function onStart(){
    detectEnv()
    console.log(rootPath)
}

function detectEnv(){
    try{
        let pyProcess = new PythonProcess(10,
            function () { console.log('success!') },
            onReceiveEnvMesssage,
            function(){onEnvDetectResult("none","none")})
    }
    catch(e){
        console.log('py not installed!')
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
    env = JSON.parse(data).content
    onEnvDetectResult(env.py,env.tf)
}

function onEnvDetectResult(pyVersion,tfVersion){
    let tfRequiredVersion  = '2.3.1'
    let pyRequiredMainVersion = '3'
    let pass = true

    $('#py-env-version').text("Python: "+pyVersion)
    if(pyVersion[0]!= pyRequiredMainVersion){
        pass = false
        let installBtn = $(document.createElement('button'))
        .text("install")
        .click(onClickInstallPython)
        $('#py-env-version').attr('style','color:red').append(installBtn)
    }

    // if python is not required, no need to check/install tf
    if(pass){
        $('#tf-env-version').text("Tensorflow: "+ tfVersion)
        if(tfVersion != tfRequiredVersion){
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