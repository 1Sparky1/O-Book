# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 16:06:26 2021

@author: spark
"""

import config_setup as config

YOUR_DOMAIN = config.lookup('DOMAIN')
parts = YOUR_DOMAIN.split('.')
wsgi = ""

for each in parts:
    wsgi += each
    wsgi += "_"
wsgi += "wsgi.py"

f = open("/var/www/"+wsgi, 'w')
for line in f:
    if line == "from flask_app import app as application  # noqa":
        line = "from maintainance_site import app as application  # noqa"
        print("Site down for maintainance")
    elif line == "from maintainance_site import app as application  # noqa":
        line = "from flask_app import app as application  # noqa"
        print("Site live for entries")
f.close()