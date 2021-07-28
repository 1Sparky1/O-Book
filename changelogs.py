# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 10:39:02 2021

@author: spark
"""
import os

project = os.path.split(__file__)[0]

def log_start(log):
    f = open(project+log, 'r')
    start = 0
    for line in f:
        if (line[0] == '#') or (line == '\n'):
            continue
        start = line
        break
    return start

def read_log(lines, start, stop):
    this_log = {}
    for line in range(start, stop):
        data = lines[line].split(':')[0].strip()
        if(data == 'Tags'):
            this_log[data] = (lines[line].split(':')[1].strip()).split(',')
            for tag in this_log['Tags']:
                tag.strip()
        elif(data == 'Changes'):
            changes = []
            for change in range(line+1, stop):
                if lines[change] == '\n':
                    break
                changes.append(lines[change].strip().strip(' -'))
            this_log[data] = changes
        elif(len(lines[line].split(':')) > 1):
            this_log[data] = lines[line].split(':')[1].strip()
    return this_log

def read_stachelog():
    prev_logs = {}
    f = open(project+'/changelogs/changelog.stache', 'r')
    lines = f.readlines()
    ln_no = 0
    starts = []
    for line in lines:
        ln_no += 1
        if line[0] == '@':
            starts.append(ln_no)
    for log in range(0, len(starts)):
        if log == (len(starts)-1):
            continue
        this_start = starts[log]-1
        next_start = starts[log+1]
        this_log = read_log(lines, this_start, next_start)
        prev_logs[lines[this_start].strip()] = this_log
    f.close()
    return prev_logs

def check_stached_log(log):
    stache = read_stachelog()
    for changelog in stache:
        if stache[changelog] == log:
            return True
    return False

def get_new_log_no():
    stache = open(project+'/changelogs/changelog.stache', 'r')
    contents = stache.read()
    current_no = int(contents[-2:])
    new_no = str(current_no + 1)
    while len(new_no) < 3:
        new_no = '0' + new_no
    return new_no

def add_log_to_stache(file, log):
    new_no = get_new_log_no()
    stache = open(project+'/changelogs/changelog.stache', 'a')
    stache.write('\n')
    for data in log:
        if data == 'Tags':
            stache.write('Tags: {}\n'.format(tags_to_string(log[data])))
        elif data == 'Changes':
            stache.write('Changes:\n')
            for change in log[data]:
                stache.write('\t- {}\n'.format(change))
        else:
            stache.write('{}: {}\n'.format(data, log[data]))
    stache.write('\n@{}\n'.format(new_no))
    stache.close()
    os.remove(project+'/changelogs/{}'.format(file))

def get_new_logs():
    new = {}
    files = os.listdir(project+'/changelogs')
    for file in files:
        if (file[0:3] == 'cl_') and (file[-4:] == '.txt'):
            l = open(project+'/changelogs/{}'.format(file), 'r')
            lines = l.readlines()
            start = 0
            for line in lines:
                if line[0] == 'A':
                    start = lines.index(line)
                    break
            log = read_log(lines, start, len(lines))
            if not check_stached_log(log):
                new[file] = log
    return new

def tags_to_string(tags):
    string = ''
    for tag in tags:
        string += tag
        if tags.index(tag) < len(tags)-1:
            string += ', '
    return string

def changes_to_string(changes):
    string = ''
    no = 0
    for change in changes:
        no += 1
        string += '{}. '.format(no) + change + '\n'
    return string

def show_new_logs(show):
    new = get_new_logs()
    for file in new:
        log = new[file]
        tags = tags_to_string(log['Tags'])
        if 'CODEBASE' in tags.upper():
            add_log_to_stache(file, log)
            continue
        changes = changes_to_string(log['Changes'])
        if show:
            print('''{date} : {author} made changes:
Change Type(s): {tags}
\n
{changes}'''.format(date=log['Date'],
                                  author=log['Author'],
                                  tags=tags.upper(),
                                  changes=changes))
        add_log_to_stache(file, log)
