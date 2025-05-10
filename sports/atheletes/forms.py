
from django import forms 
from .models import Users,DistrictChoices,Rolechoice

class UsersRegisterForm(forms.ModelForm):


    class Meta:

        model =Users


        exclude = ['active_status','uuid','profile','reg_number','join_date','last_login' ]

        widgets = {
            
                'first_name' :forms.TextInput(attrs={'class':'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
                                                        'placeholder':'Enter first name',
                                                        'required':'required'}),
                'last_name' :forms.TextInput(attrs={'class':'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
                                                        'placeholder':'Enter second name',
                                                        'required':'required'}),
                'photo' :forms.FileInput(attrs={'class':'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
                                                         }),
                'email' :forms.EmailInput(attrs={'class':'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
                                                        'placeholder':'Enter email',
                                                        'required':'required'}),
                'contact_num' :forms.TextInput(attrs={'class':'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
                                                        'placeholder':'Enter phone number',
                                                        'required':'required'}),
                'house_name' :forms.TextInput(attrs={'class':'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
                                                        'placeholder':'Enter house name',
                                                        'required':'required'}),
                'post_office' :forms.TextInput(attrs={'class':'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
                                                        'placeholder':'Enter post office',
                                                        'required':'required'}),
                'pincode' :forms.TextInput(attrs={'class':'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
                                                        'placeholder':'Enter pincode',
                                                        'required':'required'}),
                # 'join_date' :forms.DateInput(attrs={   'type':'date',
                #                                      'class':'block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input',
                #                                         'required':'required'}),
                                                      }
        

    district= forms.ChoiceField(choices=DistrictChoices.choices,widget=forms.Select(attrs={'class':'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 form-select focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray',
                                                                                            'required':'required'}))
    
    rolechoice= forms.ChoiceField(choices=Rolechoice.choices,widget=forms.Select(attrs={'class':'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 form-select focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray',
                                                                                            'required':'required'}))
    # batch = forms.ChoiceField(choices=Batch.choices,widget=forms.Select(attrs={'class':'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 form-select focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray',
    #                                                                                         'required':'required'}))

    def clean(self):
        
        cleaned_data  =super().clean()

        pincode = cleaned_data.get('pincode')



        if len(pincode)<6:
            self.add_error('pincode','pincode must be six digit')

        return cleaned_data
    
    def __init__(self, *args,**kwargs): 

        super(UsersRegisterForm,self).__init__(*args,**kwargs)

        if not self.instance:

            self.fields.get('photo').widget.attrs['required']='required'

    
    
               