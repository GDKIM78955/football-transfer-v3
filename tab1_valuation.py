import streamlit as st
import pandas as pd
import requests
import json
from datetime import datetime
from utils import (
    LEAGUE_WEIGHTS, CLUB_TIERS, CONTRACT_WEIGHTS, POSITION_WEIGHTS,
    VERSATILITY_WEIGHTS, REGISTRATION_WEIGHTS, TRANSFER_TYPE_WEIGHTS,
    BIG_STAGE_WEIGHTS, INJURY_WEIGHTS, URGENCY_WEIGHTS,
    get_positional_age_weight, get_exact_val
)

GOOGLE_SHEET_WEBAPP_URL = "https://script.google.com/macros/s/AKfycbwUX4diDBw2jD8WufrSa_0PejibYm7tIfyf1ia7O-QTfj1Ae6SQb3bZZ9pmNvDUAT6C/exec"

def render_tab1(history_df):
    c_mode1, _ = st.columns([1, 1])
    with c_mode1:
        edit_mode = st.toggle("✏️ 기존 저장된 선수 불러와서 수정 모드", value=False, key="v3_toggle")

    if edit_mode:
        st.markdown("##### 🔍 불러올 선수 선택")
        if history_df.empty or "이적시즌" not in history_df.columns or "선수명" not in history_df.columns:
            st.warning("⚠️ 시트에 저장된 기존 데이터가 없습니다.")
        else:
            c_ld1, c_ld2, c_ld3 = st.columns([1, 2, 1])
            with c_ld1:
                e_seasons = list(history_df["이적시즌"].dropna().unique())
                sel_season = st.selectbox("시즌 선택", e_seasons, key="v3_sel_season")
            
            season_df = history_df[history_df["이적시즌"] == sel_season]
            e_players = list(season_df["선수명"].dropna().unique())
            
            with c_ld2:
                sel_player = st.selectbox("선수 선택", e_players, key="v3_sel_player") if e_players else None

            with c_ld3:
                st.write("")
                st.write("")
                if st.button("📥 데이터 불러오기", type="primary", use_container_width=True, key="v3_load_btn"):
                    if sel_player:
                        matched = season_df[season_df["선수명"] == sel_player].iloc[-1]
                        idx_list = season_df.index[season_df["선수명"] == sel_player].tolist()
                        
                        st.session_state["v3_edit_row"] = idx_list[-1] + 2 if idx_list else None

                        def get_idx(val, options):
                            for i, opt in enumerate(options):
                                if str(val).strip() in opt:
                                    return i
                            return 0

                        raw_notes = str(get_exact_val(matched, "스카우팅메모", ""))
                        clean_notes = raw_notes.split(" | [영입")[0].split(" | [방출")[0].strip()

                        st.session_state["v3_name"] = str(get_exact_val(matched, "선수명", ""))
                        st.session_state["v3_nat"] = str(get_exact_val(matched, "국적", ""))
                        st.session_state["v3_age"] = int(get_exact_val(matched, "만나이", 28))
                        st.session_state["v3_from_t"] = str(get_exact_val(matched, "원소속팀명", ""))
                        st.session_state["v3_to_t"] = str(get_exact_val(matched, "이적팀명", ""))
                        st.session_state["v3_tm"] = int(get_exact_val(matched, "TM시장가치(만€)", 4500))
                        st.session_state["v3_fee"] = int(get_exact_val(matched, "실제이적료(만€)", 0))
                        st.session_state["v3_wage"] = float(get_exact_val(matched, "주급(만€)", 0.0))
                        st.session_state["v3_notes"] = clean_notes

                        st.session_state["v3_season"] = get_idx(get_exact_val(matched, "이적시즌", "26/27"), ["26/27 여름 (Summer)", "26/27 겨울 (Winter)", "기타"])
                        st.session_state["v3_ttype"] = get_idx(get_exact_val(matched, "이적형태", ""), list(TRANSFER_TYPE_WEIGHTS.keys()))
                        st.session_state["v3_pos"] = get_idx(get_exact_val(matched, "포지션", ""), list(POSITION_WEIGHTS.keys()))
                        st.session_state["v3_from_l"] = get_idx(get_exact_val(matched, "원소속리그", ""), list(LEAGUE_WEIGHTS.keys()))
                        st.session_state["v3_to_l"] = get_idx(get_exact_val(matched, "이적팀리그", ""), list(LEAGUE_WEIGHTS.keys()))
                        st.session_state["v3_tier"] = get_idx(get_exact_val(matched, "영입구단티어", ""), list(CLUB_TIERS.keys()))

                        st.session_state["v3_msg"] = f"✅ '{sel_player}' 데이터 로드 완료! (수정 타겟 행: {st.session_state['v3_edit_row']})"
                        st.rerun()
    else:
        st.session_state["v3_edit_row"] = None

    t_row = st.session_state.get("v3_edit_row")
    if edit_mode and t_row:
        st.info(f"📌 [수정 모드 활성화] 현재 대상 구글 시트 행: **{t_row}번째 행**")

    st.markdown("---")
    trade_type_choice = st.radio("거래 유형 구분", ["🔵 영입 (IN)", "🔴 방출 / 판매 (OUT)"], index=0, horizontal=True, key="v3_trade_type")
    is_out = "방출" in trade_type_choice

    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader(f"📝 {'[수정 모드] ' if (edit_mode and t_row) else ''}{'방출(OUT)' if is_out else '영입(IN)'} 선수 & 계약 정보")
        
        cs1, cs2 = st.columns(2)
        seasons = ["26/27 여름 (Summer)", "26/27 겨울 (Winter)", "기타"]
        with cs1: season_val = st.selectbox("이적 시즌 / 시장", seasons, key="v3_season")
        
        ttypes = list(TRANSFER_TYPE_WEIGHTS.keys())
        with cs2: transfer_type = st.selectbox("이적 형태 & 계약 조항", ttypes, key="v3_ttype")

        cn1, cn2, cn3 = st.columns([2, 1, 1])
        with cn1: p_name = st.text_input("선수 이름", key="v3_name")
        with cn2: p_nat = st.text_input("국적", key="v3_nat")
        with cn3: p_age = st.number_input("만 나이", 15, 45, key="v3_age")

        ct1, ct2, ct3 = st.columns(3)
        with ct1: p_from_t = st.text_input("원소속팀명", key="v3_from_t")
        with ct2: p_to_t = st.text_input("이적팀명", key="v3_to_t")
        
        leagues = list(LEAGUE_WEIGHTS.keys())
        with ct3: p_to_l = st.selectbox("이적팀 리그", leagues, key="v3_to_l")

        positions = list(POSITION_WEIGHTS.keys())
        pc1, pc2 = st.columns(2)
        with pc1: main_pos = st.selectbox("주 포지션", positions, key="v3_pos")
        with pc2: versatility = st.selectbox("멀티 포지션 소화 능력", list(VERSATILITY_WEIGHTS.keys()), key="v3_vers")

        cr1, cr2 = st.columns(2)
        with cr1: reg_status = st.selectbox("스쿼드 등록 / HG 쿼터", list(REGISTRATION_WEIGHTS.keys()), key="v3_reg")
        with cr2: big_stage = st.selectbox("UCL / 빅매치 검증도", list(BIG_STAGE_WEIGHTS.keys()), key="v3_stage")

        ci1, ci2 = st.columns(2)
        with ci1: injury_status = st.selectbox("부상 내구성", list(INJURY_WEIGHTS.keys()), key="v3_inj")
        with ci2: urgency_status = st.selectbox("구단 절박성", list(URGENCY_WEIGHTS.keys()), key="v3_urg")

        selling_league = st.selectbox("보내는 리그 (원소속 리그)", leagues, key="v3_from_l")
        
        tiers = list(CLUB_TIERS.keys())
        buying_tier = st.selectbox("영입구단티어", tiers, key="v3_tier")
        rem_contract = st.selectbox("이적 당시 잔여 계약 기간", list(CONTRACT_WEIGHTS.keys()), key="v3_contract")

        st.markdown("---")
        tm_val = st.number_input("TM시장가치(만€)", 0, step=50, key="v3_tm")
        actual_fee = st.number_input("실제이적료(만€)", 0, step=50, key="v3_fee")
        weekly_wage = st.number_input("주급(만€)", 0.0, step=0.5, key="v3_wage")
        p_notes = st.text_area("스카우팅메모", key="v3_notes")

    # 가중치 산식 계산
    lw = LEAGUE_WEIGHTS[selling_league]
    aw = get_positional_age_weight(p_age, main_pos)
    cw = CLUB_TIERS[buying_tier]
    conw = CONTRACT_WEIGHTS[rem_contract]
    pw = POSITION_WEIGHTS[main_pos]
    vw = VERSATILITY_WEIGHTS[versatility]
    rw = REGISTRATION_WEIGHTS[reg_status]
    ttw = TRANSFER_TYPE_WEIGHTS[transfer_type]
    sw = BIG_STAGE_WEIGHTS[big_stage]
    iw = INJURY_WEIGHTS[injury_status]
    uw = URGENCY_WEIGHTS[urgency_status]

    is_win = "겨울" in season_val
    s_factor = 1.10 if is_win else 1.00

    base_val = tm_val * lw * aw * cw * conw * pw * vw * rw * 1.01 * ttw * sw * iw * uw
    fair_val = base_val * s_factor
    diff_val = actual_fee - fair_val
    over_pct = (diff_val / fair_val) * 100 if fair_val > 0 else 0.0
    stat_lbl = "⚖️ 적정가 (Fair Deal)" if abs(diff_val) <= (fair_val * 0.05) else (f"⚠️ 오버페이 (+{over_pct:.1f}%)" if diff_val > 0 else f"💎 혜자 ({over_pct:.1f}%)")

    with col2:
        st.subheader("📊 분석 결과 요약")
        st.metric("산출 적정가", f"€{fair_val:,.1f}만")
        st.metric("실제 거래액", f"€{actual_fee:,.1f}만")
        st.metric("가치 평가율", f"{over_pct:+,.1f}%")

    st.markdown("---")
    action_mode = "update" if (edit_mode and t_row) else "save_all"
    btn_label = f"🔄 '{p_name or '선수'}' 구글 시트 업데이트 (행: {t_row})" if (edit_mode and t_row) else "💾 구글 시트에 신규 저장하기"

    if st.button(btn_label, type="primary", use_container_width=True, key="v3_save_btn"):
        if not p_name.strip():
            st.warning("⚠️ 선수 이름을 입력해 주세요.")
        else:
            with st.spinner("구글 시트 전송 중..."):
                payload = {
                    "action": action_mode,
                    "row_index": t_row if (edit_mode and t_row) else None,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "season": season_val,
                    "name": p_name,
                    "nat": p_nat if p_nat.strip() else "미상",
                    "age": int(p_age),
                    "pos": main_pos.split(" (")[0],
                    "from_league": selling_league.split(" (")[0],
                    "buying_tier": buying_tier.split(":")[0],
                    "transfer_type": transfer_type.split(" (")[0],
                    "tm_val": float(tm_val),
                    "fee": float(actual_fee),
                    "fair_val": round(fair_val, 1),
                    "diff": round(diff_val, 1),
                    "status": stat_lbl,
                    "deal_score": 8.0,
                    "prev_matches": 10, "prev_starts": 10, "prev_mins": 900, "prev_goals": 5, "prev_xg": 4.5, "prev_assists": 3, "prev_xa": 2.5,
                    "prev_shots": 0, "prev_sot": 0, "prev_chances": 0, "prev_dribbles": 0, "prev_touches_box": 0, "prev_tackles": 0,
                    "prev_rating": 7.20,
                    "to_league": p_to_l.split(" (")[0],
                    "proj_mins": 3000,
                    "proj_goals": 0.0, "proj_xg": 0.0, "proj_assists": 0.0, "proj_xa": 0.0, "proj_shots": 0.0, "proj_rating": 7.0,
                    "notes": p_notes,
                    "from_team": p_from_t.strip(),
                    "to_team": p_to_t.strip(),
                    "to_league_name": p_to_l.split(" (")[0],
                    "trade_type": "OUT" if is_out else "IN",
                    "weekly_wage": float(weekly_wage)
                }
                try:
                    res = requests.post(GOOGLE_SHEET_WEBAPP_URL, data=json.dumps(payload), headers={"Content-Type": "text/plain;charset=utf-8"}, timeout=30)
                    if res.status_code in [200, 302]:
                        st.session_state["v3_msg"] = f"✅ '{p_name}' 처리 완료! (구글 시트 행: {t_row if t_row else '신규'})"
                        st.session_state["v3_edit_row"] = None
                        st.cache_data.clear()
                        st.rerun()
                except Exception as e:
                    st.error(f"⚠️ 통신 오류: {e}")
