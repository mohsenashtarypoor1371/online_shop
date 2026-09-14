import datetime
from collections import UserString
from random import choice
from unicodedata import digit
import re


from django import forms
from django.contrib.auth import user_logged_in
from django.core.management.sql import emit_post_migrate_signal

from . models import *


class ContactForm(forms.ModelForm):
    class Meta:
        fields = ['first_name' ,'last_name' ,'criticisms' ,'email','subject']
        model = ContactUs

class CooperationForm(forms.ModelForm):
    class Meta:
        fields = ['name','phone','email','job_title','description']
        model = Cooperation
        widgets = {'description':forms.TextInput(attrs={'rows':4})}

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone.isdigit():
            raise forms.ValidationError('phone number must be number')
        elif phone > 11 :
            raise forms.ValidationError(' the phone number must be eleven digits')
        elif phone < 10:
            raise forms.ValidationError('the phone number must be more than ten digits')
        return phone


class CommentForm(forms.Form):
    name_user = forms.CharField(max_length=20,label='name_user')
    email_user = forms.EmailField(label='email_user')
    picture_user = forms.ImageField(label='picture_user',required=False)
    comment_user = forms.CharField(widget=forms.Textarea)

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput,max_length=8,required=True)

    def clean_username(self):
        username = self.cleaned_data['username']
        if username.isdigit():
            raise forms.ValidationError('user con not digit')
        return username


class SignupForm(forms.Form):
    username = forms.CharField(max_length=25,required=True)
    password = forms.CharField(widget=forms.PasswordInput,required=True)
    email = forms.EmailField()

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username.isdigit():
            raise forms.ValidationError('username con not digit')
        return username
    def clean_password(self):
        password = self.cleaned_data['password']
        let = re.findall(r'[A-Za-z]',password)
        if len(let)<3:
            raise forms.ValidationError('password must be at least 3 characters')
        return password
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('this email already exists')
        return email



