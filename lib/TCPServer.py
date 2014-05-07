#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: victor
# @Date:   2014-04-11
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
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#    SOFTWARE.
#
#    The MIT License (MIT)


"""

.. module:: TCPServer
    :synopsis: TCP socket listening for incoming JSON packets

.. moduleauthor:: Victor Dorneanu <info AAET dornea DOT nu>

"""

import socketserver
import json
import logging

from queue import Queue
from threading import Thread


class TCPServer(socketserver.ThreadingTCPServer):

    """ Custom TCP server """

    def __init__(self, server_address, RequestHandlerClass, in_queue=Queue()):
        """ Create new TCP socket

        Args:
            server_address: Combination of host and port
            RequestHandlerClass: Handler for incoming connections
            in_queue(Queue): Thread-safe working queue

        """
        # Set queues
        self.in_queue = in_queue

        # Call parents constructor
        super(TCPServer, self).__init__(server_address, RequestHandlerClass)

        # Avoid "address already in use" error
        socketserver.TCPServer.allow_reuse_address = True

        # Logging settings
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger("TCPServer")
        self.logger.setLevel(logging.INFO)


class TCPServerHandler(socketserver.BaseRequestHandler):

    """ Waiting for incoming (JSON) data """

    def handle(self):
        """ Wait for incoming JSON packets and pre-process them
        """
        try:
            # Wait for data
            data = json.loads(self.request.recv(1024).decode('UTF-8').strip())

            # Process data
            self.process_data(data)

        except Exception as e:
            print("Exception wile receiving message: ", e)
            self.request.sendall(
                bytes(json.dumps({'return': 'error'}), 'UTF-8'))

    def process_data(self, data):
        """ Process received data

        Args:
            data(bytes): Incoming data
        """
        self.server.in_queue.put(data)
        self.server.in_queue.task_done()
        self.server.logger.info("Added JSON to IN queue")


class JSONServer():

    """ TCP Server waiting for JSON packets """

    def __init__(self, host, port, in_queue=Queue()):
        """ Create new TCP server listening for incoming JSON packets

        Args:
            host(str): Hostname
            port(int): Port number to listen on
            in_queue(Queue): Thread-safe working queue

        """
        # Global settings
        self.host = host
        self.port = port

        # Init super class
        self.server = TCPServer(
            (self.host, self.port), TCPServerHandler, in_queue)

    def start(self):
        """ Starts JSON server
        """
        self.server.logger.info("Listening on %s" % self.port)
        server_thread = Thread(target=self.server.serve_forever)
        server_thread.start()

# EOF
