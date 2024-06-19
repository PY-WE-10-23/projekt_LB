from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Event, Registration
from .forms import UserRegisterForm, EventForm, RegistrationForm
from django.contrib import messages
from django.contrib.auth.models import User


def index(request):
    return render(request, 'base.html')


@login_required
def add_event(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'add_event.html', {'form': form})


@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'edit_event.html', {'form': form, 'event': event})

@login_required
def remove_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == "POST":
        event.delete()
        return redirect('event_list')
    return render(request, 'remove_event.html', {'event': event})

@login_required
def register_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.event = event
            registration.user = request.user
            registration.save()
            return redirect('event_list')
    else:
        form = RegistrationForm()
    return render(request, 'register_event.html', {'form': form, 'event': event})


def event_list(request):
    #events = Event.objects.all()
    #for event in events:
    #    event.remaining_slots = event.available_slots - event.registration_set.count()
    #return render(request, 'event_list.html', {'events': events})

    events = Event.objects.all()
    registrations = Registration.objects.select_related('user', 'event').all()
    event_registrations = {}
    for registration in registrations:
        if registration.event.id not in event_registrations:
            event_registrations[registration.event.id] = []
        event_registrations[registration.event.id].append(registration.user)

    # Filtry
    user_id = request.GET.get('user_id')
    if user_id:
        events = events.filter(registration__user_id=user_id)
        print(events)

    date_sort = request.GET.get('date_sort')
    if date_sort == 'asc':
        events = events.order_by('date')
    elif date_sort == 'desc':
        events = events.order_by('-date')

    slots_sort = request.GET.get('slots_sort')
    if slots_sort == 'asc':
        events = events.order_by('available_slots')
    elif slots_sort == 'desc':
        events = events.order_by('-available_slots')

    total_slots = request.GET.get('total_slots')
    if total_slots:
        events = events.filter(available_slots__gte=int(total_slots))

    # Přidání dostupných slotů do aktivit

    for event in events:
        event.registered_count = len(event_registrations.get(event.id, []))
        #event.available_count = event.available_slots - event.registered_count
        event.remaining_slots = event.available_slots - event.registration_set.count()


    context = {
        'events': events,
        'event_registrations': event_registrations,
        'user_list': User.objects.all()
    }

    return render(request, 'event_list.html', context)




def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'members/register.html', {'form': form})

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def about(request):
    return render(request, 'About.html')
@login_required
def profile(request):
    return render(request, 'members/profile.html')