from django.urls import path
from . import views
from .views import logout_view

urlpatterns = [
    path('logout/', logout_view, name='logout'),
    path('', views.login_view, name='index'),
]