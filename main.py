import streamlit as st
import pandas as pd
import requests

# ---------------------------------------------------------
# 페이지 기본 설정
# ---------------------------------------------------------
st.set_page_config(
    page_title="Global Renewable Energy Recommender",
    page_icon="🌍",
    layout="wide"
)

# ---------------------------------------------------------
# 헤더 및 탐구 동기 (연설문 내용 반영)
# ---------------------------------------------------------
st.title("🌍 전 세계 지역별 맞춤형 재생에너지 추천 시스템")
st.caption("기후위기 극복을 위한 지속가능한 글로벌 에너지전환 프로젝트 (개발자: 박서진)")

st.markdown("""
> **탐구 동기 & 배경:** 재생에너지의 단순한 양적 확대는 발전의 불안정성과 생태계 훼손을 초래합니다. 
> 세계은행(World Bank) 및 글로벌 기후 데이터(Open-Meteo)를 활용해 **전 세계 특정 도시 및 지역의 기후 특성(일사량, 풍속 등)**을 분석하고, 
> 해당 지역에 최적화된 재생에너지원과 전력망 안정화 방안(ESS 등)을 제안합니다.
""")

st.divider()

# ---------------------------------------------------------
# 글로벌 대표 도시/국가 데이터베이스 (API 백업 및 대표 지역)
# ---------------------------------------------------------
GLOBAL_CITIES = {
    "카이로, 이집트 (Cairo, Egypt)": {"lat": 30.0444, "lon": 31.2357, "coastal": False, "geothermal_zone": False},
    "레이캬비크, 아이슬란드 (Reykjavik, Iceland)": {"lat": 64.1466, "lon": -21.9426, "coastal": True, "geothermal_zone": True},
    "웰링턴, 뉴질랜드 (Wellington, New Zealand)": {"lat": -41.2865, "lon": 174.7762, "coastal": True, "geothermal_zone": True},
    "시드니, 호주 (Sydney, Australia)": {"lat": -33.8688, "lon": 151.2093, "coastal": True, "geothermal_zone": False},
    "리야드, 사우디아라비아 (Riyadh, Saudi Arabia)": {"lat": 24.7136, "lon": 46.6753, "coastal": False, "geothermal_zone": False},
    "런던, 영국 (London, UK)": {"lat": 51.5074, "lon": -0.1278, "coastal": True, "geothermal_zone": False},
    "자카르타, 인도네시아 (Jakarta, Indonesia)": {"lat": -6.2088, "lon": 106.8456, "coastal": True, "geothermal_zone": True},
    "서울, 대한민국 (Seoul, S. Korea)": {"lat": 37.5665, "lon": 126.9780, "coastal": False, "geothermal_zone": False},
    "제주, 대한민국 (Jeju, S. Korea)": {"lat": 33.4996, "lon": 126.5312, "coastal": True, "geothermal_zone": False},
    "LA, 미국 (Los Angeles, USA)": {"lat": 34.0522, "lon": -118.2437, "coastal": True, "geothermal_zone": False}
}

# ---------------------------------------------------------
# 기후 데이터 불러오기 함수 (Open-Meteo API 연동)
# ---------------------------------------------------------
@st.cache_data(ttl=3600)
def fetch_climate_data(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=shortwave_radiation_sum,windspeed_10m_max&timezone=auto"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            # 최근 일주일 평균 일사량(MJ/m²) 및 최대풍속(m/s)
            rad_list = data['daily']['shortwave_radiation_sum']
            wind_list = data['daily']['windspeed_10m_max']
            
            avg_rad = sum(rad_list) / len(rad_list) if rad_list else 15.0
            avg_wind = sum(wind_list) / len(wind_list) if wind_list else 5.0
            
            # MJ/m² -> kWh/m² 환산 (1 MJ = 0.277778 kWh)
            daily_kwh = avg_rad * 0.277778
            return round(daily_kwh, 2), round(avg_wind, 2)
    except Exception:
        pass
    return 4.2, 5.5 # 예외 발생 시 기본값

# ---------------------------------------------------------
# 사이드바: 지역 선택 및 위도/경도 직접 입력 옵션
# ---------------------------------------------------------
st.sidebar.header("📍 분석 지역 선택")
mode = st.sidebar.radio("입력 방식 선택:", ["전 세계 주요 도시 선택", "위도/경도 직접 입력"])

if mode == "전 세계 주요 도시 선택":
    selected_city = st.sidebar.selectbox("도시 선택:", list(GLOBAL_CITIES.keys()))
    city_info = GLOBAL_CITIES[selected_city]
    lat = city_info["lat"]
    lon = city_info["lon"]
    is_coastal = city_info["coastal"]
    is_geothermal = city_info["geothermal_zone"]
else:
    selected_city = "사용자 지정 좌표"
    lat = st.sidebar.number_input("위도 (Latitude):", value=37.5665, format="%.4f")
    lon = st.sidebar.number_input("경도 (Longitude):", value=126.9780, format="%.4f")
    is_coastal = st.sidebar.checkbox("해안선 인접 지역 여부", value=False)
    is_geothermal = st.sidebar.checkbox("지열 활성화 구역 (판 경계 등)", value=False)

# ---------------------------------------------------------
# 기후 데이터 분석 및 판정 로직
# ---------------------------------------------------------
solar_kwh, wind_m_s = fetch_climate_data(lat, lon)

# 추천 알고리즘
recommendations = []
reasons = []

if is_geothermal:
    recommendations.append("🌋 지열 발전 (Geothermal Energy)")
    reasons.append("판 경계에 위치하거나 지열 활성 구
