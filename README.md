# A Django social auth test: Google accounting

Uses `127.0.0.1 test.stuff.com` in `hosts` to ensure Google doesn't try to call a localhost domain.

- clone
- set up virtual env and activate it
- pip install -r requirements
- python manage.py createsuperuser

I turned off pw validation and use `admin`/`admin@example.com`/`admin`/`admin` as inputs

- python manage.py makemigrations
- python manage.py migrate
- python manage.py runserver

Then open [http://localhost:8000](http://localhost:8000) which should open up a "click here" link that will guide you through giving our app access to your Google account - specifically your standard userinfo (name, email, etc).

Running through this will create a new Django user if no user exists already for your email address.
