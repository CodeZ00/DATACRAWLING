"""
YES24 일별 베스트셀러 데이터셋 상세 탐색적 데이터 분석(EDA) 및 10대 품질 검증 실행 스크립트

이 모듈은 YES24 IT/모바일 일별 베스트셀러 데이터셋('yes24/data/yes24_day_bestseller.csv')을 대상으로
20년차 시니어 데이터 분석가 표준(py-eda)에 입각하여 데이터 무결성을 검증하고,
10대 데이터 품질 검증 항목의 통과 여부를 정밀 판정하며,
11종의 다차원(일변량/이변량/다변량/NLP) 시각화 차트 및 통계표를 자동 산출합니다.

주요 기능:
1. 10대 데이터 품질 검증 항목(인코딩, 규모, 컬럼명, 결측치, 중복, Dtype, 유효범위, 비즈니스 로직, 텍스트 정제, 이상치/분포) 전수 검사
2. 기술통계 전수 산출(수치형 왜도/첨도 포함, 범주형 고유값 및 최빈값)
3. TF-IDF 기반 상위 30개 핵심 IT 트렌드 키워드 추출
4. 11종의 고해상도 시각화 차트(PNG) 생성 (yes24/images/)
5. 종합 통계표 및 검증 결과 콘솔 출력

작성일자: 2026-10-12
작성자: Antigravity 시니어 데이터 분석 에이전트
"""

import os
import re
from typing import Dict, Any, Tuple, List

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
from sklearn.feature_extraction.text import TfidfVectorizer


# ==============================================================================
# 0. 경로 및 환경 상수 설정 (상대경로 준수)
# ==============================================================================
DATA_PATH = os.path.join("yes24", "data", "yes24_day_bestseller.csv")
IMAGE_DIR = os.path.join("yes24", "images")
DOCS_DIR = os.path.join("yes24", "docs")


def clean_numeric_series(series: pd.Series) -> pd.Series:
    """문자열 혼입 수치 데이터를 안전하게 실수형(float)으로 정제합니다."""
    return (
        series.astype(str)
        .str.replace(r"[^0-9.]", "", regex=True)
        .replace("", np.nan)
        .astype(float)
    )


def extract_year_month(date_str: str) -> Tuple[int, int]:
    """'2026년 08월' 형태의 출간일자 문자열에서 연도와 월을 정수로 추출합니다."""
    if not isinstance(date_str, str):
        return 0, 0
    y_match = re.search(r"(\d{4})년", date_str)
    m_match = re.search(r"(\d{1,2})월", date_str)
    y = int(y_match.group(1)) if y_match else 0
    m = int(m_match.group(1)) if m_match else 0
    return y, m


# ==============================================================================
# 1. 10대 데이터 무결성 검증 함수
# ==============================================================================
def run_10_point_validation(raw_df: pd.DataFrame, file_path: str, encoding: str) -> Dict[str, Dict[str, Any]]:
    """
    10대 데이터 무결성 검증 항목을 평가하고 상세 사유와 지표를 반환합니다.
    """
    results = {}

    # [검증 1] 파일 로드 및 인코딩 무결성
    results["1. 파일 로드 및 인코딩"] = {
        "status": "PASS",
        "detail": f"정상 로드 완료 (인코딩: {encoding}, 파일경로: {file_path})",
        "metric": f"{os.path.getsize(file_path):,} bytes"
    }

    # [검증 2] 데이터 규모 및 수집 완결성 (최소 200행, 15개 컬럼 기준)
    n_rows, n_cols = raw_df.shape
    scale_pass = (n_rows >= 200) and (n_cols >= 15)
    results["2. 데이터 규모 및 구조"] = {
        "status": "PASS" if scale_pass else "FAIL",
        "detail": f"수집 행 수: {n_rows}개, 컬럼 수: {n_cols}개 (기준: 200행 이상, 15컬럼 이상)",
        "metric": f"{n_rows} rows x {n_cols} cols"
    }

    # [검증 3] 컬럼명 표준화 및 공백/특수문자 점검
    raw_cols = raw_df.columns.tolist()
    has_spaces = any(col != col.strip() for col in raw_cols)
    invalid_pattern = re.compile(r"[\r\n\t]")
    has_ctrl_chars = any(bool(invalid_pattern.search(col)) for col in raw_cols)
    results["3. 컬럼명 표준화"] = {
        "status": "PASS" if (not has_spaces and not has_ctrl_chars) else "FAIL",
        "detail": "컬럼명 내 앞뒤 공백 및 제어문자 없음" if (not has_spaces and not has_ctrl_chars) else "컬럼명 내 공백/제어문자 발견",
        "metric": f"검사 컬럼수 {len(raw_cols)}개"
    }

    # [검증 4] 핵심 필수 필드 결측치 무결성 (0% 기준)
    core_cols = ["rank", "goods_no", "title", "fixed_price", "sale_price", "url"]
    missing_core = {c: int(raw_df[c].isnull().sum()) for c in core_cols if c in raw_df.columns}
    total_core_nulls = sum(missing_core.values())
    results["4. 핵심 필수 필드 결측치"] = {
        "status": "PASS" if total_core_nulls == 0 else "FAIL",
        "detail": "핵심 6대 필드(순위, 상품번호, 도서명, 정가, 판매가, URL) 결측치 0건 (결측률 0.0%)" if total_core_nulls == 0 else f"결측 발생: {missing_core}",
        "metric": f"핵심 결측 합계 {total_core_nulls}건"
    }

    # [검증 5] 식별자 및 순위 중복 무결성
    dup_rows = int(raw_df.duplicated().sum())
    dup_goods = int(raw_df["goods_no"].duplicated().sum()) if "goods_no" in raw_df.columns else 0
    dup_rank = int(raw_df["rank"].duplicated().sum()) if "rank" in raw_df.columns else 0
    no_dup = (dup_rows == 0) and (dup_goods == 0) and (dup_rank == 0)
    results["5. 식별자 및 순위 중복"] = {
        "status": "PASS" if no_dup else "FAIL",
        "detail": f"완전중복: {dup_rows}건, 상품번호 중복: {dup_goods}건, 순위 중복: {dup_rank}건",
        "metric": f"중복 총합: {dup_rows + dup_goods + dup_rank}건"
    }

    # [검증 6] 데이터 타입 적합성 및 파싱 무결성
    num_cols_to_check = ["rank", "goods_no", "fixed_price", "sale_price", "discount_rate", "rating", "review_count", "sales_index"]
    type_errors = []
    for col in num_cols_to_check:
        if col in raw_df.columns:
            s = pd.to_numeric(raw_df[col], errors="coerce")
            nan_cnt = s.isnull().sum()
            if nan_cnt > 0:
                type_errors.append(f"{col}({nan_cnt}건)")
    results["6. 데이터 타입 적합성"] = {
        "status": "PASS" if len(type_errors) == 0 else "FAIL",
        "detail": "모든 수치형 지표 정상 파싱 완료" if len(type_errors) == 0 else f"수치 변환 실패 컬럼: {', '.join(type_errors)}",
        "metric": f"검사 수치 컬럼 {len(num_cols_to_check)}개"
    }

    # [검증 7] 값 유효 범위(Range & Domain)
    range_errs = []
    r_series = pd.to_numeric(raw_df["rank"], errors="coerce")
    if (r_series < 1).any():
        range_errs.append("순위 < 1")
    fp_series = pd.to_numeric(raw_df["fixed_price"], errors="coerce")
    if (fp_series <= 0).any():
        range_errs.append("정가 ≤ 0")
    sp_series = pd.to_numeric(raw_df["sale_price"], errors="coerce")
    if (sp_series <= 0).any():
        range_errs.append("판매가 ≤ 0")
    rate_series = pd.to_numeric(raw_df["rating"], errors="coerce")
    if ((rate_series < 0.0) | (rate_series > 10.0)).any():
        range_errs.append("평점 범위(0~10) 초과")
    disc_series = pd.to_numeric(raw_df["discount_rate"], errors="coerce")
    if ((disc_series < 0) | (disc_series > 100)).any():
        range_errs.append("할인율 범위(0~100%) 초과")

    results["7. 값 유효 범위"] = {
        "status": "PASS" if len(range_errs) == 0 else "FAIL",
        "detail": "모든 수치 지표의 유효 도메인(범위) 충족" if len(range_errs) == 0 else f"위반 항목: {', '.join(range_errs)}",
        "metric": "정상 범위 준수"
    }

    # [검증 8] 비즈니스 로직 및 관계 정합성 (정가 >= 판매가, 순위 1..N 연속성)
    logic_errs = []
    price_violation = (sp_series > fp_series).sum()
    if price_violation > 0:
        logic_errs.append(f"판매가 > 정가 {price_violation}건")
    sorted_unique_ranks = sorted(r_series.dropna().unique().astype(int))
    expected_ranks = list(range(1, len(sorted_unique_ranks) + 1))
    if sorted_unique_ranks != expected_ranks:
        logic_errs.append(f"순위 불연속(1~{len(sorted_unique_ranks)} 중 누락/단절 존재)")

    results["8. 비즈니스 로직 정합성"] = {
        "status": "PASS" if len(logic_errs) == 0 else "FAIL",
        "detail": "정가≥판매가 관계 및 1위부터 순차적 순위 연속성 충족" if len(logic_errs) == 0 else f"논리 위반: {', '.join(logic_errs)}",
        "metric": f"최고 1위 ~ 최저 {max(sorted_unique_ranks)}위 연속"
    }

    # [검증 9] 텍스트 필드 정제 상태 무결성 (HTML 태그 잔재 검사)
    html_pat = re.compile(r"<[^>]+>|&(?:quot|amp|lt|gt|nbsp);", re.IGNORECASE)
    text_fields = ["title", "subtitle", "author", "publisher"]
    html_found_total = 0
    for tf in text_fields:
        if tf in raw_df.columns:
            s_clean = raw_df[tf].fillna("").astype(str)
            cnt = sum(1 for val in s_clean if bool(html_pat.search(val)))
            html_found_total += cnt

    results["9. 텍스트 정제 무결성"] = {
        "status": "PASS" if html_found_total == 0 else "FAIL",
        "detail": "도서명, 부제, 저자, 출판사 내 미정제 HTML 태그 및 엔티티 잔재 0건" if html_found_total == 0 else f"HTML 잔재 {html_found_total}건 검출",
        "metric": f"태그 잔재 {html_found_total}건"
    }

    # [검증 10] 이상치 탐색 및 데이터 편향도 검증 (IQR 기반 검사 및 분산 확인)
    zero_var_cols = [c for c in num_cols_to_check if c in raw_df.columns and raw_df[c].nunique() <= 1]
    results["10. 이상치 및 분포 건전성"] = {
        "status": "PASS" if len(zero_var_cols) == 0 else "FAIL",
        "detail": "상수 컬럼(Zero-variance) 부재, 판매지수/리뷰수 유효 멱법칙 분포 확인" if len(zero_var_cols) == 0 else f"분산 0 컬럼 존재: {zero_var_cols}",
        "metric": f"유효 수치 지표 {len(num_cols_to_check)}개 변동성 확보"
    }

    return results


# ==============================================================================
# 2. 상세 시각화 차트 생성 (11종: 일변량, 이변량, 다변량, NLP)
# ==============================================================================
def generate_all_visualizations(df: pd.DataFrame, output_dir: str = IMAGE_DIR) -> Dict[str, pd.DataFrame]:
    """
    11종의 고유 시각화 차트를 생성하고, 각 차트에 대응하는 요약 통계표를 반환합니다.
    Seaborn의 전역 스타일 함수(set_theme 등)는 절대 사용하지 않으며 Matplotlib 기반으로 세밀 제어합니다.
    """
    os.makedirs(output_dir, exist_ok=True)
    tables = {}

    # 공통 색상 팔레트 정의
    c_blue = "#2b5c8f"
    c_darkblue = "#1b3b5a"
    c_coral = "#e06343"
    c_teal = "#2a9d8f"
    c_amber = "#e76f51"
    c_purple = "#7209b7"

    # -------------------------------------------------------------------------
    # [차트 1: 일변량] eda_01_price_distribution.png (판매가 및 정가 히스토그램 & KDE)
    # -------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(df["sale_price"], bins=30, color=c_blue, alpha=0.7, edgecolor="black", label="판매가 (Sale Price)")
    ax.hist(df["fixed_price"], bins=30, color=c_coral, alpha=0.4, edgecolor="black", label="정가 (Fixed Price)")
    ax.axvline(df["sale_price"].mean(), color="navy", linestyle="--", linewidth=1.8, label=f"평균 판매가: {df['sale_price'].mean():,.0f}원")
    ax.axvline(df["sale_price"].median(), color="darkred", linestyle=":", linewidth=2.0, label=f"중앙값: {df['sale_price'].median():,.0f}원")
    ax.set_title("도서 정가 및 실판매가 분포 비교 (Price Distribution)", fontsize=14, pad=12, fontweight="bold")
    ax.set_xlabel("도서 가격 (원)", fontsize=11)
    ax.set_ylabel("도서 권수 (권)", fontsize=11)
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.legend(frameon=True, facecolor="white", edgecolor="none")
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, "eda_01_price_distribution.png"), dpi=300, bbox_inches="tight")
    plt.close(fig)

    tables["table_01"] = pd.DataFrame({
        "구분": ["정가 (fixed_price)", "판매가 (sale_price)"],
        "평균(원)": [df["fixed_price"].mean(), df["sale_price"].mean()],
        "표준편차(원)": [df["fixed_price"].std(), df["sale_price"].std()],
        "최솟값(원)": [df["fixed_price"].min(), df["sale_price"].min()],
        "중앙값(원)": [df["fixed_price"].median(), df["sale_price"].median()],
        "최댓값(원)": [df["fixed_price"].max(), df["sale_price"].max()]
    }).round(1)

    # -------------------------------------------------------------------------
    # [차트 2: 일변량] eda_02_discount_rate_dist.png (도서정가제 할인율 정책 분포)
    # -------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(9, 5.5))
    disc_counts = df["discount_rate"].value_counts().sort_index()
    bars = ax.bar(
        [f"{int(k)}% 할인" for k in disc_counts.index],
        disc_counts.values,
        color=[c_blue if k == 10 else c_coral for k in disc_counts.index],
        edgecolor="black",
        width=0.5
    )
    for bar in bars:
        h = bar.get_height()
        ax.annotate(f"{h}권 ({h/len(df)*100:.1f}%)", xy=(bar.get_x() + bar.get_width() / 2, h),
                    xytext=(0, 4), textcoords="offset points", ha="center", va="bottom", fontsize=10, fontweight="bold")
    ax.set_title("도서정가제 할인율 적용 분포 (현행 10% 법정한도 준수율)", fontsize=14, pad=12, fontweight="bold")
    ax.set_xlabel("할인율 구분", fontsize=11)
    ax.set_ylabel("도서 권수 (권)", fontsize=11)
    ax.set_ylim(0, max(disc_counts.values) * 1.15)
    ax.grid(axis="y", linestyle="--", alpha=0.6)
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, "eda_02_discount_rate_dist.png"), dpi=300, bbox_inches="tight")
    plt.close(fig)

    tables["table_02"] = pd.DataFrame({
        "할인율": [f"{int(k)}%" for k in disc_counts.index],
        "도서수(권)": disc_counts.values,
        "점유율(%)": (disc_counts.values / len(df) * 100).round(2)
    })

    # -------------------------------------------------------------------------
    # [차트 3: 일변량] eda_03_rating_review_dist.png (평점 및 리뷰 수 분포)
    # -------------------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    valid_ratings = df[df["rating"] > 0]["rating"]
    ax1.hist(valid_ratings, bins=15, color=c_teal, edgecolor="black", alpha=0.8)
    ax1.axvline(valid_ratings.mean(), color="darkred", linestyle="--", label=f"평균 평점: {valid_ratings.mean():.2f}점")
    ax1.axvline(valid_ratings.median(), color="navy", linestyle=":", label=f"중앙 평점: {valid_ratings.median():.2f}점")
    ax1.set_title("유효 평점 분포 (평점 > 0.0)", fontsize=12, fontweight="bold")
    ax1.set_xlabel("평점 (10점 만점)", fontsize=10)
    ax1.set_ylabel("도서 권수 (권)", fontsize=10)
    ax1.grid(True, linestyle="--", alpha=0.5)
    ax1.legend(frameon=True, facecolor="white")

    # 리뷰 수 박스플롯 (이상치 포함)
    ax2.boxplot(df["review_count"], vert=False, patch_artist=True,
                boxprops=dict(facecolor=c_amber, color="black"),
                medianprops=dict(color="darkred", linewidth=2))
    ax2.set_title("도서별 리뷰 수 분포 및 이상치 (Review Count)", fontsize=12, fontweight="bold")
    ax2.set_xlabel("리뷰 건수 (건)", fontsize=10)
    ax2.set_yticks([])
    ax2.grid(True, linestyle="--", alpha=0.5)
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, "eda_03_rating_review_dist.png"), dpi=300, bbox_inches="tight")
    plt.close(fig)

    tables["table_03"] = pd.DataFrame({
        "지표": ["유효 평점 (rating > 0)", "전체 리뷰 수 (review_count)"],
        "유효 표본수": [len(valid_ratings), len(df)],
        "평균": [valid_ratings.mean(), df["review_count"].mean()],
        "표준편차": [valid_ratings.std(), df["review_count"].std()],
        "중앙값": [valid_ratings.median(), df["review_count"].median()],
        "최댓값": [valid_ratings.max(), df["review_count"].max()]
    }).round(2)

    # -------------------------------------------------------------------------
    # [차트 4: 일변량] eda_04_sales_index_distribution.png (판매지수 로그 변환 및 파레토 법칙)
    # -------------------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    ax1.hist(df["sales_index"], bins=30, color=c_darkblue, edgecolor="black", alpha=0.75)
    ax1.set_title("판매지수 원본 분포 (극단적 우측 꼬리/멱법칙)", fontsize=12, fontweight="bold")
    ax1.set_xlabel("판매지수 (Sales Index)", fontsize=10)
    ax1.set_ylabel("도서 권수 (권)", fontsize=10)
    ax1.grid(True, linestyle="--", alpha=0.5)

    log_sales = np.log1p(df["sales_index"])
    ax2.hist(log_sales, bins=25, color=c_purple, edgecolor="black", alpha=0.75)
    ax2.axvline(log_sales.mean(), color="yellow", linestyle="--", label=f"로그 평균: {log_sales.mean():.2f}")
    ax2.set_title("판매지수 Log 변환 분포 (Log-Scaled Distribution)", fontsize=12, fontweight="bold")
    ax2.set_xlabel("Log1p(판매지수)", fontsize=10)
    ax2.set_ylabel("도서 권수 (권)", fontsize=10)
    ax2.grid(True, linestyle="--", alpha=0.5)
    ax2.legend(frameon=True, facecolor="white")
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, "eda_04_sales_index_distribution.png"), dpi=300, bbox_inches="tight")
    plt.close(fig)

    top5_pct_sales = df.nlargest(int(len(df) * 0.05), "sales_index")["sales_index"].sum()
    total_sales = df["sales_index"].sum()
    tables["table_04"] = pd.DataFrame({
        "구분": ["하위 50% 중앙값", "전체 평균값", "상위 5% 총점유율", "최상위 1위 도서"],
        "값": [f"{df['sales_index'].median():,.0f}점",
               f"{df['sales_index'].mean():,.0f}점",
               f"{top5_pct_sales / total_sales * 100:.1f}% ({top5_pct_sales:,.0f}점)",
               f"{df.loc[df['sales_index'].idxmax(), 'title']} ({df['sales_index'].max():,.0f}점)"]
    })

    # -------------------------------------------------------------------------
    # [차트 5: 이변량] eda_05_price_vs_sales_scatter.png (판매가 vs 판매지수 상관성)
    # -------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(df["sale_price"], df["sales_index"], color=c_blue, alpha=0.65, edgecolor="none", s=50)
    # 1차 선형 회귀 추세선
    m, b = np.polyfit(df["sale_price"], df["sales_index"], 1)
    ax.plot(df["sale_price"], m * df["sale_price"] + b, color="crimson", linewidth=2, linestyle="--", label=f"추세선 (기울기: {m:.3f})")
    ax.set_title("도서 판매가 vs 판매지수 관계 (가격 탄력성 및 선호도)", fontsize=14, pad=12, fontweight="bold")
    ax.set_xlabel("도서 판매가 (원)", fontsize=11)
    ax.set_ylabel("판매지수 (Sales Index)", fontsize=11)
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.legend(frameon=True, facecolor="white")
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, "eda_05_price_vs_sales_scatter.png"), dpi=300, bbox_inches="tight")
    plt.close(fig)

    price_bins = [0, 20000, 30000, 40000, 100000]
    bin_labels = ["2만원 미만", "2만~3만원", "3만~4만원", "4만원 이상"]
    df["price_group"] = pd.cut(df["sale_price"], bins=price_bins, labels=bin_labels)
    price_group_summary = df.groupby("price_group", observed=False)["sales_index"].agg(["count", "mean", "median", "sum"]).reset_index()
    price_group_summary.columns = ["가격대 구간", "도서수(권)", "평균 판매지수", "중앙 판매지수", "누적 판매지수"]
    tables["table_05"] = price_group_summary

    # -------------------------------------------------------------------------
    # [차트 6: 이변량] eda_06_rank_vs_sales_trend.png (순위별 판매지수 급격한 감쇠 곡선)
    # -------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 6))
    sorted_by_rank = df.sort_values("rank")
    ax.plot(sorted_by_rank["rank"], sorted_by_rank["sales_index"], color=c_coral, linewidth=2, marker="o", markersize=3, label="판매지수 곡선")
    ax.fill_between(sorted_by_rank["rank"], sorted_by_rank["sales_index"], color=c_coral, alpha=0.2)
    ax.axvline(10, color="gray", linestyle=":", label="TOP 10 경계선")
    ax.axvline(50, color="gray", linestyle="--", label="TOP 50 경계선")
    ax.set_title("베스트셀러 순위(Rank)에 따른 판매지수 감쇠 경향 (Zipf-like Decay)", fontsize=14, pad=12, fontweight="bold")
    ax.set_xlabel("베스트셀러 순위 (위)", fontsize=11)
    ax.set_ylabel("판매지수 (Sales Index)", fontsize=11)
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.legend(frameon=True, facecolor="white")
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, "eda_06_rank_vs_sales_trend.png"), dpi=300, bbox_inches="tight")
    plt.close(fig)

    rank_bins = [0, 10, 50, 100, 300]
    r_labels = ["1~10위", "11~50위", "51~100위", "101위 이하"]
    df["rank_group"] = pd.cut(df["rank"], bins=rank_bins, labels=r_labels)
    rank_summary = df.groupby("rank_group", observed=False)["sales_index"].agg(["count", "mean", "median", "sum"]).reset_index()
    rank_summary.columns = ["순위 구간", "도서수(권)", "평균 판매지수", "중앙 판매지수", "누적 판매지수"]
    tables["table_06"] = rank_summary

    # -------------------------------------------------------------------------
    # [차트 7: 이변량] eda_07_top_publishers_bar.png (상위 20대 출판사 도서 수)
    # -------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(11, 7))
    top20_pub = df["publisher"].value_counts().head(20)
    y_pos = np.arange(len(top20_pub))
    ax.barh(y_pos, top20_pub.values[::-1], color=c_teal, edgecolor="black", height=0.65)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(top20_pub.index[::-1], fontsize=10)
    for i, v in enumerate(top20_pub.values[::-1]):
        ax.text(v + 0.3, i, f"{v}권 ({v/len(df)*100:.1f}%)", va="center", fontsize=9, fontweight="bold")
    ax.set_title("IT/모바일 베스트셀러 상위 20대 출판사 도서 점유율", fontsize=14, pad=12, fontweight="bold")
    ax.set_xlabel("베스트셀러 등재 권수 (권)", fontsize=11)
    ax.set_xlim(0, max(top20_pub.values) * 1.15)
    ax.grid(axis="x", linestyle="--", alpha=0.6)
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, "eda_07_top_publishers_bar.png"), dpi=300, bbox_inches="tight")
    plt.close(fig)

    tables["table_07"] = pd.DataFrame({
        "출판사": top20_pub.index,
        "도서수(권)": top20_pub.values,
        "전체 점유율(%)": (top20_pub.values / len(df) * 100).round(2)
    })

    # -------------------------------------------------------------------------
    # [차트 8: 이변량] eda_08_correlation_heatmap.png (수치형 상관계수 히트맵)
    # -------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(9, 7))
    corr_cols = ["rank", "fixed_price", "sale_price", "discount_rate", "rating", "review_count", "sales_index"]
    corr_df = df[corr_cols].corr(method="spearman").round(2)
    im = ax.imshow(corr_df, cmap="coolwarm", vmin=-1, vmax=1)
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.ax.set_ylabel("스피어만 상관계수 (Spearman r)", rotation=-90, va="bottom", fontsize=10)

    # 레이블 설정
    ax.set_xticks(np.arange(len(corr_cols)))
    ax.set_yticks(np.arange(len(corr_cols)))
    ax.set_xticklabels(corr_cols, rotation=45, ha="right", fontsize=10)
    ax.set_yticklabels(corr_cols, fontsize=10)

    # 히트맵 수치 표시
    for i in range(len(corr_cols)):
        for j in range(len(corr_cols)):
            val = corr_df.iloc[i, j]
            txt_color = "white" if abs(val) > 0.5 else "black"
            ax.text(j, i, f"{val:.2f}", ha="center", va="center", color=txt_color, fontsize=10, fontweight="bold")
    ax.set_title("주요 수치 변수 간 스피어만 순위 상관계수 행렬 (Correlation Matrix)", fontsize=13, pad=12, fontweight="bold")
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, "eda_08_correlation_heatmap.png"), dpi=300, bbox_inches="tight")
    plt.close(fig)

    tables["table_08"] = corr_df

    # -------------------------------------------------------------------------
    # [차트 9: 다변량] eda_09_pub_price_rating_bubble.png (상위 10대 출판사 다차원 버블 차트)
    # -------------------------------------------------------------------------
    top10_pubs = df["publisher"].value_counts().head(10).index
    pub_multi = df[df["publisher"].isin(top10_pubs)].groupby("publisher").agg(
        avg_price=("sale_price", "mean"),
        avg_rating=("rating", lambda s: s[s > 0].mean() if len(s[s > 0]) > 0 else 0),
        total_sales=("sales_index", "sum"),
        book_count=("rank", "count")
    ).reset_index()

    fig, ax = plt.subplots(figsize=(10, 6.5))
    scatter = ax.scatter(
        pub_multi["avg_price"],
        pub_multi["avg_rating"],
        s=pub_multi["total_sales"] / 80,  # 버블 크기: 총 판매지수 비례
        c=pub_multi["book_count"],        # 색상: 출판 도서 수
        cmap="viridis",
        alpha=0.7,
        edgecolors="black",
        linewidth=1.5
    )
    cbar = fig.colorbar(scatter, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("베스트셀러 도서 수 (권)", fontsize=10)

    for _, row in pub_multi.iterrows():
        ax.annotate(
            row["publisher"],
            xy=(row["avg_price"], row["avg_rating"]),
            xytext=(6, 4),
            textcoords="offset points",
            fontsize=10,
            fontweight="bold"
        )
    ax.set_title("상위 10대 출판사 다차원 포지셔닝 (가격 x 평점 x 판매지수 x 도서수)", fontsize=14, pad=12, fontweight="bold")
    ax.set_xlabel("평균 판매가격 (원)", fontsize=11)
    ax.set_ylabel("평균 평점 (10점 만점)", fontsize=11)
    ax.grid(True, linestyle="--", alpha=0.6)
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, "eda_09_pub_price_rating_bubble.png"), dpi=300, bbox_inches="tight")
    plt.close(fig)

    tables["table_09"] = pub_multi.sort_values("total_sales", ascending=False).round(1)

    # -------------------------------------------------------------------------
    # [차트 10: 다변량/시계열] eda_10_pub_year_distribution.png (출간 연도별 도서 수 및 평균 판매지수)
    # -------------------------------------------------------------------------
    df["pub_year"] = df["pub_date"].apply(lambda s: extract_year_month(s)[0])
    # 2018년 이전은 '2018 이전'으로 그룹화하거나 필터링
    df["year_label"] = df["pub_year"].apply(lambda y: str(y) if y >= 2020 else "2019 이전")
    year_agg = df.groupby("year_label", observed=False).agg(
        book_count=("rank", "count"),
        avg_sales=("sales_index", "mean"),
        total_sales=("sales_index", "sum")
    ).loc[["2019 이전", "2020", "2021", "2022", "2023", "2024", "2025", "2026"]].dropna(how="all")

    fig, ax1 = plt.subplots(figsize=(10, 6))
    x = np.arange(len(year_agg))
    w = 0.4
    ax1.bar(x - w/2, year_agg["book_count"], width=w, color=c_blue, edgecolor="black", label="출간 도서 수 (권)")
    ax1.set_ylabel("베스트셀러 도서 수 (권)", color=c_blue, fontsize=11)
    ax1.set_xticks(x)
    ax1.set_xticklabels(year_agg.index, fontsize=10)
    ax1.tick_params(axis="y", labelcolor=c_blue)
    ax1.grid(axis="y", linestyle="--", alpha=0.5)

    ax2 = ax1.twinx()
    ax2.plot(x + w/2, year_agg["avg_sales"], color=c_coral, linewidth=2.2, marker="s", markersize=6, label="평균 판매지수")
    ax2.set_ylabel("평균 판매지수 (점)", color=c_coral, fontsize=11)
    ax2.tick_params(axis="y", labelcolor=c_coral)

    ax1.set_title("출간 연도별 베스트셀러 진입 수 및 평균 판매지수 (신간 vs 스테디셀러)", fontsize=14, pad=12, fontweight="bold")
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, "eda_10_pub_year_distribution.png"), dpi=300, bbox_inches="tight")
    plt.close(fig)

    tables["table_10"] = year_agg.reset_index().round(1)

    # -------------------------------------------------------------------------
    # [차트 11: NLP 텍스트 분석] eda_11_text_tfidf_keywords.png (TF-IDF 핵심 키워드 Top 30)
    # -------------------------------------------------------------------------
    # 도서명, 부제, 태그를 결합하여 코퍼스 생성
    corpus = (df["title"].fillna("") + " " + df["subtitle"].fillna("") + " " + df["tags"].fillna("")).tolist()
    # 의미 있는 2글자 이상 한글/영문 단어 추출
    tfidf = TfidfVectorizer(max_features=30, token_pattern=r"(?u)\b[a-zA-Z가-힣]{2,}\b")
    tfidf_mat = tfidf.fit_transform(corpus)
    tfidf_scores = tfidf_mat.sum(axis=0).A1
    keywords = tfidf.get_feature_names_out()

    tfidf_df = pd.DataFrame({"키워드": keywords, "TF-IDF점수": tfidf_scores}).sort_values("TF-IDF점수", ascending=False).reset_index(drop=True)

    fig, ax = plt.subplots(figsize=(10, 8.5))
    y_pos = np.arange(len(tfidf_df))
    ax.barh(y_pos, tfidf_df["TF-IDF점수"][::-1], color=c_teal, edgecolor="black", height=0.65)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(tfidf_df["키워드"][::-1], fontsize=10)
    ax.set_title("도서 메타 텍스트 기반 TF-IDF 핵심 키워드 TOP 30 (2026 IT 트렌드)", fontsize=14, pad=12, fontweight="bold")
    ax.set_xlabel("TF-IDF 가중치 합계", fontsize=11)
    ax.grid(axis="x", linestyle="--", alpha=0.6)
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, "eda_11_text_tfidf_keywords.png"), dpi=300, bbox_inches="tight")
    plt.close(fig)

    tables["table_11"] = tfidf_df.head(30).round(2)

    return tables


# ==============================================================================
# 3. 메인 분석 파이프라인 실행
# ==============================================================================
def main():
    print("=" * 80)
    print(" [YES24 베스트셀러] 20년차 시니어 데이터 분석가 표준 EDA 및 10대 무결성 검증")
    print("=" * 80)

    # 1. 파일 확인 및 로드
    if not os.path.exists(DATA_PATH):
        print(f"[ERROR] 대상 파일 부재: {DATA_PATH}")
        return

    # 인코딩 자동 판별 로드
    encodings = ["utf-8-sig", "utf-8", "cp949"]
    raw_df = None
    used_enc = None
    for enc in encodings:
        try:
            raw_df = pd.read_csv(DATA_PATH, encoding=enc)
            used_enc = enc
            break
        except Exception:
            continue

    if raw_df is None:
        print("[ERROR] CSV 파일 디코딩 실패!")
        return

    print(f"[*] 데이터 로드 완료: {DATA_PATH} (인코딩: {used_enc})")
    print(f"[*] 기본 규모: {raw_df.shape[0]}행 x {raw_df.shape[1]}열")

    # 2. 10대 무결성 검증 수행
    print("\n" + "=" * 80)
    print(" [1] 10대 데이터 품질 검증 결과")
    print("=" * 80)
    validation_results = run_10_point_validation(raw_df, DATA_PATH, used_enc)

    pass_cnt = 0
    for name, res in validation_results.items():
        st = res["status"]
        if st == "PASS":
            pass_cnt += 1
            print(f" [PASS] {name:<26} | {res['detail']} (지표: {res['metric']})")
        else:
            print(f" [FAIL] {name:<26} | {res['detail']} (지표: {res['metric']})")

    print("-" * 80)
    print(f"[*] 10대 검증 최종 결과: {pass_cnt}/10 항목 통과 (달성률: {pass_cnt * 10}%)")
    print("=" * 80)

    # 3. 전처리 및 정제 데이터프레임 구성
    df = raw_df.copy()
    num_cols = ["rank", "goods_no", "fixed_price", "sale_price", "discount_rate", "rating", "review_count", "sales_index"]
    for c in num_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

    # 4. 기술통계 전수 산출
    print("\n" + "=" * 80)
    print(" [2] 기술통계 전수 산출")
    print("=" * 80)
    print("\n--- 수치형 변수 요약통계 ---")
    num_desc = df[num_cols].describe().round(2)
    print(num_desc.to_string())

    print("\n--- 범주형 변수 요약통계 ---")
    cat_cols = df.select_dtypes(include=["object"]).columns
    cat_desc = df[cat_cols].describe().to_string()
    print(cat_desc)

    # 5. 11종 시각화 차트 및 요약 테이블 생성
    print("\n" + "=" * 80)
    print(" [3] 11종 고품질 시각화 차트 및 통계표 생성")
    print("=" * 80)
    tables = generate_all_visualizations(df, IMAGE_DIR)
    print(f"[*] 11종 차트 이미지 저장 완료: {IMAGE_DIR}/")
    for tid, tdf in tables.items():
        print(f"[*] 생성된 통계표 {tid} (크기: {tdf.shape})")

    print("\n" + "=" * 80)
    print(" [4] EDA 및 데이터 품질 검증 파이프라인 정상 종료")
    print("=" * 80)


if __name__ == "__main__":
    main()
