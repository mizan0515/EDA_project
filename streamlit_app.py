import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 데이터 로드 함수
@st.cache
def load_data():
    df = pd.read_csv('data/vaccine_data.csv', encoding='utf-8')
    return df

data = load_data()

st.title('백신 접종 데이터 시각화')

# 데이터 미리보기
st.subheader('데이터 미리보기')
st.dataframe(data.head())

# 필요한 컬럼 선택
columns_to_use = ['접종일', '당일 1차접종자 수', '1차접종 누계', '당일 2차접종자 수', '2차접종 누계', '당일 동절기접종자 수', '동절기접종 누계']
data = data[columns_to_use]

# 날짜 형식 변환
data['접종일'] = pd.to_datetime(data['접종일'], errors='coerce')

# NaT 값 제거 및 날짜로 정렬
data = data.dropna(subset=['접종일'])
data = data.sort_values('접종일')

# 사용자 입력: 날짜 선택
st.sidebar.subheader('날짜 선택')
start_date = st.sidebar.date_input('시작 날짜', data['접종일'].min())
end_date = st.sidebar.date_input('종료 날짜', data['접종일'].max())

# 사용자 입력: 접종 유형 선택
st.sidebar.subheader('접종 유형 선택')
vaccine_types = st.sidebar.multiselect(
    '시각화할 접종 유형을 선택하세요',
    ['1차접종 누계', '2차접종 누계', '동절기접종 누계'],
    default=['1차접종 누계', '2차접종 누계', '동절기접종 누계']
)

# 선택한 날짜 범위로 데이터 필터링
mask = (data['접종일'] >= pd.to_datetime(start_date)) & (data['접종일'] <= pd.to_datetime(end_date))
filtered_data = data.loc[mask]

# 시계열 그래프 그리기
st.subheader('접종 누계 추이')

fig, ax = plt.subplots()

for vaccine_type in vaccine_types:
    ax.plot(filtered_data['접종일'], filtered_data[vaccine_type], marker='o', label=vaccine_type)

ax.set_xlabel('접종일')
ax.set_ylabel('접종 누계')
ax.legend()
ax.grid(True)
st.pyplot(fig)

# 일일 접종자 수 바 차트
st.subheader('일일 접종자 수')

daily_columns = ['당일 1차접종자 수', '당일 2차접종자 수', '당일 동절기접종자 수']
selected_daily = st.multiselect(
    '시각화할 일일 접종자 수를 선택하세요',
    daily_columns,
    default=daily_columns
)

fig2, ax2 = plt.subplots()

for column in selected_daily:
    ax2.bar(filtered_data['접종일'], filtered_data[column], label=column)

ax2.set_xlabel('접종일')
ax2.set_ylabel('일일 접종자 수')
ax2.legend()
st.pyplot(fig2)

# 접종률 추이 그래프
st.subheader('접종률 추이')

# 접종률 컬럼 계산 (예시로 1차, 2차 접종률만 계산)
total_population = data['접종대상자'].iloc[0]  # 첫 번째 행의 접종대상자 수 사용

filtered_data['1차접종률(%)'] = (filtered_data['1차접종 누계'] / total_population) * 100
filtered_data['2차접종률(%)'] = (filtered_data['2차접종 누계'] / total_population) * 100

rate_columns = ['1차접종률(%)', '2차접종률(%)']
selected_rates = st.multiselect(
    '시각화할 접종률을 선택하세요',
    rate_columns,
    default=rate_columns
)

fig3, ax3 = plt.subplots()

for rate in selected_rates:
    ax3.plot(filtered_data['접종일'], filtered_data[rate], marker='o', label=rate)

ax3.set_xlabel('접종일')
ax3.set_ylabel('접종률 (%)')
ax3.legend()
ax3.grid(True)
st.pyplot(fig3)