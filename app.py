import streamlit as st
import requests
import re

# Configuração da página
st.set_page_config(layout="wide", page_title="Painel Brazukas")
st.title("🤖 Painel Brazukas - Gestão Total")

# Sidebar - Configurações Persistentes
with st.sidebar:
    st.header("⚙️ Configurações")
    st.session_state['token'] = st.text_input("Token Telegram", value=st.session_state.get('token', ''), type="password")
    st.session_state['chat_id'] = st.text_input("ID Canal", value=st.session_state.get('chat_id', ''), type="password")

def calcular_probabilidade(texto):
    numeros = re.findall(r'\d+', texto)
    gols = [int(n) for n in numeros if int(n) <= 10]
    if len(gols) < 2: return 0
    media = sum(gols) / len(gols)
    return min(media * 20, 100)

def renderizar_bloco(titulo):
    with st.container(border=True):
        st.subheader(f"🏟️ {titulo}")
        
        # Campos de entrada com persistência
        camp = st.text_input("Campeonato", value=st.session_state.get(f'c_{titulo}', ''), key=f"c_{titulo}")
        hora = st.text_input("Horário", value=st.session_state.get(f'h_{titulo}', ''), key=f"h_{titulo}")
        casa = st.text_input("Casa", value=st.session_state.get(f'ca_{titulo}', ''), key=f"ca_{titulo}")
        vis = st.text_input("Visitante", value=st.session_state.get(f'v_{titulo}', ''), key=f"v_{titulo}")
        placar = st.text_input("Placar Final", value=st.session_state.get(f'p_{titulo}', ''), key=f"p_{titulo}")
        lista = st.text_area("Lista de jogos", value=st.session_state.get(f'l_{titulo}', ''), key=f"l_{titulo}", height=100)
        
        if st.button(f"Analisar {titulo}", key=f"an_{titulo}", use_container_width=True):
            st.session_state[f"prob_{titulo}"] = calcular_probabilidade(lista)
            st.rerun()
        
        if f"prob_{titulo}" in st.session_state:
            p = st.session_state[f"prob_{titulo}"]
            p_manual = st.text_input("Ajustar Prob (%)", value=f"{p:.1f}", key=f"ajuste_{titulo}")
            p = min(float(p_manual), 100)
            
            # Gráficos
            st.write("📊 **Mercados:**")
            col1, col2 = st.columns(2)
            col1.write(f"O 1.5 ({min(p+5, 100):.0f}%)"); col1.progress(min((p+5)/100, 1.0))
            col2.write(f"O 2.5 ({min(p, 100):.0f}%)"); col2.progress(min(p/100, 1.0))
            
            col3, col4 = st.columns(2)
            col3.write(f"BTTS ({max(0, p-10):.0f}%)"); col3.progress(max(0, p-10)/100)
            col4.write(f"LTD ({max(0, 100-p):.0f}%)"); col4.progress(max(0, 100-p)/100)
            
            mercado = st.selectbox(f"Mercado ({titulo})", ["Automático", "Over 1.5 FT", "Over 2.5 FT", "Ambas Marcam (BTTS)", "LTD"], key=f"sel_{titulo}")
            tipo = mercado if mercado != "Automático" else ("Over 1.5 FT" if p >= 70 else "LTD")
            
            msg = f"🚨 *Alerta de Entrada* 🚨\n\n🏆 *Campeonato:* {camp}\n🆚 *Jogo:* {casa} x {vis}\n🎯 *Mercado:* {tipo}\n📈 *Probabilidade:* {p:.1f}%\n⏰ *Horário:* {hora}\n\n⚠️ *Aposte com responsabilidade.*"
            st.info(msg)
            
            if st.button(f"🚀 ENVIAR {titulo}", key=f"en_{titulo}", type="primary"):
                t = st.session_state.get('token')
                c = st.session_state.get('chat_id')
                if t and c:
                    requests.post(f"https://api.telegram.org/bot{t}/sendMessage", data={"chat_id": c, "text": msg, "parse_mode": "Markdown"})
                    st.session_state[f"msg_{titulo}"] = msg
                    st.rerun()
                else:
                    st.error("Preencha Token e ID na lateral!")

        # Status
        if f"msg_{titulo}" in st.session_state:
            st.write("---")
            c1, c2, c3 = st.columns(3)
            def editar(status):
                requests.post(f"https://api.telegram.org/bot{st.session_state.get('token')}/editMessageText", 
                              data={"chat_id": st.session_state.get('chat_id'), "message_id": st.session_state[f"id_{titulo}"], 
                                    "text": st.session_state[f"msg_{titulo}"] + f"\n⚽ *Placar:* {placar}\n\n🔄 *Status:* {status}", "parse_mode": "Markdown"})
            if c1.button("✅ GREEN", key=f"g_{titulo}"): editar("✅ GREEN!!")
            if c2.button("❌ RED", key=f"r_{titulo}"): editar("❌ RED!")
            if c3.button("🔄 DEV", key=f"d_{titulo}"): editar("🔄 DEVOLVIDA")

c_a, c_b = st.columns(2)
with c_a: renderizar_bloco("JOGO_A")
with c_b: renderizar_bloco("JOGO_B")
