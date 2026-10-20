1) http 요청정보와 헤더정보
Request URL
https://store.kyobobook.co.kr/api/gw/best/best-seller/online?page=1&per=50&period=001&dsplDvsnCode=001&dsplTrgtDvsnCode=004&saleCmdtClstCode=33

Request method
GET

referer
https://store.kyobobook.co.kr/bestseller/online/daily/domestic/33?page=1

accept
application/json, text/plain, */*

user-agent
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36

accept-encoding
gzip, deflate, br

2) payload (Query Parameters) 정보
page
1

per
50

period
001 (일간 베스트셀러)

dsplDvsnCode
001 (국내도서)

dsplTrgtDvsnCode
004 (분야/카테고리 지정)

saleCmdtClstCode
33 (컴퓨터/IT)

3) response 응답의 일부 (JSON)
{
  "statusCode": 200,
  "resultCode": "00000000",
  "resultMessage": "정상 처리되었습니다.",
  "detailMessage": null,
  "data": {
    "total": 370,
    "bestSeller": [
      {
        "prstRnkn": 1,
        "frmrRnkn": 1,
        "saleCmdtid": "S000218736039",
        "saleCmdtGrpDvsnCode": "SGK",
        "cmdtName": "2026 이지패스 ADsP 데이터분석 준전문가",
        "chrcName": "박현민 외",
        "pbcmName": "위키북스",
        "rlseDate": "20260102",
        "price": 30000,
        "sapr": 27000,
        "dscnRate": 10,
        "upntAcmlAmnt": 1500,
        "buyRevwNumc": 398,
        "buyRevwRvgr": 9.86,
        "revwEmtnKywrName": "도움돼요",
        "cmdtCode": "9791158396510",
        "saleCmdtClstName": "컴퓨터/IT",
        "inbukCntt": "미어캣 2026 최신 기출문제 수록 앱 제공 | 비전공자 20일 완성..."
      }
    ]
  }
}

4) 수집 및 저장 요구사항
- 1페이지 시범 수집 후 전체 페이지(총 370여 건, 1~8페이지)를 자동 페이징하여 연속 수집
- 서버 부하 방지를 위해 각 페이지 요청 간 0.5초 대기(delay) 적용
- 응답 데이터의 GZIP 압축 해제 자동 처리
- 수집된 데이터는 아래 15개 핵심 컬럼으로 정제:
  1. rank (순위, prstRnkn)
  2. prev_rank (이전순위, frmrRnkn)
  3. book_id (상품ID, saleCmdtid)
  4. title (도서명, cmdtName)
  5. author (저자, chrcName)
  6. publisher (출판사, pbcmName)
  7. pub_date (출간일, rlseDate)
  8. fixed_price (정가, price)
  9. sale_price (판매가, sapr)
  10. discount_rate (할인율, dscnRate)
  11. point (적립포인트, upntAcmlAmnt)
  12. review_count (리뷰수, buyRevwNumc)
  13. rating (리뷰평점, buyRevwRvgr)
  14. isbn (ISBN, cmdtCode)
  15. intro (도서소개, inbukCntt HTML 태그 정제)
- kyobo/data/kyobo_daily_it_bestseller_{YYYYMMDD}.csv 경로에 UTF-8-SIG 인코딩으로 저장
