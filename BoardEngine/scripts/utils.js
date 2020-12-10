function setupDropdown(dropdownMenuID,dropwdownBtnID,options,defaultValue="please select"){
    let dropdownMenu = $("#"+dropdownMenuID);
    dropdownMenu .text("");
    $('#'+dropwdownBtnID).text(defaultValue)
    for(option of options){
        let optionBtn =$(document.createElement('button'))
        .attr('class','dropdown-item')
        .text(option)
        .click(function(){
            $('#'+dropwdownBtnID).text($(this).text())
        })
        dropdownMenu .append(optionBtn)
    }
}

function setupSlider(sliderID,valueIndicatorID,minVal,maxVal){
    slider = $('#'+sliderID)
        .attr('min',minVal)
        .attr('max',maxVal)
        .change(function(){
            $('#'+valueIndicatorID).text($(this).val())
        })
    $('#'+valueIndicatorID).text(minVal)
}

function createProgressBar(curVal,maxVal,color = 'red'){
    let progressbar = $(document.createElement('div'))
    .attr('class', 'progress-bar')
    .attr('role', 'progressbar')
    .css('width',100*curVal/maxVal + '%')
    .css('background-color', color)
    
    let parent = $(document.createElement('div'))
    .css('height', '6px')
    .attr('class', 'progress md-progress')
    .append(progressbar)
    return parent
}

function createTooltipDiv(givenID,tooltipContents){
    let rootDiv = $(document.createElement('div'))
    let btn = $(document.createElement('button'))
    .attr('class','btn btn-warning')
    .text('explanation')
    .attr('data-toggle','collapse')
    .attr('data-target','#' + givenID)
    let contentDiv = $(document.createElement('div'))
    .attr('class','collapse tooltip-section')
    .attr('id',givenID)
    for(let c of tooltipContents){
        contentDiv.append($(document.createElement('p')).text(c))
    }
    return rootDiv.append(btn,contentDiv)
}
module.exports ={setupDropdown,setupSlider,createProgressBar,createTooltipDiv}