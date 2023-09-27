from django.urls import path
from . import views

urlpatterns = [

    path('', views.login_view, name='login'),
    path('dashboard/', views.user_dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),

    path('dashboard/clients/', views.clients, name='clients'),
    path('dashboard/add-client/', views.add_client, name='add_client'),

    path('dashboard/invoices',views.invoices, name='invoices'),
    path('dashboard/invoices/create',views.create_invoice, name='create-invoice'),
    path('dashboard/invoices/create-build/<slug:slug>',views.create_build_invoice, name='create-build-invoice'),

    #Delete an invoice
path('invoices/delete/<slug:slug>',views.deleteInvoice, name='delete-invoice'),

#PDF and EMAIL Paths
path('invoices/view-pdf/<slug:slug>',views.viewPDFInvoice, name='view-pdf-invoice'),
path('invoices/view-document/<slug:slug>',views.viewDocumentInvoice, name='view-document-invoice'),
path('invoices/email-document/<slug:slug>',views.emailDocumentInvoice, name='email-document-invoice'),

    path('dashboard/products',views.products, name='products'),
    

    #Company Settings Page
path('company/settings',views.companySettings, name='company-settings'),
]