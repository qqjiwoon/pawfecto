from django.db import models
from django.conf import settings


# -----------------------------------------------------------
# StyleTag (공통 스타일 태그 모델)
# -----------------------------------------------------------
class StyleTag(models.Model):
    code = models.CharField(max_length=50, unique=True)   # 영문 코드명
    name = models.CharField(max_length=50)                # 한국어 태그명 또는 표시용 이름

    def __str__(self):
        return self.name


# -----------------------------------------------------------
# 2. Campaign (캠페인) : 브랜드가 생성한 광고 캠페인
# -----------------------------------------------------------

class Campaign(models.Model):

    campaign_id = models.AutoField(primary_key=True)

    brand = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='campaigns'
    )

    product_name = models.CharField(max_length=100)
    product_image_url = models.ImageField(upload_to='campaigns/', null=True, blank=True)
    product_description = models.TextField()

    # 타겟 반려동물 : ENUM('dog', 'cat') NULL
    target_pet_type = models.CharField(
        max_length=10,
        choices=[('dog', 'Dog'), ('cat', 'Cat')],
        null=True,
        blank=True
    )

    min_follower_count = models.IntegerField(default=0)

    # 캠페인 일정
    requested_at = models.DateTimeField()
    application_deadline_at = models.DateField()
    posting_start_at = models.DateField()
    posting_end_at = models.DateField()

    required_creator_count = models.IntegerField()

    # 캠페인 스타일 태그 (StyleTag M2M 통일)
    style_tags = models.ManyToManyField(
        StyleTag,
        related_name="campaigns",
        blank=True
    )

    def __str__(self):
        return self.product_name
    
    def save(self, *args, **kwargs):
        # 1. 먼저 부모 save를 실행하여 파일 업로드 완료
        super().save(*args, **kwargs)

        # 2. 프로덕트 이미지가 있다면 GCS URL을 반영
        if self.product_image_url:
            try:
                # GCS에 업로드된 이미지의 URL을 가져옴
                self.product_image_url = self.product_image_url.url
            except Exception as e:
                print(f"GCS URL 동기화 실패: {e}")



# -----------------------------------------------------------
# 3. CampaignAcceptance (브랜드 승인 / 크리에이터 수락)
# -----------------------------------------------------------

class CampaignAcceptance(models.Model):

    campaign_acceptance_id = models.AutoField(primary_key=True)

    creator = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='campaign_acceptances'
    )

    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
        related_name='acceptances'
    )

    # 브랜드 승인 상태 : 브랜드가 크리에이터를 승인/거절
    brand_decision_status = models.CharField(
        max_length=10,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        default='pending'
    )

    # 브랜드 승인/거절 시점
    brand_decided_at = models.DateTimeField(null=True, blank=True)

    # 크리에이터 수락 상태
    acceptance_status = models.CharField(
        max_length=10,
        choices=[
            ('pending', 'Pending'),
            ('accepted', 'Accepted'),
            ('rejected', 'Rejected'),
            ('completed', 'Completed'),
        ],
        default='pending'
    )

    # 상태 변경 시점 기록
    applied_at = models.DateTimeField(null=True, blank=True)  # SQL: DATETIME (auto_now_add 아님)
    accepted_at = models.DateTimeField(null=True, blank=True)  # SQL 스키마와 동일하게 수정

    class Meta:
        # 동일 캠페인에 동일 크리에이터 중복 방지
        unique_together = ('campaign', 'creator')

    def __str__(self):
        return (
            f"{self.creator.name} - {self.campaign.product_name} "
            f"(brand={self.brand_decision_status}, creator={self.acceptance_status})"
        )


# -----------------------------------------------------------
# 4-1. 브랜드의 포스팅 요구 조건
# -----------------------------------------------------------
class DeliverableRequirement(models.Model):
    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
        related_name="requirements"
    )

    REQUIREMENT_TYPE_CHOICES = [
        ("object", "Object"),
        ("scene", "Scene"),
        ("action", "Action"),
        ("text", "Text"),
    ]

    requirement_type = models.CharField(
        max_length=20,
        choices=REQUIREMENT_TYPE_CHOICES
    )

    description = models.CharField(max_length=255)
    is_required = models.BooleanField(default=True)

# -----------------------------------------------------------
# 4-2. Deliverable (포스팅 결과물)
# -----------------------------------------------------------
class Deliverable(models.Model):

    deliverable_id = models.AutoField(primary_key=True)

    campaign_acceptance = models.OneToOneField(
        CampaignAcceptance,
        on_delete=models.CASCADE,
        related_name='deliverable'
    )

    posted_at = models.DateTimeField(null=True, blank=True)
    post_url = models.CharField(max_length=255, null=True, blank=True)

    deliverable_status = models.CharField(
        max_length=10,
        choices=[
            ('incomplete', 'Incomplete'),
            ('completed', 'Completed'),
        ],
        default='incomplete'
    )

    content = models.TextField()
    image = models.ImageField(upload_to='deliverables/', null=True, blank=True)

    ai_validation_status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("passed", "Passed"),
            ("failed", "Failed"),
        ],
        default="pending"
    )

    ai_result_raw = models.JSONField(
        null=True,
        blank=True
    )

    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Deliverable for {self.campaign_acceptance.campaign.product_name}"
