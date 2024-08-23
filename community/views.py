from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework import status
from .models import Community
from .serializers import CommunitySerializer
from comments.serializers import CommentSerializer 
from comments.models import Comment
from auths.models import User
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.pagination import PageNumberPagination


from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView

class CommunityAPIView(GenericAPIView, 
                       CreateModelMixin, 
                       RetrieveModelMixin, 
                       UpdateModelMixin, 
                       DestroyModelMixin, 
                       ListModelMixin):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer

    def get_user_from_token(self, request):
        """Helper method to extract user from JWT token"""
        auth_header = request.headers.get('Authorization')
        if auth_header:
            _, token = auth_header.split()
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            return User.objects.get(pk=user_id)
        return None

    def post(self, request, *args, **kwargs):

        # Community 생성 로직
        user = self.get_user_from_token(request)
        if user:
            serializer = CommunitySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user_id=user)
                return Response({
                    'status': 'success',
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)
        return Response({"message": "Authorization header missing or invalid"}, status=status.HTTP_401_UNAUTHORIZED)

    def patch(self, request, *args, **kwargs):
        user = self.get_user_from_token(request)
        if user:
            community = self.get_object()
            if community.user_id == user:
                response = self.partial_update(request, *args, **kwargs)
                return Response({
                    'status': 'success',
                    'data': response.data
                }, status=status.HTTP_200_OK)
            return Response({"message": "Permission denied. Only the post owner can update the post."}, status=status.HTTP_403_FORBIDDEN)
        return Response({"message": "Authorization header missing or invalid"}, status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, *args, **kwargs):
        user = self.get_user_from_token(request)
        if user:
            community = self.get_object()
            if community.user_id == user:
                serializer = CommunitySerializer(community, data=request.data)
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
            return Response({"message": "Permission denied. Only the post owner can update the post."}, status=status.HTTP_403_FORBIDDEN)
        return Response({"message": "Authorization header missing or invalid"}, status=status.HTTP_401_UNAUTHORIZED)
    
    def delete(self, request, *args, **kwargs):
        user = self.get_user_from_token(request)
        if user:
            community = self.get_object()
            if community.user_id == user:
                self.perform_destroy(community)
                return Response({
                    'status': 'success',
                    'message': 'Community post deleted successfully'
                }, status=status.HTTP_204_NO_CONTENT)
            return Response({"message": "Permission denied. Only the post owner can delete the post."}, status=status.HTTP_403_FORBIDDEN)
        return Response({"message": "Authorization header missing or invalid"}, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            community = self.get_object()
            serializer = CommunitySerializer(community)
            
            comments = Comment.objects.filter(community_id=community.id)
            comment_serializer = CommentSerializer(comments, many=True)
            return Response({
                'status': 'success',
                'data': serializer.data,
                'comments': comment_serializer.data
            }, status=status.HTTP_200_OK)

        category = request.query_params.get('category')
        order = request.query_params.get('order')

        queryset = Community.objects.all().order_by('-created_at')

        if category:
            queryset = queryset.filter(category__icontains=category)
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
                "user_id": community['user_id'],
                "category": community['category'],
            } for community in serializer.data
        ]
        return paginator.get_paginated_response({
            "status": 200,
            "message": "커뮤니티 조회 완료.",
            "data": serialized_data
        })
    
    
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
