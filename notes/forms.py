from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import *


# class ImageForm(forms.Form):
#     image = forms.ImageField(
#         widget=forms.FileInput(
#             attrs={"id": "image_field", style="height: 100px ; width : 100px ; "}
#     )

class SignInUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class AddPrivateNoteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(AddPrivateNoteForm, self).__init__(*args, **kwargs)
        self.fields['folder'].queryset = Folder.objects.filter(user=self.request.user.id)
        self.fields['folder'].empty_label = "Folder isn't selected"

    class Meta:
        model = Note
        exclude = ['user', 'slug']
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'class': 'form-textarea', 'cols': 80, 'rows': 12}),
            'folder': forms.Select(attrs={'class': 'form-select'})
        }


class AddFolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        exclude = ['user', 'slug']
        fields = '__all__'
        widgets = {'title': forms.TextInput(attrs={'class': 'form-input'})}
