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
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#    SOFTWARE.
#
#    The MIT License (MIT)


"""

.. module:: WebServer
    :synopsis: Simple web server to host the Flask application

.. moduleauthor:: Victor Dorneanu <info AAET dornea DOT nu>

"""

import logging
import os
import tornado

from threading import Thread
from tornado.wsgi import WSGIContainer
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, FallbackHandler

from web.FlaskApp import FlaskApp


class HelloHandler(RequestHandler):

    """ Dummy request handler """

    def get(self):
        self.write('Hello from tornado')


class Application(tornado.web.Application):

    """ Create new Flask application using Tornado's WSGIContainer """

    def __init__(self):
        flask_app = FlaskApp()
        app_container = WSGIContainer(flask_app.app)

        # Add here several handlers
        handlers = [
            (r'/hello-tornado', HelloHandler),
            ('.*', FallbackHandler, dict(fallback=app_container))
        ]

        # Application settings
        settings = {
            'template_path': 'templates'
        }

        # Call parents constructor
        tornado.web.Application.__init__(self, handlers, **settings)


class HTTPServer():

    """ Simple http server using Tornado """

    def __init__(self, host, port):
        """ Create HTTP server

        Args:
            host(str): Hostname
            port(int): Port number to listen on
        """
        self.host = host
        self.port = port
        self.tornado_app = Application()
        self.server = tornado.httpserver.HTTPServer(self.tornado_app)

        # Listen to ...
        self.server.listen(self.port, self.host)

        # Logging settings
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger("WebServer")
        self.logger.setLevel(logging.INFO)

    def start_server(self):
        """ Server will start a new thread and listen for incoming connections
        """
        http_server = Thread(target=IOLoop.instance().start)
        http_server.start()


class WebServer():

    """ Web server for main application """

    def __init__(self, host, port):
        """ Create web server

        Args:
            host(str): Hostname
            port(int): Port number to listen on
        """
        self.host = host
        self.port = port

        # Init http server
        self.server = HTTPServer(self.host, self.port)

    def start(self):
        """ Starts the web server in own thread
        """
        self.server.logger.info("Listening on %s" % self.port)
        server_thread = Thread(target=self.server.start_server)
        server_thread.start()

# EOF