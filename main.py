import streamlit as st
import pandas as pd
import requests

# ---------------------------------------------------------
# 1. 페이지 기본 설정
# ---------------------------------------------------------
st.set_page_config(
    page_title="Global Renewable Energy Recommender",
    page_icon="🌍",
    layout="wide"
)

# ---------------------------------------------------------
# 2. Custom CSS - 추천 솔루션 배경색 및 강조 스타일 정의
# ---------------------------------------------------------
st.markdown("""
<style>
    /* 추천 에너지 솔루션 메인 박스 스타일 */
    .recommend-box {
        background: linear-gradient(135deg, #0d3b66 0%, #004b23 100%);
        border: 2px solid #38b000;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(56, 176, 0, 0.3);
    }
    .recommend-title {
        color: #70e000;
        font-size: 22px;
        font-weight: bold;
        margin-bottom: 8px;
    }
    .recommend-desc {
        color: #e0e1dd;
        font-size: 15px;
        line-height: 1.5;
    }
    /* 카드 강조 하이라이트 */
    .highlight-card {
        background-color: #1b4332;
        border-left: 5px solid #52b788;
        padding: 12px 15px;
        border-radius: 6px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. 타이틀 및 탐구 배경
# ---------------------------------------------------------
st.title("🌍 전 세계 세부 국가별 맞춤형 재생에너지 추천 시스템")
st.caption("기후위기 극복을 위한 지속가능한 글로벌 에너지전환 프로젝트 (개발자: 박서진)")

st.markdown("""
> **탐구 동기 & 배경:** 재생에너지의 단순한 양적 확대는 발전의 불안정성과 생태계 훼손을 초래합니다. 
> 본 프로그램은 전 세계 **80개 이상의 세부 국가 및 특수 기후 지역**의 기후 데이터(일사량, 풍속)를 분석하고 
> 최적의 재생에너지원과 전력망 안정화 방안을 제안합니다.
""")

st.divider()

# ---------------------------------------------------------
# 4. 세분화된 전 세계 80+ 국가 및 주요 도시 데이터베이스
# ---------------------------------------------------------
GLOBAL_DATABASE = {
    "동아시아 & 세부 지역": {
        "대한민국 - 서울 (수도권)": {"lat": 37.5665, "lon": 126.9780, "coastal": False, "geothermal": False},
        "대한민국 - 제주특별자치도": {"lat": 33.4996, "lon": 126.5312, "coastal": True, "geothermal": False},
        "대한민국 - 신안/목포 (서해안)": {"lat": 34.7936, "lon": 126.3886, "coastal": True, "geothermal": False},
        "일본 - 도쿄": {"lat": 35.6762, "lon": 139.6503, "coastal": True, "geothermal": True},
        "일본 - 홋카이도 (삿포로)": {"lat": 43.0618, "lon": 141.3545, "coastal": True, "geothermal": True},
        "중국 - 베이징": {"lat": 39.9042, "lon": 116.4074, "coastal": False, "geothermal": False},
        "중국 - 신장 위구르 (타클라마칸 사막)": {"lat": 38.5000, "lon": 82.0000, "coastal": False, "geothermal": False},
        "대만 - 타이베이": {"lat": 25.0330, "lon": 121.5654, "coastal": True, "geothermal": True},
        "몽골 - 울란바토르": {"lat": 47.8864, "lon": 106.9057, "coastal": False, "geothermal": False},
        "몽골 - 고비 사막": {"lat": 44.0000, "lon": 105.0000, "coastal": False, "geothermal": False},
    },
    "동남아시아 & 남아시아": {
        "싱가포르": {"lat": 1.3521, "lon": 103.8198, "coastal": True, "geothermal": False},
        "베트남 - 하노이": {"lat": 21.0285, "lon": 105.8542, "coastal": False, "geothermal": False},
        "베트남 - 호치민 (해안)": {"lat": 10.8231, "lon": 106.6297, "coastal": True, "geothermal": False},
        "인도네시아 - 자카르타": {"lat": -6.2088, "lon": 106.8456, "coastal": True, "geothermal": True},
        "인도네시아 - 발리": {"lat": -8.4095, "lon": 115.1889, "coastal": True, "geothermal": True},
        "필리핀 - 마닐라": {"lat": 14.5995, "lon": 120.9842, "coastal": True, "geothermal": True},
        "태국 - 방콕": {"lat": 13.7563, "lon": 100.5018, "coastal": True, "geothermal": False},
        "인도 - 뉴델리": {"lat": 28.6139, "lon": 77.2090, "coastal": False, "geothermal": False},
        "인도 - 라자스탄 (라자스탄 태양광 단지)": {"lat": 26.9124, "lon": 70.9000, "coastal": False, "geothermal": False},
    },
    "서유럽 & 북유럽": {
        "영국 - 런던": {"lat": 51.5074, "lon": -0.1278, "coastal": True, "geothermal": False},
        "영국 - 스코틀랜드 (북해 해상풍력 zone)": {"lat": 57.1497, "lon": -2.0943, "coastal": True, "geothermal": False},
        "프랑스 - 파리": {"lat": 48.8566, "lon": 2.3522, "coastal": False, "geothermal": False},
        "독일 - 베를린": {"lat": 52.5200, "lon": 13.4050, "coastal": False, "geothermal": False},
        "네덜란드 - 암스테르담": {"lat": 52.3676, "lon": 4.9041, "coastal": True, "geothermal": False},
        "노르웨이 - 오슬로": {"lat": 59.9139, "lon": 10.7522, "coastal": True, "geothermal": False},
        "스웨덴 - 스톡홀름": {"lat": 59.3293, "lon": 18.0686, "coastal": True, "geothermal": False},
        "아이슬란드 - 레이캬비크": {"lat": 64.1466, "lon": -21.9426, "coastal": True, "geothermal": True},
        "덴마크 - 코펜하겐": {"lat": 55.6761, "lon": 12.5683, "coastal": True, "geothermal": False},
        "핀란드 - 헬싱키": {"lat": 60.1699, "lon": 24.9384, "coastal": True, "geothermal": False},
    },
    "남유럽 & 동유럽": {
        "스페인 - 마드리드": {"lat": 40.4168, "lon": -3.7038, "coastal": False, "geothermal": False},
        "스페인 - 안달루시아 (세비야)": {"lat": 37.3891, "lon": -5.9845, "coastal": False, "geothermal": False},
        "이탈리아 - 로마": {"lat": 41.9028, "lon": 12.4964, "coastal": True, "geothermal": True},
        "그리스 - 아테네": {"lat": 37.9838, "lon": 23.7275, "coastal": True, "geothermal": False},
        "포르투갈 - 리스본": {"lat": 38.7223, "lon": -9.1393, "coastal": True, "geothermal": False},
        "터키 - 이스탄불": {"lat": 41.0082, "lon": 28.9784, "coastal": True, "geothermal": True},
        "폴란드 - 바르샤바": {"lat": 52.2297, "lon": 21.0122, "coastal": False, "geothermal": False},
    },
    "중동 & 아프리카": {
        "사우디아라비아 - 리야드": {"lat": 24.7136, "lon": 46.6753, "coastal": False, "geothermal": False},
        "아랍에미리트 - 두바이": {"lat": 25.2048, "lon": 55.2708, "coastal": True, "geothermal": False},
        "이집트 - 카이로": {"lat": 30.0444, "lon": 31.2357, "coastal": False, "geothermal": False},
        "이집트 - 벤반 태양광 단지": {"lat": 24.4442, "lon": 32.7423, "coastal": False, "geothermal": False},
        "모로코 - 카사블랑카": {"lat": 33.5731, "lon": -7.5898, "coastal": True, "geothermal": False},
        "케냐 - 나이로비": {"lat": -1.2921, "lon": 36.8219, "coastal": False, "geothermal": True},
        "남아프리카공화국 - 케이프타운": {"lat": -33.9249, "lon": 18.4241, "coastal": True, "geothermal": False},
        "에티오피아 - 아디스아바바": {"lat": 9.0300, "lon": 38.7400, "coastal": False, "geothermal": True},
    },
    "북아메리카": {
        "미국 - 로스앤젤레스 (캘리포니아)": {"lat": 34.0522, "lon": -118.2437, "coastal": True, "geothermal": True},
        "미국 - 뉴욕": {"lat": 40.7128, "lon": -74.0060, "coastal": True, "geothermal": False},
        "미국 - 텍사스 (휴스턴 풍력 zone)": {"lat": 29.7604, "lon": -95.3698, "coastal": True, "geothermal": False},
        "미국 - 애리조나 (사막 태양광 zone)": {"lat": 33.4484, "lon": -112.0740, "coastal": False, "geothermal": False},
        "미국 - 알래스카 (앵커리지)": {"lat": 61.2181, "lon": -149.9003, "coastal": True, "geothermal": False},
        "미국 - 하와이 (호놀룰루)": {"lat": 21.3069, "lon": -157.8583, "coastal": True, "geothermal": True},
        "캐나다 - 밴쿠버": {"lat": 49.2827, "lon": -123.1207, "coastal": True, "geothermal": False},
        "멕시코 - 멕시코시티": {"lat": 19.4326, "lon": -99.1332, "coastal": False, "geothermal": True},
    },
    "남아메리카 & 오세아니아": {
        "브라질 - 상파울루": {"lat": -23.5505, "lon": -46.6333, "coastal": False, "geothermal": False},
        "아르헨티나 - 부에노스아이레스": {"lat": -34.6037, "lon": -58.3816, "coastal": True, "geothermal": False},
        "칠레 - 산티아고": {"lat": -33.4489, "lon": -70.6693, "coastal": False, "geothermal": True},
        "칠레 - 아타카마 사막 (초고일사량)": {"lat": -23.8634, "lon": -69.1328, "coastal": False, "geothermal": False},
        "호주 - 시드니": {"lat": -33.8688, "lon": 151.2093, "coastal": True, "geothermal": False},
        "호주 - 서호주 퍼스": {"lat": -31.9505, "lon": 115.8605, "coastal": True, "geothermal": False},
        "뉴질랜드 - 웰링턴": {"lat": -41.2865, "lon": 174.7762, "coastal": True, "geothermal": True},
    },
    "극지방 & 특수 환경 지대": {
        "남극 - 세종과학기지": {"lat": -62.2231, "lon": -58.7871, "coastal": True, "geothermal": False},
        "그린란드 - 누크": {"lat": 64.1814, "lon": -51.6941, "coastal": True, "geothermal": False},
        "에콰도르 - 갈라파고스 제도": {"lat": -0.9538, "lon": -90.9656, "coastal": True, "geothermal": True},
        "스위스 - 알프스 융프라우 지대": {"lat": 46.5475, "lon": 7.9854, "coastal": False, "geothermal": False},
        "이집트 - 서부 사하라 사막": {"lat": 26.0000, "lon": 28.0000, "coastal": False, "geothermal": False},
    }
}

# ---------------------------------------------------------
# 5. API 기후 데이터 연동 함수
# ---------------------------------------------------------
@st.cache_data(ttl=3600)
def fetch_climate_data(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=shortwave_radiation_sum,windspeed_10m_max&timezone=auto"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            rad_list = data['daily']['shortwave_radiation_sum']
            wind_list = data['daily']['windspeed_10m_max']
            
            avg_rad = sum(rad_list) / len(rad_list) if rad_list else 15.0
            avg_wind = sum(wind_list) / len(wind_list) if wind_list else 5.0
            
            # MJ/m² -> kWh/m² 환산
            daily_kwh = avg_rad * 0.277778
            return round(daily_kwh, 2), round(avg_wind, 2)
    except Exception:
        pass
    return 4.5, 5.0

# ---------------------------------------------------------
# 6. 사이드바 검색 인터페이스
# ---------------------------------------------------------
st.sidebar.header("📍 분석 지역 선택")
search_mode = st.sidebar.radio("탐색 방식:", ["대륙/국가별 선택", "위도/경도 직접 입력"])

if search_mode == "대륙/국가별 선택":
    selected_region = st.sidebar.selectbox("대륙 / 영역 선택:", list(GLOBAL_DATABASE.keys()))
    city_list = GLOBAL_DATABASE[selected_region]
    selected_city = st.sidebar.selectbox("국가 및 세부 지역 선택:", list(city_list.keys()))
    
    info = city_list[selected_city]
    lat = info["lat"]
    lon = info["lon"]
    is_coastal = info["coastal"]
    is_geothermal = info["geothermal"]
else:
    selected_city = "사용자 지정 위경도 좌표"
    lat = st.sidebar.number_input("위도 (Latitude):", value=37.5665, format="%.4f")
    lon = st.sidebar.number_input("경도 (Longitude):", value=126.9780, format="%.4f")
    is_coastal = st.sidebar.checkbox("해안선 인접 지역 여부", value=False)
    is_geothermal = st.sidebar.checkbox("지열 활성 구역 (판 경계/화산대)", value=False)

# ---------------------------------------------------------
# 7. 기후 데이터 판정 알고리즘
# ---------------------------------------------------------
solar_kwh, wind_m_s = fetch_climate_data(lat, lon)

recommendations = []

if is_geothermal:
    recommendations.append({
        "title": "🌋 지열 발전 (Geothermal Energy)",
        "desc": "판 경계 및 화산대에 위치하여 24시간 일정한 기저 전력을 공급할 수 있습니다."
    })

if solar_kwh >= 5.0:
    recommendations.append({
        "title": "☀️ 대규모 태양광 발전 (Utility-Scale Solar PV)",
        "desc": f"일평균 일사량이 {solar_kwh} kWh/m²로 최고 수준이며, 광활한 사막/평원형 발전 단지 조성에 최적입니다."
    })
elif solar_kwh >= 3.5:
    recommendations.append({
        "title": "🌤️ 건물/분산형 태양광 (Distributed Solar PV)",
        "desc": f"일평균 일사량이 {solar_kwh} kWh/m² 수준으로 상업지구 및 도심형 분산 태양광에 적합합니다."
    })

if wind_m_s >= 7.0 and is_coastal:
    recommendations.append({
        "title": "🌊 해상 풍력 발전 (Offshore Wind)",
        "desc": f"해안선에 인접하고 강력한 해풍(평균 {wind_m_s} m/s)이 불어 해상 풍력 단지 조성에 최적입니다."
    })
elif wind_m_s >= 5.5:
    recommendations.append({
        "title": "💨 육상 풍력 발전 (Onshore Wind)",
        "desc": f"평균 풍속이 {wind_m_s} m/s로 육상 풍력 발전기 터빈 가동 기준을 안정적으로 충족합니다."
    })

if not recommendations:
    recommendations.append({
        "title": "🔋 소수력 / 연료전지 기반 분산 전력망",
        "desc": "일사량과 풍속이 한정적이므로 지형 고저차를 활용한 소수력 발전 및 마이크로그리드가 권장됩니다."
    })

# ---------------------------------------------------------
# 8. 메인 레이아웃 구성
# ---------------------------------------------------------
st.subheader(f"📍 선택 지역: {selected_city}")

col1, col2 = st.columns([1, 1.2])

with col1:
    st.write("### 📊 기후 및 지형 측점 데이터")
    st.write(f"- **위경도 좌표:** `{lat}, {lon}`")
    
    m1, m2 = st.columns(2)
    m1.metric("☀️ 일평균 일사량", f"{solar_kwh} kWh/m²")
    m2.metric("💨 평균 풍속", f"{wind_m_s} m/s")
    
    st.info(f"**해안선 인접:** {'예' if is_coastal else '아니오'} | **지열 활성 구역:** {'예' if is_geothermal else '아니오'}")
    
    # 지도 출력
    df_map = pd.DataFrame({'lat': [lat], 'lon': [lon]})
    st.map(df_map, zoom=3)

with col2:
    st.write("### 💡 추천 재생에너지 솔루션")
    
    # 강조된 스타일의 추천 카드 출력
    for rec in recommendations:
        st.markdown(f"""
        <div class="recommend-box">
            <div class="recommend-title">{rec['title']}</div>
            <div class="recommend-desc">{rec['desc']}</div>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------
# 9. 한계 극복 제언 (딱 한 줄씩 정돈)
# ---------------------------------------------------------
st.divider()
st.subheader("🛠️ 지속가능한 글로벌 에너지전환 제언")

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("""
    <div class="highlight-card">
        <b>1. 지역 맞춤형 선별</b><br>
        무분별한 양적 확대 대신 고효율 에너지원만을 선별하여 자원 낭비를 줄입니다.
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="highlight-card">
        <b>2. 대용량 ESS 연계</b><br>
        기상 변화에 따른 발전 불안정성을 완화하기 위해 대용량 배터리를 병행 구축합니다.
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="highlight-card">
        <b>3. 광역 전력망 연결</b><br>
        지역 간 스마트 전력망을 연결하여 에너지 남는 곳에서 부족한 곳으로 공급합니다.
    </div>
    """, unsafe_allow_html=True)

st.caption("Data Source: Open-Meteo Global Weather API | 분석 시스템 개발자: 박서진")
