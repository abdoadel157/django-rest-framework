"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from tickets import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
router =DefaultRouter()
router.register('guests',views.viewsets_guest)
router.register('movies',views.viewsets_movie)
router.register('reservation',views.viewsets_reservaton)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('django/jsonresponsenomodel/', views.no_rest_no_model),
    path('secondway/', views.no_rest_from_model),
    path('thirdway/', views.FBV_List),
    path('thirdway/<int:pk>',views.FBV_pk),
    path('fourway/',views.CBV_List.as_view()),
    path('fourway/<int:pk>',views.CBV_pk.as_view()),
    path('fiveway/',views.Mixins_List.as_view()),
    path('fiveway/<int:pk>', views.mixins_pk.as_view()),
    path('sixway/',views.generics_list.as_view()),
    path('sixway/<int:pk>',views.generics_pk.as_view()),
    path('rest/viewsets/',include(router.urls)),
    path('search_movie/',views.search_movie),
    path('create_reservation/',views.create_reservation),
    path('api-auth',include('rest_framework.urls')),
    path('api/',obtain_auth_token),
    path('post/generics/<int:pk>',views.Post_Pk.as_view())

]
