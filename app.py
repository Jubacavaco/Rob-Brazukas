import streamlit as st
import requests
import re

# Configuração da página
st.set_page_config(layout="wide")
st.title("🤖 Painel Brazukas - Gestão Total")

# Sidebar - Configurações
st.sidebar.header("⚙️ Configurações")
token = st.sidebar.text_input("Token Telegram", type="password")
chat_id = st.sidebar.text_input("ID Canal", type="password")

def calcular_probabilidade(texto):
    numeros = re.findall(r'\d+', texto)
    gols = [int(n) for n in numeros if int(n) <= 10]
    if len(gols) < 2: return 0
    # Normalização: multiplicador ajustado para a média de gols
    media = sum(gols) / len(gols)
    prob = media * 20 
    return min(prob, 100) # Garante que nunca passa de 100%

def renderizar_bloco(titulo):
    with st.container(border=True):
        st.subheader(f"🏟️ {titulo}")
        
        # Inputs principais
        col_c1, col_c2 = st.columns(2)
        camp = col_c1.text_input(f"Campeonato", key=f"c_{titulo}")
        hora = col_c2.text_input(f"Horário", key=f"h_{titulo}")
        casa = st.text_input(f"Casa", key=f"ca_{titulo}")
        vis = st.text_input(f"Visitante", key=f"v_{titulo}")
        placar = st.text_input(f"Placar Final", key=f"p_{titulo}", placeholder="0-0")
        lista = st.text_area(f"Lista de jogos", key=f"l_{titulo}", height=100)
        
        if st.button(f"Analisar {titulo}", key=f"an_{titulo}", use_container_width=True):
            st.session_state[f"prob_{titulo}"] = calcular_probabilidade(lista)
            st.rerun()
        
        if f"prob_{titulo}" in st.session_state:
            p_base = st.session_state[f"prob_{titulo}"]
            p_manual = st.text_input("Ajustar Probabilidade (%)", value=f"{p_base:.1f}", key=f"ajuste_{titulo}")
            p = min(float(p_manual), 100) if p_manual else p_base
            
            st.write("📊 **Acompanhamento Visual:**")
            col_g1, col_g2 = st.columns(2)
            col_g1.write(f"Over 1.5 FT ({min(p+5, 100):.0f}%)")
            col_g1.progress(min((p+5)/100, 1.0))
            col_g2.write(f"Over 2.5 FT ({min(p, 100):.0f}%)")
            col_g2.progress(min(p/100, 1.0))
            
            mercado = st.selectbox(f"Mercado ({titulo})", ["Automático", "Over 1.5 FT", "Over 2.5 FT", "Ambas Marcam (BTTS)", "LTD"], key=f"sel_{titulo}")
            tipo = mercado if mercado != "Automático" else ("Over 1.5 FT" if p >= 70 else "LTD")
            
            msg = f"🚨 *Alerta de Entrada* 🚨\n\n🏆 *Campeonato:* {camp}\n🆚 *Jogo:* {casa} x {vis}\n🎯 *Mercado:* {tipo}\n📈 *Probabilidade:* {p:.1f}%\n⏰ *Horário:* {hora}\n\n⚠️ *Aposte com responsabilidade.*"
            st.info(msg)
            
            if st.button(f"🚀 ENVIAR {titulo}", key=f"en_{titulo}", type="primary"):
                if token and chat_id:
                    payload = {"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}
                    r = requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data=payload).json()
                    if r.get("ok"): 
                        st.session_state[f"id_{titulo}"] = r["result"]["message_id"]
                        st.session_state[f"msg_{titulo}"] = msg
                        st.rerun()
                else:
                    st.error("Configure Token/ID na lateral!")

        # Edição de Status
        if f"id_{titulo}" in st.session_state:
            st.write("---")
            c1, c2, c3 = st.columns(3)
            def editar_telegram(status):
                new_msg = st.session_state[f"msg_{titulo}"] + f"\n⚽ *Placar:* {placar}\n\n🔄 *Status:* {status}"
                requests.post(f"https://api.telegram.org/bot{token}/editMessageText", 
                            data={"chat_id": chat_id, "message_id": st.session_state[f"id_{titulo}"], "text": new_msg, "parse_mode": "Markdown"})
                st.success(f"Status atualizado!")

            if c1.button("✅ GREEN", key=f"g_{titulo}"): editar_telegram("✅ GREEN!!")
            if c2.button("❌ RED", key=f"r_{titulo}"): editar_telegram("❌ RED!")
            if c3.button("🔄 DEV", key=f"d_{titulo}"): editar_telegram("🔄 DEVOLVIDA")

# Layout final
col1, col2 = st.columns(2)
with col1: renderizar_bloco("JOGO_A")
with col2: renderizar_bloco("JOGO_B")
