# services/deliverable_service.py
# Deliverable AI 검증 서비스

from myapp.models import Deliverable
from ai.prompts import (
    SYSTEM_PROMPT,
    USER_PROMPT_TEMPLATE,
    OUTPUT_FORMAT_INSTRUCTION,
)
from ai.validators import validate_ai_result, AIResultValidationError
from ai.services.verification import run_ai_verification


def verify_deliverable(deliverable_id: int):
    deliverable = Deliverable.objects.select_related(
        "campaign_acceptance__campaign"
    ).get(deliverable_id=deliverable_id)

    # 검증 시작
    deliverable.ai_validation_status = "pending"
    deliverable.save(update_fields=["ai_validation_status"])

    try:
        campaign = deliverable.campaign_acceptance.campaign

        # 1) 요구조건 목록을 구조화된 문자열로 변환
        requirements_payload = [
            {
                "type": req.requirement_type,
                "description": req.description,
                "is_required": req.is_required,
            }
            for req in campaign.requirements.all()
        ]

        if not requirements_payload:
            raise ValueError("요구조건이 존재하지 않습니다.")

        # 2) 프롬프트 구성
        user_prompt = USER_PROMPT_TEMPLATE.format(
            requirements=requirements_payload,
            caption=deliverable.content or "",
        )

        full_prompt = (
            SYSTEM_PROMPT
            + "\n\n"
            + user_prompt
            + "\n\n"
            + OUTPUT_FORMAT_INSTRUCTION
        )

        # 3) AI 호출
        ai_result = run_ai_verification(
            prompt=full_prompt,
            images=[deliverable.image],
        )

        # 4) AI 결과 검증
        validate_ai_result(ai_result)

        # 5) 상태 결정
        if (
            ai_result["image_analysis_success"] is True
            and ai_result["score"] == 100
        ):
            deliverable.ai_validation_status = "passed"
            deliverable.deliverable_status = "completed"
        else:
            deliverable.ai_validation_status = "failed"

        deliverable.save(
            update_fields=[
                "ai_validation_status",
                "deliverable_status",
            ]
        )

    except (AIResultValidationError, Exception):
        deliverable.ai_validation_status = "failed"
        deliverable.save(update_fields=["ai_validation_status"])
