import streamlit as st
import pandas as pd

# 1. 분할된 탭 모듈 및 유틸 임포트
from utils import SPREADSHEET_ID
from tab1_valuation import render_tab1
from tab2_fotmob import render_tab2
from tab3_similar import render_tab3
from tab4_validation import render_tab4
from tab5_benchmark import render_tab5
from tab6_dashboard import render_tab6

# 2. 페이지 설정
st.set_page_config(
    page_title="프로페셔널 축구 이적시장 분석 시스템 v3",
    page_icon="⚽",
    layout="wide"
)

# 3. 데이터 로드 함수 (구글 시트 연동)
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

# 4. 세션 메시지 출력 관리
if "v3_msg" not in st.session_state:
    st.session_state["v3_msg"] = None

if st.session_state["v3_msg"]:
    st.success(st.session_state["v3_msg"])
    st.session_state["v3_msg"] = None

st.title("⚽ 프로페셔널 축구 이적시장 분석 시스템 v3 (Modular)")

# 5. 6개 탭 구조 선언 및 각 모듈 연결
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "💰 적정 이적료 평가", 
    "📱 FotMob 시즌 성적 & 이적 예측",
    "🔍 과거 유사 이적 사례 비교",
    "🎯 이적 첫 시즌 실제 성적 & 사후 검증",
    "👥 다각도 벤치마크",
    "🏆 종합 결산 & 데이터룸"
])

with tab1:
    render_tab1(history_df)

with tab2:
    render_tab2()

with tab3:
    render_tab3(history_df)

with tab4:
    render_tab4(val_df)

with tab5:
    render_tab5(history_df)

with tab6:
    render_tab6(history_df)
