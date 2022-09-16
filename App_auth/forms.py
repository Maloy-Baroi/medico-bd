from django import forms
from App_auth.models import *


class ProfileModelForm(forms.ModelForm):
    class Meta:
        model = ProfileModel
        exclude = ['user', 'paymentID', 'profile_picture']


class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = ProfileModel
        fields = ['profile_picture']

    def __init__(self, *args, **kwargs):
        super(ProfilePictureForm, self).__init__(*args, **kwargs)
        self.fields['profile_picture'].label = ""


