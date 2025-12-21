# ai/validators.py
from jsonschema import validate, ValidationError

from .schemas import DELIVERABLE_AI_RESULT_SCHEMA


class AIResultValidationError(Exception):
    """AI 응답 검증 실패"""
    pass


# 허용되는 requirement_type 값
# ALLOWED_REQUIREMENT_TYPES = {"object", "scene", "action", "text"}

ALLOWED_SATISFIED_VALUES = {"yes", "uncertain", "no"}

def validate_ai_result(result: dict):
    if "conditions" not in result:
        raise AIResultValidationError("conditions missing")

    for idx, cond in enumerate(result["conditions"]):
        if "requirement_type" not in cond:
            raise AIResultValidationError(f"condition[{idx}] missing requirement_type")

        if "requirement" not in cond:
            raise AIResultValidationError(f"condition[{idx}] missing requirement")

        if "satisfied" not in cond:
            raise AIResultValidationError(f"condition[{idx}] missing satisfied")

        if cond["satisfied"] not in ALLOWED_SATISFIED_VALUES:
            raise AIResultValidationError(
                f"condition[{idx}] invalid satisfied value: {cond['satisfied']}"
            )



def validate_schema(ai_result: dict):
    """
    1차 검증: JSON Schema 구조 검증
    """
    try:
        validate(instance=ai_result, schema=DELIVERABLE_AI_RESULT_SCHEMA)
    except ValidationError as e:
        raise AIResultValidationError(f"Schema validation failed: {e.message}")

def validate_business_rules(ai_result: dict):
    """
    2차 검증: 서비스 정책 기반 검증
    """

    image_success = ai_result.get("image_analysis_success")

    # 이미지 분석 실패 시
    if image_success is False:
        if not ai_result.get("error_reason"):
            raise AIResultValidationError(
                "image_analysis_success is false but error_reason is missing"
            )
        return  # 실패는 허용된 상태

    # 이미지 분석 성공 시
    score = ai_result.get("score")
    conditions = ai_result.get("conditions")

    if not isinstance(score, (int, float)):
        raise AIResultValidationError("score must be a number")

    if score < 0 or score > 100:
        raise AIResultValidationError("score must be between 0 and 100")

    if not isinstance(conditions, list) or len(conditions) == 0:
        raise AIResultValidationError("conditions must be a non-empty list")

    for idx, condition in enumerate(conditions):
        # 🔹 필수 필드 존재 여부
        if (
            "requirement_type" not in condition
            or "requirement" not in condition
            or "satisfied" not in condition
        ):
            raise AIResultValidationError(
                f"condition[{idx}] missing required fields"
            )


        # 🔹 requirement 타입 검증
        if not isinstance(condition["requirement"], str):
            raise AIResultValidationError(
                f"condition[{idx}].requirement must be string"
            )

        # 🔹 satisfied 타입 검증
        if not isinstance(condition["satisfied"], bool):
            raise AIResultValidationError(
                f"condition[{idx}].satisfied must be boolean"
            )


def validate_ai_result(result: dict):
    if "conditions" not in result or not isinstance(result["conditions"], list):
        raise ValueError("conditions missing or invalid")

    for i, cond in enumerate(result["conditions"]):
        for field in ["requirement_type", "requirement", "satisfied"]:
            if field not in cond:
                raise ValueError(f"condition[{i}] missing required fields")

        # reason은 optional로 완화
        if "reason" not in cond:
            cond["reason"] = "AI 판단 사유가 제공되지 않았습니다."
