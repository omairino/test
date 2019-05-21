from django import forms

class ReadFileForm(forms.Form):
    file = forms.FileField()
    page_id = forms.CharField()
    access_token = forms.CharField()

