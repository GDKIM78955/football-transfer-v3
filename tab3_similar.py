import streamlit as st
import pandas as pd

def render_tab3(history_df):
    st.subheader("🔍 과거 유사 이적 사례 비교 (Top 5 / Top 10)")
    if history_df.empty:
        st.warning("⚠️ 시트에 저장된 기존 데이터가 없습니다.")
    else:
        st.info("💡 과거 이적 데이터베이스에서 포지션, 연령대, 이적료 규모가 유사한 선수를 필터링하여 비교합니다.")
        
        # 필터 옵션 추가
        c1, c2 = st.columns(2)
        with c1:
            positions = ["전체"] + list(history_df["포지션"].dropna().unique()) if "포지션" in history_df.columns else ["전체"]
            sel_pos = st.selectbox("포지션 필터", positions, key="sim_pos")
        with c2:
            max_fee = int(history_df["실제이적료(만€)"].max()) if "실제이적료(만€)" in history_df.columns and not history_df["실제이적료(만€)"].empty else 20000
            fee_range = st.slider("실제 이적료 범위 (만 €)", 0, max_fee, (0, max_fee), key="sim_fee")

        filtered_df = history_df.copy()
        if sel_pos != "전체" and "포지션" in filtered_df.columns:
            filtered_df = filtered_df[filtered_df["포지션"] == sel_pos]
        if "실제이적료(만€)" in filtered_df.columns:
            filtered_df = filtered_df[(filtered_df["실제이적료(만€)"] >= fee_range[0]) & (filtered_df["실제이적료(만€)"] <= fee_range[1])]

        st.markdown(f"**검색 결과: 총 {len(filtered_df)}건의 유사 사례 발견**")
        st.dataframe(filtered_df, use_container_width=True)
