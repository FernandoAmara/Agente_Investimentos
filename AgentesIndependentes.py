from pathlib import Path
from openai import OpenAI
import pandas as pd
from Util import carregar_config, img_b64, chamar_multimodal, chamar_textual


config = carregar_config()
client = OpenAI(api_key=config["openai_api_key"])

def analisar_previsao() -> str:
    '''
    Agente que vai analisar a previsão LSTM a partir da imagem
    '''
    imagem = img_b64(Path("LSTMOutput/previsao.png"))
    prompt = config["prompts"]["independentes"]["analisar_previsao"]
    modelo = config["modelos"]["independentes"]["analisar_previsao"]
    return chamar_multimodal(prompt, imagem, modelo)

def analisar_tecnico() -> str:
    '''
    Agente que vai analisar a analise técnica a partir da imagem
    '''
    imagem = img_b64(Path("TecnicoOutput/indicadores.png"))
    prompt = config["prompts"]["independentes"]["analisar_tecnico"]
    modelo = config["modelos"]["independentes"]["analisar_tecnico"]
    return chamar_multimodal(prompt, imagem, modelo)

def analisar_noticias() -> str:
    '''
    Agente que vai analisar as noticias salvas em disco
    '''
    texto = Path("NoticiasOutput/noticias.txt").read_text(encoding="utf-8")[:4500]
    prompt = config["prompts"]["independentes"]["analisar_noticias"]
    modelo = config["modelos"]["independentes"]["analisar_noticias"]
    return chamar_textual(prompt, texto, modelo)

def analisar_fundamentalista(doc: str) -> str:
    '''
    Agente que vai fazer a analise fundamentalista, carregando arquivo padrão
    '''
    caminho_excel = Path(f"DocsAnaliseFund/{doc}")
    if not caminho_excel.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho_excel}")

    planilhas = pd.read_excel(caminho_excel, sheet_name=None)

    abas_obrigatorias = [
        "DF Ind Ativo", "DF Ind Passivo", "DF Ind Resultado Periodo",
        "DF Ind Fluxo de Caixa", "DF Ind Valor Adicionado"
    ]

    resumo = ""
    for aba in abas_obrigatorias:
        if aba in planilhas:
            df = planilhas[aba].dropna(how="all")
            if not df.empty:
                resumo += f"\n\n### {aba} ###\n"
                resumo += df.head(5).to_string(index=False)

    prompt = config["prompts"]["independentes"]["analisar_fundamentalista"]
    modelo = config["modelos"]["independentes"]["analisar_fundamentalista"]

    return chamar_textual(prompt, resumo[:4000], modelo)


