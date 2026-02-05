# Sophos 📈 — Assistente de Investimentos Multi‑Agentes (LLMs + LSTM + Análise Técnica/Fundamentalista)

Projeto do curso **“IA para Investimentos: Crie Aplicação Multi‑Agentes com LLMs”** (Udemy).  
Ele implementa uma aplicação em **Python + Streamlit** com **múltiplos agentes** para apoiar análises de um ativo (ex.: ações), combinando:

- **Previsão de preço com LSTM** (TensorFlow) + análise via LLM (multimodal)
- **Indicadores técnicos** (RSI/MACD/MME) + análise via LLM (multimodal)
- **Sentimento de notícias** (DuckDuckGo Search) + análise via LLM
- **Análise fundamentalista** a partir de planilha (Excel) enviada pelo usuário
- **Agentes avaliadores** que consolidam os pareceres em uma recomendação final

> ⚠️ **Aviso importante:** este projeto é **educacional** e **não constitui recomendação de investimento**. Use por sua conta e risco.  
O curso aborda agentes independentes, análise técnica/fundamentalista/notícias, previsão com LSTM e uma interface com Streamlit. citeturn0search0

---

## 📦 Conteúdo do repositório

Arquivos principais:

- `app.py` — interface Streamlit (“Sophos”) e orquestração do pipeline
- `AgentesIndependentes.py` — agentes especialistas (previsão, técnico, notícias, fundamentalista)
- `AgentesAvaliadores.py` — agentes avaliadores (consolidação final)
- `LSTM.py` — treinamento/execução da LSTM e geração do gráfico
- `Tecnico.py` — geração/plot de indicadores técnicos
- `Noticias.py` — busca de notícias e export para arquivo
- `Util.py` — utilitários (config, download de preços via Yahoo Finance/yfinance, helpers multimodais, limpeza de pastas)
- `Diversos/ticker.csv` — lista de empresas/tickers (Yahoo)
- Pastas de saída:
  - `LSTMOutput/` (ex.: `previsao.png`, `dados.csv`)
  - `TecnicoOutput/` (ex.: `indicadores.png`)
  - `NoticiasOutput/` (ex.: `noticias.txt`)
- Entrada fundamentalista:
  - `DocsAnaliseFund/entrada_fundamentalista.xlsx` (gerada pelo upload no app)

---

## ✅ Pré‑requisitos

- **Python 3.10+** recomendado
- Uma **OpenAI API Key** válida
- Acesso à internet (para baixar preços e buscar notícias)

---

## 🔧 Instalação

### 1) Crie e ative um ambiente virtual

**Windows (PowerShell)**
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Linux/Mac**
```bash
python -m venv .venv
source .venv/bin/activate
```

### 2) Instale as dependências

```bash
pip install -r requirements.txt
```

> Dependências incluem: `streamlit`, `openai`, `tensorflow`, `yfinance`, `duckduckgo_search`, `pandas`, `matplotlib`, etc.

---

## 🔑 Configuração da chave da OpenAI (IMPORTANTE)

O projeto lê a chave a partir do arquivo `config.yaml` (`openai_api_key:`).

### Recomendado para publicar no GitHub
1) **NÃO** commite sua chave no repositório.
2) Troque o valor em `config.yaml` por um placeholder, por exemplo:
```yaml
openai_api_key: "COLOQUE_SUA_CHAVE_AQUI"
```
3) Adicione `config.yaml` ao `.gitignore` **ou** crie um `config.example.yaml` e use o arquivo real localmente.

> Dica: como o repo já tem `python-dotenv` instalado, você pode também adaptar o código para ler `OPENAI_API_KEY` de um `.env` e manter `config.yaml` sem segredo.

---

## ▶️ Como rodar

Inicie o Streamlit:

```bash
streamlit run app.py
```

Abra no navegador o endereço exibido (geralmente `http://localhost:8501`).

---

## 🧠 Como funciona o pipeline (alto nível)

No app (`app.py`), ao clicar em **“Executar análise”**:

1) Baixa histórico do ativo via **Yahoo Finance** (`yfinance`) e salva em `LSTMOutput/dados.csv`
2) Treina/gera previsão com **LSTM** e salva o gráfico em `LSTMOutput/previsao.png`
3) Busca notícias e salva em `NoticiasOutput/noticias.txt`
4) Gera indicadores técnicos e salva em `TecnicoOutput/indicadores.png`
5) Executa os **agentes especialistas**:
   - previsão (multimodal) → lê `previsao.png`
   - técnico (multimodal) → lê `indicadores.png`
   - notícias (textual) → lê `noticias.txt`
   - fundamentalista (textual) → lê o Excel enviado
6) Executa **2 avaliadores** para consolidar a recomendação final

O resultado aparece em abas:
- LSTM / Notícias / Técnicos / Fundamentalista
- Pareceres (previsão, técnica, sentimento)
- Avaliador 1 e Avaliador 2

---

## 📄 Entrada de análise fundamentalista (Excel)

No app, você pode fazer upload de **um arquivo `.xlsx`** (ex.: demonstrativos / indicadores).  
O arquivo será salvo como:

```
DocsAnaliseFund/entrada_fundamentalista.xlsx
```

E então usado pelo agente fundamentalista.

---

## 🧯 Problemas comuns

**1) `openai_api_key` inválida / erro de autenticação**  
- Verifique se a chave está correta no `config.yaml` (e se tem créditos/permissões na conta).

**2) Erros ao baixar dados do ativo**  
- Confirme se o ticker existe no Yahoo Finance (arquivo `Diversos/ticker.csv`).
- Teste um ticker conhecido (ex.: `PETR4.SA`, `VALE3.SA`, etc.).

**3) TensorFlow pesado / instalação lenta**  
- Em Windows, prefira Python 3.10/3.11 e atualize `pip`:
```bash
pip install --upgrade pip
```

**4) Notícias vazias**  
- Alguns termos/fontes podem retornar pouco conteúdo; ajuste `config.yaml` em `noticias:`.

---

## 🔒 Boas práticas para publicar como portfólio

- Remover/ocultar segredos (OpenAI key) e dados sensíveis
- Adicionar `.env.example` / `config.example.yaml`
- Incluir uma seção “Limitações” (ex.: LSTM não garante performance, notícias podem ter viés, etc.)
- Deixar explícito o **disclaimer** (não é recomendação)

---

## 📚 Referência (curso)

**IA para Investimentos: Crie Aplicação Multi‑Agentes com LLMs** (Udemy). citeturn0search0

---

## Autor

Fernando Amaral
