import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')

# Leitura
cidades_df = pd.read_csv('data/raw/brazil_covid19_cities.csv')
regiao_df = pd.read_csv('data/raw/brazil_covid19.csv')
casos_df = pd.read_csv('data/raw/brazil_covid19_macro.csv')
populacao_df = pd.read_csv('data/raw/brazil_population_2019.csv', on_bad_lines='skip')
coordenadas_df = pd.read_csv('data/raw/brazil_cities_coordinates.csv')

# Info básica
print(f'Cidades: {cidades_df.shape[0]:,} linhas | {cidades_df.shape[1]} colunas')
print(f"Regiões: {regiao_df.shape[0]:,} linhas | {regiao_df.shape[1]} colunas")
print(f"Casos: {casos_df.shape[0]:,} linhas | {casos_df.shape[1]} colunas")
print(f"População: {populacao_df.shape[0]:,} linhas | {populacao_df.shape[1]} colunas")
print(f"Coordenadas: {coordenadas_df.shape[0]:,} linhas | {coordenadas_df.shape[1]} colunas")

print(casos_df.describe())

# Limpeza
for df in [cidades_df, casos_df, regiao_df]:
    df['date'] = pd.to_datetime(df['date'],errors='coerce')

for df in [casos_df]:df['date'].dt.strftime('%d/%m/%Y')

print(f'\nNulos em Casos_df antes: {casos_df.isnull().sum().sum()}')
casos_df = casos_df.dropna(subset=['date','cases','deaths'])
print(f'Nulos em casos_df depois: {casos_df.isnull().sum().sum()}')

print("Média de casos:", casos_df['cases'].mean())
print("Maior valor:", casos_df['cases'].max())
print("Menor valor:", casos_df['cases'].min())

# Outliers usada para identificar valores extremos tendeu
q1 = casos_df['cases'].quantile(0.25)
q3 = casos_df['cases'].quantile(0.75)
iqr = q3 - q1

limite_baixo = q1 - 1.5 * iqr
limite_alto = q3 + 1.5 * iqr

casos_df_outliers = len(casos_df)
casos_df = casos_df[
    (casos_df['cases'] >= limite_baixo) &
    (casos_df['cases'] <= limite_alto)
]

print(f'Outliers removidos : {casos_df_outliers - len(casos_df)} linhas')

casos_df['year'] = casos_df['date'].dt.year
casos_df['month'] = casos_df['date'].dt.month

#taxa mortaldidade
casos_df['taxa_mortalidade'] = np.where(
    casos_df['cases'] >= 0,
    (casos_df['deaths'] / casos_df['cases'] * 100).round(2),
0
)

casos_df['taxa_recuperacao'] = np.where(
    casos_df['cases'] >= 0,
    (casos_df['recovered'] / casos_df['cases'] * 100).round(2),
    np.nan
)

regiao_df['date'] = pd.to_datetime(regiao_df['date'],errors='coerce')
regiao_df=regiao_df.dropna(subset=['date','cases','deaths'])

estado_resumo = regiao_df.groupby('state').agg(
    total_casos=('cases', 'sum'),
    total_mortes=('deaths', 'sum'),
    primeiro_casos=('date', 'min'),
    ultimo_registro=('date', 'max')
).reset_index()

estado_resumo['taxa_mortalidadea_estado'] = (
    estado_resumo['total_mortes'] / estado_resumo['total_casos'] * 100
).round(2)

print('Resumo por Estado :',estado_resumo)

regiao_resumo = regiao_df.groupby('region').agg(
total_casos = ('cases', 'sum'),
total_mortes = ('deaths', 'sum')
).reset_index()

regiao_resumo['taxa_mortalidade_regiao'] = (
    regiao_resumo['total_mortes'] / regiao_resumo['total_casos'] * 100
).round(2)

print('Resumo por Regiao :',regiao_resumo)

serie_diaria = regiao_df.groupby('date').agg(
    casos_diarios = ('cases', 'sum'),
    mortes_diarios = ('deaths', 'sum')
).reset_index().sort_values('date')

serie_diaria['casos_media_movel_7d'] = serie_diaria['casos_diarios'].rolling(window=7, min_periods=1).mean().round(0)
serie_diaria['mortes_media_movel_7d'] = serie_diaria['mortes_diarios'].rolling(window=7, min_periods=1).mean().round(2)

serie_diaria['casos_acumulados'] = serie_diaria['casos_diarios'].cumsum()
serie_diaria['mortes_acumulados'] =serie_diaria['mortes_diarios'].cumsum()

print(f"\n Período: {serie_diaria['date'].min().date()} a {serie_diaria['date'].max().date()}")
print(f"   Total de dias: {len(serie_diaria)}")
print(f"   Casos acumulados: {serie_diaria['casos_acumulados'].iloc[-1]:,.0f}")
print(f"   Mortes acumuladas: {serie_diaria['mortes_acumulados'].iloc[-1]:,.0f}")

serie_mensal = regiao_df.copy()
serie_mensal['year_month'] = serie_mensal['date'].dt.to_period('M')
serie_mensal_agr = serie_mensal.groupby('year_month').agg(
    casos_mensais = ('cases', 'sum'),
    mortes_mensais = ('deaths', 'sum')
).reset_index()

print('Resumo Mensal (ultimo 6 meses ):',serie_mensal_agr.tail(6))

cidades_df['date'] = pd.to_datetime(cidades_df['date'], errors='coerce')
cidades_df = cidades_df.dropna(subset=['date','cases','deaths'])

cidades_resumo = cidades_df.groupby('code').agg(
    name=('name', 'first'),
    state=('state', 'first'),
    total_casos=('cases', 'sum'),
    total_mortes=('deaths', 'sum'),
    primeirocaso=('date', 'min'),
    ultimoregistro=('date', 'max')
).reset_index()

cidades_resumo ['taxa_mortalidade_cidade'] = (
    cidades_resumo['total_mortes'] / cidades_resumo['total_casos'] * 100
).round(2)

cidades_resumo = cidades_resumo.merge(
    populacao_df[['city_code', 'population']].rename(columns={'city_code': 'code'}),


    on='code',
    how='left'
)

cidades_resumo['mortes_por_100k']=(
    cidades_resumo['total_mortes'] / cidades_resumo['population'] * 100000
).round(2)

cidades_resumo['casos_por_100k']=(
    cidades_resumo['total_casos'] / cidades_resumo['population'] * 100000
).round(2)

top20_cidades = cidades_resumo.nlargest(20, 'total_casos')
print('\n Top 20 Cidades por Casos:')
print(top20_cidades[['name','state','total_casos','total_mortes','casos_por_100k']])


import os
os.makedirs('data/processed', exist_ok=True)

serie_diaria.to_csv('data/processed/01_serie_temporal_diaria.csv', index=False)
estado_resumo.to_csv('data/processed/02_resumo_por_estado.csv', index=False)
regiao_resumo.to_csv('data/processed/03_resumo_por_regiao.csv', index=False)
cidades_resumo.to_csv('data/processed/04_resumo_por_cidade.csv', index=False)
serie_mensal_agr.to_csv('data/processed/05_serie_temporal_mensal.csv', index=False)

regiao_df.to_csv('data/processed/bruto_covid_por_estado.csv', index=False)

casos_df.groupby('month')['cases'].mean().plot()
regiao_df.groupby('region')['cases'].sum()
#boxplot
sns.boxplot(x=casos_df['cases'],color= '#E2847D')
plt.title('Boxplot de casos')
plt.show()

# Casos
df_time = casos_df.groupby('date')['cases'].sum()

plt.figure(figsize=(10,5),)
df_time.plot()
plt.title('Casos ao longo do tempo')
plt.show()

# Top estados
top = regiao_df.groupby('state')['cases'].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(10,5))
top.plot(kind='bar')
plt.title('Top 10 estados')
plt.show()

# Mortes por mês
casos_df['month'] = casos_df['date'].dt.to_period('M')
monthly_deaths = casos_df.groupby('month')['deaths'].sum()

plt.figure(figsize=(10,5))
monthly_deaths.plot(kind='barh')
plt.title('Mortes por mês')
plt.show()

plt.scatter(casos_df['cases'], casos_df['deaths'],color='#E0A96D')
plt.xlabel('Casos')
plt.ylabel('Mortes')
plt.title('Casos vs Mortes')
plt.show()