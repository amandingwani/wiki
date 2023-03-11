from django import forms

class NewPageForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100, min_length=1,required=True)
    content = forms.CharField(widget=forms.Textarea)