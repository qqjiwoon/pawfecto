import re
from rest_framework import serializers
from .models import User
from myapp.models import StyleTag     
from django.contrib.auth import get_user_model

User = get_user_model()


# -----------------------------------------------------------
# StyleTag Serializer (읽기용)
# -----------------------------------------------------------
class StyleTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = StyleTag
        fields = ['id', 'code', 'name']



# -----------------------------------------------------------
# BRAND 회원가입 Serializer
# -----------------------------------------------------------
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'email',
            'name',
            'phone_number',
            'pet_type',
            'profile_image_url',
            'account_type',
        ]
        extra_kwargs = {
            'password': {'write_only': True},  # 비밀번호는 쓰기 전용
        }

    # 1. 아이디(username) 중복 검사
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("이미 사용 중인 아이디입니다.")
        return value

    # 2. 이메일 형식 및 중복 검사
    def validate_email(self, value):
        # 이메일 정규표현식 검사
        email_regex = r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, value):
            raise serializers.ValidationError("올바른 이메일 형식이 아닙니다.")
        
        # 중복 검사
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("이미 등록된 이메일 주소입니다.")
        return value

    # 3. 비밀번호 형식 검사 (8자 이상, 영문+숫자 포함)
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("비밀번호는 최소 8자 이상이어야 합니다.")
        
        if not re.search(r'[A-Za-z]', value) or not re.search(r'\d', value):
            raise serializers.ValidationError("비밀번호는 영문자와 숫자를 포함해야 합니다.")
        
        return value

    # 4. 전체 데이터 검증 (기존 로직 유지)
    def validate(self, data):
        # 계정 타입 확인
        if data.get("account_type") != "brand":
            raise serializers.ValidationError({"account_type": "이 Serializer는 브랜드 계정 전용입니다."})

        # 필수 필드 누락 검사 (기존 로직 반영)
        required_fields = ['username', 'password', 'email', 'name', 'phone_number']
        for field in required_fields:
            if not data.get(field):
                raise serializers.ValidationError({field: f"{field} 필드는 필수 입력 항목입니다."})

        return data

    # 5. 데이터 저장 (비밀번호 해싱 처리)
    def create(self, validated_data):
        # create_user를 사용해야 비밀번호가 암호화되어 DB에 저장됩니다.
        user = User.objects.create_user(**validated_data)
        return user



# -----------------------------------------------------------
# CREATOR 회원가입 Serializer
# -----------------------------------------------------------
import re
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import StyleTag  # 프로젝트 구조에 맞게 import 확인

User = get_user_model()

class CreatorSerializer(serializers.ModelSerializer):
    # style_tags는 ID 배열로 받도록 설정 (M2M 관계)
    style_tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=StyleTag.objects.all(),
        required=False
    )

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'email',
            'name',
            'sns_handle',
            'sns_url',
            'address',
            'style_tags',
            'account_type',
            'pet_type',
            'profile_image_url',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    # 1. 아이디(username) 중복 검사
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("이미 사용 중인 아이디입니다.")
        return value

    # 2. 이메일 형식 및 중복 검사
    def validate_email(self, value):
        email_regex = r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, value):
            raise serializers.ValidationError("올바른 이메일 형식이 아닙니다.")
        
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("이미 등록된 이메일 주소입니다.")
        return value

    # 3. 비밀번호 형식 검사 (8자 이상, 영문+숫자 포함)
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("비밀번호는 최소 8자 이상이어야 합니다.")
        
        if not re.search(r'[A-Za-z]', value) or not re.search(r'\d', value):
            raise serializers.ValidationError("비밀번호는 영문자와 숫자를 포함해야 합니다.")
        return value

    # 4. 전체 데이터 유효성 검사 (계정 타입 및 필수값)
    def validate(self, data):
        # 계정 타입 확인
        if data.get("account_type") != "creator":
            raise serializers.ValidationError({"account_type": "이 Serializer는 크리에이터 계정 전용입니다."})

        # 크리에이터 필수 필드 검사
        required_fields = ['username', 'password', 'email', 'name', 'sns_handle', 'sns_url', 'address']
        for field in required_fields:
            if not data.get(field):
                raise serializers.ValidationError({field: f"{field} 필드는 필수 입력 항목입니다."})

        return data

    # 5. 데이터 저장 로직
    def create(self, validated_data):
        # M2M 필드인 style_tags 분리
        style_tags = validated_data.pop("style_tags", [])

        # 비밀번호 해싱을 위해 create_user 사용
        user = User.objects.create_user(**validated_data)

        # 선택된 태그가 없으면 'no_preference' 적용
        if not style_tags:
            try:
                no_pref = StyleTag.objects.get(code="no_preference")
                style_tags = [no_pref]
            except StyleTag.DoesNotExist:
                # DB에 no_preference 태그가 없을 경우를 대비한 방어 코드
                pass

        # M2M 관계(StyleTag) 저장
        if style_tags:
            user.style_tags.set(style_tags)

        return user



# -----------------------------------------------------------
# 기본 UserSerializer (읽기 전용 뷰 등에서 사용)
# -----------------------------------------------------------
class UserSerializer(serializers.ModelSerializer):
    # 조회용
    style_tags = StyleTagSerializer(many=True, read_only=True)

    # 수정용 (code 배열 받기)
    style_tag_codes = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False
    )

    profile_image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = '__all__'

    def update(self, instance, validated_data):
        # 비밀번호 처리
        password = validated_data.pop("password", None)

        if isinstance(password, list) and len(password) > 0:
            password = password[0]

        if password:
            instance.set_password(str(password))

        # 스타일 태그 code 배열 처리
        style_tag_codes = validated_data.pop("style_tag_codes", None)

        # 이미지 및 태그
        profile_image = validated_data.pop("profile_image", None)

        # 일반 필드 업데이트
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # 비밀번호 변경
        if password:
            instance.set_password(password)

        # 4. 이미지 파일 처리 및 URL 동기화 (500 에러 주요 구간)
        if profile_image:
            instance.profile_image = profile_image
            instance.save() # 파일을 먼저 저장해야 URL이 생성됨
            try:
                # 저장된 파일의 경로를 텍스트 필드에도 복사
                instance.profile_image_url = instance.profile_image.url
            except ValueError:
                # 파일 경로 생성 실패 시 예외 처리
                pass

        instance.save()

        # 스타일 태그 반영
        if style_tag_codes is not None:
            tags = StyleTag.objects.filter(code__in=style_tag_codes)
            instance.style_tags.set(tags)

        return instance
