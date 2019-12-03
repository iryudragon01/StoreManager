from stock.models import Item,Stock
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


class EditItemform(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['price', 'type', 'is_active','user_access']


    def __init__(self, *args, **kwargs):
        super(EditItemform, self).__init__(*args, **kwargs)        
        self.fields['price'].widget = forms.TextInput(attrs={
            'type': 'number',
            'class': 'form-control',
            'name': 'price',
            'placeholder': 'price'})
        self.fields['type'].widget = forms.Select(

            choices=[('1', 'Ticket'), ('2', 'Air pay'), ('3', 'Food')],
            attrs={'class': 'custom-select'})   
            
        self.fields['is_active'].widget = forms.Select(

            choices=[('0', 'inactive'), ('1', 'active')],
            attrs={'class': 'custom-select'})   
            
        self.fields['user_access'].widget = forms.Select(

            choices=[('1', 'admin'), ('10', 'power user'), ('99', 'worker')],
            attrs={'class': 'custom-select'})   


class TopupForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['item', 'volume', 'creater_id', 'create_time', 'editer_id', 'edit_time']

