

from django.core.paginator import Paginator
from django.views import View
from .models import Feedback
from atheletes.models import Users
from django.shortcuts import render, redirect
from django.contrib import messages








# class FeedbackListView(View):
#     def get(self, request,*args,**kwargs):
#         # Fetch all feedback entries and order them by the submission date
#         feedback_list = Feedback.objects.all().order_by('-submitted_at')
        
#         # Paginate the feedback list (10 per page)
#         paginator = Paginator(feedback_list, 10)  # Show 10 feedbacks per page
#         page_number = request.GET.get('page')  # Get the page number from the URL
#         page_obj = paginator.get_page(page_number)
        
#         # Render the feedback list with pagination
#         return render(request, 'feedbacks/feedback-list.html', {'feedbacks': page_obj})
from django.views import View
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Feedback
from datetime import datetime
from django.views import View
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Feedback

class FeedbackListView(View):
    def get(self, request):
        role_filter = request.GET.get('role', '').strip()
        date_filter = request.GET.get('date', '').strip()

        feedbacks = Feedback.objects.all().order_by('-submitted_at')

        # Apply filters only if values are present
        if role_filter:
            feedbacks = feedbacks.filter(user__role__iexact=role_filter)

        if date_filter:
            feedbacks = feedbacks.filter(submitted_at__date=date_filter)

        paginator = Paginator(feedbacks, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'feedbacks/feedback-list.html', {
            'feedbacks': page_obj,
            'selected_role': role_filter,
            'selected_date': date_filter,
        })

from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Feedback
from atheletes.models import Users

class FeedbackView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'feedbacks/feedback.html')

    def post(self, request, *args, **kwargs):
        subject = request.POST.get('subjects')
        category = request.POST.get('category')
        message = request.POST.get('message')
        rating = request.POST.get('rating') or None
        usefulness_rating = request.POST.get('usefulness_rating') or None
        screenshot = request.FILES.get('screenshot')

        try:
            user_profile = Users.objects.get(profile=request.user)
        except Users.DoesNotExist:
            messages.error(request, "User profile not found.")
            return redirect('feedback')  # or wherever the form is

        Feedback.objects.create(
            user=request.user,
            name=user_profile,  # ForeignKey to Users
            subjects=subject,
            category=category,
            message=message,
            rating=rating,
            usefulness_rating=usefulness_rating,
            screenshot=screenshot
        )

        messages.success(request, "Feedback submitted successfully!")
        return redirect('tnku')  # Redirect to thank-you page



class FeedbackSuccessView(View):
    def get(self, request,*args,**kwargs):
       
        return render(request, 'feedbacks/feedback-success.html')
