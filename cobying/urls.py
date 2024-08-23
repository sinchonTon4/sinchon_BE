from django.urls import path
from .views import CobyingCreateView, CobyingListView, CobyingDetail, CountAdd, TagDetail

urlpatterns = [
    path('create/', CobyingCreateView.as_view()),
    path('', CobyingListView.as_view()),
    path('<int:pk>/', CobyingDetail.as_view()),
    path('<int:pk>/count/', CountAdd.as_view()),
    path('tag/<int:pk>/', TagDetail.as_view()),
]