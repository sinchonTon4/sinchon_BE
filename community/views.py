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
        if 'communityId' in kwargs:
            user = self.get_user_from_token(request)
            if user:
                communityId = kwargs.get('communityId')
                community = Community.objects.get(pk=communityId)
                serializer = CommentSerializer(data=request.data)
                if serializer.is_valid():
                    comment = Comment.objects.create(
                        user_id=user,
                        community_id=community,
                        description=serializer.validated_data['description'],
                        like=serializer.validated_data['like']
                    )
                    return Response({
                        "status": 201,
                        "message": "댓글 작성 완료.",
                        "data": {
                            "comment_id": comment.id
                        }    
                    }, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "Authorization header missing or invalid"}, status=status.HTTP_401_UNAUTHORIZED)

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
        response = self.list(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'data': response.data
        }, status=status.HTTP_200_OK)
    
