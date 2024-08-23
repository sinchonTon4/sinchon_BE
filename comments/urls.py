from django.urls import path
from .views import CommentList, CommentDetail, CommentLikeAdd

urlpatterns = [
    path('<int:communityId>/', CommentList.as_view()),
    path('detail/<int:pk>/', CommentDetail.as_view()),
    path('detail/<int:pk>/like', CommentLikeAdd.as_view()),
]