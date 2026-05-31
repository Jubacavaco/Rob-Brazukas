# @title 🛠️ PAINEL DE CONTROLE DE ENTRADAS { display-mode: "form" }

# @markdown ---
# @markdown ### 📅 INFORMAÇÕES BÁSICAS DO JOGO
Campeonato = "Brasileirão" 
Time_Casa = "Cruzeiro" 
Time_Visitante = "Fluminense" 
Horario_Jogo = "16h00 (BR)" 

# @markdown ---
# @markdown ### 👑 DETERMINAR FAVORITO DO CONFRONTO
Escolha_Favorito = "Casa" 

# @markdown ---
# @markdown ### 📊 ODDS ATUAIS DO MERCADO
Odd_Casa = 1.85 
Odd_Visitante = 4.40 
Odd_Over_15_FT = 1.33 
Odd_BTTS_Sim = 1.90 
Odd_Over_25_FT = 2.05 

# @markdown ---
# @markdown ### 📋 DADOS ESTATÍSTICOS DO SITE
Lista_de_Jogos_do_Site = "28.05.26 LIB  Cruzeiro  Barcelona 4 0 V 24.05.26 SRA  Cruzeiro  Chapecoense 2 1 V 19.05.26 LIB  Boca Juniors  Cruzeiro 1 1 E 16.05.26 SRA  Palmeiras  Cruzeiro 1 1 E 12.05.26 COP  Cruzeiro  Goiás 1 0 V  Mostrar mais jogos Últimos jogos: Fluminense 27.05.26 LIB  Fluminense  La Guaira 3 1 V 23.05.26 SRA  Mirassol  Fluminense 1 0 D 19.05.26 LIB  Fluminense  Bolivar 2 1 V 16.05.26 SRA  Fluminense  São Paulo 2 1 V 12.05.26 COP  Fluminense  Operário 2 1 V  Mostrar mais jogos Confrontos diretos 09.11.25 SRA  Cruzeiro  Fluminense 0 0 17.07.25 SRA  Fluminense  Cruzeiro 0 2 03.10.24 SRA  Fluminense  Cruzeiro 1 0 19.06.24 SRA  Cruzeiro  Fluminense 2 0 20.09.23 SRA  Fluminense  Cruzeiro 1 0 10.05.23 SRA  Cruzeiro  Fluminense 0 2 12.07.22 COP  Cruzeiro  Fluminense 0 3 23.06.22 COP  Fluminense  Cruzeiro 2 1 09.10.19 SRA  Cruzeiro  Fluminense 0 0 05.06.19 COP  Cruzeiro  Fluminense 3 2 2 2" 

# @markdown ---
# @markdown ### 🎯 ATUALIZAÇÃO DO RESULTADO
Resultado_Aposta = "Green" 

import re
import requests
import os
import json
import pandas as pd
import matplotlib.pyplot as plt

# Lógica de Favorito
if Escolha_Favorito == "Casa":
    Texto_Favorito = f"Casa ({Time_Casa})"
elif Escolha_Favorito == "Visitante":
    Texto_Favorito = f"Visitante ({Time_Visitante})"
else:
    Texto_Favorito = "Nenhum / Jogo Equilibrado"

if Odd_Casa <= Odd_Visitante:
    calc_odd_favorito = Odd_Casa
    calc_odd_zebra = Odd_Visitante
else:
    calc_odd_favorito = Odd_Visitante
    calc_odd_zebra = Odd
