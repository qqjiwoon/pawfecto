from rest_framework.decorators import api_view, permission_classes, parser_classes
from django.views.decorators.cache import never_cache
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from ai.validators import validate_ai_result, AIResultValidationError
from .services.deliverable_service import run_deliverable_ai_verification
from .ai_client import call_llm
from django.conf import settings
import json

from accounts.models import User
from accounts.serializers import CreatorSerializer

from .models import Campaign, CampaignAcceptance, Deliverable, StyleTag, DeliverableRequirement
from .serializers import (
    CampaignSerializer,
    CampaignListSerializer,
    CampaignAcceptanceSerializer,
    DeliverableSerializer,
    DeliverableCreateSerializer,
    DeliverableRequirementSerializer
)

from django.db.models import Q




# ============================================================
# 브랜드 기능
# ============================================================

# ------------------------------------------------------------
# 1) 브랜드 캠페인 목록 조회
# ------------------------------------------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def brand_campaign_list(request, brand_id):

    if request.user.account_type != "brand":
        return Response({"error": "브랜드만 접근할 수 있습니다."}, status=403)

    if request.user.id != int(brand_id):
        return Response({"error": "본인 캠페인만 조회 가능합니다."}, status=403)

    campaigns = Campaign.objects.filter(brand=request.user).order_by('-requested_at')

    serializer = CampaignListSerializer(campaigns, many=True)
    return Response(serializer.data, status=200)



# ------------------------------------------------------------
# 2) 캠페인 생성
# ------------------------------------------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def create_campaign(request, brand_id):

    if request.user.account_type != "brand":
        return Response({"error": "브랜드만 캠페인을 생성할 수 있습니다."}, status=403)

    if request.user.id != brand_id:
        return Response({"error": "본인 브랜드로만 캠페인을 생성할 수 있습니다."}, status=403)

    serializer = CampaignSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    campaign = serializer.save(brand=request.user)

    # 자동 매칭 실행
    auto_match_creators(campaign)

    return Response(serializer.data, status=201)




# ------------------------------------------------------------
# 3) 캠페인 상세 조회
# ------------------------------------------------------------
@api_view(['GET'])
@never_cache
@permission_classes([IsAuthenticated])
def campaign_detail(request, brand_id, campaign_id):

    campaign = get_object_or_404(
        Campaign,
        campaign_id=campaign_id,
        brand_id=brand_id
    )

    if campaign.brand != request.user:
        return Response({"error": "본인 캠페인만 조회할 수 있습니다."}, status=403)

    serializer = CampaignSerializer(campaign)
    return Response(serializer.data, status=200)



# ------------------------------------------------------------
# 4) 캠페인 수정
# ------------------------------------------------------------
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def update_campaign(request, brand_id, campaign_id):

    campaign = get_object_or_404(
        Campaign,
        campaign_id=campaign_id,
        brand_id=brand_id
    )

    if campaign.brand != request.user:
        return Response(
            {"error": "본인이 생성한 캠페인만 수정할 수 있습니다."},
            status=403
        )

    # 승인된 크리에이터가 있는지 확인
    has_approved_acceptance = CampaignAcceptance.objects.filter(
        campaign=campaign,
        brand_decision_status="approved"
    ).exists()

    if has_approved_acceptance:
        forbidden_fields = {
            "target_pet_type",
            "style_tags",
            "min_follower_count",
            "required_creator_count",
        }

        if forbidden_fields & set(request.data.keys()):
            return Response(
                {
                    "error": "크리에이터가 승인된 이후에는 가이드라인을 수정할 수 없습니다."
                },
                status=400
            )

    serializer = CampaignSerializer(
        campaign,
        data=request.data,
        partial=True
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()

    # 조건 변경에 따른 기존 추천 정리
    cleanup_invalid_acceptances(campaign)

    # 새 조건에 맞는 크리에이터 추가
    auto_match_creators(campaign)

    return Response(serializer.data, status=200)





# ------------------------------------------------------------
# 5) 캠페인 삭제
# ------------------------------------------------------------
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_campaign(request, brand_id, campaign_id):

    # 1. 캠페인 존재 여부 확인
    campaign = get_object_or_404(
        Campaign,
        campaign_id=campaign_id,
        brand_id=brand_id
    )

    # 2. 브랜드 본인 여부 확인
    if campaign.brand != request.user:
        return Response(
            {"error": "본인이 생성한 캠페인만 삭제할 수 있습니다."},
            status=403
        )

    # 3. 승인된 크리에이터가 하나라도 있으면 삭제 불가
    has_approved_acceptance = CampaignAcceptance.objects.filter(
        campaign=campaign,
        brand_decision_status="approved"
    ).exists()

    if has_approved_acceptance:
        return Response(
            {
                "error": "크리에이터가 연결된 캠페인은 삭제할 수 없습니다."
            },
            status=400
        )

    # 4. 삭제 실행
    campaign.delete()
    return Response({"message": "캠페인이 삭제되었습니다."}, status=204)



# ============================================================
# [브랜드] Campaign_requirement 관련
# ============================================================

# ------------------------------------------------------------
# [브랜드] 캠페인 포스팅 요구조건 목록 / 생성
# ------------------------------------------------------------
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def campaign_requirements(request, brand_id, campaign_id):

    campaign = get_object_or_404(
        Campaign,
        campaign_id=campaign_id,
        brand_id=brand_id
    )

    if campaign.brand != request.user:
        return Response({"error": "본인 캠페인만 접근할 수 있습니다."}, status=403)

    # GET: 요구조건 목록 조회
    if request.method == 'GET':
        serializer = DeliverableRequirementSerializer(
            campaign.requirements.all(),
            many=True
        )
        return Response(serializer.data, status=200)

    # POST: 요구조건 생성
    has_approved = CampaignAcceptance.objects.filter(
        campaign=campaign,
        brand_decision_status="approved"
    ).exists()

    if has_approved:
        return Response(
            {"error": "크리에이터 승인 이후에는 요구조건을 추가할 수 없습니다."},
            status=400
        )

    serializer = DeliverableRequirementSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(campaign=campaign)

    return Response(serializer.data, status=201)


# ------------------------------------------------------------
# [브랜드] 캠페인 포스팅 요구조건 수정
# ------------------------------------------------------------
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_campaign_requirement(
    request,
    brand_id,
    campaign_id,
    requirement_id
):

    campaign = get_object_or_404(
        Campaign,
        campaign_id=campaign_id,
        brand_id=brand_id
    )

    if campaign.brand != request.user:
        return Response({"error": "본인 캠페인만 접근할 수 있습니다."}, status=403)

    requirement = get_object_or_404(
        DeliverableRequirement,
        id=requirement_id,
        campaign=campaign
    )

    has_approved = CampaignAcceptance.objects.filter(
        campaign=campaign,
        brand_decision_status="approved"
    ).exists()

    if has_approved:
        return Response(
            {"error": "크리에이터 승인 이후에는 요구조건을 수정할 수 없습니다."},
            status=400
        )

    serializer = DeliverableRequirementSerializer(
        requirement,
        data=request.data,
        partial=True
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data, status=200)


# ------------------------------------------------------------
# [브랜드] 캠페인 포스팅 요구조건 삭제
# ------------------------------------------------------------
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_campaign_requirement(
    request,
    brand_id,
    campaign_id,
    requirement_id
):

    campaign = get_object_or_404(
        Campaign,
        campaign_id=campaign_id,
        brand_id=brand_id
    )

    if campaign.brand != request.user:
        return Response({"error": "본인 캠페인만 접근할 수 있습니다."}, status=403)

    requirement = get_object_or_404(
        DeliverableRequirement,
        id=requirement_id,
        campaign=campaign
    )

    has_approved = CampaignAcceptance.objects.filter(
        campaign=campaign,
        brand_decision_status="approved"
    ).exists()

    if has_approved:
        return Response(
            {"error": "크리에이터 승인 이후에는 요구조건을 삭제할 수 없습니다."},
            status=400
        )

    requirement.delete()
    return Response(status=204)



# ============================================================
# [브랜드] Campaign 진행 관련
# ============================================================

# ------------------------------------------------------------
# 1) 특정 캠페인에 대한 크리에이터 신청 현황 조회
# ------------------------------------------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def campaign_acceptance_list(request, brand_id, campaign_id):

    campaign = get_object_or_404(
        Campaign,
        campaign_id=campaign_id,
        brand_id=brand_id
    )

    if campaign.brand != request.user:
        return Response({"error": "본인 캠페인만 조회할 수 있습니다."}, status=403)

    acceptances = CampaignAcceptance.objects.filter(campaign=campaign).order_by('-applied_at')
    serializer = CampaignAcceptanceSerializer(acceptances, many=True)
    return Response(serializer.data, status=200)


# ------------------------------------------------------------
# 2) 브랜드가 추천받은 크리에이터 승인
# ------------------------------------------------------------
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def approve_creator(request, brand_id, campaign_id, acceptance_id):

    # 캠페인 확인 (본인 소유 캠페인만)
    campaign = get_object_or_404(
        Campaign,
        campaign_id=campaign_id,
        brand_id=brand_id
    )

    if campaign.brand != request.user:
        return Response({"error": "본인 캠페인만 승인할 수 있습니다."}, status=403)

    # CampaignAcceptance 조회
    acceptance = get_object_or_404(
        CampaignAcceptance,
        campaign_acceptance_id=acceptance_id,
        campaign=campaign
    )

    # 이미 처리된 경우 방어
    if acceptance.brand_decision_status != 'pending':
        return Response(
            {"error": "이미 승인 또는 거절된 크리에이터입니다."},
            status=400
        )

    # 승인 처리
    acceptance.brand_decision_status = 'approved'
    acceptance.brand_decided_at = timezone.now()
    acceptance.save()

    return Response({"message": "크리에이터를 승인했습니다."}, status=200)



# ------------------------------------------------------------
# 3) 브랜드가 크리에이터 거절
# ------------------------------------------------------------
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def reject_creator(request, brand_id, campaign_id, acceptance_id):

    # 캠페인 확인
    campaign = get_object_or_404(
        Campaign,
        campaign_id=campaign_id,
        brand_id=brand_id
    )

    if campaign.brand != request.user:
        return Response({"error": "본인 캠페인만 거절할 수 있습니다."}, status=403)

    # CampaignAcceptance 조회
    acceptance = get_object_or_404(
        CampaignAcceptance,
        campaign_acceptance_id=acceptance_id,
        campaign=campaign
    )

    # 이미 처리된 경우 방어
    if acceptance.brand_decision_status != 'pending':
        return Response(
            {"error": "이미 승인 또는 거절된 크리에이터입니다."},
            status=400
        )

    # 거절 처리
    acceptance.brand_decision_status = 'rejected'
    acceptance.brand_decided_at = timezone.now()
    acceptance.save()

    return Response({"message": "크리에이터를 거절했습니다."}, status=200)



# ------------------------------------------------------------
# 4) 캠페인 진행 상황(Deliverable) 조회
# ------------------------------------------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def campaign_progress(request, brand_id, campaign_id):

    campaign = get_object_or_404(
        Campaign,
        campaign_id=campaign_id,
        brand_id=brand_id
    )

    if campaign.brand != request.user:
        return Response({"error": "본인 캠페인만 진행 현황을 조회할 수 있습니다."}, status=403)

    deliverables = Deliverable.objects.filter(
        campaign_acceptance__campaign=campaign
    )

    serializer = DeliverableSerializer(deliverables, many=True)
    return Response(serializer.data, status=200)





# ============================================================
# 크리에이터 기능
# ============================================================

# ------------------------------------------------------------
# 7) 크리에이터 오퍼 조회 (CampaignAcceptance)
# ------------------------------------------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def creator_campaign_offers(request, creator_id):

    if request.user.account_type != "creator":
        return Response({"error": "크리에이터만 접근할 수 있습니다."}, status=403)

    if request.user.id != int(creator_id):
        return Response({"error": "본인 오퍼만 조회할 수 있습니다."}, status=403)

    offers = CampaignAcceptance.objects.filter(
        creator=request.user,
        brand_decision_status="approved"
    )

    serializer = CampaignAcceptanceSerializer(offers, many=True)
    return Response(serializer.data, status=200)


# ------------------------------------------------------------
# 캠페인 오퍼 수락
# ------------------------------------------------------------
# 캠페인 오퍼 수락 + Deliverable 자동 생성
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_offer(request, acceptance_id):

    acceptance = get_object_or_404(
        CampaignAcceptance,
        campaign_acceptance_id=acceptance_id,
        creator=request.user,
        brand_decision_status="approved"
    )

    # 1. 이미 수락한 경우
    if acceptance.acceptance_status == "accepted":
        return Response(
            {"error": "이미 수락한 오퍼입니다."},
            status=400
        )

    campaign = acceptance.campaign

    # 2. 현재 수락된 크리에이터 수
    accepted_count = CampaignAcceptance.objects.filter(
        campaign=campaign,
        acceptance_status="accepted"
    ).count()

    # 3. 정원 초과 체크
    if accepted_count >= campaign.required_creator_count:
        return Response(
            {"error": "이미 필요한 크리에이터 수가 모두 충원되었습니다."},
            status=400
        )

    # 4. 수락 처리
    acceptance.acceptance_status = "accepted"
    acceptance.accepted_at = timezone.now()
    acceptance.save()

    # 5. Deliverable 자동 생성 (중복 방지)
    Deliverable.objects.get_or_create(
        campaign_acceptance=acceptance,
        defaults={
            "content": "",
            "deliverable_status": "incomplete",
            "ai_validation_status": "pending"
        }
    )

    return Response(
        CampaignAcceptanceSerializer(acceptance).data,
        status=200
    )



# ------------------------------------------------------------
# 캠페인 오퍼 거절
# ------------------------------------------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reject_offer(request, acceptance_id):

    acceptance = get_object_or_404(
        CampaignAcceptance,
        campaign_acceptance_id=acceptance_id,
        creator=request.user,
        brand_decision_status="approved"
    )

    if acceptance.acceptance_status == "accepted":
        return Response(
            {"error": "이미 수락한 캠페인은 상태를 변경할 수 없습니다."},
            status=400
        )

    acceptance.acceptance_status = "rejected"
    acceptance.save()

    return Response(
        CampaignAcceptanceSerializer(acceptance).data,
        status=200
    )


# ------------------------------------------------------------
# 10) 크리에이터 진행 상황 조회
# ------------------------------------------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def creator_progress(request, creator_id):

    if request.user.account_type != "creator":
        return Response({"error": "크리에이터만 접근할 수 있습니다."}, status=403)

    if request.user.id != int(creator_id):
        return Response({"error": "본인 진행상황만 조회 가능합니다."}, status=403)

    deliverables = Deliverable.objects.filter(
        campaign_acceptance__creator=request.user
    )

    serializer = DeliverableSerializer(deliverables, many=True)
    return Response(serializer.data, status=200)

def creator_detail(request, creator_id):
    creator = get_object_or_404(
        User,
        id=creator_id,
        account_type="creator"
    )
    serializer = CreatorSerializer(creator)
    return JsonResponse(serializer.data, status=200)


# ------------------------------------------------------------
# 11) Deliverable 제출
# ------------------------------------------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_deliverable(request, deliverable_id):
    deliverable = get_object_or_404(
        Deliverable,
        deliverable_id=deliverable_id
    )

    # 권한 체크
    if request.user != deliverable.campaign_acceptance.creator:
        return Response(
            {"error": "본인 Deliverable만 제출할 수 있습니다."},
            status=403
        )

    # AI 검증 통과 여부 체크
    if deliverable.ai_validation_status != "passed":
        return Response(
            {"error": "AI 검증을 통과한 Deliverable만 제출할 수 있습니다."},
            status=400
        )

    # 이미 제출된 경우
    if deliverable.submitted_at:
        return Response(
            {"error": "이미 제출된 Deliverable입니다."},
            status=400
        )

    #  제출 처리
    deliverable.deliverable_status = "completed"
    deliverable.submitted_at = timezone.now()
    deliverable.save(
        update_fields=["deliverable_status", "submitted_at"]
    )

    return Response(
        {
            "message": "Deliverable 제출이 완료되었습니다.",
            "submitted_at": deliverable.submitted_at,
            "deliverable_status": deliverable.deliverable_status,
        },
        status=200
    )


# ============================================================
# 캠페인 자동 크리에이터 매칭
# ============================================================-

def auto_match_creators(campaign):
    """
    캠페인 조건에 맞는 모든 크리에이터에 대해
    CampaignAcceptance를 자동 생성한다.
    (이미 해당 캠페인에 acceptance가 있는 크리에이터는 제외)
    """

    # --------------------------------------------------------
    # 1. 캠페인 기본 조건
    # --------------------------------------------------------
    target_pet_type = campaign.target_pet_type
    min_follower_count = campaign.min_follower_count

    campaign_style_tags = campaign.style_tags.all()
    has_no_preference = campaign_style_tags.filter(
        code="no_preference"
    ).exists()

    # --------------------------------------------------------
    # 2. 크리에이터 기본 필터
    # --------------------------------------------------------
    creators = User.objects.filter(
        account_type="creator",
        pet_type=target_pet_type,
        follower_count__gte=min_follower_count
    )

    # --------------------------------------------------------
    # 3. 스타일 태그 필터 (no_preference 아닐 때만)
    # --------------------------------------------------------
    if not has_no_preference and campaign_style_tags.exists():
        creators = creators.filter(
            style_tags__in=campaign_style_tags
        ).distinct()

    # --------------------------------------------------------
    # 4. 이미 해당 캠페인에 acceptance가 있는 creator 제외
    # --------------------------------------------------------
    existing_creator_ids = CampaignAcceptance.objects.filter(
        campaign=campaign
    ).values_list("creator_id", flat=True)

    creators = creators.exclude(id__in=existing_creator_ids)

    # --------------------------------------------------------
    # 5. CampaignAcceptance 생성
    # --------------------------------------------------------
    now = timezone.now()
    acceptance_list = []

    for creator in creators:
        acceptance_list.append(
            CampaignAcceptance(
                campaign=campaign,
                creator=creator,
                brand_decision_status="pending",
                acceptance_status="pending",
                applied_at=now
            )
        )

    CampaignAcceptance.objects.bulk_create(acceptance_list)



# ------------------------------------------------------------
# 캠페인 조건 변경 시 기존 추천 정리
# ------------------------------------------------------------
from .models import CampaignAcceptance


def cleanup_invalid_acceptances(campaign):
    """
    캠페인 조건 변경 시,
    아직 승인되지 않은 acceptance 중
    현재 캠페인 조건을 만족하지 않는 것들을 제거한다.
    """

    # 승인된 acceptance는 절대 건드리지 않음
    pending_acceptances = CampaignAcceptance.objects.filter(
        campaign=campaign,
        brand_decision_status="pending"
    ).select_related("creator")

    for acceptance in pending_acceptances:
        creator = acceptance.creator

        # 1. 반려동물 타입
        if creator.pet_type != campaign.target_pet_type:
            acceptance.delete()
            continue

        # 2. 팔로워 수
        if creator.follower_count < campaign.min_follower_count:
            acceptance.delete()
            continue

        # 3. 스타일 태그 (no_preference 아닐 때만)
        campaign_tags = campaign.style_tags.all()

        if campaign_tags.filter(code="no_preference").exists():
            continue

        if campaign_tags.exists():
            if not creator.style_tags.filter(
                id__in=campaign_tags
            ).exists():
                acceptance.delete()




# ####################################
# AI 검증
# ####################################
# ------------------------------------------------------------
# 12) Deliverable AI 검증 요청
# ------------------------------------------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_deliverable(request, deliverable_id):
    deliverable = get_object_or_404(
        Deliverable,
        deliverable_id=deliverable_id
    )

    if request.user.account_type != "creator":
        return Response(
            {"error": "크리에이터만 검증을 요청할 수 있습니다."},
            status=403
        )

    if deliverable.campaign_acceptance.creator != request.user:
        return Response(
            {"error": "본인 Deliverable만 검증할 수 있습니다."},
            status=403
        )

    try:
        ai_result = run_deliverable_ai_verification(deliverable.deliverable_id)

        deliverable.refresh_from_db()

        # 무조건 200으로 내려줌
        return Response(
            {
                "ai_validation_status": deliverable.ai_validation_status,
                "ai_result": deliverable.ai_result_raw,
            },
            status=200
        )

    except Exception as e:
        # 진짜 서버 에러만 400
        return Response(
            {"error": str(e)},
            status=400
        )
