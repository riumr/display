from django import forms
from django.forms import ModelForm
from .models import Index

class IndexForm(ModelForm):
    class Meta:
        model=Index
        fields='__all__'