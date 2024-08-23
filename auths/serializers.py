from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from auths.models import *
from django.core.exceptions import ValidationError


def get_allowed_domains(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        domain_map = {}
        for line in file:
            # 학교 이름과 도메인을 분리
            parts = line.strip().split()
            if len(parts) > 1:
                univname = " ".join(parts[:-1])  # 학교 이름
                domain = parts[-1]  # 도메인 부분
                domain_map[domain] = univname
    return domain_map

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'phonenum', 'email', 'univname']
    
    def create(self, validated_data):
        email = validated_data['email']
        file_path = r"auths\univname.txt"  # 또는 "auths\\univname.txt"
        
        # 도메인과 학교 이름 매핑 정보 가져오기
        domain_map = get_allowed_domains(file_path)
        
        # 이메일 도메인 검증
        domain = email.split('@')[-1]  # 이메일의 도메인 부분 추출
        if domain not in domain_map:
            raise serializers.ValidationError("회원가입은 학교 도메인 이메일만 가능합니다.")
        
        univname = domain_map[domain]  # 해당 도메인에 대한 학교 이름
        
        # 유저 생성 및 저장
        user = User.objects.create(
            phonenum=validated_data['phonenum'],
            username=validated_data['username'],
            email=email,
            univname=univname  # 학교 이름 설정
        )
        user.set_password(validated_data['password'])  # 암호화한 후 저장
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