/***************************************
Authors: Matthew Reilly, Mike Bostock
16/04/2019
What it does:
renders force-directed diagram

****************************************/


function force(targetDOMelement) {
var links = [];
var forceObject = {};
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

forceObject.loadAndRenderDataset = function () {

    layoutAndRenderData();
    return forceObject;
  };


  var width = 1280,
      height = 720,
      maxRadius = 150;
      var div = d3.select("body").append("div")
          .attr("class", "tooltip")
          .style("opacity", 0);
var   enternode,updatenode,exitnode
var nodes = []
    color = d3.scaleOrdinal(d3.schemeCategory10);
    // Get the size of an object
    const simulationDurationInMs = 1000; // 20 seconds

    let startTime = Date.now();
    let endTime = startTime + simulationDurationInMs;
    var done = false
    var simulation = d3.forceSimulation(nodes)

    .force("charge", d3.forceManyBody().strength(-350))
    .force("forceX", d3.forceX().strength(.045))
    .force("forceY", d3.forceY().strength(.08))
    .force("center", d3.forceCenter())
    .alphaTarget(1)
    .on("tick", ticked);

    simulation.force('link', d3.forceLink().links(links).strength(.003).distance(1));
    var svg = d3.select(targetDOMelement).append("svg").attr("width", width).attr("height", height).classed("force",true)
        g = svg.append("g").attr("transform", "translate(" + width / 2 + "," + height / 2 + ")"),
        node = g.append("g").attr("stroke", "#fff").attr("stroke-width", 1.5).selectAll(".node");



    function layoutAndRenderData() {

      d3.csv("array.csv",function(data){
          d3.csv("linkage.csv",function(linkage){
        console.log("fffffffffff")
        console.log(data);
        console.log(linkage)
        var size = 0;
        data.forEach(function(row) {
                    size =  Object.keys(row).length
                  });

        var c =0;
        var s = "0.000000";

        var name = new Array(size);
        nodes = d3.range(size).map(function() {

          var r = data[2][s]*3,
                l = parseInt(data[3][s]),
              clu = data[4][s],
              d = { radius: r, label: l, cluster: clu};
              c++;
              s =  c+".000000";
          return d;
        });
        nodes.sort(function(x, y){
          return d3.ascending(x.label, y.label);
})
      console.log(nodes);
      var groups = [];
      for (var i = 0; i < linkage.length; i++){
      console.log(linkage.length);
        if(linkage[i]["1.0"] < linkage.length+1 && linkage[i]["2.0"] < linkage.length+1){
          list = [parseInt(linkage[i]["1.0"]),parseInt(linkage[i]["2.0"])]

          var link = {
            source: nodes[parseInt(linkage[i]["1.0"])],
            target: nodes[parseInt(linkage[i]["2.0"])],
            value: 1
          };
          links.push(link)
          groups.push(list)
        }
        else if (linkage[i]["1.0"] < linkage.length+1 && linkage[i]["2.0"] >= linkage.length+1){
          var list = groups[parseInt(linkage[i]["2.0"]-linkage.length-1)]
          console.log(list)
          console.log(nodes[parseInt(linkage[i]["1.0"])])
          for (var j = 0; j < list.length; j++){
            var link = {
              source: nodes[parseInt(linkage[i]["1.0"])],
              target: nodes[parseInt(list[j])],
              value: 1
            };
            links.push(link)

          }
          list.push(parseInt(linkage[i]["1.0"]))
          groups.push(list)
        }
        else if (linkage[i]["1.0"] >= linkage.length+1 && linkage[i]["2.0"] < linkage.length+1){
          var list = groups[parseInt(linkage[i]["1.0"]-linkage.length-1)]
          console.log(list)
          console.log(nodes[parseInt(linkage[i]["2.0"])])
          for (var j = 0; j < list.length; j++){
            var link = {
              source: nodes[parseInt(linkage[i]["2.0"])],
              target: nodes[parseInt(list[j])],
              value: 1
            };
            links.push(link)

          }
          list.push(parseInt(linkage[i]["2.0"]))
          groups.push(list)
        }
        else if (linkage[i]["1.0"] >= linkage.length+1 && linkage[i]["2.0"] >= linkage.length+1){
          var list1 = groups[parseInt(linkage[i]["1.0"]-linkage.length-1)]
          var list2 = groups[parseInt(linkage[i]["2.0"]-linkage.length-1)]
          var list = list1.concat(list2);
          console.log(list)

          for (var j = 0; j < list.length; j++){
            for (var k = 0; k < list.length; k++){
              if(list[j] != list[k]){
            var link = {
              source: nodes[parseInt(list[j])],
              target: nodes[parseInt(list[k])],
              value: 1
            };
            links.push(link)
          }
          }
          }

          groups.push(list)
        }
    }
    console.log(links);
    console.log(groups);
      // transition
      var t = d3.transition()
          .duration(750);

      // Apply the general update pattern to the nodes.
      node = node.data(nodes, function(d) { return d.name;});
      //exit
      node.exit()
      .classed("updateSelection enterSelection", false)
      .classed("exitSelection", true)
      .transition(t)
          .attr("r", 0)
          .remove();
//update
      node
      .style('fill', function(d) { return colorScale[d.cluster-1];})
      .classed("updateSelection", true)
      .classed("enterSelection exitSelection", false)

          .transition(t).delay(750)
            .attr("r", function(d){ return (d.radius); });
//enter
      node = node.enter().append("circle")
      .style('fill', function(d) { return colorScale[d.cluster-1];})
          .classed("force enterSelection", true)
          .attr("r", function(d){ return (d.radius) })
          .merge(node)
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

      // Update and restart the simulation.
      simulation.nodes(nodes)
        .force("collide", d3.forceCollide().strength(1).radius(function(d){ return (d.radius)+4; }).iterations(1));
});
});
}
//every tick
    function ticked() {
      if(Date.now() > endTime && !Boolean(done)){
      node.attr("cx", function(d) { return d.x; })
          .attr("cy", function(d) { return d.y; })
          done = true;
        }
}


return forceObject;
}
