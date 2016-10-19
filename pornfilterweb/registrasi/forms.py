from django import forms
from registrasi.models import Registrasi


class RegistrasiForm(forms.ModelForm):
    class Meta:
        model = Registrasi
        # exclude = ['author', 'updated', 'created', ]
        fields = ['mode','ip']
        widgets = {
            'mode': forms.TextInput(
                attrs={'id': 'mode','value':''}
            ),
            'ip': forms.TextInput(
                attrs={'id': 'ip','value':''}
            ),
        }
