# 색인(인덱싱) 셋업 가이드 — 바로GO 동대문구 출장마사지

목표: **빙·네이버에는 IndexNow로 즉시 통보**, **구글에는 Indexing API/사이트맵**으로 가장 빠르게 색인.

---

## 1. 빌드가 자동 생성하는 파일

`python3 build.py` 한 번이면 루트에 아래가 생성됩니다.

| 파일 | 용도 |
|---|---|
| `sitemap.xml` | 색인 대상 40개 URL (`lastmod`·`changefreq`·`priority` 포함) |
| `rss.xml` | 색인 대상 페이지 RSS 2.0 피드 (엔진 발견 보조, `<head>`에 자동 링크) |
| `robots.txt` | Googlebot·Yeti(네이버)·bingbot·Daumoa 명시 허용 + sitemap 위치 |
| `2eb079a18f2c1ced5eacd236ba79dc06.txt` | **IndexNow 키 파일** (`content/site.py`의 `INDEXNOW_KEY` 기반) |

> 키를 바꾸려면 `content/site.py`의 `INDEXNOW_KEY`만 수정 후 재빌드하면 키파일도 자동 갱신됩니다.

배포 후 확인:
- `https://dongdaemun-massage1.netlify.app/sitemap.xml`
- `https://dongdaemun-massage1.netlify.app/rss.xml`
- `https://dongdaemun-massage1.netlify.app/robots.txt`
- `https://dongdaemun-massage1.netlify.app/2eb079a18f2c1ced5eacd236ba79dc06.txt` ← 키 한 줄만 보이면 정상

---

## 2. 검색엔진 등록 (최초 1회)

### 네이버 서치어드바이저 (https://searchadvisor.naver.com)
1. 사이트 등록 → `https://dongdaemun-massage1.netlify.app/`
2. 소유확인: 메인페이지에 이미 메타태그가 들어가 있습니다(`naver-site-verification`) → **확인** 클릭
3. 요청 → **사이트맵 제출**: `sitemap.xml`
4. 요청 → **RSS 제출**: `rss.xml`

### 구글 서치 콘솔 (https://search.google.com/search-console)
1. 속성 추가 → URL 접두어 `https://dongdaemun-massage1.netlify.app/`
2. 소유확인(HTML 태그 또는 DNS) — 필요 시 메타태그를 추가로 넣어드릴 수 있습니다
3. Sitemaps → `sitemap.xml` 제출
4. URL 검사 → 주요 페이지 **색인 생성 요청**

### 빙 웹마스터 (https://www.bing.com/webmasters)
- 구글 서치 콘솔 연동(Import)으로 한 번에 등록 가능. IndexNow 키도 여기서 확인됩니다.

---

## 3. IndexNow — 빙·네이버 즉시 통보

참여 엔진(Bing·Naver·Yandex·Seznam)에 **즉시 색인 통보**. 한 곳에 보내면 공유되지만,
스크립트는 안정성을 위해 대표 엔드포인트 4곳에 동시 제출합니다.

```bash
# 최초 일괄 통보 — sitemap.xml의 모든 URL
python3 tools/indexnow.py

# 글/페이지를 새로 올렸을 때 — 해당 URL만
python3 tools/indexnow.py https://dongdaemun-massage1.netlify.app/새-경로/
```

전제: **키파일이 실제 도메인에 배포(공개)된 뒤** 실행해야 검증됩니다.
(로컬 빌드 → 배포 → 그다음 통보 순서)

---

## 4. 구글 Indexing API — 구글 즉시 통보 (선택)

구글은 IndexNow 미참여. 즉시 통보하려면 서비스 계정이 필요합니다.

준비(1회):
1. Google Cloud Console → 프로젝트 → **Indexing API** 사용 설정
2. 서비스 계정 생성 → JSON 키 다운로드
3. **서치 콘솔에서 그 서비스 계정 이메일을 사이트 '소유자'로 추가**
4. `pip install google-auth requests`

실행:
```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/service-account.json
python3 tools/google_indexing.py                       # 전체
python3 tools/google_indexing.py https://.../새글/      # 단건
python3 tools/google_indexing.py --deleted https://.../지운글/
```
> 일일 쿼터 기본 200건. 공식 대상은 JobPosting·BroadcastEvent지만 일반 URL에도 널리 사용됩니다.

---

## 5. 새 글/페이지를 올릴 때 루틴

```bash
# 1) content/에 페이지 추가 후
python3 build.py
git add -A && git commit -m "새 페이지" && git push   # → 배포

# 2) 배포 완료 확인 후 즉시 통보
python3 tools/indexnow.py https://dongdaemun-massage1.netlify.app/새-경로/     # 빙·네이버
python3 tools/google_indexing.py https://dongdaemun-massage1.netlify.app/새-경로/   # 구글(선택)
```

---

## 참고: 사이트맵 핑(ping)은 폐지됨

`google.com/ping?sitemap=` 및 빙의 ping 엔드포인트는 **2023년에 폐지**되었습니다.
따라서 자동 ping 대신 위의 **IndexNow + Indexing API + 서치 콘솔 사이트맵 제출**이
현재 가장 빠르고 공식적인 경로입니다.
