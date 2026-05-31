import streamlit as st
import requests

# Configuração da página
st.set_page_config(page_title="Robô Brazukas", layout="wide")
st.title("🚨 Painel de Controle - Robô Brazukas 🚨")

# --- ESTADO DA SESSÃO ---
if "executado" not in st.session_state: st.session_state.executado = False
if "res" not in st.session_state: st.session_state.res = "Nenhum"

# --- SIDEBAR: Configuração ---
st.sidebar.header("🤖 CONFIGURAÇÃO")
token = st.sidebar.text_input("🔑 Token do Bot:", type="password")
chat_id = st.sidebar.text_input("📢 ID do Canal (Oculto):", type="password")
st.sidebar.markdown("---")

st.sidebar.header("📅 DADOS DO JOGO")
campeonato = st.sidebar.text_input("🏆 Campeonato:", "Brasileirão")
time_casa = st.sidebar.text_input("🆚 Time Casa:", "Cruzeiro")
time_visitante = st.sidebar.text_input("🆚 Time Visitante:", "Fluminense")
horario = st.sidebar.text_input("⏰ Horário:", "16h00")
favorito = st.sidebar.selectbox("👑 Favorito:", ["Nenhum / Equilibrado", "Casa", "Visitante"])

# --- CORPO: Entrada de dados ---
st.subheader("📋 Dados Estatísticos")
lista_jogos = st.text_area("Cole o texto bruto de histórico aqui:", height=150, key="caixa_texto")

# --- LÓGICA DE CÁLCULO (Simulação das apostas recomendadas) ---
# Aqui você pode definir os seus critérios de probabilidade
recomenda_o25 = st.checkbox("Recomendar Over 2.5 FT?")
recomenda_btts = st.checkbox("Recomendar BTTS?")

# Botão de Ação
if st.button("▶️ EXECUTAR ANÁLISE", type="primary"):
    if st.session_state.caixa_texto:
        st.session_state.executado = True
    else:
        st.warning("Por favor, cole os dados na caixa de texto primeiro!")

# --- RESULTADOS ---
if st.session_state.executado:
    st.markdown("---")
    
    # Monta a parte da recomendação baseada nos cálculos
    apostas = []
    if recomenda_o25: apostas.append("Over 2.5 FT")
    if recomenda_btts: apostas.append("Ambas Marcam (BTTS)")
    
    texto_apostas = " e ".join(apostas) if apostas else "Nenhuma entrada definida"
    
    # Controle de Resultados
    st.subheader("🎯 Controle de Resultados")
    col1, col2, col3, col4 = st.columns(4)
    if col1.button("🟢 Confirmar Green"): st.session_state.res = "Green"
    if col2.button("🔴 Confirmar Red"): st.session_state.res = "Red"
    if col3.button("🟡 Confirmar Push"): st.session_state.res = "Push"
    if col4.button("⚪ Resetar Tudo"): st.session_state.executado = False; st.session_state.res = "Nenhum"; st.rerun()
    
    selo = f"\n\n👉 *Resultado:* {st.session_state.res}" if st.session_state.res != "Nenhum" else ""
    
    # MENSAGEM FINAL (Sem o favorito, apenas a aposta recomendada)
    msg = (f"🚨 *Alerta de Entrada* 🚨\n\n"
           f"🏆 *Campeonato:* {campeonato}\n"
           f"🆚 *Jogo:* {time_casa} x {time_visitante}\n"
           f"💰 *Aposta Recomendada:* {texto_apostas}\n"
           f"⏰ *Horário:* {horario}\n"
           f"{selo}")
    
    st.code(msg)
    
    # Botão de envio
    if st.button("🚀 ENVIAR PARA TELEGRAM"):
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}
        try:
            requests.post(url, data=payload)
            st.success("Sinal enviado!")
        except Exception as e:
            st.error(f"Erro: {e}")
