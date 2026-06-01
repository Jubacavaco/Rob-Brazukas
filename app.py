import streamlit as st
import requests
import re

st.set_page_config(layout="wide")
st.title("🤖 Sistema Brazukas Top Tisp")

# Sidebar para credenciais
token = st.sidebar.text_input("Token Telegram", type="password")
chat_id = st.sidebar.text_input("ID Canal", type="password")

def calcular_probabilidade(texto):
    texto_limpo = re.sub(r'\d{2}\.\d{2}\.\d{2}', '', texto)
    numeros = re.findall(r'\b[0-9]\b', texto_limpo)
    gols = [int(n) for n in numeros]
    if len(gols) < 2: return 0
    media = sum(gols) / len(gols)
    return min(media * 65, 100)

def renderizar_bloco(titulo):
    st.subheader(f"🏟️ {titulo}")
    
    # CAMPOS DE INPUT
    camp = st.text_input(f"Campeonato ({titulo})", key=f"c_{titulo}")
    casa = st.text_input(f"Casa ({titulo})", key=f"ca_{titulo}")
    vis = st.text_input(f"Visitante ({titulo})", key=f"v_{titulo}")
    hora = st.text_input(f"Horário ({titulo})", key=f"h_{titulo}")
    lista = st.text_area(f"Lista de jogos ({titulo})", key=f"l_{titulo}")
    
    # ANÁLISE
    if st.button(f"Analisar {titulo}", key=f"an_{titulo}"):
        p = calcular_probabilidade(lista)
        st.session_state[f"prob_{titulo}"] = p
        # Regras automáticas sugeridas
        st.session_state[f"conf_{titulo}"] = round(p, 1)
        st.session_state[f"stake_{titulo}"] = "1.0%" if p < 70 else "2.0%"
        st.rerun()
    
    # RESULTADOS
    if f"prob_{titulo}" in st.session_state:
        p = st.session_state[f"prob_{titulo}"]
        
        st.write("📊 **Acompanhamento Visual:**")
        st.write(f"Over 1.5 FT ({min(p+5, 100):.1f}%)"); st.progress(min((p+5)/100, 1.0))
        st.write(f"Over 2.5 FT ({min(p, 100):.1f}%)"); st.progress(min(p/100, 1.0))
        st.write(f"Ambas Marcam ({max(0, p-10):.1f}%)"); st.progress(max(0, p-10)/100)
        st.write(f"LTD ({max(0, 100-p):.1f}%)"); st.progress(max(0, 100-p)/100)
        
        # CAMPOS EDITÁVEIS
        col_a, col_b = st.columns(2)
        conf = col_a.text_input("Confiança (%)", value=str(st.session_state.get(f"conf_{titulo}", "")), key=f"inp_conf_{titulo}")
        stake = col_b.text_input("Stake Recomendada", value=str(st.session_state.get(f"stake_{titulo}", "")), key=f"inp_stake_{titulo}")
        
        mercado = st.selectbox(f"Definir Mercado ({titulo})", ["Automático", "Over 1.5 FT", "Over 2.5 FT", "Ambas Marcam (BTTS)", "LTD"], key=f"sel_{titulo}")
        tipo = mercado if mercado != "Automático" else ("Over 1.5 FT" if p >= 70 else "LTD")
        
        st.write(f"🎯 Mercado: **{tipo}** | Confiança: **{conf}%** | Stake: **{stake}**")
        
        # MENSAGEM FINAL
        msg = f"🚨 *Alerta de Entrada* 🚨\n\n🏆 *Campeonato:* {camp}\n🆚 *Jogo:* {casa} x {vis}\n🎯 *Mercado:* {tipo}\n📈 *Confiança:* {conf}%\n💰 *Stake:* {stake}\n⏰ *Horário:* {hora}\n\n⚠️ Aposte com responsabilidade."
        
        st.info(msg)
        st.session_state[f"msg_{titulo}"] = msg
        
        if st.button(f"🚀 ENVIAR {titulo}", key=f"en_{titulo}"):
            payload = {"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}
            r = requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data=payload).json()
            if r.get("ok"): 
                st.session_state[f"id_{titulo}"] = r["result"]["message_id"]
                st.rerun()

    # CONTROLE
    if f"id_{titulo}" in st.session_state:
        st.write("---")
        c1, c2, c3 = st.columns(3)
        def editar_telegram(status):
            new_msg = st.session_state[f"msg_{titulo}"] + f"\n\n🔄 *Status:* {status}"
            requests.post(f"https://api.telegram.org/bot{token}/editMessageText", 
                          data={"chat_id": chat_id, "message_id": st.session_state[f"id_{titulo}"], "text": new_msg, "parse_mode": "Markdown"})
            st.success(f"Registrado: {status}")

        if c1.button("✅ GREEN", key=f"g_{titulo}"): editar_telegram("✅ GREEN!!")
        if c2.button("❌ RED", key=f"r_{titulo}"): editar_telegram("❌ RED!")
        if c3.button("🔄 DEV", key=f"d_{titulo}"): editar_telegram("🔄 DEVOLVIDA")

col1, col2 = st.columns(2)
with col1: renderizar_bloco("JOGO_A")
with col2: renderizar_bloco("JOGO_B")
