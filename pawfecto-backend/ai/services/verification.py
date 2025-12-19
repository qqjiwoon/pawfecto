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
        "score": 100,
        "results": [
            {
                "type": "scene",
                "passed": True,
                "reason": "반려동물이 제품을 사용하는 장면이 이미지에서 확인되었습니다."
            },
            {
                "type": "object",
                "passed": True,
                "reason": "제품이 이미지 내에 명확하게 노출되어 있습니다."
            },
            {
                "type": "text",
                "passed": True,
                "reason": "캡션에 브랜드 요구사항이 충족되었습니다."
            }
        ]
    }
