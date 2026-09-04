import pandas as pd
import requests
import json
from datetime import datetime

# 1. 12대 가중치 사전 정의
LEAGUE_WEIGHTS = {
    "잉글랜드 프리미어리그 (EPL 1부)": 1.00, "스페인 라리가 (La Liga 1부)": 0.92,
    "독일 분데스리가 (Bundesliga 1부)": 0.91, "이탈리아 세리에 A (Serie A 1부)": 0.90,
    "프랑스 리그 1 (Ligue 1 1부)": 0.88, "잉글랜드 챔피언십 (EFL 2부)": 0.80,
    "포르투갈 프리메이라리가 (1부)": 0.78, "네덜란드 에레디비시 (Eredivisie 1부)": 0.77,
    "벨기에 주필러 프로 리그 (1부)": 0.75, "브라질 세리에 A (Brasileirão 1부)": 0.68,
    "독일 2. 분데스리가 (2부)": 0.67, "스페인 라리가 2 (세군다 2부)": 0.66,
    "튀르키예 쉬페르리그 (1부)": 0.65, "이탈리아 세리에 B (2부)": 0.64,
    "미국 메이저리그사커 (MLS 1부)": 0.64, "멕시코 리가 MX (1부)": 0.63,
    "스위스 슈퍼리그 (1부)": 0.62, "오스트리아 분데스리가 (1부)": 0.62,
    "덴마크 수페르리가 (1부)": 0.61, "스코틀랜드 프리미어십 (1부)": 0.60,
    "아르헨티나 프리메라 디비시온 (1부)": 0.60, "폴란드 엑스트라클라사 (1부)": 0.55,
    "프랑스 리그 2 (2부)": 0.55, "그리스 슈퍼리그 (1부)": 0.54,
    "사우디 프로리그 (SPL 1부)": 0.52, "일본 J1리그 (1부)": 0.50,
    "대한민국 K리그1 (1부)": 0.48, "스웨덴 알스벤스칸 (1부)": 0.48,
    "노르웨이 엘리테세리엔 (1부)": 0.47, "일본 J2리그 (2부)": 0.35,
    "대한민국 K리그2 (2부)": 0.33, "기타 리그": 0.30
}

CLUB_TIERS = {
    "Tier 1: 엘리트 메가클럽 (레알, 맨시티, 바이에른 등)": 1.05,
    "Tier 2: 빅클럽 (아스날, 리버풀, 바르샤 등)": 1.02,
    "Tier 3: 중상위권 클럽 (토트넘, 도르트문트 등)": 1.00,
    "Tier 4: 중하위권 클럽": 0.98,
    "Tier 5: 셀링/소형 클럽": 0.95
}

CONTRACT_WEIGHTS = {"6개월 이하 (FA 임박, -20%)": 0.80, "1년 남음 (-8%)": 0.92, "2년 남음 (기준 1.00)": 1.00, "3년 남음 (+2%)": 1.02, "4년 이상 (+4%)": 1.04}
POSITION_WEIGHTS = {"스트라이커 / 센터포워드 (ST/CF, +2%)": 1.02, "윙어 / 공격형 미드필더 (WG/CAM, +1%)": 1.01, "중앙 / 수비형 미드필더 (CM/CDM, 기준)": 1.00, "풀백 / 윙백 (RB/LB/WB, -1%)": 0.99, "센터백 (CB, -1%)": 0.99, "골키퍼 (GK, -3%)": 0.97}
VERSATILITY_WEIGHTS = {"단일 포지션 전담 (기준)": 1.00, "듀얼 롤 (+1%)": 1.01, "만능 유틸리티 (+2%)": 1.02}
REGISTRATION_WEIGHTS = {"일반 (쿼터 이슈 없음, 기준)": 1.00, "🏴󠁧󠁢󠁥󠁮󠁧󠁿 EPL 홈그로운 (+4%)": 1.04, "🏛️ 구단 유스 출신 (+2%)": 1.02, "🇪🇸🇮🇹 비EU 쿼터 소모 (-2%)": 0.98}
TRANSFER_TYPE_WEIGHTS = {"일반 완전 이적 (기준)": 1.00, "단순 1년 임대 (20%)": 0.20, "임대 후 의무 영입 (+2%)": 1.02, "임대 후 선택 영입": 0.20, "바이백 조항 (-5%)": 0.95, "셀온 지분 (-3%)": 0.97, "비공개 이적": 1.00, "FA 자유계약": 1.00}
BIG_STAGE_WEIGHTS = {"🌟 UCL 토너먼트 핵심 주전 (+3%)": 1.03, "🔥 UEL/국대 주전 (+1%)": 1.01, "⚖️ 메이저 경험 없음 (기준)": 1.00}
INJURY_WEIGHTS = {"🛡️ 철강왕 (+1%)": 1.01, "⚖️ 일반적인 수준 (기준)": 1.00, "⚠️ 잦은 잔부상 (-3%)": 0.97, "🚨 장기 부상 이력 (-6%)": 0.94}
URGENCY_WEIGHTS = {"⚖️ 일반 보강 (기준)": 1.00, "🔥 최우선 보강 타겟 (+4%)": 1.04, "🚨 패닉바이 / 대체불가 (+8%)": 1.08}

# 2. 포지션별 나이 보정 함수
def get_positional_age_weight(age, position_name):
    if "ST/CF" in position_name or "WG/CAM" in position_name:
        if age <= 19: return 1.05
        elif age <= 23: return 1.03
        elif age <= 27: return 1.00
        elif age <= 29: return 0.97
        elif age <= 31: return 0.90
        elif age <= 34: return 0.80
        else: return 0.65
    elif "GK" in position_name or "CB" in position_name:
        if age <= 19: return 1.01
        elif age <= 23: return 1.01
        elif age <= 27: return 1.00
        elif age <= 29: return 1.00
        elif age <= 31: return 0.96
        elif age <= 34: return 0.90
        else: return 0.78
    else:
        if age <= 19: return 1.03
        elif age <= 23: return 1.02
        elif age <= 27: return 1.00
        elif age <= 29: return 0.98
        elif age <= 31: return 0.92
        elif age <= 34: return 0.84
        else: return 0.70

def get_exact_val(row, col_name, default_val=""):
    try:
        if col_name in row and pd.notnull(row[col_name]) and str(row[col_name]).strip() not in ["", "nan", "None"]:
            return type(default_val)(row[col_name])
    except:
        pass
    return default_val
