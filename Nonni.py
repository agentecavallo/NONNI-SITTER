import streamlit as st
import json
import os
from datetime import datetime, timedelta

# 1. IMPOSTAZIONI PAGINA
st.set_page_config(page_title="Taxi Nipoti", page_icon="🚕", layout="centered")

FILE_MEMORIA = "programma_v2.json" # Cambiato nome per resettare la vecchia struttura
OPZIONI_CHI = ["🔴 TOCCA AI NONNI", "🟢 FACCIAMO NOI GENITORI"]
OPZIONI_ATTIVITA = ["Scuola 🏫", "Ginnastica Artistica 🤸‍♀️", "Eufonio 🎺", "Yoga 🧘‍♂️", "Musica 🎵", "Casa 🏠"]

# --- FUNZIONE DATE POTENZIATA ---
def ottieni_calendario():
    oggi = datetime.now().date()
    # Lunedì di questa settimana
    lunedi_curr = oggi - timedelta(days=oggi.weekday())
    # Lunedì della prossima settimana
    lunedi_next = lunedi_curr + timedelta(days=7)
    
    nomi_giorni = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì"]
    mesi = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", 
            "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]
    
    def formatta_settimana(lunedi_base):
        sett = {}
        for i, nome in enumerate(nomi_giorni):
            d = lunedi_base + timedelta(days=i)
            sett[nome] = {"data_testo": f"{nome} {d.day} {mesi[d.month-1]} {d.year}", "data_obj": d}
        return sett

    return {
        "corrente": formatta_settimana(lunedi_curr),
        "prossima": formatta_settimana(lunedi_next),
        "oggi_obj": oggi
    }

# 2. GESTIONE MEMORIA (Supporto per due settimane)
def crea_struttura_vuota():
    def sett_vuota():
        return {g: {
            "mattina": {"chi": "🔴 TOCCA AI NONNI", "cosa": "Scuola 🏫"},
            "sara_uguale": True,
            "pomeriggio_leo": {"chi": "🟢 FACCIAMO NOI GENITORI", "cosa": "Casa 🏠", "inizio": "16:30", "fine": "18:00"},
            "pomeriggio_sara": {"chi": "🟢 FACCIAMO NOI GENITORI", "cosa": "Casa 🏠", "inizio": "16:30", "fine": "18:00"}
        } for g in ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì"]}
    
    return {"corrente": sett_vuota(), "prossima": sett_vuota()}

def carica_programma():
    if os.path.exists(FILE_MEMORIA):
        try:
            with open(FILE_MEMORIA, "r", encoding="utf-8") as file:
                return json.load(file)
        except: return crea_struttura_vuota()
    return crea_struttura_vuota()

def salva_programma(dati):
    with open(FILE_MEMORIA, "w", encoding="utf-8") as file:
        json.dump(dati, file, indent=4)

# Inizializzazione
cal = ottieni_calendario()
programma = carica_programma()

# ==========================================
# 3. INTERFACCIA (TABS)
# ==========================================
sch_nonni, sch_genitori = st.tabs(["🚕 Vista Nonni", "⚙️ Pannello Genitori"])

# --- VISTA NONNI (Solo futuro) ---
with sch_nonni:
    st.title("🚕 Il Taxi dei Nipoti")
    st.write(f"Oggi è {cal['corrente'].get(datetime.now().strftime('%A').replace('Monday','Lunedì'), {'data_testo':''})['data_testo']}")
    st.markdown("---")

    mostrati = 0
    # Uniamo le due settimane per scorrerle in ordine
    per_nonni = [("corrente", cal["corrente"]), ("prossima", cal["prossima"])]
    
    for id_sett, giorni in per_nonni:
        for nome_g, info in giorni.items():
            # Filtro: Mostra solo se la data è oggi o nel futuro
            if info["data_obj"] >= cal["oggi_obj"]:
                mostrati += 1
                imp = programma[id_sett][nome_g]
                
                # Header Giorno
                if info["data_obj"] == cal["oggi_obj"]:
                    st.markdown(f"## 🌟 {info['data_testo'].upper()} (OGGI)")
                else:
                    st.markdown(f"### 📅 {info['data_testo']}")
                
                # Display Mattina
                t_mat = f"**☀️ MATTINA:** {imp['mattina']['cosa']}"
                if imp['mattina']['cosa'] == "Scuola 🏫": t_mat += "\n\n👉 *Ore 7:00 a casa!*"
                if "NONNI" in imp['mattina']['chi']: st.error(t_mat)
                else: st.success(t_mat)
                
                # Display Pomeriggio
                if imp.get("sara_uguale", True):
                    t_ins = f"**👦👧 LEO E SARA ({imp['pomeriggio_leo']['inizio']}-{imp['pomeriggio_leo']['fine']}):**\n\n{imp['pomeriggio_leo']['cosa']}"
                    if "NONNI" in imp['pomeriggio_leo']['chi']: st.error(t_ins)
                    else: st.success(t_ins)
                else:
                    t_l = f"**👦 LEO ({imp['pomeriggio_leo']['inizio']}-{imp['pomeriggio_leo']['fine']}):** {imp['pomeriggio_leo']['cosa']}"
                    t_s = f"**👧 SARA ({imp['pomeriggio_sara']['inizio']}-{imp['pomeriggio_sara']['fine']}):** {imp['pomeriggio_sara']['cosa']}"
                    if "NONNI" in imp['pomeriggio_leo']['chi']: st.error(t_l)
                    else: st.success(t_l)
                    if "NONNI" in imp['pomeriggio_sara']['chi']: st.error(t_s)
                    else: st.success(t_s)
                st.markdown("---")
    
    if mostrati == 0: st.info("Riposo! Non ci sono impegni imminenti. ☕")

# --- MODIFICA GENITORI (Con scelta settimana) ---
with sch_genitori:
    st.title("⚙️ Programmazione")
    
    col_s, col_g = st.columns(2)
    sett_scelta = col_s.radio("Settimana:", ["corrente", "prossima"], horizontal=True, format_func=lambda x: "Questa" if x=="corrente" else "La Prossima")
    
    # Filtriamo i giorni selezionabili: solo quelli da oggi in poi
    opzioni_giorni = []
    for nome_g, info in cal[sett_scelta].items():
        if info["data_obj"] >= cal["oggi_obj"]:
            opzioni_giorni.append(nome_g)
            
    if not opzioni_giorni:
        st.warning("Non puoi modificare giorni passati. Seleziona 'La Prossima' settimana.")
        giorno_sel = None
    else:
        giorno_sel = col_g.selectbox("Giorno:", opzioni_giorni, format_func=lambda x: cal[sett_scelta][x]["data_testo"])

    if giorno_sel:
        # Carichiamo i dati correnti del giorno scelto
        dati_g = programma[sett_scelta][giorno_sel]
        
        st.subheader("☀️ Mattina")
        c1, c2 = st.columns(2)
        chi_m = c1.selectbox("Chi?", OPZIONI_CHI, index=OPZIONI_CHI.index(dati_g["mattina"]["chi"]), key="m1")
        cos_m = c2.selectbox("Cosa?", OPZIONI_ATTIVITA, index=OPZIONI_ATTIVITA.index(dati_g["mattina"]["cosa"]), key="m2")
        
        st.markdown("---")
        st.subheader("👦 Pomeriggio LEO")
        c3, c4 = st.columns(2)
        chi_l = c3.selectbox("Chi?", OPZIONI_CHI, index=OPZIONI_CHI.index(dati_g["pomeriggio_leo"]["chi"]), key="l1")
        cos_l = c4.selectbox("Attività?", OPZIONI_ATTIVITA, index=OPZIONI_ATTIVITA.index(dati_g["pomeriggio_leo"]["cosa"]), key="l2")
        c5, c6 = st.columns(2)
        in_l = c5.text_input("Inizio", dati_g["pomeriggio_leo"]["inizio"])
        fi_l = c6.text_input("Fine", dati_g["pomeriggio_leo"]["fine"])

        sara_uguale = st.checkbox("✅ Sara fa lo stesso di Leo", value=dati_g.get("sara_uguale", True))
        
        if not sara_uguale:
            st.subheader("👧 Pomeriggio SARA")
            c7, c8 = st.columns(2)
            chi_s = c7.selectbox("Chi?", OPZIONI_CHI, index=OPZIONI_CHI.index(dati_g["pomeriggio_sara"]["chi"]), key="s1")
            cos_s = c8.selectbox("Attività?", OPZIONI_ATTIVITA, index=OPZIONI_ATTIVITA.index(dati_g["pomeriggio_sara"]["cosa"]), key="s2")
            c9, c10 = st.columns(2)
            in_s = c9.text_input("Inizio Sara", dati_g["pomeriggio_sara"]["inizio"])
            fi_s = c10.text_input("Fine Sara", dati_g["pomeriggio_sara"]["fine"])

        if st.button("💾 SALVA PROGRAMMA"):
            programma[sett_scelta][giorno_sel]["mattina"] = {"chi": chi_m, "cosa": cos_m}
            programma[sett_scelta][giorno_sel]["pomeriggio_leo"] = {"chi": chi_l, "cosa": cos_l, "inizio": in_l, "fine": fi_l}
            programma[sett_scelta][giorno_sel]["sara_uguale"] = sara_uguale
            if sara_uguale:
                programma[sett_scelta][giorno_sel]["pomeriggio_sara"] = programma[sett_scelta][giorno_sel]["pomeriggio_leo"].copy()
            else:
                programma[sett_scelta][giorno_sel]["pomeriggio_sara"] = {"chi": chi_s, "cosa": cos_s, "inizio": in_s, "fine": fi_s}
            salva_programma(programma)
            st.success("Salvato!")
            st.rerun()
