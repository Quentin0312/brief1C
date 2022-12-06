from django import forms
from django.forms import ModelForm
from .models import Paramgraph

class UploadFileForm(forms.Form):
    file = forms.FileField()

class ParamForm(ModelForm):
    class Meta:
        model = Paramgraph
        fields = ('nomgraph','param1',)

class graph3Form(ModelForm):
    class Meta:
        model = Paramgraph
        fields = ('nomgraph','param1','param2')