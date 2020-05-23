// # Plot.ly Homework - Belly Button Biodiversity

// Populate dropdown menu
d3.json("samples.json").then(data => {
        
    var data = data;
    console.log(data);
    
    // Isolate patient IDs to add to dropdown
    var patientIDs = data.samples.map(x => x.id);
    console.log(patientIDs);

    // Append options to the dropdownmenu with patientIDs
    for (var i = 0; i < patientIDs.length; i++) {
        dropdownMenu = d3.select("#selDataset");
        dropdownMenu.append("option").text(patientIDs[i]);
    };
});

// Event handler
function optionChanged (id) {
    console.log(id);
    plotID(id)
}


function plotID (id) {

    // Tracking when the function changes
    console.log(`Selection:${id}`);


    // Read data in json and create variables for data and patientIDs
    // Creating a promise to work with data - so all other manipulation must be within this function
    d3.json("samples.json").then(data => {


        // Variables
        // OTU
        var selectionOTU = data.samples.filter(x => x.id === id);
        console.log(selectionOTU);

        // *****Bar Chart Section*****
        var sampleValues = selectionOTU[0].sample_values.slice(0, 10).reverse();
        var otuIDs = selectionOTU[0].otu_ids.slice(0, 10).toString();
        var otuLabels = selectionOTU[0].otu_labels.slice(0, 10).reverse();

        var barData = [{
            x: sampleValues,
            y: otuIDs,
            type: "bar",
            orientation: "h",
            text: otuLabels,
            marker: {
              color: "#FE6625"
            }
        }]

        var barLayout = {
            title: `Belly Button Bacteria`, 
            xaxis: {title: "Frequency of Bacterial Occurence"}, 
            yaxis: {title: "Bacterial Strains"},
        };

        Plotly.newPlot("bar", barData, barLayout);

        // *****Bubble Chart Section*****
        var allSampleValues = selectionOTU[0].sample_values;
        var allOtuLabels = selectionOTU[0].otu_labels.toString();


        var bubbleData = [{
            x: allOtuLabels,
            y: allSampleValues,
            mode: 'markers',
            marker: {
              size: allSampleValues,
              color: "#FB9334"
            },
            text: allOtuLabels
          }];
      
          // set the layout for the bubble plot
          var bubbleLayout = {
            title: `Bacterial Frequency and Variance`,
            xaxis: { title: `Different types of Belly Button Bacteria` },
            yaxis: { title: 'Bacterial Strains' },
            height: 600,
            width: 1000
          };
      
        Plotly.newPlot("bubble", bubbleData, bubbleLayout);

        // *****Metadata (Demographic) Section*****
        var selectionMeta = data.metadata.filter(x => x.id === +id);
        console.log(selectionMeta);

        // Select HTML element
        var demographicData = d3.select('#sample-metadata');

        // Clear demographic data
        demographicData.html('');
  
        // Fill demographic data for metadata section
        demographicData.append('p').text(`Ethnicity: ${selectionMeta[0].ethnicity}`);
        demographicData.append('p').text(`Gender: ${selectionMeta[0].gender}`);
        demographicData.append('p').text(`Age: ${selectionMeta[0].age}`);
        demographicData.append('p').text(`Location: ${selectionMeta[0].location}`);
        demographicData.append('p').text(`Belly Button Type: ${selectionMeta[0].bbtype}`);
        demographicData.append('p').text(`Wash Frequency: ${selectionMeta[0].wfreq}`);


        // *****Gauge Chart Section*****

        var washFrequency = selectionMeta[0].wfreq

        var gaugeData = [{
              domain: { x: [0, 1], y: [0, 1] },
              value: washFrequency,
              title: { text: `Belly Button Scrub Down Routine` },
              type: 'indicator',
              mode: 'gauge+number',
              gauge: {
                axis: { range: [null, 9] },
                bar: { color: '#FB9334' },
                steps: [
                  { range: [0, 1], color: '#167070' },
                  { range: [1, 2], color: '#198080' },
                  { range: [2, 3], color: '#1d9595' },
                  { range: [3, 4], color: '#22aaaa' },
                  { range: [4, 5], color: '#26c0c0' },
                  { range: [5, 6], color: '#2ad5d5' },
                  { range: [6, 7], color: '#3fd9d9' },
                  { range: [7, 8], color: '#55dddd' },
                  { range: [8, 9], color: '#6ae2e2' }
                ]}
            }];
      
          var gaugeLayout = { width: 500, height: 400 };

          Plotly.newPlot('gauge', gaugeData, gaugeLayout);  

  
    }) 
}

// Default plot ID: 940
plotID ('940')