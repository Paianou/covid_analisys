# 🦠 Análise Exploratória — COVID-19 no Brasil

Análise exploratória de dados da pandemia de COVID-19 no Brasil, com foco em evolução temporal, comparativo entre estados e distribuição de óbitos ao longo do tempo.

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458)
![Status](https://img.shields.io/badge/Status-Em%20andamento-yellow)

---

## 📌 Sobre o projeto

Este script realiza a limpeza, tratamento e análise exploratória de dados públicos de COVID-19 no Brasil, cruzando informações por cidade, estado e período nacional.

**Perguntas exploradas:**
- Como os casos evoluíram ao longo do tempo?
- Quais estados concentram mais casos?
- Como as mortes se distribuem mês a mês?

---

## 🗂️ Datasets utilizados

| Arquivo | Descrição |
|---|---|
| `brazil_covid19_cities.csv` | Casos por município ao longo do tempo |
| `brazil_covid19.csv` | Casos e mortes por estado e região |
| `brazil_covid19_macro.csv` | Visão nacional diária (casos, mortes) |

Fonte: [Kaggle — Brazil COVID-19 Dataset](https://www.kaggle.com/datasets/taweilo/brazil-covid19-dataset)

---

## 🔬 Metodologia

**Limpeza e preparação (`eda_corona.py`):**
- Conversão da coluna `date` para datetime, com descarte de valores inválidos
- Remoção de nulos no dataset nacional (`casos_df`)
- Criação de coluna com data formatada (`dd/mm/aaaa`)
- Tratamento de outliers em `cases` usando o método IQR (intervalo interquartil)

**Análises realizadas:**
- Série temporal de casos acumulados a nível nacional
- Top 10 estados por total de casos
- Mortes agregadas por mês

---

## 📁 Estrutura atual do repositório

```
covid_analisys/
├── eda_corona.py                  ← script principal de análise
├── data_bi/                       ← outputs preparados para BI
├── brazil_covid19.csv
├── brazil_covid19_cities.csv
└── brazil_covid19_macro.csv
```

> ⚠️ **Em organização:** os CSVs ainda estão versionados na raiz do repositório. A próxima etapa é movê-los para uma pasta `data/raw/` e adicioná-los ao `.gitignore`, já que arquivos de dados brutos não devem ficar no controle de versão.

---

## ▶️ Como reproduzir

```bash
git clone https://github.com/Paianou/covid_analisys.git
cd covid_analisys
pip install pandas matplotlib
```

Baixe os CSVs em [kaggle.com/datasets/taweilo/brazil-covid19-dataset](https://www.kaggle.com/datasets/taweilo/brazil-covid19-dataset) e coloque na raiz do projeto antes de rodar:

```bash
python eda_corona.py
```

---

## 🛠️ Tecnologias

`Python` `Pandas` `Matplotlib`

---

## 🚀 Próximos passos

- [ ] Mover CSVs para `data/raw/` e adicionar `.gitignore`
- [ ] Salvar os gráficos gerados em `outputs/figures/` com `plt.savefig()`
- [ ] Calcular e documentar taxa de mortalidade por estado
- [ ] Cruzar com dados de população para taxa por 100 mil habitantes
- [ ] Adicionar `requirements.txt`
- [ ] Construir dashboard no Power BI a partir dos dados de `data_bi/`

---

## 👤 Contato

**Thiago Paiano Souza** · [LinkedIn](https://www.linkedin.com/in/thiago-paiano-souza-a44616361/)
