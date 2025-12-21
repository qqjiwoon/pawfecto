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

def run_deliverable_ai_verification(deliverable_id: int):
    deliverable = Deliverable.objects.select_related(
        "campaign_acceptance__campaign"
    ).get(deliverable_id=deliverable_id)

    deliverable.ai_validation_status = "pending"
    deliverable.save(update_fields=["ai_validation_status"])

    try:
        campaign = deliverable.campaign_acceptance.campaign

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

        ai_result_raw = run_ai_verification(
            prompt=full_prompt,
            images=[deliverable.image],
        )

        if not isinstance(ai_result_raw, dict):
            raise ValueError(f"AI 결과 타입 오류: {type(ai_result_raw)}")

        validate_ai_result(ai_result_raw)

        # ✅ PASS / FAIL 판단
        required_reqs = campaign.requirements.filter(is_required=True)

        ai_condition_map = {
            c["requirement"]: c["satisfied"]
            for c in ai_result_raw["conditions"]
        }

        is_passed = all(
            ai_condition_map.get(req.description) is True
            for req in required_reqs
        )

        deliverable.ai_result_raw = ai_result_raw
        deliverable.ai_validation_status = "passed" if is_passed else "failed"
        deliverable.save(
            update_fields=["ai_result_raw", "ai_validation_status"]
        )

        return ai_result_raw

    except Exception as e:
        deliverable.ai_validation_status = "failed"
        deliverable.ai_result_raw = {"error": str(e)}
        deliverable.save(
            update_fields=["ai_validation_status", "ai_result_raw"]
        )
        raise
