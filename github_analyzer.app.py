import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1. 웹사이트 제목 및 소개
st.set_page_config(page_title="데이터 분석 자동화 툴", layout="wide")
st.title("📊 나만의 파이썬 데이터 분석 프로그램")
st.write("엑셀(xlsx) 또는 CSV 파일을 업로드하면 자동으로 데이터를 분석하고 그래프를 그려줍니다.")

# 2. 파일 업로드 기능
uploaded_file = st.file_uploader("분석할 파일을 선택하세요 (CSV 또는 XLSX)", type=["csv", "xlsx"])

if uploaded_file is not None:
    # 파일 확장자에 따라 판다스로 읽어오기
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        st.success("✅ 파일이 성공적으로 로드되었습니다!")
        
        # 3. 데이터 미리보기 및 기본 정보
        st.subheader("📋 데이터 미리보기 (상위 5개 행)")
        st.dataframe(df.head())
        
        # 탭을 나누어 분석 결과 보여주기
        tab1, tab2, tab3 = st.tabs(["데이터 요약", "통계 분석", "시각화 그래프"])
        
        with tab1:
            st.subheader("🔍 데이터 구조 정보")
            st.write(f"**전체 행 개수:** {df.shape[0]}개 | **전체 열(컬럼) 개수:** {df.shape[1]}개")
            st.write("**데이터 컬럼 목록:**", list(df.columns))
            
        with tab2:
            st.subheader("🔢 숫자형 데이터 기술 통계")
            st.write("평균, 최솟값, 최댓값 등이 자동으로 계산됩니다.")
            st.dataframe(df.describe())
            
        with tab3:
            st.subheader("📈 맞춤형 그래프 그리기")
            # 사용자가 직접 그래프를 그릴 열을 선택할 수 있게 함
            numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
            
            if len(numeric_columns) >= 1:
                x_axis = st.selectbox("X축으로 사용할 컬럼을 선택하세요", df.columns.tolist())
                y_axis = st.selectbox("Y축으로 사용할 숫자형 컬럼을 선택하세요", numeric_columns)
                chart_type = st.radio("그래프 종류를 선택하세요", ["선 그래프 (Line)", "막대 그래프 (Bar)"])
                
                # Matplotlib 그래프 그리기
                fig, ax = plt.subplots(figsize=(10, 4))
                if chart_type == "선 그래프 (Line)":
                    ax.plot(df[x_axis], df[y_axis], marker='o', color='#4285F4')
                else:
                    ax.bar(df[x_axis], df[y_axis], color='#34A853')
                
                ax.set_xlabel(x_axis)
                ax.set_ylabel(y_axis)
                ax.set_title(f"{x_axis}에 따른 {y_axis} 분석 그래프")
                plt.xticks(rotation=45)
                
                # 스트림릿 웹 화면에 그래프 출력
                st.pyplot(fig)
            else:
                st.warning("시각화할 수 있는 숫자형 데이터 컬럼이 없습니다.")
                
    except Exception as e:
        st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")
else:
    st.info("💡 왼쪽 상단이나 중심의 업로드 버튼을 눌러 데이터 파일을 넣어보세요.")