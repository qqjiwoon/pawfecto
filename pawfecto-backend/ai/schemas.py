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
            "type": "boolean",
            "description": "이미지 분석 성공 여부"
        },
        "conditions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "requirement": {
                        "type": "string",
                        "description": "브랜드 요구사항에서 도출된 검증 조건"
                    },
                    "satisfied": {
                        "type": "boolean",
                        "description": "조건 충족 여부"
                    }
                },
                "required": ["requirement", "satisfied"]
            }
        },
        "score": {
            "type": "number",
            "description": "조건 충족 기반 점수 (100점 만점)"
        },
        "error_reason": {
            "type": ["string", "null"],
            "description": "이미지 분석 실패 시 사유"
        }
    },
    "required": [
        "image_analysis_success",
        "conditions",
        "score"
    ]
}
