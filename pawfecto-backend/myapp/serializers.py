from rest_framework import serializers
from .models import Campaign, CampaignAcceptance, Deliverable, StyleTag
from accounts.serializers import BrandSerializer, UserSerializer


# -----------------------------------------------------------
# StyleTag Serializer (공유)
# -----------------------------------------------------------
class StyleTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = StyleTag
        fields = ['id', 'code', 'name']



# -----------------------------------------------------------
# 1. CampaignSerializer (상세 페이지용)
# -----------------------------------------------------------

# Campaign Serializer (생성/조회 겸용)

class CampaignSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)

    # 조회용
    style_tags = StyleTagSerializer(many=True, read_only=True)

    # 생성/수정용
    style_tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=StyleTag.objects.all(),
        many=True,
        write_only=True
    )

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
            'style_tags',        # GET
            'style_tag_ids',     # POST / PUT
            'requested_at',
            'application_deadline_at',
            'posting_start_at',
            'posting_end_at',
            'required_creator_count',
        ]

    def create(self, validated_data):
        style_tags = validated_data.pop('style_tag_ids', [])
        campaign = Campaign.objects.create(**validated_data)
        campaign.style_tags.set(style_tags)
        return campaign

    def update(self, instance, validated_data):
        style_tags = validated_data.pop('style_tag_ids', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if style_tags is not None:
            instance.style_tags.set(style_tags)

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
    campaign = CampaignListSerializer(read_only=True)   # 신청한 캠페인의 요약 정보

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
# 4. DeliverableSerializer (납품 결과물)
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
        ]
