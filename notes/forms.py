from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import *


class SignInUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class AddPrivateNoteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(AddPrivateNoteForm, self).__init__(*args, **kwargs)
        self.fields['folder'].queryset = Folder.objects.filter(user=self.request.user.id)

    class Meta:
        model = Note
        exclude = ['user', 'slug']
        fields = '__all__'


class AddFolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        exclude = ['user', 'slug']
        fields = '__all__'
