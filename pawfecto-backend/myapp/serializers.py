import json
from rest_framework import serializers
from .models import Campaign, CampaignAcceptance, Deliverable, StyleTag, DeliverableRequirement
from accounts.serializers import BrandSerializer, UserSerializer


# -----------------------------------------------------------
# StyleTag Serializer (공유)
# -----------------------------------------------------------
class StyleTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = StyleTag
        fields = ['id', 'code', 'name']


# -----------------------------------------------------------
# 5. DeliverableRequirementSerializer 포스팅 요구 조건
# -----------------------------------------------------------
class DeliverableRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliverableRequirement
        fields = [
            'id',
            'requirement_type',
            'description',
            'is_required',
        ]

# -----------------------------------------------------------
# 1. CampaignSerializer (상세 페이지용)
# -----------------------------------------------------------
class CampaignSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)

    # [조회용] DB의 데이터를 프론트로 보낼 때 사용
    # 모델의 ForeignKey에서 related_name='requirements'가 설정되어 있지 않다면 
    # source='deliverablerequirement_set'을 사용하세요.
    requirements = DeliverableRequirementSerializer(
        many=True, 
        read_only=True,
        # source='requirements' # 모델의 related_name과 일치해야 함
    )

    # [저장용] 프론트의 FormData(문자열)를 받기 위해 사용
    requirements_data = serializers.JSONField(write_only=True, required=False)

    # 스타일 태그 처리
    style_tags = StyleTagSerializer(many=True, read_only=True)
    style_tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=StyleTag.objects.all(),
        many=True,
        write_only=True
    )

    product_image_url = serializers.ImageField(required=False)

    class Meta:
        model = Campaign
        fields = [
            'campaign_id',
            'brand',
            'product_name',
            'product_image_url',
            'product_description',
            'target_pet_type',
            'min_follower_count',
            'style_tags',      # GET용
            'style_tag_ids',   # POST/PUT용
            'requested_at',
            'application_deadline_at',
            'posting_start_at',
            'posting_end_at',
            'required_creator_count',
            'requirements',    # GET용
            'requirements_data', # POST/PUT용 (FormData 대응)
        ]

    def create(self, validated_data):
        # 1. 특수 데이터 추출
        style_tags = validated_data.pop('style_tag_ids', [])
        raw_requirements = validated_data.pop('requirements_data', '[]')

        # 2. FormData로 들어온 문자열 JSON 파싱
        if isinstance(raw_requirements, str):
            try:
                requirements_list = json.loads(raw_requirements)
            except (json.JSONDecodeError, TypeError):
                requirements_list = []
        else:
            requirements_list = raw_requirements

        # 3. 캠페인 생성
        campaign = Campaign.objects.create(**validated_data)
        
        # 4. 스타일 태그(M2M) 연결
        campaign.style_tags.set(style_tags)

        # 5. 요구사항(Requirement) 생성
        for req in requirements_list:
            DeliverableRequirement.objects.create(
                campaign=campaign,
                requirement_type=req.get('requirement_type'),
                description=req.get('description'),
                is_required=req.get('is_required', True)
            )

        return campaign

    def update(self, instance, validated_data):
        # 1. 특수 데이터 추출
        style_tags = validated_data.pop('style_tag_ids', None)
        raw_requirements = validated_data.pop('requirements_data', None)

        # 2. 기본 필드 업데이트
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # 3. 스타일 태그 업데이트
        if style_tags is not None:
            instance.style_tags.set(style_tags)

        # 4. 요구사항 업데이트 (기존 삭제 후 재생성)
        if raw_requirements is not None:
            if isinstance(raw_requirements, str):
                try:
                    requirements_list = json.loads(raw_requirements)
                except (json.JSONDecodeError, TypeError):
                    requirements_list = []
            else:
                requirements_list = raw_requirements

            # 기존 연관 데이터 삭제 (related_name 'requirements' 기준)
            instance.requirements.all().delete() 
            
            for req in requirements_list:
                DeliverableRequirement.objects.create(
                    campaign=instance,
                    requirement_type=req.get('requirement_type'),
                    description=req.get('description'),
                    is_required=req.get('is_required', True)
                )

        return instance
    

# -----------------------------------------------------------
# 2. CampaignListSerializer (요약 리스트용)
# -----------------------------------------------------------

class CampaignListSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)

    class Meta:
        model = Campaign
        fields = [
            'campaign_id',
            'product_name',
            'product_description',
            'brand',
            'product_image_url',
            'requested_at',
            'application_deadline_at',
        ]



# -----------------------------------------------------------
# 3. CampaignAcceptanceSerializer (신청/수락 정보)
# -----------------------------------------------------------

class CampaignAcceptanceSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)            # 신청한 크리에이터 정보
    campaign = CampaignSerializer(read_only=True)   # 신청한 캠페인의 요약 정보

    class Meta:
        model = CampaignAcceptance
        fields = [
            'campaign_acceptance_id',
            'creator',
            'campaign',

            # 브랜드 승인 단계
            'brand_decision_status',
            'brand_decided_at',

            # 크리에이터 수락 단계
            'acceptance_status',
            'applied_at',
            'accepted_at',
        ]



# -----------------------------------------------------------
# 4. DeliverableSerializer (납품 결과물) 조회용 
# -----------------------------------------------------------

class DeliverableSerializer(serializers.ModelSerializer):
    campaign_acceptance = CampaignAcceptanceSerializer(read_only=True)

    class Meta:
        model = Deliverable
        fields = [
            'deliverable_id',
            'campaign_acceptance',
            'posted_at',
            'post_url',
            'deliverable_status',
            'content',
            'image',
            'ai_validation_status',
            'submitted_at',
        ]

# -----------------------------------------------------------
# 4-1. 이미지 업로드 content 입력
# -----------------------------------------------------------
class DeliverableCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deliverable
        fields = [
            'content',
            'image',
            'post_url',
        ]
