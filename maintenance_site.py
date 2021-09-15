
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request, session, redirect,  render_template, jsonify
import htmltemplates

app = Flask(__name__,static_folder=".",
            static_url_path="", template_folder=".")

@app.route('/', methods=["GET", "POST"])
def home():
    app.logger.info("Attempted access during mainainance.")
    return (htmltemplates.error(title='Orienteering Signup - Maintainance',
                                        heading='Site Down For Maintainance',
                                        message="Sorry, this site is down for maintainance right now. Please check back later when the service has returned.")
                                        )

@app.route('/orienteering')
def wrong_adress():
    return redirect("/", 303)

@app.route('/orienteering/signup', methods=["GET", "POST"])
def signup():
    return redirect("/", 307)

@app.route('/orienteering/invoice', methods=["GET", "POST"])
def invoice():
    return redirect("/", 307)

@app.route('/orienteering/success', methods=["GET"])
def success():
    return redirect("/", 307)

@app.route('/orienteering/clear', methods=["GET"])
def clear():
    return redirect("/", 307)
    
@app.route('/orienteering/email-invoice', methods=["GET", "POST"])
def email():
    return redirect("/", 307)

@app.route('/orienteering/view-entries', methods=["GET", "POST"])
def view():
    return redirect("/", 307)

@app.route('/orienteering/admin', methods=["GET", "POST"])
def admin():
    return redirect("/", 307)

@app.route('/orienteering/create-checkout-session', methods=['POST'])
def create_checkout_session():
    return redirect("/", 307)