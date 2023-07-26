"""
URL configuration for project project.

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
from django.urls import path ,include
from tickets import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
router = DefaultRouter()
router.register('guest',views.viewsets_Guest)
router.register('movie',views.viewsets_Movie)
router.register('Reservation',views.viewsets_Reservation)

urlpatterns = [
    path('admin/', admin.site.urls),

    #1
    path('django/JsonResponse',views.no_rest_on_models),
    
    #2
    path('django/no_rest_from_models',views.no_rest_from_models),
    
    #3.1 GET POST form Rest Framework funciton based view @api_view
    path('django/FBV_LIST',views.FBV_LIST),

    #3.2 GET PUT DELETE form Rest Framework funciton based view @api_view
    path('django/FBV_FBV_pk/<int:pk>',views.FBV_pk),

    #4.1 GET POST form Rest Framework class based view @api_view
    path('django/CBV_List',views.CBV_List.as_view()),

    #4.2 GET PUT DELETE form Rest Framework class based view @api_view
    path('django/CBV_PK/<int:pk>',views.CBV_PK.as_view()),

    #5.1 GET POST form Rest Framework class based view Mixnis
    path('django/MixnisList',views.MixnisList.as_view()),

    #5.2 GET PUT DELETE form Rest Framework class based view Mixnis
    path('django/Mixnis_Pk/<int:pk>',views.Mixnis_Pk.as_view()),

    #6.1 GET POST form Rest Framework class based view Generics
    path('django/Generics_List',views.Generics_List.as_view()),
    path('django/Generics_pk/<int:pk>',views.Generics_pk.as_view()),

    #6.2 GET and POST GET_Pk PUT DELETE form Rest Framework class based viewsets
    path('django/viewsets_',include(router.urls)),
    path('django/viewsets_',include(router.urls)),
    path('django/viewsets_',include(router.urls)),

    #8 findMovie 
    path('fbv/find_movie',views.find_movie),

    # 9 new reservatoins
    path('fbv/newreservation',views.newreservations),

    #10 rest auth urls
    path('api-auth',include('rest_framework.urls')),

    
    #11 Token authentications 
    path('api-token-auth',obtain_auth_token),

    #12  Post pk generices Post_pk
    path('post/generices/<int:pk>',views.Post_pk.as_view()),
]
