from django import forms
from stock.models import Sale, Stock
from datetime import datetime, timedelta
from django.utils import timezone


class ItemForm(forms.Form):
    name = forms.TextInput()
    start = forms.IntegerField()
    now = forms.IntegerField()
    sale = forms.IntegerField()
    price = forms.IntegerField()
    money = forms.IntegerField()
    sum = forms.IntegerField()


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['id']


class ListTime(forms.Form):
    getDate = forms.CharField(max_length=200, widget=forms.DateTimeInput(
        attrs={'type': 'datetime-local'}
    ))

    def clean_getDate(self):
        getdate = self.cleaned_data['getDate']
        try:
            time = datetime.strptime(getdate, '%Y-%m-%dT%H:%M')
            return time

        except:
            raise forms.ValidationError('format date is not correct')
