from django.urls import path
from . import views

urlpatterns = [

    path('', views.login_view, name='login'),
    path('dashboard/', views.user_dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),

    path('dashboard/clients/', views.clients, name='clients'),
    path('dashboard/add-client/', views.add_client, name='add_client'),

    path('dashboard/invoices',views.invoices, name='invoices'),
    path('dashboard/invoices/create',views.createInvoice, name='create-invoice'),
    path('dashboard/invoices/create-build/<slug:slug>',views.createBuildInvoice, name='create-build-invoice'),


    path('dashboard/products',views.products, name='products'),
    
    # path('client/<slug:slug>/', views.view_client, name='client-detail'),
    # path('client/<slug:slug>/edit/', views.edit_client, name='edit_client'),
]