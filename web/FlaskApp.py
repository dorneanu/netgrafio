#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: victor
# @Date:   2014-04-22 18:11:07
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

.. module:: FlaskApp
    :synopsis: Flask application handler

.. moduleauthor:: Victor Dorneanu <info AAET dornea DOT nu>

"""

# Import flask stuff
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

# Import modules
from web.core.views import mod as webCore
from web.mod_traceroute.views import mod as modTraceroute
from web.mod_nmap.views import mod as modNmap
from web.mod_netanalyzer.views import mod as modNetanalyzer

# Global variable
app = None


class FlaskApp():

    """ Use Flask for better routes and temlating handling """

    def __init__(self):
        """ Creates new flask application

        .. note::
            This also makes the registered blueprints available to the main application.
        """
        self.app = Flask(__name__, template_folder="core/templates", static_folder="core/static")
        app = self.app

        # register blueprints
        app.register_blueprint(webCore)
        app.register_blueprint(modTraceroute)
        app.register_blueprint(modNmap)
        app.register_blueprint(modNetanalyzer)
