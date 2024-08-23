from django.urls import path
from .views import CobyingCreateView

urlpatterns = [
    path('create/', CobyingCreateView.as_view()), 

]