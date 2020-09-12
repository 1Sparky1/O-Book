# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 13:27:57 2020

@author: spark
"""

import openpyxl as xl
from datetime import datetime
from filelock import FileLock


def load_sheets(file):
    wb = xl.load_workbook(file)
    event = wb['EventDetails']
    fees = wb['EntryFees']
    courses = wb['Courses']
    starts = wb['StartList']
    return wb, event, fees, courses, starts

def get_members(file):
    wb = xl.load_workbook(file)
    members = wb['Members']
    members_dict = {}
    for row in members.iter_rows(min_row=2, max_col=2, values_only=True):
        members_dict[row[0]]=row[1]
    return members_dict

def strip_starts(start_times):
    ''' Returns a list of available start times '''
    ls = []
    for each in start_times.keys():
        if start_times[each] == None:
            ls.append(each)
    return ls

def read_ageclass(fees):
    ''' Reads the age classes from the Workbook and assigns their prices '''
    age_class = {}
    for row in fees.iter_rows(min_row=1, max_col=2, values_only=True):
        age_class[row[0]] = row[1]
    return age_class

def read_course(courses):
    ''' Reads the courses from the Workbook and assigns their descriptions '''
    course = {}
    for row in courses.iter_rows(min_row=1, max_col=2, values_only=True):
        course[row[0]] = row[1]
    return course

def get_event_details(event):
    ''' Reads the event details from the Workbook and returns a dict '''
    details = {}

    details["hire_available"] = False
    details["members_only"] = False

    details["name"] = str(event['B1'].value)
    details["url"] = str(event['B2'].value)
    details["date"] = event['B3'].value
    details["date_pretty"] = (event['B3'].value).strftime('%A %-d %B %Y')
    details["organiser"] = str(event ['B4'].value)
    details["org_email"] = str(event ['B5'].value)
    details["closing"] = event['B6'].value
    details["closing_pretty"] = (event['B6'].value).strftime('%-d %b %Y %-I:%M%p')
    if str(event ['B7'].value).upper()=="YES": details["hire_available"]=True
    if str(event ['B8'].value).upper()=="YES": details["members_only"]=True
    return details

def event_closed(event):
    details = get_event_details(event)
    if details["closing"]<datetime.now():
        return True
    else:
        return False

def hire_available(event):
    details = get_event_details(event)
    return details["hire_available"]

def members_only(event):
    details = get_event_details(event)
    return details["members_only"]

def get_event_summary(event):
    ''' gets the event details then creates a HTML summary, and returns it'''
    details = get_event_details(event)
    return """  <strong>{name}</strong> on {date_pretty} <br>
                being organised by {organiser}<br>
                CLOSING DATE FOR ENTRIES:<br> {closing_pretty}<br>
                see <A Href={url}>{url}</A> for details<br>
            """.format(**details)

    course = {}
    for row in courses.iter_rows(min_row=1, max_col=2, values_only=True):
        course[row[0]] = row[1]
    return course

def read_time(starts):
    ''' Reads the start times from the Workbook and assigns anyone currently booked for that time '''
    time = {}
    for row in starts.iter_rows(min_row=2, max_col=2, values_only=True):
        if row[0]:
            temp = row[0].strftime("%H:%M")
            time[temp] = row[1]
    return time

def update_sheet(starts, time, name, course, age_class, fee, dibber, phone, email):
    ''' Writes the information to the Start Sheet '''
    i=2
    for row in starts.iter_rows(min_row=2, max_col=8, values_only=True):
        if row[1]: #only consider rows with a name in the entry list, avoids an error as None.Upper() invalid
            if (row[1].upper() == name.upper() and row[3]== age_class) or (row[5] == dibber and dibber!="HIRE"):
                return False,'''This person appears to already have an entry, please <a href="javascript:history.back()">go back</a>
                        and enter a new person; make sure you are using the correct SI dibber number; if you are sure this is not a duplicate add "2" after your name, or contact the organiser.
                        If you have finished entering people <a href="/orienteering/invoice">go to your</a> invoice to finish.'''
    for row in starts.iter_rows(min_row=2, max_col=8, values_only=True):
        if row[0] and row[1] and row[0].strftime("%H:%M") == time:
            return False,'Whilst you were completing the form this timeslot has been reserved by another participant, please <a href="javascript:history.back()">go back</a> and pick another.'
        elif row[0] and row[0].strftime("%H:%M") == time :
            starts['B{}'.format(i)] = name
            starts['C{}'.format(i)] = course
            starts['D{}'.format(i)] = age_class
            starts['E{}'.format(i)] = fee
            starts['F{}'.format(i)] = dibber
            starts['G{}'.format(i)] = phone
            starts['H{}'.format(i)] = email
            return True,"Time {} successfully reserved for {}".format(time,name)
        i +=1


def write_wbook(wb,filename):
    with FileLock(filename+".lock"):
        print("Lock acquired.")
        wb.save(filename)

'''tests

wb, event, fees, courses, starts = load_sheets('data.xlsx')
time = '11:24'
name = 'Bla Bla Boom'
age_class = 'X12'
course = 'zooming'
fee = '£12'
dibber = 'boo'
phone = '123455'
email = 'wa@wa.com'

print(update_sheet(starts, time, name, course, age_class, fee, dibber, phone, email))
print(write_wbook(wb,'data.xlsx'))

'''

def get_entries(starts):
    entries=[]
    for row in starts.iter_rows(min_row=2, max_col=8, values_only=True):
        if row[1]:
            dct = {}
            dct['Name']=row[1]
            dct['Start Time']=row[0].strftime("%H:%M")
            dct['Course']=row[2]
            dct['Age Class']=row[3]
            dct['Dibber No.']=row[5]
            entries.append(dct)
    return entries