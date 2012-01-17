from django.conf.urls.defaults import *

from userena import views as userena_views

from profiles.forms import BsSignupForm, BsAuthenticationForm

urlpatterns = patterns('',
    url(r'^signup/$', userena_views.signup,
        {'signup_form': BsSignupForm}, name='userena_signup'),
    url(r'^signin/$', userena_views.signin,
        {'auth_form': BsAuthenticationForm}, name='userena_signin'),
    (r'^', include('userena.urls')),
)
