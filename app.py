import streamlit as st
import re
import requests
import os
import json
import pandas as pd
import matplotlib.pyplot as plt

# Configuração inicial da página Streamlit
st.set_page_config(page_title="Painel de Controle de Entradas", page_icon="🛠️", layout="centered")

st.title("🛠️ PAINEL DE CONTROLE DE ENTRADAS")
st.markdown("---")

# --- INTERFACE GRÁFICA (SUBSTITUINDO OS @PARAM DO COLAB) ---

st.subheader("📅 INFORMAÇÕES BÁSICAS DO JOGO")
Campeonato = st.text_input("Campeonato", value="Brasileirão")
Time_Casa = st.text_input("Time Casa", value="Cruzeiro")
Time_Visitante = st.text_input("Time Visitante", value="Fluminense")
Horario_Jogo = st.text_input("Horário do Jogo", value="16h00 (BR)")

st.markdown("---")
st.subheader("👑 DETERMINAR FAVORITO DO CONFRONTO")
Escolha_Favorito = st.selectbox("Escolha quem é o favorito ou se o jogo é equilibrado:", ["Casa", "Visitante", "Nenhum / Equilibrado"])

st.markdown("---")
st.subheader("📊 ODDS ATUAIS DO MERCADO")
col1, col2 = st.columns(2)
with col1:
    Odd_Casa = st.number_input("Odd Casa", value=1.85, format="%.2f")
    Odd_Over_15_FT = st.number_input("Odd Over 1.5 FT", value=1.33, format="%.2f")
    Odd_Over_25_FT = st.number_input("Odd Over 2.5 FT", value=2.05, format="%.2f")
with col2:
    Odd_Visitante = st.number_input("Odd Visitante", value=4.40, format="%.2f")
    Odd_BTTS_Sim = st.number_input("Odd BTTS Sim", value=1.90, format="%.2f")

st.markdown("---")
st.subheader("📋 DADOS ESTATÍSTICOS DO SITE")
texto_padrao_estatisticas = "28.05.26 LIB  Cruzeiro  Barcelona 4 0 V 24.05.26 SRA  Cruzeiro  Chapecoense 2 1 V 19.05.26 LIB  Boca Juniors  Cruzeiro 1 1 E 16.05.26 SRA  Palmeiras  Cruzeiro 1 1 E 12.05.26 COP  Cruzeiro  Goiás 1 0 V  Mostrar mais jogos Últimos jogos: Fluminense 27.05.26 LIB  Fluminense  La Guaira 3 1 V 23.05.26 SRA  Mirassol  Fluminense 1 0 D 19.05.26 LIB  Fluminense  Bolivar 2 1 V 16.05.26 SRA  Fluminense  São Paulo 2 1 V 12.05.26 COP  Fluminense  Operário 2 1 V  Mostrar mais jogos Confrontos diretos 09.11.25 SRA  Cruzeiro  Fluminense 0 0 17.07.25 SRA  Fluminense  Cruzeiro 0 2 03.10.24 SRA  Fluminense  Cruzeiro 1 0 19.06.24 SRA  Cruzeiro  Fluminense 2 0 20.09.23 SRA  Fluminense  Cruzeiro 1 0 10.05.23 SRA  Cruzeiro  Fluminense 0 2 12.07.22 COP  Cruzeiro  Fluminense 0 3 23.06.22 COP  Fluminense  Cruzeiro 2 1 09.10.19 SRA  Cruzeiro  Fluminense 0 0 05.06.19 COP  Cruzeiro  Fluminense 3 2 2 2"
Lista_de_Jogos_do_Site = st.text_area("Cole os dados estatísticos aqui:", value=texto_padrao_estatisticas, height=150)

st.markdown("---")
st.subheader("🎯 ATUALIZAÇÃO DO RESULTADO")
Resultado_Aposta = st.selectbox("Resultado da Aposta (Selecione após o fim do jogo):", ["Nenhum", "Green", "Red", "Push"])

st.markdown("---")

# --- LÓGICA DO SEU CÓDIGO ORIGINAL ---

# Define textualmente o favorito com base na escolha efetuada no painel
if Escolha_Favorito == "Casa":
    Texto_Favorito = f"Casa ({Time_Casa})"
elif Escolha_Favorito == "Visitante":
    Texto_Favorito = f"Visitante ({Time_Visitante})"
else:
    Texto_Favorito = "Nenhum / Jogo Equilibrado"

# Lógica automática para definir a Odd do Favorito e da Zebra para o cálculo do LTD
if Odd_Casa <= Odd_Visitante:
    calc_odd_favorito = Odd_Casa
    calc_odd_zebra = Odd_Visitante
else:
    calc_odd_favorito = Odd_Visitante
    calc_odd_zebra = Odd_Casa

# Arquivos locais de controle de estado
ESTADO_FILE = "estado_fluxo.txt"
IDS_FILE = "mensagens_enviadas.json"

# Carrega o estado atual (se é envio de sinal ou atualização de resultado)
if os.path.exists(ESTADO_FILE):
    with open(ESTADO_FILE, "r") as f:
        passo_atual = f.read().strip()
else:
    passo_atual = "SINAL"

# Mostrar o status do fluxo atual na tela de forma amigável
if passo_atual == "SINAL":
    st.info("🔄 Status Atual: Pronto para gerar e enviar novo **SINAL**.")
else:
    st.warning("🔄 Status Atual: Sinal já enviado. Aguardando processamento de **RESULTADO**.")

# 📤 FUNÇÃO TRANSMISSÃO TELEGRAM VIA ROTA LIMPA
def disparar_mensagem_final_com_rota_limpa(texto_da_mensagem):
    protocolo_seguro = "https://"
    subdominio_api = "api.telegram.org"
    token_atual = "8776214366:AAEQnGyhcEa6NQcYzyFAhtVDXKpQx5CoYT0"
    chat_pessoal_id = "-1003925163611"

    URL_REAL_DO_TELEGRAM = f"{protocolo_seguro}{subdominio_api}/bot{token_atual}/sendMessage"
    DADOS_DA_REQUISICAO = {
        "chat_id": chat_pessoal_id,
        "text": texto_da_mensagem,
        "parse_mode": "Markdown"
    }

    try:
        servico_post = requests.post(URL_REAL_DO_TELEGRAM, data=DADOS_DA_REQUISICAO)
        if servico_post.status_code == 200:
            resposta_json = servico_post.json()
            return resposta_json.get("result", {}).get("message_id")
        else:
            st.error(f"❌ FALHA NO SERVIDOR TELEGRAM: {servico_post.status_code} - {servico_post.text}")
            return None
    except Exception as erro_fatal_de_rede:
        st.error(f"❌ ERRO DE REDE DETECTADO: {erro_fatal_de_rede}")
        return None

# 🔄 FUNÇÃO EDITAR MENSAGEM DO TELEGRAM
def editar_mensagem_telegram(message_id, novo_texto):
    protocolo_seguro = "https://"
    subdominio_api = "api.telegram.org"
    token_atual = "8776214366:AAEQnGyhcEa6NQcYzyFAhtVDXKpQx5CoYT0"
    chat_pessoal_id = "-1003925163611"

    URL_EDIT_TELEGRAM = f"{protocolo_seguro}{subdominio_api}/bot{token_atual}/editMessageText"
    DADOS_DA_REQUISICAO = {
        "chat_id": chat_pessoal_id,
        "message_id": message_id,
        "text": novo_texto,
        "parse_mode": "Markdown"
    }

    try:
        servico_post = requests.post(URL_EDIT_TELEGRAM, data=DADOS_DA_REQUISICAO)
        if servico_post.status_code == 200:
            st.success(f"✅ MENSAGEM ID {message_id} EDITADA COM SUCESSO NO TELEGRAM!")
        else:
            st.error(f"❌ FALHA AO EDITAR NO TELEGRAM: {servico_post.status_code} - {servico_post.text}")
    except Exception as e:
        st.error(f"❌ ERRO DE REDE AO EDITAR: {e}")

# 🧠 MOTOR DE LEITURA TEXTUAL
def extrair_dados_estatisticos(texto_bruto):
    texto_limpo = " ".join(texto_bruto.split())
    bloco_casa_match = re.search(r"(.*?)(?:Últimos jogos:|Únlimos
