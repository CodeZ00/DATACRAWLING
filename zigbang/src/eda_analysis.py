"""직방 세종특별자치시 정부청사 생활권(어진동·나성동·도담동) 오피스텔 심층 EDA 분석기.

- 20년차 데이터 분석가 가이드라인 완벽 준수
- 실거주 정주 여건 및 가성비 중심 10대 고해상도(DPI 150) 시각화 차트 생성
- Scikit-learn TF-IDF 기반 거주민 리뷰 및 매물 특성 키워드 마이닝
- 대시보드 경량 연동을 위한 summary_data.json 사전 집계
"""

import json
import os
import re
import warnings
from pathlib import Path

import koreanize_matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer

warnings.filterwarnings("ignore")


def load_data():
    base_dir = Path(__file__).resolve().parent.parent / "data"
    csv_files = list(base_dir.glob("zigbang_officetel_sejong_*.csv"))
    if not csv_files:
        raise FileNotFoundError("수집된 오피스텔 CSV 파일을 찾을 수 없습니다.")
    latest_csv = sorted(csv_files)[-1]
    print(f"[*] 분석 대상 데이터셋 로드: {latest_csv.name}")
    df = pd.read_csv(latest_csv, encoding="utf-8-sig")
    return df, latest_csv


def print_basic_inspection(df):
    print("=" * 70)
    print("1. 기본 데이터 파악 (Basic Data Inspection)")
    print("=" * 70)
    print(f"총 데이터 크기: {df.shape[0]}행 x {df.shape[1]}열")
    print(f"중복 행 수: {df.duplicated().sum()}건")
    print("\n[상위 3개 행]")
    print(df[["item_id", "dong", "danji_name", "sales_type", "deposit_manwon", "rent_manwon", "total_monthly_cost_manwon"]].head(3))
    print("\n[수치형 기술통계 (describe)]")
    numeric_cols = ["deposit_manwon", "rent_manwon", "manage_cost_won", "total_monthly_cost_manwon", "exclusive_area_pyeong", "building_age", "unit_rent_per_pyeong", "manage_cost_per_pyeong"]
    print(df[numeric_cols].describe().round(2))
    print("\n[범주형 기술통계]")
    print(df[["dong", "sales_type", "danji_name"]].describe())
    print("=" * 70)


def generate_charts(df, img_dir):
    os.makedirs(img_dir, exist_ok=True)
    plt.rcParams["font.family"] = "Pretendard" if "Pretendard" in plt.rcParams["font.sans-serif"] else "Malgun Gothic"

    # 1. 01_dong_distribution_pie.png (행정동별 매물 분포 도넛 차트)
    fig, ax = plt.subplots(figsize=(8, 7), dpi=150)
    dong_counts = df["dong"].value_counts()
    colors = ["#F59E0B", "#10B981", "#3B82F6"]
    wedges, texts, autotexts = ax.pie(
        dong_counts.values,
        labels=dong_counts.index,
        autopct="%1.1f%%",
        startangle=140,
        colors=colors[:len(dong_counts)],
        wedgeprops=dict(width=0.4, edgecolor="white", linewidth=2),
        pctdistance=0.75,
        textprops=dict(fontsize=12, fontweight="bold")
    )
    for at in autotexts:
        at.set_color("white")
        at.set_fontsize(13)
    ax.set_title("세종 정부청사 생활권 행정동별 오피스텔 매물 점유율", fontsize=15, fontweight="bold", pad=20)
    plt.tight_layout()
    p1 = img_dir / "01_dong_distribution_pie.png"
    plt.savefig(p1, bbox_inches="tight")
    plt.close()
    print(f"[+] 차트 1 생성: {p1.name}")

    # 2. 02_sales_type_ratio.png (거래 유형별 비중 및 평균 보증금/월세)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), dpi=150)
    type_counts = df["sales_type"].value_counts()
    ax1.bar(type_counts.index, type_counts.values, color=["#F59E0B", "#3B82F6", "#10B981"], edgecolor="#1E293B", linewidth=1.2, width=0.5)
    for idx, val in enumerate(type_counts.values):
        ax1.text(idx, val + 0.5, f"{val}건 ({val/len(df)*100:.1f}%)", ha="center", fontsize=11, fontweight="bold")
    ax1.set_title("거래 유형별 매물 건수 분포", fontsize=13, fontweight="bold")
    ax1.set_ylabel("매물 수 (건)")
    ax1.grid(axis="y", linestyle="--", alpha=0.5)

    type_rent = df[df["sales_type"] == "월세"].groupby("dong")["rent_manwon"].mean()
    ax2.bar(type_rent.index, type_rent.values, color="#F59E0B", edgecolor="#B45309", width=0.4)
    for idx, val in enumerate(type_rent.values):
        ax2.text(idx, val + 1, f"평균 {val:.1f}만", ha="center", fontsize=11, fontweight="bold")
    ax2.set_title("동별 월세 매물 평균 임대료 (만원)", fontsize=13, fontweight="bold")
    ax2.set_ylabel("월세 (만원)")
    ax2.grid(axis="y", linestyle="--", alpha=0.5)
    plt.suptitle("거래 유형 및 동별 임대료 구조 비교", fontsize=15, fontweight="bold", y=1.02)
    plt.tight_layout()
    p2 = img_dir / "02_sales_type_ratio.png"
    plt.savefig(p2, bbox_inches="tight")
    plt.close()
    print(f"[+] 차트 2 생성: {p2.name}")

    # 3. 03_monthly_total_cost_distribution.png (월 총 주거비용 히스토그램 & KDE)
    fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
    rent_df = df[df["sales_type"] == "월세"]
    costs = rent_df["total_monthly_cost_manwon"]
    bins = np.arange(costs.min() - 5, costs.max() + 10, 5)
    n, b, patches = ax.hist(costs, bins=bins, color="#FBBF24", edgecolor="#D97706", alpha=0.7, density=True)
    sns.kdeplot(costs, ax=ax, color="#B45309", linewidth=2.5, label="밀도 추정선 (KDE)")
    mean_cost = costs.mean()
    median_cost = costs.median()
    ax.axvline(mean_cost, color="#DC2626", linestyle="--", linewidth=1.8, label=f"평균: {mean_cost:.1f}만원")
    ax.axvline(median_cost, color="#2563EB", linestyle=":", linewidth=2.0, label=f"중앙값: {median_cost:.1f}만원")
    ax.set_title("실거주자 월 총 주거비용(월세 + 관리비) 구간 분포", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("월 총 주거비용 (만원)")
    ax.set_ylabel("밀도 (Density)")
    ax.legend(fontsize=11)
    ax.grid(axis="x", linestyle="--", alpha=0.4)
    plt.tight_layout()
    p3 = img_dir / "03_monthly_total_cost_distribution.png"
    plt.savefig(p3, bbox_inches="tight")
    plt.close()
    print(f"[+] 차트 3 생성: {p3.name}")

    # 4. 04_area_vs_rent_scatter.png (전용면적 대비 월세 상관관계)
    fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
    sns.regplot(
        data=rent_df,
        x="exclusive_area_pyeong",
        y="rent_manwon",
        ax=ax,
        scatter_kws={"color": "#F59E0B", "s": 80, "alpha": 0.8, "edgecolors": "white"},
        line_kws={"color": "#B45309", "linewidth": 2.2, "label": "선형 회귀 추세선"}
    )
    # 어진동 호수의아침, 푸르지오시티 라벨링
    for _, row in rent_df.iterrows():
        if row["rent_manwon"] >= 70 or row["exclusive_area_pyeong"] >= 10:
            ax.annotate(
                f"{row['danji_name']} ({row['rent_manwon']}만)",
                xy=(row["exclusive_area_pyeong"], row["rent_manwon"]),
                xytext=(5, 5),
                textcoords="offset points",
                fontsize=9,
                color="#1E293B"
            )
    corr = rent_df["exclusive_area_pyeong"].corr(rent_df["rent_manwon"])
    ax.set_title(f"전용면적(평) vs 월세 상관관계 분석 (상관계수 r = {corr:.2f})", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("전용면적 (평)")
    ax.set_ylabel("월세 (만원)")
    ax.legend(fontsize=11)
    ax.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    p4 = img_dir / "04_area_vs_rent_scatter.png"
    plt.savefig(p4, bbox_inches="tight")
    plt.close()
    print(f"[+] 차트 4 생성: {p4.name}")

    # 5. 05_pyeong_rent_by_dong.png (행정동별 전용 평당 월세 가성비 박스플롯)
    fig, ax = plt.subplots(figsize=(9, 6), dpi=150)
    sns.boxplot(
        data=rent_df,
        x="dong",
        y="unit_rent_per_pyeong",
        palette=["#F59E0B", "#10B981", "#3B82F6"],
        ax=ax,
        width=0.45,
        fliersize=5
    )
    sns.stripplot(
        data=rent_df,
        x="dong",
        y="unit_rent_per_pyeong",
        color="#1E293B",
        alpha=0.6,
        size=6,
        jitter=0.15,
        ax=ax
    )
    ax.set_title("행정동별 전용 평당 월세 단가(가성비) 분포 비교", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("행정동")
    ax.set_ylabel("전용 평당 월세단가 (만원/평)")
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    p5 = img_dir / "05_pyeong_rent_by_dong.png"
    plt.savefig(p5, bbox_inches="tight")
    plt.close()
    print(f"[+] 차트 5 생성: {p5.name}")

    # 6. 06_manage_cost_burden_by_danji.png (단지별 평당 관리비 부담률)
    fig, ax = plt.subplots(figsize=(11, 6), dpi=150)
    danji_manage = df.groupby("danji_name")["manage_cost_per_pyeong"].mean().sort_values()
    bars = ax.barh(danji_manage.index, danji_manage.values, color="#F59E0B", edgecolor="#B45309", height=0.55)
    for b in bars:
        w = b.get_width()
        ax.text(w + 300, b.get_y() + b.get_height()/2, f"{int(w):,}원/평", va="center", fontsize=10, fontweight="bold")
    ax.set_title("주요 단지별 전용 평당 관리비 부담률 비교", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("전용 평당 관리비 (원/평)")
    ax.set_xlim(0, danji_manage.max() * 1.2)
    ax.grid(axis="x", linestyle="--", alpha=0.5)
    plt.tight_layout()
    p6 = img_dir / "06_manage_cost_burden_by_danji.png"
    plt.savefig(p6, bbox_inches="tight")
    plt.close()
    print(f"[+] 차트 6 생성: {p6.name}")

    # 7. 07_floor_premium_analysis.png (층수 비율별 평당 임대료 프리미엄)
    fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
    rent_df["floor_group"] = pd.cut(
        rent_df["floor_ratio"],
        bins=[0, 0.35, 0.7, 1.0],
        labels=["저층 (하위 35%)", "중층 (35~70%)", "고층 (상위 30%)"]
    )
    floor_stats = rent_df.groupby("floor_group")["unit_rent_per_pyeong"].agg(["mean", "count"]).dropna()
    ax.plot(floor_stats.index, floor_stats["mean"], marker="o", markersize=10, linewidth=2.5, color="#D97706", label="평균 평당 월세")
    for idx, (grp, row) in enumerate(floor_stats.iterrows()):
        ax.text(idx, row["mean"] + 0.15, f"{row['mean']:.2f}만/평\n(N={int(row['count'])}건)", ha="center", fontsize=11, fontweight="bold")
    ax.set_title("층수 비율(저층·중층·고층)에 따른 평당 임대료 프리미엄 추이", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("층수 그룹")
    ax.set_ylabel("평균 평당 월세 (만원/평)")
    ax.set_ylim(floor_stats["mean"].min() - 0.5, floor_stats["mean"].max() + 0.8)
    ax.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    p7 = img_dir / "07_floor_premium_analysis.png"
    plt.savefig(p7, bbox_inches="tight")
    plt.close()
    print(f"[+] 차트 7 생성: {p7.name}")

    # 8. 08_building_age_vs_rent_depreciation.png (노후도 감가상각 분석)
    fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
    age_stats = rent_df.groupby("building_age")["unit_rent_per_pyeong"].mean()
    ax.plot(age_stats.index, age_stats.values, marker="s", markersize=8, color="#2563EB", linewidth=2.2, label="경과연수별 평당 월세")
    ax.scatter(rent_df["building_age"], rent_df["unit_rent_per_pyeong"], color="#93C5FD", alpha=0.7, s=50, label="개별 매물 관측치")
    for x, y in age_stats.items():
        ax.annotate(f"{y:.2f}만", xy=(x, y), xytext=(0, 8), textcoords="offset points", ha="center", fontsize=9, fontweight="bold")
    ax.set_title("준공 후 경과연수(노후도)에 따른 임대료 감가상각 추이", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("준공 후 경과연수 (년)")
    ax.set_ylabel("전용 평당 월세 (만원/평)")
    ax.legend(fontsize=11)
    ax.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    p8 = img_dir / "08_building_age_vs_rent_depreciation.png"
    plt.savefig(p8, bbox_inches="tight")
    plt.close()
    print(f"[+] 차트 8 생성: {p8.name}")

    # 9. 09_tfidf_resident_review_keywords.png (TF-IDF 상위 30대 키워드 분석)
    text_corpus = (df["title"].fillna("") + " " + df["review_recent"].fillna("")).tolist()
    # 한글 및 영문 2글자 이상 추출 정제
    cleaned_corpus = [re.sub(r"[^\w\s]", " ", t) for t in text_corpus if len(t.strip()) > 3]

    tfidf = TfidfVectorizer(max_features=30, min_df=1, token_pattern=r"(?u)\b\w{2,}\b")
    tfidf_matrix = tfidf.fit_transform(cleaned_corpus)
    scores = np.asarray(tfidf_matrix.mean(axis=0)).ravel()
    keywords = sorted(zip(tfidf.get_feature_names_out(), scores), key=lambda x: x[1], reverse=True)

    fig, ax = plt.subplots(figsize=(12, 8), dpi=150)
    kw_names = [k[0] for k in keywords[:25]][::-1]
    kw_scores = [k[1] for k in keywords[:25]][::-1]
    bars = ax.barh(kw_names, kw_scores, color="#F59E0B", edgecolor="#B45309", height=0.6)
    for b in bars:
        ax.text(b.get_width() + 0.002, b.get_y() + b.get_height()/2, f"{b.get_width():.3f}", va="center", fontsize=9)
    ax.set_title("세종 오피스텔 거주민 리뷰 & 매물 설명 TF-IDF 상위 25대 핵심 키워드", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("TF-IDF 평균 가중치 (Mean Importance Score)")
    ax.grid(axis="x", linestyle="--", alpha=0.5)
    plt.tight_layout()
    p9 = img_dir / "09_tfidf_resident_review_keywords.png"
    plt.savefig(p9, bbox_inches="tight")
    plt.close()
    print(f"[+] 차트 9 생성: {p9.name}")

    # 10. 10_sejong_officetel_geo_bubble.png (지리적 가성비 버블 차트)
    fig, ax = plt.subplots(figsize=(10, 8), dpi=150)
    sc = ax.scatter(
        df["lng"],
        df["lat"],
        s=df["exclusive_area_pyeong"] * 25,
        c=df["total_monthly_cost_manwon"],
        cmap="YlOrRd",
        alpha=0.8,
        edgecolors="#1E293B",
        linewidth=1.2
    )
    cbar = plt.colorbar(sc, ax=ax)
    cbar.set_label("월 총 주거비용 (만원/월)", fontsize=11, fontweight="bold")
    
    # 단지별 대표 라벨
    for dong_name, grp in df.groupby("dong"):
        center_x = grp["lng"].mean()
        center_y = grp["lat"].mean()
        ax.annotate(
            f"[{dong_name}]\n평균 {grp['total_monthly_cost_manwon'].mean():.1f}만",
            xy=(center_x, center_y),
            fontsize=11,
            fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8, edgecolor="#D97706"),
            ha="center"
        )
    ax.set_title("정부세종청사 생활권 오피스텔 지리적 공간 분포 및 총 주거비용", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("경도 (Longitude)")
    ax.set_ylabel("위도 (Latitude)")
    ax.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()
    p10 = img_dir / "10_sejong_officetel_geo_bubble.png"
    plt.savefig(p10, bbox_inches="tight")
    plt.close()
    print(f"[+] 차트 10 생성: {p10.name}")

    return keywords


def export_summary_json(df, keywords, out_path):
    """대시보드 실시간 렌더링용 집계 요약 JSON 생성"""
    rent_df = df[df["sales_type"] == "월세"]
    
    summary = {
        "metadata": {
            "title": "세종특별자치시 정부청사 생활권(어진동·나성동·도담동) 오피스텔 실매물 분석",
            "total_items": len(df),
            "total_rent_items": len(rent_df),
            "generated_at": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        "kpi": {
            "avg_deposit": round(float(df["deposit_manwon"].mean()), 1),
            "avg_rent": round(float(rent_df["rent_manwon"].mean()), 1) if len(rent_df) > 0 else 0,
            "avg_manage_cost": round(float(df["manage_cost_won"].mean()), 0),
            "avg_total_cost": round(float(rent_df["total_monthly_cost_manwon"].mean()), 1) if len(rent_df) > 0 else 0,
            "avg_pyeong": round(float(df["exclusive_area_pyeong"].mean()), 1),
            "avg_pyeong_rent": round(float(rent_df["unit_rent_per_pyeong"].mean()), 2) if len(rent_df) > 0 else 0
        },
        "dong_stats": {
            dong: {
                "count": int(sub.shape[0]),
                "avg_rent": round(float(sub[sub["sales_type"] == "월세"]["rent_manwon"].mean()), 1) if len(sub[sub["sales_type"] == "월세"]) > 0 else 0,
                "avg_total_cost": round(float(sub[sub["sales_type"] == "월세"]["total_monthly_cost_manwon"].mean()), 1) if len(sub[sub["sales_type"] == "월세"]) > 0 else 0,
                "avg_pyeong": round(float(sub["exclusive_area_pyeong"].mean()), 1),
                "avg_pyeong_rent": round(float(sub[sub["sales_type"] == "월세"]["unit_rent_per_pyeong"].mean()), 2) if len(sub[sub["sales_type"] == "월세"]) > 0 else 0
            }
            for dong, sub in df.groupby("dong")
        },
        "sales_type_counts": df["sales_type"].value_counts().to_dict(),
        "top_keywords": [{"keyword": k[0], "score": round(float(k[1]), 4)} for k in keywords[:20]],
        "items": df.to_dict(orient="records")
    }

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(f"[+] 대시보드 요약 JSON 생성 완료: {out_path.name}")


def main():
    df, csv_path = load_data()
    print_basic_inspection(df)

    img_dir = Path(__file__).resolve().parent.parent / "images"
    keywords = generate_charts(df, img_dir)

    summary_path = Path(__file__).resolve().parent.parent / "data" / "summary_data.json"
    export_summary_json(df, keywords, summary_path)


if __name__ == "__main__":
    main()
