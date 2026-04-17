import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sales Dashboard", layout="wide")

# 1) 사이드바 필터 ── 여기에 날짜 선택, 지역 필터 추가
with st.sidebar:
    st.title(" 필터")
    # TODO: st.date_input() 으로 날짜 범위 추가
    # TODO: st.multiselect() 로 지역 필터 추가

# 2) KPI 카드 4개 ── st.columns(4) 사용
col1, col2, col3, col4 = st.columns(4)
# TODO: 각 열에 st.metric() 배치

# 3) 탭 3개 ── 매출 분석 / 제품 현황 / 지역 현황
tab1, tab2, tab3 = st.tabs([" 매출 분석", " 제품 현황", " 지역 현황"])

# 4) 원본 데이터 expander
with st.expander(" 원본 데이터 보기", expanded=False):
    st.write("데이터를 여기에 표시하세요")


@st.cache_data
def load_data():
    df = pd.read_csv("sales_data.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df


df = load_data()

# 사이드바 필터
with st.sidebar:
    st.title(" 필터")
    selected_regions = st.multiselect(
        "지역", df["region"].unique(), default=df["region"].unique()
    )
    date_range = st.date_input("기간", value=[df["date"].min(), df["date"].max()])

# 필터 적용
df_f = df[
    df["region"].isin(selected_regions)
    & (df["date"] >= pd.Timestamp(date_range[0]))
    & (df["date"] <= pd.Timestamp(date_range[1]))
]

# KPI + 차트 — df_f 를 사용하도록 수정
col1, col2 = st.columns(2)
col1.metric("필터 적용 후 총 매출", f'₩{df_f["sales"].sum():,}')
col2.metric("주문 건수", f"{len(df_f):,}건")
