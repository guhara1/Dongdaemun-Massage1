# 사이트 공통 설정
# 배포 도메인 확정 후 BASE_URL 을 실제 도메인으로 변경하세요.
BASE_URL = "https://dongdaemun-massage1.pages.dev"

BRAND = "바로GO"
BRAND_DESC = "서울 동대문구 전지역 방문형 출장마사지·홈타이 예약 안내"
PHONE = "0508-202-4719"
PHONE_DISPLAY = "0508-202-4719"

# IndexNow 키 — 빌드 시 루트에 <KEY>.txt 키파일이 자동 생성된다.
# (Bing·Naver·Yandex 등 IndexNow 참여 검색엔진에 즉시 색인 통보용)
INDEXNOW_KEY = "2eb079a18f2c1ced5eacd236ba79dc06"

# 메인(허브) 페이지 — 루트(/)에서 바로 노출한다.
MAIN_PATH = ""
MAIN_URL = "/"

# 상단 메뉴 — 하위 메뉴에는 키워드를 반복하지 않고 지역명·역명만 표시한다.
NAV = [
    ("동대문 홈", MAIN_URL, [
        ("동대문구 출장마사지 메인", MAIN_URL),
        ("동대문구 홈타이 이용 기준", "/hometai-guide/#standard"),
        ("대표동 선택 안내", "/seoul/dongdaemun/areas/"),
        ("예약 전 확인사항", "/precautions/"),
    ]),
    ("지역별 안내", "/seoul/dongdaemun/areas/", [
        ("동대문구 전체", "/seoul/dongdaemun/areas/"),
        ("신설동", "/seoul/dongdaemun/sinseol-dong-chuljangmassage/"),
        ("용두동", "/seoul/dongdaemun/yongdu-dong-chuljangmassage/"),
        ("제기동", "/seoul/dongdaemun/jegi-dong-chuljangmassage/"),
        ("전농동", "/seoul/dongdaemun/jeonnong-dong-chuljangmassage/"),
        ("답십리동", "/seoul/dongdaemun/dapsimni-dong-chuljangmassage/"),
        ("장안동", "/seoul/dongdaemun/jangan-dong-chuljangmassage/"),
        ("청량리동", "/seoul/dongdaemun/cheongnyangni-dong-chuljangmassage/"),
        ("회기동", "/seoul/dongdaemun/hoegi-dong-chuljangmassage/"),
        ("휘경동", "/seoul/dongdaemun/hwigyeong-dong-chuljangmassage/"),
        ("이문동", "/seoul/dongdaemun/imun-dong-chuljangmassage/"),
    ]),
    ("역세권 안내", "/seoul/dongdaemun/stations/", [
        ("역 전체", "/seoul/dongdaemun/stations/"),
        ("청량리역", "/seoul/dongdaemun/cheongnyangni-station-chuljangmassage/"),
        ("회기역", "/seoul/dongdaemun/hoegi-station-chuljangmassage/"),
        ("외대앞역", "/seoul/dongdaemun/hankuk-univ-foreign-studies-station-chuljangmassage/"),
        ("신이문역", "/seoul/dongdaemun/sinimun-station-chuljangmassage/"),
        ("제기동역", "/seoul/dongdaemun/jegi-dong-station-chuljangmassage/"),
        ("신설동역", "/seoul/dongdaemun/sinseol-dong-station-chuljangmassage/"),
        ("용두역", "/seoul/dongdaemun/yongdu-station-chuljangmassage/"),
        ("답십리역", "/seoul/dongdaemun/dapsimni-station-chuljangmassage/"),
        ("장한평역", "/seoul/dongdaemun/janghanpyeong-station-chuljangmassage/"),
        ("고려대역 인접", "/seoul/dongdaemun/korea-univ-nearby-area-chuljangmassage/"),
    ]),
    ("생활권 안내", "/seoul/dongdaemun/districts/", [
        ("생활권 전체", "/seoul/dongdaemun/districts/"),
        ("청량리역 생활권", "/seoul/dongdaemun/cheongnyangni-station-area-chuljangmassage/"),
        ("회기역 대학가 생활권", "/seoul/dongdaemun/hoegi-university-area-chuljangmassage/"),
        ("경희대·외대 생활권", "/seoul/dongdaemun/kyunghee-hufs-area-chuljangmassage/"),
        ("장안동 주거지 생활권", "/seoul/dongdaemun/jangan-residential-area-chuljangmassage/"),
        ("답십리역 생활권", "/seoul/dongdaemun/dapsimni-station-area-chuljangmassage/"),
        ("전농동 주거지 생활권", "/seoul/dongdaemun/jeonnong-residential-area-chuljangmassage/"),
        ("제기동 약령시장 생활권", "/seoul/dongdaemun/jegi-medicine-market-area-chuljangmassage/"),
        ("신설동 로터리 생활권", "/seoul/dongdaemun/sinseol-rotary-area-chuljangmassage/"),
        ("용두동·동대문구청 인근", "/seoul/dongdaemun/yongdu-office-area-chuljangmassage/"),
        ("이문·휘경 재정비 생활권", "/seoul/dongdaemun/imun-hwigyeong-renewal-area-chuljangmassage/"),
        ("중랑천 인접 생활권", "/seoul/dongdaemun/jungnangcheon-area-chuljangmassage/"),
    ]),
    ("예약 안내", "/reservation/", [
        ("예약 가능 지역 확인", "/reservation/#area"),
        ("예약 가능 시간 안내", "/reservation/#hours"),
        ("추가 이동비 안내", "/reservation/#move"),
        ("결제 방식 안내", "/reservation/#payment"),
        ("예약 변경 안내", "/reservation/#change"),
        ("취소 기준 안내", "/reservation/#cancel"),
    ]),
    ("이용 전 확인사항", "/precautions/", [
        ("방문 가능 주소 확인", "/precautions/#address"),
        ("자택 이용 전 확인사항", "/precautions/#home"),
        ("숙소 이용 전 확인사항", "/precautions/#lodging"),
        ("사무실 인근 이용 안내", "/precautions/#office"),
        ("개인정보 처리 기준", "/precautions/#privacy"),
        ("고객 안전 안내", "/precautions/#safety"),
        ("불법·선정적 서비스 불가", "/precautions/#prohibited"),
    ]),
    ("홈타이 이용 가이드", "/hometai-guide/", [
        ("홈타이란?", "/hometai-guide/#what"),
        ("출장마사지와 홈타이 차이", "/hometai-guide/#diff"),
        ("동대문구 이용 전 기준", "/hometai-guide/#standard"),
        ("지역별 이동 기준", "/hometai-guide/#move"),
        ("추가 비용 확인 기준", "/hometai-guide/#cost"),
        ("처음 이용하는 고객 안내", "/hometai-guide/#first"),
    ]),
    ("고객센터", "/support/", [
        ("문의하기", "/support/#contact"),
        ("자주 묻는 질문", "/support/#faq"),
        ("운영 기준", "/support/#policy"),
        ("사이트 소개", "/about/"),
        ("개인정보 처리방침", "/privacy/"),
        ("이용약관", "/terms/"),
    ]),
]
