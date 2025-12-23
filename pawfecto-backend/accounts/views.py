from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status

import requests
from django.http import JsonResponse

from django.contrib.auth import authenticate, logout, get_user_model
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from myproject.utils import upload_to_gcs

from django.conf import settings
from accounts.models import User

from django.views.decorators.csrf import csrf_exempt

import json


from .serializers import (
    UserSerializer,
    BrandSerializer,
    CreatorSerializer,
    StyleTagSerializer
)


User = get_user_model()
token_generator = PasswordResetTokenGenerator()

# ============================================
# 1) 회원가입
# ============================================
@api_view(['POST'])
def signup(request):
    account_type = request.data.get("account_type")

    if account_type == "brand":
        serializer = BrandSerializer(data=request.data)
    elif account_type == "creator":
        serializer = CreatorSerializer(data=request.data)
    else:
        return Response({"error": "Invalid account_type"}, status=400)

    if serializer.is_valid():
        user = serializer.save()
        return Response(
            {"message": "signup success", "user": UserSerializer(user).data},
            status=201
        )

    return Response(serializer.errors, status=400)


# ============================================
# 2) 로그인 (JWT)
# ============================================
@api_view(['POST'])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response(
            {"error": "username and password are required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(username=username, password=password)

    if user is None:
        return Response(
            {"error": "Invalid username or password"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    # JWT 토큰 발급
    refresh = RefreshToken.for_user(user)

    if user.account_type == "brand":
        user_data = BrandSerializer(user).data
    else:
        user_data = CreatorSerializer(user).data

    return Response(
        {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": user_data,
        },
        status=status.HTTP_200_OK
    )



# ============================================
# 2-0) 인스타그램 정보 연동
# ============================================
@csrf_exempt
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])  # 로그인된 유저만 접근 가능
def instagram_callback(request):
    """
    프론트엔드에서 전달받은 code로 인스타그램 Access Token을 발급받고,
    유저 정보를 조회하여 현재 로그인된 유저(request.user)의 프로필을 업데이트합니다.
    """
    
    # [수정 1] DRF에서는 request.data로 접근
    auth_code = request.data.get('code')
    
    # 프론트엔드 주소 (기본값 설정)
    redirect_uri = request.data.get('redirect_uri', "https://localhost:5173/callback/instagram")

    if not auth_code:
        return Response({'error': 'Code가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)

    # ------------------------------------------------------------------
    # [3단계] Access Token 요청
    # 주소: https://api.instagram.com/oauth/access_token
    # ------------------------------------------------------------------
    token_url = "https://api.instagram.com/oauth/access_token"
    
    payload = {
        'client_id': settings.INSTAGRAM_CLIENT_ID,
        'client_secret': settings.INSTAGRAM_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'redirect_uri': redirect_uri,
        'code': auth_code
    }
    
    try:
        # POST 요청 (form-data 형식으로 전송됨)
        token_res = requests.post(token_url, data=payload)
        token_res.raise_for_status()  # 200 OK가 아니면 예외 발생
    except requests.exceptions.RequestException as e:
        # 인스타그램 에러 메시지 확인용
        error_detail = token_res.json() if token_res.content else str(e)
        return Response({
            'error': '토큰 발급 실패', 
            'details': error_detail
        }, status=status.HTTP_400_BAD_REQUEST)
    
    access_token = token_res.json().get('access_token')

    # ------------------------------------------------------------------
    # [4단계] 유저 정보 요청
    # 주소: https://graph.instagram.com/v24.0/me
    # ------------------------------------------------------------------
    fields = "user_id,username,profile_picture_url,followers_count,follows_count,media_count"
    user_info_url = f"https://graph.instagram.com/v24.0/me?fields={fields}&access_token={access_token}"
    
    try:
        user_res = requests.get(user_info_url)
        user_res.raise_for_status()
    except requests.exceptions.RequestException as e:
        return Response({
            'error': '유저 정보 조회 실패',
            'details': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
    
    insta_data = user_res.json()

    # ------------------------------------------------------------------
    # [5단계] 정보 업데이트 로직
    # ------------------------------------------------------------------
    
    # API 버전에 따라 id 필드명이 다를 수 있어 안전하게 가져오기
    insta_id = insta_data.get('id') or insta_data.get('user_id')
    username = insta_data.get('username')
    profile_url = insta_data.get('profile_picture_url')
    followers = insta_data.get('followers_count', 0)
    following = insta_data.get('follows_count', 0)
    media_count = insta_data.get('media_count', 0)
    
    sns_url = f"https://www.instagram.com/{username}/"

    # [수정 2] 로그인된 유저 본인 객체 (JWT Authentication 통해 식별됨)
    user = request.user 

    # [수정 3] 모델 필드 업데이트
    user.instagram_id = insta_id  # DB 모델에 이 필드가 있어야 함
    user.sns_handle = username
    user.profile_image_url = profile_url
    user.follower_count = followers
    user.following_count = following
    user.total_post_count = media_count
    user.sns_url = sns_url

    # [수정 4] 변경된 필드만 DB에 저장 (최적화)
    user.save(update_fields=[
        'instagram_id',
        'sns_handle', 
        'profile_image_url', 
        'follower_count', 
        'following_count', 
        'total_post_count', 
        'sns_url'
    ])
            
    return Response({
        "message": "인스타그램 정보가 성공적으로 연동되었습니다.",
        "username": user.username,
        "instagram_username": username,
        "is_created": False 
    }, status=status.HTTP_200_OK)



# ============================================
# 2-1) 아이디  찾기
# ============================================
@api_view(['POST'])
def find_id(request):
    email = request.data.get("email")

    if not email:
        return Response(
            {"error": "email is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.filter(email=email).first()

    if not user:
        return Response(
            {"error": "user not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    username = user.username

    # 아이디 마스킹 (앞 3글자 + *** + 뒤 2글자)
    if len(username) <= 5:
        masked = username[0] + "***"
    else:
        masked = username[:3] + "***" + username[-2:]

    return Response(
        {"username_hint": masked},
        status=status.HTTP_200_OK
    )

# ============================================
# 2-2) 패스워드 찾기
# ============================================
@api_view(['POST'])
def password_reset(request):
    username = request.data.get("username")
    email = request.data.get("email")

    if not username or not email:
        return Response(
            {"error": "username and email are required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.filter(username=username, email=email).first()

    if not user:
        return Response(
            {"error": "user not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    # uid + token 생성
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = token_generator.make_token(user)

    # 프론트 ResetPasswordView 주소
    reset_link = (
        f"https://localhost:5173/reset-password?"
        f"uid={uid}&token={token}"
    )
    return Response(
        {"message": "password reset email sent"},
        status=status.HTTP_200_OK
    )

# ============================================
# 3) 로그아웃
# ============================================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)
    return Response({"message": "logout success"}, status=status.HTTP_200_OK)


# ============================================
# 4) 내 정보 조회 / 수정
# ============================================
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def me(request):
    user = request.user

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data, status=200)

    elif request.method == 'PUT':
        # partial=True로 일부 필드만 받아도 되게 설정
        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            # 1. 시리얼라이저를 통해 먼저 기본 정보를 저장 (이때 모델의 save()가 호출됨)
            # 픽클 에러를 방지하기 위해 instance를 직접 넘겨받음
            updated_user = serializer.save()

            # 2. 만약 요청에 비밀번호가 포함되어 있다면 별도로 암호화 처리
            password = request.data.get('password')
            if password:
                updated_user.set_password(password)
                updated_user.save()

            # 3. 최신 정보를 다시 시리얼라이즈하여 응답
            # 저장 후 새로고침된 데이터를 반환하여 픽클 에러가 난 객체와의 연결을 끊음
            final_serializer = UserSerializer(updated_user)
            return Response(final_serializer.data, status=200)

        return Response(serializer.errors, status=400)


# ============================================
# 5) 브랜드 프로필 조회
# ============================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def brand_profile(request, brand_id):
    user = get_object_or_404(User, id=brand_id, account_type="brand")
    serializer = UserSerializer(user)
    return Response(serializer.data, status=200)


# ============================================
# 6) 크리에이터 프로필 조회
# ============================================
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def creator_profile(request, creator_id):
    user = get_object_or_404(User, id=creator_id, account_type="creator")
    serializer = UserSerializer(user)
    return Response(serializer.data, status=200)


# ============================================
# 7) 프로필 수정
# ============================================
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user

    data = request.data.copy()
    data.pop("account_type", None)
    data.pop("profile_image", None)

    password = data.get("password")
    image = request.FILES.get("profile_image")

    serializer = UserSerializer(user, data=data, partial=True)

    if serializer.is_valid():
        user = serializer.save()

        # 비밀번호 처리
        if password:
            if isinstance(password, list):
                password = password[0]
            user.set_password(str(password))
            user.save(update_fields=["password"])

        # 프로필 이미지 처리 (storages가 GCS로 자동 업로드)
        if image:
            user.profile_image.save(image.name, image, save=True)

        return Response(
            {"message": "profile updated", "user": serializer.data},
            status=200
        )

    return Response(serializer.errors, status=400)



# ============================================
# 8) 크리에이터 스타일 태그 수정
# ============================================
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_style_tags(request, creator_id):

    if request.user.id != creator_id:
        return Response({"error": "본인만 수정할 수 있습니다."}, status=403)

    user = get_object_or_404(User, id=creator_id, account_type="creator")
    style_tag_ids = request.data.get("style_tags", [])

    if not isinstance(style_tag_ids, list):
        return Response(
            {"error": "style_tags must be a list of IDs"},
            status=400
        )

    if not style_tag_ids:
        from myapp.models import StyleTag
        no_pref = get_object_or_404(StyleTag, code="no_preference")
        style_tag_ids = [no_pref.id]

    user.style_tags.set(style_tag_ids)

    return Response(
        {
            "message": "style tags updated",
            "style_tags": StyleTagSerializer(
                user.style_tags.all(),
                many=True
            ).data
        },
        status=200
    )
