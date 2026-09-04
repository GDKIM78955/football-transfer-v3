import streamlit as st
import pandas as pd

def render_tab4(val_df):
    st.subheader("🎯 이적 첫 시즌 실제 성적 & 사후 검증 존 ([검증데이터] 2번 시트 연동)")
    if val_df.empty:
        st.warning("⚠️ 2번 시트(검증데이터)를 불러오지 못했거나 데이터가 비어 있습니다.")
    else:
        st.info("💡 선수의 사전 평가치와 이적 후 첫 시즌 실제 퍼포먼스를 교차 검증하는 공간입니다.")
        st.dataframe(val_df, use_container_width=True)
