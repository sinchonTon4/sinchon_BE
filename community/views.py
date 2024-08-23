from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework import status
from .models import Community
from .serializers import CommunitySerializer
from comments.serializers import CommentSerializer 
from comments.models import Comment
from rest_framework.permissions import IsAuthenticated

from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

class CommunityAPIView(GenericAPIView, 
                       CreateModelMixin, 
                       RetrieveModelMixin, 
                       UpdateModelMixin, 
                       DestroyModelMixin, 
                       ListModelMixin):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer

    def post(self, request, *args, **kwargs):
        response = self.create(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'data': response.data
        }, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            community = self.get_object()
            serializer = CommunitySerializer(community)
            
            comments = Comment.objects.filter(community_id=community.id)
            comment_serializer = CommentSerializer(comments, many=True)
            return Response({
                'status': 'success',
                'data': serializer.data,
                'comments': comment_serializer.data  # 관련된 댓글들을 응답에 포함
            }, status=status.HTTP_200_OK)
        
        cobying = request.query_params.get('cobying')
        community = request.query_params.get('community')
        order = request.query_params.get('order')
        
        queryset = Community.objects.all().order_by('-created_at')
        if cobying:
            queryset = queryset.filter(city__icontains=cobying)
        if community:
            queryset = queryset.filter(category__icontains=community)
        if order == 'like':
            queryset = queryset.order_by('-like')

        paginator = PageNumberPagination()
        paginator.page_size = 3
        communities = paginator.paginate_queryset(queryset, request)
        serializer = CommunitySerializer(communities, many=True)

        serialized_data = [
            {
                "id": community['id'],
                "title": community['title'],
                "description": community['description'],
                "img": community['img'],
                "like": community['like'],
                "user_id": community['user_id']    
            } for community in serializer.data
        ]
        return paginator.get_paginated_response({
            "status": 200,
            "message": "커뮤니티 조회 완료.",
            "data": serialized_data
        })

    def patch(self, request, *args, **kwargs):
        response = self.partial_update(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'data': response.data
        }, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        post_id = kwargs.get('pk')
        post = self.get_object()
        serializer = CommunitySerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            'status': 'error',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Community post deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)
    
class CommunityLikeAdd(APIView):
    def get_object(request, pk):
        community = get_object_or_404(Community, pk=pk)
        return community
    
    def patch(self, request, pk):
        community = self.get_object(pk)
        community.like += 1
        community.save()

        return Response({
            "status": 200,
            "message": "댓글 LIKE 추가 완료.",
            "data": {
                "community_id": community.id,
                "like": community.like
            }
        }, status=status.HTTP_200_OK)