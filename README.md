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
> 
> **NOTE: Replace 'Europe/London' with your appropriate contient/city if you aren't using**
> **GMT/BST time.**
>
> - To prepare for cloning later, also add '/O-Book' to
> ```
> project_home = '/home/username/mysite'
> ```
> after 'mysite', making sure it is still **inside the quotes**. It should look like
> ```
> project_home = '/home/username/mysite/O-Book'
> ```
>
> - Click the 'Save' button in the top right.
>
> <br>

### Setting Up The Code
> <br>
> 
> In order to set up the code, you need to clone the GitHub repository.
> - Use the burger menu (three bars in the top right) to select 'Files'.
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
> - Click on the 'Files' tab at the top of the page.
> - Select 'mysite/' from the directory list, then 'O-Book/'.
> - Open 'config.txt' in the file list.
> - Change the options to the appropriate values, then click the 'Save' button in the top right.
> 
> **NOTE: The only parts of the config files needing replaced are the placeholder names. The ALL CAPS**
> **names left of the equals, and the equals, MUST BE UNCHANGED. The comments right of the '#' can be**
> **deleted, though this is unnecessary. The header and blank line MUST ALSO BE UNCHANGED.**
> <br>

### Generating Project Skeleton
> <br>
>
> The next step in setting up the site is to run the setup script.
> - Use the burger menu (three bars in the top right) to select 'Files'.
> - Select 'mysite/' from the directory list, then 'O-Book/'
> - Click 'Open Bash console here' above the file list.
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
> **NOTE: Stripe offers four types of keys: Live and Test, and Secret and Public versions**
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

### Updating The Code
> <br>
>
> As work on O-Book is a continuous project, changes will be made to the code on the GitHub to
> address new feature requests and bug reports. In order to have these changes made live on
> your site
> - Open a new bash console in the 'O-Book' directory.
> - Enter
> ```
> git pull
> ```
> To check what has been changed with this update, and for information on any changes you
> may need to make
> - Enter
> ```
> python changelog.py
> ```
> In order to update your site with the new code
> - Open any of the site's files
> - Click the 'Reload Site' button (the refresh symbol) in the top right.
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

## FAQs
> <br>
>
> This PDF contains a list of the most common questions users have about the site.
> While these are ready to go and use, you may wish to replace the file with more
> tailored answers, including contact emails or other questions you find getting
> asked a lot. The easiest way to do so would be to copy and paste the contents
> into a word processor, make your modifications, and export the file as a PDF.
> 
> **NOTE: The file MUST still be called 'FAQs.pdf' or the code will not be able to locate it.**
>
> <br>

## EDIT_ENTRY.PY
> <br>
>
> This file is a simple utility for quickly modifying entries. It is most useful
> when a competitior needs to change their timeslot or other details, as it
> allows the modification to be made without fiddling with the .xlsx file and/or 
> the live site down to avoid double booking.
>
> To use the program
> - First, open a bash console in your O-Book directory
> - Now, type
> ```
> python edit_entry.py
> ```
> - This will prompt you with a list of all your events, with a number in square brackets on the far left. Type the number next to the event you need to edit.
> - This will now prompt you with yet another list, this time of every entry already made in that event. Again, enter the number next to the entry you need to edit.
> - Once more, you will be prompted with a list of all the details for that entry. Enter the letter associated with the necessary field.
> - You may now enter your new value. Once you press enter, you must confirm the change by typing either "Y" or "y" before it will be changed. If you wish to cancel your entry, type anything else or simple press enter.
>
> <br>