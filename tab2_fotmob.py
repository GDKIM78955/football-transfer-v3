import streamlit as st

def render_tab2():
    st.subheader("📱 FotMob 시즌 성적 입력 및 이적 예측 프로젝션 존")
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.number_input("출전 경기", 0, 60, value=1, key="v3_f_matches")
    with c2: st.number_input("선발 출전", 0, 60, value=0, key="v3_f_starts")
    with c3: st.number_input("출전 시간(분)", 0, 4500, value=90, key="v3_f_mins")
    with c4: st.number_input("FotMob 평점", 0.0, 10.0, value=6.5, key="v3_f_rating")
    st.info("💡 2번 탭의 성적 데이터는 저장/수정 시 전송됩니다.")
