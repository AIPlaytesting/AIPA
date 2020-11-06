const PythonProcess = require('../scripts/pythonProcess')
const dbmanager = require('../scripts/dbmanager')
const dataVisualizer = require('../scripts/dataVisualizer')

function onClickPlaytest(){
    let pyProcess = new PythonProcess(12,
	    function () { console.log('success!') },
        onReceiveTrainMesssage)
    $('#data-status').text('Is playtesting...')
}

function onReceiveTrainMesssage(data){
    simulateInfo = JSON.parse(data).content
    let curprogress =   simulateInfo.curprogress
    let maxprogress =  simulateInfo.maxprogress
    $('#simulate-progress').attr("style","width:"+(curprogress*100/maxprogress)+"%")
    $('#simulate-progress').text(curprogress+'/'+maxprogress)
    if(simulateInfo.curprogress >= simulateInfo.maxprogress){
        onFinishPlaytest()
    }
}

function onFinishPlaytest(){
    $('#data-status').attr('class','d-none')
    $('#data-display-root').removeClass('d-none')
    drawStatisticPage()
}

function drawStatisticPage(){
    $('#data-page').text("")
    drawBasicDataSection()
    drawCardsDataSection()
    drawCardRelationshipDataSection()
}

function createSection(sectionName,sectionID){
    let sectionDiv = $(document.createElement('div'))
    .attr('class','container')
    let collapseBtn = $(document.createElement('button'))
    .attr('class','btn col-12')
    .attr('data-toggle','collapse')
    .attr('data-target','#'+sectionID)
    .attr('style','background-color: #58635b;')
    .text(sectionName)

    let collapseDiv = $(document.createElement('div'))
    .attr('id',sectionID)
    .attr('class','collapse show')
    sectionDiv.append(collapseBtn,collapseDiv)

    return sectionDiv  
}

function drawBasicDataSection(){
    let setionDiv = createSection('basic','basic-data-section')
    $('#data-page').append(setionDiv)

    let winrateCard = $(document.createElement('div'))
    .attr('class','card bg-secondary text-white display-3')
    .text("winrate: 86.7%")

    let playerHPCard = $(document.createElement('div'))
    .attr('class','card bg-danger text-white display-4')
    .text("average Boss HP: 23.1")

    let bossHPCard = $(document.createElement('div'))
    .attr('class','card bg-danger text-white display-4')
    .text("average Player HP: 23.1")

    let turnCountCard = $(document.createElement('div'))
    .attr('class','card bg-info text-white display-4')
    .text("average Turn Count: 3.56")

    $('#basic-data-section').append(winrateCard,playerHPCard,bossHPCard,turnCountCard)
}

function drawCardsDataSection(){
    let setionDiv = createSection('cards','cards-data-section')
    $('#data-page').append(setionDiv)
    dataVisualizer.drawRankChart('cards-data-section')
}

function drawCardRelationshipDataSection(){
    let setionDiv = createSection('cards relationship','cards-relatioship-data-section')
    $('#data-page').append(setionDiv)
    let tableDiv = $(document.createElement('div')).attr('id','card-relationship-table')
    let pieDiv = $(document.createElement('div')).attr('id','card-relationship-pie')
    $('#cards-relatioship-data-section').append(tableDiv,pieDiv)
    dataVisualizer.drawRelationshipTable('card-relationship-table')
    let data = {a: 9, b: 20, c:30, d:8, e:12}
    dataVisualizer.drawPieChart('card-relationship-pie',data)
    
}

function drawAnomaliesPage(){
    $('#data-page').text("")
    drawAnomaliesSection('FastWin')
    drawAnomaliesSection('MaxDamage')
    drawAnomaliesSection('LongestGame')
}


function drawAnomaliesSection(anomaliesType){
    let sectionID = anomaliesType +'-section'
    let setionDiv = createSection(anomaliesType,sectionID)
    $('#data-page').append(setionDiv)
    dbmanager.loadDB(function(){
        let currentGame = dbmanager.getCurrentGameName()
        let recordDataRoot = dbmanager.getGameRecordDataRoot(currentGame,false)
        console.log("fastwin: "+recordDataRoot)
        $('#'+sectionID).text("")
        let recordGroupList = $(document.createElement('ul')).attr('class','list-group')
        $('#'+sectionID).append(recordGroupList)
        for(i = 0; i < 10; i++){
            let recordItem = $(document.createElement('li')).text("record"+i).attr('class','list-group-item')
            let recordPlayBtn = $(document.createElement('button')).text("Play").click(onClickReplay)
            let reocrdTimeline = $(document.createElement('span')).text("-timeline-----------------------------------------")
            recordItem.append(recordPlayBtn,reocrdTimeline)
            recordGroupList.append(recordItem)
        }
    })
}

function onClickReplay(){ 
    let rootPath = require('electron-root-path').rootPath
    let child = require('child_process').execFile;
    let executablePath = rootPath + '/executables/recorderbuild/AIPA.exe';
    console.log('launch recorder at: '+executablePath)
    child(executablePath, function(err, data) {
        if(err){
           console.error(err);
           return;
        }
     
        console.log(data.toString());
    })
}