# 바로GO — 동대문구 출장마사지·홈타이 안내 사이트

서울 동대문구 전지역 방문형 관리(출장마사지·홈타이) 안내용 정적 사이트입니다.
예약전화: **0508-202-4719**

## 구조

- 정적 HTML 사이트 — 어느 호스팅(GitHub Pages, Netlify, 일반 웹서버)에서든 그대로 서빙 가능
- `build.py` + `content/` 패키지에서 페이지를 생성하는 빌드 방식
- 생성물(각 디렉터리의 `index.html`, `sitemap.xml`, `robots.txt`)도 저장소에 포함

```
build.py            # 빌드 스크립트 (레이아웃·글자수 검사·sitemap 생성)
content/
  site.py           # 상호·전화·BASE_URL·메뉴(NAV) 구조
  main.py           # 메인(허브) 페이지 (+ Organization/WebPage/BreadcrumbList/FAQPage JSON-LD)
  areas.py          # 대표동: 허브 + 대표 동 10개
  stations.py       # 역세권: 허브 + 역 10개
  districts.py      # 생활권: 허브 + 생활권 11개
  info.py           # 예약 안내·이용 전 확인사항·홈타이 가이드·고객센터·개인정보·약관
  about.py          # 사이트 소개 (E-E-A-T)
  pricing.py        # 공용 요금 블록
assets/             # CSS(프리미엄 팔레트·Pretendard), 모바일 내비 JS, 파비콘·OG 이미지
```

## URL 구조

- 메인: `/seoul/dongdaemun-gu-chuljangmassage/` (루트 `/` 는 메인으로 리다이렉트)
- 대표동: `/seoul/dongdaemun/<동>-dong-chuljangmassage/`
- 역세권: `/seoul/dongdaemun/<역>-station-chuljangmassage/`
- 생활권: `/seoul/dongdaemun/<거점>-area-chuljangmassage/`
- 안내: `/reservation/`, `/precautions/`, `/hometai-guide/`, `/support/`, `/about/`, `/privacy/`, `/terms/`

## 빌드

```bash
python3 build.py
```

빌드 시 페이지별 본문 글자수 리포트가 출력됩니다.

## SEO 운영 원칙 (빌드에 강제됨)

- 본문 **2,000자 미만 페이지는 자동 `noindex`** 처리되고 sitemap에서 제외
- 메타 디스크립션은 80자 이내로 작성
- 대표동은 10개만 — 번호 행정동(전농1·2동, 답십리1·2동, 장안1·2동, 휘경1·2동, 이문1·2동)은 대표동에 통합, 개별 페이지 없음
- 역은 역 1개당 페이지 1개 — 환승역(청량리·신설동역)도 URL 하나, 출구별·노선별 분리 없음
- **동대문역·동대문역사문화공원역**은 도심 생활권 성격이라 동대문구 핵심 역세권으로 만들지 않음
- 고려대역은 성북구 성격이라 제기동·용두동 인접 생활권으로 처리
- 실제 오프라인 사업장 주소가 없는 방문형 사이트이므로 **LocalBusiness Schema 미사용** (Organization/WebPage 사용)
- 모든 색인 페이지 본문은 페이지별 고유 작성 (지역명만 바꾼 복붙 없음)

## 배포 전 해야 할 일

1. `content/site.py`의 `BASE_URL`을 실제 도메인으로 변경
2. `python3 build.py` 재실행 (canonical·sitemap·robots.txt에 반영됨)
3. Google Search Console에 `sitemap.xml` 제출
