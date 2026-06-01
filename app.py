import streamlit as st
import requests
import re

# Configuração da página
st.set_page_config(layout="wide", page_title="Painel Brazukas")
st.title("🤖 Painel Brazukas - Gestão Total")

# Tenta carregar o Token e ID do "Secrets" automaticamente
try:
    TOKEN = st.secrets["token"]
    CHAT_ID = st.secrets["chat_id"]
except Exception:
    st.error("❌ Erro: Não encontrei as credenciais no 'Secrets'. Configure-as no Settings do Streamlit.")
    st.stop()

def calcular_probabilidade(texto):
    numeros = re.findall(r'\d+', texto)
    gols = [int(n) for n in numeros if int(n) <= 10]
    if len(gols) < 2: return 0
    media = sum(gols) / len(gols)
    return min(media * 20, 100)

def renderizar_bloco(titulo):
    with st.container(border=True):
        st.subheader(f"🏟️ {titulo}")
        
        # Campos com persistência de estado
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
            c_g1, c_g2 = st.columns(2)
            c_g1.write(f"O 1.5 ({min(p+5, 100):.0f}%)"); c_g1.progress(min((p+5)/100, 1.0))
            c_g2.write(f"O 2.5 ({min(p, 100):.0f}%)"); c_g2.progress(min(p/100, 1.0))
            
            mercado = st.selectbox(f"Mercado ({titulo})", ["Automático", "Over 1.5 FT", "Over 2.5 FT", "Ambas Marcam (BTTS)", "LTD"], key=f"sel_{titulo}")
            tipo = mercado if mercado != "Automático" else ("Over 1.5 FT" if p >= 70 else "LTD")
            
            msg = f"🚨 *Alerta de Entrada* 🚨\n\n🏆 *Campeonato:* {camp}\n🆚 *Jogo:* {casa} x {vis}\n🎯 *Mercado:* {tipo}\n📈 *Probabilidade:* {p:.1f}%\n⏰ *Horário:* {hora}\n\n⚠️ *Aposte com responsabilidade.*"
            st.info(msg)
            
            if st.button(f"🚀 ENVIAR {titulo}", key=f"en_{titulo}", type="primary"):
                # Usa TOKEN e CHAT_ID que definimos lá em cima
                res = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}).json()
                if res.get("ok"):
                    st.session_state[f"id_{titulo}"] = res["result"]["message_id"]
                    st.session_state[f"msg_{titulo}"] = msg
                    st.rerun()

        # Edição de Status
        if f"id_{titulo}" in st.session_state:
            st.write("---")
            c1, c2, c3 = st.columns(3)
            def editar(status):
                msg_id = st.session_state.get(f"id_{titulo}")
                if msg_id:
                    requests.post(f"https://api.telegram.org/bot{TOKEN}/editMessageText", 
                                  data={"chat_id": CHAT_ID, "message_id": msg_id, 
                                        "text": st.session_state.get(f"msg_{titulo}", "") + f"\n⚽ *Placar:* {placar}\n\n🔄 *Status:* {status}", "parse_mode": "Markdown"})
                    st.success(f"Status atualizado!")

            if c1.button("✅ GREEN", key=f"g_{titulo}"): editar("✅ GREEN!!")
            if c2.button("❌ RED", key=f"r_{titulo}"): editar("❌ RED!")
            if c3.button("🔄 DEV", key=f"d_{titulo}"): editar("🔄 DEVOLVIDA")

c_a, c_b = st.columns(2)
with c_a: renderizar_bloco("JOGO_A")
with c_b: renderizar_bloco("JOGO_B")
