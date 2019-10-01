# Inventory Management System #

Inventory Management System is a web based Application developed in Python/Django. The Software is designed for the small business to maintain there records, customer ledger, sales and etc.<br>
<br>Designed by <a href="partumsolutions.com">Partum Solutions</a> (New Startup in Quetta, Pakistan. Provides Services and Solutions).

## Features

Retailers (Multi Tenancy)<br>
Customer and Ledgers <br>
Stock Management <br>
Low Stock Notification <br>
Sales <br>
Employees <br>
Expenses <br>
Suppliers <br>
Feedback <br>
Sales Reports (Daily, Weekly, Monthly) <br>
Stocks Logs (Daily, Monthly) <br>

## Python Version
2.7.10<br>

Using Django Framework and JQuery on the Frontend


## Demo URL

<a href="http://demo-inventory.herokuapp.com/"> You can find the Demo here</a>


## To Get Started ##

1. Create a Virtual Environment

2. Create a Fork and Clone Project by using the following command

> git clone git@github.com:janzaheer/partum_inventory.git

3. Create local settings file and add the local database configuration, You can use any database SQLite, Mysql or Postgress SQL etc. Following is the configuration code for SQLite database.
```
# settings_local.py

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.local'),
    }
}
```

4. Go to the main directory where `manage.py` file exists abd install all the requirements by running the command:
> pip install -r requirements.txt

4. Migrate by runnning the following command.
> python manage.py migrate

5. Create super user to access the admin
> python manage.py createsuperuser

6. Run the Django Server by using following command.
> python manage.py runserver

Now you can access the application in your browser by URL `http://localhost:8000`

## Need Help? ##
<ul>
<li>You can ask me any question any time, email me zaheerjanbadini@gmail.com</li>
<li>Please use GitHub issues to report issues.</li>
</ul>

## Contribute
As an open source project with a strong focus on the user community, we welcome contributions as GitHub pull requests. See our Contributor Guides to get going. Discussions and RFCs for features happen on the design discussions section of our Forum.


