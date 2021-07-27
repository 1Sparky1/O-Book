
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request, session, redirect,  render_template, jsonify
import traceback
import htmltemplates
from backend import *
import glob
import secrets
import collections
import mail
import json
import os
from datetime import datetime
import stripe
from dotenv import load_dotenv
import config_setup as config

# allows stripe key to be loaded from .env which is in git ignore.
project_folder = os.path.expanduser('~/mysite/O-Book')
load_dotenv(os.path.join(project_folder, 'stripe.env'))
stripe.api_key = os.environ.get('STRIPE_API_KEY')

SITEPATH = project_folder+"/"
EVENTSPATH = SITEPATH+"events/"
MEMBERFILE = SITEPATH + "private/members.xlsx"
YOUR_DOMAIN = config.lookup('DOMAIN')



wb, start, start_times, age_classes, courses, starts = None, None, None, None, None, None

app = Flask(__name__,static_folder=".",
            static_url_path="", template_folder=".")
app.config["DEBUG"] = False
app.config["SECRET_KEY"] = secrets.token_urlsafe(256)

help_title = "Why Do We Need This?"
help_info = "We may need these details to contact you if the event is cancelled.  We MAY be required to share this information with Health Protection Scotland if someone at the event develops symptoms of a communicable disease."

club_list = ['FVO','AROS','AUOC','AYROC','BASOC','CLYDE','ECKO','ESOC','EUOC',
            'GRAMP','INT','INVOC','KFO','MAROC','Masterplan','MOR','RR',
            'SOLWAY','STAG','STUOC','TAY','TINTO','USOC',
            'Other'
            ]

def checkout_required(session):
    script = ''
    if 'running_total' in session and 'checkout' in session:
        if not session['checkout']:
            script = '<script src="{}/checkout_warning.js"></script>'.format(YOUR_DOMAIN)
            pass
    return script


''' #uncomment to reinstate
@app.route('/', methods=["GET", "POST"])
def home():
    script = ""
    return htmltemplates.error(title="Registration disabled",
                                     heading='Entries disabled!', footer="",
                                     message="""Registration currently disabled whilst we review the advice from SOA & SportScotland following the
                                     First Minister's announcement on 4th January 2020.  If you have already enterred we will be in touch about events
                                     which are postponed and refunds/credit for future entries.""")

'''
#comment to lock site
@app.route('/', methods=["GET", "POST"])
def home():
    script = checkout_required(session)
    event_options = [os.path.splitext(os.path.basename(file))[0] for file in glob.glob(EVENTSPATH+'*.xlsx')]
    app.logger.info(event_options)
    return (htmltemplates.get_dropdown(title='Orienteering Signup - Home',
                                        heading='Local Orienteering Events - Select the event',
                                        footer=htmltemplates.navbar,
                                        info="Select the event you wish to register for.  The current list of entrants can be accessed from the menu at top of page",
                                        dd_list=event_options, form_action="/orienteering/signup",
                                        script=script)
                                        )


@app.route('/orienteering/signup', methods=["GET", "POST"])
def signup():
    script = checkout_required(session)
    if 'running_total' not in session:
        session['running_total']=0
    if 'all_entries' not in session:
        session['all_entries']=[]

    app.logger.info('signup page opened')

    if request.method == "GET":
        try:
            session['file_name'] = request.args.get('type')
            session['file']=EVENTSPATH+session['file_name']+'.xlsx'
        except:
            return redirect('/orienteering', code=302)
        session['start_times']=None
        session['age_classes']=None
        session['courses']=None
        session['starts'] =None
        wb, event, fees, courses, start = load_sheets(session['file'])
        app.logger.info('Page running as GET; File: {} opened'.format(session['file']))
        session['start_times'] = read_time(start)
        session['age_classes'] = read_ageclass(fees,event)
        session['age_classes_mod'] = session['age_classes'].copy()
        for each in session['age_classes_mod']:
            session['age_classes_mod'][each] = '£'+str(session['age_classes_mod'][each])
        session['courses'] = read_course(event, courses)
        session['starts'] = strip_starts(session['start_times'])
        event_summary = get_event_summary(event)
        session['event_summary']=event_summary

        if hire_available(event):
            dibber_section = htmltemplates.tick_to_close(label="I need to hire an SI card/dibber (if you don't know what this is, tick the box)",
                                        action = 'data-toggle="collapse" data-target="#collapsedib" onclick="togglerqd()"',
                                        id='dib',
                                        content=htmltemplates.input_box('Dibber', 'Dibber Number', valid='number', extra_params='min="1000" max="9999999" required'))
        else:
            dibber_section = htmltemplates.input_box('Dibber', 'Dibber Number', valid='number', required='True', extra_params='min="1000" max="9999999"')

        if members_only(event):
            name_section = htmltemplates.select_box_ls("Name", sorted(get_members(MEMBERFILE).keys()), required='True')
        else:
            name_section = htmltemplates.input_box('Name', 'Full Name of Participant', valid='text', required='True')

        maps_left, maps_message=get_remaining_maps(courses, session)

        if check_covid_warning(event) and session['running_total'] == 0:
            modal = htmltemplates.covid_popup()
        else:
            modal = ""

        if event_closed(event) or not maps_left:
            app.logger.info('Event closing date passed.')
            return htmltemplates.warning(title='Orienteering Signup - Enter', script=script, heading='This event is now closed', message=event_summary, footer=htmltemplates.navbar.format(session['file_name']))
        
        elif late_entries(event):
            title = 'Limited maps remaining'
            heading = 'Limited Maps Remaining - Enter your details <p><small>Entry fees include a late entry premium</small></p><p>Every attendee must be registerred - if entering as a family select the shadowing option for the other family members.</p>'
            first_section = htmltemplates.warning_box.format(message=maps_message) + name_selection
            app.logger.info('Late entries open.')
        else:
            title = 'Orienteering Signup - Enter'
            heading = '<p>Enter your details</p><p style="color:red;"><small>Every attendee must be registerred separately - if entering as a family select the shadowing option for the other family members.</small></p>'
            first_section = name_selection
            app.logger.info('Normal entries open.')
            
        return htmltemplates.get_form(10, title=title, modal=modal, heading=heading, info=event_summary, footer=htmltemplates.navbar.format(session['file_name']),
                                    submit_loc="/orienteering/signup", add_script=script).format(first_section,
                                                                                htmltemplates.input_box_help('Email', 'Contact Email Address', help_title, help_info, valid='email', required='True'),
                                                                                htmltemplates.input_box_help('Phone', 'Contact Phone Number', help_title, help_info, valid='tel', required='True'),
                                                                                htmltemplates.tick_to_close('<strong>Untick this box if NOT a member</strong> of a British/Scottish Orienteering (all {} members should tick this)'.format(config.lookup('CLUB')), 'member', htmltemplates.select_box_ls('Club', club_list, True, 'id="Club"')
                                                                                +"""<script>
                                                                                        function togglerqd() {
                                                                                            if (document.getElementById("dib").checked == true || document.getElementById("sha").checked == true){
                                                                                                document.getElementById("Dibber").removeAttribute("required");
                                                                                            } else {
                                                                                                document.getElementById("Dibber").setAttribute("required","");
                                                                                            }
                                                                                            if (document.getElementById("sha").checked == true){
                                                                                                document.getElementById("Sex").removeAttribute("required");
                                                                                                document.getElementById("YOB").removeAttribute("required");
                                                                                            } else {
                                                                                                document.getElementById("Sex").setAttribute("required","");
                                                                                                document.getElementById("YOB").setAttribute("required","");
                                                                                            }
                                                                                            if (document.getElementById("member").checked == true){
                                                                                                document.getElementById("Club").setAttribute("required","");
                                                                                            } else {
                                                                                                document.getElementById("Club").removeAttribute("required");
                                                                                            }
                                                                                        }
                                                                                    </script>""", 'data-toggle="collapse" data-target="#collapsemember" onclick="togglerqd()" checked'),
                                                                                "<p><strong>Course Details:</strong><p>",
                                                                                htmltemplates.tick_to_close_multi(label="This partipant is shadowing",
                                                                                action = 'data-toggle="collapse" data-target=".multi-collapse" onclick="togglerqd()"',
                                                                                id='sha',
                                                                                content=htmltemplates.select_box_ls('Sex', ['Male', 'Female'], True, 'id="Sex"')
                                                                                + htmltemplates.input_box('YOB', 'Year Of Birth', valid='number', required='True', extra_params='min="1900" max="2021"')
                                                                                + dibber_section),
                                                                                htmltemplates.collapse_box_closed_multi.format(id='sha2', content=htmltemplates.toggle_box.format(id='shamap', label='Shadow With Map?', action='')),
                                                                                '<div></div>',
                                                                                htmltemplates.select_box_dict('Course', session['courses'], required='True'),
                                                                                htmltemplates.select_box_ls('PREFERRED Start Time', session['starts'], required='True')
                                                                                )


    if request.method == "POST":
        wb, event, fees, courses, start = load_sheets(session['file'])  # reload the workbook in case changed in the meantime
        session['checkout']=False
        session["card_payments"]=False
        if card_payments(event) : session["card_payments"]=True
        script = checkout_required(session)
        app.logger.info('Page running as POST; File: {} opened'.format(session['file']))
        name, email, phone, details, date, year, age, age_class, age_class_mod, fee, course, desc, start_time, dib, club = None, None, None, None, None, None, None, None, None, None, None, None, None, None, None
        name = request.form["Name"]
        email = request.form["Email"]
        phone = request.form["Phone"]
        details = get_event_details(event)
        if request.form.get('sha') == None:
            date = details["date"]
            year = date.year
            age = year - int(request.form["YOB"])
            if request.form["Sex"] == 'Male':
                age_class = 'M{}'.format(get_age_class(age))
            else:
                age_class = 'W{}'.format(get_age_class(age))
            if request.form.get('member'):
                age_class_mod = age_class + ' (SOA/BOF Member)'
                club = request.form["Club"]
            else:
                age_class_mod = age_class + ' (Non-Member)'
                club = 'Independant'
            if request.form.get('dib') == None:
                dib = request.form["Dibber"]
            else:
                dib = "HIRE"
        else:
            age_class = 'Shadowing'
            if request.form.get('shamap') == None:
                age_class_mod = age_class + ' (NO map)'
            else:
                age_class_mod = age_class + ' (WITH map)'
            if request.form.get('member'):
                club = request.form["Club"]
            else:
                club = 'Independant'
            dib = 'N/A'
        fee = session['age_classes'][age_class_mod]
        course = request.form["Course"]
        start_time = request.form["PREFERRED Start Time"]
        app.logger.info('Data from form: {} opened'.format([name, email, phone, age_class, fee, course, start_time, dib]))
        result, message = update_sheet(event, start, courses, start_time, name, course, age_class_mod, fee, dib, phone, email, club)
        app.logger.info(message)
        if result:
            write_wbook(wb,session['file'])
            session['running_total'] += float(fee)
            this_entry = {}
            this_entry["Event"] = session["file_name"]
            this_entry['Name'] = name
            this_entry['Start Time'] = start_time
            this_entry['Course'] = course
            this_entry['Age Class'] = age_class
            this_entry['Cost'] = '£{}'.format(fee)
            this_entry['Dibber No.'] = dib
            this_entry['Phone'] = phone
            this_entry['Email'] = email
            this_entry['Running Total'] = '£' + str(session['running_total']).strip('0').strip('.')

            temp = [this_entry]
            session['all_entries'] += temp
            result = mail.simple_message(
                            to=email, subject='{} Event entry'.format(config.lookup('CLUB')),
                            content=(htmltemplates.table(title='Orienteering Signup - Invoice',
                                        footer="",
                                        pgheading='You Made This Entry - UNCONFIRMED:',
                                        info="""Your preferred start time is shown, this time has been temporarily reserved for you.
                                                <strong>We are now using credit card payments for most events - entries are only secured after payment.</strong>
                                                The event organiser will confirm start times after the closing date.
                                                Please ensure you follow the <a href='https://bof2.sharepoint.com/:b:/g/Competitions/EfX0-LmKllFDiR_DAzbLLhEB7CdDSNDQvXfky33Tk4U5Zw?e=xRd4NC'>British Orienteering Covid Code of Conduct.</a>
                                                <p>You can checkout on the same device you reserved the times on here (link may not work after a period of time):
                                                    <A Href={domain}/orienteering/invoice>{domain}/orienteering/invoice</a></p> """.format(domain=config.lookup('DOMAIN')),
                                        data=temp,
                                        headings=['Name', 'Start Time', 'Course', 'Age Class', 'Cost', 'Dibber No.', 'Phone', 'Email', 'Event'])

                                    ))

            if session:
                if session['card_payments'] == True and session['running_total'] > 0:
                    message = message + "Please add any other entrants, <strong>then</strong> pay for your order."
                    return (htmltemplates.success(title='Orienteering Signup - Success',
                                                heading="Success! Don't forget to checkout",
                                                footer=htmltemplates.navbar.format(session['file_name']), message=message, script=script)
                        + htmltemplates.checkout_three_buttons(label1='Add Another Entrant',
                                                ln1=('/orienteering/signup?type='+session['file_name']),
                                                label2='Enter Another Event',
                                                ln2='/'
                                                ))

            return (htmltemplates.success(title='Orienteering Signup - Success', heading='Success!', footer=htmltemplates.navbar.format(session['file_name']), message=message, script=script)
                    + htmltemplates.two_buttons_ln(label1="Show your Invoice",
                                                label2='Add Another Entrant',
                                                ln1='/orienteering/invoice',
                                                ln2=('/orienteering/signup?type='+session['file_name'])
                                                ))
        else:
            return htmltemplates.error(title='Orienteering Signup - Failure', heading='Something went wrong!', footer=htmltemplates.navbar.format(session['file_name']), message=message)

@app.route('/orienteering/invoice', methods=["GET", "POST"])
def invoice():
    if 'all_entries' in session:
        session['checkout'] = True
        payment_method = '''Print, take a screenshot of this page, on click <a href="/orienteering/email-invoice">here</a> to get an email list of your entries,
                            you will be billed by the club for your entries from time to time.'''
        if 'card_payments' in session and session['running_total'] > 0 :
            if session['card_payments'] == True:
                session['checkout'] = False
                payment_method = '''You still need to pay for these entries via Stripe - click here to {} or cancel ALL above {}'''.format(htmltemplates.stripe_button,htmltemplates.clear_button)
        script = checkout_required(session)
        return (htmltemplates.table(title='Orienteering Signup - Invoice', script=script,
                footer=htmltemplates.navbar.format(session['file_name']),
                pgheading='You Requested These Entries:',
                info="""<p>Your preferred start times are shown, the event organiser will confirm start times after the closing date.
                        Entry confirmation will be subject to the payment arrangements below.</p>"""+
                        htmltemplates.warning_box.format(message='Your Total Cost is: £{}'.format(str(session['running_total']).strip('0').strip('.'))) +
                        "<h4>What do I do now?</h4>" +
                        htmltemplates.info_box.format(message=payment_method),
                data=session['all_entries'],
                headings=['Name', 'Start Time', 'Course', 'Age Class', 'Cost', 'Dibber No.', 'Phone', 'Email', 'Event'])
                )

    else:
        return (htmltemplates.error(title='Orienteering Signup - Invoice',
            footer=htmltemplates.navbar.format(""),
            message='Your have no pending requests or your session has expired - if you are having problems please contact {}'.format(config.lookup('EMAIL'))))


@app.route('/orienteering/success', methods=["GET"])
def success():
    for entry in session['all_entries']:
        status = confirmed_paid(EVENTSPATH+entry['Event']+".xlsx",entry['Start Time'],entry['Name'], entry['Course'])
    session.clear()
    app.logger.info("Session cleared")
    app.logger.info(status)
    script = ""
    if status : return htmltemplates.info(title='Sucess', heading='Payment Successful', footer=htmltemplates.navbar.format(""), message='''Your entries were successful, and payment was received.  Please remember the organiser may adjust times.  If you are required to self isolate please do not attend the event - contact us to discuss a refund.''')
    else: return htmltemplates.error(title='WARNING', heading='Your Payment was Successful but entry has a problem', footer=htmltemplates.navbar.format(""), message='''Your entries were not saved properly but payment was received.  Please contact {} for advice.'''.format(config.lookup('EMAIL')))


@app.route('/orienteering/clear', methods=["GET"])
def clear():
    for entry in session['all_entries']:
        cancel_entry(EVENTSPATH+entry['Event']+".xlsx",entry['Start Time'],entry['Name'], entry['Course'])
    session.clear()
    return htmltemplates.warning(title='Sessions cleared', heading='ALL UNPAID ENTRIES CLEARED', footer=htmltemplates.navbar.format(""), message='''Your unpaid entries booked on this device were cleared.''')

@app.route('/orienteering/email-invoice', methods=["GET", "POST"])
def email():
    script = checkout_required(session)
    result = mail.simple_message(
                            to=session['all_entries'][0]['Email'], subject='{} Event entry'.format(config.lookup('CLUB')),
                            content=(htmltemplates.table(title='Orienteering Signup - Invoice',
                                        footer="",
                                        pgheading='You Made These Entries:',
                                        info="Your preferred start times are shown, the event organiser will confirm start times after the closing date.",
                                        data=session['all_entries'],
                                        headings=['Name', 'Start Time', 'Course', 'Age Class', 'Cost', 'Dibber No.', 'Phone', 'Email', 'Event'])
                                        + htmltemplates.warning_box.format(message='Your Total Cost is: £{}'.format(str(session['running_total']).strip('0').strip('.')))
                                    ))
    if result:
        return htmltemplates.success(title='Orienteering Signup - Email Confirmed', heading='Success!', footer=htmltemplates.navbar.format(session['file_name']), script=script, message='Your invoice for {} has been successfully sent to {}.'.format(session['file_name'],session['all_entries'][0]['Email']))
    else:
        return htmltemplates.error(title='Orienteering Signup - Failure', heading='Something Went Wrong', script=script, footer=htmltemplates.navbar.format(session['file_name']), message='''Something went wrong when sending you your invoice by email, please <a href="/orienteering/email-invoice">try again</a>''')
    #return htmltemplates.error(title='Orienteering Signup - Failure', heading='Something Went Wrong', message='''Something went wrong when sending you your invoice by email, please <a href="/orienteering/email-invoice">try again</a>''')

@app.route('/orienteering/view-entries', methods=["GET", "POST"])
def view():
    script = checkout_required(session)
    event_options = [os.path.splitext(os.path.basename(file))[0] for file in glob.glob(EVENTSPATH +'*.xlsx')]
    app.logger.info(event_options)
    try:
        session['file_name'] = request.args.get('type')
        session['file']=EVENTSPATH+session['file_name']+'.xlsx'
        wb, event, fees, courses, start = load_sheets(session['file'])
        event_summary = get_event_summary(event)
        session['event_summary']=event_summary
    except:
        return htmltemplates.get_dropdown(title='Orienteering Signup - View Entries', script=script, heading='Select the event you wish to view', footer=htmltemplates.navbar.format(session['file_name']), dd_list=event_options, form_action="/orienteering/view-entries")
    entries = get_entries(start)
    return (htmltemplates.get_dropdown(title='Orienteering Signup - View Entries', script=script, footer=htmltemplates.navbar.format(session['file_name']),
        heading='Choose a different event?', dd_list=event_options, form_action="/orienteering/view-entries", info=event_summary)
        + htmltemplates.table(pgheading='Current Entries: <p style="color:red"><small>(subject to change check the link above for final version)</small></p>', data=entries, headings=['Name', 'Start Time', 'Course', 'Age Class', 'Dibber No.', 'Club']))

@app.route('/orienteering/admin', methods=["GET", "POST"])
def admin():
    event_options = [os.path.splitext(os.path.basename(file))[0] for file in glob.glob(EVENTSPATH+'*.xlsx')]
    app.logger.info(event_options)

    try:
        session['file_name'] = request.args.get('type')
        session['file']=EVENTSPATH+session['file_name']+'.xlsx'
        wb, event, fees, courses, start = load_sheets(session['file'])
        event_summary = get_event_summary(event)
        session['event_summary']=event_summary

    except:
        msg = "Select an event to get the event file sent to the registered organiser"
        return htmltemplates.get_dropdown(title='Orienteering Signup - View Entries', heading=msg, dd_list=event_options, form_action="/orienteering/admin")

    details = get_event_details(event)
    result = mail.with_attachment(
                            to=details['org_email'],
                            subject='{} Event entry file'.format(config.lookup('CLUB')),
                            content="The file you requested is attached",
                            file_path=session['file'],
                            file_type="application/vnd.ms-excel")
    app.logger.info("email send requested to:"+details['org_email'])
    app.logger.info("RESULT = "+str(result))

    msg = "The event file below has been sent to registered email address of the organiser"
    return (htmltemplates.get_dropdown(title='Orienteering Organiser Download', footer=htmltemplates.navbar.format(session['file_name']),
        heading=msg, dd_list=event_options, form_action="/orienteering/admin", info=event_summary))




@app.route('/orienteering/create-checkout-session', methods=['POST'])
def create_checkout_session():
    app.logger.info("checkout session initiated")
    stripe_session = stripe.checkout.Session.create(
                        customer_email=session['all_entries'][0]['Email'],
                        payment_method_types=['card'],
                        line_items=[
                                    {
                                        'price_data': {
                                            'currency': 'gbp',
                                            'unit_amount': int(float(entry['Cost'][1:])*100),
                                            'product_data': {
                                                'name': entry['Event'] + " for " + entry['Name'] ,
                                            },
                                        },
                                        'quantity': 1,
                                    }
                                    for entry in session['all_entries'] ],
                        mode='payment',
                        success_url=YOUR_DOMAIN + '/orienteering/success',
                        cancel_url=YOUR_DOMAIN + '/orienteering/invoice' )
    return jsonify(id=stripe_session.id)





