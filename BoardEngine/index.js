const PythonProcess = require('./pythonProcess.js')

function onStart(){
    detectEnv()
}

function detectEnv(){
    let pyProcess = new PythonProcess(10,
	    function () { console.log('success!') },
        onReceiveEnvMesssage)
}

function onReceiveEnvMesssage(data){
    let tfversion  = '2.3.1'
    let pyMainVersion = '3'
    let pass = true
    env = JSON.parse(data).content
    $('#py-env-version').text("Python: "+env.py)
    if(env.py[0]!= pyMainVersion){
        pass = false
        $('#py-env-version').attr('style','color:red')
    }
    $('#tf-env-version').text("Tensorflow: "+env.tf)
    if(env.tf != tfversion){
        pass = false
        $('#tf-env-version').attr('style','color:red')
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