# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 18:47:44 2021

@author: spark
"""

import os
import time
import config_setup as config


def reload_site():
    YOUR_DOMAIN = config.lookup('DOMAIN')
    parts = YOUR_DOMAIN.split('.')
    wsgi = ""
    
    for each in parts:
        wsgi += each
        wsgi += "_"
    wsgi += "wsgi.py"
    w_path = "/var/www/"+wsgi
    
    t = time.time()
    
    os.utime(w_path, (t, t))