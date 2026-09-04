import streamlit as st
import pandas as pd
from utils import LEAGUE_WEIGHTS, CLUB_TIERS, get_positional_age_weight

# 1. 페이지 설정
st.set_page_config(
    page_title="프로페셔널 축구 이적시장 분석 시스템 v3",
    page_icon="⚽",
    layout="wide"
)

# 2. 데이터 로드 설정 (구글 시트 연동 준비)
SPREADSHEET_ID = "16CeAQp1-xqc-mhtvlP0vLlQu5k1pg8DW5A-m29WCFdw"

@st.cache_data(ttl=0)
def fetch_sheet_history():
    try:
        csv_url = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/export?format=csv&gid=0"
        df = pd.read_csv(csv_url)
        if not df.empty:
            return df
    except Exception:
        pass
    return pd.DataFrame()

@st.cache_data(ttl=0)
def fetch_validation_data():
    try:
        val_url = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/export?format=csv&gid=15389686"
        df = pd.read_csv(val_url)
        if not df.empty:
            return df
    except Exception:
        pass
    return pd.DataFrame()

history_df = fetch_sheet_history()
val_df = fetch_validation_data()

st.title("⚽ 프로페셔널 축구 이적시장 분석 시스템 v3")

# 3. 6개 탭 구조 선언
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "💰 적정 이적료 평가", 
    "📱 FotMob 시즌 성적 & 이적 예측",
    "🔍 과거 유사 이적 사례 비교",
    "🎯 이적 첫 시즌 실제 성적 & 사후 검증",
    "👥 다각도 벤치마크",
    "🏆 종합 결산 & 데이터룸"
])

# --- [TAB 1] 적정 이적료 평가 (기본 뼈대) ---
with tab1:
    st.subheader("💰 12대 가중치 기반 적정 이적료 산출 및 관리 존")
    st.info("💡 utils.py와 정상적으로 연동되었습니다. 다음 단계에서 입력 폼과 계산 엔진을 결합합니다.")
    
    # 간단한 테스트 입력으로 연동 확인
    c1, c2 = st.columns(2)
    with c1:
        test_age = st.number_input("테스트 나이", 15, 45, value=25)
        test_league = st.selectbox("테스트 리그", list(LEAGUE_WEIGHTS.keys()))
    with c2:
        st.write("선택된 리그 가중치:", LEAGUE_WEIGHTS[test_league])

# --- [TAB 2] FotMob 성적 입력 및 예측 ---
with tab2:
    st.subheader("📱 FotMob 시즌 성적 입력 및 이적 예측 프로젝션 존")

# --- [TAB 3] 과거 유사 이적 사례 비교 ---
with tab3:
    st.subheader("🔍 과거 유사 이적 사례 비교")
    if not history_df.empty:
        st.dataframe(history_df, use_container_width=True)
    else:
        st.warning("시트 데이터를 불러오는 중이거나 데이터가 없습니다.")

# --- [TAB 4] 이적 첫 시즌 실제 성적 & 사후 검증 ---
with tab4:
    st.subheader("🎯 이적 첫 시즌 실제 성적 & 사후 검증 존")
    if not val_df.empty:
        st.dataframe(val_df, use_container_width=True)
    else:
        st.warning("검증 데이터를 불러오는 중이거나 데이터가 없습니다.")

# --- [TAB 5] 벤치마크 교차 비교 ---
with tab5:
    st.subheader("👥 신규 이적생 vs 과거 선수 다각도 벤치마크 교차 비교")

# --- [TAB 6] 종합 결산 & 데이터룸 ---
with tab6:
    st.subheader("🏆 구단별 결산, 파워 랭킹 & 데이터 관리실")
    if not history_df.empty:
        st.dataframe(history_df, use_container_width=True)
