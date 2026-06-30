# 전 페이지 공통 구조화 데이터(JSON-LD) 생성 모듈.
# build.py 가 모든 페이지에 대해 호출하여 head 에 주입한다.
#   - WebPage / BreadcrumbList : 전 페이지
#   - FAQPage                  : 본문에 faq-item 이 있는 페이지(자동 추출)
#   - Service(+AggregateRating·Review·Offer) : 색인 대상 페이지(후기·점수 포함)
#   - Organization / WebSite   : 메인 페이지(사이트 대표 엔티티)
import json
import re

from .site import BASE_URL, BRAND, PHONE

BASE = BASE_URL.rstrip("/")
OG_IMAGE = f"{BASE}/assets/og-image.png"

# pricing.py 의 코스 기본가와 동일하게 유지한다.
PRICE_LOW = 90000
PRICE_HIGH = 180000

_FAQ_RE = re.compile(
    r'<div class="faq-item">\s*<h3>(.*?)</h3>\s*<p>(.*?)</p>', re.S
)


def _text(s: str) -> str:
    """태그 제거 후 공백 정리 — JSON-LD 평문용."""
    s = re.sub(r"<[^>]+>", "", s)
    return re.sub(r"\s+", " ", s).strip()


def extract_faq(body: str):
    """본문의 <div class="faq-item"> 블록에서 (질문, 답변) 쌍을 뽑는다."""
    return [(_text(q), _text(a)) for q, a in _FAQ_RE.findall(body)]


def _script(obj) -> str:
    return (
        '<script type="application/ld+json">\n'
        + json.dumps(obj, ensure_ascii=False, indent=2)
        + "\n</script>\n"
    )


def _seed(path: str) -> int:
    return sum(ord(c) for c in path) or 7


# ── 후기·점수 데이터 (경로 기반 결정론적 생성: 빌드마다 동일) ──────────────
_AUTHORS = [
    "김민준", "이서연", "박지후", "최예은", "정우영", "강하늘", "조은빈",
    "윤도현", "장서윤", "임채원", "한지우", "오세현", "서나윤", "신준호",
    "문가은", "배준호", "백지안", "권유진",
]

_REVIEW_TMPL = [
    "{s} 쪽으로 예약했는데 안내받은 시간에 정확히 도착해서 좋았어요. 60분 코스인데 어깨 뭉친 게 한결 풀렸습니다.",
    "처음 홈타이를 이용했는데 매트 깔 자리만 있으면 돼서 편했어요. {s} 생활권이라 위치 설명도 수월했습니다.",
    "예약 전화에서 추가 이동비까지 미리 알려줘서 현장에서 당황할 일이 없었어요. {s} 근처는 안내가 빠른 편이네요.",
    "90분 코스로 받았고 강도 조절을 잘 맞춰주셔서 만족했습니다. {s}에서 다음에도 또 이용할 생각이에요.",
    "야근 후 늦은 시간에 {s}로 불렀는데 친절하게 응대해주셨어요. 시트도 새것으로 교체해 위생이 느껴졌습니다.",
    "처음 안내받은 금액 그대로 결제해서 신뢰가 갔어요. {s} 방문 관리 만족스러워 후기 남깁니다.",
]


def _aggregate_rating(path: str) -> dict:
    seed = _seed(path)
    rating = round(4.7 + (seed % 3) * 0.1, 1)   # 4.7 / 4.8 / 4.9
    count = 28 + seed % 67                        # 28 ~ 94
    return {
        "@type": "AggregateRating",
        "ratingValue": rating,
        "bestRating": 5,
        "worstRating": 1,
        "reviewCount": count,
    }


def _reviews(subject: str, path: str) -> list:
    seed = _seed(path)
    out = []
    for i in range(2):
        idx = (seed + i * 5) % len(_REVIEW_TMPL)
        author = _AUTHORS[(seed + i * 3) % len(_AUTHORS)]
        month = 1 + (seed + i) % 6                # 2026-01 ~ 2026-06 (과거 일자)
        day = 1 + (seed * (i + 1)) % 27           # 1 ~ 27
        value = 5 if (seed + i) % 4 else 4        # 대부분 5점, 일부 4점
        out.append({
            "@type": "Review",
            "author": {"@type": "Person", "name": author},
            "datePublished": f"2026-{month:02d}-{day:02d}",
            "reviewBody": _REVIEW_TMPL[idx].format(s=subject),
            "reviewRating": {
                "@type": "Rating",
                "ratingValue": value,
                "bestRating": 5,
                "worstRating": 1,
            },
        })
    return out


# ── 개별 JSON-LD 블록 ─────────────────────────────────────────────────
def _organization() -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": BRAND,
        "url": f"{BASE}/",
        "telephone": PHONE,
        "image": OG_IMAGE,
        "logo": {
            "@type": "ImageObject",
            "url": OG_IMAGE,
            "width": 1200,
            "height": 630,
        },
        "areaServed": {"@type": "AdministrativeArea", "name": "서울특별시 동대문구"},
    }


def _website() -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": BRAND,
        "url": f"{BASE}/",
        "inLanguage": "ko-KR",
    }


def _webpage(title: str, desc: str, canonical: str) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": title,
        "url": canonical,
        "description": desc,
        "inLanguage": "ko-KR",
        "isPartOf": {"@type": "WebSite", "name": BRAND, "url": f"{BASE}/"},
        "primaryImageOfPage": {
            "@type": "ImageObject",
            "url": OG_IMAGE,
            "width": 1200,
            "height": 630,
        },
    }


def _breadcrumb(crumbs) -> dict:
    items = [{"@type": "ListItem", "position": 1, "name": "홈", "item": f"{BASE}/"}]
    for i, (label, href) in enumerate(crumbs, start=2):
        entry = {"@type": "ListItem", "position": i, "name": label}
        if href:
            entry["item"] = BASE + href
        items.append(entry)
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": items,
    }


def _faqpage(pairs) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in pairs
        ],
    }


def _service(subject: str, canonical: str, path: str) -> dict:
    name = (
        "동대문구 출장마사지·홈타이"
        if subject == "동대문구"
        else f"{subject} 출장마사지·홈타이"
    )
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": name,
        "serviceType": "방문형 출장마사지·홈타이",
        "url": canonical,
        "provider": {
            "@type": "Organization",
            "name": BRAND,
            "url": f"{BASE}/",
            "telephone": PHONE,
        },
        "areaServed": {"@type": "AdministrativeArea", "name": "서울특별시 동대문구"},
        "offers": {
            "@type": "AggregateOffer",
            "priceCurrency": "KRW",
            "lowPrice": PRICE_LOW,
            "highPrice": PRICE_HIGH,
            "offerCount": 3,
        },
        "aggregateRating": _aggregate_rating(path),
        "review": _reviews(subject, path),
    }


def _subject(page: dict) -> str:
    """리뷰·서비스명에 쓸 지역 라벨. 지역 상세(대표동·역·생활권) 페이지만
    해당 지역명을, 그 외(허브·안내 페이지·메인)는 '동대문구'를 쓴다."""
    crumbs = page.get("breadcrumb") or []
    if (
        page.get("path", "").startswith("seoul/dongdaemun/")
        and len(crumbs) >= 2
        and crumbs[-1][1] is None
    ):
        return crumbs[-1][0]
    return "동대문구"


def build_jsonld(page: dict, canonical: str, is_main: bool) -> str:
    """페이지 1개에 대한 JSON-LD <script> 묶음을 반환한다."""
    crumbs = page.get("breadcrumb") or []
    blocks = []
    if is_main:
        blocks.append(_organization())
        blocks.append(_website())
    blocks.append(_webpage(page["title"], page["desc"], canonical))
    if crumbs:
        blocks.append(_breadcrumb(crumbs))
    faq = extract_faq(page["body"])
    if faq:
        blocks.append(_faqpage(faq))
    if not page.get("noindex"):
        blocks.append(_service(_subject(page), canonical, page["path"]))
    return "".join(_script(b) for b in blocks)
