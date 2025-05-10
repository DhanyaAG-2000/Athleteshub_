


# class RegistrationView(View):

#     def get(self, request, *args, **kwargs):

#         form = UsersRegisterForm()

#         return render(request, 'atheletes/registration.html', {'form': form})
    

#     def post(self, request, *args, **kwargs):

#         form = UsersRegisterForm(request.POST, request.FILES)

#         if form.is_valid():

#             with transaction.atomic():

#                 user = form.save(commit=False)

#                 user.reg_number = get_registration_number()

#                 username = user.email

#                 password = get_password()

#                 role=user.rolechoice

#                 print("the role is:",role)

#                 # Create user profile

#                 profile = Profile.objects.create_user(username=username, password=password,role=role)

#                 user.profile = profile

#                 user.save()


#                 # Sending login credentials via email

#                 subject = 'Your Password for Sports Management'

#                 recipients = [user.email]

#                 template = 'emails/login-credential.html'  # Ensure this file exists

#                 context = {'name': f'{user.first_name} {user.last_name}', "username": username, "password": password,"role":role}
                

#                 try:
#                     send_email(subject, recipients, template, context)

#                 except Exception as e:
                    
#                     print(f"Error sending email: {e}")  # Debugging purpose

#                 return redirect('user-management')

#         return render(request, "atheletes/registration.html", {'form': form})













