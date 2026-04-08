import json
from rest_framework import serializers

from .models import (
    Campaign,
    CampaignAcceptance,
    Deliverable,
    DeliverableRequirement,
    StyleTag,
)
from accounts.serializers import BrandSerializer


class StyleTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = StyleTag
        fields = ["id", "code", "name"]


class DeliverableRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliverableRequirement
        fields = [
            "id",
            "requirement_type",
            "description",
            "is_required",
        ]


class CampaignSerializer(serializers.ModelSerializer):
    brand = serializers.SerializerMethodField()
    requirements = DeliverableRequirementSerializer(many=True, read_only=True)
    requirements_data = serializers.JSONField(write_only=True, required=False)
    style_tags = StyleTagSerializer(many=True, read_only=True)
    style_tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=StyleTag.objects.all(),
        many=True,
        write_only=True,
    )
    product_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Campaign
        fields = [
            "campaign_id",
            "brand",
            "product_name",
            "product_image_url",
            "product_description",
            "target_pet_type",
            "min_follower_count",
            "style_tags",
            "style_tag_ids",
            "requested_at",
            "application_deadline_at",
            "posting_start_at",
            "posting_end_at",
            "required_creator_count",
            "requirements",
            "requirements_data",
        ]

    def get_brand(self, obj):
        if not obj.brand_id:
            return None

        return {
            "id": obj.brand_id,
            "name": obj.brand.name,
            "profile_image_url": obj.brand.profile_image_url,
            "account_type": obj.brand.account_type,
        }

    def get_product_image_url(self, obj):
        image = obj.product_image_url
        if not image:
            return None

        try:
            return image.url
        except Exception:
            return str(image)

    def create(self, validated_data):
        style_tags = validated_data.pop("style_tag_ids", [])
        raw_requirements = validated_data.pop("requirements_data", "[]")

        if isinstance(raw_requirements, str):
            try:
                requirements_list = json.loads(raw_requirements)
            except (json.JSONDecodeError, TypeError):
                requirements_list = []
        else:
            requirements_list = raw_requirements

        campaign = Campaign.objects.create(**validated_data)
        campaign.style_tags.set(style_tags)

        for req in requirements_list:
            DeliverableRequirement.objects.create(
                campaign=campaign,
                requirement_type=req.get("requirement_type"),
                description=req.get("description"),
                is_required=req.get("is_required", True),
            )

        return campaign

    def update(self, instance, validated_data):
        style_tags = validated_data.pop("style_tag_ids", None)
        raw_requirements = validated_data.pop("requirements_data", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if style_tags is not None:
            instance.style_tags.set(style_tags)

        if raw_requirements is not None:
            if isinstance(raw_requirements, str):
                try:
                    requirements_list = json.loads(raw_requirements)
                except (json.JSONDecodeError, TypeError):
                    requirements_list = []
            else:
                requirements_list = raw_requirements

            instance.requirements.all().delete()

            for req in requirements_list:
                DeliverableRequirement.objects.create(
                    campaign=instance,
                    requirement_type=req.get("requirement_type"),
                    description=req.get("description"),
                    is_required=req.get("is_required", True),
                )

        return instance


class CampaignListSerializer(serializers.ModelSerializer):
    brand = serializers.SerializerMethodField()
    product_image_url = serializers.SerializerMethodField()

    def get_brand(self, obj):
        if not obj.brand_id:
            return None

        return {
            "id": obj.brand_id,
            "name": obj.brand.name,
            "profile_image_url": obj.brand.profile_image_url,
            "account_type": obj.brand.account_type,
        }

    def get_product_image_url(self, obj):
        image = obj.product_image_url
        if not image:
            return None

        try:
            return image.url
        except Exception:
            return str(image)

    class Meta:
        model = Campaign
        fields = [
            "campaign_id",
            "product_name",
            "product_description",
            "brand",
            "product_image_url",
            "requested_at",
            "application_deadline_at",
        ]


class CampaignAcceptanceSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()
    campaign = serializers.SerializerMethodField()

    def get_creator(self, obj):
        creator = obj.creator
        if not creator:
            return None

        return {
            "id": creator.id,
            "username": creator.username,
            "name": creator.name,
            "sns_handle": creator.sns_handle,
            "profile_image_url": creator.profile_image_url,
            "pet_type": creator.pet_type,
            "follower_count": creator.follower_count,
            "style_tags": StyleTagSerializer(creator.style_tags.all(), many=True).data,
        }

    def get_campaign(self, obj):
        campaign = obj.campaign
        if not campaign:
            return None

        image = campaign.product_image_url
        if not image:
            product_image_url = None
        else:
            try:
                product_image_url = image.url
            except Exception:
                product_image_url = str(image)

        return {
            "campaign_id": campaign.campaign_id,
            "product_name": campaign.product_name,
            "product_description": campaign.product_description,
            "product_image_url": product_image_url,
            "min_follower_count": campaign.min_follower_count,
            "requested_at": campaign.requested_at,
            "application_deadline_at": campaign.application_deadline_at,
            "style_tags": StyleTagSerializer(campaign.style_tags.all(), many=True).data,
            "brand": {
                "id": campaign.brand_id,
                "name": campaign.brand.name,
                "profile_image_url": campaign.brand.profile_image_url,
                "account_type": campaign.brand.account_type,
            },
        }

    class Meta:
        model = CampaignAcceptance
        fields = [
            "campaign_acceptance_id",
            "creator",
            "campaign",
            "brand_decision_status",
            "brand_decided_at",
            "acceptance_status",
            "applied_at",
            "accepted_at",
        ]


class DeliverableSerializer(serializers.ModelSerializer):
    campaign_acceptance = CampaignAcceptanceSerializer(read_only=True)

    class Meta:
        model = Deliverable
        fields = [
            "deliverable_id",
            "campaign_acceptance",
            "posted_at",
            "post_url",
            "deliverable_status",
            "content",
            "image",
            "ai_validation_status",
            "submitted_at",
        ]


class DeliverableCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deliverable
        fields = [
            "content",
            "image",
            "post_url",
        ]
