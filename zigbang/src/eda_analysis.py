# -*- coding: utf-8 -*-
"""
충북 청주시 청원구 오창읍 원룸·빌라 월세 심층 탐색적 데이터 분석 (EDA) 스크립트
- 20년차 데이터 분석가 수준의 전문 시각화 11종 생성 (DPI 150)
- Scikit-learn TF-IDF 기반 상위 30대 핵심 키워드 가중치 추출
- 대시보드 경량 로딩을 위한 summary_data.json 산출
- Seaborn 전역 스타일(set_theme, set_style) 설정 금지 원칙 준수
"""

import json
import os
import re
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
import koreanize_matplotlib

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
IMAGES_DIR = BASE_DIR / "images"
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

CSV_PATH = DATA_DIR / "zigbang_daily_ochang_monthly_rent_20261029.csv"


def run_eda():
    print(f"[*] CSV 데이터 로드: {CSV_PATH}")
    df = pd.read_csv(CSV_PATH)
    print(f"    - 총 데이터 크기: {df.shape[0]}행, {df.shape[1]}열")
    print(f"    - 결측치 수: {df.isnull().sum().sum()}개")
    print(f"    - 중복치 수: {df.duplicated(subset=['item_id']).sum()}개")

    # 1. 기술통계 및 기본 지표 산출
    num_cols = ["deposit_manwon", "rent_manwon", "manage_cost_manwon", "total_monthly_cost", "size_pyeong", "cost_per_pyeong"]
    desc_num = df[num_cols].describe().round(2)
    print("\n=== 수치형 변수 기술통계 ===")
    print(desc_num)

    # 차트 색상 팔레트 정의
    c_blue = "#2563eb"
    c_indigo = "#4f46e5"
    c_sky = "#0284c7"
    c_teal = "#0d9488"
    c_amber = "#d97706"
    c_rose = "#e11d48"
    c_slate = "#475569"

    # ==========================================
    # Chart 01: 실질 월세 및 총 주거비용 분포 (히스토그램 & KDE)
    # ==========================================
    fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
    sns.histplot(df["rent_manwon"], kde=True, color=c_blue, bins=25, ax=ax, label="순수 월세 (만원)", alpha=0.5)
    sns.histplot(df["total_monthly_cost"], kde=True, color=c_rose, bins=25, ax=ax, label="실질 총주거비 (월세+관리비)", alpha=0.4)
    ax.axvline(df["rent_manwon"].median(), color=c_blue, linestyle="--", linewidth=1.5, label=f"월세 중위수 ({df['rent_manwon'].median():.0f}만원)")
    ax.axvline(df["total_monthly_cost"].median(), color=c_rose, linestyle="--", linewidth=1.5, label=f"실질비용 중위수 ({df['total_monthly_cost'].median():.1f}만원)")
    ax.set_title("오창읍 원룸·빌라 월세 및 실질 총 주거비용 분포 (KDE & 히스토그램)", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("비용 (만원/월)", fontsize=11)
    ax.set_ylabel("매물 빈도수 (건)", fontsize=11)
    ax.legend(frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1")
    ax.grid(True, linestyle=":", alpha=0.6)
    plt.tight_layout()
    fig.savefig(IMAGES_DIR / "chart01_monthly_rent_dist.png")
    plt.close()
    print("[+] Chart 01 저장 완료")

    # ==========================================
    # Chart 02: 방 구조별 매물 구성비 (도넛 차트)
    # ==========================================
    fig, ax = plt.subplots(figsize=(8, 8), dpi=150)
    struct_counts = df["structure_type"].value_counts()
    colors = [c_blue, c_indigo, c_teal, c_amber, c_rose, c_slate][:len(struct_counts)]
    wedges, texts, autotexts = ax.pie(
        struct_counts,
        labels=struct_counts.index,
        autopct="%1.1f%%",
        startangle=140,
        colors=colors,
        pctdistance=0.75,
        wedgeprops=dict(width=0.4, edgecolor="#ffffff", linewidth=2)
    )
    for at in autotexts:
        at.set_fontsize(10)
        at.set_fontweight("bold")
    ax.set_title("오창읍 매물 방 구조 유형별 점유 비율", fontsize=14, fontweight="bold", pad=15)
    plt.tight_layout()
    fig.savefig(IMAGES_DIR / "chart02_structure_composition.png")
    plt.close()
    print("[+] Chart 02 저장 완료")

    # ==========================================
    # Chart 03: 세부 권역(리)별 월세 분포 비교 (박스플롯)
    # ==========================================
    fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
    dong_order = df["sub_dong"].value_counts().index[:5]
    sub_df = df[df["sub_dong"].isin(dong_order)]
    sns.boxplot(x="sub_dong", y="rent_manwon", data=sub_df, order=dong_order, ax=ax, palette="Blues_r", boxprops=dict(alpha=0.8))
    sns.stripplot(x="sub_dong", y="rent_manwon", data=sub_df, order=dong_order, ax=ax, color="#1e293b", size=4, alpha=0.3, jitter=0.2)
    ax.set_title("오창읍 주요 권역(리)별 월세 분포 및 이상치 비교", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("오창읍 세부 권역", fontsize=11)
    ax.set_ylabel("월세 (만원)", fontsize=11)
    ax.grid(True, axis="y", linestyle=":", alpha=0.6)
    plt.tight_layout()
    fig.savefig(IMAGES_DIR / "chart03_subdong_rent_boxplot.png")
    plt.close()
    print("[+] Chart 03 저장 완료")

    # ==========================================
    # Chart 04: 전용면적(평) 대비 실질 총주거비 산점도 & 회귀선
    # ==========================================
    fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
    sns.scatterplot(
        x="size_pyeong",
        y="total_monthly_cost",
        hue="structure_type",
        data=df,
        ax=ax,
        palette="tab10",
        alpha=0.75,
        s=45
    )
    # 추세 회귀선
    sns.regplot(
        x="size_pyeong",
        y="total_monthly_cost",
        data=df,
        scatter=False,
        ax=ax,
        color="#dc2626",
        line_kws={"linestyle": "--", "linewidth": 2, "label": "면적-주거비 추세선"}
    )
    ax.set_title("전용면적(평) 대비 실질 총 주거비용 상관관계", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("전용면적 (평)", fontsize=11)
    ax.set_ylabel("실질 총 주거비용 (만원/월)", fontsize=11)
    ax.set_xlim(4, 30)
    ax.set_ylim(10, 150)
    ax.legend(frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1")
    ax.grid(True, linestyle=":", alpha=0.6)
    plt.tight_layout()
    fig.savefig(IMAGES_DIR / "chart04_rent_vs_size_scatter.png")
    plt.close()
    print("[+] Chart 04 저장 완료")

    # ==========================================
    # Chart 05: 보증금 구간별 평균 월세 및 건수 비교
    # ==========================================
    df["deposit_bin"] = pd.cut(
        df["deposit_manwon"],
        bins=[-1, 200, 300, 500, 1000, 10000],
        labels=["200만 이하", "201~300만", "301~500만", "501~1,000만", "1,000만 초과"]
    )
    dep_summary = df.groupby("deposit_bin", observed=True).agg(
        avg_rent=("rent_manwon", "mean"),
        count=("item_id", "count")
    ).reset_index()

    fig, ax1 = plt.subplots(figsize=(10, 6), dpi=150)
    ax2 = ax1.twinx()
    bars = ax1.bar(dep_summary["deposit_bin"], dep_summary["avg_rent"], color=c_indigo, alpha=0.8, width=0.45, label="평균 월세 (만원)")
    lines = ax2.plot(dep_summary["deposit_bin"], dep_summary["count"], color=c_amber, marker="o", linewidth=2.5, markersize=7, label="매물수 (건)")
    
    for b in bars:
        h = b.get_height()
        ax1.text(b.get_x() + b.get_width() / 2, h + 1, f"{h:.1f}만", ha="center", va="bottom", fontsize=10, fontweight="bold")
    
    for i, txt in enumerate(dep_summary["count"]):
        ax2.annotate(f"{txt}건", (i, txt + 5), ha="center", fontsize=10, fontweight="bold", color=c_amber)

    ax1.set_title("보증금 구간별 평균 월세 수준 및 매물 분포", fontsize=14, fontweight="bold", pad=15)
    ax1.set_xlabel("보증금 구간", fontsize=11)
    ax1.set_ylabel("평균 월세 (만원)", fontsize=11, color=c_indigo)
    ax2.set_ylabel("매물 건수 (건)", fontsize=11, color=c_amber)
    ax1.set_ylim(0, dep_summary["avg_rent"].max() * 1.25)
    ax2.set_ylim(0, dep_summary["count"].max() * 1.3)
    ax1.grid(True, axis="y", linestyle=":", alpha=0.6)
    plt.tight_layout()
    fig.savefig(IMAGES_DIR / "chart05_deposit_rent_tradeoff.png")
    plt.close()
    print("[+] Chart 05 저장 완료")

    # ==========================================
    # Chart 06: 방 구조별 평당 실질 주거비용 (가성비 지수)
    # ==========================================
    fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
    cost_order = df.groupby("structure_type")["cost_per_pyeong"].mean().sort_values(ascending=False).index
    sns.barplot(x="structure_type", y="cost_per_pyeong", data=df, order=cost_order, ax=ax, palette="mako", ci=None)
    for p in ax.patches:
        h = p.get_height()
        ax.annotate(f"{h:.1f}만원/평", (p.get_x() + p.get_width() / 2., h + 0.1), ha="center", va="bottom", fontsize=10, fontweight="bold")
    ax.set_title("방 구조 유형별 평당 실질 주거비용 (가성비 지수)", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("방 구조 유형", fontsize=11)
    ax.set_ylabel("평당 실질비용 (만원/평)", fontsize=11)
    ax.set_ylim(0, df["cost_per_pyeong"].max() * 0.7)
    ax.grid(True, axis="y", linestyle=":", alpha=0.6)
    plt.tight_layout()
    fig.savefig(IMAGES_DIR / "chart06_cost_per_pyeong_rank.png")
    plt.close()
    print("[+] Chart 06 저장 완료")

    # ==========================================
    # Chart 07: 층수 구분별(저/중/고) 월세 및 면적 비교
    # ==========================================
    fig, ax = plt.subplots(figsize=(9, 6), dpi=150)
    floor_stats = df.groupby("floor_category").agg(
        avg_rent=("rent_manwon", "mean"),
        avg_size=("size_pyeong", "mean")
    ).reindex(["저층", "중층", "고층"])
    
    x = np.arange(len(floor_stats))
    width = 0.35
    ax.bar(x - width/2, floor_stats["avg_rent"], width, label="평균 월세 (만원)", color=c_blue, alpha=0.85)
    ax.bar(x + width/2, floor_stats["avg_size"], width, label="평균 면적 (평)", color=c_teal, alpha=0.85)
    
    for i in range(len(floor_stats)):
        ax.text(x[i] - width/2, floor_stats["avg_rent"].iloc[i] + 0.8, f"{floor_stats['avg_rent'].iloc[i]:.1f}만", ha="center", fontsize=10, fontweight="bold")
        ax.text(x[i] + width/2, floor_stats["avg_size"].iloc[i] + 0.8, f"{floor_stats['avg_size'].iloc[i]:.1f}평", ha="center", fontsize=10, fontweight="bold")

    ax.set_title("층수 카테고리별 평균 월세 및 평균 전용면적 비교", fontsize=14, fontweight="bold", pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(floor_stats.index, fontsize=11)
    ax.set_ylabel("수치", fontsize=11)
    ax.set_ylim(0, floor_stats["avg_rent"].max() * 1.25)
    ax.legend(frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1")
    ax.grid(True, axis="y", linestyle=":", alpha=0.6)
    plt.tight_layout()
    fig.savefig(IMAGES_DIR / "chart07_floor_level_analysis.png")
    plt.close()
    print("[+] Chart 07 저장 완료")

    # ==========================================
    # Chart 08: 엘리베이터 유무 및 풀옵션 여부별 월세 차이
    # ==========================================
    fig, ax = plt.subplots(figsize=(9, 6), dpi=150)
    df["ele_label"] = df["has_elevator"].map({1: "엘리베이터 있음", 0: "엘리베이터 없음"})
    df["opt_label"] = df["has_full_option"].map({1: "풀옵션 완료", 0: "기본/일반"})
    opt_summary = df.groupby(["ele_label", "opt_label"])["rent_manwon"].mean().reset_index()
    sns.barplot(x="ele_label", y="rent_manwon", hue="opt_label", data=opt_summary, ax=ax, palette=["#38bdf8", "#0284c7"])
    for p in ax.patches:
        h = p.get_height()
        if h > 0:
            ax.annotate(f"{h:.1f}만", (p.get_x() + p.get_width() / 2., h + 0.8), ha="center", va="bottom", fontsize=10, fontweight="bold")
    ax.set_title("엘리베이터 유무 및 풀옵션 여부에 따른 평균 월세 프리미엄", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("편의시설 (승강기)", fontsize=11)
    ax.set_ylabel("평균 월세 (만원)", fontsize=11)
    ax.set_ylim(0, opt_summary["rent_manwon"].max() * 1.25)
    ax.legend(title="옵션 수준", frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1")
    ax.grid(True, axis="y", linestyle=":", alpha=0.6)
    plt.tight_layout()
    fig.savefig(IMAGES_DIR / "chart08_option_score_effect.png")
    plt.close()
    print("[+] Chart 08 저장 완료")

    # ==========================================
    # Chart 09: 오창읍 매물 지리적 공간 분포 (위경도 산점도)
    # ==========================================
    fig, ax = plt.subplots(figsize=(10, 7), dpi=150)
    sns.scatterplot(
        x="longitude",
        y="latitude",
        hue="sub_dong",
        size="rent_manwon",
        sizes=(20, 150),
        data=df,
        ax=ax,
        palette="viridis",
        alpha=0.75
    )
    ax.set_title("오창읍 원룸·빌라 매물 지리적 공간 분포 및 월세 클러스터", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("경도 (Longitude)", fontsize=11)
    ax.set_ylabel("위도 (Latitude)", fontsize=11)
    ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1")
    ax.grid(True, linestyle=":", alpha=0.6)
    plt.tight_layout()
    fig.savefig(IMAGES_DIR / "chart09_spatial_cluster_kde.png")
    plt.close()
    print("[+] Chart 09 저장 완료")

    # ==========================================
    # Chart 10: Scikit-learn TF-IDF 상위 30대 핵심 키워드 가중치
    # ==========================================
    # 텍스트 정제
    titles = df["title"].dropna().tolist()
    clean_titles = []
    stop_words = {"오창", "청주", "청원구", "매물", "원룸", "빌라", "투룸", "월세", "전세", "보증금", "추천", "즉시", "입주", "가능", "완료", "최고", "인기", "강추"}
    for t in titles:
        # 한글, 영문, 숫자 추출
        words = re.findall(r"[가-힣a-zA-Z0-9]+", str(t))
        filtered = [w for w in words if len(w) >= 2 and w not in stop_words]
        clean_titles.append(" ".join(filtered))

    tfidf = TfidfVectorizer(max_features=30)
    tfidf_matrix = tfidf.fit_transform(clean_titles)
    tfidf_scores = np.array(tfidf_matrix.sum(axis=0)).flatten()
    keywords = tfidf.get_feature_names_out()
    
    tfidf_df = pd.DataFrame({"keyword": keywords, "score": tfidf_scores}).sort_values("score", ascending=True)

    fig, ax = plt.subplots(figsize=(10, 8), dpi=150)
    bars = ax.barh(tfidf_df["keyword"], tfidf_df["score"], color=c_teal, alpha=0.85)
    ax.set_title("직방 오창읍 매물 제목/설명 Scikit-learn TF-IDF 핵심 키워드 Top 30", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("TF-IDF 중요도 총합 점수", fontsize=11)
    ax.grid(True, axis="x", linestyle=":", alpha=0.6)
    plt.tight_layout()
    fig.savefig(IMAGES_DIR / "chart10_tfidf_keywords_top30.png")
    plt.close()
    print("[+] Chart 10 저장 완료")

    # ==========================================
    # Chart 11: 주요 수치형 변수 간 상관관계 히트맵
    # ==========================================
    corr_cols = ["deposit_manwon", "rent_manwon", "manage_cost_manwon", "total_monthly_cost", "size_pyeong", "cost_per_pyeong", "current_floor", "option_score"]
    corr_labels = ["보증금", "월세", "관리비", "총주거비", "전용면적(평)", "평당비용", "층수", "옵션스코어"]
    corr_matrix = df[corr_cols].corr()
    corr_matrix.columns = corr_labels
    corr_matrix.index = corr_labels

    fig, ax = plt.subplots(figsize=(9, 7), dpi=150)
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", cbar=True, vmin=-1, vmax=1, ax=ax, linewidths=0.5)
    ax.set_title("오창읍 원룸·빌라 주요 주거 지표 피어슨 상관계수 매트릭스", fontsize=14, fontweight="bold", pad=15)
    plt.tight_layout()
    fig.savefig(IMAGES_DIR / "chart11_correlation_matrix.png")
    plt.close()
    print("[+] Chart 11 저장 완료")

    # ==========================================
    # 대시보드 사전 집계 summary_data.json 생성
    # ==========================================
    kpi_data = {
        "total_items": int(df.shape[0]),
        "avg_rent": float(round(df["rent_manwon"].mean(), 1)),
        "median_rent": float(round(df["rent_manwon"].median(), 1)),
        "avg_deposit": float(round(df["deposit_manwon"].mean(), 1)),
        "avg_total_cost": float(round(df["total_monthly_cost"].mean(), 1)),
        "avg_size_pyeong": float(round(df["size_pyeong"].mean(), 1)),
        "avg_cost_per_pyeong": float(round(df["cost_per_pyeong"].mean(), 1)),
        "full_option_ratio": float(round(df["has_full_option"].mean() * 100, 1)),
        "elevator_ratio": float(round(df["has_elevator"].mean() * 100, 1)),
    }

    # 차트용 사전 집계
    summary = {
        "kpi": kpi_data,
        "structure_counts": df["structure_type"].value_counts().to_dict(),
        "subdong_counts": df["sub_dong"].value_counts().to_dict(),
        "subdong_avg_rent": df.groupby("sub_dong")["rent_manwon"].mean().round(1).to_dict(),
        "structure_avg_rent": df.groupby("structure_type")["rent_manwon"].mean().round(1).to_dict(),
        "structure_avg_size": df.groupby("structure_type")["size_pyeong"].mean().round(1).to_dict(),
        "deposit_bins": dep_summary.to_dict(orient="records"),
        "top_keywords": tfidf_df.tail(15).to_dict(orient="records"),
        "floor_stats": floor_stats.reset_index().to_dict(orient="records"),
        "items": df.to_dict(orient="records")  # 전수 매물 데이터 포함 (대시보드 실시간 검색/테이블/지도용)
    }

    summary_path = DATA_DIR / "summary_data.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(f"[+] summary_data.json 생성 완료: {summary_path}")

    return df, desc_num


if __name__ == "__main__":
    run_eda()
