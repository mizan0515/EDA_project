# pages/1_📈_누계_추이.py
import streamlit as st
import matplotlib.pyplot as plt
import koreanize_matplotlib
import pandas as pd

@st.cache_data
def load_data():
    df = pd.read_csv('data/vaccine_data.csv', encoding='utf-8')
    return df

# Session State에 데이터 저장
if 'data' not in st.session_state:
    st.session_state['data'] = load_data()


# Session State에서 데이터 불러오기
data = st.session_state['data']

st.header('접종 누계 추이')

# 필요한 컬럼 선택
columns_to_use = ['접종일', '1차접종 누계', '2차접종 누계', '동절기접종 누계']
data = data[columns_to_use]

# 날짜 형식 변환 및 정렬
data['접종일'] = pd.to_datetime(data['접종일'], errors='coerce')
data = data.dropna(subset=['접종일'])
data = data.sort_values('접종일')

# 사용자 입력: 날짜 선택
start_date = st.date_input('시작 날짜', data['접종일'].min())
end_date = st.date_input('종료 날짜', data['접종일'].max())

# 사용자 입력: 접종 유형 선택
vaccine_types = st.multiselect(
    '시각화할 접종 유형을 선택하세요',
    ['1차접종 누계', '2차접종 누계', '동절기접종 누계'],
    default=['1차접종 누계', '2차접종 누계', '동절기접종 누계']
)

# 데이터 필터링
mask = (data['접종일'] >= pd.to_datetime(start_date)) & (data['접종일'] <= pd.to_datetime(end_date))
filtered_data = data.loc[mask]

# 그래프 그리기
fig, ax = plt.subplots()
for vaccine_type in vaccine_types:
    ax.plot(filtered_data['접종일'], filtered_data[vaccine_type], marker='o', label=vaccine_type)
ax.set_xlabel('접종일')
ax.set_ylabel('접종 누계')
ax.legend()
ax.grid(True)
st.pyplot(fig)