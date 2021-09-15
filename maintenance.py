# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 16:06:26 2021

@author: spark
"""

import config_setup as config
import os

YOUR_DOMAIN = config.lookup('DOMAIN')
parts = YOUR_DOMAIN.split('.')
wsgi = ""

for each in parts:
    wsgi += each
    wsgi += "_"
wsgi += "wsgi.py"
w_path = "/var/www/"+wsgi

rest_of_file = ""

f = open(w_path, 'r')
lines = f.readlines()
for line in lines:
    if line == "from flask_app import app as application  # noqa":
        new_line = "from maintenance_site import app as application  # noqa"
        print("Site down for maintenance")
    elif line == "from maintenance_site import app as application  # noqa":
        new_line = "from flask_app import app as application  # noqa"
        print("Site live for entries")
    else:
        rest_of_file += line
f.close()

f = open(w_path, 'w')
f.write(rest_of_file+new_line)
f.close()
os.system("touch {}".format(w_path))
