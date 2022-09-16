from django.urls import path
from App_auth.views import *

app_name = 'App_auth'

urlpatterns = [
    path('login-or-signup/', login_or_signup, name='login-or-signup'),
    path('login-signup', login_signup, name='login-signup'),
    path('logout/', logout_view, name='logout'),
    path('profile-view/', profile_view, name='profile-view'),
    path('profile-submit/', profile_submit, name='profile-submit'),
    path('profile-picture-submit/', profile_picture_upload, name='profile-picture-submit'),
]
