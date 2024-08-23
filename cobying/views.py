from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Cobying
from .serializers import CobyingSerializer

class CobyingCreateView(APIView):
    def post(self, request, *args, **kwargs):
        # 요청 데이터를 CobyingSerializer를 사용해 역직렬화(deserialize)
        serializer = CobyingSerializer(data=request.data)
        
        # 데이터 검증
        if serializer.is_valid():
            # 데이터가 유효한 경우 새로운 Cobying 인스턴스를 저장
            serializer.save()
            # 생성된 객체와 상태 코드 201을 포함한 성공 응답 반환
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # 데이터가 유효하지 않은 경우 오류 응답 반환
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
