from django import forms
 
from .models import Pokemon
 
class MoveForm (forms.ModelForm):
 
    class Meta:
        model = Pokemon
        fields = ('lieu',)