from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Cobying
from .serializers import CobyingSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import get_object_or_404

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
    
class CobyingListView(APIView):
    def get(self, request, *args, **kwargs):
        product_category = request.query_params.get('category')
        order = request.query_params.get('order')

        queryset = Cobying.objects.all().order_by('-created_at')

        if product_category:
            queryset = queryset.filter(category__icontains=product_category)
        if order == 'people_num':
            queryset = queryset.order_by('-people_num')

        paginator = PageNumberPagination()
        paginator.page_size = 3
        cobyings = paginator.paginate_queryset(queryset, request)
        serializer = CobyingSerializer(cobyings, many=True)

        serialized_data = [
            {
                "id": cobying['id'],
                "title": cobying['title'],
                "description": cobying['description'],
                "img": cobying['img'],
                "tag": cobying['tag'],
                "price": cobying['price'],
                "product_name": cobying['product_name'],
                "link": cobying['link'],
                "people_num": cobying['people_num'],
                "product_category": cobying['product_category'],
                "created_at": cobying['created_at'],
            } for cobying in serializer.data
        ]

        return paginator.get_paginated_response({
            "status": 200,
            "message": "공동구매 조회 완료.",
            "data": serialized_data
        })


class CobyingDetail(APIView):
    def get_object(request, pk):
        cobying = get_object_or_404(Cobying, pk=pk)
        return cobying

    def get(self, request, pk):
        cobying = self.get_object(pk)
        serializer = CobyingSerializer(cobying)
        return Response(serializer.data)
    

class CountAdd(APIView):
    def get_object(request, pk):
        cobying = get_object_or_404(Cobying, pk=pk)
        return cobying
    
    def patch(self, request, pk):
        cobying = self.get_object(pk)
        cobying.count += 1
        cobying.save()

        return Response({
            "status": 200,
            "message": "참여하기 완료.",
            "data": {
                "cobying": cobying.id,
                "count": cobying.count,
            }
        }, status=status.HTTP_200_OK)