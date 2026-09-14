from django import forms

class OrderForm(forms.Form):
    name = forms.CharField(max_length=25)
    phone = forms.CharField(max_length=11)
    address = forms.CharField(max_length=250)

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if len(phone) > 11:
            raise forms.ValidationError('number phone max 11')
        elif not phone.isdigit():
            raise forms.ValidationError('phone should digit')
        elif len(phone) <10:
            raise forms.ValidationError('phone not 10')
        return phone
