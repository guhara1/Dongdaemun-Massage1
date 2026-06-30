#!/usr/bin/env python3
"""바로GO 동대문구 출장마사지·홈타이 — 정적 사이트 빌드 스크립트.

content/ 패키지의 페이지 정의를 읽어 정적 HTML을 생성한다.

규칙(자동 적용):
  - 본문 텍스트 2,000자 미만 페이지는 robots noindex 처리
  - sitemap.xml 에는 index 허용 페이지만 포함
  - 지역+역+테마 조합 경로는 생성 자체가 불가능한 구조
"""
import html
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import date

from content import PAGES, schema
from content.site import (BASE_URL, BRAND, BRAND_DESC, NAV, PHONE,
                          PHONE_DISPLAY, MAIN_PATH, MAIN_URL, INDEXNOW_KEY)

ROOT = os.path.dirname(os.path.abspath(__file__))
MIN_INDEX_CHARS = 2000

# 내부링크 강화 — 롱테일 앵커텍스트로 허브·안내 페이지를 상호 연결한다.
# 지역 상세(대표동·역·생활권) 페이지용 세트와 안내 페이지용 세트로 나눈다.
RELATED_LOCATION = [
    ("/seoul/dongdaemun/areas/", "동대문구 대표동별 출장마사지·홈타이 안내"),
    ("/seoul/dongdaemun/stations/", "청량리·회기·장한평 역세권 출장마사지 안내"),
    ("/seoul/dongdaemun/districts/", "동대문구 생활권별 방문 관리 안내"),
    ("/reservation/", "출장마사지 예약 방법·가능 시간·이동비 안내"),
    ("/hometai-guide/", "홈타이 처음 이용 가이드와 코스 선택 기준"),
    ("/precautions/", "방문 전 주소·출입·개인정보 확인사항"),
]
RELATED_INFO = [
    ("/seoul/dongdaemun/areas/", "동대문구 대표동별 출장마사지·홈타이 안내"),
    ("/seoul/dongdaemun/stations/", "동대문구 주요 역세권 출장마사지 안내"),
    ("/seoul/dongdaemun/districts/", "동대문구 생활권별 방문 관리 안내"),
    ("/reservation/", "예약 방법과 가능 시간·결제 기준 안내"),
    ("/hometai-guide/", "홈타이와 출장마사지 차이·이용 가이드"),
    ("/support/", "자주 묻는 질문과 고객센터 안내"),
]


def render_related(path: str) -> str:
    """페이지 하단 내부링크 블록(관련 안내). 자기 자신은 제외한다."""
    table = RELATED_LOCATION if path.startswith("seoul/dongdaemun/") else RELATED_INFO
    self_href = "/" + path
    items = [(h, t) for h, t in table if h != self_href][:6]
    links = "".join(
        f'<li><a href="{h}">{t}</a></li>' for h, t in items
    )
    return (
        '<nav class="related-links" aria-label="관련 안내">'
        '<p class="related-title">이런 페이지도 함께 보세요</p>'
        f'<ul class="related-grid">{links}</ul></nav>'
    )


def insert_related(body: str, related: str) -> str:
    """요금·CTA 블록 바로 앞에 관련 링크 블록을 끼워 넣는다."""
    for marker in ('<section class="pricing">', '<section class="cta">'):
        idx = body.find(marker)
        if idx != -1:
            return body[:idx] + related + body[idx:]
    return body + related


def text_length(body_html: str) -> int:
    """태그를 제거한 본문 글자수(공백 포함, 연속 공백은 1자).
    공통 요금 블록은 페이지 고유 본문이 아니므로 측정에서 제외한다."""
    text = re.sub(r'<section class="pricing">.*?</section>', " ", body_html, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return len(text)


def render_nav(current_path: str) -> str:
    items = []
    for label, href, children in NAV:
        active = " is-active" if href == "/" + current_path else ""
        if children:
            sub = "".join(
                f'<li><a href="{c_href}">{c_label}</a></li>'
                for c_label, c_href in children
            )
            items.append(
                f'<li class="nav-item has-sub{active}">'
                f'<a href="{href}">{label}</a>'
                f'<ul class="sub-menu">{sub}</ul></li>'
            )
        else:
            items.append(
                f'<li class="nav-item{active}"><a href="{href}">{label}</a></li>'
            )
    return "".join(items)


def render_breadcrumb(crumbs) -> str:
    if not crumbs:
        return ""
    parts = ['<nav class="breadcrumb" aria-label="현재 위치"><ol>']
    parts.append('<li><a href="/">홈</a></li>')
    for label, href in crumbs:
        if href:
            parts.append(f'<li><a href="{href}">{label}</a></li>')
        else:
            parts.append(f"<li><span>{label}</span></li>")
    parts.append("</ol></nav>")
    return "".join(parts)


def inject_toc(body: str):
    """본문 섹션(h2)에 id를 보장하고 좌측 목차 데이터를 만든다."""
    items = []
    counter = [0]

    def repl(m):
        attrs, title = m.group(1), m.group(2)
        idm = re.search(r'id="([^"]+)"', attrs)
        if idm:
            sid = idm.group(1)
            opening = f"<section{attrs}>"
        else:
            counter[0] += 1
            sid = f"sec-{counter[0]}"
            opening = f'<section id="{sid}"{attrs}>'
        label = re.sub(r"<[^>]+>", "", title).strip()
        items.append((sid, label))
        return f"{opening}<h2>{title}</h2>"

    body = re.sub(r"<section([^>]*)>\s*<h2>(.*?)</h2>", repl, body, flags=re.S)
    return body, items


def render_toc(items) -> str:
    if len(items) < 3:
        return ""
    links = "".join(
        f'<li><a href="#{sid}">{label}</a></li>' for sid, label in items
    )
    return (
        '<aside class="page-toc"><nav aria-label="페이지 목차">'
        '<p class="toc-title">목차</p>'
        f"<ul>{links}</ul></nav></aside>"
    )


def render_page(page: dict) -> str:
    path = page["path"]
    title = page["title"]
    desc = page["desc"]
    h1 = page["h1"]
    body = page["body"]
    crumbs = page.get("breadcrumb") or []
    extra_head = page.get("extra_head", "")
    hero = page.get("hero", "")

    chars = text_length(body)
    noindex = page.get("noindex", False) or chars < MIN_INDEX_CHARS
    robots = (
        '<meta name="robots" content="noindex,follow">'
        if noindex
        else '<meta name="robots" content="index,follow">'
    )
    canonical = BASE_URL.rstrip("/") + "/" + path

    # 구조화 데이터(JSON-LD) — 전 페이지 자동 주입.
    is_main = path == MAIN_PATH
    schema_html = schema.build_jsonld(page, canonical, is_main)

    # 내부링크 강화 블록 — 색인 대상 페이지에만 넣는다.
    if not noindex:
        body = insert_related(body, render_related(path))

    # 히어로가 있는 페이지(메인)는 H1을 히어로 안에서 출력한다.
    if hero:
        page_head = hero
    else:
        page_head = ""

    h1_html = "" if hero else f"<h1>{h1}</h1>"

    body, toc_items = inject_toc(body)
    toc_html = render_toc(toc_items)
    layout_cls = "page-layout has-toc" if toc_html else "page-layout"

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{robots}
<link rel="canonical" href="{canonical}">
<link rel="alternate" type="application/rss+xml" title="{BRAND}" href="{BASE_URL.rstrip('/')}/rss.xml">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:image" content="{BASE_URL.rstrip('/')}/assets/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{BASE_URL.rstrip('/')}/assets/og-image.png">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<meta name="theme-color" content="#0a1120">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@600;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/style.css">
{schema_html}{extra_head}</head>
<body>
<header class="site-header">
  <div class="header-accent" aria-hidden="true"></div>
  <div class="header-top">
    <div class="header-inner">
      <a class="brand" href="{MAIN_URL}"><span class="brand-mark">바</span> <span class="brand-text">{BRAND}</span></a>
      <p class="header-tagline"><span class="tag-gem">◆</span> 동대문구 전지역 방문 관리 <span class="tag-gem">◆</span> 24시간 상담</p>
      <a class="header-call" href="tel:{PHONE}"><span class="call-label">예약전화</span> {PHONE_DISPLAY}</a>
      <button class="nav-toggle" aria-label="메뉴 열기" aria-expanded="false"><span></span><span></span><span></span></button>
    </div>
  </div>
  <nav class="main-nav" aria-label="주 메뉴">
    <div class="nav-inner"><ul class="nav-list">{render_nav(path)}</ul></div>
  </nav>
</header>
{page_head}<main class="site-main">
  <div class="container {layout_cls}">
    {toc_html}
    <article class="page-content">
      {render_breadcrumb(crumbs)}
      {h1_html}
      {body}
    </article>
  </div>
</main>
<footer class="site-footer">
  <div class="container footer-grid">
    <div class="footer-col footer-about">
      <p class="footer-brand">{BRAND}</p>
      <p class="footer-desc">동대문구 전지역 방문형 출장마사지·홈타이 안내 사이트입니다. 모든 서비스는 안내된 관리 범위와 위생·안전 기준 안에서만 제공됩니다.</p>
      <address class="footer-contact">
        <span class="footer-contact-row"><span class="footer-label">예약전화</span> <a href="tel:{PHONE}">{PHONE_DISPLAY}</a></span>
        <span class="footer-contact-row"><span class="footer-label">상담시간</span> 연중무휴 24시간</span>
        <span class="footer-contact-row"><span class="footer-label">서비스 지역</span> 서울특별시 동대문구 전지역</span>
      </address>
    </div>
    <nav class="footer-col" aria-label="지역 안내">
      <p class="footer-title">지역 안내</p>
      <ul>
        <li><a href="{MAIN_URL}">동대문구 출장마사지</a></li>
        <li><a href="/seoul/dongdaemun/areas/">지역별 안내</a></li>
        <li><a href="/seoul/dongdaemun/stations/">역세권 안내</a></li>
        <li><a href="/seoul/dongdaemun/districts/">생활권 안내</a></li>
        <li><a href="/hometai-guide/">홈타이 이용 가이드</a></li>
      </ul>
    </nav>
    <nav class="footer-col" aria-label="이용 안내">
      <p class="footer-title">이용 안내</p>
      <ul>
        <li><a href="/reservation/">예약 안내</a></li>
        <li><a href="/precautions/">이용 전 확인사항</a></li>
        <li><a href="/support/">고객센터</a></li>
        <li><a href="/support/#faq">자주 묻는 질문</a></li>
        <li><a href="/support/#biz">제휴·기업 문의</a></li>
      </ul>
    </nav>
    <nav class="footer-col" aria-label="정책 및 기준">
      <p class="footer-title">정책</p>
      <ul>
        <li><a href="/about/">사이트 소개</a></li>
        <li><a href="/privacy/">개인정보 처리방침</a></li>
        <li><a href="/terms/">이용약관</a></li>
        <li><a href="/precautions/#safety">위생·안전 기준</a></li>
        <li><a href="/precautions/#prohibited">불법·선정적 서비스 불가</a></li>
      </ul>
    </nav>
  </div>
  <div class="footer-bottom">
    <div class="container footer-bottom-inner">
      <p class="footer-copy">&copy; {BRAND}. All rights reserved.</p>
      <p class="footer-note">건전한 방문 관리 서비스를 운영하며, 불법적인 요청은 어떤 경우에도 응하지 않습니다.</p>
      <div class="footer-tg-row">
        <a class="footer-tg-btn" href="https://t.me/googleseolab" target="_blank" rel="noopener nofollow">
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9.78 18.65l.28-4.23 7.68-6.92c.34-.31-.07-.46-.52-.19L7.74 13.3 3.64 12c-.88-.25-.89-.86.2-1.3l15.97-6.16c.73-.33 1.43.18 1.15 1.3l-2.72 12.81c-.19.91-.74 1.13-1.5.71l-4.14-3.05-1.99 1.93c-.23.23-.42.42-.83.42z"/></svg>
          웹사이트 제작문의
        </a>
        <a class="footer-tg-btn" href="https://t.me/googleseolab" target="_blank" rel="noopener nofollow">
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9.78 18.65l.28-4.23 7.68-6.92c.34-.31-.07-.46-.52-.19L7.74 13.3 3.64 12c-.88-.25-.89-.86.2-1.3l15.97-6.16c.73-.33 1.43.18 1.15 1.3l-2.72 12.81c-.19.91-.74 1.13-1.5.71l-4.14-3.05-1.99 1.93c-.23.23-.42.42-.83.42z"/></svg>
          제휴문의
        </a>
      </div>
    </div>
  </div>
</footer>
<a class="call-fab" href="tel:{PHONE}" aria-label="전화 예약 {PHONE_DISPLAY}">
  <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>
  <span class="call-fab-label">예약 전화</span>
</a>
<script src="/assets/nav.js"></script>
</body>
</html>
"""


def esc(s: str) -> str:
    """RSS/XML 텍스트용 이스케이프."""
    return html.escape(s, quote=False)


def build() -> None:
    report = []
    sitemap_urls = []
    index_pages = []  # (loc, title, desc) — sitemap·rss 공용

    for page in PAGES:
        path = page["path"]  # "seoul/dongdaemun/sinseol-dong-chuljangmassage/" 형태
        out_dir = os.path.join(ROOT, path)
        os.makedirs(out_dir, exist_ok=True)
        html_out = render_page(page)
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(html_out)

        chars = text_length(page["body"])
        noindex = page.get("noindex", False) or chars < MIN_INDEX_CHARS
        if not noindex:
            loc = BASE_URL.rstrip("/") + "/" + path
            sitemap_urls.append(loc)
            index_pages.append((loc, page["title"], page["desc"]))
        report.append((path or "/", chars, "noindex" if noindex else "index"))

    base = BASE_URL.rstrip("/")
    today = date.today().isoformat()

    # sitemap.xml — lastmod 포함
    urls = "\n".join(
        f"  <url><loc>{u}</loc><lastmod>{today}</lastmod>"
        f"<changefreq>weekly</changefreq>"
        f"<priority>{'1.0' if u == base + '/' else '0.8'}</priority></url>"
        for u in sitemap_urls
    )
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            f"{urls}\n</urlset>\n"
        )

    # rss.xml — 색인 대상 페이지 피드 (빙·네이버·구글 발견 보조)
    now_rfc = date.today().strftime("%a, %d %b %Y 00:00:00 +0900")
    items = "\n".join(
        "  <item>"
        f"<title>{esc(title)}</title>"
        f"<link>{loc}</link>"
        f"<guid isPermaLink=\"true\">{loc}</guid>"
        f"<description>{esc(desc)}</description>"
        f"<pubDate>{now_rfc}</pubDate>"
        "</item>"
        for loc, title, desc in index_pages
    )
    with open(os.path.join(ROOT, "rss.xml"), "w", encoding="utf-8") as f:
        f.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
            "<channel>\n"
            f"  <title>{esc(BRAND)}</title>\n"
            f"  <link>{base}/</link>\n"
            f'  <atom:link href="{base}/rss.xml" rel="self" type="application/rss+xml" />\n'
            f"  <description>{esc(BRAND_DESC)}</description>\n"
            "  <language>ko-KR</language>\n"
            f"  <lastBuildDate>{now_rfc}</lastBuildDate>\n"
            f"{items}\n"
            "</channel>\n</rss>\n"
        )

    # robots.txt — 주요 봇 명시 허용 + sitemap
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(
            "User-agent: *\n"
            "Allow: /\n\n"
            "# 검색엔진 크롤러 명시 허용\n"
            "User-agent: Googlebot\nAllow: /\n\n"
            "User-agent: Yeti\nAllow: /\n\n"          # Naver
            "User-agent: bingbot\nAllow: /\n\n"
            "User-agent: Daumoa\nAllow: /\n\n"        # Daum/Kakao
            f"Sitemap: {base}/sitemap.xml\n"
        )

    # IndexNow 키 파일 — https://도메인/<KEY>.txt 에서 키를 검증한다
    with open(os.path.join(ROOT, f"{INDEXNOW_KEY}.txt"), "w", encoding="utf-8") as f:
        f.write(INDEXNOW_KEY + "\n")

    # .nojekyll (GitHub Pages)
    open(os.path.join(ROOT, ".nojekyll"), "w").close()

    width = max(len(p) for p, _, _ in report)
    print(f"{'PATH'.ljust(width)}  CHARS  ROBOTS")
    for p, c, r in sorted(report):
        flag = "" if (r == "noindex" or MIN_INDEX_CHARS <= c <= 2500) else "  ⚠"
        print(f"{p.ljust(width)}  {str(c).rjust(5)}  {r}{flag}")
    print(f"\n{len(report)} pages built, {len(sitemap_urls)} in sitemap.")


if __name__ == "__main__":
    build()
