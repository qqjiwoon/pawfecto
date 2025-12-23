from django.urls import path
from . import views

app_name = 'myapp'

urlpatterns = [

    # =====================================================
    # 브랜드 기능
    # =====================================================

    # 1) 브랜드 캠페인 목록 조회
    path(
        'brand/<int:brand_id>/campaign/',
        views.brand_campaign_list,
        name='brand_campaign_list'
    ),

    # 2) 캠페인 생성
    path(
        'brand/<int:brand_id>/campaign/create/',
        views.create_campaign,
        name='create_campaign'
    ),

    # 3) 캠페인 상세 조회
    path(
        'brand/<int:brand_id>/campaign/<int:campaign_id>/',
        views.campaign_detail,
        name='campaign_detail'
    ),

    # 4) 캠페인 수정
    path(
        'brand/<int:brand_id>/campaign/<int:campaign_id>/update/',
        views.update_campaign,
        name='update_campaign'
    ),

    # 4-2) 캠페인 삭제
    path(
        'brand/<int:brand_id>/campaign/<int:campaign_id>/delete/',
        views.delete_campaign,
        name='delete_campaign'
    ),

    # ============================================================
    # [브랜드] Campaign_requirement 관련
    # ============================================================

    # 포스팅 요구조건 조회/생성
    path(
        "brand/<int:brand_id>/campaign/<int:campaign_id>/requirements/",
        views.campaign_requirements,
        name='campaign_requirements'
    ),

    # 캠페인 포스팅 요구조건 수정
    path(
        'brand/<int:brand_id>/campaign/<int:campaign_id>/requirements/<int:requirement_id>/update/',
        views.update_campaign_requirement,
        name='update_campaign_requirement'
    ),

    # 캠페인 포스팅 요구조건 삭제
    path(
        'brand/<int:brand_id>/campaign/<int:campaign_id>/requirements/<int:requirement_id>/delete/',
        views.delete_campaign_requirement,
        name='delete_campaign_requirement'
    ),


    # ============================================================
    # [브랜드] Campaign 진행 관련
    # ============================================================

    # 1) 특정 캠페인의 오퍼(신청) 목록 조회
    path(
        'brand/<int:brand_id>/campaign/<int:campaign_id>/acceptances/',
        views.campaign_acceptance_list,
        name='campaign_acceptance_list'
    ),

    # 2) 브랜드가 크리에이터 승인
    path(
        'brand/<int:brand_id>/campaign/<int:campaign_id>/acceptances/<int:acceptance_id>/approve/',
        views.approve_creator,
        name='approve_creator'
    ),

    # 3) 브랜드가 크리에이터 거절
    path(
        'brand/<int:brand_id>/campaign/<int:campaign_id>/acceptances/<int:acceptance_id>/reject/',
        views.reject_creator,
        name='reject_creator'
    ),

    # 4) 캠페인 진행 상황 조회 (Deliverable)
    path(
        'brand/<int:brand_id>/campaign/<int:campaign_id>/progress/',
        views.campaign_progress,
        name='campaign_progress'
    ),


    # =====================================================
    # 크리에이터 기능
    # =====================================================

    # 7) 크리에이터 오퍼 조회
    path(
        'creator/<int:creator_id>/offers/',
        views.creator_campaign_offers,
        name='creator_campaign_offers'
    ),

    # 8) 캠페인 오퍼 수락
    path(
        'creator/offers/<int:acceptance_id>/accept/',
        views.accept_offer,
        name='accept_offer'
    ),

    # 9) 캠페인 오퍼 거절
    path(
        'creator/offers/<int:acceptance_id>/reject/',
        views.reject_offer,
        name='reject_offer'
    ),

    # 10) 진행상황 조회 (크리에이터 관점)
    path(
        'creator/<int:creator_id>/progress/',
        views.creator_progress,
        name='creator_progress'
    ),
    # 11) 기본 정보 조회
    path(
        'creator/<int:creator_id>/',
        views.creator_detail,
        name='creator_detail'
    ),
    # deliverable 제출
    path(
        'deliverables/<int:deliverable_id>/submit/',
        views.submit_deliverable,
        name='submit_deliverable',
    ),
    # deliverable 저장하기
    path(
        'deliverables/<int:deliverable_id>/save/', 
        views.save_deliverable, 
        name='save_deliverable'
    ),
    # Deliverable AI 검증 요청
    path(
        'deliverables/<int:deliverable_id>/verify/',
        views.verify_deliverable,
        name='verify_deliverable',
    ),

]
