# A Django social auth test: Google accounting

Uses `127.0.0.1 test.stuff.com` in `hosts` to ensure Google doesn't try to call a localhost domain.

- clone
- set up virtual env and activate it
- pip install -r requirements
- python manage.py createsuperuser

I turned off pw validation in `settings.py`, ran `python manage.py createsuperuser` and gave it `admin`/`admin@example.com`/`admin`/`admin` as inputs for simplicity. Then:

You'll also need a `client_secrets.json` file of the following form in the root dir:

```
{
  "web": {
    "client_id": "google-indicated client id",
    "client_secret": "google-indicated secret for said client id",
    "redirect_uris": ["http://test.stuff.com:8000/oauth2callback"],
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://accounts.google.com/o/oauth2/token"
  }
}
```

- python manage.py makemigrations
- python manage.py migrate
- python manage.py runserver

We should be good to go: open [http://localhost:8000](http://localhost:8000) which should open up a "click here" link that will guide you through giving our app access to your Google account - specifically your standard userinfo (name, email, etc).

Running through this will create a new Django user if no user exists already for your email address.
