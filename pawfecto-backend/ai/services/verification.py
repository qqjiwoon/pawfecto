# ai/services/verification.py
# AI 검증 실행 서비스 (mock 단계)

from myapp.models import DeliverableRequirement


def run_ai_verification(prompt: str, images: list):
    """
    MOCK AI 검증
    - 실제 AI 연동 전 단계
    - 캠페인에 정의된 요구조건을 그대로 PASS 처리
    """

    # ⚠️ prompt 안에는 deliverable_id 정보가 없으므로
    # 실제 mock에서는 "프롬프트에 포함된 요구조건 문자열"을 신뢰하지 않는다
    # → 서비스 계층에서 requirement description을 기준으로 결과를 맞춘다

    # MOCK 결과 예시 (실제 requirement와 반드시 일치해야 함)
    return {
    "image_analysis_success": True,
    "conditions": [
        {
            "requirement_type": "object",
            "requirement": "dog wearing harness",
            "satisfied": True
        },
        {
            "requirement_type": "scene",
            "requirement": "outdoor field",
            "satisfied": True
        },
        {
            "requirement_type": "action",
            "requirement": "walking",
            "satisfied": True
        },
        {
            "requirement_type": "text",
            "requirement": "mention product benefits",
            "satisfied": True
        }
    ],
    "score": 100,
    "error_reason": None
}
