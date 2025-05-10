from django import forms
from .models import ProfileDetails, Gender
from atheletes.models import DistrictChoices


class EventRegistrationForm(forms.ModelForm):
    class Meta:
        model = ProfileDetails
        exclude = ['registration_fee', 'student', 'category','created_at','updated_at','active_status','uuid']  # 👈 Add 'student' and 'category' here since they are set in view

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'required': 'required'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'required': 'required'
            }),
            'dob': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-input',
                'placeholder': 'Select date of birth',
                'required': 'required'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'required': 'required'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter address',
                'required': 'required'
            }),
            'pincode': forms.TextInput(attrs={
                'class': 'form-control',
                'required': 'required'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'required': 'required'
            }),
            'institution': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter institution',
                'required': 'required'
            }),
            'university': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter university',
                'required': 'required'
            }),
            'reg_number': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter student ID',
                'required': 'required'
            }),
            'Id_proof': forms.FileInput(attrs={
                'class': 'form-input'
            }),
        }

    gender = forms.ChoiceField(
        choices=Gender.choices,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'required': 'required'
        })
    )

    student_district = forms.ChoiceField(
        choices=DistrictChoices.choices,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'required': 'required'
        })
    )

    institution_districts = forms.ChoiceField(
        choices=DistrictChoices.choices,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'required': 'required'
        })
    ) 

    def clean(self):
        cleaned_data  =super().clean()

        pincode = cleaned_data.get('pincode')

        email= cleaned_data.get('email')

        

        if len(pincode)<6:
            self.add_error('pincode','pincode must be six digit')

        return cleaned_data
    
    def __init__(self, *args,**kwargs): 

        super(EventRegistrationForm,self).__init__(*args,**kwargs)

        if not self.instance:

            self.fields.get('Id_proof').widget.attrs['required']='required'

    
    
               