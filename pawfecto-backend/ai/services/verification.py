# ai/services/verification.py
# AI 검증 실행 서비스 (mock 단계)

def run_ai_verification(prompt: str, images: list):
    """
    AI 검증 실행
    - prompt: myapp에서 조합한 전체 프롬프트
    - images: 이미지 경로 리스트 (string)
    
    반환값은 schemas / validators에서 정의한 형식을 따른다.
    """

    # NOTE:
    # 현재는 GMS 연동 전 mock 단계이므로
    # 항상 성공 케이스를 반환한다.
    # 이후 이 함수 내부를 실제 GMS API 호출로 교체한다.

    return {
        "image_analysis_success": True,
        "conditions": [
            {
                "requirement": "사료를 급여하는 장면 포함",
                "satisfied": True
            },
            {
                "requirement": "제품이 이미지에 노출되어야 함",
                "satisfied": True
            },
            {
                "requirement": "캡션에 브랜드명이 포함되어야 함",
                "satisfied": True
            }
        ],
        "score": 100,
        "error_reason": None
    }
