# 메인 페이지 — 동대문구 출장마사지·홈타이 허브. 키워드를 몰아넣지 않고 상세 페이지로 연결한다.
from .site import BASE_URL, BRAND, PHONE, PHONE_DISPLAY, MAIN_PATH, MAIN_URL
from .pricing import PRICING

_CANON = BASE_URL.rstrip("/") + MAIN_URL

# 실제 오프라인 사업장 주소가 없는 방문형 사이트이므로 LocalBusiness 대신
# Organization / WebPage / BreadcrumbList / ImageObject / FAQPage 만 사용한다.
_JSONLD = f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "{BRAND}",
  "url": "{_CANON}",
  "telephone": "{PHONE}",
  "logo": {{
    "@type": "ImageObject",
    "url": "{BASE_URL.rstrip('/')}/assets/og-image.png",
    "width": 1200,
    "height": 630
  }},
  "areaServed": {{
    "@type": "AdministrativeArea",
    "name": "서울특별시 동대문구"
  }}
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "동대문구 출장마사지·동대문구 홈타이 지역별 예약 안내",
  "url": "{_CANON}",
  "description": "동대문구 출장마사지·홈타이 예약 전 청량리, 회기, 장안동, 답십리 생활권을 확인하세요.",
  "primaryImageOfPage": {{
    "@type": "ImageObject",
    "url": "{BASE_URL.rstrip('/')}/assets/og-image.png",
    "width": 1200,
    "height": 630
  }},
  "inLanguage": "ko-KR",
  "isPartOf": {{ "@type": "WebSite", "name": "{BRAND}", "url": "{BASE_URL.rstrip('/')}/" }}
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {{
      "@type": "Question",
      "name": "동대문구 전지역 방문이 가능한가요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "예약 시간, 정확한 위치, 배정 상황에 따라 가능 여부가 달라집니다. 지역별 안내에서 신설동, 용두동, 제기동, 전농동, 답십리동, 장안동, 청량리동, 회기동, 휘경동, 이문동 기준으로 확인할 수 있습니다."
      }}
    }},
    {{
      "@type": "Question",
      "name": "전농1동·전농2동은 왜 따로 없나요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "전농1동·전농2동, 답십리1·2동, 장안1·2동, 휘경1·2동, 이문1·2동처럼 번호로 나뉜 행정동은 각 대표 동 페이지에서 세부 생활권으로 통합 안내하여 중복 페이지 위험을 줄입니다."
      }}
    }},
    {{
      "@type": "Question",
      "name": "동대문역도 동대문구 역세권으로 안내하나요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "동대문역과 동대문역사문화공원역은 이름과 달리 종로·중구 도심 생활권 성격이 강해 동대문구 핵심 역세권으로 다루지 않습니다. 동대문구 역세권은 청량리역, 회기역, 신설동역, 장한평역을 중심으로 안내합니다."
      }}
    }}
  ]
}}
</script>
"""

_HERO = f"""<section class="hero">
  <div class="hero-inner">
    <p class="hero-badge">Premium Visiting Spa · 서울 동대문구 전지역</p>
    <h1>동대문구 출장마사지·홈타이<br>지역별 예약 안내</h1>
    <p class="hero-lead">샵까지 갈 필요 없이, 계신 곳에서 받는 방문형 관리 서비스.<br>청량리·회기·장안·답십리 생활권을 확인하고 전화 한 통으로 예약하세요.</p>
    <div class="hero-actions">
      <a class="hero-btn primary" href="tel:{PHONE}">📞 {PHONE_DISPLAY}</a>
      <a class="hero-btn" href="/seoul/dongdaemun/areas/">대표동 안내 보기</a>
    </div>
    <ul class="hero-stats">
      <li><strong>10개</strong><span>대표동</span></li>
      <li><strong>10개</strong><span>역세권</span></li>
      <li><strong>11개</strong><span>생활권</span></li>
      <li><strong>24시간</strong><span>예약 상담</span></li>
    </ul>
  </div>
</section>
"""

_BODY = f"""
<section id="standard">
<h2>동대문구에서 출장마사지를 찾을 때 먼저 확인할 기준</h2>
<p>동대문구 출장마사지를 찾는 분들은 보통 현재 위치에서 가까운 방문 가능 지역을 먼저 확인합니다. 동대문구는 서울 동북권과 도심을 연결하는 지역으로, 청량리역을 중심으로 한 교통 생활권, 회기역과 외대앞역 주변의 대학가 생활권, 장안동과 답십리동의 주거지 생활권, 신설동과 용두동의 도심 인접 생활권이 함께 있습니다. 그래서 이 사이트는 “동대문 전지역 가능”만 반복하는 방식 대신, 대표동과 역세권, 생활권을 나누어 안내하는 구조로 만들었습니다. 예약 전에는 방문 가능 주소, 예약 가능 시간, 추가 이동비 여부, 결제 방식, 취소 기준, 개인정보 처리 기준을 먼저 확인하시는 것이 좋습니다.</p>
</section>

<section id="difference">
<h2>청량리·회기·장안·답십리 생활권 차이</h2>
<p>같은 동대문구라도 생활권마다 분위기와 이동 조건이 다릅니다. 청량리역 일대는 지하철과 철도, 버스 환승 수요가 큰 교통 중심 상권이고, 회기역과 외대앞역 주변은 경희대·한국외대 학생과 직장인이 섞인 대학가 생활권입니다. 장안동과 답십리동은 천호대로와 중랑천을 끼고 형성된 주거지 생활권이며, 신설동과 용두동은 도심과 맞닿은 서쪽 생활권입니다. 생활권에 따라 방문 시간대와 차량 이동 기준이 달라질 수 있어, 각 페이지에 지역별 이동 기준을 분명하게 적어 두었습니다. 본인 생활 패턴과 가까운 생활권을 먼저 확인하면 필요한 정보를 더 빨리 찾을 수 있습니다.</p>
</section>

<section id="areas">
<h2>대표동별 방문 가능 지역 안내</h2>
<p>대표동은 신설동, 용두동, 제기동, 전농동, 답십리동, 장안동, 청량리동, 회기동, 휘경동, 이문동으로 구성합니다. 전농1동·전농2동, 답십리1·2동, 장안1·2동, 휘경1·2동, 이문1·2동처럼 번호로 나뉜 행정동은 개별 페이지로 만들지 않고 대표동 안에서 세부 생활권으로 설명합니다. 각 페이지에서는 해당 생활권의 특징과 가까운 역, 방문 전 확인사항을 동마다 고유한 내용으로 안내합니다.</p>
<ul class="card-grid">
<li><a href="/seoul/dongdaemun/sinseol-dong-chuljangmassage/">신설동</a></li>
<li><a href="/seoul/dongdaemun/yongdu-dong-chuljangmassage/">용두동</a></li>
<li><a href="/seoul/dongdaemun/jegi-dong-chuljangmassage/">제기동</a></li>
<li><a href="/seoul/dongdaemun/jeonnong-dong-chuljangmassage/">전농동</a></li>
<li><a href="/seoul/dongdaemun/dapsimni-dong-chuljangmassage/">답십리동</a></li>
<li><a href="/seoul/dongdaemun/jangan-dong-chuljangmassage/">장안동</a></li>
<li><a href="/seoul/dongdaemun/cheongnyangni-dong-chuljangmassage/">청량리동</a></li>
<li><a href="/seoul/dongdaemun/hoegi-dong-chuljangmassage/">회기동</a></li>
<li><a href="/seoul/dongdaemun/hwigyeong-dong-chuljangmassage/">휘경동</a></li>
<li><a href="/seoul/dongdaemun/imun-dong-chuljangmassage/">이문동</a></li>
</ul>
<p>동대문구 전체 구성이 궁금하시면 <a href="/seoul/dongdaemun/areas/">지역별 안내 허브</a>에서 한눈에 확인하실 수 있습니다.</p>
</section>

<section id="stations">
<h2>청량리역·회기역·신설동역·장한평역 역세권 안내</h2>
<p>역세권 안내는 실제 검색 의도가 분명한 역을 기준으로 구성합니다. 청량리역, 회기역, 외대앞역, 신이문역, 제기동역, 신설동역, 용두역, 답십리역, 장한평역과 고려대역 인접 생활권을 다룹니다. 환승역은 노선별로 쪼개지 않고 역마다 페이지를 하나만 운영하며, 본문에서 환승 특징을 설명합니다. 다만 동대문역과 동대문역사문화공원역은 이름과 달리 도심 생활권 성격이 강해 동대문구 핵심 역세권으로 다루지 않습니다.</p>
<ul class="card-grid">
<li><a href="/seoul/dongdaemun/cheongnyangni-station-chuljangmassage/">청량리역</a></li>
<li><a href="/seoul/dongdaemun/hoegi-station-chuljangmassage/">회기역</a></li>
<li><a href="/seoul/dongdaemun/hankuk-univ-foreign-studies-station-chuljangmassage/">외대앞역</a></li>
<li><a href="/seoul/dongdaemun/sinimun-station-chuljangmassage/">신이문역</a></li>
<li><a href="/seoul/dongdaemun/jegi-dong-station-chuljangmassage/">제기동역</a></li>
<li><a href="/seoul/dongdaemun/sinseol-dong-station-chuljangmassage/">신설동역</a></li>
<li><a href="/seoul/dongdaemun/yongdu-station-chuljangmassage/">용두역</a></li>
<li><a href="/seoul/dongdaemun/dapsimni-station-chuljangmassage/">답십리역</a></li>
<li><a href="/seoul/dongdaemun/janghanpyeong-station-chuljangmassage/">장한평역</a></li>
<li><a href="/seoul/dongdaemun/korea-univ-nearby-area-chuljangmassage/">고려대역 인접 생활권</a></li>
</ul>
<p>생활권·주요 거점 기준 안내는 <a href="/seoul/dongdaemun/districts/">생활권 안내 허브</a>에서 확인하세요.</p>
</section>

<section id="check">
<h2>동대문구 홈타이 예약 전 확인사항</h2>
<p>동대문구 홈타이는 자택, 숙소, 사무실 인근에서 예약 가능 여부를 확인한 뒤 이용하는 방문형 관리 서비스입니다. 청량리역과 회기역처럼 교통 접근성이 좋은 지역도 있지만, 장안동, 답십리동, 이문동 일부 지역은 시간대에 따라 차량 이동 기준이 달라질 수 있습니다. 예약 전에는 <a href="/reservation/">예약 안내</a>에서 가능 시간과 결제 방식, 취소 기준을, <a href="/precautions/">이용 전 확인사항</a>에서 방문 가능 주소와 개인정보 처리 기준을 확인해 주세요. 홈타이가 처음이라면 <a href="/hometai-guide/">홈타이 이용 가이드</a>가 도움이 됩니다.</p>
</section>

<section id="dedup">
<h2>동대문구 페이지 중복 방지 운영 기준</h2>
<p>동대문구 사이트에서 가장 중요한 운영 기준은 번호 동을 무리하게 쪼개지 않는 것입니다. 전농1동과 전농2동, 답십리1동과 답십리2동, 장안1동과 장안2동, 휘경1동과 휘경2동, 이문1동과 이문2동을 각각 개별 페이지로 만들면 본문이 비슷해질 위험이 큽니다. 그래서 대표동 기준으로 통합하고, 같은 본문에서 지역명만 바꾸는 방식은 사용하지 않습니다. 청량리역처럼 환승 수요가 큰 역도 노선별 페이지를 만들지 않고 하나의 URL로 운영합니다. 고려대역은 성북구 성격이 있어 제기동·용두동 인접 생활권으로 처리합니다.</p>
</section>

<section id="howto">
<h2>동대문구 출장마사지 사이트 이용 방법</h2>
<p>거주하거나 머무시는 동이 분명하면 대표동 페이지를, 역 기준 위치가 익숙하면 역세권 페이지를, 상권·대학가·주거지 같은 생활권 기준이 편하면 생활권 페이지를 보시면 됩니다. 어느 페이지를 보셔도 예약 절차와 비용 기준은 동일하며, 최종 안내는 언제나 정확한 주소를 기준으로 이루어집니다. 메인 페이지는 동대문구 전체 구조를 안내하는 허브 역할을 하고, 세부 정보는 각 상세 페이지에서 고유하게 설명합니다.</p>
</section>

{PRICING}
<section id="contact" class="cta">
<h2>예약문의</h2>
<p>동대문구 방문형 관리 예약과 상담은 전화로 가장 빠르게 진행됩니다. 위치와 희망 시간을 알려주시면 가능 여부를 바로 확인해 드립니다.</p>
<a class="cta-phone" href="tel:{PHONE}">{PHONE_DISPLAY}</a>
</section>
"""

PAGE = {
    "path": MAIN_PATH,
    "title": "동대문구 출장마사지｜청량리·회기·장안·답십리 홈타이 지역 안내",
    "desc": "동대문구 출장마사지·홈타이 예약 전 청량리, 회기, 장안동, 답십리 생활권을 확인하세요.",
    "h1": "동대문구 출장마사지 · 동대문구 홈타이 지역별 예약 안내",
    "body": _BODY,
    "extra_head": _JSONLD,
    "breadcrumb": [],
    "hero": _HERO,
}
