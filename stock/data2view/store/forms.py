from django import forms
from stock.models import User,Worker


class WorkerCreateForm(forms.Form):
    username = forms.SlugField(
        label='worker id',
        max_length=200,
        min_length=1,
        widget=forms.TextInput(
            attrs={'placeholder': 'worker id','class':'form-control border border-primary'}
        )

    )
    password = forms.CharField(
        label='worker password',
        max_length=200,
        min_length=1,
        widget=forms.PasswordInput(
            attrs={'placeholder': 'password for worker','class':'form-control border border-primary '}
        )

    )
    confirm_password = forms.CharField(
        label='confirm password',
        max_length=200,
        min_length=1,
        widget=forms.PasswordInput(
            attrs={'placeholder': 'confirm password','class':'form-control border border-primary border border-primary'}
        )

    )
    

    def clean(self):
        cleaned_data = super(WorkerCreateForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        username = cleaned_data.get('username')
        if not username:
            raise forms.ValidationError('username is not correct')

        if password != confirm_password:
            raise forms.ValidationError('password and confirm password do not match')


class WorkerLoginForm(forms.Form):
    username = forms.CharField(max_length=255,min_length=1)
    password = forms.CharField(widget=forms.PasswordInput(),min_length=1)


class EditWorkerForm(forms.ModelForm):

    class Meta:
        model = Worker
        fields =['access_level']
