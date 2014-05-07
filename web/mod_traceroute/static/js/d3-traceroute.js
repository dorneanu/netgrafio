/*
* @Author: victor
* @Date:   2014-04-10
* @Last Modified by:   victor
* @Last Modified time: 2014-04-23
* @Copyright:
*
*    This file is part of the netgrafio project.
*
*
*    Copyright (c) 2014 Victor Dorneanu <info AAET dornea DOT nu>
*
*    Permission is hereby granted, free of charge, to any person obtaining a copy
*    of this software and associated documentation files (the "Software"), to deal
*    in the Software without restriction, including without limitation the rights
*    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
*    copies of the Software, and to permit persons to whom the Software is
*    furnished to do so, subject to the following conditions:
*
*    The above copyright notice and this permission notice shall be included in all
*    copies or substantial portions of the Software.
*
*    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
*    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
*    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
*    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
*    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
*    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
*    SOFTWARE.
*
*    The MIT License (MIT)
*/


/* --------------------------------------------------------------------------
   DataTable functions
   ----------------------------------------------------------------------- */
function updateTables() {
  // First destroy dataTable object
  $('#dataTables-example').dataTable().fnDestroy();
  $('#dataTables-example').empty();

  // Add new one
  newDataTable("d3-table", ["id", "host", "time"]);
  updateDataTable("d3-table",force.links(), ["id", "host", "time"]);
  $('#dataTables-example').dataTable();
}


function updateDataTable(el, data, columns) {
    var table = d3.select("#" + el).select('table');
    var tbody = table.selectAll('tbody');

    // create a row for each object in the data
    var rows = tbody.selectAll("tr")
        .data(data)
        .enter()
        .append("tr");

    // create a cell in each row for each column
    var cells = rows.selectAll("td")
        .data(function(d) { return [d.source.route_id, d.source.id, d.source.route_time]; })
        .enter()
        .append("td")
            .text(function(d) { return d; });
}

function newDataTable(el, columns) {
    // Create a single element if none is found
    d3.select("#" + el).selectAll("table").data([0]).enter().append('table');
    var table = d3.select("#" + el).select('table')
                  .attr("id", "dataTables-example")
                  .attr("class", "table table-striped table-bordered table-hover")

    table.selectAll('thead').data([0]).enter().append('thead');
    var thead = table.select('thead');

    table.selectAll('tbody').data([0]).enter().append('tbody');
    var tbody = table.select('tbody');

    // append the header row
    thead.append("tr")
        .selectAll("th")
        .data(columns )
        .enter()
        .append("th")
            .text(function(column) { return column; });
}


/* --------------------------------------------------------------------------
     WebSocket handler
  -------------------------------------------------------------------------*/
function WebSocketConn(graph, url) {
  // WebSocket
  var ws = new WebSocket(url);
  var nodes = graph.getNodes();
  var currentNode;

  // Show connection success
  $.pnotify({
      title: 'WebSocket',
      text: 'Connected to ' + url,
      type: 'success'
  });

  // Wait for new data
  ws.onmessage = function(evt) {
      // Insert new value
      var data = JSON.parse(evt.data);

      // Insert new node
      if (typeof data.nodes != 'undefined') {
        data.nodes.forEach(function (node) {
          nodeObject = node;

          // Check if node already in graph
          found_node = graph.findNode(nodeObject.id);

          if (found_node == undefined) {
            graph.addNode(nodeObject);

            // Mark first node
            if (nodes.length == 1)
              graph.addAttrToNode("class", "first", nodeObject.id);

            // No links between empty nodes
            if (currentNode) {
              new_link = { "source": currentNode, "target": nodeObject.id}
              graph.addLink(new_link);
            }

            // Set current node and also last element in the traceroute chain
            if (currentNode)
              graph.removeAttrFromNode("class", "last", currentNode);
            currentNode = nodeObject.id;
            graph.addAttrToNode("class", "last", currentNode);
          } else {
            currentNode = found_node.id;
          }
        })

        // Add tipsy tooltips
        $("g").tipsy({
             gravity: "e",
             fade: true,
             html: true,
             title: function() {
                 d = this.__data__, n = d.id;
                 var hover = "<div class='hoverPopUp'>";
                 hover += "<span class='courseTitle'> " + n + "</span><br />";
                 hover += "</div>";
                 return hover;
             }
         });

      }
  }
}


/* --------------------------------------------------------------------------
     Add new graph
  -------------------------------------------------------------------------*/

// Add new data table
var peopleTable = newDataTable("d3-table", ["ID", "Host", "Time in ms"])

// Create new graph class and override some methods
function TracerouteGraph () {
    this.link_distance = 10;
    this.node_charge = -5;
}

// Override methods
TracerouteGraph.prototype = new D3Graph("d3-traceroute-graph");
TracerouteGraph.prototype.updateLinks = function () {
    updateTables();
    this.update();
}

// Add new graph
d3DirectedGraph = new TracerouteGraph();
force = d3DirectedGraph.getForce();
d3DirectedGraph.init();

// Tell graph it should behave like a tree
d3DirectedGraph.setTree(true);
d3DirectedGraph.setSelf(d3DirectedGraph);

// Create controller
graph = new D3GraphController(d3DirectedGraph);

// Add new WebSocket
ws = new WebSocketConn(graph, "ws://localhost:8080/websocket");

$.pnotify({
    title: 'Waiting for packets',
    text: 'Now you should send some JSON packets to the websocket. Have a look at the informational stuff tabs how to do that.',
    nonblock: true,
    hide: false,
    closer: false,
    sticker: false,
    type: 'info'
});

// Add some dummy nodes and links
/*
graph.addNodeByID("127.0.0.1");
graph.addNodeByID("google.com");
graph.addNodeByID("facebook.com");
graph.addNodeByID("faz.net");
graph.addNodeByID("nullsecurity.net");
graph.addNodeByID("nsa.gov");

graph.addLink("127.0.0.1", "google.com");
graph.addLink("facebook.com", "nsa.gov");
graph.addLink("127.0.0.1", "nsa.gov");
graph.addLink("nullsecurity.net", "google.com");
graph.addLink("google.com", "faz.net");
graph.addLink("google.com", "facebook.com");

// */

var colors = d3.scale.category20();
// Add tooltip



