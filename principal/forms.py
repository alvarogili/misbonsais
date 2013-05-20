#encoding:utf-8
from django.forms import ModelForm
from django import forms
from principal.models import Bonsai, Labor, EMail
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from fields import ReCaptchaField 

class BonsaiForm(ModelForm):
    class Meta:
		model = Bonsai        

class LaborForm(ModelForm):
    class Meta:
		model = Labor

#formulario para el registro de un nuevo usuario
class RegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=30)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=75)
    recaptcha = ReCaptchaField()

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.username = self.cleaned_data["username"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

#formulario para el envío de contraseña
class sendPassword(ModelForm):
    class Meta:
        model = EMail

#edición de usuario
class UserEditForm(ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=75)

    class meta:
        model = User
        fields = ("first_name", "last_name", "email")    