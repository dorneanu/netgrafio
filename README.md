# Introduction

I love computer science and new technologies to play with. Besides that I like to keep things simple and pay attention
to aspects that really mather. But I also like sharing my world and thoughts with people not involved in computer science.
In fact technology is not dehumanizing. It's what makes us human.


### Why? Don't you have better things to do?

The whole project was basically a wish I had during some **network analysis**:
I wanted to **visualize** my results in some fancier way. There were a lot of dependencies between several hosts
and I'm not good at reading raw packet data. And since **graphs** are an excellent data structure to represent
(computer) networks I've decided to begin my journey :smirk:

During some [D3](http://d3js.org/) experiments  I wanted to capture data from the command line and send it to my D3 application.
Of course I could have read the data from some CSV, JSON, whatever file but that wasn't "real-time" enough. So I had a

* data source
* D3 code applying some magic to the data

The *data source* in that case were some grep lines transformed to JSON data. In fact I was missing the
linking part between mentioned components.


### D3? Never heard of!

**D3** stands for Data-Driven Documents. Its basically a **JavaScript** library aimed to manipulate "documents based on data".
A neat side-effect of using JavaScript: You can use a **browser** to visualize your data. No need for extra GUI, clients whatever.
There are douzens of useful examples how to use D3, especially force layouts which are ment to implement graphs.

# Meet netgrafio!

**netgrafio** provides more or less tools and libraries to visualize your data regardless of its type.
I tried to make the libraries OOP-friendly but as you may know: JS and OOP is really a pain.
In fact I had to code a lot of JS (for the first time in my life as a coder:D).
Its not perfect and it might be buggy. But it works for me :v:

![netgrafio-first-page.png](http://dl.dornea.nu/img/netgrafio/netgrafio-first-page.png)

# Documentation

Make sure you'll have a look at the official documentation available at [http://netgrafio.readthedocs.org/](http://netgrafio.readthedocs.org/).


### Screenshots

![netgrafio-module-analysis.png](http://dl.dornea.nu/img/netgrafio/netgrafio-module-analysis.png)
The network analysis module.

![netgrafio-module-nmap.png](http://dl.dornea.nu/img/netgrafio/netgrafio-module-nmap.png)
Visualize nmap results.

### Basic idea

*netgrafio* listens for some data on a **TCP** socket and passes it through some **WebSocket** to all connected web clients.
The web clients have some JS code which will receive the incoming data and apply some magic to it.

> At the moment only JSON data is supported.

In order to transfer data from one socket to the another a (deadlock free) queue is being used (**producer and consumer pattern**).


### Run me

#### System requirements

In order to run netgrafio several requirements on your system have to be met. Basically you'll need:

* Python 3.x
* [virtualenv](http://www.virtualenv.org)
* [PIP](http://www.pip-installer.org/)


#### Clone project

Make sure you have installed these packages on your system. Afterwards you can clone this project:

```bash
$ git clone https://github.com/nullsecuritynet/netgrafio
$ cd netgrafio
```

#### Setup virtualenv

Now you'll need to setup a isolated python environment using *virtualenv*:

```bash
$ virtualenv env
Using base prefix '/usr'
New python executable in env/bin/python3
Also creating executable in env/bin/python
Installing setuptools, pip...done.
```

Make sure to activate the virtual environment:

```bash
$ source env/bin/activate
```


#### Install additional packages

Having set the virtualenv environment let's install some missing packages:

```bash
$ pip install -r env/requirements.pip
```


#### Fire up netgrafio

Now you're ready to start netgrafion and have some fun.

These are the basic parameters:

```bash
python netgrafio.py -h
usage: netgrafio.py [-h] [--tcp-port TCP_PORT] [--ws-port WS_PORT]
                    [--web-port WEB_PORT] [--host HOST]

netgrafio - visualize your network

optional arguments:
  -h, --help           show this help message and exit
  --tcp-port TCP_PORT  Specify TCP port to listen for JSON packets (default:
                       8081)
  --ws-port WS_PORT    Specify WebSocket port to send JSON data to (default:
                       8080)
  --web-port WEB_PORT  Specify web port to server web application (default:
                       5000)
  --host HOST          Specify host to bind socket on (default: 127.0.0.1)

```

If you start netgrafio without any arguments, then you'll have a

* *TCP-Socket* listening on port 8081
* *WebSocket* listening on port 8080
* *Web-Application* available at http://localhost:5000


```bash
$ python netgrafio.py
2014-04-24 16:18:12,984 - INFO - [WebSocketServer] - Starting WebSocket server on port 8080
2014-04-24 16:18:12,984 - INFO - [WebSocketServer] - Start collector server
2014-04-24 16:18:12,985 - INFO - [WebSocketServer] - Waiting for incoming data ...
2014-04-24 16:18:12,989 - INFO - [WebServer] - Listening on 5000
2014-04-24 16:18:12,989 - INFO - [TCPServer] - Listening on 8081
```

Now open your browser and navigate to [http://localhost:5000](http://localhost:5000)

