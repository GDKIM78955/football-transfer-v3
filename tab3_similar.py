import streamlit as st

def render_tab3(history_df):
    st.subheader("🔍 과거 유사 이적 사례 비교 (Top 5 / Top 10)")
    if history_df.empty:
        st.warning("⚠️ 시트에 저장된 기존 데이터가 없습니다.")
    else:
        st.dataframe(history_df, use_container_width=True)
