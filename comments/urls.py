from django.urls import path
from .views import CommentList, CommentDetail

urlpatterns = [
    path('<int:communityId>/', CommentList.as_view()),
    path('<int:pk>/', CommentDetail.as_view()),
]