# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 10:11:03 2021

@author: spark
"""

def config():
    configs = {}
    f = open('config.txt', 'r')
    for line in f:
        if (line[0] == '#') or (line == '\n'):
            continue
        data = line.split('#')[0]
        configs[data.split('=')[0].strip()] = data.split('=')[1].strip()
    f.close()
    return configs
    
def lookup(search):
    configs = config()
    if search in configs:
        return configs[search]
    else:
        return
    