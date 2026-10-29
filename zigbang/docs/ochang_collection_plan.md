# 📋 [수집 계획서 & API 명세서] 오창읍 원룸·빌라 월세 데이터 파이프라인

> **문서 버전**: 1.0.0  
> **최종 갱신일**: 2026-10-29  
> **대상 지역**: 충청북도 청주시 청원구 오창읍 전역  
> **수집 소스**: 직방(Zigbang) 프론트엔드 모바일/웹 지도 API  

---

## 1. 수집 개요 및 목적
- **목적**: 오창과학산업단지 및 오창제2산업단지 배후의 1인 가구 및 청년 근로자 실거주 월세 시세 및 가성비 주거 데이터 전수 수집
- **수집 대상**: 직방 지도 상의 원룸(단독, 분리형, 복층형) 및 빌라(다세대/다가구, 투룸, 쓰리룸+) 월세 매물
- **수집 주기 및 전략**: 일간 정기 수집(Daily Snapshot) 및 15개 배치 최적화 통신

---

## 2. 직방 통신 프로토콜 정밀 분석 & API 명세

### 2.1 지리 좌표 영역 매물 식별 (클러스터링)
- **URL**: `https://apis.zigbang.com/house/property/v1/items/villas` 및 `items/onerooms`
- **Method**: `GET`
- **주요 파라미터**:
  - `geohash`: 암호화된 지도 영역 토큰
  - `salesPriceMin`: 0
  - `depositMin`: 0
  - `rentMin`: 0
- **응답 구조**:
  - `items`: `[ { "id": 50855368, "lat": 36.7119, "lng": 127.428, "userNo": 347582 }, ... ]`
- **오창읍 지리 바운딩 박스 필터링**:
  - 위도: `36.660 <= lat <= 36.775`
  - 경도: `127.370 <= lng <= 127.495`

### 2.2 매물 상세 스펙 배치 조회 API (Data Gateway)
- **URL**: `https://apis.zigbang.com/house/property/v1/items/list`
- **Method**: `POST`
- **Headers**:
  ```http
  Content-Type: application/json
  User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ...
  Origin: https://www.zigbang.com
  Referer: https://www.zigbang.com/
  ```
- **Request Body (배치 한도: 정확히 15개)**:
  ```json
  {
    "itemIds": [50855368, 50878689, 50800164, 50809162, ...]
  }
  ```
  > ⚠️ **주의사항 (API 제약)**: `itemIds` 배열 길이가 16개 이상일 경우 직방 서버에서 `HTTP Error 400: Bad Request`를 반환하므로, 반드시 15개 이하 단위로 청크 분할 전송해야 합니다.

- **Response Body**:
  ```json
  {
    "items": [
      {
        "item_id": 50855368,
        "sales_type": "월세",
        "deposit": 200,
        "rent": 30,
        "size_m2": 28.1,
        "floor": "2",
        "building_floor": "4",
        "title": "오창 양청리 호수공원 인근 풀옵션 분리형 원룸",
        "manage_cost": "50000",
        "reg_date": "2026-10-25T14:20:00+09:00",
        "addressOrigin": {
          "local1": "충청북도",
          "local2": "청주시 청원구",
          "local3": "오창읍",
          "fullText": "충청북도 청주시 청원구 오창읍 양청리 ..."
        },
        "location": { "lat": 36.7125, "lng": 127.4281 },
        "images_thumbnail": "https://ic.zigbang.com/ic/items/50855368/1.jpg"
      }
    ],
    "totalCount": 15
  }
  ```

---

## 3. 예외 처리 및 복원력 설계
1. **지수 백오프 재시도 (Exponential Backoff)**: 배치 요청 실패 시 1초, 2초, 4초 간격으로 최대 3회 재시도
2. **트래픽 부하 방지**: 각 배치 요청 간 `time.sleep(0.3)` 의무 준수
3. **인코딩 무결성**: 엑셀 및 다양한 BI 툴 호환을 위해 반드시 `UTF-8-SIG` (BOM 포함) 인코딩으로 저장
