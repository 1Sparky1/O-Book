# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 11:17:29 2021

@author: spark
"""


import os
import config_setup as config
import changelogs

project = os.path.split(__file__)[0]
skeleton = [project+'/events/archive',
            project+'/events/pending',
            project+'/private']

modules = ['sendgrid', 'python-dotenv', 'openpyxl==2.6.4']

html = '''<html>
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
                <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
                <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk" crossorigin="anonymous">
                <title>Events Privacy Policy</title>
            </head>
            <body>
                <div class="row mx-md-n5">
                    <div class="col px-md-5"><div class="p-3 border bg-light"><p></p></div></div>
                </div>
                <div class="container">
                    <br>
                    <H5>Your Personal Data</H5>
                    <br>
                    <p>{name} (“the Club”) is the controller of personal data which is collected on this website.
                    The club’s privacy notice can be viewed here <a href='{notice}'>{notice}</a>
                    or downloaded here: <a href='{notice}.pdf'>{notice}.pdf</a>
                    </p>
                    <p>This website for event registration has been created in response to the COVID-19 outbreak and the data we collect about you may be used to manage our risk mitigation in line with advice from our sport’s governing bodies, and government departments.
                    </p>
                    <p>
                    The information we collect or hold about you on this website may include (depending on the requirements of the event organiser):
                    <ul>
                    <li>Your name and club affiliation – this is information, which is already publicly available,
                    for example via the British Orienteering ranking list.  We also ask for your Year of Birth and Sex in order to automatically determine your age class which is shown in all Orienteering results lists, and so publically available.</li>
                    <li>Which events and courses you have entered.  This is information which would
                    appear in any public record of results, either on the club or British Orienteering website.</li>
                    <li>Your email address.  This information is requested to ensure that we are able
                    to contact you about changes to the event such as cancellation, COVID-19 precautions
                    or to help health officials contact you in the event of a communicable disease case being associated with the event.</li>
                    <li>Your phone number.  This information is requested to help health officials
                    contact you in the event of a communicable disease case being associated with the event.
                    We may also use this information to attempt to contact you if you fail to download at the end of an event – to ensure your safety.</li>
                    <li>Your SI dibber number.  This information is required to support timing of the event, the information is generally in the public domain.</li>
                    </ul></p>
                    <p>Your personal data is required in order to manage the event.
                    Your contact details may be shared with our governing bodies,
                    our insurers or health officials where we either have a legal obligation to share
                    this information or where in our opinion it is in the legitimate interests of the
                    Club or other participants to share your information.
                    If we do have to share your information, we will remind the recipient that it is
                    Personal Data and that they have legal obligations to safeguard it.</p>

                    <p>The information will only be available to:
                        (1) The event organiser (listed in the event details section);
                        (2) Club officials or volunteers trusted with organising the event, managing the website or following up on any incident.
                    The data is secured with username and password and other than the details which would appear on any result sheet is not publicly accessible.</p>

                    <p>The membership secretary may use the data you have provided to verify the accuracy of membership records,
                    but will contact you if they believe the records need amended.  You should not rely on this method to update the Club,
                    or governing bodies with changes to your details.</p>

                    <p>Personal data entered on these pages will NOT be used to market or promote our services to you.
                    If you have provided details elsewhere, they may be used to update you about club events.  We will not sell this information.</p>

                    <p>The data on these servers is held within the European Union.
                    The servers are hosted by PythonAnywhere.com – we do not share any of your personal information with PythonAnywhere.</p>
                    <hr></hr>
                    <h5>COOKIES</h5>

                    <p>This site uses “sessions” to securely store information about your visit to the website, and manage progression between pages.  The information stored in the sessions is encrypted and accessible only to this app.  We do not track where you came to this page, where you go, or use any cookies that are part of advertising or analytics services.
                    </p>




                    <nav class="navbar fixed-top navbar-expand-lg navbar-dark bg-dark">
                        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarToggler" aria-controls="navbarToggler" aria-expanded="false" aria-label="Toggle navigation">
                            <span class="navbar-toggler-icon"></span>
                        </button>
                        <div class="collapse navbar-collapse" id="navbarToggler">
                            <a class="navbar-brand" href="{site}">{club} Website</a>
                            <ul class="navbar-nav mr-auto mt-2 mt-lg-0">
                                <li class="nav-item active">
                                    <a class="nav-link" href="/">Enter event ></a>
                                </li>
                                <li class="nav-item active">
                                    <a class="nav-link" href="/orienteering/view-entries?type=FreedomVille 20th Sept 2020 (Members only)">Entry list</a>
                                </li>
                                <li class="nav-item">
                                    <a class="nav-link" href="/Entries_Privacy_Notice.html">Privacy<span class="sr-only">(current)</span</a>
                                </li>
                            </ul>
                        </div>
                    </nav>
                </body>
            </html>'''.format(name=config.lookup('NAME'),
                            notice=config.lookup('PRIVACY_NOTICE'),
                            site=config.lookup('CLUB_SITE'),
                            club=config.lookup('CLUB'))

for path in skeleton:
    if os.path.exists(path):
        print('Directory {} already exists. Skipping...'.format(path))
        continue
    try:
        os.mkdir(path)
    except OSError:
        print('Failed to create new directory {}. Please create directory manually'.format(path))
    else:
        print('New directory {} successfully created.'.format(path))
        

if os.path.isfile(project+'/Entries_Privacy_Notice.html'):
    print('Privacy Notice already exists, skipping...')
else:
    try:
        p = open('Entries_Privacy_Notice.html', 'w')
        p.write(html)
        p.close()
    except:
        print('WARNING! Failed to create Privacy Notice from config file.')
    else:
        print('Privacy Notice successfully created from config file.')
        
if os.path.isfile(project+'/sendgrid.env'):
    print('Sendgrid Environment already exists. Skipping...')
else:
    try:
        sg = open('sendgrid.env', 'w')
        sg.write("export SENDGRID_API_KEY=''")
        sg.close()
    except:
        print('Failed to create SendGrid Environment. Please create file manually.')
    else:
        print('SendGrid Environment successfully created.')
        
if os.path.isfile(project+'/stripe.env'):
    print('Stripe Environment already exists. Skipping...')
else:
    try:
        s = open('stripe.env', 'w')
        s.write("export STRIPE_API_KEY=''")
        s.close()
    except:
        print('Failed to create Stripe Environment. Please create file manually.')
    else:
        print('Stripe Environment successfully created.')
        
if os.path.isfile(project+'/changelogs/changelog.stache'):
    print('Changelog Stache already exists. Skipping...')
else:
    try:
        cs = open('changelogs/changelog.stache', 'w')
        cs.write('''# Stache Log #\n# Contains all the previously read changelogs\n\n@000''')
        cs.close()
        changelogs.show_new_logs(False)
    except:
        print('Failed to create Changelog Stache. Please create file manually.')
    else:
        print('Changelog Stache successfully created.')
        

for module in modules:
    try:
        os.system('pip3.9 install --user {}'.format(module))
    except OSError:
        print('Failed to install module {}.'.format(module))
    else:
        print('Module {} successfully installed.'.format(module))
    
