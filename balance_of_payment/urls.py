"""
URL configuration for balance_of_payment project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from revenue import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("transactions/all/",views.TransactionListView.as_view(),name="transaction-list"),
    path("transactions/add/",views.TransactionCreateView.as_view(),name="transaction-add"),
    path("transactions/<int:pk>/",views.TransactionDetailView.as_view(),name="transaction-detail"),
    path("transactions/<int:pk>/remove/",views.TransactionDeleteView.as_view(),name="transaction-delete"),
    path("transactions/<int:pk>/change/",views.TransactionEditView.as_view(),name="transaction-edit"),
    path("signup/",views.SignUpView.as_view(),name="signup"),
    path("signin/",views.SignInView.as_view(),name="signin"),
    
]