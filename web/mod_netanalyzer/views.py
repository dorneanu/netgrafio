#!/usr/bin/env python3
#-*- coding: utf-8 -*-
from flask import Blueprint, render_template, flash, g, redirect, url_for

mod = Blueprint("mod_netanalyzer", 
				__name__, 
				url_prefix="/module/netanalyzer", 
				template_folder="templates",
				static_folder="static"
				)

@mod.route("/")
def home():
	return render_template("mod_netanalyzer/index.html")