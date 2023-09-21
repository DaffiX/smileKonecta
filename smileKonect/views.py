from django.shortcuts import get_list_or_404
from django.shortcuts import render, redirect 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm

from .models import Client
from .forms import ClientForm
# Create your views here.


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Change this URL to your custom user dashboard URL
    else:
        form = LoginForm()
    return render(request, 'smile/getin.html', {'form': form})



# @login_required  # This decorator ensures only authenticated users can access this view
# def user_dashboard(request):
#     # Add logic to display user-specific dashboard content here
#     return render(request, 'smile/dashboard.html')

@login_required
def user_dashboard(request):
    # The user object is available in the context due to the @login_required decorator
    # You can access user-related information like username, full name, etc.
    username = request.user.username
    full_name = request.user.get_full_name()

    # Add any other logic to display user-specific dashboard content here

    return render(request, 'smile/dashboard.html', {'username': username, 'full_name': full_name})

# def clients(request):
#     clients = Client.objects.all()
#     return render(request, 'smile/clients.html', {'clients': clients})

@login_required
def clients(request):
    context = {}
    clients = Client.objects.all()
    context['clients'] = clients

    if request.method == 'GET':
        form = ClientForm()
        context['form'] = form
        return render(request, 'smile/clients.html', context)

    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

            messages.success(request, 'New Client Added')
            return redirect('clients')
        else:
            messages.error(request, 'Problem processing your request')
            return redirect('clients')


    return render(request, 'smile/clients.html', context)

def add_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES)
        if form.is_valid():
            client = form.save()
            return redirect('client-detail', slug=client.slug)
    else:
        form = ClientForm()
    return render(request, 'smile/add_client.html', {'form': form})



def view_client(request, slug):
    client = get_object_or_404(Client, slug=slug)
    return render(request, 'view_client.html', {'client': client})

def edit_client(request, slug):
    client = get_object_or_404(Client, slug=slug)
    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client-detail', slug=client.slug)
    else:
        form = ClientForm(instance=client)
    return render(request, 'edit_client.html', {'form': form, 'client': client})


def logout_view(request):
    logout(request)
    return redirect('login')
