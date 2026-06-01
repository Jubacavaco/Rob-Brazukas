import streamlit as st
import requests
import re

st.set_page_config(page_title="Robô Brazukas Dual", layout="wide")
st.title("🤖 Painel Brazukas - Gestão Dual Independente")

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

def get_msg_completa(tipo, camp, casa, vis, hora):
    base = f"🚨 *Alerta de Entrada* 🚨\n\n🏆 *Campeonato:* {camp}\n🆚 *Jogo:* {casa} x {vis}\n"
    rodape = "\n\n⚠️ Aposte com responsabilidade. Não há garantias de lucro."
    
    if tipo == "Over 2.5":
        corpo = f"🎯 *Mercado:* Over Gols\n💥 *Prognóstico:* 2.5 FT\n⏰ *Horário:* {hora}\n\n📌 Entrada recomendada (Probabilidade > 65%!)"
    elif tipo == "Over 1.5":
        corpo = f"🎯 *Mercado:* Over Gols\n💥 *Prognóstico:* 1.5 FT\n⏰ *Horário:* {hora}\n\n📌 Entrada recomendada (Probabilidade > 70%!)"
    elif tipo == "BTTS":
        corpo = f"🎯 *Mercado:* BTTS\n💥 *Prognóstico:* Ambas - SIM\n⏰ *Horário:* {hora}\n\n📌 Entrada recomendada (Probabilidade > 55%!)"
    else:
        corpo = f"🎯 *Mercado:* Match Odd´s\n💥 *Prognóstico:* Contra o Empate (LTD)\n⏰ *Horário:* {hora}\n\n📌 Entrada recomendada (Probabilidade > 51%!)"
    
    return base + corpo + rodape

# --- FUNÇÃO DE BLOCO INDEPENDENTE ---
def gerar_bloco_independente(titulo):
    st.subheader(f"🏟️ {titulo}")
    with st.form(key=f"form_{titulo}"):
        camp = st.text_input(f"Campeonato ({titulo})")
        casa = st.text_input(f"Time Casa ({titulo})")
        vis = st.text_input(f"Time Vis ({titulo})")
        hora = st.text_input(f"Horário ({titulo})")
        lista = st.text_area(f"Cole a lista de jogos para {titulo}:", height=100)
        
        submit_analise = st.form_submit_button("📊 Analisar e Enviar Sinal Completo")
        
        if submit_analise:
            if not token or not chat_id:
                st.error("Preencha o Token e ID na barra lateral!")
            elif not lista:
                st.warning("Cole a lista de jogos primeiro.")
            else:
                prob = calcular_probabilidade(lista)
                tipo = decidir_tipo(prob)
                
                if tipo:
                    msg = get_msg_completa(tipo, camp, casa, vis, hora)
                    payload = {"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}
                    resp = requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data=payload).json()
                    
                    if resp.get("ok"):
                        st.success(f"✅ Sinal {titulo} enviado! ({prob:.1f}%)")
                        st.info(msg)
                    else:
                        st.error("Erro ao enviar. Verifique o Token/ID.")
                else:
                    st.warning("Probabilidade abaixo do limite para envio.")

# --- LAYOUT DUAL ---
col1, col2 = st.columns(2)

with col1:
    gerar_bloco_independente("Jogo 01")

with col2:
    gerar_bloco_independente("Jogo 02")
