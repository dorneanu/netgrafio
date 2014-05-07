#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: victor
# @Date:   2014-04-22
# @Last Modified by:   victor
# @Last Modified time: 2014-05-06
# @Copyright:
#
#    This file is part of the netgrafio project.
#
#
#    Copyright (c) 2014 Victor Dorneanu <info AAET dornea DOT nu>
#
#    Permission is hereby granted, free of charge, to any person obtaining a copy
#    of this software and associated documentation files (the "Software"), to deal
#    in the Software without restriction, including without limitation the rights
#    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#    copies of the Software, and to permit persons to whom the Software is
#    furnished to do so, subject to the following conditions:
#
#    The above copyright notice and this permission notice shall be included in all
#    copies or substantial portions of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE boru
#    WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#    SOFTWARE.
#
#    The MIT License (MIT)


"""

.. module:: WebSocket
    :synopsis: A simple HTML5 WebSocket handler

.. moduleauthor:: Victor Dorneanu <info AAET dornea DOT nu>

"""


import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import logging
import json

from threading import Thread
from queue import Queue

# Handle WebSocket clients
clients = []


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    """ Handle default WebSocket connections """

    # Logging settings
    logger = logging.getLogger("WebSocketHandler")
    logger.setLevel(logging.INFO)

    def open(self):
        """ New connection has been established """
        clients.append(self)
        self.logger.info("New connection")

    def on_message(self, message):
        """ Data income event callback """
        self.write_message(u"%s" % message)

    def on_close(self):
        """ Connection was closed """
        clients.remove(self)
        self.logger.info("Connection removed")


class IndexPageHandler(tornado.web.RequestHandler):

    """ Default index page handler. Not implemented yet. """

    def get(self):
        pass


class Application(tornado.web.Application):

    """ Tornado application """

    def __init__(self):
        # Add here several handlers
        handlers = [
            (r'/', IndexPageHandler),
            (r'/websocket', WebSocketHandler)
        ]

        # Application settings
        settings = {
            'template_path': 'templates'
        }

        # Call parents constructor
        tornado.web.Application.__init__(self, handlers, **settings)


class WebSocketServer():

    """ Create tornado HTTP server serving our application

    .. note::
        Uses tornado as backend.
    """

    def __init__(self, host, port, in_queue=Queue()):
        """ Constructor for the WebSocketServer class

        Args:
            host(str): Hostname
            port(int): Port number to listen on
            in_queue(Queue): Thread-safe working queue

        """

        # Settings
        self.application = Application()
        self.server = tornado.httpserver.HTTPServer(self.application)
        self.host = host
        self.port = port
        self.in_queue = in_queue

        # Listen to ..
        self.server.listen(self.port, self.host)

        # Logging settings
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger("WebSocketServer")
        self.logger.setLevel(logging.INFO)

    def start_server(self):
        """ Starts the HTTP server
        """
        self.logger.info("Starting WebSocket server on port %d" % self.port)
        http_server = Thread(target=tornado.ioloop.IOLoop.instance().start)
        http_server.start()

    def start_collector(self):
        """ Starts collecting packages
        """
        self.logger.info("Start collector server")
        collector_server = Thread(target=self.collect_data)
        collector_server.start()

    def collector_process_data(self, data):
        """ Process incoming data and send it to all available clients

        Args:
            data: Received data

        """
        for c in clients:
            c.on_message(json.dumps(data))

    def collect_data(self):
        """ Wait for data  in individual thread
        """
        self.logger.info("Waiting for incoming data ...")
        while True:
            item = self.in_queue.get()
            self.logger.info("Received data!")
            self.collector_process_data(item)

    def start(self):
        """ Starts the server

        .. note::
            The server will listen for incoming JSON packets and pass them
            to all clients connected to the WebSocket.
        """
        # Start HTTP server
        self.start_server()

        # Start data collector
        self.start_collector()
