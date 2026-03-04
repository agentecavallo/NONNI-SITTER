import streamlit as st
import json
import os
from datetime import datetime, timedelta

# 1. IMPOSTAZIONI PAGINA
st.set_page_config(page_title="Taxi Nipoti", page_icon="🚕", layout="centered")

FILE_MEMORIA = "programma.json"
OPZIONI_CHI = ["🔴 TOCCA AI NONNI", "🟢 FACCIAMO NOI GENITORI"]
OPZIONI_ATTIVITA = ["Scuola 🏫", "Ginnastica Artistica 🤸‍♀️", "Eufonio 🎺", "Yoga 🧘‍♂️", "Musica 🎵", "Casa 🏠"]

# --- FUNZIONE DATE ---
def ottieni_date_settimana():
    oggi = datetime.now()
    # Calcola il lunedì della settimana corrente
    lunedi = oggi - timedelta(days=oggi.weekday())
    
    nomi_giorni = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì"]
    mesi = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", 
            "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]
    
    date_formattate = {}
    for i, nome in enumerate(nomi_giorni):
        data_giorno = lunedi + timedelta(days=i)
        data_testo = f"{nome} {data_giorno.day} {mesi[data_giorno.month-1]} {data_giorno.year}"
        date_formattate[nome] = data_testo
        
    # Otteniamo il nome del giorno di oggi in italiano per il confronto
    giorni_ita = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]
    oggi_ita = giorni_ita[oggi.weekday()]
    
    return date_formattate, oggi_ita

# 2. GESTIONE MEMORIA
def crea_settimana_base():
    settimana = {}
    for g in ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì"]:
        settimana[g] = {
            "mattina": {"chi": "🔴 TOCCA AI NONNI", "cosa": "Scuola 🏫"},
            "sara_uguale": True,
            "pomeriggio_leo": {"chi": "🟢 FACCIAMO NOI GENITORI", "cosa": "Casa 🏠", "inizio": "16:30", "fine": "18:00"},
            "pomeriggio_sara": {"chi": "🟢 FACCIAMO NOI GENITORI", "cosa": "Casa 🏠", "inizio": "16:30", "fine": "18:00"}
        }
    return settimana

def carica_programma():
    if os.path.exists(FILE_MEMORIA):
        try:
            with open(FILE_MEMORIA, "r", encoding="utf-8") as file:
                dati = json.load(file)
                # Se il file è vecchio (manca pomeriggio_leo), resetta
                if "Lunedì" in dati and "pomeriggio_leo" not in dati["Lunedì"]:
                    return crea_settimana_base()
                return dati
        except: return crea_settimana_base()
    return crea_settimana_base()

def salva_programma(dati):
    with open(FILE_MEMORIA, "w", encoding="utf-8") as file:
        json.dump(dati, file, indent=4)

programma = carica_programma()
date_settimana, oggi_nome_ita = ottieni_date_settimana()

# ==========================================
# 3. INTERFACCIA (TABS)
# ==========================================
sch_nonni, sch_genitori = st.tabs(["🚕 Vista Nonni", "⚙️ Modifica"])

# --- VISTA NONNI ---
with sch_nonni:
    st.title("🚕 Il Taxi dei Nipoti")
    
    # BOX DI EVIDENZA PER OGGI
    if oggi_nome_ita in date_settimana:
        st.info(f"🌟 **OGGI È {date_settimana[oggi_nome_ita].upper()}**")
    else:
        st.info("📅 Fine settimana! Ecco il programma della settimana passata o futura.")
    
    st.markdown("---")

    for giorno_chiave, impegni in programma.items():
        data_display = date_settimana[giorno_chiave]
        
        # EVIDENZIAZIONE GIORNO
        if giorno_chiave == oggi_nome_ita:
            st.markdown(f"## 🌟 {data_display.upper()} (OGGI)")
        else:
            st.markdown(f"### 📅 {data_display}")
        
        # MATTINA
        testo_mat = f"**☀️ MATTINA:** {impegni['mattina']['cosa']}"
        if impegni['mattina']['cosa'] == "Scuola 🏫":
             testo_mat += "\n\n👉 *Vi aspettiamo alle 7:00 a casa!*"

        if "NONNI" in impegni['mattina']['chi']:
            st.error(testo_mat)
        else:
            st.success(testo_mat)
            
        # POMERIGGIO
        if impegni.get("sara_uguale", True):
            t_ins = f"**👦👧 LEO E SARA ({impegni['pomeriggio_leo']['inizio']} - {impegni['pomeriggio_leo']['fine']}):**\n\n{impegni['pomeriggio_leo']['cosa']}"
            if "NONNI" in impegni['pomeriggio_leo']['chi']: st.error(t_ins)
            else: st.success(t_ins)
        else:
            t_leo = f"**👦 LEO ({impegni['pomeriggio_leo']['inizio']} - {impegni['pomeriggio_leo']['fine']}):**\n\n{impegni['pomeriggio_leo']['cosa']}"
            t_sara = f"**👧 SARA ({impegni['pomeriggio_sara']['inizio']} - {impegni['pomeriggio_sara']['fine']}):**\n\n{impegni['pomeriggio_sara']['cosa']}"
            if "NONNI" in impegni['pomeriggio_leo']['chi']: st.error(t_leo)
            else: st.success(t_leo)
            if "NONNI" in impegni['pomeriggio_sara']['chi']: st.error(t_sara)
            else: st.success(t_sara)
            
        st.markdown("---")

# --- MODIFICA GENITORI ---
with sch_genitori:
    st.title("⚙️ Pannello Controllo")
    scelta = st.selectbox("Seleziona Giorno:", list(programma.keys()), 
                          format_func=lambda x: date_settimana[x])
    
    st.subheader("☀️ Mattina")
    c1, c2 = st.columns(2)
    chi_m = c1.selectbox("Chi?", OPZIONI_CHI, index=OPZIONI_CHI.index(programma[scelta]["mattina"]["chi"]), key="m1")
    cos_m = c2.selectbox("Cosa?", OPZIONI_ATTIVITA, index=OPZIONI_ATTIVITA.index(programma[scelta]["mattina"]["cosa"]), key="m2")
    
    st.markdown("---")
    st.subheader("👦 Pomeriggio LEO")
    c3, c4 = st.columns(2)
    chi_l = c3.selectbox("Chi Leo?", OPZIONI_CHI, index=OPZIONI_CHI.index(programma[scelta]["pomeriggio_leo"]["chi"]), key="l1")
    cos_l = c4.selectbox("Cosa?", OPZIONI_ATTIVITA, index=OPZIONI_ATTIVITA.index(programma[scelta]["pomeriggio_leo"]["cosa"]), key="l2")
    c5, c6 = st.columns(2)
    in_l = c5.text_input("Inizio", programma[scelta]["pomeriggio_leo"]["inizio"])
    fi_l = c6.text_input("Fine", programma[scelta]["pomeriggio_leo"]["fine"])

    sara_uguale = st.checkbox("✅ Sara fa lo stesso di Leo", value=programma[scelta].get("sara_uguale", True))
    
    if not sara_uguale:
        st.subheader("👧 Pomeriggio SARA")
        c7, c8 = st.columns(2)
        chi_s = c7.selectbox("Chi Sara?", OPZIONI_CHI, index=OPZIONI_CHI.index(programma[scelta]["pomeriggio_sara"]["chi"]), key="s1")
        cos_s = c8.selectbox("Cosa?", OPZIONI_ATTIVITA, index=OPZIONI_ATTIVITA.index(programma[scelta]["pomeriggio_sara"]["cosa"]), key="s2")
        c9, c10 = st.columns(2)
        in_s = c9.text_input("Inizio Sara", programma[scelta]["pomeriggio_sara"]["inizio"])
        fi_s = c10.text_input("Fine Sara", programma[scelta]["pomeriggio_sara"]["fine"])

    if st.button("💾 SALVA PROGRAMMA"):
        programma[scelta]["mattina"] = {"chi": chi_m, "cosa": cos_m}
        programma[scelta]["pomeriggio_leo"] = {"chi": chi_l, "cosa": cos_l, "inizio": in_l, "fine": fi_l}
        programma[scelta]["sara_uguale"] = sara_uguale
        if sara_uguale:
            programma[scelta]["pomeriggio_sara"] = programma[scelta]["pomeriggio_leo"].copy()
        else:
            programma[scelta]["pomeriggio_sara"] = {"chi": chi_s, "cosa": cos_s, "inizio": in_s, "fine": fi_s}
        salva_programma(programma)
        st.success("Salvato correttamente!")
        st.rerun()
