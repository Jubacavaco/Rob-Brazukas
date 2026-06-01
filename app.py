def get_msg(tipo, camp, casa, vis, hora):
    base = f"🚨 *Alerta de Entrada* 🚨\n\n🏆 *Campeonato:* {camp}\n🆚 *Jogo:* {casa} x {vis}\n"
    rodape = "\n\n⚠️ Aposte com responsabilidade. Não há garantias de lucro."
    
    if tipo == "LTD":
        corpo = """🎯 *Mercado:* Match Odd´s
💥 *Prognóstico:* Contra o Empate (LTD)
⏰ *Horário:* """ + hora + """

📌 Entrada recomendada Ao vivo!

⚽ **Gestão de Jogo (Ao Vivo):**
* Se houver 1 gol no HT, sugiro que saia do mercado com um pequeno lucro.
* Se terminar 0 x 0 no HT, permaneça na posição LTD."""

    elif tipo == "BTTS":
        corpo = """🎯 *Mercado:* BTTS
💥 *Prognóstico:* Ambas - SIM
⏰ *Horário:* """ + hora + """

📌 Entrada recomendada antes do início!

⚽ **Gestão de Jogo (Ao Vivo):**
* Se houver 1 gol no HT, sugiro que saia do mercado com um pequeno lucro.
* Se terminar 0 x 0 no HT, permaneça na posição Ambas Sim."""

    elif tipo == "Casa Vence":
        corpo = """🎯 *Mercado:* Match Odd´s
💥 *Prognóstico:* Casa Vence
⏰ *Horário:* """ + hora + """

📌 Entrada recomendada antes do início!

⚽ **Gestão de Jogo (Ao Vivo):**
* Essa é uma entrada para FT (Full Time)."""

    elif tipo == "Over 1.5":
        corpo = """🎯 *Mercado:* Over Gols
💥 *Prognóstico:* 1.5 FT
⏰ *Horário:* """ + hora + """

📌 Entrada recomendada antes do início!

⚽ **Gestão de Jogo (Ao Vivo):**
* Se houver 1 gol no HT, sugiro que saia do mercado com um pequeno lucro.
* Se terminar 0 x 0 no HT, permaneça no Over 1.5 FT."""

    elif tipo == "Over 2.5":
        corpo = """🎯 *Mercado:* Over Gols
💥 *Prognóstico:* 2.5 FT
⏰ *Horário:* """ + hora + """

📌 Entrada recomendada antes do início!

⚽ **Gestão de Jogo (Ao Vivo):**
* Se houver 2 gols no HT, sugiro que saia do mercado com um pequeno lucro.
* Essa é uma entrada para FT (Full Time)."""
    
    return base + corpo + rodape
