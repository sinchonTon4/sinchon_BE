from django.urls import path
from .views import CommunityAPIView

urlpatterns = [
    path('community/', CommunityAPIView.as_view(), name='community-list'),  # 전체 조회 및 새 글 작성 (GET, POST)
    path('community/<int:pk>/', CommunityAPIView.as_view(), name='community-detail'),  # 단일 조회, 업데이트, 삭제 (GET, PUT, PATCH, DELETE)
]