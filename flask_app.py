
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request, session, redirect,  render_template, jsonify
import traceback
import htmltemplates
from backend import *
import glob
import secrets
import collections
import fvomail
import json
import os
from datetime import datetime
import stripe

stripe.api_key = ""

SITEPATH = "/home/fvo/mysite/"
EVENTSPATH = SITEPATH+"events/"
MEMBERFILE = SITEPATH + "private/members.xlsx"
YOUR_DOMAIN = 'http://fvo.eu.pythonanywhere.com'

last_question, v, Qkeys, two_parts, Qt = None, None, None, False, None
wb, start, start_times, age_classes, courses, starts = None, None, None, None, None, None

app = Flask(__name__,static_folder=".",
            static_url_path="", template_folder=".")
app.config["DEBUG"] = False
app.config["SECRET_KEY"] = secrets.token_urlsafe(256)

checkout_warning =  ""
help_title = "Why Do We Need This?"
help_info = "We may need these details to contact you if the event is cancelled.  We MAY be required to share this information with Health Protection Scotland if someone at the event develops symptoms of a communicable disease."

def checkout_required(session):
    script = ''
    if 'running_total' in session and 'card_payments' in session:
        #if session['running_total']>0 and session['card_payments']==True: script = '<script src="https://fvo.eu.pythonanywhere.com/checkout_warning.js"></script>'
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
                                        dd_list=event_options, form_action="/orienteering/signup")
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
                                        content=htmltemplates.input_box('Dibber', 'Dibber Number', valid='number', extra_params='min="1000" max="9999999" required') +
                                                """<script>
                                                        function togglerqd() {
                                                                if (document.getElementById("dib").checked == true){
                                                                    document.getElementById("Dibber").removeAttribute("required");
                                                                    } else {
                                                                    document.getElementById("Dibber").setAttribute("required","");
                                                                    }
                                                                }
                                                    </script>""")
        else:
            dibber_section = htmltemplates.input_box('Dibber', 'Dibber Number', valid='number', required='True', extra_params='min="1000" max="9999999"')

        if members_only(event):
            name_section = htmltemplates.select_box_ls("Name", sorted(get_members(MEMBERFILE).keys()), required='True')
        else:
            name_section = htmltemplates.input_box('Name', 'Full Name of Participant', valid='text', required='True')



        if event_closed(event):
            app.logger.info('Event closing date passed...')
            if late_entries(event):
                app.logger.info('...but late entries still open' )
                if session['running_total'] > 0:
                    modal = False
                else :
                    modal = True
                return htmltemplates.get_form(9, title='Limited maps remaining', modal=modal, heading='Limited Maps Remaining - Enter your details <p><small>Entry fees include a late entry premium</small></p><p>Every attendee must be registerred - if entering as a family select the shadowing option for the other family members.</p>', info=event_summary, footer=htmltemplates.navbar.format(session['file_name']),
                                    submit_loc="/orienteering/signup").format(  name_section,
                                                                                htmltemplates.input_box_help('Email', 'Contact Email Address', help_title, help_info, valid='email', required='True'),
                                                                                htmltemplates.input_box_help('Phone', 'Contact Phone Number', help_title, help_info, valid='tel', required='True'),
                                                                                "<p><strong>Course Details:</strong><p>",
                                                                                htmltemplates.select_box_dict('Age Class', session['age_classes_mod'], required='True'),
                                                                                htmltemplates.select_box_dict('Course', session['courses'], required='True'),
                                                                                htmltemplates.select_box_ls('PREFERRED Start Time', session['starts'], required='True'),
                                                                                '<div></div>',
                                                                                dibber_section)


            else:
                return htmltemplates.warning(title='Orienteering Signup - Enter', script=script, heading='This event is now closed', message=event_summary, footer=htmltemplates.navbar.format(session['file_name']))

        else:
            if session['running_total'] > 0:
                modal = False
            else :
                modal = True
            return htmltemplates.get_form(9, title='Orienteering Signup - Enter', modal=modal, heading='<p>Enter your details</p><p style="color:red;"><small>Every attendee must be registerred separately - if entering as a family select the shadowing option for the other family members.</small></p>', info=event_summary, footer=htmltemplates.navbar.format(session['file_name']),
                                    submit_loc="/orienteering/signup").format(  name_section,
                                                                                htmltemplates.input_box_help('Email', 'Contact Email Address', help_title, help_info, valid='email', required='True'),
                                                                                htmltemplates.input_box_help('Phone', 'Contact Phone Number', help_title, help_info, valid='tel', required='True'),
                                                                                "<p><strong>Course Details:</strong><p>",
                                                                                htmltemplates.select_box_dict('Age Class', session['age_classes_mod'], required='True'),
                                                                                htmltemplates.select_box_dict('Course', session['courses'], required='True'),
                                                                                htmltemplates.select_box_ls('PREFERRED Start Time', session['starts'], required='True'),
                                                                                '<div></div>',
                                                                                dibber_section)


    if request.method == "POST":
        wb, event, fees, courses, start = load_sheets(session['file'])  # reload the workbook in case changed in the meantime
        session["card_payments"]=False
        if card_payments(event) : session["card_payments"]=True
        app.logger.info('Page running as POST; File: {} opened'.format(session['file']))
        name, email, phone, age_class, age_class, fee, course, desc, start_time, dib = None, None, None, None, None, None, None, None, None, None
        name = request.form["Name"]
        email = request.form["Email"]
        phone = request.form["Phone"]
        age_class = request.form["Age Class"]
        fee = session['age_classes'][age_class]
        course = request.form["Course"]
        start_time = request.form["PREFERRED Start Time"]
        dib = request.form.get('dib')
        if dib == None:
            dib = request.form["Dibber"]
        else:
            dib = "HIRE"
        app.logger.info('Data from form: {} opened'.format([name, email, phone, age_class, fee, course, start_time, dib]))
        result, message = update_sheet(event, start, courses, start_time, name, course, age_class, fee, dib, phone, email)
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
            this_entry['Cost'] = session['age_classes_mod'][age_class]
            this_entry['Dibber No.'] = dib
            this_entry['Phone'] = phone
            this_entry['Email'] = email
            this_entry['Running Total'] = '£' + str(session['running_total']).strip('0').strip('.')

            temp = [this_entry]
            session['all_entries'] += temp
            result = fvomail.simple_message(
                            to=email, subject='FVO Event entry',
                            content=(htmltemplates.table(title='Orienteering Signup - Invoice',
                                        footer="",
                                        pgheading='You Made This Entry - UNCONFIRMED:',
                                        info="""Your preferred start time is shown, this time has been temporarily reserved for you.
                                                <strong>We are now using credit card payments for most events - entries are only secured after payment.</strong>
                                                The event organiser will confirm start times after the closing date.
                                                Please ensure you follow the <a href='https://bof2.sharepoint.com/:b:/g/Competitions/EfX0-LmKllFDiR_DAzbLLhEB7CdDSNDQvXfky33Tk4U5Zw?e=xRd4NC'>British Orienteering Covid Code of Conduct.</a>
                                                <p>You can checkout on the same device you reserved the times on here (link may not work after a period of time):
                                                    <A Href=https://fvo.eu.pythonanywhere.com/orienteering/invoice>https://fvo.eu.pythonanywhere.com/orienteering/invoice</a></p> """,
                                        data=temp,
                                        headings=['Name', 'Start Time', 'Course', 'Age Class', 'Cost', 'Dibber No.', 'Phone', 'Email', 'Event'])

                                    ))

            if session:
                if session['card_payments'] == True and session['running_total'] > 0:
                    return (htmltemplates.success(title='Orienteering Signup - Success',
                                                heading="Success! Don't forget to checkout",
                                                footer=htmltemplates.navbar.format(session['file_name']), message=message, script=script)
                        + htmltemplates.checkout_two_buttons(label2='Add Another Entrant',
                                                ln2=('/orienteering/signup?type='+session['file_name'])
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
    script = checkout_required(session)
    payment_method = '''Print, take a screenshot of this page, on click <a href="/orienteering/email-invoice">here</a> to get an email list of your entries,
                        you will be billed by the club for your entries from time to time.'''
    if 'all_entries' in session:
        if 'card_payments' in session and session['running_total'] > 0 :
            if session['card_payments'] == True:
                #checkout_warning='<script src="https://fvo.eu.pythonanywhere.com/checkout_warning.js"></script>'
                payment_method = '''You still need to pay for these entries via Stripe - click here to {} or cancel ALL above {}'''.format(htmltemplates.stripe_button,htmltemplates.clear_button)

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
            footer=htmltemplates.navbar.format(),
            message='Your have no pending requests or your session has expired - if you are having problems please contact membership@fvo.org.uk'))


@app.route('/orienteering/success', methods=["GET"])
def success():
    script = checkout_required(session)
    for entry in session['all_entries']:
        status = confirmed_paid(EVENTSPATH+entry['Event']+".xlsx",entry['Start Time'],entry['Name'], entry['Course'])
    session.clear()
    app.logger.info("Session cleared")
    app.logger.info(status)
    script = ""
    if status : return htmltemplates.info(title='Sucess', heading='Payment Successful', footer=htmltemplates.navbar.format(checkout_warning), message='''Your entries were successful, and payment was received.  Please remember the organiser may adjust times.  If you are required to self isolate please do not attend the event - contact us to discuss a refund.''')
    else: return htmltemplates.error(title='WARNING', heading='Your Payment was Successful but entry has a problem', footer=htmltemplates.navbar.format(checkout_warning), message='''Your entries were not saved properly but payment was received.  Please contact membership@fvo.org.uk for advice.''')


@app.route('/orienteering/clear', methods=["GET"])
def clear():
    for entry in session['all_entries']:
        cancel_entry(EVENTSPATH+entry['Event']+".xlsx",entry['Start Time'],entry['Name'], entry['Course'])
    session.clear()
    return htmltemplates.warning(title='Sessions cleared', heading='ALL UNPAID ENTRIES CLEARED', footer=htmltemplates.navbar.format(checkout_warning), message='''Your unpaid entries booked on this device were cleared.''')

@app.route('/orienteering/email-invoice', methods=["GET", "POST"])
def email():
    script = checkout_required(session)
    result = fvomail.simple_message(
                            to=session['all_entries'][0]['Email'], subject='FVO Event entry',
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
        + htmltemplates.table(pgheading='Current Entries: <p style="color:red"><small>(subject to change check the link above for final version)</small></p>', data=entries, headings=['Name', 'Start Time', 'Course', 'Age Class', 'Dibber No.']))

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
    result = fvomail.with_attachment(
                            to=details['org_email'],
                            subject='FVO Event entry file',
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





