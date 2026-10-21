"""[20년차 데이터 분석가 EDA 템플릿] Universal EDA Template

수집된 CSV 데이터를 기반으로 정밀 탐색적 데이터 분석을 수행하고,
10종 이상의 고해상도(DPI 150) 시각화 차트와 Scikit-Learn TF-IDF 텍스트 분석을 자동 생성합니다.
한글 폰트 깨짐 방지(`koreanize_matplotlib`) 및 전역 스타일 금지 원칙을 엄격히 준수합니다.
"""

import os
from pathlib import Path

import koreanize_matplotlib  # 한글 폰트 깨짐 방지 필수 임포트
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer


class UniversalEDA:
    def __init__(self, csv_path: str, output_img_dir: str = "images"):
        self.csv_path = Path(csv_path)
        self.output_img_dir = Path(output_img_dir)
        self.output_img_dir.mkdir(parents=True, exist_ok=True)
        
        # 데이터 로드 (BOM UTF-8 자동 처리)
        self.df = pd.read_csv(self.csv_path, encoding="utf-8-sig")
        print(f"📊 [{self.csv_path.name}] 데이터셋 로드 완료: {self.df.shape[0]:,}행, {self.df.shape[1]}열")

    def print_overview(self):
        """1단계: 데이터 기본 구조 및 결측치 전수 점검"""
        print("\n" + "=" * 60)
        print("📌 [1. 기본 데이터 파악 (Overview)]")
        print("=" * 60)
        print("\n[상위 5개 행]")
        print(self.df.head())
        print("\n[하위 5개 행]")
        print(self.df.tail())
        
        print("\n[데이터 구조 및 결측치 정보]")
        print(self.df.info())
        
        print("\n[중복 행 수]:", self.df.duplicated().sum(), "건")
        
        print("\n[수치형 변수 기술통계]")
        print(self.df.describe())
        
        cat_cols = self.df.select_dtypes(include=["object"]).columns
        if len(cat_cols) > 0:
            print("\n[범주형 변수 기술통계]")
            print(self.df.describe(include=["object"]))

    def run_tfidf_analysis(self, text_column: str = "title", top_n: int = 30) -> pd.DataFrame:
        """2단계: Scikit-learn TF-IDF 기반 핵심 키워드 가중치 분석"""
        print("\n" + "=" * 60)
        print(f"🔤 [2. 텍스트 마이닝: TF-IDF 상위 {top_n} 키워드 분석]")
        print("=" * 60)

        texts = self.df[text_column].dropna().astype(str).tolist()

        # 한국어 2글자 이상 단어 매칭 및 불용어 제거
        vectorizer = TfidfVectorizer(
            token_pattern=r"(?u)\b\w{2,}\b",
            max_features=500,
            stop_words=["있는", "하는", "위한", "대한", "통한", "따른", "따라", "부터"],
        )

        tfidf_matrix = vectorizer.fit_transform(texts)
        scores = np.asarray(tfidf_matrix.mean(axis=0)).ravel()
        feature_names = np.array(vectorizer.get_feature_names_out())

        top_indices = scores.argsort()[::-1][:top_n]
        top_df = pd.DataFrame({
            "keyword": feature_names[top_indices],
            "tfidf_score": scores[top_indices]
        })

        print(top_df.to_string(index=False))
        return top_df

    def generate_all_visualizations(self, text_column: str = "title"):
        """3단계: 10종 고해상도 시각화 차트 자동 생성 (DPI 150)
        
        * 주의: Seaborn 전역 스타일(sns.set_theme 등)은 적용하지 않습니다.
        """
        print("\n" + "=" * 60)
        print("📈 [3. 10종 핵심 시각화 차트 생성 시작]")
        print("=" * 60)

        df = self.df.copy()
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()

        # 1. 수치형 변수 히스토그램 및 KDE (예: 가격/할인가 분포)
        primary_num = num_cols[1] if len(num_cols) > 1 else num_cols[0]
        fig, ax = plt.subplots(figsize=(10, 5), dpi=150)
        sns.histplot(df[primary_num], kde=True, color="#3B82F6", ax=ax)
        ax.set_title(f"1. {primary_num} 데이터 분포 및 확률밀도 (KDE)", fontsize=14, fontweight="bold")
        ax.set_xlabel(primary_num)
        ax.set_ylabel("빈도수")
        plt.tight_layout()
        plt.savefig(self.output_img_dir / "01_distribution_histogram.png")
        plt.close()
        print(" ✅ 1/10 생성: 01_distribution_histogram.png")

        # 2. 범주형 상위 항목 빈도 막대그래프 (예: 카테고리/출판사/브랜드)
        cat_cols = df.select_dtypes(include=["object"]).columns.tolist()
        primary_cat = cat_cols[0] if cat_cols else None
        if primary_cat:
            top_cats = df[primary_cat].value_counts().head(10)
            fig, ax = plt.subplots(figsize=(10, 5), dpi=150)
            sns.barplot(x=top_cats.values, y=top_cats.index, palette="Blues_r", ax=ax)
            ax.set_title(f"2. 주요 {primary_cat} 상위 10개 점유 빈도", fontsize=14, fontweight="bold")
            ax.set_xlabel("건수")
            plt.tight_layout()
            plt.savefig(self.output_img_dir / "02_top_categories_bar.png")
            plt.close()
            print(" ✅ 2/10 생성: 02_top_categories_bar.png")

        # 3. 박스플롯을 통한 이상치 및 사분위수 분석
        fig, ax = plt.subplots(figsize=(9, 4), dpi=150)
        sns.boxplot(x=df[primary_num], color="#60A5FA", ax=ax)
        ax.set_title(f"3. {primary_num} 사분위수 및 이상치(Outlier) 점검", fontsize=14, fontweight="bold")
        plt.tight_layout()
        plt.savefig(self.output_img_dir / "03_box_plot_outliers.png")
        plt.close()
        print(" ✅ 3/10 생성: 03_box_plot_outliers.png")

        # 4. TF-IDF 상위 20대 핵심 키워드 가중치 수평 막대그래프
        if text_column in df.columns:
            top_keywords = self.run_tfidf_analysis(text_column=text_column, top_n=20)
            fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
            sns.barplot(data=top_keywords, x="tfidf_score", y="keyword", palette="crest", ax=ax)
            ax.set_title("4. 텍스트 마이닝 TF-IDF 상위 20대 핵심 키워드 가중치", fontsize=14, fontweight="bold")
            ax.set_xlabel("TF-IDF 평균 점수")
            plt.tight_layout()
            plt.savefig(self.output_img_dir / "04_tfidf_top20_keywords.png")
            plt.close()
            print(" ✅ 4/10 생성: 04_tfidf_top20_keywords.png")

        # 5. 수치형 상관계수 히트맵
        if len(num_cols) >= 2:
            corr = df[num_cols].corr()
            fig, ax = plt.subplots(figsize=(8, 6), dpi=150)
            sns.heatmap(corr, annot=True, cmap="Blues", fmt=".2f", linewidths=0.5, ax=ax)
            ax.set_title("5. 주요 수치형 변수 간 상관관계 히트맵", fontsize=14, fontweight="bold")
            plt.tight_layout()
            plt.savefig(self.output_img_dir / "05_correlation_heatmap.png")
            plt.close()
            print(" ✅ 5/10 생성: 05_correlation_heatmap.png")

        # 6. 이변량 산점도 및 추세선 (예: 순위 vs 가격 또는 리뷰 수)
        if len(num_cols) >= 2:
            x_col = num_cols[0]
            y_col = num_cols[1]
            fig, ax = plt.subplots(figsize=(9, 5), dpi=150)
            sns.regplot(data=df, x=x_col, y=y_col, scatter_kws={"alpha": 0.5, "color": "#2563EB"}, line_kws={"color": "#DC2626"}, ax=ax)
            ax.set_title(f"6. {x_col}와 {y_col} 간의 선형 회귀 추세 분석", fontsize=14, fontweight="bold")
            plt.tight_layout()
            plt.savefig(self.output_img_dir / "06_bivariate_scatter.png")
            plt.close()
            print(" ✅ 6/10 생성: 06_bivariate_scatter.png")

        # 7. 범주별 수치 집계 바이올린 플롯 (또는 스트립 플롯)
        if primary_cat and len(df[primary_cat].value_counts()) >= 2:
            top_5_cats = df[primary_cat].value_counts().head(5).index
            filtered_df = df[df[primary_cat].isin(top_5_cats)]
            fig, ax = plt.subplots(figsize=(10, 5), dpi=150)
            sns.violinplot(data=filtered_df, x=primary_cat, y=primary_num, palette="pastel", ax=ax)
            ax.set_title(f"7. 주요 5대 {primary_cat}별 {primary_num} 밀도 비교 (Violin Plot)", fontsize=14, fontweight="bold")
            plt.xticks(rotation=15)
            plt.tight_layout()
            plt.savefig(self.output_img_dir / "07_category_violin.png")
            plt.close()
            print(" ✅ 7/10 생성: 07_category_violin.png")

        # 8. 파이 / 도넛 차트 (상위 그룹 비중)
        if primary_cat:
            pie_data = df[primary_cat].value_counts().head(5)
            fig, ax = plt.subplots(figsize=(7, 7), dpi=150)
            ax.pie(pie_data.values, labels=pie_data.index, autopct="%1.1f%%", startangle=140, colors=sns.color_palette("Set3"))
            centre_circle = plt.Circle((0, 0), 0.70, fc="white")
            fig.gca().add_artist(centre_circle)
            ax.set_title(f"8. 상위 5대 {primary_cat} 점유율 도넛 차트", fontsize=14, fontweight="bold")
            plt.tight_layout()
            plt.savefig(self.output_img_dir / "08_market_share_donut.png")
            plt.close()
            print(" ✅ 8/10 생성: 08_market_share_donut.png")

        # 9. 순위 구간별 집계 바 차트 (예: 1~100위, 101~200위 등)
        if "rank" in df.columns:
            df["rank_group"] = pd.cut(df["rank"], bins=[0, 100, 200, 300, 400, 500, 1000], labels=["Top 100", "101-200", "201-300", "301-400", "401-500", "500+"])
            group_mean = df.groupby("rank_group", observed=False)[primary_num].mean()
            fig, ax = plt.subplots(figsize=(9, 5), dpi=150)
            group_mean.plot(kind="bar", color="#6366F1", ax=ax)
            ax.set_title(f"9. 순위 구간별 {primary_num} 평균 비교", fontsize=14, fontweight="bold")
            ax.set_ylabel(f"평균 {primary_num}")
            plt.xticks(rotation=0)
            plt.tight_layout()
            plt.savefig(self.output_img_dir / "09_rank_group_comparison.png")
            plt.close()
            print(" ✅ 9/10 생성: 09_rank_group_comparison.png")

        # 10. 누적 분포 함수 (ECDF)
        fig, ax = plt.subplots(figsize=(9, 5), dpi=150)
        sns.ecdfplot(data=df, x=primary_num, color="#059669", ax=ax)
        ax.set_title(f"10. {primary_num} 경험적 누적 분포 함수 (ECDF)", fontsize=14, fontweight="bold")
        ax.set_ylabel("누적 확률")
        ax.grid(True, linestyle="--", alpha=0.5)
        plt.tight_layout()
        plt.savefig(self.output_img_dir / "10_ecdf_cumulative_distribution.png")
        plt.close()
        print(" ✅ 10/10 생성: 10_ecdf_cumulative_distribution.png")

        print("\n🎉 총 10종 고해상도 시각화 차트 생성이 완료되었습니다!")


def main():
    # 사용 예시
    # eda = UniversalEDA("data/example.csv", "images")
    # eda.print_overview()
    # eda.generate_all_visualizations(text_column="title")
    pass


if __name__ == "__main__":
    main()
