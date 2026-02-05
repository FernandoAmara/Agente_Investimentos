import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

def gerar_indicadores_tecnicos():
    """
    Lê o arquivo LSTMOutput/dados.csv, (dados originais do B3 baixados)
    calcula indicadores técnicos (RSI, MACD, Médias Móveis),
    e salva em TecnicoOutput/indicadores.csv
    """
    entrada = Path("LSTMOutput/dados.csv")
    if not entrada.exists():
        print("Erro: o arquivo LSTMOutput/dados.csv não foi encontrado.")
        return

    df = pd.read_csv(entrada)

    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)

    if 'Close' not in df.columns:
        print("Erro: coluna 'Close' não encontrada nos dados.")
        return

    # RSI (14 dias)
    delta = df['Close'].diff()
    ganho = delta.clip(lower=0)
    perda = -delta.clip(upper=0)
    media_ganho = ganho.rolling(window=14).mean()
    media_perda = perda.rolling(window=14).mean()
    rs = media_ganho / media_perda
    df['RSI_14'] = 100 - (100 / (1 + rs))

    # MACD
    ema_12 = df['Close'].ewm(span=12, adjust=False).mean()
    ema_26 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = ema_12 - ema_26
    df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

    # Médias móveis exponenciais
    df['MME_20'] = df['Close'].ewm(span=20, adjust=False).mean()
    df['MME_50'] = df['Close'].ewm(span=50, adjust=False).mean()
    df['MME_200'] = df['Close'].ewm(span=200, adjust=False).mean()

    # Salvar
    output_dir = Path("TecnicoOutput")
    output_dir.mkdir(parents=True, exist_ok=True)
    df.reset_index().to_csv(output_dir / "indicadores.csv", index=False)

    print(f"Indicadores técnicos salvos em: {output_dir / 'indicadores.csv'}")

def plotar_indicadores_tecnicos():
    """
    Gera gráficos para RSI, MACD e Médias Móveis com base no 
    arquivo gerado por gerar_indicadores_tecnicos e salva como TecnicoOutput/indicadores.png
    Esta imagem que é utilizada pelos Agentes
    """
    caminho_csv = Path("TecnicoOutput/indicadores.csv")
    if not caminho_csv.exists():
        print("Erro: Arquivo de indicadores técnicos não encontrado.")
        return

    df = pd.read_csv(caminho_csv)
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    plt.figure(figsize=(14, 10))

    # 1. Preço + Médias móveis
    plt.subplot(3, 1, 1)
    plt.plot(df['Close'], label='Fechamento')
    plt.plot(df['MME_20'], label='MME 20')
    plt.plot(df['MME_50'], label='MME 50')
    plt.plot(df['MME_200'], label='MME 200')
    plt.title('Preço + Médias Móveis')
    plt.legend()

    # 2. MACD
    plt.subplot(3, 1, 2)
    plt.plot(df['MACD'], label='MACD', color='blue')
    plt.plot(df['MACD_Signal'], label='Signal', color='red')
    plt.bar(df.index, df['MACD'] - df['MACD_Signal'], color='gray', alpha=0.3)
    plt.title('MACD e Signal')
    plt.legend()

    # 3. RSI
    plt.subplot(3, 1, 3)
    plt.plot(df['RSI_14'], label='RSI (14)', color='purple')
    plt.axhline(70, linestyle='--', color='red', alpha=0.6)
    plt.axhline(30, linestyle='--', color='green', alpha=0.6)
    plt.title('Índice de Força Relativa (RSI)')
    plt.legend()

    # Layout final
    plt.tight_layout()
    saida = Path("TecnicoOutput/indicadores.png")
    plt.savefig(saida)
    plt.close()

    print(f"Gráfico salvo em: {saida}")

