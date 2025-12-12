import re


def normalize_place_name(place_name: str) -> str:
    """
    장소명 정규화
    - 괄호 및 괄호 안 제거
    - 특수문자 제거
    - 공백 제거
    """
    if not place_name:
        return ""

    place_name = re.sub(r"\(.*?\)", "", place_name)
    place_name = re.sub(r"[^가-힣a-zA-Z0-9]", "", place_name)

    return place_name.strip()


def generate_ngrams(text: str, n: int = 2) -> set:
    """
    n-gram 생성
    """
    if len(text) < n:
        return set()

    return {text[i:i+n] for i in range(len(text) - n + 1)}


def ngram_containment_similarity(a: str, b: str, n: int = 2) -> float:
    """
    Containment 기반 n-gram 유사도
    |A ∩ B| / |B|
    """
    a_ngrams = generate_ngrams(a, n)
    b_ngrams = generate_ngrams(b, n)

    if not a_ngrams or not b_ngrams:
        return 0.0

    intersection = a_ngrams & b_ngrams
    return len(intersection) / len(b_ngrams)
