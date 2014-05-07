#!/usr/bin/env python3
#-*- coding: utf-8 -*-
from flask import Blueprint, render_template, flash, g, redirect, url_for

mod = Blueprint("core", 
				__name__,  
				template_folder="templates",
				static_folder="static"
				)

@mod.route("/")
@mod.route("/index")
def home():
	return render_template("core/index.html")

@mod.route("/license")
def license():
	return render_template("core/license.html")

@mod.route("/authors")
def authors():
	return "Authors go here"