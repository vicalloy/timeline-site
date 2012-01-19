from userena.forms import SignupForm, AuthenticationForm, ChangeEmailForm
from userena.utils import get_profile_model
from django.contrib.auth.forms import PasswordChangeForm

from bootstrap.forms import BootstrapMixin, BootstrapModelForm

class BsSignupForm(SignupForm, BootstrapMixin):

    def __init__(self, *args, **kw):
        super(BsSignupForm, self).__init__(*args, **kw)
        self.__bootstrap__()

class BsAuthenticationForm(AuthenticationForm, BootstrapMixin):

    def __init__(self, *args, **kw):
        super(BsAuthenticationForm, self).__init__(*args, **kw)
        self.__bootstrap__()

class BsPasswordChangeForm(PasswordChangeForm, BootstrapMixin):

    def __init__(self, *args, **kw):
        super(BsPasswordChangeForm, self).__init__(*args, **kw)
        self.__bootstrap__()

class BsChangeEmailForm(ChangeEmailForm, BootstrapMixin):

    def __init__(self, *args, **kw):
        print "------------xxx"
        super(BsChangeEmailForm, self).__init__(*args, **kw)
        self.__bootstrap__()

class BsEditProfileForm(BootstrapModelForm):

    class Meta:
        model = get_profile_model()
        exclude = ['user']

    def save(self, force_insert=False, force_update=False, commit=True):
        profile = super(BsEditProfileForm, self).save(commit=commit)
        user = profile.user
        user.save()
        return profile
