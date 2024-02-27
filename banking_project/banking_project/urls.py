"""
URL configuration for banking_project project.

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
from django.urls import path,include
# from transactions.views import create_transaction, get_transactions

# from banking_app.views import LoginView
from rest_framework.decorators import action
from rest_framework.response import Response




urlpatterns = [
    path('admin/', admin.site.urls),
    path("",include('banking_app.urls')),
     path('api/create-transaction/', create_transaction, name='create_transaction'),
    path('api/get-transactions/', get_transactions, name='get_transactions'),
    # path('login/token/', LoginView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
  
]
