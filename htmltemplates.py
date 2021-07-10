html_skeleton = '''
            <html>
                <head>
                    {head}



                    <script src="https://js.stripe.com/v3/"></script>
                </head>
                <body>
                    <div class="row mx-md-n5">
                        <div class="col px-md-5"><div class="p-3 border bg-light"><p></p></div></div>
                    </div>
                    {body}
                    {footer}
                </body>

            </html>'''

stripe_script = '''
                <script type="text/javascript">
                // Create an instance of the Stripe object with your publishable API key
                var stripe = Stripe("pk_live_51H5yQDGH1HRuykisgVkqgc1yXUSRAW47G2NSQa2OSP9hBnU46uLEYEi2Kv9sUNUwJO2WHkxGEgDy1ltxRNiaNe6l00dfprr5eU");
                var checkoutButton = document.getElementById("checkout-button");
                checkoutButton.addEventListener("click", function () {
                  fetch("/orienteering/create-checkout-session", {
                    method: "POST",
                  })
                    .then(function (response) {
                      return response.json();
                    })
                    .then(function (session) {
                      return stripe.redirectToCheckout({ sessionId: session.id });
                    })
                    .then(function (result) {
                      // If redirectToCheckout fails due to a browser or network
                      // error, you should display the localized error message to your
                      // customer using error.message.
                      if (result.error) {
                        alert(result.error.message);
                      }
                    })
                    .catch(function (error) {
                      console.error("Error:", error);
                    });
                });
              </script>
              '''

html_head_custom_script = '''
                    <meta charset="utf-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
                    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
                    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
                    {script}
                    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk" crossorigin="anonymous">
                    <title>{title}</title>
            '''


html_head = '''
                    <meta charset="utf-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
                    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
                    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
                    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk" crossorigin="anonymous">
                    <title>{title}</title>
            '''

basic_page = '''
            <div class="container">
                    <br>
                    <H3>{header}</H3>
                    {info}
                    <br>
                    {content}
            </div>
            '''

dropdown = '''<div class="container">
                <script> $("[data-toggle=dropdown]").dropdown() </script>
                <div class="dropdown">
                        <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="true">
                            Choose Event...
                        </button>
                        <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                            {choices}
                        </div>
                </div>
                <script> $("[data-toggle=dropdown]").dropdown() </script>
            </div>
            '''

inbox = '''
            <div class="input-group mb-3">
                <div class="input-group-prepend">
                    <span class="input-group-text" id="basic-addon1">{pre}</span>
                </div>
                <input name="{pre}" id="{pre}" type="{valid}" {required} class="form-control" placeholder="{name}" {extra_params}>
            </div>'''


inbox_help = '''
            <script> $("[data-toggle=popover]").popover() </script>
            <div class="input-group mb-3">
                <div class="input-group-prepend">
                    <span class="input-group-text" id="basic-addon1">{pre}</span>
                </div>
                <input name={pre} type={valid} class="form-control" placeholder="{name}" {required} {extra_params}>
                <div class="input-group-append">
                    <button type="button" class="btn btn-outline-info btn-sm" data-toggle="popover" data-container="body" data-placement="left" title="{title}" data-content="{helpinfo}">?</button>
                </div>
            </div>
            <script> $("[data-toggle=popover]").popover() </script>'''


select_box = '''
                <div>
                    <select {required} class="custom-select" name="{name}" placeholder="{name}" {extra_params}>
                        <option value="" disabled selected hidden>{name}</option>
                        {options}
                    </select>
                </div>
                <br>
                '''

toggle_box = '''
                <div class="form-check form-check-inline">
                    <input class="form-check-input" type="checkbox" id="{id}" name="{id}" value="{label}" {action}>
                    <label class="form-check-label" for="inlineCheckbox1">{label}</label>
                </div>'''

collapse_box_closed = '''
                <div class="collapse" id="collapse{id}">
                    {content}
                </div>'''

collapse_box_open = '''
                <div class="collapse show" id="collapse{id}">
                    {content}
                </div>'''

success_box = '''
            <div class="alert alert-success" role="alert">
                {message}
            </div>'''

error_box = '''
            <div class="alert alert-danger" role="alert">
                {message}
            </div>'''

warning_box = '''
            <div class="alert alert-warning" role="alert">
                {message}
            </div>'''

info_box = '''
            <div class="alert alert-info" role="alert">
                {message}
            </div>'''

ln_button = '''
            <a role="button" class="btn btn-success" href="{ln}">{label}</a>'''

clear_button = '''
            <a role="button" class="btn btn-danger" href="https://fvo.eu.pythonanywhere.com/orienteering/clear">Cancel Unpaid Entries</a>'''

stripe_button = """
    <button type="button" class="btn btn-primary" id="checkout-button">Checkout</button>"""+stripe_script



table_skeleton = '''<table class="table">
                <thead>
                    <tr>
                    {head}
                    </tr>
                </thead>
                <tbody>
                    {body}
                </tbody>
            </table>'''

table_header = '''<th scope="col">{title}</th>'''

table_body = '''<tr>
                    <th scope="row">{content}</th>
                    {morecontent}
                </tr>'''

table_row = '''<td>{content}</td>'''

navbar = '''
    <nav class="navbar fixed-top navbar-expand-lg navbar-dark bg-dark">
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarToggler" aria-controls="navbarToggler" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarToggler">
            <a class="navbar-brand" href="https://www.fvo.org.uk">FVO Website</a>
            <ul class="navbar-nav mr-auto mt-2 mt-lg-0">
              <li class="nav-item active">
                <a class="nav-link" href="/">Enter event <span class="sr-only">(current)</span></a>
              </li>
              <li class="nav-item active">
                <a class="nav-link" href="/orienteering/view-entries?type={}">Entry list</a>
              </li>
              <li class="nav-item active">
                <a class="nav-link" href="/Entries_Privacy_Notice.html">Privacy</a>
              </li>
              <li class="nav-item active">
                <a class="nav-link" href="/orienteering/invoice">Review pending bookings</a>
              </li>
              <li class="nav-item active">
                <a class="nav-link" href="/FVO_FAQs.pdf">FAQs</a>
              </li>
            </ul>
        </div>
    </nav>
    '''

covid_modal = '''   <div class="container">

                    <!-- Modal -->
                    <div class="modal fade" id="staticBackdrop" data-backdrop="static" data-keyboard="false" tabindex="-1" role="dialog" aria-labelledby="staticBackdropLabel" aria-hidden="true">
                      <div class="modal-dialog">
                        <div class="modal-content">
                          <div class="modal-header">
                            <h5 class="modal-title" id="staticBackdropLabel">All entrants must acknowledge the British Orienteering COVID Code of Conduct</h5>
                              <span aria-hidden="true">&times;</span>
                            </button>
                          </div>
                          <div class="modal-body">
                            <div class="alert alert-danger" role="alert">
                    Individuals <strong>should not enter</strong> an event if:
                        <ul>
                        <li>They are unwell with a cough, fever or other respiratory symptoms</li>
                        <li>If you or someone in your household or your support bubble is showing coronavirus symptoms, everyone in your support bubble should stay home.
                        If you or a member of your support bubble is contacted as part of the test and trace programme, the individual contacted should stay at home.
                        If that individual becomes symptomatic, everyone in the support bubble must then isolate.</li>
                        <li>If they have returned from any overseas country (except for ROI or one of the exempted countries identified by the government)
                        until they have completed the self-quarantine period for 14 days, even if they are symptom-free</li>
                        <li>If they are undergoing COVID-19 testing, until they have received negative test results and are symptom-free</li>
                        <li>If they have been advised to stay at home by a health professional.</li>
                        </ul>
                    </div>

                    <div class="alert alert-secondary" role="alert">
                    Only share transport to an event with other members of your household.
                    </div>

                    <div class="alert alert-secondary" role="alert">
                    Arrive at an event during the time window that you have been allocated by the organising club.
                    </div>

                    <div class="alert alert-warning" role="alert">
                    <strong>Observe social distancing requirements at all times</strong> at an event, including - but not only:
                        <ul>
                        <li>when you arrive, at registration,</li>
                        <li>while on the course,</li>
                        <li>at download, and </li>
                        <li>when you leave.</li>
                        </ul>
                    </div>

                    <div class="alert alert-secondary" role="alert">
                    Minimise, as far as possible, contact with others from outside your household before, during and after the race.
                    </div>

                    <div class="alert alert-danger" role="alert">
                    <strong>Keep your distance</strong> from other participants and members of the public <strong>when waiting to start, on the course, and at the finish</strong>
                    </div>

                    <div class="alert alert-warning" role="alert">
                    <strong>Move quickly away from controls after you have punched</strong> – do not stand next to a control looking at your map to work out your route to the next control.
                    </div>

                    <div class="alert alert-success" role="alert">
                    <strong>Give way to members of the public on narrow paths and at gates or stiles.</strong>
                    </div>

                    <div class="alert alert-secondary" role="alert">
                    After finishing a course, move away from the finish, allow yourself to recover (e.g. by catching your breath and reducing your rate of perspiration), and then <strong>move swiftly through download and to your vehicle.</strong>
                    </div>

                    <div class="alert alert-danger" role="alert">
                    Do not congregate in groups at an event.
                    </div>

                    <div class="alert alert-success" role="alert">
                    Be patient, courteous and respectful of others at all times. Do anything that a club volunteer asks you to do – their request may be necessary to comply with rules put in place to enable the event to take place.
                    </div>
                  </div>
                  <div class="modal-footer">
                    <button type="button" class="btn btn-primary" data-dismiss="modal">Agreed</button>
                  </div>
                </div>
              </div>
            </div>
        '''

modal_jscript = ''' <script type="text/javascript"> $(window).on('load',function(){{$('#staticBackdrop').modal('show');}});</script>'''

def get_dropdown(title="", heading="",dd_list=None, form_action="#", dropdown=dropdown, basic_page=basic_page,
                html_head=html_head, html_skeleton=html_skeleton, footer="", info="", script=""):
    dd = dropdown.format(choices = "".join( ['<li><a class="dropdown-item" href="'+form_action+'?type='+option+'">'+option+'</a></li>\n' for option in dd_list]))
    if info != "": info=info_box.format(message=info)
    page = basic_page.format(header=heading, info=info, content = dd)
    head = html_head_custom_script.format(title=title,script=script)
    return html_skeleton.format(head=head, body=page, footer=footer)

def get_form(size=0, title="", heading="", basic_page=basic_page, html_head=html_head,html_skeleton=html_skeleton, submit_loc="", footer="", info="", modal="", add_script=""):
    fields = '<form method="post" action="{}">'.format(submit_loc)
    for i in range(size):
        fields += " <div></div> {} "
        if i == (size-1):
            fields += '<button type="submit" class="btn btn-success">Submit</button></form>'
    if modal:
        script=modal_jscript+add_script
        content=modal+fields
    else:
        script = add_script
        #script='<script src="https://fvo.eu.pythonanywhere.com/checkout_warning.js"></script>'
        content=fields
    head = html_head_custom_script.format(title=title,script=script)
    page = basic_page.format(header=heading, info=info_box.format(message=info), content=content)

    return html_skeleton.format(head=head, body=page, footer=footer)

def input_box(prefix="", name="", valid="text", required=False, extra_params=""):
    if required : required = "required"
    return inbox.format(pre=prefix, name=name, valid=valid, required=required, extra_params=extra_params)

def input_box_help(prefix="", name="", title="", helpinfo="", valid="text", required=False, extra_params=""):
    if required : required = "required"
    return inbox_help.format(pre=prefix, name=name, title=title, helpinfo=helpinfo, valid=valid, required=required, extra_params=extra_params)

def select_box_dict(name="", dict={0:0}, required=False, extra_params=""):
    if required : required = "required"
    return select_box.format(name=name,required=required,
                        options="".join( ['<option value="'
                                        +key+
                                        '">'
                                        +key+
                                        ' ('
                                        +str(dict[key])+
                                        ')</option>' for key in dict if key != None]),
                                        extra_params=extra_params)

def tick_to_close(label="", id="", content="", action="", toggle_box=toggle_box, collapse_box=collapse_box_open):
    box = toggle_box.format(label=label, action=action, id=id)
    hidden = collapse_box.format(id=id, content=content)
    return box + '<div></div><br>' + hidden

def tick_to_open(label="", id="", content="", action="", toggle_box=toggle_box, collapse_box=collapse_box_closed):
    box = toggle_box.format(label=label, action=action, id=id)
    hidden = collapse_box.format(id=id, content=content)
    return box + '<div></div><br>' + hidden

def select_box_ls(name="", ls=[], required=False, extra_params=""):
    if required : required = "required"
    return select_box.format(name=name, required=required,
                                        options="".join(['<option value="'
                                        +item+
                                        '">'
                                        +item+
                                        '</option>' for item in ls]),
                                        extra_params=extra_params)

def success(title="", heading="", message="", footer="", script=""):
    alert = success_box.format(message=message)
    head = html_head_custom_script.format(title=title,script=script)
    page = basic_page.format(header=heading, info="", content=alert)
    return html_skeleton.format(head=head, body=page, footer=footer)

def error(title="", heading="", message="", footer="", script=""):
    alert = error_box.format(message=message)
    head = html_head_custom_script.format(title=title,script=script)
    page = basic_page.format(header=heading, info="", content=alert)
    return html_skeleton.format(head=head, body=page, footer=footer)

def warning(title="", heading="", message="", footer="", script=""):
    alert = warning_box.format(message=message)
    head = html_head_custom_script.format(title=title,script=script)
    page = basic_page.format(header=heading, info="", content=alert)
    return html_skeleton.format(head=head, body=page, footer=footer)

def info(title="", heading="", message="", footer="", script=""):
    alert = info_box.format(message=message)
    head = html_head_custom_script.format(title=title,script=script)
    page = basic_page.format(header=heading, info="", content=alert)
    return html_skeleton.format(head=head, body=page, footer=footer)

def two_buttons_ln(heading="", label1="", label2="", ln1="#", ln2="#", footer=""):
    button1 = ln_button.format(label=label1, ln=ln1)
    button2 = ln_button.format(label=label2, ln=ln2)
    return basic_page.format(header=heading, content=button1+' Or '+button2, info="", footer=footer)

def checkout_three_buttons(heading="", label1="", ln1="#", label2="", ln2="#", footer=""):
    button1 = ln_button.format(label=label1, ln=ln1)
    button2 = ln_button.format(label=label2, ln=ln2)
    button3 = stripe_button
    return basic_page.format(header=heading, content=button1+button2+button3, info="")


def table(title="", pgheading="", data=[], headings=None, footer="", info="", script=""):
    if not headings: headings = data[0].keys()
    rows, headers = [], []
    for row in data:
        cells = [row[key] for key in headings]
        rows.append(table_body.format(content=cells[0], morecontent="".join([table_row.format(content=info) for info in cells[1:]])))
    for heading in headings:
        headers.append(table_header.format(title=heading))
    tab = table_skeleton.format(head="".join([header for header in headers]),
                                body="".join([row for row in rows]))
    if info != "": info=info_box.format(message=info)
    page = basic_page.format(header=pgheading, content=tab, info=info)
    pghead = html_head_custom_script.format(title=title,script=script)
    return html_skeleton.format(head=pghead, body=page, footer=footer)

def button_ln(heading="", label="", ln="#", footer=""):
    button = ln_button.format(label=label, ln=ln)
    return basic_page.format(header=heading, content=button, info="", footer=footer)

def covid_popup():
    return covid_modal














