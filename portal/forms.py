from django import forms


class Dashboardform(forms.Form):
    inputtextFacebook = forms.CharField(max_length=1000,initial=None,required=False)
    inputtextTwitter = forms.CharField(max_length=1000,initial=None,required=False)
    inputtextLinkedIn = forms.CharField(max_length=1000,initial=None,required=False)
    inputfileFacebook = forms.FileField(initial=None,required=False)
    inputfileTwitter = forms.FileField(initial=None,required=False)


