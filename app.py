import streamlit as st
import requests
import re

st.set_page_config(page_title="Robô Brazukas Dual", layout="wide")
st.title("🤖 Painel Brazukas - Gestão Dual Completa")

# --- CONFIGURAÇÕES ---
st.sidebar.header("⚙️ Configurações Telegram")
token = st.sidebar.text_input("🔑 Token Telegram", type="password")
chat_id = st.sidebar.text_input("📢 ID do Canal", type="password")

# --- FUNÇÕES ---
def calcular_probabilidade(texto):
    numeros = re.findall(r'\d+', texto)
    gols = [int(n) for n in numeros if int(n) <= 10]
    if len(gols) < 2: return 0
    media = sum(gols) / len(gols)
    return min(media * 35, 100)

def gerar_mensagem(tipo, camp, casa, vis, hora):
    return f"🚨 *Alerta de Entrada* 🚨\n\n🏆 *Camp:* {camp}\n🆚 {casa} x {vis}\n🎯 *Mercado:* {tipo}\n⏰ *Horário:* {hora}\n\n⚠️ Aposte com responsabilidade."

# --- BLOCO DE JOGO ---
def renderizar_bloco(titulo):
    st.subheader(f"🏟️ {titulo}")
    # Usamos um container para manter tudo organizado
    with st.container():
        camp = st.text_input(f"Campeonato ({titulo})", key=f"camp_{titulo}")
        casa = st.text_input(f"Casa ({titulo})", key=f"casa_{titulo}")
        vis = st.text_input(f"Visitante ({titulo})", key=f"vis_{titulo}")
        hora = st.text_input(f"Horário ({titulo})", key=f"hora_{titulo}")
        lista = st.text_area(f"Lista de Jogos ({titulo})", key=f"lista_{titulo}")
        
        if st.button(f"Analisar e Enviar {titulo}", key=f"btn_{titulo}"):
            prob = calcular_probabilidade(lista)
            st.write(f"📈 **Probabilidade:** {prob:.1f}%")
            
            # Regras
            tipo = None
            if prob >= 65: tipo = "Over 2.5 FT"
            elif prob >= 70: tipo = "Over 1.5 FT"
            elif prob >= 55: tipo = "BTTS"
            elif prob >= 51: tipo = "LTD"
            
            if tipo:
                msg = gerar_mensagem(tipo, camp, casa, vis, hora)
                if token and chat_id:
                    resp = requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                                       data={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}).json()
                    if resp.get("ok"):
                        st.session_state[f"id_{titulo}"] = resp["result"]["message_id"]
                        st.session_state[f"msg_{titulo}"] = msg
                        st.success("Sinal enviado com sucesso!")
                    else:
                        st.error("Erro ao enviar ao Telegram.")
                else:
                    st.warning("Configure o Token e
