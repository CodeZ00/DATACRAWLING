"""교보문고 컴퓨터/IT 베스트셀러 데이터 심층 탐색적 데이터 분석(EDA) 스크립트.

수집된 CSV 데이터를 바탕으로 통계 분석, TF-IDF 키워드 추출,
다양한 일변량/이변량/다변량 시각화를 수행하고 이미지를 저장합니다.
"""

import io
import re
from pathlib import Path
import koreanize_matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer


def run_eda():
    data_path = Path("kyobo/data/kyobo_daily_it_bestseller_20261020.csv")
    images_dir = Path("kyobo/images")
    images_dir.mkdir(parents=True, exist_ok=True)

    # 1. 데이터 로드
    df = pd.read_csv(data_path, encoding="utf-8-sig")

    print(f"데이터 크기: {df.shape[0]}행, {df.shape[1]}열")
    print(f"중복 데이터 수: {df.duplicated().sum()}건")

    # 수치형 변수 형변환 및 전처리
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

    # 출간연도 파싱 (YYYYMMDD 형식)
    df["pub_date_str"] = df["pub_date"].astype(str)
    df["pub_year"] = df["pub_date_str"].str.slice(0, 4)
    # 연도가 1900~2030 범위를 벗어나는 경우 등 이상치 처리
    df["pub_year_num"] = pd.to_numeric(df["pub_year"], errors="coerce")
    df["pub_year_valid"] = df["pub_year_num"].apply(
        lambda y: str(int(y)) if 1990 <= y <= 2030 else "기타"
    )

    # 순위 구간 범주 생성
    bins = [0, 50, 100, 200, 350, 700]
    labels = ["1-50위", "51-100위", "101-200위", "201-350위", "351위 이상"]
    df["rank_group"] = pd.cut(df["rank"], bins=bins, labels=labels)

    # ----------------------------------------------------
    # 시각화 1: 판매가(sale_price) 분포 (일변량)
    # ----------------------------------------------------
    plt.figure(figsize=(10, 6))
    plt.hist(
        df["sale_price"].dropna(),
        bins=30,
        color="#3498db",
        edgecolor="black",
        alpha=0.7,
        density=True,
    )
    df["sale_price"].dropna().plot(kind="kde", color="#e74c3c", linewidth=2)
    plt.title("도서 판매가(Sale Price) 분포 및 밀도 추정", fontsize=14, pad=12)
    plt.xlabel("판매가 (원)", fontsize=11)
    plt.ylabel("밀도 (Density)", fontsize=11)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(images_dir / "01_sale_price_distribution.png", dpi=150)
    plt.close()

    # ----------------------------------------------------
    # 시각화 2: 리뷰 평점(rating) 분포 (일변량)
    # ----------------------------------------------------
    # 평점 0점(리뷰 없음)과 0점 초과 분리 파악
    plt.figure(figsize=(10, 6))
    valid_ratings = df[df["rating"] > 0]["rating"]
    plt.hist(
        valid_ratings,
        bins=25,
        color="#2ecc71",
        edgecolor="black",
        alpha=0.7,
    )
    plt.title("도서 리뷰 평점 분포 (평점 보유 도서 대상, 10점 만점)", fontsize=14, pad=12)
    plt.xlabel("리뷰 평점", fontsize=11)
    plt.ylabel("도서 수 (권)", fontsize=11)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(images_dir / "02_rating_distribution.png", dpi=150)
    plt.close()

    # ----------------------------------------------------
    # 시각화 3: 할인율(discount_rate) 빈도 분포 (일변량)
    # ----------------------------------------------------
    plt.figure(figsize=(9, 5))
    disc_counts = df["discount_rate"].value_counts().sort_index()
    bars = plt.bar(
        disc_counts.index.astype(str) + "%",
        disc_counts.values,
        color="#9b59b6",
        edgecolor="black",
        alpha=0.8,
    )
    for bar in bars:
        yval = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            yval + 5,
            f"{yval}권",
            ha="center",
            va="bottom",
            fontsize=10,
        )
    plt.title("컴퓨터/IT 베스트셀러 할인율(Discount Rate) 분포", fontsize=14, pad=12)
    plt.xlabel("할인율", fontsize=11)
    plt.ylabel("도서 수 (권)", fontsize=11)
    plt.grid(True, linestyle="--", alpha=0.5, axis="y")
    plt.tight_layout()
    plt.savefig(images_dir / "03_discount_rate_distribution.png", dpi=150)
    plt.close()

    # ----------------------------------------------------
    # 시각화 4: 출간 연도별 베스트셀러 도서 수 추이 (일변량/시계열)
    # ----------------------------------------------------
    year_counts = (
        df[df["pub_year_valid"] != "기타"]["pub_year_valid"]
        .value_counts()
        .sort_index()
    )
    recent_years = year_counts[year_counts.index >= "2018"]
    plt.figure(figsize=(10, 5))
    plt.plot(
        recent_years.index,
        recent_years.values,
        marker="o",
        color="#e67e22",
        linewidth=2.5,
        markersize=7,
    )
    for x, y in zip(recent_years.index, recent_years.values):
        plt.annotate(
            f"{y}권",
            (x, y),
            textcoords="offset points",
            xytext=(0, 8),
            ha="center",
            fontweight="bold",
        )
    plt.title("출간 연도별 베스트셀러 진입 도서 수 (2018년 이후)", fontsize=14, pad=12)
    plt.xlabel("출간 연도", fontsize=11)
    plt.ylabel("도서 수 (권)", fontsize=11)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(images_dir / "04_publication_year_trend.png", dpi=150)
    plt.close()

    # ----------------------------------------------------
    # 시각화 5: 상위 30대 출판사 점유율 (범주형)
    # ----------------------------------------------------
    top30_publishers = df["publisher"].value_counts().head(30)
    plt.figure(figsize=(12, 10))
    y_pos = np.arange(len(top30_publishers))
    plt.barh(
        y_pos,
        top30_publishers.values,
        color="#1abc9c",
        edgecolor="black",
        alpha=0.8,
    )
    plt.yticks(y_pos, top30_publishers.index, fontsize=10)
    plt.gca().invert_yaxis()  # 1위가 위로 오도록
    for i, v in enumerate(top30_publishers.values):
        plt.text(v + 0.5, i, f"{v}권", va="center", fontsize=9)
    plt.title("컴퓨터/IT 베스트셀러 상위 30대 출판사 도서 등록 건수", fontsize=14, pad=12)
    plt.xlabel("등록 도서 수 (권)", fontsize=11)
    plt.grid(True, linestyle="--", alpha=0.5, axis="x")
    plt.tight_layout()
    plt.savefig(images_dir / "05_top30_publishers.png", dpi=150)
    plt.close()

    # ----------------------------------------------------
    # 시각화 6: 도서 소개(intro) TF-IDF 상위 30대 키워드 (텍스트 분석)
    # ----------------------------------------------------
    # 한글 및 영문 2글자 이상 단어 추출
    corpus = df["intro"].fillna("").astype(str)
    # 간단한 불용어 리스트
    korean_stopwords = {
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
        "이 책은",
        "하는",
    }
    tfidf = TfidfVectorizer(
        token_pattern=r"(?u)\b[가-힣a-zA-Z]{2,}\b",
        stop_words=list(korean_stopwords),
        max_features=500,
    )
    tfidf_matrix = tfidf.fit_transform(corpus)
    feature_names = np.array(tfidf.get_feature_names_out())
    # 전체 문서에서의 평균 TF-IDF 가중치
    mean_tfidf = np.asarray(tfidf_matrix.mean(axis=0)).ravel()
    top30_indices = mean_tfidf.argsort()[::-1][:30]
    top30_words = feature_names[top30_indices]
    top30_scores = mean_tfidf[top30_indices]

    plt.figure(figsize=(12, 10))
    y_pos = np.arange(len(top30_words))
    plt.barh(y_pos, top30_scores, color="#e74c3c", edgecolor="black", alpha=0.8)
    plt.yticks(y_pos, top30_words, fontsize=10)
    plt.gca().invert_yaxis()
    for i, v in enumerate(top30_scores):
        plt.text(v + 0.0005, i, f"{v:.4f}", va="center", fontsize=9)
    plt.title("도서 소개(Intro) 텍스트 TF-IDF 상위 30대 핵심 키워드", fontsize=14, pad=12)
    plt.xlabel("TF-IDF 평균 가중치", fontsize=11)
    plt.grid(True, linestyle="--", alpha=0.5, axis="x")
    plt.tight_layout()
    plt.savefig(images_dir / "06_top30_tfidf_keywords.png", dpi=150)
    plt.close()

    # ----------------------------------------------------
    # 시각화 7: 순위(rank)와 판매가(sale_price) 관계 (이변량)
    # ----------------------------------------------------
    plt.figure(figsize=(10, 6))
    plt.scatter(
        df["rank"],
        df["sale_price"],
        alpha=0.5,
        color="#2980b9",
        edgecolors="none",
        s=35,
    )
    # 추세선 추가
    valid_data = df[["rank", "sale_price"]].dropna()
    z = np.polyfit(valid_data["rank"], valid_data["sale_price"], 1)
    p = np.poly1d(z)
    plt.plot(
        valid_data["rank"].sort_values(),
        p(valid_data["rank"].sort_values()),
        "r--",
        linewidth=2,
        label=f"추세선 (기울기: {z[0]:.2f})",
    )
    plt.title("베스트셀러 순위와 판매 가격 간의 상관 관계", fontsize=14, pad=12)
    plt.xlabel("순위 (Rank)", fontsize=11)
    plt.ylabel("판매가 (원)", fontsize=11)
    plt.legend(fontsize=11)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(images_dir / "07_rank_vs_saleprice.png", dpi=150)
    plt.close()

    # ----------------------------------------------------
    # 시각화 8: 순위 구간별 리뷰 수(review_count) 분포 (이변량)
    # ----------------------------------------------------
    plt.figure(figsize=(10, 6))
    # 리뷰 수가 극단적으로 큰 경우가 있으므로 log scale 또는 상위 95% 분위수 제한 고려
    sns_box_data = [
        df[df["rank_group"] == grp]["review_count"].dropna().values
        for grp in labels
    ]
    plt.boxplot(
        sns_box_data,
        tick_labels=labels,
        showfliers=False,
        patch_artist=True,
        boxprops=dict(facecolor="#f39c12", color="black", alpha=0.7),
        medianprops=dict(color="red", linewidth=2),
    )
    plt.title(
        "베스트셀러 순위 구간별 도서 리뷰 수 분포 (이상치 제외 박스플롯)",
        fontsize=14,
        pad=12,
    )
    plt.xlabel("순위 구간", fontsize=11)
    plt.ylabel("리뷰 수 (건)", fontsize=11)
    plt.grid(True, linestyle="--", alpha=0.5, axis="y")
    plt.tight_layout()
    plt.savefig(images_dir / "08_rankgroup_vs_reviewcount.png", dpi=150)
    plt.close()

    # ----------------------------------------------------
    # 시각화 9: 주요 수치형 변수 상관관계 히트맵 (다변량)
    # ----------------------------------------------------
    plt.figure(figsize=(9, 7))
    corr_cols = [
        "rank",
        "fixed_price",
        "sale_price",
        "discount_rate",
        "point",
        "review_count",
        "rating",
    ]
    corr_labels = [
        "순위",
        "정가",
        "판매가",
        "할인율",
        "포인트",
        "리뷰수",
        "평점",
    ]
    corr_matrix = df[corr_cols].corr()
    corr_matrix.columns = corr_labels
    corr_matrix.index = corr_labels

    sns.heatmap(
        corr_matrix,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        vmin=-1,
        vmax=1,
        linewidths=0.5,
        cbar_kws={"shrink": 0.8},
    )
    plt.title("주요 수치형 변수 간 피어슨 상관계수 히트맵", fontsize=14, pad=12)
    plt.tight_layout()
    plt.savefig(images_dir / "09_correlation_heatmap.png", dpi=150)
    plt.close()

    # ----------------------------------------------------
    # 시각화 10: 상위 10대 출판사별 평균 가격 및 리뷰수/평점 분석 (다변량)
    # ----------------------------------------------------
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
        .sort_values(by="도서수", ascending=False)
    )

    fig, ax1 = plt.subplots(figsize=(11, 6))
    ax2 = ax1.twinx()

    x = np.arange(len(pub_summary))
    width = 0.35

    b1 = ax1.bar(
        x - width / 2,
        pub_summary["평균판매가"],
        width,
        label="평균 판매가(원)",
        color="#34495e",
        alpha=0.8,
    )
    b2 = ax2.bar(
        x + width / 2,
        pub_summary["평균리뷰수"],
        width,
        label="평균 리뷰수(건)",
        color="#e67e22",
        alpha=0.8,
    )

    ax1.set_xlabel("상위 10대 출판사", fontsize=11)
    ax1.set_ylabel("평균 판매가 (원)", color="#34495e", fontsize=11)
    ax2.set_ylabel("평균 리뷰 수 (건)", color="#e67e22", fontsize=11)
    ax1.set_xticks(x)
    ax1.set_xticklabels(pub_summary.index, rotation=30, ha="right", fontsize=10)
    plt.title("상위 10대 출판사별 평균 판매가 및 평균 리뷰 수 비교", fontsize=14, pad=12)
    ax1.grid(True, linestyle="--", alpha=0.3)
    fig.tight_layout()
    plt.savefig(images_dir / "10_top10_publishers_price_reviews.png", dpi=150)
    plt.close()

    # ----------------------------------------------------
    # 시각화 11: 정가 vs 판매가 산점도 및 할인율 구간 (이변량/다변량)
    # ----------------------------------------------------
    plt.figure(figsize=(9, 6))
    scatter = plt.scatter(
        df["fixed_price"],
        df["sale_price"],
        c=df["discount_rate"],
        cmap="viridis",
        alpha=0.6,
        s=40,
        edgecolors="none",
    )
    cbar = plt.colorbar(scatter)
    cbar.set_label("할인율 (%)", fontsize=10)
    plt.plot([0, 80000], [0, 80000], "k--", alpha=0.5, label="정가선 (할인 없음)")
    plt.plot(
        [0, 80000], [0, 72000], "r--", alpha=0.7, label="10% 할인선 (도서정가제)"
    )
    plt.title("도서 정가 대비 실제 판매가 및 할인율 분포", fontsize=14, pad=12)
    plt.xlabel("정가 (원)", fontsize=11)
    plt.ylabel("판매가 (원)", fontsize=11)
    plt.xlim(0, 85000)
    plt.ylim(0, 85000)
    plt.legend(fontsize=10)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(images_dir / "11_fixed_vs_sale_price.png", dpi=150)
    plt.close()

    print("모든 시각화 이미지 11개 저장 완료!")

    # 기술통계 및 요약 테이블 출력
    print("\n=== 데이터프레임 기본 정보 ===")
    buffer = io.StringIO()
    df.info(buf=buffer)
    print(buffer.getvalue())

    print("\n=== 수치형 변수 기술통계 ===")
    print(df[numeric_cols].describe().to_string())

    print("\n=== 범주형 변수 기술통계 ===")
    cat_cols = ["book_id", "title", "author", "publisher", "isbn"]
    print(df[cat_cols].describe(include=["object"]).to_string())

    print("\n=== 상위 30대 TF-IDF 키워드 및 가중치 ===")
    for rank, (w, s) in enumerate(zip(top30_words, top30_scores), 1):
        print(f"{rank:2d}. {w}: {s:.4f}")

    print("\n=== 순위 구간별 집계 통계표 ===")
    rank_summary = df.groupby("rank_group", observed=False).agg(
        도서수=("book_id", "count"),
        평균판매가=("sale_price", "mean"),
        중앙판매가=("sale_price", "median"),
        평균리뷰수=("review_count", "mean"),
        중앙리뷰수=("review_count", "median"),
        평균평점=("rating", "mean"),
    )
    print(rank_summary.to_string())

    print("\n=== 상위 10대 출판사 요약 ===")
    print(pub_summary.to_string())


if __name__ == "__main__":
    run_eda()
