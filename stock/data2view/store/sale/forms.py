from django import forms

class ItemFrom(forms.Form):
    name= forms.TextInput()
    start = forms.IntegerField()
    now = forms.IntegerField()
    sale=forms.IntegerField()
    price = forms.IntegerField()
    money = forms.IntegerField()
    sum = forms.IntegerField()