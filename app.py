from pathlib import Path
import pandas as pd
import streamlit as st
from core import process,to_excel

st.set_page_config(page_title='Automação de Relatórios',layout='wide')
st.title('Automação de planilhas e relatórios')
st.caption('Pipeline demonstrativo de validação e criação de relatórios; dados fictícios.')
u=st.file_uploader('Carregue CSV ou XLSX (ou utilize o exemplo)',type=['csv','xlsx'])
try:
    if u is None: df=pd.read_csv(Path(__file__).parent/'dados_exemplo/indicadores.csv')
    elif u.name.lower().endswith('.xlsx'): df=pd.read_excel(u)
    else: df=pd.read_csv(u)
    clean,issues,report=process(df)
    c1,c2,c3=st.columns(3)
    c1.metric('Registros recebidos',len(df))
    c2.metric('Registros válidos',len(clean))
    c3.metric('Registros com problemas',len(issues))
    st.subheader('Indicadores por setor')
    st.dataframe(report, use_container_width=True)
    st.subheader('Inconsistências')
    st.dataframe(issues, use_container_width=True)
    st.subheader('Dados tratados')
    st.dataframe(clean, use_container_width=True)
    st.download_button('Baixar relatório Excel (3 abas)',to_excel(clean,issues,report),'relatorio_gerado.xlsx',mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
except (ValueError,ImportError,UnicodeDecodeError,pd.errors.ParserError) as exc:
    st.error(f'Problema ao processar arquivo: {exc}')
