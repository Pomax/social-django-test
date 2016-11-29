import random
import string
from django.http import HttpResponse
from httplib2 import Http
from oauth2client import client
from django.contrib.auth.models import User
from apiclient.discovery import build
from django.core import serializers

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
TEMPORARY: THESE THINGS SHOULD LIVE ON THE SESSION USER OBJECT!
"""
credentials = False
http_auth = False


"""
utility function
"""
def random_password(length=16):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))


"""
Initial page with a link that lets us sign in through Google
"""
def index(request):
    auth_uri = flow.step1_get_authorize_url()

    return HttpResponse("Hello, world, let's log in: <a href='" + str(auth_uri) + "'>CLICK HERE</a>")


"""
An explicit logout route.
"""
def logout(request):
    global credentials
    global http_auth

    if credentials is not False:
        credentials.revoke(http_auth)
        credentials = False
        http_auth = False

    return HttpResponse("revoked, hopefully")


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
        global credentials
        global http_auth

        credentials = flow.step2_exchange(auth_code)
        http_auth = credentials.authorize(Http())

        service = build('oauth2', 'v2', http=http_auth)
        userinfo = service.userinfo().get().execute()

        name = userinfo['name']
        email = userinfo['email']

        try:
            user = User.objects.get(email=email)
            print "found user in database based on email address."

        except User.DoesNotExist:
            user = User.objects.create_user(
                username=name,
                email=email,
                # we generate a random password: the user will never use -nor need to know- this.
                password=random_password()
            )
            print "user not found: created user based on email address."

        return HttpResponse("login succeeded, with code: " + str(auth_code))

    return HttpResponse("callback happened without an error or code query argument: wtf")
