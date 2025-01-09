from django import forms
from .models import Restaurant,MenuItem, Order, MenuItem

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = '__all__'



class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = '__all__'


class OrderForm(forms.ModelForm):
    menu_items = forms.ModelMultipleChoiceField(queryset=MenuItem.objects.filter(available=True), widget=forms.CheckboxSelectMultiple)
    quantity = forms.IntegerField(min_value=1)

    class Meta:
        model = Order
        fields = '__all__'