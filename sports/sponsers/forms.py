# forms.py

from django import forms
from .models import SponsorCompany,SponsorshipRequest,STATUS_CHOICES


class SponsorCompanyForm(forms.ModelForm):
    class Meta:
        model = SponsorCompany
        exclude = ['status', 'created_at', 'updated_at','sponsor']  # Exclude unnecessary fields
        widgets = {
            'company_name': forms.TextInput(attrs={'style': 'width:100%; padding:10px; margin-bottom:15px;'}),
            'company_email': forms.EmailInput(attrs={'style': 'width:100%; padding:10px; margin-bottom:15px;'}),
            'company_phone': forms.TextInput(attrs={'style': 'width:100%; padding:10px; margin-bottom:15px;'}),
            'company_address': forms.Textarea(attrs={'style': 'width:100%; padding:10px; margin-bottom:15px;', 'rows':3}),
            'location': forms.TextInput(attrs={'style': 'width:100%; padding:10px; margin-bottom:15px;'}),
            'website': forms.URLInput(attrs={'style': 'width:100%; padding:10px; margin-bottom:15px;'}),
            'description': forms.Textarea(attrs={'style': 'width:100%; padding:10px; margin-bottom:15px;', 'rows':4}),
            'logo': forms.ClearableFileInput(attrs={'style': 'margin-bottom:15px;'}),
        }


# from django import forms
# from .models import SponsorshipRequest

# class SponsorshipRequestForm(forms.ModelForm):
#     class Meta:
#         model = SponsorshipRequest
#         fields = ['message']
#         widgets = {
#             'message': forms.TextInput(attrs={'style': 'width:100%; padding:10px; margin-bottom:15px;','rows':4})}

    

    