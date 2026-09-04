import streamlit as st
import pandas as pd

def render_tab6(history_df):
    st.subheader("🏆 구단별 결산, 파워 랭킹 & 데이터 관리실")
    if history_df.empty:
        st.warning("⚠️ 관리할 데이터가 없습니다.")
    else:
        st.info("💡 구단별 총 이적료 지출/수입 정산 및 전체 데이터베이스 관리 룸입니다.")
        
        if "이적팀명" in history_df.columns and "실제이적료(만€)" in history_df.columns:
            club_summary = history_df.groupby("이적팀명")["실제이적료(만€)"].sum().reset_index()
            club_summary.columns = ["구단명", "총 이적료 지출 합계 (만€)"]
            club_summary = club_summary.sort_values(by="총 이적료 지출 합계 (만€)", ascending=False)
            
            st.markdown("##### 📊 구단별 총 투자 규모 랭킹")
            st.dataframe(club_summary, use_container_width=True)
            st.markdown("---")
            
        st.markdown("##### 📂 전체 이적 데이터 원본 관리 룸")
        st.dataframe(history_df, use_container_width=True)
