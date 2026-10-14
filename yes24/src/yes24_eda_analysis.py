"""
YES24 일별 베스트셀러 데이터셋 탐색적 데이터 분석(EDA) 스크립트

이 모듈은 YES24 IT/모바일 일별 베스트셀러 데이터(yes24_day_bestseller.csv)를 로드하여
데이터 무결성 검증, 결측치 분석, 가격 및 할인율 통계, 인기 지표 간 상관관계,
주요 출판사 점유율, 기술 키워드 트렌드, 출간 연도별 시계열 분포를 분석하고
고해상도 시각화 차트(PNG)를 자동 생성합니다.

[주요 기능]
1. CSV 데이터 로드 및 타입 변환, 파생 변수(출간연도, 할인액 등) 생성
2. 수치형 데이터 기술 통계량 및 이상치 분석
3. 6종의 고품질 시각화 차트 생성 (yes24/images/ 디렉토리에 저장)
   - eda_01_price_distribution.png: 도서 가격 분포 및 할인율 통계
   - eda_02_correlation_heatmap.png: 수치형 지표 간 상관계수 히트맵
   - eda_03_sales_vs_reviews.png: 판매지수와 리뷰 수 간의 관계 및 이상치
   - eda_04_top_publishers.png: 베스트셀러 상위 10대 출판사 시장 점유율
   - eda_05_keyword_frequency.png: 태그 및 도서명 핵심 키워드 빈도 TOP 20
   - eda_06_pub_year_trend.png: 출간 연도별 도서 분포 (신간 vs 스테디셀러)
4. 콘솔 상세 통계 보고서 출력

[파일 정보]
- 작성 모듈: yes24/src/yes24_eda_analysis.py
- 생성 일자: 2026-10-07
- 입력 데이터: yes24/data/yes24_day_bestseller.csv
- 시각화 저장: yes24/images/
"""

import os
import re
from collections import Counter
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# ==============================================================================
# 한글 폰트 및 시각화 스타일 전역 설정
# ==============================================================================
plt.rcParams["font.family"] = "Malgun Gothic"  # Windows 한글 폰트 설정
plt.rcParams["axes.unicode_minus"] = False     # 음수 마이너스 부호 깨짐 방지
sns.set_theme(style="whitegrid", font="Malgun Gothic", rc={"axes.unicode_minus": False})


def load_and_preprocess_data(csv_path: str = os.path.join("yes24", "data", "yes24_day_bestseller.csv")) -> pd.DataFrame:
    """
    베스트셀러 CSV 파일을 로드하고 EDA 분석에 필요한 타입 변환 및 파생 변수를 생성합니다.

    Args:
        csv_path (str): 분석 대상 CSV 파일 상대 또는 절대 경로.

    Returns:
        pd.DataFrame: 전처리가 완료된 베스트셀러 데이터프레임.

    Raises:
        FileNotFoundError: 대상 파일이 존재하지 않는 경우 발생.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"데이터 파일을 찾을 수 없습니다: {csv_path}")

    df = pd.read_csv(csv_path, encoding="utf-8-sig")

    # 1. 수치형 컬럼 강제 변환 및 결측치 처리
    numeric_cols = [
        "rank", "fixed_price", "sale_price", "discount_rate",
        "point", "rating", "review_count", "sales_index"
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # 2. 파생 변수 생성: 실질 할인액 (정가 - 판매가)
    df["discount_amount"] = df["fixed_price"] - df["sale_price"]

    # 3. 파생 변수 생성: 출간 연도 및 출간 월 추출 (예: '2026년 08월' -> 2026, 8)
    def extract_year(date_str: str) -> int:
        if not isinstance(date_str, str):
            return 0
        match = re.search(r"(\d{4})년", date_str)
        return int(match.group(1)) if match else 0

    def extract_month(date_str: str) -> int:
        if not isinstance(date_str, str):
            return 0
        match = re.search(r"(\d{1,2})월", date_str)
        return int(match.group(1)) if match else 0

    df["pub_year"] = df["pub_date"].apply(extract_year)
    df["pub_month"] = df["pub_date"].apply(extract_month)

    # 4. 텍스트 결측치 빈 문자열 처리
    text_cols = ["subtitle", "tags", "author", "publisher"]
    for col in text_cols:
        df[col] = df[col].fillna("")

    return df


def plot_price_distribution(df: pd.DataFrame, output_dir: str = os.path.join("yes24", "images")) -> str:
    """
    도서 정가, 판매가 및 할인율의 분포를 시각화하여 저장합니다.

    Args:
        df (pd.DataFrame): 전처리된 베스트셀러 데이터프레임.
        output_dir (str): 차트 이미지를 저장할 디렉토리 경로.

    Returns:
        str: 생성된 이미지 파일의 경로.
    """
    os.makedirs(output_dir, exist_ok=True)
    save_path = os.path.join(output_dir, "eda_01_price_distribution.png")

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # 1. 판매가 히스토그램 & KDE
    sns.histplot(df["sale_price"], kde=True, ax=axes[0], color="#2b5c8f", bins=20)
    median_price = df["sale_price"].median()
    mean_price = df["sale_price"].mean()
    axes[0].axvline(median_price, color="red", linestyle="--", label=f"중앙값 ({median_price:,.0f}원)")
    axes[0].axvline(mean_price, color="orange", linestyle=":", label=f"평균값 ({mean_price:,.0f}원)")
    axes[0].set_title("도서 판매가(Sale Price) 분포", fontsize=13, fontweight="bold")
    axes[0].set_xlabel("판매가 (원)")
    axes[0].set_ylabel("도서 수 (권)")
    axes[0].legend()

    # 2. 정가 vs 판매가 박스플롯
    price_data = pd.melt(df[["fixed_price", "sale_price"]], var_name="가격 유형", value_name="가격")
    price_data["가격 유형"] = price_data["가격 유형"].map({"fixed_price": "정가", "sale_price": "판매가"})
    sns.boxplot(data=price_data, x="가격 유형", y="가격", ax=axes[1], palette=["#4c72b0", "#55a868"])
    axes[1].set_title("정가 대비 판매가 비교 (박스플롯)", fontsize=13, fontweight="bold")
    axes[1].set_ylabel("가격 (원)")

    # 3. 할인율 분포 (막대 그래프)
    discount_counts = df["discount_rate"].value_counts().sort_index()
    sns.barplot(x=discount_counts.index, y=discount_counts.values, ax=axes[2], palette="Blues_d")
    axes[2].set_title("도서 할인율(Discount Rate) 분포", fontsize=13, fontweight="bold")
    axes[2].set_xlabel("할인율 (%)")
    axes[2].set_ylabel("도서 수 (권)")
    for p in axes[2].patches:
        height = p.get_height()
        if height > 0:
            axes[2].annotate(f"{int(height)}권", (p.get_x() + p.get_width() / 2., height + 3),
                             ha="center", fontsize=10)

    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()
    return save_path


def plot_correlation_heatmap(df: pd.DataFrame, output_dir: str = os.path.join("yes24", "images")) -> str:
    """
    주요 수치형 지표(순위, 판매지수, 판매가, 평점, 리뷰 수 등) 간의 상관계수 히트맵을 생성합니다.

    Args:
        df (pd.DataFrame): 전처리된 베스트셀러 데이터프레임.
        output_dir (str): 차트 이미지를 저장할 디렉토리 경로.

    Returns:
        str: 생성된 이미지 파일의 경로.
    """
    os.makedirs(output_dir, exist_ok=True)
    save_path = os.path.join(output_dir, "eda_02_correlation_heatmap.png")

    target_cols = [
        "rank", "sales_index", "sale_price",
        "discount_rate", "rating", "review_count", "discount_amount"
    ]
    col_korean = {
        "rank": "베스트 순위",
        "sales_index": "판매지수",
        "sale_price": "판매가",
        "discount_rate": "할인율",
        "rating": "회원 평점",
        "review_count": "리뷰 수",
        "discount_amount": "할인액"
    }

    sub_df = df[target_cols].rename(columns=col_korean)
    corr = sub_df.corr(method="spearman")  # 비정규 분포 고려 스피어만 순위상관계수 적용

    plt.figure(figsize=(9, 7))
    sns.heatmap(
        corr, annot=True, fmt=".2f", cmap="coolwarm",
        vmin=-1, vmax=1, cbar_kws={"label": "스피어만 상관계수"},
        linewidths=0.5
    )
    plt.title("베스트셀러 주요 지표 간 스피어만 상관계수 히트맵", fontsize=14, fontweight="bold", pad=15)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()
    return save_path


def plot_sales_vs_reviews(df: pd.DataFrame, output_dir: str = os.path.join("yes24", "images")) -> str:
    """
    판매지수와 리뷰 수 간의 관계를 산점도로 시각화하고 상위 핵심 도서를 라벨링합니다.

    Args:
        df (pd.DataFrame): 전처리된 베스트셀러 데이터프레임.
        output_dir (str): 차트 이미지를 저장할 디렉토리 경로.

    Returns:
        str: 생성된 이미지 파일의 경로.
    """
    os.makedirs(output_dir, exist_ok=True)
    save_path = os.path.join(output_dir, "eda_03_sales_vs_reviews.png")

    plt.figure(figsize=(10, 6))

    # 산점도 플롯 (평점 기준 컬러맵 적용)
    valid_rating = df["rating"].apply(lambda x: x if x > 0 else np.nan)
    scatter = plt.scatter(
        df["review_count"] + 1, df["sales_index"] + 1,
        c=valid_rating, cmap="viridis",
        s=60, alpha=0.75, edgecolors="none"
    )
    cbar = plt.colorbar(scatter)
    cbar.set_label("회원 평점 (10점 만점)", fontsize=11)

    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("리뷰 수 (Log Scale, +1)", fontsize=12)
    plt.ylabel("판매지수 (Log Scale, +1)", fontsize=12)
    plt.title("도서별 판매지수 vs 리뷰 수 관계 분석 (로그 스케일)", fontsize=14, fontweight="bold")

    # 판매지수 상위 5개 도서 라벨링
    top_books = df.sort_values(by="sales_index", ascending=False).head(5)
    for _, row in top_books.iterrows():
        title_abbr = row["title"][:15] + ".." if len(row["title"]) > 15 else row["title"]
        plt.annotate(
            f"{row['rank']}위: {title_abbr}",
            (row["review_count"] + 1, row["sales_index"] + 1),
            xytext=(10, 5), textcoords="offset points",
            fontsize=9, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.2", fc="yellow", alpha=0.5)
        )

    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()
    return save_path


def plot_top_publishers(df: pd.DataFrame, output_dir: str = os.path.join("yes24", "images")) -> str:
    """
    베스트셀러 도서 수 기준 상위 10대 출판사의 시장 점유율과 총 판매지수 합계를 시각화합니다.

    Args:
        df (pd.DataFrame): 전처리된 베스트셀러 데이터프레임.
        output_dir (str): 차트 이미지를 저장할 디렉토리 경로.

    Returns:
        str: 생성된 이미지 파일의 경로.
    """
    os.makedirs(output_dir, exist_ok=True)
    save_path = os.path.join(output_dir, "eda_04_top_publishers.png")

    pub_stats = df.groupby("publisher").agg(
        book_count=("goods_no", "count"),
        total_sales_index=("sales_index", "sum"),
        mean_price=("sale_price", "mean")
    ).sort_values(by="book_count", ascending=False).head(10)

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # 1. 상위 10개 출판사 도서 수
    sns.barplot(x=pub_stats["book_count"], y=pub_stats.index, ax=axes[0], palette="crest_r")
    axes[0].set_title("상위 10대 출판사 베스트셀러 등재 도서 수", fontsize=13, fontweight="bold")
    axes[0].set_xlabel("등재 도서 수 (권)")
    axes[0].set_ylabel("출판사")
    for i, v in enumerate(pub_stats["book_count"]):
        axes[0].text(v + 0.5, i, f"{v}권 ({v/len(df)*100:.1f}%)", va="center", fontsize=10)

    # 2. 상위 10개 출판사 총 판매지수
    pub_sales_sorted = pub_stats.sort_values(by="total_sales_index", ascending=False)
    sns.barplot(x=pub_sales_sorted["total_sales_index"] / 1000, y=pub_sales_sorted.index, ax=axes[1], palette="flare_r")
    axes[1].set_title("상위 출판사별 누적 판매지수 합계 (천 단위)", fontsize=13, fontweight="bold")
    axes[1].set_xlabel("누적 판매지수 (x1,000)")
    axes[1].set_ylabel("")
    for i, v in enumerate(pub_sales_sorted["total_sales_index"] / 1000):
        axes[1].text(v + 1, i, f"{v:,.1f}k", va="center", fontsize=10)

    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()
    return save_path


def plot_keyword_frequency(df: pd.DataFrame, output_dir: str = os.path.join("yes24", "images")) -> str:
    """
    태그(#) 및 도서명에서 추출한 주요 IT 기술 키워드 출현 빈도 TOP 20을 시각화합니다.

    Args:
        df (pd.DataFrame): 전처리된 베스트셀러 데이터프레임.
        output_dir (str): 차트 이미지를 저장할 디렉토리 경로.

    Returns:
        str: 생성된 이미지 파일의 경로.
    """
    os.makedirs(output_dir, exist_ok=True)
    save_path = os.path.join(output_dir, "eda_05_keyword_frequency.png")

    # 태그에서 키워드 추출
    tag_counter = Counter()
    for tag_str in df["tags"]:
        if tag_str:
            # '#태그명' 형태 분리
            tags = [t.strip().replace("#", "") for t in tag_str.split(",") if t.strip()]
            tag_counter.update(tags)

    # 상위 20개 키워드 추출
    top_20 = tag_counter.most_common(20)
    if not top_20:
        # 태그가 부족한 경우 제목에서 키워드 추출
        words = []
        for title in df["title"]:
            words.extend(re.findall(r"[가-힣A-Za-z0-9]{2,}", title))
        top_20 = Counter(words).most_common(20)

    keywords, counts = zip(*top_20)

    plt.figure(figsize=(12, 6))
    colors = sns.color_palette("viridis", len(keywords))
    bars = plt.barh(keywords[::-1], counts[::-1], color=colors)
    plt.title("YES24 베스트셀러 주요 태그/키워드 출현 빈도 TOP 20", fontsize=14, fontweight="bold")
    plt.xlabel("출현 빈도 (회)", fontsize=12)
    plt.ylabel("키워드 / 태그", fontsize=12)

    for bar in bars:
        width = bar.get_width()
        plt.text(width + 0.3, bar.get_y() + bar.get_height() / 2, f"{int(width)}회", va="center", fontsize=10)

    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()
    return save_path


def plot_pub_year_trend(df: pd.DataFrame, output_dir: str = os.path.join("yes24", "images")) -> str:
    """
    도서 출간 연도별 분포를 분석하여 최신간과 스테디셀러의 시장 비중을 시각화합니다.

    Args:
        df (pd.DataFrame): 전처리된 베스트셀러 데이터프레임.
        output_dir (str): 차트 이미지를 저장할 디렉토리 경로.

    Returns:
        str: 생성된 이미지 파일의 경로.
    """
    os.makedirs(output_dir, exist_ok=True)
    save_path = os.path.join(output_dir, "eda_06_pub_year_trend.png")

    valid_years = df[df["pub_year"] > 2015]["pub_year"]
    year_counts = valid_years.value_counts().sort_index()

    fig, axes = plt.subplots(1, 2, figsize=(16, 5))

    # 1. 연도별 도서 수 추이
    sns.barplot(x=year_counts.index.astype(int), y=year_counts.values, ax=axes[0], palette="magma")
    axes[0].set_title("출간 연도별 베스트셀러 도서 수 분포", fontsize=13, fontweight="bold")
    axes[0].set_xlabel("출간 연도")
    axes[0].set_ylabel("도서 수 (권)")
    for p in axes[0].patches:
        height = p.get_height()
        axes[0].annotate(f"{int(height)}권", (p.get_x() + p.get_width() / 2., height + 1),
                         ha="center", fontsize=10)

    # 2. 신간 vs 스테디셀러 비중 (2025~2026년 기준)
    df["is_recent"] = df["pub_year"].apply(lambda y: "최신간 (2025~2026)" if y >= 2025 else "스테디셀러 (2024 이전)")
    recent_counts = df["is_recent"].value_counts()
    axes[1].pie(
        recent_counts.values,
        labels=recent_counts.index,
        autopct="%1.1f%%",
        startangle=140,
        colors=["#3470a3", "#e07a5f"],
        explode=[0.05, 0],
        textprops={"fontsize": 11, "fontweight": "bold"}
    )
    axes[1].set_title("베스트셀러 내 최신간 vs 스테디셀러 구성 비중", fontsize=13, fontweight="bold")

    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()
    return save_path


def run_full_eda() -> Dict[str, any]:
    """
    전체 EDA 파이프라인을 실행하고 통계 요약 딕셔너리를 반환합니다.

    Returns:
        Dict[str, any]: 핵심 통계 결과 딕셔너리.
    """
    print("=" * 70)
    print("YES24 일별 베스트셀러 탐색적 데이터 분석(EDA) 파이프라인 시작")
    print("=" * 70)

    # 1. 데이터 로드 및 전처리
    df = load_and_preprocess_data()
    total_count = len(df)
    print(f"[1] 데이터 로드 완료: 총 {total_count}개 도서 레코드")

    # 2. 6대 시각화 차트 생성
    output_dir = os.path.join("yes24", "images")
    p1 = plot_price_distribution(df, output_dir)
    print(f"  -> [차트 1 저장] 가격 및 할인율 분포: {p1}")

    p2 = plot_correlation_heatmap(df, output_dir)
    print(f"  -> [차트 2 저장] 스피어만 상관계수 히트맵: {p2}")

    p3 = plot_sales_vs_reviews(df, output_dir)
    print(f"  -> [차트 3 저장] 판매지수 vs 리뷰 수 산점도: {p3}")

    p4 = plot_top_publishers(df, output_dir)
    print(f"  -> [차트 4 저장] 상위 10대 출판사 점유율: {p4}")

    p5 = plot_keyword_frequency(df, output_dir)
    print(f"  -> [차트 5 저장] 키워드/태그 빈도 TOP 20: {p5}")

    p6 = plot_pub_year_trend(df, output_dir)
    print(f"  -> [차트 6 저장] 출간 연도별 시계열 분포: {p6}")

    # 3. 주요 기술 통계량 산출
    stats_summary = {
        "total_books": total_count,
        "mean_sale_price": round(df["sale_price"].mean()),
        "median_sale_price": round(df["sale_price"].median()),
        "mean_fixed_price": round(df["fixed_price"].mean()),
        "common_discount_rate": int(df["discount_rate"].mode()[0]),
        "mean_rating": round(df[df["rating"] > 0]["rating"].mean(), 2),
        "mean_review_count": round(df["review_count"].mean(), 1),
        "max_sales_index": int(df["sales_index"].max()),
        "top_sales_book": df.loc[df["sales_index"].idxmax(), "title"],
        "top_publisher": df["publisher"].mode()[0],
        "top_publisher_books": int(df["publisher"].value_counts().iloc[0]),
        "recent_book_ratio": round((df["pub_year"] >= 2025).mean() * 100, 1)
    }

    print("\n" + "=" * 70)
    print("[주요 분석 요약]")
    print(f" - 평균 판매가: {stats_summary['mean_sale_price']:,}원 (중앙값: {stats_summary['median_sale_price']:,}원)")
    print(f" - 지배적 할인율: {stats_summary['common_discount_rate']}% (도서정가제 표준)")
    print(f" - 평균 평점: {stats_summary['mean_rating']}점 / 평균 리뷰 수: {stats_summary['mean_review_count']}개")
    print(f" - 1위 판매지수 도서: {stats_summary['top_sales_book']} ({stats_summary['max_sales_index']:,}점)")
    print(f" - 최대 점유 출판사: {stats_summary['top_publisher']} ({stats_summary['top_publisher_books']}권, {stats_summary['top_publisher_books']/total_count*100:.1f}%)")
    print(f" - 최신간(2025~2026) 비중: {stats_summary['recent_book_ratio']}%")
    print("=" * 70)

    return stats_summary


if __name__ == "__main__":
    run_full_eda()
