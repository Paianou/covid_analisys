import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Leitura
cidades_df = pd.read_csv('brazil_covid19_cities.csv')
regiao_df = pd.read_csv('brazil_covid19.csv')
casos_df = pd.read_csv('brazil_covid19_macro.csv')
populacao_df = pd.read_csv('brazil_population_2019.csv', sep=';')
coordenadas_df = pd.read_csv('brazil_cities_coordinates.csv')

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