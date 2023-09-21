from django.shortcuts import get_list_or_404
from django.shortcuts import render, redirect 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from uuid import uuid4
from .forms import *
from .models import *

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
    
    # username = request.user.username
    # full_name = request.user.get_full_name()

    # Add any other logic to display user-specific dashboard content here

    return render(request, 'smile/dashboard.html')

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

@login_required
def invoices(request):
    msimbo = {}
    invoices = Invoice.objects.all()
    msimbo['invoices'] = invoices

    return render(request, 'smile/invoices.html', msimbo)


@login_required
def products(request):
    context = {}
    products = Product.objects.all()
    context['products'] = products

    return render(request, 'smile/products.html', context)

# def view_client(request, slug):
#     client = get_object_or_404(Client, slug=slug)
#     return render(request, 'view_client.html', {'client': client})

# def edit_client(request, slug):
#     client = get_object_or_404(Client, slug=slug)
#     if request.method == 'POST':
#         form = ClientForm(request.POST, request.FILES, instance=client)
#         if form.is_valid():
#             form.save()
#             return redirect('client-detail', slug=client.slug)
#     else:
#         form = ClientForm(instance=client)
#     return render(request, 'edit_client.html', {'form': form, 'client': client})
#--------------- Builder ------------

@login_required
def createInvoice(request):
    #create a blank invoice ....
    number = 'INV-'+str(uuid4()).split('-')[1]
    newInvoice = Invoice.objects.create(number=number)
    newInvoice.save()

    inv = Invoice.objects.get(number=number)
    return redirect('create-build-invoice', slug=inv.slug)




def createBuildInvoice(request, slug):
    #fetch that invoice
    try:
        invoice = Invoice.objects.get(slug=slug)
        pass
    except:
        messages.error(request, 'Something went wrong')
        return redirect('invoices')

    #fetch all the products - related to this invoice
    products = Product.objects.filter(invoice=invoice)


    context = {}
    context['invoice'] = invoice
    context['products'] = products

    if request.method == 'GET':
        prod_form  = ProductForm()
        inv_form = InvoiceForm(instance=invoice)
        client_form = ClientSelectForm(initial_client=invoice.client)
        context['prod_form'] = prod_form
        context['inv_form'] = inv_form
        context['client_form'] = client_form
        return render(request, 'smile/create-invoice.html', context)

    if request.method == 'POST':
        prod_form  = ProductForm(request.POST)
        inv_form = InvoiceForm(request.POST, instance=invoice)
        client_form = ClientSelectForm(request.POST, initial_client=invoice.client, instance=invoice)

        if prod_form.is_valid():
            obj = prod_form.save(commit=False)
            obj.invoice = invoice
            obj.save()

            messages.success(request, "Invoice product added succesfully")
            return redirect('create-build-invoice', slug=slug)
        elif inv_form.is_valid and 'paymentTerms' in request.POST:
            inv_form.save()

            messages.success(request, "Invoice updated succesfully")
            return redirect('create-build-invoice', slug=slug)
        elif client_form.is_valid() and 'client' in request.POST:

            client_form.save()
            messages.success(request, "Client added to invoice succesfully")
            return redirect('create-build-invoice', slug=slug)
        else:
            context['prod_form'] = prod_form
            context['inv_form'] = inv_form
            context['client_form'] = client_form
            messages.error(request,"Problem processing your request")
            return render(request, 'smile/create-invoice.html', context)


    return render(request, 'smile/create-invoice.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')
