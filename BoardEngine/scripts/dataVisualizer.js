function drawRankChart(csvURL,divID,hookedRadarDivID=''){
    let optionDiv = $(document.createElement('div'))
    let chartDiv = $(document.createElement('div')).attr('id',divID+'-chart')
    $('#'+divID).append(optionDiv,chartDiv)

    // set the dimensions and margins of the graph
    var margin = {top: 30, right: 30, bottom: 70, left: 60},
        width = 460 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;


    // append the svg object to the body of the page
    var svg = d3.select("#"+divID+'-chart')
    .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform","translate(" + margin.left + "," + margin.top + ")");

    // Initialize the X axis
    var x = d3.scaleBand()
    .range([ 0, width ])
    .padding(0.2);
    var xAxis = svg.append("g")
    .attr("transform", "translate(0," + height + ")")

    // Initialize the Y axis
    var y = d3.scaleLinear()
    .range([ height, 0]);
    var yAxis = svg.append("g")
    .attr("class", "myYaxis")

    let radarData = []
    let radarColors= ["#69257F", "#CA0D59", "#CA0D19", "#CA1D52"]
    // A function that create / update the plot for a given variable:
    function update(selectedVar,color) {
        // clear radar chart
        if(hookedRadarDivID != ''){
            $('#'+hookedRadarDivID).text("")
        }
        radarData = []
        // Parse the Data
        d3.csv(csvURL, function(data) {

            // X axis
            x.domain(data.map(function(d) { return d.group; }))
            xAxis.transition().duration(1000).call(d3.axisBottom(x))

            // Add Y axis
            y.domain([0, d3.max(data, function(d) { return +d[selectedVar] }) ]);
            yAxis.transition().duration(1000).call(d3.axisLeft(y));

            // variable u: map data to existing bars
            var u = svg.selectAll("rect")
            .data(data)

            function mouseover(){
                d3.select(this)
                .style("stroke", "black")
                .style("opacity", 1)
            }
        
            function mouseleave(){
                d3.select(this)
                .style("stroke", "none")
                .style("opacity", 0.8)
            }
            
            function mouseclick(){
                if(hookedRadarDivID != ""){
                    $('#'+hookedRadarDivID).text("")
                    radarData.push(
                        [
                          {"area": "rawards", "value": 100*Math.random()},
                          {"area": "playPosition", "value": 100*Math.random()},
                          {"area": "playCount", "value": 100*Math.random()}
                          ])
                    drawRadarChart(hookedRadarDivID,radarData,radarColors)   
                }
            }
            // update bars
            u
            .enter()
            .append("rect")
            .merge(u)
            .transition()
            .duration(1000)
                .attr("x", function(d) { return x(d.group); })
                .attr("y", function(d) { return y(d[selectedVar]); })
                .attr("width", x.bandwidth())
                .attr("height", function(d) { return height - y(d[selectedVar]); })
                .attr("fill", color)
            
            svg.selectAll("rect")
            .on('mouseover',mouseover)
            .on('mouseleave',mouseleave)
            .on('click',mouseclick)
        })
    }

    // fill option Buttons
    var optionList = ['rewards','playPosition','playCount']
    let colorDict={
        'rewards':"#69b3a2",
        'playPosition':"#eba434",
        'playCount':'#e82cb6'
    }
    for( i = 0 ; i < optionList.length; i++){
        let optionBtn = $(document.createElement('button'))
        .text(optionList[i])
        .attr('class', 'btn')
        .css('color',colorDict[optionList[i]])
        .click(function(){
            let option = $(this).text()
            let color = colorDict[option]
            update($(this).text(),color)})
        optionDiv.append(optionBtn)
    }
    // Initialize plot
    update('rewards',"#69b3a2")
}

function drawRelationshipTable(divID){
    // set the dimensions and margins of the graph
    var margin = {top: 80, right: 25, bottom: 30, left: 40},
    width = 450 - margin.left - margin.right,
    height = 450 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    var svg = d3.select("#"+divID)
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform",
        "translate(" + margin.left + "," + margin.top + ")");

    //Read the data
    d3.csv("../static/cardrelationship.csv", function(data) {

    // Labels of row and columns -> unique identifier of the column called 'group' and 'variable'
    var myGroups = d3.map(data, function(d){return d.group;}).keys()
    var myVars = d3.map(data, function(d){return d.variable;}).keys()

    // Build X scales and axis:
    var x = d3.scaleBand()
    .range([ 0, width ])
    .domain(myGroups)
    .padding(0.05);
    svg.append("g")
    .style("font-size", 15)
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(x).tickSize(0))
    .select(".domain").remove()

    // Build Y scales and axis:
    var y = d3.scaleBand()
    .range([ height, 0 ])
    .domain(myVars)
    .padding(0.05);
    svg.append("g")
    .style("font-size", 15)
    .call(d3.axisLeft(y).tickSize(0))
    .select(".domain").remove()

    // Build color scale
    var myColor = d3.scaleSequential()
    .interpolator(d3.interpolateInferno)
    .domain([1,100])

    // create a tooltip
    var tooltip = d3.select("#"+divID)
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
    let data = {a: Math.random(), b: Math.random(), c:Math.random(), d:Math.random(), e:Math.random()}
    drawPieChart('card-relationship-pie',data)

    tooltip
        .style("opacity", 1)
    d3.select(this)
        .style("stroke", "black")
        .style("opacity", 1)
    }
    var mousemove = function(d) {
    tooltip
        .html("The exact value of<br>this cell is: " + d.value)
        .style("left", (d3.mouse(this)[0]+70) + "px")
        .style("top", (d3.mouse(this)[1]) + "px")
    }
    var mouseleave = function(d) {
    tooltip
        .style("opacity", 0)
    d3.select(this)
        .style("stroke", "none")
        .style("opacity", 0.8)
    }

    // add the squares
    svg.selectAll()
    .data(data, function(d) {return d.group+':'+d.variable;})
    .enter()
    .append("rect")
        .attr("x", function(d) { return x(d.group) })
        .attr("y", function(d) { return y(d.variable) })
        .attr("rx", 4)
        .attr("ry", 4)
        .attr("width", x.bandwidth() )
        .attr("height", y.bandwidth() )
        .style("fill", function(d) { return myColor(d.value)} )
        .style("stroke-width", 4)
        .style("stroke", "none")
        .style("opacity", 0.8)
    .on("mouseover", mouseover)
    .on("mousemove", mousemove)
    .on("mouseleave", mouseleave)
    })

    // Add title to graph
    svg.append("text")
        .attr("x", 0)
        .attr("y", -50)
        .attr("text-anchor", "left")
        .style("font-size", "22px")
        .text("Cards Relationship");

    // Add subtitle to graph
    svg.append("text")
        .attr("x", 0)
        .attr("y", -20)
        .attr("text-anchor", "left")
        .style("font-size", "14px")
        .style("fill", "grey")
        .style("max-width", 400)
        .text("A short description of cards relationship");
}

function drawPieChart(divID,data){   
    // clear 
    $("#"+divID).text("")
    // set the dimensions and margins of the graph
    var width = 450
    height = 450
    margin = 40

    // The radius of the pieplot is half the width or half the height (smallest one). I subtract a bit of margin.
    var radius = Math.min(width, height) / 2 - margin

    // append the svg object to the div called 'my_dataviz'
    var svg = d3.select("#"+divID)
    .append("svg")
    .attr("width", width)
    .attr("height", height)
    .append("g")
    .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

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

function drawRadarChart(divID,data,colors){
    var RadarChart = {
        draw: function(id, d, options,colors){
          var cfg = {
           radius: 5,
           w: 600,
           h: 600,
           factor: 1,
           factorLegend: .85,
           levels: 3,
           maxValue: 0,
           radians: 2 * Math.PI,
           opacityArea: 0.5,
           ToRight: 5,
           TranslateX: 80,
           TranslateY: 30,
           ExtraWidthX: 100,
           ExtraWidthY: 100,
           color: d3.scaleOrdinal().range(colors)
          };
          
          if('undefined' !== typeof options){
            for(var i in options){
            if('undefined' !== typeof options[i]){
              cfg[i] = options[i];
            }
            }
          }
          
          cfg.maxValue = 100;
          
          var allAxis = (d[0].map(function(i, j){return i.area}));
          var total = allAxis.length;
          var radius = cfg.factor*Math.min(cfg.w/2, cfg.h/2);
          var Format = d3.format('%');
          d3.select(id).select("svg").remove();
      
          var g = d3.select(id)
              .append("svg")
              .attr("width", cfg.w+cfg.ExtraWidthX)
              .attr("height", cfg.h+cfg.ExtraWidthY)
              .append("g")
              .attr("transform", "translate(" + cfg.TranslateX + "," + cfg.TranslateY + ")");
      
              var tooltip;
          
          //Circular segments
          for(var j=0; j<cfg.levels; j++){
            var levelFactor = cfg.factor*radius*((j+1)/cfg.levels);
            g.selectAll(".levels")
             .data(allAxis)
             .enter()
             .append("svg:line")
             .attr("x1", function(d, i){return levelFactor*(1-cfg.factor*Math.sin(i*cfg.radians/total));})
             .attr("y1", function(d, i){return levelFactor*(1-cfg.factor*Math.cos(i*cfg.radians/total));})
             .attr("x2", function(d, i){return levelFactor*(1-cfg.factor*Math.sin((i+1)*cfg.radians/total));})
             .attr("y2", function(d, i){return levelFactor*(1-cfg.factor*Math.cos((i+1)*cfg.radians/total));})
             .attr("class", "line")
             .style("stroke", "grey")
             .style("stroke-opacity", "0.75")
             .style("stroke-width", "0.3px")
             .attr("transform", "translate(" + (cfg.w/2-levelFactor) + ", " + (cfg.h/2-levelFactor) + ")");
          }
      
          //Text indicating at what % each level is
          for(var j=0; j<cfg.levels; j++){
            var levelFactor = cfg.factor*radius*((j+1)/cfg.levels);
            g.selectAll(".levels")
             .data([1]) //dummy data
             .enter()
             .append("svg:text")
             .attr("x", function(d){return levelFactor*(1-cfg.factor*Math.sin(0));})
             .attr("y", function(d){return levelFactor*(1-cfg.factor*Math.cos(0));})
             .attr("class", "legend")
             .style("font-family", "sans-serif")
             .style("font-size", "10px")
             .attr("transform", "translate(" + (cfg.w/2-levelFactor + cfg.ToRight) + ", " + (cfg.h/2-levelFactor) + ")")
             .attr("fill", "#737373")
             //.text((j+1)*100/cfg.levels);
          }
      
          series = 0;
      
          var axis = g.selectAll(".axis")
              .data(allAxis)
              .enter()
              .append("g")
              .attr("class", "axis");
      
          axis.append("line")
            .attr("x1", cfg.w/2)
            .attr("y1", cfg.h/2)
            .attr("x2", function(d, i){return cfg.w/2*(1-cfg.factor*Math.sin(i*cfg.radians/total));})
            .attr("y2", function(d, i){return cfg.h/2*(1-cfg.factor*Math.cos(i*cfg.radians/total));})
            .attr("class", "line")
            .style("stroke", "grey")
            .style("stroke-width", "1px");
      
          axis.append("text")
            .attr("class", "legend")
            .text(function(d){return d})
            .style("font-family", "sans-serif")
            .style("font-size", "20px")
            .attr("text-anchor", "middle")
            .attr("dy", "1.5em")
            .attr("transform", function(d, i){return "translate(0, -10)"})
            .attr("x", function(d, i){return cfg.w/2*(1-cfg.factorLegend*Math.sin(i*cfg.radians/total))-60*Math.sin(i*cfg.radians/total);})
            .attr("y", function(d, i){return cfg.h/2*(1-Math.cos(i*cfg.radians/total))-20*Math.cos(i*cfg.radians/total);});
      
       
          d.forEach(function(y, x){
            dataValues = [];
            g.selectAll(".nodes")
            .data(y, function(j, i){
              dataValues.push([
              cfg.w/2*(1-(parseFloat(Math.max(j.value, 0))/cfg.maxValue)*cfg.factor*Math.sin(i*cfg.radians/total)), 
              cfg.h/2*(1-(parseFloat(Math.max(j.value, 0))/cfg.maxValue)*cfg.factor*Math.cos(i*cfg.radians/total))
              ]);
            });
            dataValues.push(dataValues[0]);
            g.selectAll(".area")
                   .data([dataValues])
                   .enter()
                   .append("polygon")
                   .attr("class", "radar-chart-serie"+series)
                   .style("stroke-width", "2px")
                   .style("stroke", cfg.color(series))
                   .attr("points",function(d) {
                     var str="";
                     for(var pti=0;pti<d.length;pti++){
                       str=str+d[pti][0]+","+d[pti][1]+" ";
                     }
                     return str;
                    })
                   .style("fill", function(j, i){return cfg.color(series)})
                   .style("fill-opacity", cfg.opacityArea)
                   .on('mouseover', function (d){
                            z = "polygon."+d3.select(this).attr("class");
                            g.selectAll("polygon")
                             .transition(200)
                             .style("fill-opacity", 0.1); 
                            g.selectAll(z)
                             .transition(200)
                             .style("fill-opacity", .7);
                            })
                   .on('mouseout', function(){
                            g.selectAll("polygon")
                             .transition(200)
                             .style("fill-opacity", cfg.opacityArea);
                   });
            series++;
          });
          series=0;
      
      
      var tooltip = d3.select("body").append("div").attr("class", "toolTip");
          d.forEach(function(y, x){
            g.selectAll(".nodes")
            .data(y).enter()
            .append("svg:circle")
            .attr("class", "radar-chart-serie"+series)
            .attr('r', cfg.radius)
            .attr("alt", function(j){return Math.max(j.value, 0)})
            .attr("cx", function(j, i){
              dataValues.push([
              cfg.w/2*(1-(parseFloat(Math.max(j.value, 0))/cfg.maxValue)*cfg.factor*Math.sin(i*cfg.radians/total)), 
              cfg.h/2*(1-(parseFloat(Math.max(j.value, 0))/cfg.maxValue)*cfg.factor*Math.cos(i*cfg.radians/total))
            ]);
            return cfg.w/2*(1-(Math.max(j.value, 0)/cfg.maxValue)*cfg.factor*Math.sin(i*cfg.radians/total));
            })
            .attr("cy", function(j, i){
              return cfg.h/2*(1-(Math.max(j.value, 0)/cfg.maxValue)*cfg.factor*Math.cos(i*cfg.radians/total));
            })
            .attr("data-id", function(j){return j.area})
            .style("fill", "#fff")
            .style("stroke-width", "2px")
            .style("stroke", cfg.color(series)).style("fill-opacity", .9)
            .on('mouseover', function (d){
              console.log(d.area)
                  tooltip
                    .style("left", d3.event.pageX - 40 + "px")
                    .style("top", d3.event.pageY - 80 + "px")
                    .style("display", "inline-block")
                            .html((d.area) + "<br><span>" + (d.value) + "</span>");
                  })
                  .on("mouseout", function(d){ tooltip.style("display", "none");});
      
            series++;
          });
          }
    };  

    var width = 300,height = 300;

    // Config for the Radar chart
    var config = {
        w: width,
        h: height,
        maxValue: 100,
        levels: 5,
        ExtraWidthX: 300
    }

    RadarChart.draw("#"+divID, data, config,colors);

    var svg = d3.select('body')
        .selectAll('svg')
        .append('svg')
        .attr("width", width)
        .attr("height", height);
}

module.exports ={
    drawRankChart,
    drawRelationshipTable,
    drawPieChart,
    drawRadarChart
}