from django import forms
from .models import Feedback
from django.core.exceptions import ValidationError

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        exclude = ["first_name","last_name",'user', 'submitted_at']  # Exclude fields that are set in the view (user, submitted_at)

        widgets = {
           
             'subjects': forms.TextInput(attrs={
                'class': 'form-control',
                'required': 'required',
                'placeholder': 'Enter subject'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select',
                'required': 'required'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'required': 'required',
                'placeholder': 'Provide more details about the issue'
            }),
            'rating': forms.Select(attrs={
                'class': 'form-select',
                'required': 'required'
            }),
            'usefulness_rating': forms.Select(attrs={
                'class': 'form-select',
                'required': 'required'
            }),
            'screenshot': forms.ClearableFileInput(attrs={
                'class': 'form-control-file',
                'accept': 'image/*'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # You can add dynamic changes to fields here if needed
        self.fields['category'].choices = [
            ('suggestion', 'Suggestion'),
            ('complaint', 'Complaint'),
            ('praise', 'Praise'),
            ('other', 'Other'),
        ]
        
    def clean(self):
        cleaned_data = super().clean()
        subject = cleaned_data.get('subject')
        message = cleaned_data.get('message')

        if not subject or not message:
            raise ValidationError("Both subject and message are required.")

        return cleaned_data
