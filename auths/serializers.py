from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from auths.models import *
from django.core.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'phonenum', 'email']
    
    def create(self, validated_data):
        #create 함수를 작성하여 입력받은 유저 데이터 저장 처리
        email = validated_data['email']

        # 이메일 도메인 검증
        allowed_domains = ('@ewha.ac.kr', '@sogang.ac.kr', '@hongik.ac.kr', '@yonsei.ac.kr')
        if not email.endswith(allowed_domains):
            raise serializers.ValidationError("회원가입은 학교 도메인 이메일만 가능합니다.")
        
        # 유저 생성 및 저장
        user = User.objects.create(
            phonenum=validated_data['phonenum'], #전달받은 데이터 그대로 저장
            username=validated_data['username'],
            email=email,
        )
        user.set_password(validated_data['password']) #암호화한 후 저장
        user.save()
        return user
    

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=64)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data): #입력받은 데이터의 유효성을 검증
        username=data.get('username', None)
        password=data.get('password', None)

        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)

            if not user.check_password(password):
                raise serializers.ValidationError('잘못된 비밀번호입니다.')
            else:
                token = RefreshToken.for_user(user)
                refresh = str(token)
                access = str(token.access_token)

                data = {
                    'id': user.id,
                    'username': user.username,
                    'access_token': access
                }
                return data      
        else:
            raise serializers.ValidationError('존재하지않는 유저입니다.')  