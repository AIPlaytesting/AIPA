
function createCardElement(imgPath,cardName,description,energy){
    let imgDiv = $(document.createElement('div'))
    imgDiv.attr('class','col-2')
    let imgElement = $(document.createElement('img'))
    imgElement.attr('src',imgPath)
    imgDiv.append(imgElement)   
    //imgDiv.append(cardName)
    return imgDiv
}

module.exports = {createCardElement}