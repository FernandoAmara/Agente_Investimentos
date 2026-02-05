from duckduckgo_search import DDGS
from pathlib import Path
from Util import carregar_config

config = carregar_config()

def buscar_noticias_financeiras_ddg(empresa: str):
    '''
    Busca e salva noticiais financeiras da empresa
    Usa mecanismo DuckDuckGo
    Parametrôs de Busca definidos na configuração
    '''
    termos = config["noticias"].get("termos", [])
    fontes = config["noticias"].get("fontes", [])
    max_noticias = config["noticias"]["maximo_resultados"]

    output_dir = Path("NoticiasOutput")
    output_dir.mkdir(exist_ok=True)
    arquivo = output_dir / "noticias.txt"

    ddgs = DDGS()
    noticias = []

    for termo in termos:
        query = f"{empresa} {termo}"
        for resultado in ddgs.news(keywords=query, region="br-pt", max_results=max_noticias):
            link = resultado.get("url", "")
            if any(fonte in link for fonte in fontes):
                titulo = resultado.get("title", "Sem título")
                corpo = resultado.get("body", "")
                noticias.append((titulo, corpo, link))
            if len(noticias) >= max_noticias:
                break
        if len(noticias) >= max_noticias:
            break

    with open(arquivo, "w", encoding="utf-8") as f:
        if noticias:
            f.write(f"Resumo de notícias financeiras sobre {empresa}\n\n")
            for i, (titulo, corpo, link) in enumerate(noticias, 1):
                f.write(f"{i}. {titulo}\n")
                if corpo:
                    f.write(f"{corpo}\n")
                f.write(f"Link: {link}\n\n")
        else:
            f.write(f"Nenhuma notícia financeira encontrada para {empresa}.\n")

    print(f"{len(noticias)} notícias salvas em: {arquivo}")

