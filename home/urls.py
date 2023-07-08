"""MediTracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path,include
from home import views

urlpatterns = [
    path('',views.home,name='home'),
    path('feedback',views.feedbackk,name='feedbackk'),
    path('login',views.loginn,name='login'),
    path('signup',views.signup,name='signup'),
    path('fagin',views.fakd_login,name='fake'),
    path('logout',views.logoutt,name='logoutt'),
    path('addmedd',views.addmed,name='logoutt'),
    path('viewdoses',views.viewdos,name='viewdoses'),
    path('edit/<int:sno>',views.edit,name='edit'),
    path('update/<int:sno>',views.update,name='update'),
    path('delete/<int:sno>',views.delete,name='delete'),
    path('verify/<auth_token>',views.verify,name='verify'),
    
]