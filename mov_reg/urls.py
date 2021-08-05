"""Movement_Register URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import HomeView,MovDetailView,AddMovView_Empty,AddMovView_Initial,UpdateMovView,DeleteMovView
urlpatterns = [
path('',views.index,name="index"),
path('home',HomeView.as_view(),name="home"),
path('movement/<int:pk>',MovDetailView.as_view(),name="mov_details"),
path('add_mov_init',AddMovView_Initial.as_view(),name="add_mov_init"),
path('add_mov_empty',AddMovView_Empty.as_view(),name="add_mov_empty"),
path('movement/edit/<int:pk>',UpdateMovView.as_view(),name="update_mov"),
path('movement/<int:pk>/delete/',DeleteMovView.as_view(),name="delete_mov"),
path('filter',views.FilterView,name="filter"),
path('veh_list',views.VehicleView,name="veh_list"),
path('veh_details/<str:veh_no>',views.VehicleDetailView,name="veh_details"),
path('vehicle',views.Vehicle,name="vehicle"),
path('upload',views.FileUpload,name="upload"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
