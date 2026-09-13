from django import forms
from django.contrib.auth.models import User
import re


class ContactForm(forms.Form):
    f_name = forms.CharField(max_length=25)
    l_name = forms.CharField(max_length=25)
    email = forms.EmailField()
    subject = forms.CharField(max_length=25)
    message = forms.CharField(widget=forms.TextInput)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=25)
    password = forms.CharField(widget=forms.PasswordInput)

class SignUpForm(forms.Form):
    first_name = forms.CharField(max_length=25)
    last_name = forms.CharField(max_length=25)
    username = forms.CharField(max_length=25)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()

    def clean_username(self):
        username =self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('username is exists')
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password)>15 or len(password)<4:
            raise forms.ValidationError('password must contain')
        elif not re.search(r'[A-Za-z]',password):
            raise forms.ValidationError('password must contain a letter')
        elif not re.search(r'[0-9]',password):
            raise forms.ValidationError('password must contain number')
        return password

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('email already exists')
        return email


class RecruitmentForm(forms.Form):
    f_name = forms.CharField(max_length=25)
    l_name = forms.CharField(max_length=25)
    email = forms.EmailField()
    phone= forms.CharField(max_length=11)
    address = forms.CharField(widget=forms.Textarea)
    job_title = forms.CharField(max_length=25)
    skill = forms.CharField(widget=forms.Textarea)
    work_history = forms.CharField(widget=forms.Textarea)

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if len(phone) != 11:
            raise forms.ValidationError('the phone must be 11 digit long')
        if not phone.isdigit():
            raise forms.ValidationError('the phone number must be digit')
        return phone

class CommentForm(forms.Form):
    text = forms.CharField(widget=forms.TextInput)
    rating = forms.IntegerField(min_value=1,max_value=5)

class EditCommentForm(forms.Form):
    text = forms.CharField(widget=forms.TextInput)
    rating = forms.IntegerField(max_value=5,min_value=1)