from PaymentApp.Utils.placenormalizer import normalize_place_name, ngram_containment_similarity

# 🔹 카테고리 룰 (DB 카테고리와 1:1 대응 가능)
CATEGORY_RULES = {
    "카페": ["카페", "스타벅스", "이디야", "투썸", "메가커피", "빽다방", "우지커피", "컴포즈", "바나프레소", "커피빈",
           "숨맑은집", "엔제리너스", "할리스", "감성커피"],
    "편의점": ["CU", "씨유", "GS25", "지에스25", "세븐일레븐", "이마트24"],
    "패스트푸드": ["롯데리아", "맥도날드", "버거킹", "KFC", "맘스터치"],
    "식당": ["김밥천국", "한솥", "본죽", "홍콩반점"],
    "문화/여가": ["CGV", "메가박스", "롯데시네마", "PC방", "피시", "피씨"],
    "금융": ["토스", "카카오뱅크", "신한", "국민", "이체", "입금", "출금", "신영미", "이건민"],
    "기타": []
}

NGRAM_SIZE = 2
SIMILARITY_THRESHOLD = 0.5  # n-gram 기준에서는 0.4~0.5가 적절


def classify_place_category(place_name: str) -> str:
    """
    n-gram 기반 장소 카테고리 분류
    """
    normalized = normalize_place_name(place_name)

    best_category = "기타"
    best_score = 0.0

    for category, keywords in CATEGORY_RULES.items():
        for keyword in keywords:
            score = ngram_containment_similarity(normalized, keyword, NGRAM_SIZE)
            if score > best_score:
                best_score = score
                best_category = category

    if best_score >= SIMILARITY_THRESHOLD:
        return best_category

    return "기타"


def is_financial_category(category: str) -> bool:
    """
    금융 카테고리 여부 판단 (소비 합산 제외용)
    """
    return category == "금융"