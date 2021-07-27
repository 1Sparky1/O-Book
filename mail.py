#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 16:28:02 2020

@author: neilpolwart
"""

# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python

import os
import base64
from sendgrid.helpers.mail import (
    Mail, Attachment, FileContent, FileName,
    FileType, Disposition, ContentId)
from sendgrid import SendGridAPIClient
from dotenv import load_dotenv
import config_setup as config

project_folder = os.path.expanduser('~/mysite')
load_dotenv(os.path.join(project_folder, 'sendgrid.env'))
print ('Hello')

def with_attachment(to="", subject="Missing Subject Line", content="<strong>HTML content missing</strong>",file_path ='',file_type='application/pdf'):
    '''for excel files set file_type to "application/vnd.ms-excel"
    '''
    path, filename = os.path.split(file_path)
    message = Mail(
        from_email=config.lookup('EMAIL'),
        to_emails=to,
        subject=subject,
        html_content=content)
    with open(file_path, 'rb') as f:
        data = f.read()
        f.close()
    encoded = base64.b64encode(data).decode()
    attachment = Attachment()
    attachment.file_content = FileContent(encoded)
    attachment.file_type = FileType(file_type)
    attachment.file_name = FileName(filename)
    attachment.disposition = Disposition('attachment')
    message.attachment = attachment
    try:
        sendgrid_client = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sendgrid_client.send(message)
        if response.status_code == 202:
            return True
        else:
            return False
    except Exception as e:
        print(e.message)

def simple_message(to="", subject="Missing Subject Line", content="<strong>HTML content missing</strong>"):
    message = Mail(
            from_email=config.lookup('EMAIL'),
            to_emails=to,
            subject=subject,
            html_content=content)
    print (os.environ.get('SENDGRID_API_KEY'))
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        if response.status_code == 202:
            return True
        else:
            return False
    except Exception as e:
        print(e.message)

