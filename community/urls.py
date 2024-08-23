from django.urls import path
from .views import CommunityAPIView, CommunityLikeAdd

urlpatterns = [
    path('', CommunityAPIView.as_view(), name='community-list'),  # 전체 조회 및 새 글 작성 (GET, POST)
    path('<int:pk>/', CommunityAPIView.as_view(), name='community-detail'),  # 단일 조회, 업데이트, 삭제 (GET, PUT, PATCH, DELETE)
    path('<int:pk>/like/', CommunityLikeAdd.as_view()),
]