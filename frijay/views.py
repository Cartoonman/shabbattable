'''Views for the frijay app'''
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from frijay.models import Event, Reservation
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Event
from django.template import loader
from frijay.forms import UserForm, UserProfileForm


def index(request):
    '''index page view'''
    context_dict = {'title': "Frijay!"}
    return render(request, 'frijay/index.html', context_dict)


def about(request):
    '''about page view'''
    context_dict = {'title': "About!"}

    return render(request, 'frijay/about.html', context_dict)

def signup(request):
    '''signup page view'''
    # A boolean value for telling the template
    # whether the registration was successful.
    # Set to False initially. Code changes value to
    # True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of only the UserForm
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms is valid...
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves,
            # we set commit=False. This delays saving the model
            # until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and
            # put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

             # Update our variable to indicate that the template
             # registration was successful.
            registered = True

        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            print(user_form.errors, profile_form.errors)
    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances. # These forms will be blank, ready for user input.
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request, 'frijay/signup.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})


def user_login(request):
    '''login page view'''
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        # We use request.POST.get('<variable>') as opposed
        # to request.POST['<variable>'], because the
        # request.POST.get('<variable>') returns None if the
        # value does not exist, while request.POST['<variable>'] # will raise a KeyError exception.
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Use Django's machinery to attempt to see if the username/password # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)
        # If we have a User object, the details are correct.
        # If None, no user # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in. # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
            # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
        # The request is not a HTTP POST, so display the login form. # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the # blank dictionary object...
        return render(request, 'frijay/login.html', {})

@login_required
def user_logout(request):
    # Only logout if user is already logged in
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect(reverse('index'))

def profile(request):
    '''user profile page view'''
    context_dict = {'title': "Profile"}
    return render(request, 'frijay/profile.html', context_dict)

def redir(request):
    '''redirection view'''
    return redirect('/frijay')

def events(request):
    '''Event View'''
    all_events = Event.objects.all()
    html = ''

    for event in all_events:
        url = '/frijay/events/' + str(event.id) + '/'
        html += '<a href="' + url + '">' + event.title + '</a><br>'
    context_dict = {'html_list' : html}

    return render(request, 'frijay/events.html', context_dict)

@login_required
def reservation(request):
    uid = request.user
    userobj = User.objects.get(id=int(uid.id))
    if(request.POST.get('reserve')):
        evnt = Event.objects.get(title=request.POST.get('event'))
        res = Reservation.objects.get_or_create(event=evnt, guest=userobj)[0]
        res.save()
    elif(request.POST.get('cancel')):
        evnt = Event.objects.get(title=request.POST.get('cancel'))
        Reservation.objects.get(event=evnt, guest=userobj).delete()

    context_dict = {}
    context_dict['events'] = Event.objects.all()
    reservations = Reservation.objects.filter(guest=userobj)
    context_dict['reservations'] = [x for x in reservations]
    return render(request, 'frijay/reservation.html', context_dict)

def reservationsEvent(request, event_id):
    '''Event view for specific event'''
    eventModel = Event.objects.get(id = event_id)
    context_dict = {'event_id' : event_id,
                    'event_title' : eventModel.title,
                    'event_host' : eventModel.host,
                    'event_address' : eventModel.address,
                    'event_date' : eventModel.date,
                    'event_time' : eventModel.time,
                    'event_seats' : eventModel.openSeats,
                    'event_details' : eventModel.additionalDetails
                    }
    return render(request, 'frijay/reservationEventPage.html',context_dict)
    '''Reservations view for specific event'''
    #return HttpResponse("<h2>Details for event id " + str(event_id) + "</h2>")
