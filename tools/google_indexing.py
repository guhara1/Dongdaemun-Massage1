#!/usr/bin/env python3
"""Google Indexing API 색인 통보 스크립트.

구글은 IndexNow에 참여하지 않으므로, 구글에 즉시 통보하려면 Indexing API를
사용합니다. 서비스 계정 키(JSON)가 필요합니다.

준비 (1회):
  1) Google Cloud Console에서 프로젝트 생성 → "Indexing API" 사용 설정
  2) 서비스 계정 생성 → JSON 키 다운로드
  3) Google Search Console에서 해당 사이트 속성에 서비스 계정 이메일을
     '소유자(Owner)'로 추가
  4) pip install google-auth requests

사용법:
  export GOOGLE_APPLICATION_CREDENTIALS=/path/service-account.json

  # sitemap.xml의 모든 URL 통보
  python tools/google_indexing.py

  # 특정 URL만 통보 (새 글)
  python tools/google_indexing.py https://도메인/새글/

  # 삭제 통보
  python tools/google_indexing.py --deleted https://도메인/지운글/

참고: Indexing API는 공식적으로 JobPosting·BroadcastEvent 대상이지만,
      일반 URL 통보에도 널리 쓰입니다. 일일 호출 쿼터(기본 200건)가 있습니다.
"""
import os
import sys
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
SCOPES = ["https://www.googleapis.com/auth/indexing"]


def urls_from_sitemap() -> list:
    path = os.path.join(ROOT, "sitemap.xml")
    if not os.path.exists(path):
        sys.exit("sitemap.xml이 없습니다. 먼저 `python3 build.py`를 실행하세요.")
    tree = ET.parse(path)
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    return [loc.text.strip() for loc in tree.findall(".//s:loc", ns)]


def main() -> None:
    args = sys.argv[1:]
    notify_type = "URL_UPDATED"
    if "--deleted" in args:
        notify_type = "URL_DELETED"
        args.remove("--deleted")

    try:
        from google.oauth2 import service_account
        from google.auth.transport.requests import AuthorizedSession
    except ImportError:
        sys.exit("의존성 필요: pip install google-auth requests")

    cred_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not cred_path or not os.path.exists(cred_path):
        sys.exit("환경변수 GOOGLE_APPLICATION_CREDENTIALS에 서비스 계정 JSON 경로를 지정하세요.")

    creds = service_account.Credentials.from_service_account_file(
        cred_path, scopes=SCOPES)
    session = AuthorizedSession(creds)

    urls = args or urls_from_sitemap()
    print(f"type={notify_type}  URL {len(urls)}건 통보:")
    ok = 0
    for u in urls:
        resp = session.post(ENDPOINT, json={"url": u, "type": notify_type}, timeout=20)
        status = "OK" if resp.status_code == 200 else f"ERR {resp.status_code}"
        if resp.status_code == 200:
            ok += 1
        print(f"  [{status}] {u}")
        if resp.status_code != 200:
            print(f"        {resp.text[:200]}")
    print(f"\n완료: {ok}/{len(urls)} 성공")


if __name__ == "__main__":
    main()
