
from AgentesIndependentes import analisar_previsao, analisar_tecnico, analisar_noticias, analisar_fundamentalista
from AgentesAvaliadores import avaliador_1, avaliador_2
from LSTM import prever_com_lstm
from Noticias import buscar_noticias_financeiras_ddg
from Tecnico import gerar_indicadores_tecnicos, plotar_indicadores_tecnicos
import streamlit as st
import pandas as pd
from datetime import date
import os
from Util import limpar_pastas, baixar_dados_b3, carregar_config

config = carregar_config()

st.set_page_config(
    page_title="Agente Assistente de Investimentos",
    layout="wide",  
    initial_sidebar_state="expanded"
)

# Título da aplicação
st.markdown("<h1 style='text-align: center;'>📈 Sophos 📈</h1>", unsafe_allow_html=True) # title
st.markdown("<h3 style='text-align: center;'>Assistente de Investimentos Multi-Agentes</h3>", unsafe_allow_html=True) # title

# Leitura do arquivo de tickers
tickers_df = pd.read_csv("Diversos/ticker.csv")  # colunas: Papel, Nome, YahooTicker
ticker_dict = dict(zip(tickers_df["Nome"], tickers_df["YahooTicker"]))

# Seleção do ativo
empresa_nome = st.selectbox("Selecione a empresa", options=list(ticker_dict.keys()))
ticker_yahoo = ticker_dict[empresa_nome]

# Seleção de período
col1, col2 = st.columns(2)
with col1:
    data_inicio = st.date_input("Data de início", value=date(2024, 1, 1))
with col2:
    data_fim = st.date_input("Data de fim", value=date(2024, 12, 31))

# Controle de previsão com LSTM
dias_previsao = st.slider(
    "Quantos dias futuros deseja prever com LSTM?",
    min_value=30,
    max_value=180,
    value=126,
    step=1
)

# Upload de arquivos PDF adicionais
uploaded_files = st.file_uploader(
    "📎 Upload de documentos para análise (Excel)",
    type=["xlsx"],
    accept_multiple_files=False
)

# Salvar os arquivos na pasta DocsAnaliseFund
uploaded_excel_path = "DocsAnaliseFund/entrada_fundamentalista.xlsx"
if uploaded_files:
    os.makedirs("DocsAnaliseFund", exist_ok=True)
    with open(uploaded_excel_path, "wb") as f:
        f.write(uploaded_files.read())
    st.success("Arquivo salvo como sucesso!")

# Botão para executar o pipeline
if st.button("Executar análise"):
    with st.spinner("Processando..."):

        # Etapas principais
        df = baixar_dados_b3(ticker=ticker_yahoo, inicio=str(data_inicio), fim=str(data_fim))
        prever_com_lstm(df, ticker_yahoo, dias_previsao=dias_previsao)
        buscar_noticias_financeiras_ddg(empresa_nome)
        gerar_indicadores_tecnicos()
        plotar_indicadores_tecnicos()

        # Análises individuais
        ind_previsao = analisar_previsao()
        ind_tecnico = analisar_tecnico()
        ind_noticias = analisar_noticias()
        ind_fundamentalista = analisar_fundamentalista("entrada_fundamentalista.xlsx")

        # Avaliações finais
        pareceres = [ind_previsao, ind_tecnico, ind_noticias,ind_fundamentalista]
        avalia_1 = avaliador_1(pareceres)
        avalia_2 = avaliador_2(pareceres)


    # Interface com abas para resultados
    aba1, aba2, aba3, aba4, aba5, aba6, aba7, aba8, aba9 = st.tabs([
        "🔧 LSTM", "🔧 Notícias", "🔧 Técnicos", "💡 Fundamentalista",
        "💡 Previsão", "💡 Técnica", "💡 Sentimento", 
        "🧠 Avaliador 1", "🧠 Avaliador 2"
    ])

    with aba1:
        st.image("LSTMOutput/previsao.png", caption="Previsão com LSTM", use_container_width=True)

    with aba2:
        try:
            with open("NoticiasOutput/noticias.txt", "r", encoding="utf-8") as f:
                noticias_texto = f.read()
            st.text_area("Notícias Financeiras", noticias_texto, height=400)
        except FileNotFoundError:
            st.warning("Arquivo de notícias não encontrado.")

    with aba3:
        st.image("TecnicoOutput/indicadores.png", caption="Indicadores Técnicos", use_container_width=True)

    with aba4:
        st.markdown(f"### Análise Fundamentalista\n{ind_fundamentalista}")

    with aba5:
        st.markdown(f"### Análise de Previsão\n{ind_previsao}")

    with aba6:
        st.markdown(f"### Análise Técnica\n{ind_tecnico}")

    with aba7:
        st.markdown(f"### Análise de Sentimento\n{ind_noticias}")

    with aba8:
        st.markdown(f"### Avaliador 1\n{avalia_1}")

    with aba9:
        st.markdown(f"### Avaliador 2\n{avalia_2}")

limpar_pastas()