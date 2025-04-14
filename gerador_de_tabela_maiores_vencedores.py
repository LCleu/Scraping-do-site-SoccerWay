# %%
import requests
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl
import xlrd
import datetime as dt
import numpy as np

# %%

def get_matches_table(url: str) -> pd.DataFrame:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Garante erro explícito se o request falhar

    soup = BeautifulSoup(response.content, "html.parser")

    # Encontra a tabela pela classe ou outro seletor
    table_container = soup.find("div", class_="table-container redesign")
    table = table_container.find("table", class_="matches")

    # Transforma a tabela HTML em string e depois em DataFrame
    df = pd.read_html(str(table))[0]

    return df

url = "https://br.soccerway.com/teams/brazil/fortaleza-esporte-clube/327/matches/"
df = get_matches_table(url)
#print(df.head())

# %%
urls = [
    "https://br.soccerway.com/teams/brazil/clube-atletico-mineiro/317/matches/",
    "https://br.soccerway.com/teams/brazil/esporte-clube-bahia/341/matches/",
    "https://br.soccerway.com/teams/brazil/botafogo-de-futebol-e-regatas/323/matches/",
    "https://br.soccerway.com/teams/brazil/ceara-sporting-club/333/matches/",
    "https://br.soccerway.com/teams/brazil/sport-club-corinthians-paulista/320/matches/",
    "https://br.soccerway.com/teams/brazil/cruzeiro-esporte-clube-belo-horizonte/304/matches/",
    "https://br.soccerway.com/teams/brazil/clube-de-regatas-de-flamengo/318/matches/",
    "https://br.soccerway.com/teams/brazil/fluminense-football-club/312/matches/",
    "https://br.soccerway.com/teams/brazil/fortaleza-esporte-clube/327/matches/",
    "https://br.soccerway.com/teams/brazil/gremio-foot-ball-porto-alegrense/313/matches/",
    "https://br.soccerway.com/teams/brazil/sport-club-internacional/308/matches/",
    "https://br.soccerway.com/teams/brazil/esporte-clube-juventude/314/matches/",
    "https://br.soccerway.com/teams/brazil/mirassol-futebol-clube/10164/matches/",
    "https://br.soccerway.com/teams/brazil/sociedade-esportiva-palmeiras/310/matches/",
    "https://br.soccerway.com/teams/brazil/clube-atletico-bragantino/2827/matches/",
    "https://br.soccerway.com/teams/brazil/santos-futebol-clube-sao-paulo/319/matches/",
    "https://br.soccerway.com/teams/brazil/sport-club-do-recife/338/matches/",
    "https://br.soccerway.com/teams/brazil/sao-paulo-futebol-clube/302/matches/",
    "https://br.soccerway.com/teams/brazil/cr-vasco-da-gama/321/matches/",
    "https://br.soccerway.com/teams/brazil/esporte-clube-vitoria/306/matches/",
]
#Achei melhor fazer  com for porque o map estava juntando todas as tabelas em uma só, com o for cada item da lista é um df diferente
lista_de_times = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19","20"]
for i in range(len(lista_de_times)):
    lista_de_times[i] = get_matches_table(urls[i])
#lista_de_times = list(map(get_matches_table, urls))


# %%
for i in range(len(lista_de_times)):#percorre todos os df da lista

    lista_de_times[i]['Data'] = pd.to_datetime(lista_de_times[i]['Data'])# muda a coluna data de string para date

# %%
for i in range(len(lista_de_times)):#percorre todos os df da lista

    lista_de_times[i]['Data'] >= dt.datetime(2025,1,1) # retorna True or False
    lista_de_times[i] = lista_de_times[i][lista_de_times[i]['Data'] >= dt.datetime(2025,1,1)] # salva e  filtra apenas os valores 
    #verdadeiros no DF

# %%
for i in range(len(lista_de_times)):#percorre todos os df da lista

    lista_de_times[i][lista_de_times[i]['Competição'] != "ADC"]
    lista_de_times[i] = lista_de_times[i][lista_de_times[i]['Competição'] != "ADC"]

# %%
# apagar colunas away tem e unnamed
for i in range(len(lista_de_times)):#percorre todos os df da lista

    lista_de_times[i].drop(lista_de_times[i].columns[[5,6]],axis = 1, inplace = True)

#vai de tabela em tabela apagando as duas ultimas colunas
#.drop apaga as colunas, lista_de_times[0].columns[[5,6]] são as colunas que serao dropadas
#axis 1 sinaliza que est´apagando colunas, inplace = true faz nao precisar criar outro df

# %%
for i in range(len(lista_de_times)):    
    lista_de_times[i]['Time Avaliado'] = 1 #cria a coluna time avaliado e coloca um valor 1 temporario nela


# %%
for j in range(len(lista_de_times)):#percorre a lista de times com os df de cada time

    for i in range(len(lista_de_times[j]['Outcome'])):#percorre cada linha da coluna outcome dos dfs dos times.
        lista_de_times[j]['Time Avaliado'].iloc[i] = lista_de_times[j]['Outcome'].mode()[0] #troca o 1 temporario da coluna time avaliado parao time que mais aparece na coluna outcome


# %%
for j in range(len(lista_de_times)):#percorre a lista de times com os df de cada time
    for i in range(len(lista_de_times[j]['Home team'])):#percorre cada linha da coluna home team dos dfs dos times.
        if lista_de_times[j].iloc[i,3][0] == "P": #lista de times[x]-> primeira tabela da lista,  iloc[i,3] -> item da linha i coluna 3, [0] primeiro caractere do item
            lista_de_times[j].iloc[i,3] = lista_de_times[j].iloc[i,3][3:-3] #retira todos os P que indicam cobrença de penalti


# %%
for i in range(len(lista_de_times)):    
    lista_de_times[i]['Gols pro'] = 1 #cria a coluna gols pro e coloca um valor 1 temporario nela


# %%
for j in range(len(lista_de_times)):#percorre a lista de times com os df de cada time
    lista_de_times[j].reset_index(drop = True, inplace = True) # reseta o index de volta oa normal 0 1 2 3, pq o drop linhas da proxima celula  só funciona com index 
    #drop = true para nao criar uma coluna com o index antigo
    #inplace  =  true faz n precisa criar outro df


# %%
for j in range(len(lista_de_times)):  # percorre a lista de times com os df de cada time
    rows_to_drop = []  # lista para armazenar os índices das linhas a serem dropadas

    for i in range(len(lista_de_times[j]['Home team'])):  # percorre cada linha da coluna outcome dos dfs dos times.
        if (len(lista_de_times[j].iloc[i, 3]) > 6) or (len(lista_de_times[j].iloc[i, 3]) < 5):  # verifica o comprimento
            rows_to_drop.append(i)  # adiciona o índice da linha à lista

    # dropa as linhas após a iteração
    lista_de_times[j].drop(rows_to_drop, inplace=True)


# %%
for j in range(len(lista_de_times)):#percorre a lista de times com os df de cada time
    for i in range(len(lista_de_times[j]['Outcome'])):#percorre cada linha da coluna outcome dos dfs dos times.
        if lista_de_times[j].iloc[i,2] == lista_de_times[j].iloc[i,5]:  # se outcome = time avaliado, pega o gol do lado esquerdo e bota em gols pro
            lista_de_times[j].iloc[i,6] = lista_de_times[j].iloc[i,3][0]

        if lista_de_times[j].iloc[i,2] != lista_de_times[j].iloc[i,5]: # se outcome != time avaliado, pega o gol da direita e bota em gols pro 
            lista_de_times[j].iloc[i,6] = lista_de_times[j].iloc[i,3][-1]
        

# %%
for j in range(len(lista_de_times)):    
    lista_de_times[j]['Gols contra'] = 1 #cria a coluna gols pro e coloca um valor 1 temporario nela


# %%
for j in range(len(lista_de_times)):#percorre a lista de times com os df de cada time
    for i in range(len(lista_de_times[j]['Outcome'])):#percorre cada linha da coluna outcome dos dfs dos times.
        if lista_de_times[j].iloc[i,2] == lista_de_times[j].iloc[i,5]:  # se outcome = time avaliado, pega o gol do lado direito e bota em gols contra
            lista_de_times[j].iloc[i,7] = lista_de_times[j].iloc[i,3][-1]

        if lista_de_times[j].iloc[i,2] != lista_de_times[j].iloc[i,5]: # se outcome != time avaliado, pega o gol da esquerda e bota em gols contra 
            lista_de_times[j].iloc[i,7] = lista_de_times[j].iloc[i,3][0]


# %%
for j in range(len(lista_de_times)):    
    lista_de_times[j]['Time desafiante'] = 1 #cria a coluna gols pro e coloca um valor 1 temporario nela


# %%
for j in range(len(lista_de_times)):#percorre a lista de times com os df de cada time

    for i in range(len(lista_de_times[j]['Outcome'])):#percorre cada linha da coluna outcome dos dfs dos times.
        if lista_de_times[j].iloc[i,2] == lista_de_times[j].iloc[1,5]:
            lista_de_times[j].iloc[i,8] = lista_de_times[j].iloc[i,4]

        if lista_de_times[j].iloc[i,2] != lista_de_times[j].iloc[1,5]:
            lista_de_times[j].iloc[i,8] = lista_de_times[j].iloc[i,2]


        

# %%
for j in range(len(lista_de_times)):    
    lista_de_times[j]['Vitoria'] = 1 #cria a coluna gols pro e coloca um valor 1 temporario nela


# %%
for j in range(len(lista_de_times)):#percorre a lista de times com os df de cada time

    for i in range(len(lista_de_times[j]['Vitoria'])):
        if lista_de_times[j].iloc[i,6] > lista_de_times[j].iloc[i,7]:
            lista_de_times[j].iloc[i,9] = "Sim"
        else:
            lista_de_times[j].iloc[i,9] = "Nao"


# %%
for j in range(len(lista_de_times)):#percorre todos os df da lista

    lista_de_times[j][lista_de_times[j]['Vitoria'] == "Sim"]
    lista_de_times[j] = lista_de_times[j][lista_de_times[j]['Vitoria'] == "Sim"]

# %%
nomes_dos_times = [
    "Clube Atlético Mineiro",
    "Esporte Clube Bahia",
    "Botafogo de Futebol e Regatas",
    "Ceará Sporting Club",
    "Sport Club Corinthians Paulista",
    "Cruzeiro Esporte Clube Belo Horizonte",
    "Clube de Regatas do Flamengo",
    "Fluminense Football Club",
    "Fortaleza Esporte Clube",
    "Grêmio Foot-Ball Porto Alegrense",
    "Sport Club Internacional",
    "Esporte Clube Juventude",
    "Mirassol Futebol Clube",
    "Sociedade Esportiva Palmeiras",
    "Clube Atlético Bragantino",
    "Santos Futebol Clube São Paulo",
    "Sport Club do Recife",
    "São Paulo Futebol Clube",
    "CR Vasco da Gama",
    "Esporte Clube Vitória"
]
df_de_vitorias = pd.DataFrame(columns = ['Times','Qty vitorias', 'Times vencidos'])
df_de_vitorias['Times'] = nomes_dos_times


# %%

lista_Qty_vitorias = []

for j in range(20):
    unicos = np.unique(lista_de_times[j]['Time desafiante'])
    qty_unicos = len(unicos)
    lista_Qty_vitorias.append(qty_unicos)
    
df_de_vitorias['Qty vitorias'] = lista_Qty_vitorias


# %%

lista_times_vencidos = []

for j in range(20):

    lista_times_vencidos.append(np.unique(lista_de_times[j]['Time desafiante']))

df_de_vitorias['Times vencidos'] = lista_times_vencidos

print(df_de_vitorias.sort_values(by=['Qty vitorias'], ascending=False))


# %%


# %%
#lista de times na ordem dos links para nomear as planilhas
nomes_dos_times = [
    "Clube Atlético Mineiro",
    "Esporte Clube Bahia",
    "Botafogo de Futebol e Regatas",
    "Ceará Sporting Club",
    "Sport Club Corinthians Paulista",
    "Cruzeiro Esporte Clube Belo Horizonte",
    "Clube de Regatas do Flamengo",
    "Fluminense Football Club",
    "Fortaleza Esporte Clube",
    "Grêmio Foot-Ball Porto Alegrense",
    "Sport Club Internacional",
    "Esporte Clube Juventude",
    "Mirassol Futebol Clube",
    "Sociedade Esportiva Palmeiras",
    "Clube Atlético Bragantino",
    "Santos Futebol Clube São Paulo",
    "Sport Club do Recife",
    "São Paulo Futebol Clube",
    "CR Vasco da Gama",
    "Esporte Clube Vitória"
]

#Passando os dados para um formato excel de 1 time por planilha
'''
with pd.ExcelWriter("tabela_times_dados_brutos.xlsx") as writer:
    for i in range(len(lista_de_times)):
        lista_de_times[i].to_excel(writer, sheet_name=nomes_dos_times[i])'''


