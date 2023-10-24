"""
URL configuration for drinks project.

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
from django.urls import path
from drinks import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('drinks/', views.drink_list),
    path('drinks/<int:id>', views.drink_detail),
    path('target/', views.target_list),
    path('target/<int:id>', views.target_detail),
    path('target/list/', views.TargetListView.as_view()),
    path('flight/', views.flight_list),
    path('flight/<int:id>', views.flight_detail),
    path('flight/list/', views.FlightListView.as_view()),
    path('ff/', views.invokeFF),
    path('signup/', views.signup),
]

# the following line allow url input in browser as http...drink.json which will result in json format response
urlpatterns = format_suffix_patterns(urlpatterns)
