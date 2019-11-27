from django import forms
from stock.models import Sale

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