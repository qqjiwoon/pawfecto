# ai/schemas.py
# AI 응답 스키마 정의

# 현재 기준
# - AI는 결과만 도출
# - 100점만 pass
# - 이미지 분석 실패 → fail
# - review 없음

DELIVERABLE_AI_RESULT_SCHEMA = {
    "type": "object",
    "properties": {
        "image_analysis_success": {
            "type": "boolean"
        },
        "conditions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "requirement_type": {
                        "type": "string",
                        "enum": ["object", "scene", "action", "text"]
                    },
                    "requirement": {
                        "type": "string"
                    },
                    "satisfied": {
                        "type": "boolean"
                    }
                },
                "required": ["requirement", "satisfied"]
            }
        },
        "score": {
            "type": "number"
        },
        "error_reason": {
            "type": ["string", "null"]
        }
    },
    "required": ["image_analysis_success", "conditions", "score"]
}