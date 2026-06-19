#!/usr/bin/env python3
"""IndexNow 일괄/단건 색인 통보 스크립트.

IndexNow는 하나의 엔드포인트에 통보하면 참여 검색엔진(Bing·Naver·Yandex·
Seznam 등)에 공유됩니다. 이 스크립트는 안정성을 위해 대표 엔드포인트
여러 곳에 동시에 제출합니다. (구글은 IndexNow 미참여 → tools/google_indexing.py 사용)

사용법:
  # sitemap.xml의 모든 URL을 통보 (최초 일괄 통보)
  python tools/indexnow.py

  # 특정 URL만 통보 (글/페이지를 새로 올렸을 때)
  python tools/indexnow.py https://도메인/새글/ https://도메인/또다른글/

전제: build.py 실행으로 루트에 <KEY>.txt 키파일과 sitemap.xml이 생성되어
      실제 도메인에 배포(공개)되어 있어야 합니다.
"""
import json
import os
import sys
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from content.site import BASE_URL, INDEXNOW_KEY  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = BASE_URL.rstrip("/")
HOST = BASE.split("://", 1)[-1].split("/", 1)[0]
KEY_LOCATION = f"{BASE}/{INDEXNOW_KEY}.txt"

# IndexNow 참여 엔드포인트 (하나만 보내도 공유되지만 중복 제출은 무해)
ENDPOINTS = [
    "https://api.indexnow.org/indexnow",
    "https://www.bing.com/indexnow",
    "https://searchadvisor.naver.com/indexnow",
    "https://yandex.com/indexnow",
]


def urls_from_sitemap() -> list:
    path = os.path.join(ROOT, "sitemap.xml")
    if not os.path.exists(path):
        sys.exit("sitemap.xml이 없습니다. 먼저 `python3 build.py`를 실행하세요.")
    tree = ET.parse(path)
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    return [loc.text.strip() for loc in tree.findall(".//s:loc", ns)]


def submit(endpoint: str, payload: dict) -> None:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        endpoint, data=data, method="POST",
        headers={"Content-Type": "application/json; charset=utf-8"},
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            print(f"  [{r.status}] {endpoint}")
    except urllib.error.HTTPError as e:
        # 200/202 외에도 일부 엔진은 키 검증 전 4xx 반환 → 본문 출력
        body = e.read().decode("utf-8", "ignore")[:200]
        print(f"  [{e.code}] {endpoint}  {body}")
    except Exception as e:  # noqa: BLE001
        print(f"  [ERR] {endpoint}  {e}")


def main() -> None:
    urls = sys.argv[1:] or urls_from_sitemap()
    if not urls:
        sys.exit("통보할 URL이 없습니다.")
    print(f"host={HOST}  key={INDEXNOW_KEY}")
    print(f"keyLocation={KEY_LOCATION}")
    print(f"URL {len(urls)}건 통보:")
    for u in urls:
        print(f"  - {u}")
    payload = {
        "host": HOST,
        "key": INDEXNOW_KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": urls,
    }
    print("\n제출 결과:")
    for ep in ENDPOINTS:
        submit(ep, payload)
    print("\n완료. (키파일이 실제 도메인에 배포되어 있어야 검증됩니다)")


if __name__ == "__main__":
    main()
