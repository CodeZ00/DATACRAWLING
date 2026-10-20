"""EDA 통계 요약 데이터 및 정제된 마크다운 테이블 생성 스크립트."""

import json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer


def df_to_md(df: pd.DataFrame) -> str:
    """pandas DataFrame을 마크다운 표 문자열로 안전하게 변환."""
    headers = list(df.columns)
    lines = []
    lines.append("| " + " | ".join(str(h) for h in headers) + " |")
    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for _, row in df.iterrows():
        row_str = " | ".join(str(val) for val in row)
        lines.append(f"| {row_str} |")
    return "\n".join(lines)


def generate_tables():
    data_path = Path("kyobo/data/kyobo_daily_it_bestseller_20261020.csv")
    df = pd.read_csv(data_path, encoding="utf-8-sig")

    numeric_cols = [
        "rank",
        "prev_rank",
        "fixed_price",
        "sale_price",
        "discount_rate",
        "point",
        "review_count",
        "rating",
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # 1. 원시 데이터 Head / Tail
    head_5 = df.head(5)[
        [
            "rank",
            "title",
            "author",
            "publisher",
            "sale_price",
            "review_count",
            "rating",
        ]
    ]
    tail_5 = df.tail(5)[
        [
            "rank",
            "title",
            "author",
            "publisher",
            "sale_price",
            "review_count",
            "rating",
        ]
    ]

    # 2. 기술통계 (수치형)
    desc_num = df[numeric_cols].describe().round(2).reset_index()
    desc_num.rename(columns={"index": "통계량"}, inplace=True)

    # 3. 기술통계 (범주형)
    cat_cols = ["book_id", "title", "author", "publisher", "isbn"]
    desc_cat = (
        df[cat_cols]
        .astype(str)
        .describe()
        .reset_index()
        .rename(columns={"index": "통계량"})
    )

    # 4. TF-IDF 분석 (의미 있는 핵심 키워드 중심 추출)
    korean_stopwords = [
        "수",
        "등",
        "및",
        "을",
        "를",
        "이",
        "가",
        "의",
        "에",
        "로",
        "으로",
        "한",
        "한다",
        "제공",
        "통해",
        "위한",
        "있는",
        "있다",
        "책",
        "도서",
        "내용",
        "구성",
        "다양한",
        "함께",
        "대한",
        "모든",
        "가장",
        "대해",
        "하는",
        "있습니다",
        "있도록",
        "어떻게",
        "필요한",
        "다시",
        "학습",
        "아니라",
        "바로",
        "세계",
        "독자",
        "우리가",
        "따라",
        "통한",
        "수록",
        "위해",
        "그",
        "더",
        "잘",
        "직접",
        "대한",
        "모두",
        "쉽게",
        "완성",
        "지금",
        "새로운",
        "자신의",
        "그대로",
    ]
    tfidf = TfidfVectorizer(
        token_pattern=r"(?u)\b[가-힣a-zA-Z]{2,}\b",
        stop_words=korean_stopwords,
        max_features=500,
    )
    corpus = df["intro"].fillna("").astype(str)
    tfidf_matrix = tfidf.fit_transform(corpus)
    feature_names = np.array(tfidf.get_feature_names_out())
    mean_tfidf = np.asarray(tfidf_matrix.mean(axis=0)).ravel()
    top30_idx = mean_tfidf.argsort()[::-1][:30]

    top30_tfidf_list = [
        {"순위": i + 1, "키워드": feature_names[idx], "가중치": round(mean_tfidf[idx], 4)}
        for i, idx in enumerate(top30_idx)
    ]
    df_tfidf = pd.DataFrame(top30_tfidf_list)

    # 5. 각 시각화 차트별 통계 요약표
    # 차트 1: 판매가 분위수 및 구간 빈도표
    price_bins = [0, 15000, 20000, 25000, 30000, 35000, 40000, 100000]
    price_labels = [
        "1.5만원 미만",
        "1.5만~2만원",
        "2만~2.5만원",
        "2.5만~3만원",
        "3만~3.5만원",
        "3.5만~4만원",
        "4만원 이상",
    ]
    df["price_group"] = pd.cut(
        df["sale_price"], bins=price_bins, labels=price_labels
    )
    price_dist = df["price_group"].value_counts().sort_index().reset_index()
    price_dist.columns = ["가격대 구간", "도서수(권)"]
    price_dist["비율(%)"] = (
        price_dist["도서수(권)"] / len(df) * 100
    ).round(2)

    # 차트 2: 평점 구간 분포표
    rating_bins = [-1, 0, 7.9, 8.9, 9.4, 9.9, 10.0]
    rating_labels = [
        "평점없음(0점)",
        "8.0점 미만",
        "8.0~8.9점",
        "9.0~9.4점",
        "9.5~9.9점",
        "10.0점 만점",
    ]
    df["rating_group"] = pd.cut(
        df["rating"], bins=rating_bins, labels=rating_labels
    )
    rating_dist = df["rating_group"].value_counts().sort_index().reset_index()
    rating_dist.columns = ["평점 구간", "도서수(권)"]
    rating_dist["비율(%)"] = (
        rating_dist["도서수(권)"] / len(df) * 100
    ).round(2)

    # 차트 3: 할인율 분포표
    disc_dist = df["discount_rate"].value_counts().sort_index().reset_index()
    disc_dist.columns = ["할인율(%)", "도서수(권)"]
    disc_dist["비율(%)"] = (disc_dist["도서수(권)"] / len(df) * 100).round(2)

    # 차트 4: 최근 출간 연도별 분포표
    df["pub_date_str"] = df["pub_date"].astype(str)
    df["pub_year"] = df["pub_date_str"].str.slice(0, 4)
    year_dist = (
        df[df["pub_year"] >= "2018"]["pub_year"]
        .value_counts()
        .sort_index(ascending=False)
        .reset_index()
    )
    year_dist.columns = ["출간 연도", "도서수(권)"]
    year_dist["비율(%)"] = (year_dist["도서수(권)"] / len(df) * 100).round(2)

    # 차트 5: 상위 30대 출판사 도서수 및 점유율
    top30_pub_df = df["publisher"].value_counts().head(30).reset_index()
    top30_pub_df.columns = ["출판사명", "등록도서수(권)"]
    top30_pub_df["누적점유율(%)"] = (
        top30_pub_df["등록도서수(권)"].cumsum() / len(df) * 100
    ).round(2)

    # 차트 8: 순위 구간별 집계표
    bins_rank = [0, 50, 100, 200, 350, 700]
    labels_rank = [
        "1-50위(최상위)",
        "51-100위(상위)",
        "101-200위(중상위)",
        "201-350위(중위)",
        "351위 이상(하위)",
    ]
    df["rank_group"] = pd.cut(
        df["rank"], bins=bins_rank, labels=labels_rank
    )
    rank_summary = (
        df.groupby("rank_group", observed=False)
        .agg(
            도서수=("book_id", "count"),
            평균판매가=("sale_price", "mean"),
            중앙판매가=("sale_price", "median"),
            평균리뷰수=("review_count", "mean"),
            중앙리뷰수=("review_count", "median"),
            평균평점=("rating", "mean"),
        )
        .round(1)
        .reset_index()
    )

    # 차트 10: 상위 10대 출판사 요약 통계
    top10_pubs = df["publisher"].value_counts().head(10).index
    pub_summary = (
        df[df["publisher"].isin(top10_pubs)]
        .groupby("publisher")
        .agg(
            도서수=("book_id", "count"),
            평균판매가=("sale_price", "mean"),
            평균리뷰수=("review_count", "mean"),
            평균평점=("rating", "mean"),
        )
        .round(1)
        .sort_values(by="도서수", ascending=False)
        .reset_index()
    )

    # 상관행렬
    corr_cols = [
        "rank",
        "fixed_price",
        "sale_price",
        "discount_rate",
        "point",
        "review_count",
        "rating",
    ]
    corr_df = df[corr_cols].corr().round(3).reset_index()
    corr_df.rename(columns={"index": "변수명"}, inplace=True)

    # 결과를 마크다운용 딕셔너리로 저장
    result = {
        "head_5": df_to_md(head_5),
        "tail_5": df_to_md(tail_5),
        "desc_num": df_to_md(desc_num),
        "desc_cat": df_to_md(desc_cat),
        "top30_tfidf": df_to_md(df_tfidf),
        "price_dist": df_to_md(price_dist),
        "rating_dist": df_to_md(rating_dist),
        "disc_dist": df_to_md(disc_dist),
        "year_dist": df_to_md(year_dist),
        "top30_pub": df_to_md(top30_pub_df),
        "rank_summary": df_to_md(rank_summary),
        "pub_summary": df_to_md(pub_summary),
        "corr_matrix": df_to_md(corr_df),
    }

    with open(
        "kyobo/reports/eda_tables.json", "w", encoding="utf-8"
    ) as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print("통계 요약 테이블 JSON 생성 완료!")


if __name__ == "__main__":
    generate_tables()
