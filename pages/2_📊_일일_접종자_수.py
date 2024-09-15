# pages/2_📊_일일_접종자_수.py
import streamlit as st
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np

@st.cache_data
def load_data():
    df = pd.read_csv('data/vaccine_data.csv', encoding='utf-8')
    return df

# Session State에 데이터 저장
if 'data' not in st.session_state:
    st.session_state['data'] = load_data()


# Session State에서 데이터 불러오기
data = st.session_state['data']

st.header('일일 접종자 수')

# 필요한 컬럼 선택
columns_to_use = ['접종일', '당일 1차접종자 수', '당일 2차접종자 수', '당일 동절기접종자 수']
data = data[columns_to_use]

# 날짜 형식 변환 및 정렬
data['접종일'] = pd.to_datetime(data['접종일'], errors='coerce')
data = data.dropna(subset=['접종일'])
data = data.sort_values('접종일')

# 사용자 입력: 날짜 선택
start_date = st.date_input('시작 날짜', data['접종일'].min())
end_date = st.date_input('종료 날짜', data['접종일'].max())

# 사용자 입력: 접종 유형 선택
daily_columns = ['당일 1차접종자 수', '당일 2차접종자 수', '당일 동절기접종자 수']
selected_daily = st.multiselect(
    '시각화할 일일 접종자 수를 선택하세요',
    daily_columns,
    default=daily_columns
)

# 데이터 필터링
mask = (data['접종일'] >= pd.to_datetime(start_date)) & (data['접종일'] <= pd.to_datetime(end_date))
filtered_data = data.loc[mask]

# 막대 그래프 그리기 (옆에 나란히)
x = np.arange(len(filtered_data['접종일']))
width = 0.2

fig, ax = plt.subplots()

for i, column in enumerate(selected_daily):
    ax.bar(x + i * width, filtered_data[column], width=width, label=column)

ax.set_xlabel('접종일')
ax.set_ylabel('일일 접종자 수')

# x축 눈금 간격 조정
max_xticks = 10  # x축에 표시할 최대 눈금의 개수를 설정
tick_spacing = max(1, len(x) // max_xticks) #눈금 사이의 간격을 계산. 데이터 포인트의 수에 따라 간격을 동적으로 조절
xticks = x + width * (len(selected_daily) - 1) / 2 
ax.set_xticks(xticks[::tick_spacing]) # 계산된 간격에 따라 x축 눈금을 설정
ax.set_xticklabels(filtered_data['접종일'].dt.strftime('%Y-%m-%d').values[::tick_spacing], rotation=45) # 계산된 간격에 따라 x축 눈금을 설정


ax.legend()
st.pyplot(fig)
