# services/deliverable_service.py
# Deliverable AI 검증 서비스

from myapp.models import Deliverable
from ai.prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE, OUTPUT_FORMAT_INSTRUCTION
from ai.validators import validate_ai_result
from ai.services.verification import run_ai_verification


def satisfied_to_score(value: str) -> float:
    return {
        "yes": 1.0,
        "uncertain": 0.5,
        "no": 0.0
    }.get(value, 0.0)


def run_deliverable_ai_verification(deliverable_id: int):
    deliverable = Deliverable.objects.select_related(
        "campaign_acceptance__campaign"
    ).get(deliverable_id=deliverable_id)

    # 1. content 필수
    if not deliverable.content or not deliverable.content.strip():
        deliverable.ai_validation_status = "failed"
        deliverable.ai_result_raw = {
            "error_reason": "게시글 내용(content)이 입력되지 않았습니다."
        }
        deliverable.save(update_fields=["ai_validation_status", "ai_result_raw"])
        return deliverable.ai_result_raw

    # 2. 이미지 필수
    if not deliverable.image:
        deliverable.ai_validation_status = "failed"
        deliverable.ai_result_raw = {
            "error_reason": "이미지가 첨부되지 않았습니다."
        }
        deliverable.save(update_fields=["ai_validation_status", "ai_result_raw"])
        return deliverable.ai_result_raw

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
            caption=deliverable.content,
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

        validate_ai_result(ai_result_raw)

        # === 판정 로직 ===
        scores = []
        failed_reasons = []

        for cond in ai_result_raw["conditions"]:
            score = satisfied_to_score(cond["satisfied"])
            scores.append(score)

            if cond["satisfied"] == "no":
                failed_reasons.append(
                    f"{cond['requirement']} 충족되지 않음: {cond.get('reason', '')}"
                )

        avg_score = sum(scores) / len(scores)

        if avg_score >= 0.5:
            status = "passed"
        elif avg_score >= 0.3:
            status = "review"
        else:
            status = "failed"

        deliverable.ai_validation_status = status
        deliverable.ai_result_raw = ai_result_raw

        if failed_reasons:
            deliverable.ai_result_raw["error_reason"] = " / ".join(failed_reasons)

        deliverable.save(
            update_fields=["ai_validation_status", "ai_result_raw"]
        )

        return deliverable.ai_result_raw

    except Exception as e:
        deliverable.ai_validation_status = "failed"
        deliverable.ai_result_raw = {"error_reason": str(e)}
        deliverable.save(
            update_fields=["ai_validation_status", "ai_result_raw"]
        )
        return deliverable.ai_result_raw
