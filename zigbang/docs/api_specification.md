# 📡 직방(Zigbang) 오피스텔 지도 Gateway REST API 기술 명세서

본 문서는 직방 웹 프론트엔드가 내부적으로 사용하는 Gateway REST API의 엔드포인트, 요청 방식, 헤더 및 데이터 스키마를 정리한 공식 기술 명세서입니다.

---

## 1. 개요 및 인증 방식
- **호스트 도메인**: `https://apis.zigbang.com`
- **프로토콜**: HTTPS REST
- **인증 방식**: 별도의 유료 API Key 없이 브라우저 표준 헤더(`User-Agent`, `Referer: https://www.zigbang.com/`) 기반 통신
- **데이터 인코딩**: UTF-8, JSON

---

## 2. 주요 엔드포인트 상세

### 2.1 행정동 및 키워드 검색 API
- **Endpoint**: `GET /v2/search`
- **URL**: `https://apis.zigbang.com/v2/search?leaseYn=N&os=web&q={검색어}&serviceType={유형}`
- **파라미터**:
  - `q`: 검색할 행정동 또는 단지명 (예: `세종특별자치시 어진동`, `세종포레뷰`)
  - `serviceType`: `오피스텔` 또는 `아파트`
  - `leaseYn`: `N` (전월세 포함)
  - `os`: `web`
- **응답 스키마 요약**:
  ```json
  {
    "success": true,
    "code": "200",
    "items": [
      {
        "id": 3611011000,
        "type": "address",
        "name": "어진동",
        "description": "세종특별자치시 어진동",
        "lat": 36.5005018,
        "lng": 127.263465,
        "_source": {
          "local1": "세종특별자치시",
          "local3": "어진동",
          "법정동코드": "3611011000"
        }
      }
    ]
  }
  ```

---

### 2.2 단지 상세 정보 API
- **Endpoint**: `GET /v2/danjis/{danji_id}`
- **URL**: `https://apis.zigbang.com/v2/danjis/68606`
- **주요 응답 필드**:
  - `id`: 단지 고유 번호
  - `name`: 단지명
  - `local1`, `local2`, `local3`: 시/도, 시/군/구, 읍/면/동
  - `roadAddress`, `jibunAddress`: 도로명/지번 주소
  - `lat`, `lng`: 위도/경도 WGS84 좌표
  - `총세대수`, `총동수`, `최고층`, `최저층`: 건축 규모
  - `주차대수`, `세대당주차대수`: 주차 스펙
  - `사용승인일`: 준공 연월일 (YYYYMMDD)
  - `건설사`, `시행사`: 시공/시행 주체
  - `용적률`, `건폐율`: 건축 비율
  - `review_score`, `review_cnt`, `review_recent`: 거주민 실평점 및 리뷰 전문

---

### 2.3 영역 내 오피스텔 매물 ID 조회 API
- **Endpoint**: `GET /house/property/v1/items/officetels`
- **URL**: `https://apis.zigbang.com/house/property/v1/items/officetels?geohash={인코딩토큰}&salesPriceMin=0&depositMin=0&rentMin=0&withBuildings=true`
- **응답**: 해당 지도 영역 내 등록된 오피스텔 매물 ID 목록 반환

---

### 2.4 실매물 전수 스펙 일괄 조회 API (Core)
- **Endpoint**: `POST /house/property/v1/items/list`
- **Headers**:
  - `Content-Type: application/json`
  - `Referer: https://www.zigbang.com/`
- **Payload**:
  ```json
  {
    "itemIds": [50821560, 50851080, 50802864, ...]
  }
  ```
- **응답 스키마 요약**:
  ```json
  {
    "items": [
      {
        "item_id": 50821560,
        "sales_type": "월세",
        "deposit": 500,
        "rent": 55,
        "manage_cost": "110000",
        "size_m2": 28.74,
        "전용면적": { "m2": 28.74, "p": "8.7" },
        "공급면적": { "m2": 56.66, "p": "17.1" },
        "floor": "11",
        "building_floor": "17",
        "title": "호수공원 조망권 풀옵션 전입신고 가능",
        "service_type": "오피스텔",
        "addressOrigin": {
          "local3": "어진동",
          "fullText": "세종특별자치시 어진동"
        },
        "location": { "lat": 36.5005, "lng": 127.2634 }
      }
    ]
  }
  ```
