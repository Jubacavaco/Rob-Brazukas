import streamlit as st
import requests
import re
from supabase import create_client

# Configurações e Conexão
SUPABASE_URL = "https://levzsvuikgqfnosykigi.supabase.co"
SUPABASE_KEY = "sb_publishable_esm8GzVdsIrPSjfcAkcX8Q_0NYasNBn"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
TOKEN = "8776214366:AAEQnGyhcEa6NQcYzyFAhtVDXKpQx5CoYT0"
CHAT_ID = "-1003925163611"

def calcular_probabilidade(texto):
    numeros = re.findall(r'\b\d+\b', texto)
    gols = [int(n) for n in numeros if int(n) <= 10]
    over15 = over25 = btts = ltd = 0
    v_casa = v_vis = empate = total = 0
    i = 0
    while i < len(gols) - 1:
        g1, g2 = gols[i], gols[i+1]
        total += 1
        if (g1 + g2) >= 2: over15 += 1
        if (g1 + g2) >= 3: over25 += 1
        if g1 > 0 and g2 > 0: btts += 1
        if g1 != g2: ltd += 1
        if g1 > g2: v_casa += 1
        elif g2 > g1: v_vis += 1
        else: empate += 1
        i += 2
    if total == 0: return 0, 0, 0, 0, 0, 0, 0
    p15 = min(round(((over15/total)*100)+5, 1), 95)
    p25 = min(round(((over25/total)*100)+5, 1), 90)
    pb = min(round((btts/total)*100, 1), 85)
    pl = min(round((ltd/total)*100, 1), 95)
    return round((v_casa/total)*100, 1), round((v_vis/total)*100, 1), round((empate/total)*100, 1), p15, p25, pb, pl

def renderizar_bloco(titulo):
    st.subheader(f"🏟️ {titulo}")
    camp = st.text_input("Campeonato", key=f"c_{titulo}")
    casa = st.text_input("Casa", key=f"ca_{titulo}")
    vis = st.text_input("Visitante", key=f"v_{titulo}")
    prob = st.text_input("Probabilidade", key=f"pb_{titulo}")
    hora = st.text_input("Horário", key=f"h_{titulo}")
    pm = st.text_input("Momento", key=f"pm_{titulo}")
    pht = st.text_input("HT", key=f"pht_{titulo}")
    pf = st.text_input("Final", key=f"pf_{titulo}")
    lista = st.text_area("Lista de jogos", key=f"l_{titulo}")

    if st.button("Analisar", key=f"an_{titulo}"):
        st.session_state[f"res_{titulo}"] = calcular_probabilidade(lista)

    db_res = supabase.table("sinais").select("*").eq("bloco", titulo).eq("status", "ativa").execute()
    msg_ativa = db_res.data[0] if db_res.data else None

    if f"res_{titulo}" in st.session_state:
        pc, pv, pe, p15, p25, pb, pl = st.session_state[f"res_{titulo}"]
        st.write("🔥 **Mercados Fortes:**")
        sugestao = "Nenhuma"
        if p15 >= 75: st.write(f"✅ Over 1.5 ({p15}%)"); sugestao = "Over 1.5 FT"
        if p25 >= 65: st.write(f"🔥 Over 2.5 ({p25}%)"); sugestao = "Over 2.5 FT"
        if pb >= 60: st.write(f"🔥 BTTS ({pb}%)"); sugestao = "BTTS"
        if pl >= 80: st.write(f"🔥 LTD ({pl}%)"); sugestao = "LTD"
        st.success(f"💡 Aposta Recomendada: {sugestao}")
        tipo = st.selectbox("Mercado Principal", ["Over 2.5 FT", "Over 1.5 FT", "BTTS", "LTD", "Casa Vence", "Visitante Vence"], key=f"sel_{titulo}")
        
        msg = (f"🚨 Alerta de Entrada 🚨\n\n🏆 Campeonato: {camp}\n🆚 Jogo: {casa} x {vis}\n🎯 Mercado: {tipo}\n📈 Probabilidade: {prob}%\n⏰ Horário: {hora}\n\n\n🔞 Aposte com responsabilidade.\n⚠️ Não há garantias de lucro.")
        st.info(msg)
        
        if st.button("🚀 ENVIAR PARA TELEGRAM", key=f"en_{titulo}"):
            res = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg}).json()
            if res.get("ok"):
                supabase.table("sinais").insert({"message_id": int(res["result"]["message_id"]), "bloco": titulo, "msg_original": msg, "status": "ativa"}).execute()
                st.success("Enviado!"); st.rerun()

    if msg_ativa:
        st.warning(f"⚠️ Alerta Ativo (ID: {msg_ativa['message_id']})")
        def at(status, info):
            new_text = f"{msg_ativa['msg_original']}\n\n⚽ {info}\n\n🔄 {status}"
            requests.post(f"https://api.telegram.org/bot{TOKEN}/editMessageText", data={"chat_id": CHAT_ID, "message_id": msg_ativa['message_id'], "text": new_text})
            supabase.table("sinais").update({"status": "finalizada"}).eq("message_id", msg_ativa['message_id']).execute()
            st.rerun()
            
        c1, c2, c3, c4 = st.columns(4)
        if c1.button("Momento", key=f"m_{titulo}"): at("GREEN 🟢", f"Momento: {pm}")
        if c2.button("HT", key=f"ht_{titulo}"): at("EM ANDAMENTO ⚪", f"HT: {pht}")
        if c3.button("Final", key=f"f_{titulo}"): at("GREEN 🟢", f"HT: {pht} | Final: {pf}")
        if c4.button("RED", key=f"r_{titulo}"): at("RED 🔴", f"HT: {pht} | Final: {pf}")

# --- CHAMADA FINAL ---
col1, col2, col3, col4 = st.columns(4)
with col1: renderizar_bloco("JOGO_A")
with col2: renderizar_bloco("JOGO_B")
with col3: renderizar_bloco("JOGO_C")
with col4: renderizar_bloco("JOGO_D")
