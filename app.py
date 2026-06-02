import streamlit as st
import requests
import re

st.set_page_config(layout="wide", page_title="Sistema Brazukas 4 Jogos")
st.title("🤖 Sistema Brazukas Top Tips (4 Jogos)")

TOKEN = st.secrets.get("token", "")
CHAT_ID = st.secrets.get("chat_id", "")

# =========================

# NOVA LÓGICA ESTATÍSTICA

# =========================

def calcular_probabilidade(texto):

```
linhas = texto.strip().splitlines()

over15 = 0
over25 = 0
btts = 0
ltd = 0

vitoria_casa = 0
vitoria_visitante = 0
empate = 0

gols_marcados = 0
gols_sofridos = 0

total = 0

for linha in linhas:

    numeros = re.findall(r'\d+', linha)

    if len(numeros) >= 2:

        g1 = int(numeros[-2])
        g2 = int(numeros[-1])

        total += 1

        gols_marcados += g1
        gols_sofridos += g2

        total_gols = g1 + g2

        # OVER 1.5
        if total_gols >= 2:
            over15 += 1

        # OVER 2.5
        if total_gols >= 3:
            over25 += 1

        # BTTS
        if g1 > 0 and g2 > 0:
            btts += 1

        # LTD
        if g1 != g2:
            ltd += 1

        # RESULTADOS
        if g1 > g2:
            vitoria_casa += 1

        elif g2 > g1:
            vitoria_visitante += 1

        else:
            empate += 1

if total == 0:
    return 50, 50, 0, 0, 0, 0, 0

# PORCENTAGENS
p_over15 = (over15 / total) * 100
p_over25 = (over25 / total) * 100
p_btts = (btts / total) * 100
p_ltd = (ltd / total) * 100

p_casa = (vitoria_casa / total) * 100
p_visitante = (vitoria_visitante / total) * 100
p_empate = (empate / total) * 100

# MÉDIAS
media_marcados = gols_marcados / total
media_sofridos = gols_sofridos / total

# AJUSTES
if media_marcados >= 2:
    p_over15 += 5
    p_over25 += 5

if media_sofridos >= 1.5:
    p_btts += 5

# LIMITES
p_over15 = min(p_over15, 95)
p_over25 = min(p_over25, 90)
p_btts = min(p_btts, 85)
p_ltd = min(p_ltd, 95)

return (
    round(p_casa, 1),
    round(p_visitante, 1),
    round(p_empate, 1),
    round(p_over15, 1),
    round(p_over25, 1),
    round(p_btts, 1),
    round(p_ltd, 1)
)
```

# =========================

# SUGESTÃO DE MERCADO

# =========================

def obter_sugestao(p15, p25, pbtts, pltd):

```
if p25 >= 65:
    return "Over 2.5 FT"

elif p15 >= 75:
    return "Over 1.5 FT"

elif pbtts >= 51:
    return "Ambas Marcam (BTTS)"

elif pltd >= 51:
    return "LTD"

else:
    return "Nenhum mercado recomendado"
```

# =========================

# BLOCO DOS JOGOS

# =========================

def renderizar_bloco(titulo):

```
st.subheader(f"🏟️ {titulo}")

camp = st.text_input("Campeonato", key=f"c_{titulo}")
casa = st.text_input("Casa", key=f"ca_{titulo}")
vis = st.text_input("Visitante", key=f"v_{titulo}")
hora = st.text_input("Horário", key=f"h_{titulo}")

# VOCÊ ESCOLHE A % MANUALMENTE
prob_manual = st.text_input("Probabilidade (%)", key=f"pr_{titulo}")

pm = st.text_input("Placar Momento", key=f"pm_{titulo}")
pht = st.text_input("Placar HT", key=f"pht_{titulo}")
pf = st.text_input("Placar Final", key=f"pf_{titulo}")

lista = st.text_area("Lista de jogos", key=f"l_{titulo}")

if st.button("Analisar", key=f"an_{titulo}"):

    st.session_state[f"probs_{titulo}"] = calcular_probabilidade(lista)

if f"probs_{titulo}" in st.session_state:

    pc, pv, pe, p15, p25, pbtts, pltd = st.session_state[f"probs_{titulo}"]

    sugestao = obter_sugestao(p15, p25, pbtts, pltd)

    if sugestao != "Nenhum mercado recomendado":
        st.success(f"🎯 Sugestão: {sugestao}")

    # BARRAS
    st.progress(min(max(p25/100, 0), 1), text=f"O2.5: {p25:.0f}%")
    st.progress(min(max(p15/100, 0), 1), text=f"O1.5: {p15:.0f}%")
    st.progress(min(max(pbtts/100, 0), 1), text=f"BTTS: {pbtts:.0f}%")
    st.progress(min(max(pltd/100, 0), 1), text=f"LTD: {pltd:.0f}%")

    st.progress(
        min(max(pc/100, 0), 1),
        text=f"Vit. {casa if casa else 'Casa'}: {pc:.1f}%"
    )

    st.progress(
        min(max(pv/100, 0), 1),
        text=f"Vit. {vis if vis else 'Visitante'}: {pv:.1f}%"
    )

    # MERCADO
    tipo = st.selectbox(
        "Mercado",
        [
            sugestao,
            "Over 2.5 FT",
            "Over 1.5 FT",
            "Ambas Marcam (BTTS)",
            "LTD"
        ],
        key=f"sel_{titulo}"
    )

    # % MANUAL
    prob = prob_manual if prob_manual else "0"

    # MENSAGEM TELEGRAM
    msg_base = (
        f"🚨 *Alerta de Entrada* 🚨\n\n"
        f"🏆 Campeonato: {camp}\n"
        f"🆚 Jogo: {casa} x {vis}\n"
        f"🎯 Mercado: {tipo}\n"
        f"📈 Probabilidade: {prob}%\n"
        f"⏰ Horário: {hora}\n\n"
        f"🔞 Aposte com responsabilidade.\n"
        f"⚠️ Não há garantias de lucros."
    )

    st.info(f"Prévia:\n{msg_base}")

    # =========================
    # RESUMO FINAL
    # =========================

    st.write("### 📊 Resumo Final")

    resumo = f"""
```

| Mercado                                  | Probabilidade |
| ---------------------------------------- | ------------- |
| ✅ Over 1.5 FT                            | {p15:.0f}%    |
| ⚠️ Over 2.5 FT                           | {p25:.0f}%    |
| ⚠️ Ambas Marcam (BTTS)                   | {pbtts:.0f}%  |
| 🔥 LTD (Sem Empate)                      | {pltd:.0f}%   |
| 🟦 Vitória {casa if casa else 'Casa'}    | {pc:.0f}%     |
| 🟥 Vitória {vis if vis else 'Visitante'} | {pv:.0f}%     |
| 🤝 Empate                                | {pe:.0f}%     |
| """                                      |               |

```
    st.markdown(resumo)

    # =========================
    # MERCADOS MAIS FORTES
    # =========================

    st.write("### 🎯 Mercados Mais Fortes")

    mercados = []

    if p15 >= 75:
        mercados.append("✅ Over 1.5 FT — Muito Forte")

    if p25 >= 65:
        mercados.append("🔥 Over 2.5 FT — Forte")
    elif p25 >= 50:
        mercados.append("⚠️ Over 2.5 FT — Moderado")

    if pbtts >= 60:
        mercados.append("🔥 BTTS — Forte")
    elif pbtts >= 45:
        mercados.append("⚠️ BTTS — Moderado")

    if pltd >= 80:
        mercados.append("🔥 LTD (Sem Empate) — Muito Forte")

    for m in mercados:
        st.write(m)

    # =========================
    # PLACARES COMPATÍVEIS
    # =========================

    st.write("### 📌 Placares Compatíveis")

    placares = []

    if p15 >= 70 and pbtts < 50:
        placares = ["2x0", "1x0", "2x1", "1x1"]

    elif p25 >= 65 and pbtts >= 55:
        placares = ["2x1", "3x1", "2x2", "3x2"]

    elif pbtts >= 60:
        placares = ["1x1", "2x1", "2x2"]

    else:
        placares = ["1x0", "1x1", "2x0"]

    for p in placares:
        st.write(f"• {p}")

    # =========================
    # ENVIAR TELEGRAM
    # =========================

    if st.button("🚀 ENVIAR", key=f"en_{titulo}", type="primary"):

        res = requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            data={
                "chat_id": CHAT_ID,
                "text": msg_base,
                "parse_mode": "Markdown"
            }
        ).json()

        if res.get("ok"):

            st.session_state[f"id_{titulo}"] = res["result"]["message_id"]
            st.session_state[f"msg_base_{titulo}"] = msg_base

            st.success("Enviado!")

# =========================
# BOTÕES STATUS
# =========================
if f"id_{titulo}" in st.session_state:

    st.write("---")

    def atualizar_telegram(status, modo):

        msg_id = st.session_state[f"id_{titulo}"]
        msg_base = st.session_state.get(f"msg_base_{titulo}", "")

        if modo == "MOMENTO":

            txt_placar = f"\n⚽ Momento: {pm}"
            status = "GREEN 🟢✅"

        elif modo == "HT":

            txt_placar = f"\n⚽ HT: {pht}"

        elif modo == "FINAL":

            txt_placar = f"\n⚽ HT: {pht}\n⚽ Final: {pf}"

        elif modo == "RED":

            txt_placar = f"\n⚽ HT: {pht}\n⚽ Final: {pf}"

        txt = (
            f"{msg_base}\n"
            f"{txt_placar}\n\n"
            f"🔄 STATUS ATUAL: {status}"
        )

        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/editMessageText",
            data={
                "chat_id": CHAT_ID,
                "message_id": msg_id,
                "text": txt,
                "parse_mode": "Markdown"
            }
        )

        st.success(f"Atualizado: {status}")

    c1, c2, c3, c4 = st.columns(4)

    if c1.button("Momento", key=f"m_{titulo}"):
        atualizar_telegram("GREEN 🟢✅", "MOMENTO")

    if c2.button("HT", key=f"ht_{titulo}"):
        atualizar_telegram("EM ANDAMENTO ⚪", "HT")

    if c3.button("Final", key=f"f_{titulo}"):
        atualizar_telegram("GREEN 🟢✅", "FINAL")

    if c4.button("RED", key=f"r_{titulo}"):
        atualizar_telegram("RED 🔴❌", "RED")
```

# =========================

# 4 COLUNAS

# =========================

col1, col2, col3, col4 = st.columns(4)

with col1:
renderizar_bloco("JOGO_A")

with col2:
renderizar_bloco("JOGO_B")

with col3:
renderizar_bloco("JOGO_C")

with col4:
renderizar_bloco("JOGO_D")
