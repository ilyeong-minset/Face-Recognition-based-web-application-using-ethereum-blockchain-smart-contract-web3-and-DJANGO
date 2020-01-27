from django import forms

class FormName(forms.Form):
    Ethereum_Private_Key=forms.CharField(
        max_length=250,
        widget=forms.TextInput(
            attrs={
                'size':50,
                'placeholder': 'Enter here'
            }
        )
    )

    def clean(self):
        all_clean_data=super().clean()
        x=all_clean_data['Ethereum_Private_Key']
        y="c3e146b8e2b9f3facc919358f36fbecdc4f4cd0987f8da1d8f9c1ef45f0696ff"
        if x!=y:
            raise forms.ValidationError("Please enter your correct Ethereum private key")
