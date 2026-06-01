import streamlit as st
import requests
import re

# Configuração da página
st.set_page_config(page_title="Sistema Brazukas", layout="wide")

# Título Estilizado
st.markdown("<h1 style='text-align: center; color: #2E86C1;'>🤖 Sistema Brazukas Top Tisp</h1>", unsafe_allow_html=True)
st.markdown("---")

# Sidebar
st.sidebar.header("⚙️ Configurações")
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
    with st.container(border=True):
        st.subheader(f"🏟️ {titulo}")
        
        # Organização em colunas para os inputs
        c1, c2 = st.columns(2)
        camp = c1.text_input(f"Campeonato", key=f"c_{titulo}")
        hora = c2.text_input(f"Horário", key=f"h_{titulo}")
        
        casa = st.text_input(f"Time Casa", key=f"ca_{titulo}")
        vis = st.text_input(f"Time Visitante", key=f"v_{titulo}")
        placar = st.text_input(f"Placar Final (Preencher após jogo)", key=f"p_{titulo}")
        lista = st.text_area(f"Lista de jogos", key=f"l_{titulo}", height=100)
        
        if st.button(f"Analisar {titulo}", key=f"an_{titulo}", use_container_width=True):
            p = calcular_probabilidade(lista)
            st.session_state[f"prob_{titulo}"] = p
            st.session_state[f"val_prob_{titulo}"] = round(p, 1)
            st.rerun()
        
        if f"prob_{titulo}" in st.session_state:
            p = st.session_state[f"prob_{titulo}"]
            st.markdown("---")
            st.write("📊 **Probabilidades:**")
            
            # Gráficos coloridos
            cols_g = st.columns(2)
            cols_g[0].write(f"Over 1.5: {min(p+5, 100):.0f}%"); cols_g[0].progress(min((p+5)/100, 1.0))
            cols_g[1].write(f"Over 2.5: {min(p, 100):.0f}%"); cols_g[1].progress(min(p/100, 1.0))
            
            prob_val = st.text_input("Ajustar Probabilidade (%)", value=str(st.session_state.get(f"val_prob_{titulo}", "")), key=f"inp_prob_{titulo}")
            mercado = st.selectbox(f"Definir Mercado", ["Automático", "Over 1.5 FT", "Over 2.5 FT", "Ambas Marcam (BTTS)", "LTD"], key=f"sel_{titulo}")
            tipo = mercado if mercado != "Automático" else ("Over 1.5 FT" if p >= 70 else "LTD")
            
            msg = f"🚨 *Alerta de Entrada* 🚨\n\n🏆 *Campeonato:* {camp}\n🆚 *Jogo:* {casa} x {vis}\n🎯 *Mercado:* {tipo}\n📈 *Probabilidade:* {prob_val}%\n⏰ *Horário:* {hora}\n\n⚠️ Aposte com responsabilidade."
            
            st.info(msg)
            st.session_state[f"msg_{titulo}"] = msg
            
            if st.button(f"🚀 ENVIAR PARA TELEGRAM", key=f"en_{titulo}", type="primary", use_container_width=True):
                payload = {"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}
                r = requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data=payload).json()
                if r.get("ok"): 
                    st.session_state[f"id_{titulo}"] = r["result"]["message_id"]
                    st.rerun()

        # Botões de controle em destaque
        if f"id_{titulo}" in st.session_state:
            st.markdown("---")
            col_b1, col_b2, col_b3 = st.columns(3)
            def editar_telegram(status):
                new_msg = st.session_state[f"msg_{titulo}"] + f"\n⚽ *Placar Final:* {placar}\n\n🔄 *Status:* {status}"
                requests.post(f"https://api.telegram.org/bot{token}/editMessageText", 
                              data={"chat_id": chat_id, "message_id": st.session_state[f"id_{titulo}"], "text": new_msg, "parse_mode": "Markdown"})
                st.success(f"Status atualizado!")

            if col_b1.button("✅ GREEN", key=f"g_{titulo}"): editar_telegram("✅ GREEN!!")
            if col_b2.button("❌ RED", key=f"r_{titulo}"): editar_telegram("❌ RED!")
            if col_b3.button("🔄 DEV", key=f"d_{titulo}"): editar_telegram("🔄 DEVOLVIDA")

# Layout principal
col1, col2 = st.columns(2)
with col1: renderizar_bloco("JOGO_A")
with col2: renderizar_bloco("JOGO_B")
