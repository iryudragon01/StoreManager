from stock.models import Item
from django import forms


class CreateItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'price', 'type']

    def __init__(self, *args, **kwargs):
        super(CreateItemForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget = forms.TextInput(attrs={
            'id': 'name',
            'class': 'form-control',
            'name': 'name',
            'placeholder': 'Item Name'})
        self.fields['price'].widget = forms.TextInput(attrs={
            'type': 'number',
            'class': 'form-control',
            'name': 'price',
            'placeholder': 'price'})
        self.fields['type'].widget = forms.Select(

            choices=[('1', 'Ticket'), ('2', 'Air pay'), ('3', 'Food')],
            attrs={'class': 'custom-select'})
