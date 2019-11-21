from django import forms
from stock.models import Worker, User
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import authenticate, login


class RegisterForm(forms.ModelForm):
    password = forms.CharField(min_length=6, max_length=200, widget=forms.PasswordInput())
    confirm_password = forms.CharField(min_length=6, max_length=200, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['email', 'full_name','url']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = User.objects.filter(email=email)
        if user.exists():
            raise forms.ValidationError(email + ' is already exists')
        return email

    def clean_confirm_password(self):
        # Check that the password and confirm password entries match
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords don't match")
        return confirm_password

    def save(self, commit=True):
        # Save provide password in hashed format
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserAdminCreationForm(forms.ModelForm):
    password = forms.CharField(min_length=6, max_length=200, widget=forms.PasswordInput())
    confirm_password = forms.CharField(min_length=6, max_length=200, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['email', 'full_name']

    def clean_confirm_password(self):
        # Check that the password and confirm password entries match
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords don't match")
        return confirm_password

    def save(self, commit=True):
        # Save provide password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
       the user, but replaces the password field with admin's
       password hash display field.
       """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['email', 'url', 'password', 'active', 'admin']

        def clean_password(self):
            # Regardless of what the user provides, return the initial value.
            # This is done here, rather than on the field, because the
            # field does not have access to the initial value
            return self.initial["password"]


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        email = self.cleaned_data.get('email')
        user = User.objects.filter(email=email)
        if not user.exists():
            raise forms.ValidationError(email + " is don't exists!!")
        password = self.cleaned_data['password']
        user = authenticate(email=email, password=password)
        if user is None:
            raise forms.ValidationError('wrong password')
