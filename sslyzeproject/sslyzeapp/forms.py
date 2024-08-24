from django import forms

class TextInputForm(forms.Form):
    user_input = forms.CharField(label='Enter Text', max_length=100)
