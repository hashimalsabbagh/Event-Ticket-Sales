"""
URL configuration for eventsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', include('main.urls')),
    path('', views.home, name = 'home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logoutt, name='logout'),
    path('events/', views.viewEvents, name='viewEvents'),
    path('buy/<int:id>/', views.buyTickets, name='buyTickets'),
    path("reservations/", views.viewReservations, name="viewReservations"),
    path("delete/<int:id>", views.cancelReservation, name="cancelReservation"),
    path("wallet/", views.viewWallet, name="viewWallet"),
    path('addWallet/', views.addWallet, name='addWallet'),
    path('cancellations/', views.manageCancellation, name='manageCancellation'),
    path('cancellations/approve/<int:id>/', views.approve_cancellation, name='approve_cancellation'),
    path('cancellations/reject/<int:id>/', views.reject_cancellation, name='reject_cancellation'),
    
]
