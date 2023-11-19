from django.urls import path
from . import views


urlpatterns = [
    path('',views.home,name='homepage'),
    path('register/',views.registration_view,name = 'registration vieew'),
    path('login/',views.login,name = 'login view'),
    path('logout/',views.logout,name = 'logout view'),
    path('profile/',views.profile,name = 'profile page'),
]