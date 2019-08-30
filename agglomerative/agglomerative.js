/***************************************
Authors: Matthew Reilly, Mike Bostock
16/04/19
What it does:
renders agglomerative cluster algorthim inputted from csv created in python

****************************************/


function agglomerative(targetDOMelement) {

var agglomerativeObject = {};
var target = targetDOMelement;
var colorScale = ["red","purple","yellow","green","blue","cyan","orange","gray","red","purple","yellow","green","red","cyan","orange","gray","red","purple","yellow","green","red","cyan","orange","gray"];


//get size of object
Object.size = function(obj) {
      var size = 0, key;
      for (key in obj) {
        console.log(key);
          if (obj.hasOwnProperty(key)) size++;
      }
      return size;
  };

agglomerativeObject.loadAndRenderDataset = function () {

    layoutAndRenderData();
    return agglomerativeObject;
  };


  var width = 1280,
      height = 720,
      maxRadius = 150;
      var div = d3.select("body").append("div")
    .attr("class", "tooltip")
    .style("opacity", 0);
var nodes = []
    color = d3.scaleOrdinal(d3.schemeCategory10);


    function layoutAndRenderData() {
      d3.csv("array.csv",function(data){
        console.log(data);
        console.log(data);
        var size = 0;
        data.forEach(function(row) {
                    size =  Object.keys(row).length
                  });
        console.log(size)
      console.log(size)
        var c =0;
        var s = "0.000000";

        var name = new Array(size);
        nodes = d3.range(size).map(function() {
          var x = parseFloat(data[0][s]),
              y = parseFloat(data[1][s]),
              r = data[2][s],
              l = parseInt(data[3][s]),
              clu = data[4][s],
              d = {x: x,y: y, radius: r, label: l, cluster: clu};
              c++;
              s =  c+".000000";
          return d;
        });
      console.log(nodes);

      var svg = d3.select("body").append("svg")
                                     .attr("width", width)
                                      .attr("height", height);
  var g = svg.append("g").attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");
  var circles = g.selectAll("circle")
                           .data(nodes)
                           .enter()
                           .append("circle");

  var circle = circles
                        .attr("cx", function (d) { return d.x*3; })
                        .attr("cy", function (d) { return d.y*3; })
                        .attr("r", function (d) { return d.radius*3; })
                        .style("fill", function(d) { return colorScale[parseFloat(d.cluster)-1]; })
                        .style("opacity", 0.5)
                        .style("stroke-width", 1)
                        .style("stroke", "gray")
                        .on("mouseover", function(d) {
                         div.transition()
                           .duration(200)
                           .style("opacity", .9);
                         div.html(d.label)
                           .style("left", (d3.event.pageX) + "px")
                           .style("top", (d3.event.pageY - 28) + "px");
                         })
                       .on("mouseout", function(d) {
                         div.transition()
                           .duration(500)
                           .style("opacity", 0);
                         });

      });

    }

return agglomerativeObject;
}
