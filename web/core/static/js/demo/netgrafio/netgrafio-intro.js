// Create new graph class and override some methods
function TracerouteGraph () {
    this.link_distance = 150;
    this.node_charge = -20;
}

// Override methods
TracerouteGraph.prototype = new D3Graph("d3-explain-graph");

// Add new graph
d3DirectedGraph = new TracerouteGraph();
force = d3DirectedGraph.getForce();
d3DirectedGraph.init();

// Tell graph it should behave like a tree
d3DirectedGraph.setTree(true);
d3DirectedGraph.setSelf(d3DirectedGraph);

// Create controller
graph = new D3GraphController(d3DirectedGraph);


// Add some dummy nodes and links
node_netgrafio = {"id":"netgrafio", "class": "netgrafio", "name": "netgrafio" }
node_websocket = {"id":"websocket", "class": "websocket", "name": "Web Socket" }
node_tcpsocket = {"id":"tcpsocket", "class": "tcpsocket", "name": "TCP Socket" }
node_webapp	   = {"id":"webapp", "class": "webapp", "name": "netgrafio web application" }
node_data	   = {"id":"data", "class": "data", "name":"Data source"}

graph.addNode(node_netgrafio)
graph.addNode(node_websocket)
graph.addNode(node_tcpsocket)
graph.addNode(node_webapp)
graph.addNode(node_data)

// Create links

graph.addLink({"source": "netgrafio", "target": "websocket"});

graph.addLink({"source": "netgrafio", "target": "tcpsocket"});
graph.addLink({"source": "websocket", "target": "netgrafio"});
graph.addLink({"source": "tcpsocket", "target": "netgrafio"});

graph.addLink({"source": "webapp",  "target": "websocket"})
graph.addLink({"source": "websocket", "target": "webapp"})

graph.addLink({"source": "data", "target": "tcpsocket"})
graph.addLink({"source": "tcpsocket", "target":"data"})

// Add tipsy tooltips
$(".node.netgrafio").tipsy({  
       //gravity: $.fn.tipsy.autoNS,
       gravity: "e",
       fade: true, 
       html: true, 
       title: function() {
           var hover = "<div class='hoverPopUp'>";
           hover += "<p>This is the main application. Once started it will create several sockets (WebSocket, TCPSocket) and fire up the web application. </p>";
           hover += "</div>";
           return hover; 
       }
 });

$(".node.tcpsocket").tipsy({  
       //gravity: $.fn.tipsy.autoNS,
       gravity: "e",
       fade: true, 
       html: true, 
       title: function() {
           var hover = "<div class='hoverPopUp'>";
           hover += "<p>This socket will listen for incoming packets (JSON) and forward them to the main application.</p>";
           hover += "</div>";
           return hover; 
       }
 });

$(".node.websocket").tipsy({  
       //gravity: $.fn.tipsy.autoNS,
       gravity: "e",
       fade: true, 
       html: true, 
       title: function() {
           var hover = "<div class='hoverPopUp'>";
           hover += "<p>The web socket is mainly used by the web application itself in order to communicate with <b>netgrafio</b>. Once connected to it, it will wait for incoming packets and forward them to the web application.</p>";
           hover += "</div>";
           return hover; 
       }
 });

$(".node.data").tipsy({  
       //gravity: $.fn.tipsy.autoNS,
       gravity: "e",
       fade: true, 
       html: true, 
       title: function() {
           var hover = "<div class='hoverPopUp'>";
           hover += "<p>The data source (command line, script whatever) will send packets to the <b>TCP socket</b>.</p>";
           hover += "</div>";
           return hover; 
       }
 });

$(".node.webapp").tipsy({  
       //gravity: $.fn.tipsy.autoNS,
       gravity: "e",
       fade: true, 
       html: true, 
       title: function() {
           var hover = "<div class='hoverPopUp'>";
           hover += "<p>The web application will process the incoming packets (through the <b>web socket</b>) and visualize them in a previously defined way.</p>";
           hover += "</div>";
           return hover; 
       }
 });