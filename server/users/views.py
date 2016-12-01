import random
import string
from httplib2 import Http
from oauth2client import client

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import login, logout
from apiclient.discovery import build

from .models import GoogleUser

"""
The flow variable is used to run through oauth2 workflows.
"""
flow = client.flow_from_clientsecrets(
    # we keep the creds in a separate file that we don't check in.
    'client_secrets.json',

    # we want to be able to get a user's name and email
    scope = 'https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile',

    # this url-to-codepath binding is set up in ./users/urls.py
    redirect_uri = 'http://test.stuff.com:8000/oauth2callback',
)

"""
Initial page with a link that lets us sign in through Google
"""
def index(request):
    user = request.user
    if user.is_authenticated:
        return HttpResponse("Hello "+user.email+"! You are already logged in, do you want to <a href='/logout'>log out?</a>")
    auth_uri = flow.step1_get_authorize_url()
    return HttpResponse("Hello there! <a href='" + str(auth_uri) + "'>Click here to log in</a>")


"""
An explicit logout route.
"""
def forceLogout(request):
    user=request.user
    if not user.is_authenticated:
        return redirect("/")
    email=user.email
    logout(request)
    return redirect("/")


"""
The callback route that Google will send the user to when authentication
finishes (with successfully, or erroneously).
"""
def callback(request):
    error = request.GET.get('error', False)
    auth_code = request.GET.get('code', False)

    if error is not False:
        return HttpResponse("login failed: " + str(error))

    if auth_code is not False:
        credentials = flow.step2_exchange(auth_code)
        http_auth = credentials.authorize(Http())
        service = build('oauth2', 'v2', http=http_auth)
        userinfo = service.userinfo().get().execute()

        # get this user's information
        name = userinfo['name']
        email = userinfo['email']

        try:
            # Get the db record for this user and make sure their
            # name matches what google says it should be.
            user = GoogleUser.objects.get(email=email)
            user.name = name
            print "found user in database based on email address."

        except GoogleUser.DoesNotExist:
            # Create a new database entry for this user.
            user = GoogleUser.objects.create_user(
                name=name,
                email=email
            )
            print "user not found: created user based on email address."

        # As this user just authenticated, we mark this user as logged in
        # for the duration of this session.
        login(request, user)

        request.session['csrf'] = "lolcakes";

        #return HttpResponse("login succeeded, with code: " + str(auth_code))
        return HttpResponse("User "+email+" logged in.")

    return HttpResponse("callback happened without an error or code query argument: wtf")
