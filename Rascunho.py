import requests
from bs4 import BeautifulSoup
import pandas as pd

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

urls = [
    "https://br.soccerway.com/teams/brazil/clube-atletico-mineiro/317/matches/",
    "https://br.soccerway.com/teams/brazil/esporte-clube-bahia/341/matches/",
    "https://br.soccerway.com/teams/brazil/botafogo-de-futebol-e-regatas/323/matches/",
    "https://br.soccerway.com/teams/brazil/ceara-sporting-club/333/matches/",
    "https://br.soccerway.com/teams/brazil/sport-club-corinthians-paulista/320/matches/",
    "https://br.soccerway.com/teams/brazil/cruzeiro-esporte-clube-belo-horizonte/304/matches/",
    "https://br.soccerway.com/teams/brazil/sport-club-corinthians-paulista/320/matches/",
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

lista_de_times = list(map(get_matches_table, urls))
lista_de_times



