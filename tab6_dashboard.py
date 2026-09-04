import streamlit as st

def render_tab6(history_df):
    st.subheader("🏆 구단별 결산, 파워 랭킹 & 데이터 관리실")
    if history_df.empty:
        st.warning("⚠️ 관리할 데이터가 없습니다.")
    else:
        st.dataframe(history_df, use_container_width=True)
