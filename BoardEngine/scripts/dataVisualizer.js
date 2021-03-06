const cardRenderer = require('../scripts/cardRenderer'
)

function drawCurve(divID,yDomain,xDomin,data1,data2) {
    $('#' + divID).text("")
    // set the dimensions and margins of the graph
    var margin = { top: 10, right: 30, bottom: 30, left: 60 },
        width = 1460 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    var svg = d3.select('#' + divID)
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

    var x = d3.scaleLinear()
        .domain(xDomin)
        .range([0, width]);
    svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x));

    // Add Y axis
    var y = d3.scaleLinear()
        .domain(yDomain)
        .range([height, 0]);
    svg.append("g")
        .call(d3.axisLeft(y));

    // Add the line
    svg.append("path")
        .datum(data1)
        .attr("fill", "none")
        .attr("stroke", "#85847d")
        .attr("stroke-width", 1.5)
        .attr("d", d3.line()
            .x(function (d) { return x(d[0]) })
            .y(function (d) { return y(d[1]) })
        )


    svg.append("path")
    .datum(data2)
    .attr("fill", "none")
    .attr("stroke", "#6223a2")
    .attr("stroke-width", 1.5)
    .attr("d", d3.line()
        .x(function (d) { return x(d[0]) })
        .y(function (d) { return y(d[1]) })
    )

    // draw lastest indicator
    if(data1.length > 0){
        let lastValue = data1[data1.length-1][1].toFixed(2)
        svg.append("circle").attr("cx", 30).attr("cy", 30).attr("r", 6).style("fill", "#85847d")
        svg.append("text").attr("x", 50).attr("y", 30).text("latest reward: "+lastValue).style("font-size", "15px").attr("alignment-baseline", "middle")    
    }

    if(data2.length > 0){
        let lastValue = data2[data2.length-1][1].toFixed(2)
        svg.append("circle").attr("cx", 30).attr("cy", 10).attr("r", 9).style("fill", "#6223a2")
        svg.append("text").attr("x", 50).attr("y", 10).text("recent win rate: "+lastValue+"%").style("font-size", "20px").attr("alignment-baseline", "middle")    
    }
}

function drawHistorgram(csvURL, xValName,valueName,divID,color){
    $('#' + divID).text("")
    let titleDiv = $(document.createElement('h2')).text(valueName)
    let chartDiv = $(document.createElement('div')).attr('id', divID + '-chart')
    $('#' + divID).append(titleDiv, chartDiv)

    // set the dimensions and margins of the graph
    var margin = { top: 30, right: 30, bottom: 70, left: 60 },
        width = 960 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;


    // append the svg object to the body of the page
    var svg = d3.select("#" + divID + '-chart')
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    // Initialize the X axis
    var x = d3.scaleBand()
        .range([0, width])
        .padding(0.2);
    var xAxis = svg.append("g")
        .attr("transform", "translate(0," + height + ")")

    // Initialize the Y axis
    var y = d3.scaleLinear()
        .range([height, 0]);
    var yAxis = svg.append("g")
        .attr("class", "myYaxis")

    update(valueName,color)

    // A function that create / update the plot for a given variable:
    function update(selectedVar, color) {
        // Parse the Data
        d3.csv(csvURL, function (data) {
            // rank data
            for(let i = 0; i < data.length; i++){
                for(let j = i+1; j < data.length; j++){
                    if(parseFloat(data[i][selectedVar]) > parseFloat(data[j][selectedVar])){
                        let temp = data[i]
                        data[i] = data[j]
                        data[j] = temp
                    }
                }
            }
            // X axis
            x.domain(data.map(function (d) { return d[xValName]; }))
            xAxis.transition().duration(1000).call(d3.axisBottom(x))

            // Add Y axis
            y.domain([0, d3.max(data, function (d) { return +d[selectedVar] })]);
            yAxis.transition().duration(1000).call(d3.axisLeft(y));

            // variable u: map data to existing bars
            var u = svg.selectAll("rect")
                .data(data)

            function mouseover() {
                d3.select(this)
                    .style("stroke", "black")
                    .style("opacity", 1)
            }

            function mouseleave() {
                d3.select(this)
                    .style("stroke", "none")
                    .style("opacity", 0.8)
            }

            function mouseclick() {

            }
            // update bars
            u
                .enter()
                .append("rect")
                .merge(u)
                .transition()
                .duration(1000)
                .attr("x", function (d) { return x(d[xValName]); })
                .attr("y", function (d) { return y(d[selectedVar]); })
                .attr("width", x.bandwidth())
                .attr("height", function (d) { return height - y(d[selectedVar]); })
                .attr("fill", color)

            svg.selectAll("rect")
                .on('mouseover', mouseover)
                .on('mouseleave', mouseleave)
                .on('click', mouseclick)
        })
    }
}

function drawRankChart(csvURL, xValName, divID) {
    $('#' + divID).text("")
    let optionDiv = $(document.createElement('div'))
    let chartDiv = $(document.createElement('div')).attr('id', divID + '-chart')
    $('#' + divID).append(optionDiv, chartDiv)

    // set the dimensions and margins of the graph
    var margin = { top: 30, right: 30, bottom: 70, left: 60 },
        width = 460 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;


    // append the svg object to the body of the page
    var svg = d3.select("#" + divID + '-chart')
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    // Initialize the X axis
    var x = d3.scaleBand()
        .range([0, width])
        .padding(0.2);
    var xAxis = svg.append("g")
        .attr("transform", "translate(0," + height + ")")

    // Initialize the Y axis
    var y = d3.scaleLinear()
        .range([height, 0]);
    var yAxis = svg.append("g")
        .attr("class", "myYaxis")


    // A function that create / update the plot for a given variable:
    function update(selectedVar, color) {
        // Parse the Data
        d3.csv(csvURL, function (data) {
            // X axis
            x.domain(data.map(function (d) { return d[xValName]; }))
            xAxis.transition().duration(1000).call(d3.axisBottom(x))

            // Add Y axis
            y.domain([0, d3.max(data, function (d) { return +d[selectedVar] })]);
            yAxis.transition().duration(1000).call(d3.axisLeft(y));

            // variable u: map data to existing bars
            var u = svg.selectAll("rect")
                .data(data)

            function mouseover() {
                d3.select(this)
                    .style("stroke", "black")
                    .style("opacity", 1)
            }

            function mouseleave() {
                d3.select(this)
                    .style("stroke", "none")
                    .style("opacity", 0.8)
            }

            function mouseclick() {

            }
            // update bars
            u
                .enter()
                .append("rect")
                .merge(u)
                .transition()
                .duration(1000)
                .attr("x", function (d) { return x(d[xValName]); })
                .attr("y", function (d) { return y(d[selectedVar]); })
                .attr("width", x.bandwidth())
                .attr("height", function (d) { return height - y(d[selectedVar]); })
                .attr("fill", color)

            svg.selectAll("rect")
                .on('mouseover', mouseover)
                .on('mouseleave', mouseleave)
                .on('click', mouseclick)
        })
    }

    // fill option Buttons
    d3.csv(csvURL, function (data) {
        let optionList = data.columns
        optionList.shift()
        console.log(optionList)
        for (i = 0; i < optionList.length; i++) {
            let optionBtn = $(document.createElement('button'))
                .text(optionList[i])
                .attr('class', 'btn')
                .css('color', '#69b3a2')
                .click(function () {
                    let option = $(this).text()
                    let color = '#69b3a2'
                    update($(this).text(), color)
                })
            optionDiv.append(optionBtn)
        }
        // Initialize plot
        update(optionList[0], "#69b3a2")
    })
}

function drawRelationshipTable(cvsURL, divID, gameName) {
    let CARD_ONE_KEY = "Card One Name"
    let CARD_TWO_KEY = "Card Two Name"
    let VALUE_KEY = "Combination Play Count"

    $("#" + divID).text("")
    // set the dimensions and margins of the graph
    var margin = { top: 10, right: 25, bottom: 0, left: 120 },
        width = 670 - margin.left - margin.right,
        height = 480 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    var svg = d3.select("#" + divID)
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

    //Read the data
    d3.csv(cvsURL, function (data) {
        // Labels of row and columns -> unique identifier of the column called 'group' and 'variable'
        var myGroups = d3.map(data, function (d) { return d[CARD_ONE_KEY]; }).keys()
        var myVars = d3.map(data, function (d) { return d[CARD_TWO_KEY]; }).keys()

        // Build X scales and axis:
        var x = d3.scaleBand()
            .range([0, width])
            .domain(myGroups)
            .padding(0.05);
        svg.append("g")
            .style("font-size", 15)
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(x).tickSize(0))
            .select(".domain").remove()

        // Build Y scales and axis:
        var y = d3.scaleBand()
            .range([height, 0])
            .domain(myVars)
            .padding(0.05);
        svg.append("g")
            .style("font-size", 15)
            .call(d3.axisLeft(y).tickSize(0))
            .select(".domain").remove()

        // Build color scale
        let max = d3.max(data, function (d) { return parseInt(d[VALUE_KEY]); });
        var myColor = d3.scaleLinear()
            .range(["white", "#ff1100"])
            .domain([1, max])

        // create a tooltip
        var tooltip = d3.select("#" + divID)
            .append("div")
            .style("opacity", 0)
            .attr("class", "tooltip")
            .style("background-color", "white")
            .style("border", "solid")
            .style("border-width", "2px")
            .style("border-radius", "5px")
            .style("padding", "5px")
            .style("position", "relative")
            .style("width", "300px")

        // Three function that change the tooltip when user hover / move / leave a cell
        var mouseover = function (d) {
            tooltip
                .style("opacity", 1)
            d3.select(this)
                .style("stroke", "black")
                .style("opacity", 1)
            $

            let card1 = d[CARD_ONE_KEY]
            let card2 = d[CARD_TWO_KEY]
            refreshCardTooltips(card1, card2)
        }

        var mousemove = function (d) {
            let card1 = d[CARD_ONE_KEY]
            let card2 = d[CARD_TWO_KEY]
            tooltip
                .html("occur times: " + d[VALUE_KEY])
                .style("left", (d3.mouse(this)[0] + 70) + "px")
                .style("top", (d3.mouse(this)[1]) - 560 + "px")
        }
        var mouseleave = function (d) {
            tooltip
                .style("opacity", 0)
            d3.select(this)
                .style("stroke", "none")
                .style("opacity", 0.8)
            clearCardTooltips()
        }

        // add the squares
        svg.selectAll()
            .data(data, function (d) { return d[CARD_ONE_KEY] + ':' + d[CARD_TWO_KEY]; })
            .enter()
            .append("rect")
            .attr("x", function (d) { return x(d[CARD_ONE_KEY]) })
            .attr("y", function (d) { return y(d[CARD_TWO_KEY]) })
            .attr("rx", 4)
            .attr("ry", 4)
            .attr("width", x.bandwidth())
            .attr("height", y.bandwidth())
            .style("fill", function (d) { return myColor(d[VALUE_KEY]) })
            .style("stroke-width", 4)
            .style("stroke", "none")
            .style("opacity", 0.8)
            .on("mouseover", mouseover)
            .on("mousemove", mousemove)
            .on("mouseleave", mouseleave)
    })

    let card1DivID = 'card-relationship-card1'
    let card2DivID = 'card-relationship-card2'
    function refreshCardTooltips(cardName1, cardName2) {
        $('#' + card1DivID).text("")
            .append(cardRenderer.createCardElementByName(gameName, cardName1))
            .append('<h2>First Card</h2>')

        $('#' + card2DivID).text("")
            .append(cardRenderer.createCardElementByName(gameName, cardName2))
            .append('<h2>Second Card</h2>')
    }

    function clearCardTooltips(cardName1, cardName2) {
        $('#' + card1DivID).text("")
        $('#' + card2DivID).text("")
    }
}

function drawDistribution(cvsURL, divID) {
    $("#" + divID).text("")
    // set the dimensions and margins of the graph
    var margin = { top: 30, right: 30, bottom: 30, left: 60 },
        width = 460 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    var svg = d3.select("#" + divID)
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

    // get the data
    d3.csv(cvsURL, function (data) {
        // add the x Axis
        var x = d3.scaleLinear()
            .domain([0, 100])
            .range([0, width]);
        svg.append("g")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(x));


        // Compute kernel density estimation
        var kde = kernelDensityEstimator(kernelEpanechnikov(7), x.ticks(60))
        var density = kde(data.map(function (d) { return d.value; }))
        let maxDen = d3.max(density, function (d) { return parseFloat(d[1]); });
        //console.log(density)

        // add the y Axis
        var y = d3.scaleLinear()
            .range([height, 0])
            .domain([0, maxDen]);

        svg.append("g")
            .call(d3.axisLeft(y));

        // Plot the area
        svg.append("path")
            .attr("class", "mypath")
            .datum(density)
            .attr("fill", "#69b3a2")
            .attr("opacity", ".8")
            .attr("stroke", "#000")
            .attr("stroke-width", 1)
            .attr("stroke-linejoin", "round")
            .attr("d", d3.line()
                .curve(d3.curveBasis)
                .x(function (d) { return x(d[0]); })
                .y(function (d) { return y(d[1]); })
            );
    });

    // Handmade legend
    // svg.append("circle").attr("cx", 300).attr("cy", 30).attr("r", 6).style("fill", "#69b3a2")
    // svg.append("circle").attr("cx", 300).attr("cy", 60).attr("r", 6).style("fill", "#69b3a2")
    // svg.append("circle").attr("cx", 300).attr("cy", 90).attr("r", 6).style("fill", "#69b3a2")
    // svg.append("circle").attr("cx", 300).attr("cy", 120).attr("r", 6).style("fill", "#404080")
    // svg.append("text").attr("x", 320).attr("y", 30).text("average: 123").style("font-size", "15px").attr("alignment-baseline", "middle")
    // svg.append("text").attr("x", 320).attr("y", 60).text("middle: 123").style("font-size", "15px").attr("alignment-baseline", "middle")
    // svg.append("text").attr("x", 320).attr("y", 90).text("max:999").style("font-size", "15px").attr("alignment-baseline", "middle")
    // svg.append("text").attr("x", 320).attr("y", 120).text("min:-1").style("font-size", "15px").attr("alignment-baseline", "middle")

    // Function to compute density
    function kernelDensityEstimator(kernel, X) {
        return function (V) {
            return X.map(function (x) {
                return [x, d3.mean(V, function (v) { return kernel(x - v); })];
            });
        };
    }


    function kernelEpanechnikov(k) {
        return function (v) {
            return Math.abs(v /= k) <= 1 ? 0.75 * (1 - v * v) / k : 0;
        };
    }
}

function drawDualDistribution(csvURL, divID) {
    $("#" + divID).text("")
    // set the dimensions and margins of the graph
    var margin = { top: 30, right: 30, bottom: 30, left: 60 },
        width = 460 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    var svg = d3.select("#" + divID)
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

    // get the data
    d3.csv(csvURL, function (data) {
        let range = [-50, 250]
        // add the x Axis
        var x = d3.scaleLinear()
            .domain(range)
            .range([0, width]);
        svg.append("g")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(x));


        // Compute kernel density estimation
        var kde = kernelDensityEstimator(kernelEpanechnikov(7), x.ticks(60))
        var density1 = kde(data
            .filter(function (d) { return d.type === "Player HP" })
            .map(function (d) { return d.value; }))
        let maxDen1 = d3.max(density1, function (d) { return parseFloat(d[1]); });

        var density2 = kde(data
            .filter(function (d) { return d.type === "Boss HP" })
            .map(function (d) { return d.value; }))
        let maxDen2 = d3.max(density2, function (d) { return parseFloat(d[1]); });

        // add the first y Axis
        var y1 = d3.scaleLinear()
            .range([height / 2, 0])
            .domain([0, maxDen1]);
        svg.append("g")
            .attr("transform", "translate(-20,0)")
            .call(d3.axisLeft(y1).tickValues([0.05, 0.1]));

        // add the first y Axis
        var y2 = d3.scaleLinear()
            .range([height / 2, height])
            .domain([0, maxDen2]);
        svg.append("g")
            .attr("transform", "translate(-20,0)")
            .call(d3.axisLeft(y2).ticks(2).tickSizeOuter(0));

        // Plot the area
        svg.append("path")
            .attr("class", "mypath")
            .datum(density1)
            .attr("fill", "#69b3a2")
            .attr("opacity", ".6")
            .attr("stroke", "#000")
            .attr("stroke-width", 1)
            .attr("stroke-linejoin", "round")
            .attr("d", d3.line()
                .curve(d3.curveBasis)
                .x(function (d) { return x(d[0]); })
                .y(function (d) { return y1(d[1]); })
            );

        // Plot the area
        svg.append("path")
            .attr("class", "mypath")
            .datum(density2)
            .attr("fill", "#404080")
            .attr("opacity", ".6")
            .attr("stroke", "#000")
            .attr("stroke-width", 1)
            .attr("stroke-linejoin", "round")
            .attr("d", d3.line()
                .curve(d3.curveBasis)
                .x(function (d) { return x(d[0]); })
                .y(function (d) { return y2(d[1]); })
            );

    });

    // Handmade legend
    svg.append("circle").attr("cx", 290).attr("cy", 30).attr("r", 6).style("fill", "#69b3a2")
    svg.append("circle").attr("cx", 290).attr("cy", 60).attr("r", 6).style("fill", "#404080")
    svg.append("text").attr("x", 310).attr("y", 30).text("player HP").style("font-size", "15px").attr("alignment-baseline", "middle")
    svg.append("text").attr("x", 310).attr("y", 60).text("boss HP").style("font-size", "15px").attr("alignment-baseline", "middle")

    // Function to compute density
    function kernelDensityEstimator(kernel, X) {
        return function (V) {
            return X.map(function (x) {
                return [x, d3.mean(V, function (v) { return kernel(x - v); })];
            });
        };
    }
    function kernelEpanechnikov(k) {
        return function (v) {
            return Math.abs(v /= k) <= 1 ? 0.75 * (1 - v * v) / k : 0;
        };
    }

}

function drawRadarChart(divID, data, colors) {
    var RadarChart = {
        draw: function (id, d, options, colors) {
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

            if ('undefined' !== typeof options) {
                for (var i in options) {
                    if ('undefined' !== typeof options[i]) {
                        cfg[i] = options[i];
                    }
                }
            }

            cfg.maxValue = 100;

            var allAxis = (d[0].map(function (i, j) { return i.area }));
            var total = allAxis.length;
            var radius = cfg.factor * Math.min(cfg.w / 2, cfg.h / 2);
            var Format = d3.format('%');
            d3.select(id).select("svg").remove();

            var g = d3.select(id)
                .append("svg")
                .attr("width", cfg.w + cfg.ExtraWidthX)
                .attr("height", cfg.h + cfg.ExtraWidthY)
                .append("g")
                .attr("transform", "translate(" + cfg.TranslateX + "," + cfg.TranslateY + ")");

            var tooltip;

            //Circular segments
            for (var j = 0; j < cfg.levels; j++) {
                var levelFactor = cfg.factor * radius * ((j + 1) / cfg.levels);
                g.selectAll(".levels")
                    .data(allAxis)
                    .enter()
                    .append("svg:line")
                    .attr("x1", function (d, i) { return levelFactor * (1 - cfg.factor * Math.sin(i * cfg.radians / total)); })
                    .attr("y1", function (d, i) { return levelFactor * (1 - cfg.factor * Math.cos(i * cfg.radians / total)); })
                    .attr("x2", function (d, i) { return levelFactor * (1 - cfg.factor * Math.sin((i + 1) * cfg.radians / total)); })
                    .attr("y2", function (d, i) { return levelFactor * (1 - cfg.factor * Math.cos((i + 1) * cfg.radians / total)); })
                    .attr("class", "line")
                    .style("stroke", "grey")
                    .style("stroke-opacity", "0.75")
                    .style("stroke-width", "0.3px")
                    .attr("transform", "translate(" + (cfg.w / 2 - levelFactor) + ", " + (cfg.h / 2 - levelFactor) + ")");
            }

            //Text indicating at what % each level is
            for (var j = 0; j < cfg.levels; j++) {
                var levelFactor = cfg.factor * radius * ((j + 1) / cfg.levels);
                g.selectAll(".levels")
                    .data([1]) //dummy data
                    .enter()
                    .append("svg:text")
                    .attr("x", function (d) { return levelFactor * (1 - cfg.factor * Math.sin(0)); })
                    .attr("y", function (d) { return levelFactor * (1 - cfg.factor * Math.cos(0)); })
                    .attr("class", "legend")
                    .style("font-family", "sans-serif")
                    .style("font-size", "10px")
                    .attr("transform", "translate(" + (cfg.w / 2 - levelFactor + cfg.ToRight) + ", " + (cfg.h / 2 - levelFactor) + ")")
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
                .attr("x1", cfg.w / 2)
                .attr("y1", cfg.h / 2)
                .attr("x2", function (d, i) { return cfg.w / 2 * (1 - cfg.factor * Math.sin(i * cfg.radians / total)); })
                .attr("y2", function (d, i) { return cfg.h / 2 * (1 - cfg.factor * Math.cos(i * cfg.radians / total)); })
                .attr("class", "line")
                .style("stroke", "grey")
                .style("stroke-width", "1px");

            axis.append("text")
                .attr("class", "legend")
                .text(function (d) { return d })
                .style("font-family", "sans-serif")
                .style("font-size", "20px")
                .attr("text-anchor", "middle")
                .attr("dy", "1.5em")
                .attr("transform", function (d, i) { return "translate(0, -10)" })
                .attr("x", function (d, i) { return cfg.w / 2 * (1 - cfg.factorLegend * Math.sin(i * cfg.radians / total)) - 60 * Math.sin(i * cfg.radians / total); })
                .attr("y", function (d, i) { return cfg.h / 2 * (1 - Math.cos(i * cfg.radians / total)) - 20 * Math.cos(i * cfg.radians / total); });


            d.forEach(function (y, x) {
                dataValues = [];
                g.selectAll(".nodes")
                    .data(y, function (j, i) {
                        dataValues.push([
                            cfg.w / 2 * (1 - (parseFloat(Math.max(j.value, 0)) / cfg.maxValue) * cfg.factor * Math.sin(i * cfg.radians / total)),
                            cfg.h / 2 * (1 - (parseFloat(Math.max(j.value, 0)) / cfg.maxValue) * cfg.factor * Math.cos(i * cfg.radians / total))
                        ]);
                    });
                dataValues.push(dataValues[0]);
                g.selectAll(".area")
                    .data([dataValues])
                    .enter()
                    .append("polygon")
                    .attr("class", "radar-chart-serie" + series)
                    .style("stroke-width", "2px")
                    .style("stroke", cfg.color(series))
                    .attr("points", function (d) {
                        var str = "";
                        for (var pti = 0; pti < d.length; pti++) {
                            str = str + d[pti][0] + "," + d[pti][1] + " ";
                        }
                        return str;
                    })
                    .style("fill", function (j, i) { return cfg.color(series) })
                    .style("fill-opacity", cfg.opacityArea)
                    .on('mouseover', function (d) {
                        z = "polygon." + d3.select(this).attr("class");
                        g.selectAll("polygon")
                            .transition(200)
                            .style("fill-opacity", 0.1);
                        g.selectAll(z)
                            .transition(200)
                            .style("fill-opacity", .7);
                    })
                    .on('mouseout', function () {
                        g.selectAll("polygon")
                            .transition(200)
                            .style("fill-opacity", cfg.opacityArea);
                    });
                series++;
            });
            series = 0;


            var tooltip = d3.select("body").append("div").attr("class", "toolTip");
            d.forEach(function (y, x) {
                g.selectAll(".nodes")
                    .data(y).enter()
                    .append("svg:circle")
                    .attr("class", "radar-chart-serie" + series)
                    .attr('r', cfg.radius)
                    .attr("alt", function (j) { return Math.max(j.value, 0) })
                    .attr("cx", function (j, i) {
                        dataValues.push([
                            cfg.w / 2 * (1 - (parseFloat(Math.max(j.value, 0)) / cfg.maxValue) * cfg.factor * Math.sin(i * cfg.radians / total)),
                            cfg.h / 2 * (1 - (parseFloat(Math.max(j.value, 0)) / cfg.maxValue) * cfg.factor * Math.cos(i * cfg.radians / total))
                        ]);
                        return cfg.w / 2 * (1 - (Math.max(j.value, 0) / cfg.maxValue) * cfg.factor * Math.sin(i * cfg.radians / total));
                    })
                    .attr("cy", function (j, i) {
                        return cfg.h / 2 * (1 - (Math.max(j.value, 0) / cfg.maxValue) * cfg.factor * Math.cos(i * cfg.radians / total));
                    })
                    .attr("data-id", function (j) { return j.area })
                    .style("fill", "#fff")
                    .style("stroke-width", "2px")
                    .style("stroke", cfg.color(series)).style("fill-opacity", .9)
                    .on('mouseover', function (d) {
                        console.log(d.area)
                        tooltip
                            .style("left", d3.event.pageX - 40 + "px")
                            .style("top", d3.event.pageY - 80 + "px")
                            .style("display", "inline-block")
                            .html((d.area) + "<br><span>" + (d.value) + "</span>");
                    })
                    .on("mouseout", function (d) { tooltip.style("display", "none"); });

                series++;
            });
        }
    };

    var width = 300, height = 300;

    // Config for the Radar chart
    var config = {
        w: width,
        h: height,
        maxValue: 100,
        levels: 5,
        ExtraWidthX: 300
    }

    RadarChart.draw("#" + divID, data, config, colors);

    var svg = d3.select('body')
        .selectAll('svg')
        .append('svg')
        .attr("width", width)
        .attr("height", height);
}

function drawPieChart(divID, data) {
    // clear 
    $("#" + divID).text("")
    // set the dimensions and margins of the graph
    var width = 450
    height = 450
    margin = 40

    // The radius of the pieplot is half the width or half the height (smallest one). I subtract a bit of margin.
    var radius = Math.min(width, height) / 2 - margin

    // append the svg object to the div called 'my_dataviz'
    var svg = d3.select("#" + divID)
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
        .value(function (d) { return d.value; })
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
        .attr('fill', function (d) { return (color(d.data.key)) })
        .attr("stroke", "black")
        .style("stroke-width", "2px")
        .style("opacity", 0.7)

    // Now add the annotation. Use the centroid method to get the best coordinates
    svg
        .selectAll('mySlices')
        .data(data_ready)
        .enter()
        .append('text')
        .text(function (d) { return "grp " + d.data.key })
        .attr("transform", function (d) { return "translate(" + arcGenerator.centroid(d) + ")"; })
        .style("text-anchor", "middle")
        .style("font-size", 17)
}

module.exports = {
    drawHistorgram,
    drawRankChart,
    drawRelationshipTable,
    drawPieChart,
    drawRadarChart,
    drawDistribution,
    drawDualDistribution,
    drawCurve
}