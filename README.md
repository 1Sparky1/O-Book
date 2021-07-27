# SET UP

### Setting Up Pythonanywhere
> <br>
>
> The first step is setting up your pythonanywhere site.
> - Firstly, set up a pythonanywhere account.
> This can be done at https://www.pythonanywhere.com/registration/register/beginner/
>
> **NOTE: If you are in Europe, in order to comply with GDPR, you should use the EU**
> **hosted site. A box should pop-up when you register.**
> **If not, try at https://eu.pythonanywhere.com/registration/register/beginner/**
>
> - Now, you should click on the 'Open Web tab' button.
> - Click 'Add a new web app'.
> - Take a quick note of your domain name (It can be found later), then press next.
> - Select 'Flask', then 'Python 3.9 (Flask 2.0.0)'.
> - Press next.
>
> **NOTE: Pythonanywhere sites are supported indefinitely, but to save servers,**
> **sites are automatically disabled after 3 months. You will recieve an email**
> **warning you that this will happen. In order to renew the site for another**
> **3 months, simply use the 'Run until 3 months from today' button on the web**
> **app page.**
>
> <br>

### Setting Up Time Zones
> <br>
>
> To ensure accurate closure times for events, you need to set the timezone of the website (UTC by default)
> - From the web app page, scroll down to the 'Code' section, and click on the 'WSGI configuration file'.
> - Add this code the the page, underneath 'import sys'
> ```
> import os
> import time
>
> os.environ["TZ"] = "Europe/London"
> time.tzset()
> ```
> - Click the 'Save' button in the top right.
> 
> **NOTE: Replace 'Europe/London' with your appropriate contient/city if you aren't using**
> **GMT/BST time.**
>
> <br>

### Setting Up The Code
> <br>
>
> - In order to set up the code, click on the 'Files' tab at the top of the page.
> - Click 'mysite/' in the directory list.
> - Press the 'delete' button (the bin) next to 'flask_app.py'.
> - Click 'Open Bash console here' above the file list.
> - Enter this into the console
> ```
> git clone https://github.com/1Sparky1/O-Book
> ```
> Assuming you get no errors, everything is now set up correctly.
> - Use the burger menu (three bars in the top right) to select 'Consoles'.
> - Click the X next to 'Bash console \******'.
>
> <br>
	
### Setting Up The Config Files
> <br>
>
> The next file to set up is the config file.
> - Click on the 'Files' tab again.
> - Select 'mysite/' from the directory list, then 'O-Book/'.
> - Open 'config.txt' in the file list.
> - Change the options to the appropriate values, then click the 'Save' button in the top right.
>
> <br>

### Generating Project Skeleton
> <br>
>
> The next step in setting up the site is to run the setup script.
> - To do so, open a new bash console in the 'O-Book' directory.
> - Enter
> ```
> python project_setup.py
> ```
> Assuming you get no errors, everything is now set up correctly.
> - Use the burger menu (three bars in the top right) to select 'Consoles'.
> - Click the X next to 'Bash console \******'.
>
> <br>

### Adding the .env files
> <br>
>
> After registering for both SendGrid (https://signup.sendgrid.com/)
> and Stripe (https://dashboard.stripe.com/register), you need to obtain their API keys.
>> #### **Stripe**
>> - After logging into Stripe, click on the 'Developers' tab on the left, then the
>> 'API Keys' subtab.
>> - Click on 'Create Secret Key' on the right.
>> - Copy the key when it is presented to you. Paste this **BETWEEN THE QUOTES** in the
>> 'stripe.env' file.
>> - Click the 'Save' button in the top right.
>
> **Note: Stripe offers four types of keys: Live and Test, and Secret and Public versions**
> **of both. For use on a live site, you need the Secret Live key (Starts: sk_live) but for**
> **testing, you should use the Secret Test key (Starts: sk_test). Test keys don't actually**
> **charge anything, so are good for making sure the system works.**
>
>> #### **SendGrid**
>> - After logging into SendGrid, click on 'Settings' in the bottom left, then on 'API Keys'.
>> - Click 'Create API Key', then name the key and select 'Full Access'.
>> - Copy the key when it is presented to you. Paste this **BETWEEN THE QUOTES** in the
>> 'sendgrid.env' file.
>> - Click the 'Save' button in the top right.
>
> - Before closing the last file, click the 'Reload Site' button (the refresh symbol) in the top right.
>
> <br>

<br>

# PROJECT DETAILS

## EVENTS
> <br>
>
> This folder is for uploading new events. Read internal README for more 
> information.
>
> <br>

## PRIVATE
> <br>
>
> This folder should contain the members.xlsx file if "members only" is being 
> used for any event.
>
> <br>
