/*
* @Author: victor
* @Date:   2014-04-22
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
  newDataTable("d3-table", ["source", "target", "count"]);
  updateDataTable("d3-table", graph.getLinks(), ["source", "target", "count"]);
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
        .data(function(d) { return [d.source.id, d.target.id, d.count]; })
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

      // Insert new nodes
      if (typeof data.nodes != 'undefined') {
        data.nodes.forEach(function (node) {
          if (node) {
              nodeObject = {"id": node.id, "class": node.class}
              graph.addNode(nodeObject);
          }
        });
      }

      // Insert new links
      if (typeof data.links != 'undefined') {
        data.links.forEach(function (link) {
          var linkObject = {
            "source": link.source,
            "target": link.target
          }
          graph.addLink(linkObject);
        });
      }

  // Add tipsy tooltips
  $("g").tipsy({
       //gravity: $.fn.tipsy.autoNS,
       gravity: "e",
       fade: true,
       html: true,
       title: function() {
           d = this.__data__, n = d.id, count = d.count;
           var hover = "<div class='hoverPopUp'>";
           hover += "<span class='courseTitle'>ID: " + n + "</span><br />";
           hover += "<span class='count'>Packets: " + count + "</span><br />";
           hover += "</div>";
           return hover;
       }
   });
  }



}


/* --------------------------------------------------------------------------
     Add new graph
  -------------------------------------------------------------------------*/

// Add new data table
var peopleTable = newDataTable("d3-table", ["source", "target", "count"])

// Create new graph class and override some methods
function TrafficAnalysisGraph () {
    this.link_distance = 60;
    this.node_charge = -10;
}

// Override method
TrafficAnalysisGraph.prototype = new D3Graph("d3-force-directed-graph");
TrafficAnalysisGraph.prototype.updateLinks = function () {
    updateTables();
    this.update();
}

// Add new graph
d3DirectedGraph = new TrafficAnalysisGraph();
d3DirectedGraph.init();
d3DirectedGraph.start();
graph = new D3GraphController(d3DirectedGraph);

// Add new WebSocket
ws = new WebSocketConn(graph, "ws://localhost:8080/websocket");


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

$.pnotify({
    title: 'Waiting for packets',
    text: 'Now you should send some JSON packets to the websocket. Have a look at the informational stuff tabs how to do that.',
    nonblock: true,
    hide: false,
    closer: false,
    sticker: false,
    type: 'info'
});
