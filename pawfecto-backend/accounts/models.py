from django.db import models
from django.contrib.auth.models import AbstractUser
from myapp.models import StyleTag
from django.core.validators import RegexValidator

# -----------------------------------
# User 모델 (Brand / Creator 통합)
# -----------------------------------
class User(AbstractUser):
    ACCOUNT_TYPES = [
        ('brand', 'Brand (광고주)'),
        ('creator', 'Creator (인플루언서)'),
    ]

    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^[0-9\-]+$',
                message='전화번호는 숫자와 하이픈(-)만 입력 가능합니다.'
            )
        ]
    )

    pet_type = models.CharField(
        max_length=10,
        choices=[('dog', 'Dog'), ('cat', 'Cat')],
        null=True,
        blank=True
    )

    # Brand
    # --- 이미지 관련 필드 ---
    # 브랜드가 파일을 업로드할 때, 폼(Form) 처리를 위해 기존 필드는 남겨두되,
    # 실제 이미지는 GCS에 올라가고, DB에는 아래 'profile_image_url'만 주로 쓰게 됩니다.
    profile_image = models.ImageField(upload_to='temp_uploads/', null=True, blank=True)

    # ★ 핵심: 브랜드(GCS URL)와 크리에이터(Instagram URL) 모두 여기에 주소가 저장됩니다.
    profile_image_url = models.CharField(max_length=1000, null=True, blank=True)

    # Creator
    address = models.TextField(null=True, blank=True)
    sns_handle = models.CharField(max_length=50, null=True, blank=True)
    sns_url = models.CharField(max_length=255, null=True, blank=True)
    total_post_count = models.IntegerField(null=True, blank=True)
    follower_count = models.IntegerField(null=True, blank=True)
    following_count = models.IntegerField(null=True, blank=True)  # follows_count
    # [추천] 사용자가 아이디를 바꿔도 계정을 찾을 수 있게 고유 ID 저장(계정명과 별개)
    instagram_id = models.CharField(max_length=50, null=True, blank=True, unique=True)

    # 핵심: through 반드시 지정
    style_tags = models.ManyToManyField(
        StyleTag,
        through="UserStyleTag",
        related_name="users",
        blank=True
    )

    def __str__(self):
        return f"[{self.account_type.upper()}] {self.name} ({self.username})"
    
    def save(self, *args, **kwargs):
        # 1. 먼저 부모 save를 실행 (GCS 업로드 완료)
        super().save(*args, **kwargs)

        # 2. 업로드 완료 후 URL이 생성되었다면, 필드만 조용히 업데이트
        if self.profile_image:
            try:
                new_url = self.profile_image.url
                if self.profile_image_url != new_url:
                    # update()를 사용하면 save()가 다시 호출되지 않아 Pickle/무한루프 에러가 절대 안 납니다.
                    self.__class__.objects.filter(pk=self.pk).update(profile_image_url=new_url)
                    self.profile_image_url = new_url
            except Exception as e:
                print(f"GCS URL 동기화 실패: {e}")



# -----------------------------------
# User ↔ StyleTag 중간 테이블
# -----------------------------------
class UserStyleTag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    style_tag = models.ForeignKey(StyleTag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "style_tag")

    def __str__(self):
        return f"{self.user_id} - {self.style_tag_id}"
