# Rodapé fixo com o espaçamento solicitado (2 linhas para baixo do status)
RODAPE = "\n\n🔞Aposte com responsabilidade.\n⚠️ Não há garantias de lucro."

def telegram(msg, msg_id=None):
    url = f"https://api.telegram.org/bot{TOKEN}/"
    # Adiciona o rodapé fixo ao final de toda mensagem
    texto_final = msg + RODAPE
    try:
        if msg_id:
            requests.post(url + "editMessageText", json={"chat_id": CHAT_ID, "message_id": msg_id, "text": texto_final})
        else:
            resp = requests.post(url + "sendMessage", json={"chat_id": CHAT_ID, "text": texto_final}).json()
            return resp.get("result", {}).get("message_id")
    except: return None

# --- DENTRO DA FUNÇÃO jogo_normal ---
# Ajuste dos botões para seguir o espaçamento solicitado:
        mid = st.session_state.get(f"mid_{nome}")
        if mid:
            base = f"🚨 Alerta de Cantos 🚨\n\n🏆 Campeonato: {camp}\n🆚 Jogo: {casa} x {vis}\n🎯 Mercado: {mercado}\n💥 Prognóstico: {prog_str}\n📈 Probabilidade: {prob}%\n⏰ Horário: {horario} (BR)"
            b1, b2 = st.columns(2)
            
            # Espaçamento: 1 linha após horário, e 2 linhas antes do status
            if b1.button("⏱️ MOMENTO", key=f"mom_{nome}"): 
                telegram(f"{base}\n\nPlacar: {ht}\n\n⚪ Em Andamento", mid)
            
            if b1.button("✅ HT", key=f"htg_{nome}"): 
                telegram(f"{base}\n\nPlacar: {ht}\n\n✅✅✅ GREEN ✅✅✅", mid)
            
            # Placar Final: HT na linha, FT logo abaixo, 2 linhas para o status
            if b2.button("🏆 FINAL", key=f"fng_{nome}"): 
                telegram(f"{base}\n\nPlacar HT: {ht}\nPlacar FT: {ft}\n\n🏆🏆🏆 GREEN FINAL 🏆🏆🏆", mid)
            
            if b2.button("❌ RED", key=f"red_{nome}"): 
                telegram(f"{base}\n\nPlacar: {ft}\n\n❌❌❌ RED ❌❌❌", mid)
