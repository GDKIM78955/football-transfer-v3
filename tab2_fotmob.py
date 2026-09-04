import streamlit as st
import pandas as pd

def render_tab2():
    st.subheader("📱 FotMob 시즌 성적 입력 및 이적 예측 프로젝션 존")
    st.info("💡 직전 시즌 스탯을 기반으로 신규 팀에서의 예상 성적(프로젝션)과 비교 시각화 차트를 제공합니다.")

    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### 📥 직전 시즌 실제 기록 입력")
        p_matches = st.number_input("출전 경기", 0, 60, value=34, key="v3_f_matches")
        p_starts = st.number_input("선발 출전", 0, 60, value=30, key="v3_f_starts")
        p_mins = st.number_input("출전 시간(분)", 0, 5400, value=2800, key="v3_f_mins")
        p_goals = st.number_input("득점 (Goals)", 0.0, 50.0, value=12.0, step=1.0, key="v3_f_goals")
        p_xg = st.number_input("기대 득점 (xG)", 0.0, 50.0, value=10.5, step=0.5, key="v3_f_xg")
        p_assists = st.number_input("도움 (Assists)", 0.0, 40.0, value=7.0, step=1.0, key="v3_f_assists")
        p_xa = st.number_input("기대 도움 (xA)", 0.0, 40.0, value=6.2, step=0.5, key="v3_f_xa")
        p_rating = st.number_input("FotMob 시즌 평균 평점", 0.0, 10.0, value=7.42, step=0.01, key="v3_f_rating")

    # 프로젝션 자동 산출 로직
    proj_mins_val = 3000
    coef = proj_mins_val / max(p_mins, 500)
    proj_g = round(p_goals * coef * 0.95, 2)
    proj_xg_val = round(p_xg * coef * 0.95, 2)
    proj_a = round(p_assists * coef * 0.95, 2)
    proj_xa_val = round(p_xa * coef * 0.95, 2)
    proj_rt = round(p_rating * 0.98, 2)

    with col2:
        st.markdown("##### 📈 이적 후 예상 프로젝션 (3000분 기준 환산)")
        
        m1, m2 = st.columns(2)
        with m1:
            st.metric("예상 출전 시간", f"{proj_mins_val:,}분")
            st.metric("예상 득점 (G)", f"{proj_g}골", delta=f"xG {proj_xg_val}")
        with m2:
            st.metric("예상 평점", f"{proj_rt}")
            st.metric("예상 도움 (A)", f"{proj_a}개", delta=f"xA {proj_xa_val}")

        st.markdown("---")
        st.markdown("##### 📊 공격 포인트 효율성 비교 차트")
        
        chart_data = pd.DataFrame(
            {
                "지표": ["득점 (G)", "기대득점 (xG)", "도움 (A)", "기대도움 (xA)"],
                "직전 시즌": [p_goals, p_xg, p_assists, p_xa],
                "이적 후 프로젝션": [proj_g, proj_xg_val, proj_a, proj_xa_val]
            }
        ).set_index("지표")
        
        st.bar_chart(chart_data)
