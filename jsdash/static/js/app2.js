// //create empty list for each id
// var idList = [] 

// //read json file
// var file = "samples.json";
// var data = []

// //select Demo info panel and create an ordered list tag
// var demoPanel = d3.select(".panel-body")
// demoPanel.append("ol").classed("panel-list", true)
// var panelList = d3.select(".panel-list")


//use d3 to create a dropdown list of all ids
function load(){
    var dropdownMenu = d3.select("#selDataset")
        
    d3.json("samples.json").then((incoming)=> {
                    
        incoming.names.forEach(function (id){ 
            dropSelect
            .append("option")
            .text(id)
            // buildplot(id);
        });
    });
};

load()

//optionChanged function to send selected value from downdown
//to buildplot function
function optionChanged(value){
    console.log(value)
    buildplot(value);
};


function buildplot(id){ 

    d3.json(file).then((incoming)=> {

        //filter json by value selected and set variables for charts
        var filteredId = incoming.samples.filter(d => d.id === id);
        var idNum = filteredId[0].id;
        var values = filteredId[0].sample_values;
        var otuIds = filteredId[0].otu_ids;
        var hoverLabels = filteredId[0].otu_labels;
        var values10 = filteredId[0].sample_values.slice(0, 10);
        var otuIds10 = filteredId[0].otu_ids.slice(0, 10).toString();
        var hoverLabels10 = filteredId[0].otu_labels.slice(0, 10);
        conssole.log(otuIds);
        //collect metadata for demo info chart
        var filteredMeta = incoming.metadata.filter(d => d.id === +id);
        var freq = incoming.metadata.filter(d => d.id === +id).map(d => d.wfreq);
        console.log(`meta wash: ${freq}`)
      
        //remove any list from demo panel if it exists
        panelList.selectAll('li').remove("html");
        
        //create a <li> of demo info within panel
        Object.entries(filteredMeta[0]).forEach( function(key, value){
            console.log(key, value);
            d3.select(".panel-list").append("li").text(key[0].toUpperCase() + ": " + key[1])
        });

          //build chart info
        var data = [{
            x: values10,
            y: otuIds10,
            text: hoverLabels10,
            type: "bar",
            orientation: "h",
            marker: {
                color: "blue"
                // width: 5
            }
        }];
         
        //bubble chart
        var data1 = [{
            x: otuIds,
            y: values,
            mode: "markers",
            marker: {
                size: values,
                color: otuIds
            },
            text: hoverLabels
        }];

        //set data for guage chart
        var data2 = [{
                domain: {x: [0, 1], y: [0, 1] },
                value: parseFloat(freq),
                title: {text: `Weekly Washing Frequency ` },
                type: "indicator",
                mode: "gauge+number+delta",
                gauge: {
                    axis: {range: [null, 9] },
                    steps: [
                        {range: [0, 2], color: "cyan" },
                        {range: [2, 4], color: "royalblue" },
                        {range: [4, 6], color: "darkblue" },
                        {range: [6, 9], color: "lightgreen" }
                    ],
                    threshold: {
                        line: {color: "red", width: 5 },
                        thickness: 1,
                        value: 9
                      }
                }
            }];
        
        //layout for charts
        var layout = {
            title: `Top 10 OTU for Subject ID: ${idNum}`, 
            xaxis: {title: "Sample Values"}, 
            yaxis: {title: "OTU ids",
                    tickmode: "linear",
                    ticktext: [otuIds],
                    tickvtextsrc: otuIds},
            margin: {
                l: 75,
                r: 75,
                t: 75,
                b: 30
            }
        };
        //bubble chart
        var layout1 = {
            xaxis: { title: `OTU ID ${idNum}` },
            height: 500,
            width: 900
        };

        //guage chart
        
        var degrees = (20 * freq), radius = .15;
        var radians = degrees * Math.PI / 180;
        var x = radius - (radius * Math.cos(radians)) +.1;
        var y = radius * Math.sin(radians) +.3;
        if (degrees >= 90){
            x = x + .5;
        };
 
        var layout2 = {
            shapes:[{
                type: 'line',
                x0: .5,
                y0: .1,
                x1: x,
                y1: y,
                line: {
                  color: 'black',
                  width: 5
                }
              }],
            width: 700,
            height: 500,
            xaxis: {visible: false, range: [-1, 1]},
            yaxis: {visible: false, range: [-1, 1]}
        };
        
    //plot charts
    Plotly.newPlot("bubble", data1, layout1);
    Plotly.newPlot("bar", data, layout);
    Plotly.newPlot("gauge", data2, layout2, {staticPlot: true});
    });
};

//initiate webpage with id 940
buildplot('940');