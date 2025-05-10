from django import forms
from .models import SportsEvent,SPORT_CHOICES,DistrictChoices

class SportsEventForm(forms.ModelForm):
    class Meta:
        model = SportsEvent
        exclude = ['reg_number']
        widgets = {
           
            'title': forms.TextInput(attrs={'class':'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
                                                        'placeholder':'Enter first name',
                                                        'required':'required'}),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'style': 'padding: 12px; width: 100%; border: 1px solid #ccc; border-radius: 6px; background: #f9f9f9; box-shadow: inset 0 1px 3px rgba(0,0,0,0.06); font-size: 14px; resize: vertical;'
            }),

            'image' :forms.FileInput(attrs={'class':'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
                                                         }),   




            'date': forms.DateInput(attrs={
                                  'type': 'date','class':'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
                                 'placeholder':'Enter date',
                                 'required':'required'
                                          }),
            'time': forms.TimeInput(attrs={'type': 'time','class':'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
                                           'placeholder':'Enter time',
                                            'required':'required'}),

            'venue': forms.TextInput(attrs={'class':'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
                                                        'placeholder':'Enter first name',
                                                        'required':'required'})
            
               }
        sport_type = forms.ChoiceField(choices=SPORT_CHOICES.choices,widget=forms.Select(attrs={'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 form-select focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray',
        'required': 'required'
        }))
        district= forms.ChoiceField(choices=DistrictChoices.choices,widget=forms.Select(attrs={'class':'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 form-select focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray',
                                                                                            'required':'required'}))
    













