[README.md](https://github.com/user-attachments/files/28552153/README.md)
# 🦠 Análise da COVID-19 no Brasil (2020-2021)
### Análise Exploratória Completa · Python · Power BI · Dashboard Interativo

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-1.3-150458)
![Power BI](https://img.shields.io/badge/PowerBI-Dashboard-ffd700)
![Status](https://img.shields.io/badge/Status-Completo-brightgreen)

---

## 📌 Visão Geral do Projeto

Este projeto realiza uma **análise exploratória completa** do impacto da COVID-19 no Brasil, cobrindo:

- **Evolução temporal** da pandemia (fevereiro 2020 — maio 2021)
- **Comparativo entre estados e regiões** — quem foi mais afetado?
- **Taxa de mortalidade** por população — incidência por 100k habitantes
- **Análise de cidades** — identificar hotspots da doença
- **Dashboard interativo** em Power BI para visualização dinâmica

**Pergunta central**: Como a COVID-19 se distribuiu geograficamente pelo Brasil e como evoluiu ao longo do tempo?

---

## 📊 Principais Descobertas

| Métrica | Valor |
|---|---|
| **Período analisado** | Fev/2020 — Mai/2021 (15 meses) |
| **Casos totais** | ~16.4 milhões |
| **Mortes totais** | ~460 mil |
| **Taxa de mortalidade geral** | ~2.8% |
| **Estado mais afetado** | São Paulo (casos) |
| **Estado com maior taxa** | Amazonas (% da população) |
| **Cidades analisadas** | 5.570 municípios |

---

## 🗂️ Estrutura do Repositório

```
covid19-analise-brasil/
├── analise_covid_brasil_completa.py    ← Script principal (limpeza + análise)
├── data_bi/                             ← Outputs para Power BI
│   ├── 01_serie_temporal_diaria.csv
│   ├── 02_resumo_por_estado.csv
│   ├── 03_resumo_por_regiao.csv
│   ├── 04_resumo_por_cidade.csv
│   ├── 05_serie_temporal_mensal.csv
│   └── bruto_covid_por_estado.csv
├── outputs/figures/                     ← Gráficos estáticos
│   ├── 01_evolucao_temporal.png
│   ├── 02_top10_estados.png
│   ├── 03_mortes_por_regiao.png
│   ├── 04_taxa_mortalidade_por_estado.png
│   └── 05_casos_vs_mortes_diarias.png
├── power_bi/
│   └── covid19_brasil_dashboard.pbix   ← Dashboard Power BI (publicar)
├── requirements.txt
└── README.md
```

---

## 🔬 Metodologia

### Limpeza de Dados

- **Conversão de datas** com validação de erros
- **Remoção de nulos** nas colunas críticas (date, cases, deaths)
- **Tratamento de outliers** usando IQR (Interquartile Range)
  - Removidos ~X registros extremos que distorciam tendências
- **Validação de integridade** — garantir que casos ≥ 0 e mortes ≤ casos

### Transformações

- **Colunas derivadas**: year, month, week, day_of_week
- **Taxa de mortalidade** = (mortes / casos) × 100
- **Taxa por 100k habitantes** = (casos / população) × 100.000
- **Média móvel 7 dias** para suavizar flutuações diárias
- **Séries acumuladas** para visualizar crescimento cumulativo

### Agregações

| Nível | Descrição |
|---|---|
| **Diário** | Casos e mortes por dia (série temporal) |
| **Mensal** | Agregação para análise de tendências sazonais |
| **Por estado** | Total acumulado + taxa de mortalidade |
| **Por região** | Agregação em 5 regiões geográficas (Norte, Nordeste, etc) |
| **Por cidade** | 5.570 municípios com taxa por 100k |

---

## 📈 Análises Realizadas

### 1️⃣ Evolução Temporal
```python
# Série temporal diária com média móvel
serie_diaria = regiao_df.groupby('date').agg({
    'cases': 'sum',
    'deaths': 'sum'
})
```
**Insight**: Dois picos marcantes — um em julho 2020 e outro em março 2021. A média móvel revela a verdadeira tendência além das flutuações semanais.

### 2️⃣ Comparativo Estados
```python
# Top 10 estados por casos acumulados
estado_resumo.nlargest(10, 'total_casos')
```
**Insight**: São Paulo, Minas Gerais e Rio de Janeiro concentram ~40% dos casos nacionais.

### 3️⃣ Taxa de Mortalidade por População
```python
# Casos por 100 mil habitantes
cidades_resumo['casos_por_100k'] = (
    cidades_resumo['total_casos'] / cidades_resumo['population'] * 100000
)
```
**Insight**: Pequenas cidades do Amazonas têm taxa de incidência 10x maior que capitais.

### 4️⃣ Análise de Regiões
Agregação em Norte, Nordeste, Centro-Oeste, Sudeste e Sul mostra disparidades regionais.

---

## 🛠️ Tecnologias Utilizadas

| Ferramenta | Uso |
|---|---|
| **Python 3.8+** | Limpeza, transformação e análise |
| **Pandas** | Manipulação de dados (2.3M linhas) |
| **NumPy** | Cálculos numéricos e IQR |
| **Matplotlib & Seaborn** | Visualizações estáticas exploratórias |
| **Power BI** | Dashboard interativo e publicação |



## 📚 Documentação dos Dados

### Fonte Original
[Kaggle — Brazil COVID-19 Dataset](https://www.kaggle.com/datasets/taweilo/brazil-covid19-dataset)

### Arquivos Utilizados

| Arquivo | Linhas | Colunas | Descrição |
|---|---|---|---|
| `brazil_covid19.csv` | 12k | 5 | Casos diários por estado e região |
| `brazil_covid19_cities.csv` | 2.3M | 6 | Casos por município (dados granulares) |
| `brazil_covid19_macro.csv` | 450 | 7 | Visão nacional diária (recuperados, monitorados) |
| `brazil_population_2019.csv` | 2.8k | 8 | População por cidade (censo 2019) |
| `brazil_cities_coordinates.csv` | 5.5k | 6 | Latitude/longitude de municípios |

---

## 🎯 Próximos Passos

- [ ] Adicionar análise de sentimento em comentários públicos
- [ ] Correlação com indicadores socioeconômicos (PIB por estado)
- [ ] Previsão com ARIMA ou Prophet para período futuro
- [ ] Mapa interativo em Folium (Python) ou Mapbox (Power BI)
- [ ] Exportar dashboard como PDF automatizado
- [ ] Integrar dados em tempo real via API (se disponível)

---

## 📈 Métricas de Sucesso

Quando apresentar este projeto:

✅ **Dado real** — dataset público de 2.3M de registros  
✅ **Problema bem definido** — entender a distribuição geográfica  
✅ **Metodologia documentada** — cada decisão de limpeza explicada  
✅ **Múltiplos níveis de análise** — temporal, geográfico, por população  
✅ **Visualizações claras** — 5+ gráficos estáticos + dashboard interativo  
✅ **Output reutilizável** — CSVs prontos para BI, código limpable  
✅ **Portfolio-ready** — README, estrutura, commits organizados  


---

## 🤝 Contato

**Seu Nome** · [LinkedIn](https://linkedin.com/in/seu-perfil) · seu@email.com

---

## 📄 Licença

MIT License — veja LICENSE.txt para detalhes.

---

## 🙏 Créditos

Dataset: [Kaggle Brazil COVID-19 Dataset](https://www.kaggle.com/datasets/taweilo/brazil-covid19-dataset)  
Análise realizada em maio 2024
