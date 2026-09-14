from django import forms
#
class OrderForm(forms.Form):
    name = forms.CharField(max_length=25)
    phone = forms.CharField(max_length=11)
    address = forms.CharField(widget=forms.Textarea)

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if len(phone) >11:
            raise forms.ValidationError('phone must be 11')
        elif len(phone)<11:
            raise forms.ValidationError('The phone number must not be less than 11 digits.')
        if  not phone.isdigit():
            raise forms.ValidationError('phone must contain only number')
        return phone

    def clean_name(self):
        name = self.cleaned_data['name']
        if any(char.isdigit() for char in  name):
            raise forms.ValidationError('The name must be of type string.')
        return name
