#!/usr/bin/env python

from distutils.core import setup
import py2exe

setup(name="CogDevApp",
      version="1.0.1",
      description="Cog Engine Project - Development Application",
      author="Steven M. Castellotti",
      author_email="SteveC@innocent.com",
      url="http://cogengine.sourceforge.net/",
	scripts=["CogDevApp.py"],
     )