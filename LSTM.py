import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Input
from pathlib import Path
import numpy as np
import pandas as pd


def prever_com_lstm(dados: pd.DataFrame, ticker: str, dias_previsao: int = 126):
    '''
    Faz forecast utilizando LSTM a partir dos dados baixados do Yahoo Finance
    Considera a coluna "Close"
    Salva Previsão + Imagem
    Imagem é carregada pela Aplicação e Avalidas pelo Agente
    
    '''

    if dados.empty or 'Close' not in dados.columns:
        print("Erro: DataFrame inválido.")
        return

    if 'Date' in dados.columns:
        dados['Date'] = pd.to_datetime(dados['Date'])
        dados.set_index('Date', inplace=True)

    df = dados[['Close']].copy()
    df.dropna(inplace=True)

    # Normalizar
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(df)

    # Criar sequência
    x_train, y_train = [], []
    timestamp = 45
    for i in range(timestamp, len(scaled)):
        x_train.append(scaled[i - timestamp:i, 0])
        y_train.append(scaled[i, 0])

    x_train, y_train = np.array(x_train), np.array(y_train)
    x_train = x_train.reshape((x_train.shape[0], x_train.shape[1], 1))

    # Modelo
    model = Sequential()
    model.add(Input(shape=(x_train.shape[1], 1)))
    model.add(LSTM(120, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(120, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(120, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(120, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')

    model.fit(x_train, y_train, epochs=50, batch_size=32, verbose=0)

    # Previsão futura
    entrada = scaled[-timestamp:].reshape(1, timestamp, 1)
    previsoes = []
    for _ in range(dias_previsao):
        pred = model.predict(entrada, verbose=0)
        previsoes.append(pred[0, 0])
        entrada = np.concatenate([entrada[:, 1:, :], pred.reshape(1, 1, 1)], axis=1)

    previsoes_desnormalizadas = scaler.inverse_transform(np.array(previsoes).reshape(-1, 1)).flatten()

    ult_data = df.index[-1]
    futuras_datas = pd.bdate_range(start=ult_data + pd.Timedelta(days=1), periods=dias_previsao, freq='B')

    # Criar pasta de saída
    output_dir = Path("LSTMOutput")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Gráfico
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['Close'], label='Histórico')
    plt.plot(futuras_datas, previsoes_desnormalizadas, label='Previsão LSTM', linestyle='--')
    plt.title(f'Previsão de {dias_previsao} dias para {ticker}')
    plt.xlabel('Data')
    plt.ylabel('Preço de Fechamento')
    plt.legend()
    plt.savefig(output_dir / "previsao.png")
    plt.close()

    # CSV
    df_previsoes = pd.DataFrame({
        'Data': futuras_datas,
        'Preco_Previsto': previsoes_desnormalizadas
    })
    df_previsoes.to_csv(output_dir / "previsao.csv", index=False)

    print(f"Gráfico salvo em: {output_dir / 'previsao.png'}")
    print(f"Previsões salvas em: {output_dir / 'previsao.csv'}")



