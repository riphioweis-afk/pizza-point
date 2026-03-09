from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('order/', views.order_view, name='order'),
    path('kitchen/', views.kitchen_view, name='kitchen'),
    path('logout/', views.logout_view, name='logout'),
    path('secret/', views.secret_view, name='secret'),
]