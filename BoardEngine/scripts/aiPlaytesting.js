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
}

function drawStatisticPage(){
    $('#data-page').text("")
    drawStatisticCatagories()
    drawWinrateSection()
}

function drawStatisticCatagories(){
    $('#data-tab-second').text("")
    let catagories = ["Basic","Cards","CardRelationship"]
    let clicks = [drawBasicData,drawCardsData,drawCardRelationshipData]
    for(i = 0; i < catagories.length; i++){
        let catagoryBtn = $(document.createElement('button')).attr('class','btn').text(catagories[i]).click(clicks[i])
        $('#data-tab-second').append(catagoryBtn)
    }
}

function drawBasicData(){
    $('#data-page').text("")
    dataVisualizer.drawRankChart('data-page')
}

function drawCardsData(){
    $('#data-page').text("")
    dataVisualizer.drawRankChart('data-page')
}


function drawCardRelationshipData(){
    $('#data-page').text("")
    dataVisualizer.drawRelationshipTable('data-page')
}



function drawWinrateSection(){
    let winrateDiv = $(document.createElement('div'))
    winrateDiv.text("winrate: 86.7%")
    $('#data-page').append(winrateDiv)
}

function drawAnomaliesPage(){
    $('#data-page').text("")
    drawAnomaliesCatagories()
}

function drawAnomaliesCatagories(){
    $('#data-tab-second').text("")
    let catagories = ["FastWin","MaxDamage","LongestGame"]
    let clicks = [drawFastwinCatagory,drawFastwinCatagory,drawFastwinCatagory]
    for(i = 0; i < catagories.length; i++){
        let catagoryBtn = $(document.createElement('button')).attr('class','btn').text(catagories[i]).click(clicks[i])
        $('#data-tab-second').append(catagoryBtn)
    }
}

function drawFastwinCatagory(){
    dbmanager.loadDB(function(){
        let currentGame = dbmanager.getCurrentGameName()
        let recordDataRoot = dbmanager.getGameRecordDataRoot(currentGame,false)
        console.log("fastwin: "+recordDataRoot)
        $('#data-page').text("")
        let recordGroupList = $(document.createElement('ul')).attr('class','list-group')
        $('#data-page').append(recordGroupList)
        for(i = 0; i < 10; i++){
            let recordItem = $(document.createElement('li')).text("record"+i).attr('class','list-group-item')
            let recordPlayBtn = $(document.createElement('button')).text("Play")
            let reocrdTimeline = $(document.createElement('span')).text("-timeline-----------------------------------------")
            recordItem.append(recordPlayBtn,reocrdTimeline)
            recordGroupList.append(recordItem)
        }
    })
}

function showPieChart(){   
    // clear 
    $("#my_dataviz").text("")
    // set the dimensions and margins of the graph
    var width = 450
    height = 450
    margin = 40

    // The radius of the pieplot is half the width or half the height (smallest one). I subtract a bit of margin.
    var radius = Math.min(width, height) / 2 - margin

    // append the svg object to the div called 'my_dataviz'
    var svg = d3.select("#my_dataviz")
    .append("svg")
    .attr("width", width)
    .attr("height", height)
    .append("g")
    .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

    // Create dummy data
    var data = {a: 9, b: 20, c:30, d:8, e:12}

    // set the color scale
    var color = d3.scaleOrdinal()
    .domain(data)
    .range(d3.schemeSet2);

    // Compute the position of each group on the pie:
    var pie = d3.pie()
    .value(function(d) {return d.value; })
    var data_ready = pie(d3.entries(data))
    // Now I know that group A goes from 0 degrees to x degrees and so on.

    // shape helper to build arcs:
    var arcGenerator = d3.arc()
    .innerRadius(0)
    .outerRadius(radius)

    // Build the pie chart: Basically, each part of the pie is a path that we build using the arc function.
    svg
    .selectAll('mySlices')
    .data(data_ready)
    .enter()
    .append('path')
    .attr('d', arcGenerator)
    .attr('fill', function(d){ return(color(d.data.key)) })
    .attr("stroke", "black")
    .style("stroke-width", "2px")
    .style("opacity", 0.7)

    // Now add the annotation. Use the centroid method to get the best coordinates
    svg
    .selectAll('mySlices')
    .data(data_ready)
    .enter()
    .append('text')
    .text(function(d){ return "grp " + d.data.key})
    .attr("transform", function(d) { return "translate(" + arcGenerator.centroid(d) + ")";  })
    .style("text-anchor", "middle")
    .style("font-size", 17)
}

function showZoomHis(){
    // clear 
    $("#my_dataviz").text("")
    // set the dimensions and margins of the graph
    var width = 460
    var height = 460

    // append the svg object to the body of the page
    var svg = d3.select("#my_dataviz")
    .append("svg")
        .attr("width", width)
        .attr("height", height)

    // Read data
    d3.csv("https://raw.githubusercontent.com/holtzy/data_to_viz/master/Example_dataset/11_SevCatOneNumNestedOneObsPerGroup.csv", function(data) {

    // Filter a bit the data -> more than 1 million inhabitants
    data = data.filter(function(d){ return d.value>10000000 })

    // Color palette for continents?
    var color = d3.scaleOrdinal()
        .domain(["Asia", "Europe", "Africa", "Oceania", "Americas"])
        .range(d3.schemeSet1);

    // Size scale for countries
    var size = d3.scaleLinear()
        .domain([0, 1400000000])
        .range([7,55])  // circle will be between 7 and 55 px wide

    // create a tooltip
    var Tooltip = d3.select("#my_dataviz")
        .append("div")
        .style("opacity", 0)
        .attr("class", "tooltip")
        .style("background-color", "white")
        .style("border", "solid")
        .style("border-width", "2px")
        .style("border-radius", "5px")
        .style("padding", "5px")

    // Three function that change the tooltip when user hover / move / leave a cell
    var mouseover = function(d) {
        Tooltip
        .style("opacity", 1)
    }
    var mousemove = function(d) {
        Tooltip
        .html('<u>' + d.key + '</u>' + "<br>" + d.value + " inhabitants")
        .style("left", (d3.mouse(this)[0]+20) + "px")
        .style("top", (d3.mouse(this)[1]) + "px")
    }
    var mouseleave = function(d) {
        Tooltip
        .style("opacity", 0)
    }

    // Initialize the circle: all located at the center of the svg area
    var node = svg.append("g")
        .selectAll("circle")
        .data(data)
        .enter()
        .append("circle")
        .attr("class", "node")
        .attr("r", function(d){ return size(d.value)})
        .attr("cx", width / 2)
        .attr("cy", height / 2)
        .style("fill", function(d){ return color(d.region)})
        .style("fill-opacity", 0.8)
        .attr("stroke", "black")
        .style("stroke-width", 1)
        .on("mouseover", mouseover) // What to do when hovered
        .on("mousemove", mousemove)
        .on("mouseleave", mouseleave)
        .call(d3.drag() // call specific function when circle is dragged
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended));

    // Features of the forces applied to the nodes:
    var simulation = d3.forceSimulation()
        .force("center", d3.forceCenter().x(width / 2).y(height / 2)) // Attraction to the center of the svg area
        .force("charge", d3.forceManyBody().strength(.1)) // Nodes are attracted one each other of value is > 0
        .force("collide", d3.forceCollide().strength(.2).radius(function(d){ return (size(d.value)+3) }).iterations(1)) // Force that avoids circle overlapping

    // Apply these forces to the nodes and update their positions.
    // Once the force algorithm is happy with positions ('alpha' value is low enough), simulations will stop.
    simulation
        .nodes(data)
        .on("tick", function(d){
            node
                .attr("cx", function(d){ return d.x; })
                .attr("cy", function(d){ return d.y; })
        });

    // What happens when a circle is dragged?
    function dragstarted(d) {
        if (!d3.event.active) simulation.alphaTarget(.03).restart();
        d.fx = d.x;
        d.fy = d.y;
    }
    function dragged(d) {
        d.fx = d3.event.x;
        d.fy = d3.event.y;
    }
    function dragended(d) {
        if (!d3.event.active) simulation.alphaTarget(.03);
        d.fx = null;
        d.fy = null;
    }

    })
}