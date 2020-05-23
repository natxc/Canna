// from data.js
var tableData = data;

//  declaring variables

var tbody = d3.select("tbody");
var table = d3.selectAll(".table");
var button = d3.select(".btn-default");
var inputField= d3.select("#datetime");
var columns = ["datetime", "city", "state", "country", "shape", "durationMinutes", "comments"]

data.forEach((alienSigthing) => {
  // for each element in data, append a row to tbody
  var row = tbody.append("tr");
  Object.entries(alienSigthing).forEach(([key, value]) => {
    var cell = row.append("td");
    cell.text(value);
  });
});


// filter datetime button
var button = d3.select("#filter-btn");

button.on("click", function() {
    var date = d3.select("#datetime").property("value");
    filtered = tableData
    if (date) {
        filtered = filtered.filter((row) => row.datetime === date);
    };
        console.log(filtered);
        // clear tbody rows
        tbody.html("");

        filtered.forEach((ufoSight) => {
            var row = tbody.append("tr");
            Object.entries(ufoSight).forEach(([key, value]) => {
                var cell = row.append("td");
                cell.text(value);
            });
        });
    });
