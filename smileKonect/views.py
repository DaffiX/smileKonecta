
from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from uuid import uuid4
from .forms import *
from .models import *


from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from .functions import *
from django.contrib.auth.models import User, auth
from random import randint

from django.http import HttpResponse

import pdfkit
from django.template.loader import get_template
import os

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
            messages.success(request, 'New Client Added')
            # return redirect('client-detail', slug=client.slug)
            return redirect('clients')
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


#--------------- Builder ------------

@login_required
def create_invoice(request):
    #create a blank invoice ....
    number = 'INV-'+str(uuid4()).split('-')[1]
    newInvoice = Invoice.objects.create(number=number)
    newInvoice.save()

    inv = Invoice.objects.get(number=number)
    return redirect('create-build-invoice', slug=inv.slug)


def create_build_invoice(request, slug):
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

def viewPDFInvoice(request, slug):
    #fetch that invoice
    try:
        invoice = Invoice.objects.get(slug=slug)
        pass
    except:
        messages.error(request, 'Something went wrong')
        return redirect('invoices')

    #fetch all the products - related to this invoice
    products = Product.objects.filter(invoice=invoice)

    #Get Client Settings
    p_settings = Setting.objects.get(clientName='Smile Connect')

    #Calculate the Invoice Total
    invoiceCurrency = ''
    invoiceTotal = 0.0
    if len(products) > 0:
        for x in products:
            y = float(x.quantity) * float(x.price)
            invoiceTotal += y
            invoiceCurrency = x.currency



    context = {}
    context['invoice'] = invoice
    context['products'] = products
    context['p_settings'] = p_settings
    context['invoiceTotal'] = "{:.2f}".format(invoiceTotal)
    context['invoiceCurrency'] = invoiceCurrency

    return render(request, 'smile/invoice-template.html', context)



def viewDocumentInvoice(request, slug):
    #fetch that invoice
    try:
        invoice = Invoice.objects.get(slug=slug)
        pass
    except:
        messages.error(request, 'Something went wrong')
        return redirect('invoices')

    #fetch all the products - related to this invoice
    products = Product.objects.filter(invoice=invoice)

    #Get Client Settings
    p_settings = Setting.objects.get(clientName='Smile Connect')

    #Calculate the Invoice Total
    subtotal = 0.00
    if len(products) > 0:
        for x in products:
            subtotal = float(x.quantity) * float(x.price)

    invoiceTotal = 0.0
    if len(products) > 0:
        for x in products:
            y = float(x.quantity) * float(x.price)
            invoiceTotal += y



    context = {}
    context['invoice'] = invoice
    context['products'] = products
    context['p_settings'] = p_settings
    context['subtotal'] = "{:.2f}".format(subtotal)
    context['invoiceTotal'] = "{:.2f}".format(invoiceTotal)

    #The name of your PDF file
    filename = '{}.pdf'.format(invoice.uniqueId)

    #HTML FIle to be converted to PDF - inside your Django directory
    template = get_template('smile/pdf-template.html')


    #Render the HTML
    html = template.render(context)

    #Options - Very Important [Don't forget this]
    options = {
          'encoding': 'UTF-8',
          'javascript-delay':'10', #Optional
          'enable-local-file-access': None, #To be able to access CSS
          'page-size': 'A4',
          'custom-header' : [
              ('Accept-Encoding', 'gzip')
          ],
      }
      #Javascript delay is optional

    #Remember that location to wkhtmltopdf
    config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')

    #IF you have CSS to add to template
    # css1 = os.path.join(settings.CSS_LOCATION, 'smile', 'css', 'bootstrap.min.css')
    # css2 = os.path.join(settings.CSS_LOCATION, 'smile', 'css', 'dashboard.css')

    #Create the file
    file_content = pdfkit.from_string(html, False, configuration=config, options=options)

    #Create the HTTP Response
    response = HttpResponse(file_content, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename = {}'.format(filename)

    #Return
    return response


def emailDocumentInvoice(request, slug):
    #fetch that invoice
    try:
        invoice = Invoice.objects.get(slug=slug)
        pass
    except:
        messages.error(request, 'Something went wrong')
        return redirect('invoices')

    #fetch all the products - related to this invoice
    products = Product.objects.filter(invoice=invoice)

    #Get Client Settings
    p_settings = Setting.objects.get(clientName='Smile Connect')

    #Calculate the Invoice Total
    invoiceTotal = 0.0
    if len(products) > 0:
        for x in products:
            y = float(x.quantity) * float(x.price)
            invoiceTotal += y



    context = {}
    context['invoice'] = invoice
    context['products'] = products
    context['p_settings'] = p_settings
    context['invoiceTotal'] = "{:.2f}".format(invoiceTotal)

    #The name of your PDF file
    filename = '{}.pdf'.format(invoice.uniqueId)

    #HTML FIle to be converted to PDF - inside your Django directory
    template = get_template('smile/pdf-template.html')


    #Render the HTML
    html = template.render(context)

    #Options - Very Important [Don't forget this]
    options = {
          'encoding': 'UTF-8',
          'javascript-delay':'1000', #Optional
          'enable-local-file-access': None, #To be able to access CSS
          'page-size': 'A4',
          'custom-header' : [
              ('Accept-Encoding', 'gzip')
          ],
      }
      #Javascript delay is optional

    #Remember that location to wkhtmltopdf
    config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')

    #Saving the File
    filepath = os.path.join(settings.MEDIA_ROOT, 'client_invoices')
    os.makedirs(filepath, exist_ok=True)
    pdf_save_path = filepath+filename
    #Save the PDF
    pdfkit.from_string(html, pdf_save_path, configuration=config, options=options)


    #send the emails to client
    to_email = invoice.client.emailAddress
    from_client = p_settings.clientName
    emailInvoiceClient(to_email, from_client, pdf_save_path)

    invoice.status = 'EMAIL_SENT'
    invoice.save()

    #Email was send, redirect back to view - invoice
    messages.success(request, "Email sent to the client succesfully")
    return redirect('create-build-invoice', slug=slug)


def deleteInvoice(request, slug):
    try:
        Invoice.objects.get(slug=slug).delete()
        messages.success(request, "Sucessfull deleted")
    except:
        messages.error(request, 'Mhhh! Somthing went wrong')
        return redirect('invoices')

    return redirect('invoices')


def companySettings(request):
    company = Setting.objects.get(clientName='Smile Connect')
    context = {'company': company}
    return render(request, 'smile/company-settings.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')
