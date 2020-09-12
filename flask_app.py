
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

SITEPATH = "/home/fvo/mysite/"
EVENTSPATH = SITEPATH+"events/"
MEMBERFILE = SITEPATH + "private/members.xlsx"



last_question, v, Qkeys, two_parts, Qt = None, None, None, False, None
wb, start, start_times, age_classes, courses, starts = None, None, None, None, None, None

app = Flask(__name__,static_folder=".",
            static_url_path="", template_folder=".")
app.config["DEBUG"] = False
app.config["SECRET_KEY"] = secrets.token_urlsafe(256)

help_title = "Why Do We Need This?"
help_info = "We may need these details to contact you if the event is cancelled.  We MAY be required to share this information with Health Protection Scotland if someone at the event develops symptoms of a communicable disease."


@app.route('/', methods=["GET", "POST"])
def home():
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
        wb, event, fees, course, start = load_sheets(session['file'])
        app.logger.info('Page running as GET; File: {} opened'.format(session['file']))
        session['start_times'] = read_time(start)
        session['age_classes'] = read_ageclass(fees)
        session['age_classes_mod'] = session['age_classes'].copy()
        for each in session['age_classes_mod']:
            session['age_classes_mod'][each] = '£'+str(session['age_classes_mod'][each])
        session['courses'] = read_course(course)
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
            return htmltemplates.warning(title='Orienteering Signup - Enter', heading='This event is now closed', message=event_summary, footer=htmltemplates.navbar.format(session['file_name']))
        else:
            if session['running_total'] > 0:
                modal = False
            else :
                modal = True
            return htmltemplates.get_form(9, title='Orienteering Signup - Enter', modal=modal, heading='Enter your details', info=event_summary, footer=htmltemplates.navbar.format(session['file_name']),
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
        wb, event, fees, course, start = load_sheets(session['file'])  # reload the workbook in case changed in the meantime
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
        result, message = update_sheet(start, start_time, name, course, age_class, fee, dib, phone, email)
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
                                        pgheading='You Made This Entry:',
                                        info="Your preferred start time is shown, the event organiser will confirm start times after the closing date. Please ensure you follow the <a href='https://bof2.sharepoint.com/:b:/g/Competitions/EfX0-LmKllFDiR_DAzbLLhEB7CdDSNDQvXfky33Tk4U5Zw?e=xRd4NC'>British Orienteering Covid Code of Conduct.</a>",
                                        data=temp,
                                        headings=['Name', 'Start Time', 'Course', 'Age Class', 'Cost', 'Dibber No.', 'Phone', 'Email', 'Event'])

                                    ))


            return (htmltemplates.success(title='Orienteering Signup - Success', heading='Success!', footer=htmltemplates.navbar.format(session['file_name']), message=message)
                    + htmltemplates.two_buttons_ln(label1='Get Your Invoice',
                                                label2='Add Another Entrant',
                                                ln1='/orienteering/invoice',
                                                ln2=('/orienteering/signup?type='+session['file_name'])
                                                ))
        else:
            return htmltemplates.error(title='Orienteering Signup - Failure', heading='Something went wrong!', footer=htmltemplates.navbar.format(session['file_name']), message=message)

@app.route('/orienteering/invoice', methods=["GET", "POST"])
def invoice():
    return (htmltemplates.table(title='Orienteering Signup - Invoice',
            footer=htmltemplates.navbar.format(session['file_name']),
            pgheading='You Made These Entries:',
            info="Your preferred start times are shown, the event organiser will confirm start times after the closing date.",
            data=session['all_entries'],
            headings=['Name', 'Start Time', 'Course', 'Age Class', 'Cost', 'Dibber No.', 'Phone', 'Email', 'Event'])
            + htmltemplates.warning(message='Your Total Cost is: £{}'.format(str(session['running_total']).strip('0').strip('.')))
            + htmltemplates.info(heading='What Do I Do Now?', message='''Print, take a screenshot of this page, on click <a href="/orienteering/email-invoice">here</a> to get an email list of your entries,
                                                                         you will be billed by the club for your entries from time to time.'''))

@app.route('/orienteering/email-invoice', methods=["GET", "POST"])
def email():

    result = fvomail.simple_message(
                            to=session['all_entries'][0]['Email'], subject='FVO Event entry',
                            content=(htmltemplates.table(title='Orienteering Signup - Invoice',
                                        footer="",
                                        pgheading='You Made These Entries:',
                                        info="Your preferred start times are shown, the event organiser will confirm start times after the closing date.",
                                        data=session['all_entries'],
                                        headings=['Name', 'Start Time', 'Course', 'Age Class', 'Cost', 'Dibber No.', 'Phone', 'Email', 'Event'])
                                        + htmltemplates.warning(message='Your Total Cost is: £{}'.format(str(session['running_total']).strip('0').strip('.')))
                                    ))
    if result:
        return htmltemplates.success(title='Orienteering Signup - Email Confirmed', heading='Success!', footer=htmltemplates.navbar.format(session['file_name']), message='Your invoice for {} has been successfully sent to {}.'.format(session['file_name'],session['all_entries'][0]['Email']))
    else:
        return htmltemplates.error(title='Orienteering Signup - Failure', heading='Something Went Wrong', footer=htmltemplates.navbar.format(session['file_name']), message='''Something went wrong when sending you your invoice by email, please <a href="/orienteering/email-invoice">try again</a>''')
    #return htmltemplates.error(title='Orienteering Signup - Failure', heading='Something Went Wrong', message='''Something went wrong when sending you your invoice by email, please <a href="/orienteering/email-invoice">try again</a>''')

@app.route('/orienteering/view-entries', methods=["GET", "POST"])
def view():
    event_options = [os.path.splitext(os.path.basename(file))[0] for file in glob.glob(EVENTSPATH +'*.xlsx')]
    app.logger.info(event_options)
    try:
        session['file_name'] = request.args.get('type')
        session['file']=EVENTSPATH+session['file_name']+'.xlsx'
        wb, event, fees, course, start = load_sheets(session['file'])
        event_summary = get_event_summary(event)
        session['event_summary']=event_summary
    except:
        return htmltemplates.get_dropdown(title='Orienteering Signup - View Entries', heading='Select the event you wish to view', dd_list=event_options, form_action="/orienteering/view-entries")
    entries = get_entries(start)
    return (htmltemplates.get_dropdown(title='Orienteering Signup - View Entries', footer=htmltemplates.navbar.format(session['file_name']),
        heading='Choose a different event?', dd_list=event_options, form_action="/orienteering/view-entries", info=event_summary)
        + htmltemplates.table(pgheading='Current Entries:', data=entries, headings=['Name', 'Start Time', 'Course', 'Age Class', 'Dibber No.']))

@app.route('/orienteering/admin', methods=["GET", "POST"])
def admin():
    event_options = [os.path.splitext(os.path.basename(file))[0] for file in glob.glob(EVENTSPATH+'*.xlsx')]
    app.logger.info(event_options)

    try:
        session['file_name'] = request.args.get('type')
        session['file']=EVENTSPATH+session['file_name']+'.xlsx'
        wb, event, fees, course, start = load_sheets(session['file'])
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







