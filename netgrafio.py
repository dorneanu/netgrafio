#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: victor
# @Date:   2014-04-22
# @Last Modified by:   victor
# @Last Modified time: 2014-04-23
# @Copyright:
#
#    This file is part of the netgrafio project.
#
#
#    Copyright (c) 2014 Victor Dorneanu <info AAET dornea DOT nu >
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

import sys
import argparse
import logging
from queue import Queue

# Local packages
from lib.TCPServer import JSONServer
from lib.WebSocketServer import WebSocketServer
from lib.WebServer import WebServer


def parse_args(params):
    """ Parse cmd line arguments """
    parser = argparse.ArgumentParser(
        description="netgrafio - visualize your network",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # Set parameters
    parser.add_argument("--tcp-port", action="store", type=int,
                        help="Specify TCP port to listen for JSON packets", default=8081)
    parser.add_argument("--ws-port", action="store", type=int,
                        help="Specify WebSocket port to send JSON data to", default=8080)
    parser.add_argument("--web-port", action="store", type=str,
                        help="Specify web port to server web application", default=5000)
    parser.add_argument("--host", action="store", default="127.0.0.1",
                        help="Specify host to bind socket on")
    args = parser.parse_args(params)

    return args


def main(params):
    # Global logging settings
    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s - %(levelname)s - [%(name)s] - %(message)s")

    # Init in queue (producer and consumer pattern)
    in_queue = Queue()

    # Set default host
    host = params.host

    # Start WebSocket server
    websocket_server = WebSocketServer(host, int(params.ws_port), in_queue)
    websocket_server.start()

    # Start Web Server
    web_server = WebServer(host, int(params.web_port))
    web_server.start()

    # Start JSON server
    tcp_server = JSONServer(host, int(params.tcp_port), in_queue)
    tcp_server.start()


if __name__ == "__main__":
    main(parse_args(sys.argv[1:]))

# EOF