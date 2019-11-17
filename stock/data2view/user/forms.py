from django import forms
from stock.models import User,UserExtend
import hashlib

class RegisterForm(forms.Form):
    email = forms.EmailField()
    username = forms.CharField(min_length=3, max_length=200)
    password = forms.CharField(min_length=6, max_length=200, widget=forms.PasswordInput())
    confirm_password = forms.CharField(min_length=6, max_length=200, widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        if password != confirm_password:
            raise forms.ValidationError('password and confirm password do not match')

        if User.objects.filter(username=username).count() > 0 or \
                User.objects.filter(email=email).count() > 0:
            raise forms.ValidationError('This User already exist!!')
        else:
            user = User(
                email=email,
                username=username,
                password=hashlib.sha512(password.encode('utf-8')).hexdigest()
            )
            user.save()


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'username or email',
                   'class': 'username_class'}
        )
    )
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if User.objects.filter(username=username).count()>0:
            login =User.objects.get(username=username)
        elif User.objects.filter(email=username).count()>0:
            login = User.objects.get(email=username)
        else:
            raise forms.ValidationError(username + ' is not found')
        if login.password == hashlib.sha512(password.encode('utf-8')).hexdigest():
            print('login success')
        else:
            raise forms.ValidationError('password is not correct')


class WorkerForm(forms.Form):
    username = forms.CharField(
        label='worker id',
        max_length=200,
        min_length=1,
        widget=forms.TextInput(
            attrs={'placeholder':'worker id'}
        )

    )
    password = forms.CharField(
        label='worker password',
        max_length=200,
        min_length=1,
        widget=forms.PasswordInput(
            attrs={'placeholder':'password for worker'}
        )

    )
    confirm_password = forms.CharField(
        label='confirm password',
        max_length=200,
        min_length=1,
        widget=forms.PasswordInput(
            attrs={'placeholder':'confirm password'}
        )

    )

    def clean(self):
        cleaned_data = super(WorkerForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        username = cleaned_data.get('username')
        if password != confirm_password:
            raise forms.ValidationError('password and confirm password do not match')

        if UserExtend.objects.filter(username=username).count() > 0:
            raise forms.ValidationError('This User already exist!!')
        else:
            user = User(
                username=username,
                password=hashlib.sha512(password.encode('utf-8')).hexdigest()
            )
            user.save()

