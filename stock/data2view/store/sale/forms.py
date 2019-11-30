from django import forms
from stock.models import Sale
from datetime import datetime,timedelta
from django.utils import timezone

class ItemForm(forms.Form):
    name= forms.TextInput()
    start = forms.IntegerField()
    now = forms.IntegerField()
    sale=forms.IntegerField()
    price = forms.IntegerField()
    money = forms.IntegerField()
    sum = forms.IntegerField()


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale    
        fields = ['id']


class ListTime(forms.Form):
    getDate=forms.CharField(max_length=200,widget=forms.DateTimeInput(
        attrs={'type':'datetime-local'}
    ))

    def clean_getDate(self):
        getdate = self.cleaned_data['getDate']
        diff=timediff()
        try:
           rawtime = datetime.strptime(getdate,'%Y-%m-%dT%H:%M')+\
                     timedelta(hours=diff['hour'],minutes=diff['minute'])
           return rawtime

        except:
            raise forms.ValidationError('format date is not correct')


def timediff() :
    timeZ = timezone.now()
    timeD = datetime.now()
    subz = 24*60*timeZ.day+60*timeZ.hour+timeZ.minute
    subd = 24*60*timeD.day+60*timeD.hour+timeD.minute
    diff = subz-subd
    hour = int(diff / 60)
    minute =diff-hour*60
    return {'hour':hour,'minute':minute}