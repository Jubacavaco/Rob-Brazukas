import streamlit as st
import pandas as pd
import re
import requests
import matplotlib.pyplot as plt

# ==============================================================================
# CONFIGURAÇÕES DA PÁGINA
# ==============================================================================
st.set_page_config(page_title="Robô Brazukas - Painel Estatístico", layout="wide")

st.title("🚨 Painel de Controle - Robô Brazukas 🚨")
st.write("Insira as informações do jogo, configure o Telegram na barra lateral e clique em Dar Play.")

# 🧠 SISTEMA DE MEMÓRIA DE ESTADO (SESSION STATE)
if "play_executado" not in st.session_state:
    st.session_state.play_executado = False

if "resultado_selecionado" not in st.session_state:
    st.session_state.resultado_selecionado = "Nenhum"

# ==============================================================================
# PAINEL LATERAL / CONFIGURAÇÕES E TELEGRAM
# ==============================================================================
st.sidebar.header("🤖 CONFIGURAÇÃO DO TELEGRAM")
token_telegram = st.sidebar.text_input(
    "🔑 Token do Bot:", 
    value="8776214366:AAEQnGyhcEa6NQcYzyFAhtVDXKpQx5CoYT0", 
    type="password"
)
chat_id_telegram = st.sidebar.text_input(
    "📢 ID do Canal/Grupo:", 
    value="-1003925163611"
)

st.sidebar.markdown("---")
st.sidebar.header("📅 Informações Básicas")
campeonato = st.sidebar.text_input("🏆 Campeonato:", value="Brasileirão")
time_casa = st.sidebar.text_input("🆚 Time da Casa:", value="Cruzeiro")
time_visitante = st.sidebar.text_input("🆚 Time Visitante:", value="Fluminense")
horario_jogo = st.sidebar.text_input("⏰ Horário do Jogo:", value="16h00 (BR)")

st.sidebar.markdown("---")
st.sidebar.header("👑 Definição de Favorito")
escolha_favorito = st.sidebar.selectbox("Escolha o Favorito:", ["Casa", "Visitante", "Nenhum / Equilibrado"])

st.sidebar.markdown("---")
st.sidebar.header("📊 Odds Atuais")
odd_casa = st.sidebar.number_input("Odd Casa:", value=1.85, min_value=1.0, step=0.01)
odd_visitante = st.sidebar.number_input("Odd Visitante:", value=4.40, min_value=1.0, step=0.01)
odd_over_15_ft = st.sidebar.number_input("Odd Over 1.5 FT:", value=1.33, min_value=1.0, step=0.01)
odd_btts_sim = st.sidebar.number_input("Odd BTTS Sim:", value=1.90, min_value=1.0, step=0.01)
odd_over_25_ft = st.sidebar.number_input("Odd Over 2.5 FT:", value=2.05, min_value=1.0, step=0.01)

# ==============================================================================
# FUNÇÃO DE ENVIO PARA O TELEGRAM
# ==============================================================================
def enviar_mensagem_telegram(texto_da_mensagem):
    url = f"https://api.telegram.org/bot{token_telegram}/sendMessage"
    dados = {
        "chat_id": chat_id_telegram,
        "text": texto_da_mensagem,
        "parse_mode": "Markdown"
    }
    try:
        resposta = requests.post(url, data=dados)
        return resposta.status_code == 200
    except Exception as e:
        st.sidebar.error(f"Erro de rede ao enviar: {e}")
        return False

# ==============================================================================
# CORPO PRINCIPAL - DADOS ESTATÍSTICOS
# ==============================================================================
st.subheader("📋 Dados Estatísticos do Site")

# Exemplo textual padrão passado em uma única linha contínua para evitar quebras de string do Python
texto_padrao = "28.05.26 LIB Cruzeiro Barcelona 4 0 V 24.05.26 SRA Cruzeiro Chapecoense 2 1 V 19.05.26 LIB Boca Juniors Cruzeiro 1 1 E 16.05.26 SRA Palmeiras Cruzeiro 1 1 E 12.05.26 COP Cruzeiro Goiás 1 0 V Mostrar mais jogos Últimos jogos: Fluminense 27.05.26 LIB Fluminense La Guaira 3 1 V 23.05.26 SRA Mirassol Fluminense 1 0 D 19.05.26 LIB Fluminense Bolivar 2 1 V 16.05.26 SRA Fluminense São Paulo 2 1 V 12.05.26 COP Fluminense Operário 2 1 V Mostrar mais jogos Confrontos diretos 09.11.25 SRA Cruzeiro Fluminense 0 0 17.07.25 SRA Fluminense Cruzeiro 0 2 03.10.24 SRA Fluminense Cruzeiro 1 0 19.06.24 SRA Cruzeiro Fluminense 2 0 20.09.23 SRA Fluminense Cruzeiro 1 0 10.05.23 SRA Cruzeiro Fluminense 0 2 12.07.22 COP Cruzeiro Fluminense 0 3 23.06.22 COP Fluminense Cruzeiro 2 1 09.10.19 SRA Cruzeiro Fluminense 0 0 05.06.19 COP Cruzeiro Fluminense 3 2 2 2"

lista_de_jogos_do_site = st.text_area(
    "Cole o texto bruto de histórico de jogos aqui:",
    value=texto_padrao,
    height=120
)

st.markdown("### 🛠️ Execução do Motor Matemático")
botao_play = st.button("▶️ EXECUTAR ANÁLISE E ENVIAR SINAL (DAR PLAY)", type="primary", use_container_width=True)

# 🧠 MOTOR DE LEITURA TEXTUAL (REGEX)
def extrair_dados_estatisticos(texto_bruto):
    texto_limpo = " ".join(texto_bruto.split())
    bloco_casa_match = re.search(r"(.*?)(?:Últimos jogos:|Únlimos jogos:)", texto_limpo, re.IGNORECASE)
    bloco_vis_match = re.search(r"(?:Últimos jogos:|Únlimos jogos:)(.*?)(?:Confrontos diretos)", texto_limpo, re.IGNORECASE)
    bloco_h2h_match = re.search(r"(?:Confrontos diretos)(.*)", texto_limpo, re.IGNORECASE)

    if not bloco_casa_match or not bloco_vis_match or not bloco_h2h_match:
        return None

    gols_casa = [int(n) for n in re.findall(r"\b\d\b", bloco_casa_match.group(1))]
    gols_vis = [int(n) for n in re.findall(r"\b\d\b", bloco_vis_match.group(1))]
    gols_h2h = [int(n) for n in re.findall(r"\b\d\b", bloco_h2h_match.group(1))]

    if len(gols_casa) < 10 or len(gols_vis) < 10 or len(gols_h2h) < 2:
        return None

    g_casa_p, g_casa_s = gols_casa[0:10:2], gols_casa[1:10:2]
    g_vis_p, g_vis_s = gols_vis[0:10:2], gols_vis[1:10:2]
    h2h_1, h2h_2 = gols_h2h[0::2], gols_h2h[1::2]

    tamanho_limite = min(len(h2h_1), len(h2h_2))
    return g_casa_p[:5], g_casa_s[:5], g_vis_p[:5], g_vis_s[:5], h2h_1[:tamanho_limite], h2h_2[:tamanho_limite]

# Guardar estado quando clica em Play
if botao_play:
    st.session_state.play_executado = True
    st.session_state.mensagens_enviadas_telegram = False

# Só roda se o Play estiver ativo
if st.session_state.play_executado:

    dados_finais = extrair_dados_estatisticos(lista_de_jogos_do_site)

    if dados_finais is None:
        st.error("🚨 ERRO CRÍTICO: O formato do texto estatístico colado não pôde ser lido.")
    else:
        g_casa_p, g_casa_s, g_vis_p, g_vis_s, h2h_1, h2h_2 = dados_finais
        
        # DataFrames de Cálculo
        df_casa = pd.DataFrame({"GM": g_casa_p, "GS": g_casa_s})
        df_vis = pd.DataFrame({"GM": g_vis_p, "GS": g_vis_s})
        df_h2h = pd.DataFrame({"T1": h2h_1, "T2": h2h_2})

        for df in [df_casa, df_vis]:
            df["TOTAL"] = df["GM"] + df["GS"]
            df["O15"] = df["TOTAL"] > 1.5
            df["O25"] = df["TOTAL"] > 2.5
            df["BTTS"] = (df["GM"] > 0) & (df["GS"] > 0)

        df_h2h["TOTAL"] = df_h2h["T1"] + df_h2h["T2"]
        df_h2h["O15"] = df_h2h["TOTAL"] > 1.5
        df_h2h["O25"] = df_h2h["TOTAL"] > 2.5
        df_h2h["BTTS"] = (df_h2h["T1"] > 0) & (df_h2h["T2"] > 0)

        # Probabilidades
        p_o15_lista = (((df_casa["O15"].mean() + df_vis["O15"].mean()) / 2 + df_h2h["O15"].mean()) / 2) * 100
        p_o25_lista = (((df_casa["O25"].mean() + df_vis["O25"].mean()) / 2 + df_h2h["O25"].mean()) / 2) * 100
        p_btts_lista = (((df_casa["BTTS"].mean() + df_vis["BTTS"].mean()) / 2 + df_h2h["BTTS"].mean()) / 2) * 100

        empates = (df_h2h["T1"] == df_h2h["T2"]).sum()
        total_h2h = len(df_h2h)
        prob_ltd_lista = ((total_h2h - empates) / total_h2h) * 100

        p_o15_odd = (1 / odd_over_15_ft) * 100
        p_o25_odd = (1 / odd_over_25_ft) * 100
        p_btts_odd = (1 / odd_btts_sim) * 100

        calc_odd_favorito = odd_casa if odd_casa <= odd_visitante else odd_visitante
        calc_odd_zebra = odd_visitante if odd_casa <= odd_visitante else odd_casa
        p_ltd_odd = ((1 / calc_odd_favorito) + (1 / calc_odd_zebra)) * 100
        if p_ltd_odd > 100: p_ltd_odd = 99

        p_o15 = (p_o15_lista + p_o15_odd) / 2
        p_o25 = (p_o25_lista + p_o25_odd) / 2
        p_btts = (p_btts_lista + p_btts_odd) / 2
        prob_ltd = (prob_ltd_lista + p_ltd_odd) / 2

        # Gráfico e Métricas
        st.markdown("---")
        col_grafico, col_metricas = st.columns([3, 2])
        
        with col_grafico:
            fig, ax = plt.subplots(figsize=(7, 3.5))
            mercados = ["Over 1.5 FT", "Over 2.5 FT", "BTTS SIM", "LTD"]
            porcentagens = [p_o15, p_o25, p_btts, prob_ltd]
            paleta_cores = ["#3498db", "#34495e", "#2ecc71", "#f1c40f"]
            barras = ax.bar(mercados, porcentagens, color=paleta_cores, edgecolor="black", width=0.5)
            ax.set_ylabel("Probabilidade (%)", fontsize=9, fontweight="bold")
            ax.set_ylim(0, 115)
            for barra in barras:
                altura = barra.get_height()
                ax.text(barra.get_x() + barra.get_width() / 2.0, altura + 2, f"{altura:.1f}%", ha="center", va="bottom", fontweight="bold", fontsize=8)
            ax.grid(axis="y", linestyle="--", alpha=0.5)
            st.pyplot(fig)

        with col_metricas:
            st.markdown("### 📈 Índices de Assertividade")
            st.metric("📊 Over 1.5 FT", f"{p_o15:.1f}%")
            st.metric("📊 Over 2.5 FT", f"{p_o25:.1f}%")
            st.metric("📊 BTTS SIM", f"{p_btts:.1f}%")
            st.metric("📊 Lay The Draw (LTD)", f"{prob_ltd:.1f}%")

        # ==============================================================================
        # CONTROLE DE RESULTADOS (GREEN, RED, PUSH)
        # ==============================================================================
        st.markdown("---")
        st.subheader("🎯 Controle e Monitoramento de Resultados")
        
        c_btn1, c_btn2, c_btn3, c_btn4 = st.columns(4)
        if c_btn1.button("🟢 Confirmar GREEN", use_container_width=True):
            st.session_state.resultado_selecionado = "Green"
        if c_btn2.button("🔴 Confirmar RED", use_container_width=True):
            st.session_state.resultado_selecionado = "Red"
        if c_btn3.button("🟡 Confirmar REEMBOLSO / PUSH", use_container_width=True):
            st.session_state.resultado_selecionado = "Push"
        if c_btn4.button("⚪ Resetar / Limpar", use_container_width=True):
            st.session_state.resultado_selecionado = "Nenhum"
            st.session_state.play_executado = False

        selo = ""
        if st.session_state.resultado_selecionado == "Green":
            selo = "\n\n✅✅ *GREEN!!* ✅✅"
            st.success("Operação salva como GREEN!")
        elif st.session_state.resultado_selecionado == "Red":
            selo = "\n\n❌❌ *RED!* ❌❌"
            st.error("Operação salva como RED!")
        elif st.session_state.resultado_selecionado == "Push":
            selo = "\n\n🔄🔄 *REEMBOLSO / PUSH* 🔄🔄"
            st.warning("Operação salva como REEMBOLSO!")

        # ==============================================================================
        # MONTAGEM DOS ALERTAS AUTOMÁTICOS
        # ==============================================================================
        st.markdown("---")
        st.subheader("📋 Mensagens Geradas")

        texto_favorito = f"Casa ({time_casa})" if escolha_favorito == "Casa" else (f"Visitante ({time_visitante})" if escolha_favorito == "Visitante" else "Nenhum / Jogo Equilibrado")
        
        lista_de_mensagens_rodada = []

        if p_o25 >= 65:
            lista_de_mensagens_rodada.append(f"🚨 *Alerta de Entrada* 🚨\n\n🏆 *Campeonato:* {campeonato}\n🆚 *Jogo:* {time_casa} x {time_visitante}\n🎯 *Mercado:* Over Gols\n💥 *Prognóstico:* Over 2.5 FT\n⏰ *Horário:* {horario_jogo}\n\n📌 Entrada recomendada antes do início!\n\n⚠️ Aposte com responsabilidade.{selo}")
        elif p_o15 >= 75:
            lista_de_mensagens_rodada.append(f"🚨 *Alerta de Entrada* 🚨\n\n🏆 *Campeonato:* {campeonato}\n🆚 *Jogo:* {time_casa} x {time_visitante}\n🎯 *Mercado:* Over Gols\n💥 *Prognóstico:* Over 1.5 FT\n⏰ *Horário:* {horario_jogo}\n\n📌 Entrada recomendada antes do início!\n\n⚠️ Aposte com responsabilidade.{selo}")

        if p_btts >= 55:
            lista_de_mensagens_rodada.append(f"🚨 *Alerta de Entrada* 🚨\n\n🏆 *Campeonato:* {campeonato}\n🆚 *Jogo:* {time_casa} x {time
