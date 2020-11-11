
function createCardElement(imgPath,cardName,description,energy){
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
        .css('left','15px')
    

    let nameText = $(document.createElement('span'))
        .text(cardName)
        .attr('class','text-center')
        .css('width',textFrameWidth)
        .css('position','absolute')
        .css('top','20px')
        .css('left','40px')
        .css('color','white')

    let energyText = $(document.createElement('span'))
        .text(energy)
        .css('position','absolute')
        .css('top','0px')
        .css('left','25px')
        .css('color','white')
        .css('font-size','26px')
    
    let descriptionText = $(document.createElement('p'))
        .text(description)
        .attr('class','text-center')
        .css('position','absolute')
        .css('top','130px')
        .css('left','40px')
        .css('width',textFrameWidth)
        .css('color','white')

    imgDiv.append(imgElement,cardFrame,nameText,energyText,descriptionText) 
    return imgDiv
}

module.exports = {createCardElement}