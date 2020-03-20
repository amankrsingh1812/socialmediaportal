from django import forms
from django.forms import ModelForm
from .models import Employee

class Dashboardform(forms.Form):
    inputtextFacebook = forms.CharField(max_length=1000,initial=None,required=False)
    inputtextTwitter = forms.CharField(max_length=1000,initial=None,required=False)
    inputtextLinkedIn = forms.CharField(max_length=1000,initial=None,required=False)
    inputfileFacebook = forms.FileField(initial=None,required=False)
    inputfileTwitter = forms.FileField(initial=None,required=False)

class AdminForm(ModelForm):
    class Meta:
        model=Employee
        exclude=('emp_id',)

