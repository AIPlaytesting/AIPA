const dbmanager = require('../scripts/dbmanager')

function createCardElement(imgPath,cardName,description,energy,hoverImgPath = "", onClickListener = undefined){
    let frameWidth = '166px'
    let textFrameWidth = '130px'
    let framwHeight = '220px'

    let cardFramePath = "../static/cardframe.png"
    let imgDiv = $(document.createElement('div'))
        .attr('class','card-div')
        .css('position','relative')
    imgDiv.attr('class','col-2')

    let imgElement = $(document.createElement('img'))
        .attr('src',imgPath)  
        .css('width',frameWidth)
        .css('height',framwHeight)

    let cardFrame =  $(document.createElement('img'))
        .attr('src',cardFramePath)
        .css('position','absolute')
        .css('width',frameWidth)
        .css('height',framwHeight)
        .css('top','0px')
        .css('left','10px')
    

    let nameText = $(document.createElement('span'))
        .text(cardName)
        .attr('class','text-center')
        .css('width',textFrameWidth)
        .css('position','absolute')
        .css('top','20px')
        .css('left','40px')
        .css('color','white')
        .css('font-weight','bold')

    let energyText = $(document.createElement('span'))
        .text(energy)
        .css('position','absolute')
        .css('top','0px')
        .css('left','25px')
        .css('color','red')
        .css('font-size','26px')
        .css('font-weight','bold')
    
    let descriptionText = $(document.createElement('p'))
        .text(description)
        .attr('class','text-center')
        .css('position','absolute')
        .css('top','130px')
        .css('left','40px')
        .css('width',textFrameWidth)
        .css('color','white')

    let hoverSign = ""
    if(hoverImgPath!=""){
        hoverSign = $(document.createElement('img'))
        .attr('src',hoverImgPath)
        .css('position','absolute')
        .css('width','70%')
        .css('height','70%')
        .css('top','15%')
        .css('left','15%')
        .css('opacity',0)
        .hover(function(){
            $(this).css('opacity', 0.9).css('background-color','rgba(1,0,0,0)');
            }, function(){
            $(this).css('opacity', 0).css('background-color','rgba(0,0,0,0)');
        })
        .click(function(){
            if(onClickListener!==undefined){
                onClickListener()
            }
        })
    }   

    imgDiv.append(imgElement,cardFrame,nameText,energyText,descriptionText,hoverSign) 
    return imgDiv
}

function createCardElementByName(gameName,cardName){
    let gamedata = dbmanager.loadGameData(gameName)
    let card = gamedata.cards[cardName]
    let cardImgFullPath = "../static/defaultcard.png"
    if( "img_relative_path" in card){
        cardImgFullPath = dbmanager.getResourceRoot()+'\\'+card.img_relative_path
    }

    let cardElement = createCardElement(
        cardImgFullPath,
        cardName,                    
        card.description,
        card.energy_cost)

    return cardElement
}

module.exports = {createCardElement,createCardElementByName}