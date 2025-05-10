

from django.db import transaction
from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from .models import SportsEvent
from .forms import SportsEventForm  # create this form
from django.db.models import Q

from .utility import get_registration_number

class SportsEventView(View):

    def get(self, request, *args, **kwargs):

        events = SportsEvent.objects.all()

        return render(request,'events/event.html',{'events': events})
    


class EventList(View):
    def get(self, request, *args, **kwargs):
        search_query = request.GET.get('search', '')
        events = SportsEvent.objects.all()

        if search_query:
            events = events.filter(
                Q(title__icontains=search_query) |
                Q(sport_type__icontains=search_query) |
                Q(venue__icontains=search_query) |
                Q(district__icontains=search_query)|
                Q(reg_number__icontains=search_query)|
                Q(sport_type__icontains=search_query)
            )

        return render(request, 'events/event-list.html', {
            'events': events,
            'search_query': search_query
        })
    
class SportsEventRegisteredView(View):

    def get(self, request, *args, **kwargs):
        form = SportsEventForm()
        return render(request, 'events/event-register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = SportsEventForm(request.POST, request.FILES)

        if form.is_valid():
            with transaction.atomic():
                event = form.save(commit=False)
                event.reg_number = get_registration_number()
                event.save()
                
                return redirect('success')
            
        return render(request, "events/event-register.html", {'form': form})


class SportsEventUpdateView(View):

    def get(self, request, pk, *args, **kwargs):

        event = get_object_or_404(SportsEvent, pk=pk)

        form = SportsEventForm(instance=event)

        return render(request, 'events/event-update.html', {'form': form})

    def post(self, request, pk, *args, **kwargs):

        event = get_object_or_404(SportsEvent, pk=pk)

        form = SportsEventForm(request.POST, request.FILES, instance=event)

        if form.is_valid():

            form.save()

            return redirect('event')
        
        return render(request, 'events/event-update.html', {'form': form})


class SportsEventDeleteView(View):

    def get(self, request, pk, *args, **kwargs):

        event = get_object_or_404(SportsEvent, pk=pk)

        event.delete()

        return redirect('event')

       
