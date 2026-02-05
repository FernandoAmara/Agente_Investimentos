import pandas as pd
import yfinance as yf
from pathlib import Path
from openai import OpenAI
import yaml
import os
import shutil
import base64

def carregar_config(path_yaml: str = "config.yaml") -> dict:
    """
    Função para carregar dados de configuração
    """
    with open(path_yaml, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

config = carregar_config()
client = OpenAI(api_key=config["openai_api_key"])


def img_b64(path: Path) -> str:
    '''
    Converte imagem em string codificada em base 64
    Formato necessário para Imagens para Modelos Multi-Modal
    '''
    return base64.b64encode(path.read_bytes()).decode()

def baixar_dados_b3(ticker: str, inicio: str, fim: str) -> pd.DataFrame:
    '''
    Função para baixar dados do b3, usando Yahoo Finance
    Salva na pasta LSTMOutput
    '''
    try:
        acao = yf.Ticker(ticker)
        dados = acao.history(start=inicio, end=fim)

        if dados.empty:
            print("Nenhum dado foi retornado para o período especificado.")
            return pd.DataFrame()

        dados.reset_index(inplace=True)
        dados = dados[["Date", "Open", "High", "Low", "Close", "Volume"]]

        output_dir = Path("LSTMOutput")
        output_dir.mkdir(parents=True, exist_ok=True)
        caminho_csv = output_dir / "dados.csv"
        dados.to_csv(caminho_csv, index=False)

        print(f"Dados salvos com sucesso em: {caminho_csv}")
        return dados

    except Exception as e:
        print(f"Erro ao baixar ou salvar dados: {e}")
        return pd.DataFrame()


def chamar_multimodal(prompt: str, img_b64_str: str, modelo: str) -> str:
    '''
    Função para Modelos Multi-Modal    
    '''
    resposta = client.chat.completions.create(
        model=modelo,
        messages=[
            {"role": "system", "content": prompt},
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{img_b64_str}"}
                    }
                ]
            }
        ],
        temperature=0.2,
        max_tokens=512
    )
    return resposta.choices[0].message.content.strip()

def chamar_textual(prompt: str, text: str, modelo: str) -> str:
    '''
    Função para Modelos 
    '''
    resposta = client.chat.completions.create(
        model=modelo,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": text}
        ],
        temperature=0.3,
        max_tokens=512
    )
    return resposta.choices[0].message.content.strip()


def limpar_pastas():
    '''
    Limpa todos os dados gerados pela aplicação ao final da execução    
    '''
    pastas = ["LSTMOutput", "NoticiasOutput", "TecnicoOutput", "DocsAnaliseFund"]
    for pasta in pastas:
        if os.path.exists(pasta):
            for nome_arquivo in os.listdir(pasta):
                caminho_arquivo = os.path.join(pasta, nome_arquivo)
                try:
                    if os.path.isfile(caminho_arquivo):
                        os.remove(caminho_arquivo)
                    elif os.path.isdir(caminho_arquivo):
                        shutil.rmtree(caminho_arquivo)
                except Exception as e:
                    print(f"Erro ao remover {caminho_arquivo}: {e}")
        else:
            print(f"Pasta não encontrada: {pasta}")


    

