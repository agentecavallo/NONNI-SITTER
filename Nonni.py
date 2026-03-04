import streamlit as st
import json
import os
from datetime import datetime, timedelta

# 1. IMPOSTAZIONI PAGINA
st.set_page_config(page_title="Taxi Nipoti", page_icon="🚕", layout="centered")

FILE_MEMORIA = "programma_v4.json" # Nuova versione per la nuova logica
OPZIONI_CHI = ["🟢 FACCIAMO NOI GENITORI", "🔴 TOCCA AI NONNI"]
OPZIONI_ATTIVITA = ["Ginnastica Artistica 🤸‍♀️", "Eufonio 🎺", "Yoga 🧘‍♂️", "Musica 🎵", "Casa 🏠"]

# --- FUNZIONI CORE ---
def ottieni_calendario():
    oggi = datetime.now().date()
    lunedi_curr = oggi - timedelta(days=oggi.weekday())
    lunedi_next = lunedi_curr + timedelta(days=7)
    mesi = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]
    
    def formatta(base):
        giorni_nomi = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì"]
        return {giorni_nomi[i]: {
            "data_testo": f"{giorni_nomi[i]} {(base + timedelta(days=i)).day} {mesi[(base + timedelta(days=i)).month-1]} {(base + timedelta(days=i)).year}",
            "data_obj": base + timedelta(days=i)
        } for i in range(5)}
    
    return {"corrente": formatta(lunedi_curr), "prossima": formatta(lunedi_next), "oggi_obj": oggi}

def resetta_giorno_a_verde():
    """Imposta il giorno selezionato sui valori di default (Genitori)"""
    s = st.session_state.sett_scelta
    g = st.session_state.giorno_sel
    
    st.session_state.programma[s][g] = {
        "mattina": {"chi": "🟢 FACCIAMO NOI GENITORI", "cosa": "Scuola 🏫"},
        "sara_uguale": True,
        "pomeriggio_leo": {"chi": "🟢 FACCIAMO NOI GENITORI", "cosa": "Casa 🏠", "inizio": "16:30", "fine": "18:00"},
        "pomeriggio_sara": {"chi": "🟢 FACCIAMO NOI GENITORI", "cosa": "Casa 🏠", "inizio": "16:30", "fine": "18:00"}
    }
    salva_programma()

def carica_programma():
    if os.path.exists(FILE_MEMORIA):
        try:
            with open(FILE_MEMORIA, "r", encoding="utf-8") as file: return json.load(file)
        except: return crea_struttura_iniziale()
    return crea_struttura_iniziale()

def crea_struttura_iniziale():
    def sett_vuota():
        return {g: {
            "mattina": {"chi": "🟢 FACCIAMO NOI GENITORI", "cosa": "Scuola 🏫"},
            "sara_uguale": True,
            "pomeriggio_leo": {"chi": "🟢 FACCIAMO NOI GENITORI", "cosa": "Casa 🏠", "inizio": "16:30", "fine": "18:00"},
            "pomeriggio_sara": {"chi": "🟢 FACCIAMO NOI GENITORI", "cosa": "Casa 🏠", "inizio": "16:30", "fine": "18:00"}
        } for g in ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì"]}
    return {"corrente": sett_vuota(), "prossima": sett_vuota()}

def salva_programma():
    with open(FILE_MEMORIA, "w", encoding="utf-8") as file:
        json.dump(st.session_state.programma, file, indent=4)

# Inizializzazione sessione
if "programma" not in st.session_state:
    st.session_state.programma = carica_programma()

cal = ottieni_calendario()

# ==========================================
# 3. INTERFACCIA
# ==========================================
sch_nonni, sch_genitori = st.tabs(["🚕 Vista Nonni", "⚙️ Pannello Genitori"])

# --- VISTA NONNI ---
with sch_nonni:
    st.title("🚕 Il Taxi dei Nipoti")
    st.markdown("---")
    per_nonni = [("corrente", cal["corrente"]), ("prossima", cal["prossima"])]
    for id_sett, giorni in per_nonni:
        for nome_g, info in giorni.items():
            if info["data_obj"] >= cal["oggi_obj"]:
                imp = st.session_state.programma[id_sett][nome_g]
                if info["data_obj"] == cal["oggi_obj"]:
                    st.markdown(f"## 🌟 {info['data_testo'].upper()} (OGGI)")
                else:
                    st.markdown(f"### 📅 {info['data_testo']}")
                
                # Mattina
                t_mat = f"**☀️ MATTINA:** Scuola 🏫\n\n👉 *Ore 7:00 a casa!*"
                st.success(t_mat) if "GENITORI" in imp['mattina']['chi'] else st.error(t_mat)
                
                # Pomeriggio
                if imp.get("sara_uguale", True):
                    t_ins = f"**👦👧 LEO E SARA ({imp['pomeriggio_leo']['inizio']}-{imp['pomeriggio_leo']['fine']}):**\n\n{imp['pomeriggio_leo']['cosa']}"
                    st.success(t_ins) if "GENITORI" in imp['pomeriggio_leo']['chi'] else st.error(t_ins)
                else:
                    for f, k in [("👦 LEO", "pomeriggio_leo"), ("👧 SARA", "pomeriggio_sara")]:
                        t = f"**{f} ({imp[k]['inizio']}-{imp[k]['fine']}):** {imp[k]['cosa']}"
                        st.success(t) if "GENITORI" in imp[k]['chi'] else st.error(t)
                st.markdown("---")

# --- MODIFICA GENITORI (CON RESET AUTOMATICO) ---
with sch_genitori:
    st.title("⚙️ Programmazione")
    
    # Selettori Settimana e Giorno con trigger di reset
    st.radio("Seleziona Settimana:", ["corrente", "prossima"], 
             horizontal=True, key="sett_scelta", 
             format_func=lambda x: "Questa" if x=="corrente" else "La Prossima",
             on_change=resetta_giorno_a_verde)
    
    opzioni_g = [n for n, i in cal[st.session_state.sett_scelta].items() if i["data_obj"] >= cal["oggi_obj"]]
    
    st.selectbox("Scegli Giorno da programmare:", opzioni_g, 
                 key="giorno_sel", 
                 format_func=lambda x: cal[st.session_state.sett_scelta][x]["data_testo"],
                 on_change=resetta_giorno_a_verde)

    # Nota: Il reset avviene quando cambi i selettori sopra
    d = st.session_state.programma[st.session_state.sett_scelta][st.session_state.giorno_sel]
    
    st.info(f"Impostazione attuale per: **{st.session_state.giorno_sel}**")
    
    st.subheader("☀️ Mattina: Scuola 🏫")
    d["mattina"]["chi"] = st.selectbox("Chi accompagna?", OPZIONI_CHI, 
                                      index=OPZIONI_CHI.index(d["mattina"]["chi"]), 
                                      key="m_chi", on_change=salva_programma)
    
    st.markdown("---")
    st.subheader("👦 Pomeriggio LEO")
    c1, c2 = st.columns(2)
    d["pomeriggio_leo"]["chi"] = c1.selectbox("Chi?", OPZIONI_CHI, index=OPZIONI_CHI.index(d["pomeriggio_leo"]["chi"]), key="l_chi", on_change=salva_programma)
    d["pomeriggio_leo"]["cosa"] = c2.selectbox("Attività?", OPZIONI_ATTIVITA, index=OPZIONI_ATTIVITA.index(d["pomeriggio_leo"]["cosa"]) if d["pomeriggio_leo"]["cosa"] in OPZIONI_ATTIVITA else 0, key="l_cos", on_change=salva_programma)
    
    c3, c4 = st.columns(2)
    d["pomeriggio_leo"]["inizio"] = c3.text_input("Inizio", d["pomeriggio_leo"]["inizio"], key="l_in", on_change=salva_programma)
    d["pomeriggio_leo"]["fine"] = c4.text_input("Fine", d["pomeriggio_leo"]["fine"], key="l_fi", on_change=salva_programma)

    d["sara_uguale"] = st.checkbox("✅ Sara fa lo stesso di Leo", value=d.get("sara_uguale", True), key="s_ug", on_change=salva_programma)
    
    if not d["sara_uguale"]:
        st.subheader("👧 Pomeriggio SARA")
        c5, c6 = st.columns(2)
        d["pomeriggio_sara"]["chi"] = c5.selectbox("Chi Sara?", OPZIONI_CHI, index=OPZIONI_CHI.index(d["pomeriggio_sara"]["chi"]), key="s_chi", on_change=salva_programma)
        d["pomeriggio_sara"]["cosa"] = c6.selectbox("Attività Sara?", OPZIONI_ATTIVITA, index=OPZIONI_ATTIVITA.index(d["pomeriggio_sara"]["cosa"]) if d["pomeriggio_sara"]["cosa"] in OPZIONI_ATTIVITA else 0, key="s_cos", on_change=salva_programma)
        c7, c8 = st.columns(2)
        d["pomeriggio_sara"]["inizio"] = c7.text_input("Inizio Sara", d["pomeriggio_sara"]["inizio"], key="s_in", on_change=salva_programma)
        d["pomeriggio_sara"]["fine"] = c8.text_input("Fine Sara", d["pomeriggio_sara"]["fine"], key="s_fi", on_change=salva_programma)
    else:
        d["pomeriggio_sara"] = d["pomeriggio_leo"].copy()

    st.caption("✨ Ogni volta che cambi giorno, il sistema riparte da 'Tutto Verde'. Modifica solo se serve l'aiuto dei nonni.")
