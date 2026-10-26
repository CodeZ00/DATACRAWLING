# 스타벅스 코리아 매장 찾기 REST API 기술 명세서

## 1. 개요
스타벅스 코리아 공식 웹사이트([store_map.do](https://www.starbucks.co.kr/store/store_map.do))에서 비동기 매장 검색에 사용하는 내부 Gateway REST API 엔드포인트에 대한 명세입니다.

- **기본 엔드포인트**: `https://www.starbucks.co.kr/store/getStore.do?r=2G30D88Z8X`
- **프로토콜**: HTTPS POST
- **인코딩**: UTF-8
- **인증 방식**: 불필요 (Cookie/세션 없이 표준 AJAX 헤더로 접근 가능)

---

## 2. 요청 헤더 (HTTP Headers)
```http
POST /store/getStore.do?r=2G30D88Z8X HTTP/1.1
Host: www.starbucks.co.kr
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
X-Requested-With: XMLHttpRequest
Accept: application/json, text/javascript, */*; q=0.01
```

---

## 3. 요청 본문 (Form URL-Encoded Payload)

### 3.1 파라미터 상세
| 파라미터명 | 설명 | 서울 수집값 | 전국 수집값 | 비고 |
| :--- | :--- | :--- | :--- | :--- |
| `p_sido_cd` | 시/도 코드 | `01` | `""` (공백) | `01`=서울, 비워두면 전국 전체 조회 |
| `p_gugun_cd` | 구/군 코드 | `""` (공백) | `""` (공백) | 특정 구/군 지정 시 사용 |
| `iend` | 조회 최대 개수 | `1000` | `3000` | 전국 매장 수(~2,210개)보다 크게 지정 |
| `search_type` | 검색 유형 | `C` | `C` | 지역 검색 모드 |
| `in_biz_cds` | 비즈니스 코드 | `0` | `0` | 기본값 |
| `in_scodes` | 매장 코드 | `0` | `0` | 기본값 |
| `ins_lat` | 기준 위도 | `37.56682` | `37.56682` | 서울 중심 위도 |
| `ins_lng` | 기준 경도 | `126.97865` | `126.97865` | 서울 중심 경도 |
| `isError` | 에러 여부 | `N` | `N` | 기본값 |
| `in_distance`| 검색 반경 | `0` | `0` | 0은 전체 |
| `searchEgg` | 특수 플래그 | `N` | `N` | 기본값 |
| `pageSize` | 페이지 크기 | `20` | `100` | 기본값 |

---

## 4. 응답 구조 (JSON Schema)

### 4.1 루트 구조
```json
{
  "list": [
    {
      "s_code": "124",
      "s_name": "울산대",
      "tel": "1522-3232",
      "sido_code": "07",
      "sido_name": "울산",
      "gugun_code": "0711",
      "gugun_name": "남구",
      "addr": "울산광역시 남구 무거동 1456 바보사거리 101,102...",
      "doro_address": "울산광역시 남구 대학로 138 (무거동)...",
      "lat": "37.44645476107155",
      "lot": "126.70117355019587",
      "open_dt": "20061222",
      "new_state": "N",
      "theme_state": "T05@T08@T16@T17@...",
      "defaultimage": "/upload/store/2026/02/9387_20260225055424_0w2r4.jpg"
    }
  ]
}
```

### 4.2 주요 특화 테마 코드 (`theme_state`)
- `T05`: 드라이브 스루 (Drive Thru, DT)
- `T08` / `T21`: 스타벅스 리저브 (Reserve)
- `T43` / `P80`: 딜리버스 (Delivers, 배달 서비스)
- `T17`: 주차 가능
- `T20`: 지하철 인접
