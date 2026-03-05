from django.urls import path
from . import views # Import views to connect routes to view functions

urlpatterns = [
    path('', views.order_view, name='order'),
    path('kitchen/', views.kitchen_view, name='kitchen'),
]
