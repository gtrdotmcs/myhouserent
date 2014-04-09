from django import forms

class CountryForm(forms.Form):
    print forms.Form,"ff"
    OPTIONS = (
            ("AUT", "Australia"),
            ("DEU", "Germany"),
            ("NLD", "Neitherlands"),
            )
    Countries = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                         choices=OPTIONS)   