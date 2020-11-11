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
module.exports ={setupDropdown,setupSlider}