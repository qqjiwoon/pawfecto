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
# 2-0) 인스타로 로그인
# ============================================
def instagram_callback(request):
    # 리디렉션 URI에서 받은 인증 코드
    code = request.GET.get('code')
    if not code:
        return JsonResponse({'error': 'Code missing'}, status=400)

    # 액세스 토큰 요청
    url = "https://api.instagram.com/oauth/access_token"
    data = {
        'client_id': 'YOUR_CLIENT_ID',  # Instagram 앱의 client_id
        'client_secret': 'YOUR_CLIENT_SECRET',  # Instagram 앱의 client_secret
        'grant_type': 'authorization_code',
        'redirect_uri': 'https://localhost:5500/callback/instagram',  # 리디렉션 URI
        'code': code  # 인증 코드
    }

    response = requests.post(url, data=data)
    if response.status_code == 200:
        access_token_data = response.json()  # 액세스 토큰 데이터
        access_token = access_token_data.get('access_token')
        user_id = access_token_data.get('user_id')

        # 액세스 토큰으로 사용자 정보 요청
        user_data_url = f"https://graph.instagram.com/{user_id}?fields=id,username&access_token={access_token}"
        user_data_response = requests.get(user_data_url)

        if user_data_response.status_code == 200:
            user_data = user_data_response.json()  # 사용자 데이터
            return JsonResponse(user_data)
        else:
            return JsonResponse({'error': 'Failed to get user data'}, status=400)
    else:
        return JsonResponse({'error': 'Failed to get access token'}, status=400)


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
        f"http://localhost:5173/reset-password?"
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
