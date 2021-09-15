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

rest_of_file = ""

f = open("/var/www/"+wsgi, 'r')
for line in f:
    print(line)
    if line == "from flask_app import app as application  # noqa":
        new_line = "from maintainance_site import app as application  # noqa"
        print("Site down for maintainance")
    elif line == "from maintainance_site import app as application  # noqa":
        new_line = "from flask_app import app as application  # noqa"
        print("Site live for entries")
    else:
        rest_of_file += line
f.close()

f = open("/var/www/"+wsgi, 'w')
# f.write(rest_of_file+'\n'+new_line)
f.close()
