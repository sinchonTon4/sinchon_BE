from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework import status
from .models import Community
from .serializers import CommunitySerializer

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
            response = self.retrieve(request, *args, **kwargs)
            return Response({
                'status': 'success',
                'data': response.data
            }, status=status.HTTP_200_OK)
        response = self.list(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'data': response.data
        }, status=status.HTTP_200_OK)

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