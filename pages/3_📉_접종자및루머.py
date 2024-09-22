import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path, encoding='utf-8')
    return df

# Session State에 데이터 저장
if 'data1' not in st.session_state:
    st.session_state['data1'] = load_data('data/vaccine_data.csv')

if 'data2' not in st.session_state:
    st.session_state['data2'] = load_data('data/grouped_vaccine.csv')

# Session State에서 데이터 불러오기
data = st.session_state['data2']

st.header('접종자 및 루머')

# '접종일'을 datetime으로 변환
data['접종일'] = pd.to_datetime(data['접종일'])

# 슬라이더를 사용하기 위해 '접종일'을 datetime.date 형식으로 변환
data['접종일_date'] = data['접종일'].dt.date

# 슬라이더로 선택한 기간 가져오기
start_date, end_date = st.slider(
    '접종일 범위를 선택하세요:',
    min_value=data['접종일_date'].min(),
    max_value=data['접종일_date'].max(),
    value=(data['접종일_date'].min(), data['접종일_date'].max()),
    format="YYYY-MM-DD"
)

# 선택한 날짜를 pd.Timestamp 형식으로 변환해 필터링
start_date = pd.Timestamp(start_date)
end_date = pd.Timestamp(end_date)

# 선택한 기간에 맞게 데이터 필터링
filtered_df = data[(data['접종일'] >= start_date) & (data['접종일'] <= end_date)]

# 필터링된 데이터를 시각화 (두 개의 y축 설정)
fig, ax1 = plt.subplots()

# 첫 번째 y축: '당일 1차접종자 수'
ax1.set_xlabel('접종일')
ax1.set_ylabel('당일 1차접종자 수', color='tab:blue')
ax1.plot(filtered_df['접종일'], filtered_df['당일 1차접종자 수'], color='tab:blue', label='당일 1차접종자 수')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# 두 번째 y축: '백신 가짜뉴스'
ax2 = ax1.twinx()
ax2.set_ylabel('백신 가짜뉴스', color='tab:red')
ax2.plot(filtered_df['접종일'], filtered_df['백신 가짜뉴스'], color='tab:red', label='백신 가짜뉴스')
ax2.tick_params(axis='y', labelcolor='tab:red')

# 그래프 제목 설정
plt.title('당일 1차접종자 수와 백신 가짜뉴스')

# 그래프 표시
st.pyplot(fig)
