import streamlit as st
import requests
import re

st.set_page_config(page_title="Robô Brazukas Dual", layout="wide")
st.title("🤖 Painel Brazukas - Gestão Dual Completa")

# --- CONFIGURAÇÕES NO SIDEBAR ---
st.sidebar.header("⚙️ Configurações Telegram")
token = st.sidebar.text_input("🔑 Token", type="password")
chat_id = st.sidebar.text_input("📢 ID Canal", type="password")

# --- FUNÇÕES ---
def calcular_probabilidade(texto):
    numeros = re.findall(r'\d+', texto)
    gols = [int(n) for n in numeros if int(n) <= 10]
    if len(gols) < 2: return 0
    media = sum(gols) / len(gols)
    return min(media * 35, 100)

def decidir_tipo(prob):
    if prob >= 65: return "Over 2.5"
    elif prob >= 70: return "Over 1.5"
    elif prob >= 55: return "BTTS"
    elif prob >= 51: return "LTD"
    return None

def get_msg(tipo, camp, casa, vis, hora):
    base = f"🚨 *Alerta de Entrada* 🚨\n\n🏆 *Campeonato:* {camp}\n🆚 *Jogo:* {casa} x {vis}\n"
    rodape = "\n\n⚠️ Aposte com responsabilidade."
    corpos = {
        "Over 2.5": "🎯 *Mercado:* Over Gols\n💥 *Prognóstico:* 2.5 FT\n⏰ *Horário:* " + hora,
        "Over 1.5": "🎯 *Mercado:* Over Gols\n💥 *Prognóstico:* 1.5 FT\n⏰ *Horário:* " + hora,
        "BTTS": "🎯 *Mercado:* BTTS\n💥 *Prognóstico:* Ambas - SIM\n⏰ *Horário:* " + hora,
        "LTD": "🎯 *Mercado:* Match Odd´s\n💥 *Prognóstico:* Contra o Empate (LTD)\n⏰ *Horário:* " + hora
    }
    return base + corpos.get(tipo, "Entrada Padrão") + rodape

# --- FUNÇÃO DO BLOCO COM BOTÕES ---
def gerar_bloco(titulo):
    st.subheader(f"🏟️ {titulo}")
    with st.form(key=f"form_{titulo}"):
        camp = st.text_input(f"Campeonato ({titulo})")
        casa = st.text_input(f"Time Casa ({titulo})")
        vis = st.text_input(f"Time Vis ({titulo})")
        hora = st.text_input(f"Horário ({titulo})")
        lista = st.text_area(f"Lista de jogos ({titulo}):", height=80)
        submit = st.form_submit_button("📊 Analisar e Enviar")

        if submit:
            prob = calcular_probabilidade(lista)
            tipo = decidir_tipo(prob)
            if tipo:
                msg = get_msg(tipo, camp, casa, vis, hora)
                resp = requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                                    data={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}).json()
                if resp.get("ok"):
                    st.session_state[f"msg_id_{titulo}"] = resp["result"]["message_id"]
                    st.session_state[f"msg_txt_{titulo}"] = msg
                    st.success(f"Sinal {titulo} enviado!")
                else:
                    st.error("Erro no envio! Verifique Token/ID.")
            else:
                st.warning("Probabilidade insuficiente.")

    # Botões de Resultado
    if f"msg_id_{titulo}" in st.session_state:
        st.write(f"--- Controle {titulo} ---")
        c1, c2, c3 = st.columns(3)
        def registrar(status):
            msg_id = st.session_state[f"msg_id_{titulo}"]
            txt = st.session_state[f"msg_txt_{titulo}"] + f"\n\n🔄 *Status:* {status}"
            requests.post(f"https://api.telegram.org/bot{token}/editMessageText", 
                          data={"chat_id": chat_id, "message_id": msg_id, "text": txt, "parse_mode": "Markdown"})
            st.success(f"Status atualizado: {status}")
        
        if c1.button("✅ GREEN", key=f"g_{titulo}"): registrar("✅ GREEN!!")
        if c2.button("❌ RED", key=f"r_{titulo}"): registrar("❌ RED!")
        if c3.button("🔄 DEV", key=f"d_{titulo}"): registrar("🔄 DEVOLVIDA")

# --- LAYOUT DUAL ---
col1, col2 = st.columns(2)
with col1: gerar_bloco("Jogo_1")
with col2: gerar_bloco("Jogo_2")
