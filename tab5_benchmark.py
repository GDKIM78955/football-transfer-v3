import streamlit as st
import pandas as pd

def render_tab5(history_df):
    st.subheader("👥 신규 이적생 vs 과거 선수 다각도 벤치마크 교차 비교")
    if history_df.empty:
        st.warning("⚠️ 비교할 데이터가 부족합니다.")
    else:
        st.info("💡 데이터베이스 내 두 선수를 선택하여 가치 산정 지표와 스탯을 나란히 비교합니다.")
        players = list(history_df["선수명"].dropna().unique()) if "선수명" in history_df.columns else []
        if len(players) >= 2:
            col1, col2 = st.columns(2)
            with col1: p1 = st.selectbox("비교 대상 A", players, index=0, key="bench_p1")
            with col2: p2 = st.selectbox("비교 대상 B", players, index=1, key="bench_p2")
            
            df_p1 = history_df[history_df["선수명"] == p1]
            df_p2 = history_df[history_df["선수명"] == p2]
            
            comparison_df = pd.concat([df_p1, df_p2])
            st.dataframe(comparison_df, use_container_width=True)
        else:
            st.dataframe(history_df, use_container_width=True)
