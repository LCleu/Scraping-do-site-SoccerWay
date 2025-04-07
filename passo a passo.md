# 📝 Log de Tratamento da Planilha de Jogos - Análise do Melhor Time do Ano

Este documento descreve, passo a passo, o processo de limpeza e transformação dos dados brutos de partidas de futebol para análise do desempenho de um time específico (neste caso, **Atlético-MG**). A ideia é que qualquer pessoa (inclusive recrutadores) possa entender o processo seguido e até reproduzi-lo.

## ✅ Etapas Realizadas

### 1. Aplicação de Filtros e Tratamento Inicial

- Apliquei **filtros** na tabela inteira.
- Mudei o **tipo de dado da coluna "Data"** de número para **data**.
- Criei filtro na **coluna "Data"** para exibir **apenas o ano de 2025**.
- Na **coluna "Competição"**, apliquei filtro para **remover os amistosos de clubes (ADC)**.
- Na **coluna "Home Team"**:
  - Apliquei filtro por **condição** para remover os jogos que **ainda não aconteceram**, mas já têm horário definido (`:`).
  - Apliquei filtro por **valor** para remover os jogos com o símbolo `-`, que representam partidas com data, mas **sem horário confirmado**.

---

### 2. Limpeza de Colunas e Criação de Novas

- **Apaguei as colunas G e H**, que não seriam utilizadas.
- Criei novas colunas com os seguintes nomes:
  - **H:** Time Avaliado
  - **I:** Gols Time Avaliado
  - **J:** Gols Time Desafiante
  - **K:** Time Desafiante

- Ao lado direito da antiga coluna "Home Team", adicionei duas colunas para **separar os gols de cada time**:
  - Usei a fórmula `=LEFT()` para capturar o número de gols do time da casa.
  - Usei a fórmula `=RIGHT()` para capturar o número de gols do time visitante.
- Copiei essas colunas e colei como **valores**, eliminando o vínculo com fórmulas.
- Apaguei a coluna original **"Home Team"**.

---

### 3. Organização e Classificação de Dados

- Na coluna **"Time Avaliado" (I)**, preenchi todas as linhas com o valor **"Atlético-MG"**.

---

### 4. Criação de Fórmulas Auxiliares

- **Coluna J – Gols Time Avaliado**
  ```excel
  =IF(I10=D10;E10;F10)
  ```
  Se o time avaliado for o mesmo da coluna D (mandante), pega os gols da coluna E, senão pega os da F.

- **Coluna K – Gols Time Desafiante**
  ```excel
  =IF(L11=D11;E11;F11)
  ```
  Mesmo princípio da fórmula anterior, porém aplicada à coluna "Time Desafiante".

- **Coluna L – Time Desafiante**
  ```excel
  =IF(D10<>I10;D10;G10)
  ```
  Se o mandante (coluna D) for diferente do time avaliado, ele é o desafiante. Senão, o desafiante é o visitante (coluna G).

---

### 5. Identificação de Vitórias

- **Coluna M – Vitória**
  ```excel
  =IF(J11>K11;"SIM";"NÃO")
  ```
  Verifica se o time avaliado fez mais gols do que o desafiante. Se sim, retorna **"SIM"**, caso contrário, **"NÃO"**.

- Apliquei um **filtro na coluna "Vitória"** para exibir apenas os jogos vencidos pelo time avaliado.
  > ⚠️ Nota: é esperado que alguns times desafiantes apareçam mais de uma vez.

---

## 📌 Observações Finais

- Este processo foi feito manualmente no Excel e registrado passo a passo para permitir **reprodutibilidade** e **transparência**.
- Ideal para quem deseja transformar dados brutos em insights prontos para análise.

---

📂 **Este log pode ser usado por outros analistas ou estudantes que queiram entender ou replicar o fluxo de tratamento de dados de partidas esportivas.**
