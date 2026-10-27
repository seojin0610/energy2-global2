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
# 2. Custom CSS - 가독성 향상 및 글자색 명확화
# ---------------------------------------------------------
st.markdown("""
<style>
    /* 추천 에너지 솔루션 메인 박스 스타일 */
    .recommend-box {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        border: 2px solid #4ea8de;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(78, 168, 222, 0.3);
    }
    .recommend-title {
        color: #f8f9fa !important;
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 8px;
    }
    .recommend-desc {
        color: #e9ecef !important;
        font-size: 15px;
        line-height: 1.5;
    }
    /* 제언 카드 - 글자 가독성 극대화 (밝은 카드 + 어두운 대비 글자) */
    .highlight-card {
        background-color: #f0fdf4;
        border: 2px solid #22c55e;
        border-left: 6px solid #15803d;
        padding: 16px 18px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .card-title {
        color: #14532d !important;
        font-size: 17px;
        font-weight: bold;
        margin-bottom: 6px;
    }
