from django import forms

from .validators import validate_url


class SubmitURLForm(forms.Form):
    url = forms.CharField(
        label='',
        validators=[validate_url],
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Long URL',
                'class': 'form-control'
            }
        )
    )


    # def clean(self):
    #     cleaned_data = super().clean()
    #     url = cleaned_data.get('url')
    #     url_validator = URLValidator()
    #     try:
    #         url_validator(url)
    #     except:
    #         raise ValidationError('Invalid URL for this field')
    #     return url


    def clean_url(self):
        url = self.cleaned_data.get('url')
        if not url.startswith('http'):
            url = 'http://' + url
        return url