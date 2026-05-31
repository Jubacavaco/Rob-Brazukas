import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# --- CONFIGURAÇÃO DA PÁGINA WEB ---
st.set_page_config(page_title="Painel de Análise Híbrida PRO", page_icon="⚽", layout="wide")

st.title("🏆 Painel Automatizado de Entradas de Futebol")
st.markdown("Busque dados diretamente da API-Football, calcule as probabilidades híbridas e envie para o Telegram com 1 clique.")

# --- SIDEBAR: CHAVES E AUTENTICAÇÕES ---
st.sidebar.header("🛠️ Configurações e Chaves")

# CHAVES E CREDENCIAIS JÁ EMUTIDAS NO CÓDIGO DO SITE
TOKEN_TELEGRAM_PADRAO = "8776214366:AAEQnGyhcEa6NQcYzyFAhtVDXKpQx5CoYT0"
CHAT_ID_TELEGRAM_PADRAO = "-1003925163611"
CHAVE_RAPIDAPI_PADRAO = "1210ab781emsh959d0c8e3852319p10afc7jsn083ac5956b5a"

token_telegram = st.sidebar.text_input("Token do Bot Telegram", value=TOKEN_TELEGRAM_PADRAO, type="password")
chat_telegram = st.sidebar.text_input("ID do Canal Telegram", value=CHAT_ID_TELEGRAM_PADRAO)
chave_rapidapi = st.sidebar.text_input("X-RapidAPI-Key (Chave API-Football)", value=CHAVE_RAPIDAPI_PADRAO, type="password")

# --- BLOCO 1: FORMULÁRIO DE ENTRADA DO JOGO ---
st.header("📅 Informações do Confronto & Preços do Mercado")

col1, col2, col3 = st.columns(3)
with col1:
    campeonato = st.text_input("Campeonato", "LaLiga 2")
    id_time_casa = st.number_input("ID Time Casa (na API)", min_value=1, value=541, help="Busque o ID do time na documentação da API ou use mecanismos de busca de ID.")
with col2:
    horario_jogo = st.text_input("Horário do Jogo", "16h00 (BR)")
    id_time_visitante = st.number_input("ID Time Visitante (na API)", min_value=1, value=532)
with col3:
    escolha_favorito = st.selectbox("Determinar Favorito", ["Casa", "Visitante", "Nenhum / Equilibrado"])

st.markdown("#### 📊 Odds Atuais da Casa de Apostas")
col_o1, col_o2, col_o3, col_o4, col_o5 = st.columns(5)
with col_o1:
    odd_casa = st.number_input("Odd Casa", min_value=1.01, value=1.95, step=0.01)
with col_o2:
    odd_visitante = st.number_input("Odd Visitante", min_value=1.01, value=3.60, step=0.01)
with col_o3:
    odd_o15 = st.number_input("Odd Over 1.5 FT", min_value=1.01, value=1.35, step=0.01)
with col_o4:
    odd_o25 = st.number_input("Odd Over 2.5 FT", min_value=1.01, value=2.10, step=0.01)
with col_o5:
    odd_btts = st.number_input("Odd BTTS Sim", min_value=1.01, value=1.85, step=0.01)

# --- FUNÇÃO DE ENVIO TELEGRAM ---
def enviar_telegram(texto):
    url = f"https://telegram.org{token_telegram}/sendMessage"
    payload = {"chat_id": chat_telegram, "text": texto, "parse_mode": "Markdown"}
    try:
        r = requests.post(url, json=payload)
        return r.status_code == 200
    except:
        return False

# --- BOTÃO DE DISPARO DA ANÁLISE ---
if st.button("🚀 Executar Análise Híbrida via API", type="primary"):
    if not chave_rapidapi:
        st.error("🚨 Por favor, insira uma chave válida da RapidAPI na barra lateral antes de continuar.")
    else:
        with st.spinner("Conectando aos servidores da API-Football e coletando histórico..."):
            # --- ACESSO DIRETO VIA API-FOOTBALL (H2H) ---
            url_api = "https://rapidapi.com"
            querystring = {"h2h": f"{id_time_casa}-{id_time_visitante}", "last": "10"}
            headers = {
                "X-RapidAPI-Host": "://rapidapi.com",
                "X-RapidAPI-Key": chave_rapidapi
            }
            
            try:
                response = requests.get(url_api, headers=headers, params=querystring)
                dados_api = response.json()
                
                if "response" not in dados_api or len(dados_api["response"]) == 0:
                    st.error("❌ Nenhum jogo encontrado para os IDs informados. Verifique se os IDs dos times estão corretos na API-Football.")
                else:
                    # Coleta os nomes reais gravados na API
                    nome_casa = dados_api["response"][0]["teams"]["home"]["name"]
                    nome_visitante = dados_api["response"][0]["teams"]["away"]["name"]
                    
                    # Processamento dos gols das partidas estruturadas da API
                    gols_total_confrontos = []
                    btts_confrontos = []
                    empates_contagem = 0
                    
                    for game in dados_api["response"]:
                        g_home = game["goals"]["home"]
                        g_away = game["goals"]["away"]
                        
                        if g_home is not None and g_away is not None:
                            total_gols = g_home + g_away
                            gols_total_confrontos.append(total_gols)
                            btts_confrontos.append(g_home > 0 and g_away > 0)
                            if g_home == g_away:
                                empates_contagem += 1
                    
                    total_jogos_validos = len(gols_total_confrontos)
                    
                    if total_jogos_validos == 0:
                        st.error("❌ Os dados coletados não possuem informações completas de gols.")
                    else:
                        # Cálculos Estatísticos Puros com base no JSON da API
                        p_o15_lista = (sum(1 for g in gols_total_confrontos if g > 1.5) / total_jogos_validos) * 100
                        p_o25_lista = (sum(1 for g in gols_total_confrontos if g > 2.5) / total_jogos_validos) * 100
                        p_btts_lista = (sum(1 for b in btts_confrontos if b) / total_jogos_validos) * 100
                        prob_ltd_lista = ((total_jogos_validos - empates_contagem) / total_jogos_validos) * 100
                        
                        # Cálculos de Probabilidades das Odds
                        p_o15_odd = (1 / odd_o15) * 100
                        p_o25_odd = (1 / odd_o25) * 100
                        p_btts_odd = (1 / odd_btts) * 100
                        
                        calc_odd_favorito = odd_casa if odd_casa <= odd_visitante else odd_visitante
                        calc_odd_zebra = odd_visitante if odd_casa <= odd_visitante else odd_casa
                        p_ltd_odd = ((1 / calc_odd_favorito) + (1 / calc_odd_zebra)) * 100
                        if p_ltd_odd > 100: p_ltd_odd = 99
                        
                        # Fusão Híbrida Final
                        p_o15 = (p_o15_lista + p_o15_odd) / 2
                        p_o25 = (p_o25_lista + p_o25_odd) / 2
                        p_btts = (p_btts_lista + p_btts_odd) / 2
                        prob_ltd = (prob_ltd_lista + p_ltd_odd) / 2
                        
                        # --- EXIBIÇÃO DE RESULTADOS NA TELA WEB ---
                        st.success(f"Análise Concluída com Sucesso para: {nome_casa} vs {nome_visitante}!")
                        
                        col_r1, col_r2 = st.columns(2)
                        
                        with col_r1:
                            st.subheader("📈 Probabilidades Híbridas Finais")
                            st.metric("Over 1.5 FT", f"{p_o15:.1f}%")
                            st.metric("Over 2.5 FT", f"{p_o25:.1f}%")
                            st.metric("Ambas Marcam (BTTS)", f"{p_btts:.1f}%")
                            st.metric("LTD (Contra o Empate)", f"{prob_ltd:.1f}%")
                        
                        with col_r2:
                            st.subheader("📊 Gráfico de Performance Real")
                            fig, ax = plt.subplots(figsize=(6, 4.2))
                            mercados = ["Over 1.5", "Over 2.5", "BTTS Sim", "LTD"]
                            valores = [p_o15, p_o25, p_btts, prob_ltd]
                            cores = ["#3498db", "#34495e", "#2ecc71", "#f1c40f"]
                            
                            bars = ax.bar(mercados, valores, color=cores, edgecolor="black", width=0.5)
                            ax.set_ylim(0, 110)
                            ax.set_ylabel("Percentual (%)")
                            
                            for bar in bars:
                                h = bar.get_height()
                                ax.text(bar.get_x() + bar.get_width()/2., h + 2, f"{h:.1f}%", ha="center", va="bottom", fontweight="bold")
                            
                            st.pyplot(fig)
                        
                        # --- VERIFICAÇÃO DE DIRETRIZES E DISPARO ---
                        st.header("⭐ Histórico de Alertas Gerados & Status de Transmissão")
                        
                        texto_favorito = f"Casa ({nome_casa})" if escolha_favorito == "Casa" else (f"Visitante ({nome_visitante})" if escolha_favorito == "Visitante" else "Nenhum / Equilibrado")
                        
                        alertas_gerados = 0
                        
                        if p_o25 >= 65:
                            msg = f"🚨 *Alerta de Entrada* 🚨\n\n🏆 *Campeonato:* {campeonato}\n🆚 *Jogo:* {nome_casa} x {nome_visitante}\n🎯 *Mercado:* Over Gols\n💥 *Prognóstico:* Over 2.5 FT\n⏰ *Horário:* {horario_jogo}\n\n📌 Entrada recomendada antes do início!\n\n⚠️ Aposte com responsabilidade."
                            st.text_area("🟢 Enviado ao Telegram (Over 2.5):", msg, height=150)
                            if enviar_telegram(msg): st.toast("Mensagem Over 2.5 enviada!")
                            alertas_gerados += 1
                        elif p_o15 >= 75:
                            msg = f"🚨 *Alerta de Entrada* 🚨\n\n🏆 *Campeonato:* {campeonato}\n🆚 *Jogo:* {nome_casa} x {nome_visitante}\n🎯 *Mercado:* Over Gols\n💥 *Prognóstico:* Over 1.5 FT\n⏰ *Horário:* {horario_jogo}\n\n📌 Entrada recomendada antes do início!\n\n⚠️ Aposte com responsabilidade."
                            st.text_area("🟢 Enviado ao Telegram (Over 1.5):", msg, height=150)
