from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from .models import Comment
from .serializers import CommentSerializer
from auths.models import User
from communities.models import Community

class CommentList(APIView):
    def get(self, request, communityId):
        community = Community.objects.get(pk=communityId)
        comments = Comment.objects.filter(community_id=community)
        serializer = CommentSerializer(comments, many=True)
        serialized_data = [
            {
                "comment_id": comment['id'],
                "user_id": comment['user_id'],
                "community_id": comment['community_id'],
                "description": comment['description'],
                "like": comment['like'],
                "createdAt": comment['created_at']
            } for comment in serializer.data
        ]
        return Response({
            "status": 200,
            "message": "댓글 조회 완료.",
            "data": {
                "Comments": serialized_data
            }
        })
    
    def post(self, request, communityId):
        auth_header = request.headers.get('Authorization')
        _, token = auth_header.split()
        access_token = AccessToken(token)
        user_id = access_token['user_id']

        user = User.objects.get(pk=user_id)
        community = Community.objects.get(pk=communityId)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            comment = Comment.objects.create(
                user_id = user,
                community_id = community,
                description = serializer.validated_data['description'],
                like = serializer.validated_data['like']
            )
            return Response({
                "status": 201,
                "message": "댓글 작성 완료.",
                "data": {
                    "comment_id": comment.id
                }    
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetail(APIView):
    def get_object(request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        return comment

    # 상세 댓글 조회
    def get(self, request, pk):
        comment = Comment.objects.get(pk)
        serializer = CommentSerializer(comment)
        return Response({
            "status": 200,
            "message": "상세 댓글 조회 완료.",
            "data": {
                "comment": {
                    "comment_id": serializer.data['id'],
                    "user_id": serializer.data['user_id'],
                    "community_id": serializer.data['community_id'],
                    "description": serializer.data['description'],
                    "like": serializer.data['like'],
                    "createdAt": serializer.data['createdAt']
                }
            }    
        }, status=status.HTTP_200_OK)

    # 댓글 수정
    def patch(self, request, pk):
        auth_header = request.headers.get('Authorization')
        _, token = auth_header.split()
        access_token = AccessToken(token)
        user_id = access_token['user_id']

        user = User.objects.get(pk=user_id)
        comment = self.get_object(pk)

        if comment.user_id == user:
            serializer = CommentSerializer(comment, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({
                    "status": 200,
                    "message": "댓글 수정 완료.",
                    "data": {
                        "comment": {
                            "comment_id": serializer.data['id'],
                            "user_id": serializer.data['user_id'],
                            "community_id": serializer.data['community_id'],
                            "description": serializer.data['description'],
                            "like": serializer.data['like'],
                            "createdAt": serializer.data['createdAt']
                        }
                    }    
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "status": 403,
                "message": "해당 반려동물 수정 권한이 없습니다."
            }, status=status.HTTP_403_FORBIDDEN)
    
    # 댓글 삭제
    def delete(self, request, pk):
        auth_header = request.headers.get('Authorization')
        _, token = auth_header.split()
        access_token = AccessToken(token)
        user_id = access_token['user_id']

        user = User.objects.get(pk=user_id)
        comment = self.get_object(pk)

        if comment.user_id == user:
            comment.delete()
            return Response({
                "status": 200,
                "message": "댓글 삭제 완료.",
                "data": {}    
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "status": 403,
                "message": "해당 댓글 삭제 권한이 없습니다."
            }, status=status.HTTP_403_FORBIDDEN)
        