import streamlit as st
import requests
import re

st.set_page_config(page_title="Robô Brazukas Dual", layout="wide")
st.title("🤖 Painel Brazukas - Gestão Visual e Independente")

# --- CONFIGURAÇÕES ---
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

def registrar_resultado(titulo, status, token, chat_id):
    if f"msg_id_{titulo}" in st.session_state:
        msg_id = st.session_state[f"msg_id_{titulo}"]
        txt = st.session_state[f"msg_txt_{titulo}"] + f"\n\n🔄 *Status:* {status}"
        requests.post(f"https://api.telegram.org/bot{token}/editMessageText", 
                      data={"chat_id": chat_id, "message_id": msg_id, "text": txt, "parse_mode": "Markdown"})
        st.success(f"Status {titulo} atualizado para: {status}")

# --- BLOCO PRINCIPAL ---
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
            st.session_state[f"prob_{titulo}"] = prob
            
            if prob >= 65: tipo = "Over 2.5 FT"
            elif prob >= 70: tipo = "Over 1.5 FT"
            elif prob >= 55: tipo = "BTTS"
            elif prob >= 51: tipo = "LTD"
            else: tipo = None

            if tipo:
                msg = f"🚨 *Alerta de Entrada* 🚨\n\n🏆 *Camp:* {camp}\n🆚 {casa} x {vis}\n🎯 *Mercado:* {tipo}\n⏰ *Horário:* {hora}\n\n⚠️ Aposte com responsabilidade."
                resp = requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                                    data={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}).json()
                if resp.get("ok"):
                    st.session_state[f"msg_id_{titulo}"] = resp["result"]["message_id"]
                    st.session_state[f"msg_txt_{titulo}"] = msg
                    st.success("Sinal enviado!")
            else:
                st.warning("Probabilidade abaixo do limite.")

    # --- GRÁFICOS ---
    if f"prob_{titulo}" in st.session_state:
        p = st.session_state[f"prob_{titulo}"]
        st.write(f"**Probabilidade Atual: {p:.1f}%**")
        st.caption("Gráfico de Potencial")
        st.progress(min(p/100, 1.0))

    # --- BOTÕES ---
    if f"msg_id_{titulo}" in st.session_state:
        c1, c2, c3 = st.columns(3)
        if c1.button("✅ GREEN", key=f"g_{titulo}"): registrar_resultado(titulo, "✅ GREEN!!", token, chat_id)
        if c2.button("❌ RED", key=f"r_{titulo}"): registrar_resultado(titulo, "❌ RED!", token, chat_id)
