import streamlit as st
import json
import os
from datetime import datetime, timedelta

# 1. IMPOSTAZIONI PAGINA
st.set_page_config(page_title="Taxi Nipoti", page_icon="🚕", layout="centered")

FILE_MEMORIA = "programma_v3.json" # Aggiornato per riflettere la nuova logica semplificata
OPZIONI_CHI = ["🔴 TOCCA AI NONNI", "🟢 FACCIAMO NOI GENITORI"]
OPZIONI_ATTIVITA = ["Ginnastica Artistica 🤸‍♀️", "Eufonio 🎺", "Yoga 🧘‍♂️", "Musica 🎵", "Casa 🏠"]

# --- FUNZIONE CALENDARIO ---
def ottieni_calendario():
    oggi = datetime.now().date()
    lunedi_curr = oggi - timedelta(days=oggi.weekday())
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

    return {"corrente": formatta_settimana(lunedi_curr), "prossima": formatta_settimana(lunedi_next), "oggi_obj": oggi}

# 2. GESTIONE MEMORIA
def crea_struttura_vuota():
    def sett_vuota():
        return {g: {
            "mattina": {"chi": "🔴 TOCCA AI NONNI", "cosa": "Scuola 🏫"}, # "cosa" ora è fisso
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

cal = ottieni_calendario()
programma = carica_programma()

# ==========================================
# 3. INTERFACCIA (TABS)
# ==========================================
sch_nonni, sch_genitori = st.tabs(["🚕 Vista Nonni", "⚙️ Pannello Genitori"])

# --- VISTA NONNI (Invariata, mostra sempre Scuola la mattina) ---
with sch_nonni:
    st.title("🚕 Il Taxi dei Nipoti")
    st.markdown("---")
    mostrati = 0
    per_nonni = [("corrente", cal["corrente"]), ("prossima", cal["prossima"])]
    
    for id_sett, giorni in per_nonni:
        for nome_g, info in giorni.items():
            if info["data_obj"] >= cal["oggi_obj"]:
                mostrati += 1
                imp = programma[id_sett][nome_g]
                
                if info["data_obj"] == cal["oggi_obj"]:
                    st.markdown(f"## 🌟 {info['data_testo'].upper()} (OGGI)")
                else:
                    st.markdown(f"### 📅 {info['data_testo']}")
                
                # MATTINA: Sempre Scuola
                t_mat = f"**☀️ MATTINA:** Scuola 🏫\n\n👉 *Ore 7:00 a casa!*"
                if "NONNI" in imp['mattina']['chi']: st.error(t_mat)
                else: st.success(t_mat)
                
                # POMERIGGIO
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

# --- MODIFICA GENITORI (Semplificata) ---
with sch_genitori:
    st.title("⚙️ Programmazione")
    col_s, col_g = st.columns(2)
    sett_scelta = col_s.radio("Settimana:", ["corrente", "prossima"], horizontal=True, format_func=lambda x: "Questa" if x=="corrente" else "La Prossima")
    
    opzioni_giorni = [n for n, i in cal[sett_scelta].items() if i["data_obj"] >= cal["oggi_obj"]]
    if not opzioni_giorni:
        st.warning("Seleziona 'La Prossima' settimana.")
        giorno_sel = None
    else:
        giorno_sel = col_g.selectbox("Giorno:", opzioni_giorni, format_func=lambda x: cal[sett_scelta][x]["data_testo"])

    if giorno_sel:
        dati_g = programma[sett_scelta][giorno_sel]
        
        # MATTINA SEMPLIFICATA: Solo scelta colore
        st.subheader("☀️ Mattina: Scuola 🏫")
        chi_m = st.selectbox("Chi accompagna a scuola?", OPZIONI_CHI, index=OPZIONI_CHI.index(dati_g["mattina"]["chi"]), key="m_chi")
        
        st.markdown("---")
        st.subheader("👦 Pomeriggio LEO")
        c3, c4 = st.columns(2)
        chi_l = c3.selectbox("Chi?", OPZIONI_CHI, index=OPZIONI_CHI.index(dati_g["pomeriggio_leo"]["chi"]), key="l1")
        cos_l = c4.selectbox("Attività?", OPZIONI_ATTIVITA, index=OPZIONI_ATTIVITA.index(dati_g["pomeriggio_leo"]["cosa"]) if dati_g["pomeriggio_leo"]["cosa"] in OPZIONI_ATTIVITA else 0, key="l2")
        c5, c6 = st.columns(2)
        in_l = st.text_input("Inizio", dati_g["pomeriggio_leo"]["inizio"], key="l_in")
        fi_l = st.text_input("Fine", dati_g["pomeriggio_leo"]["fine"], key="l_fi")

        sara_uguale = st.checkbox("✅ Sara fa lo stesso di Leo", value=dati_g.get("sara_uguale", True))
        
        if not sara_uguale:
            st.subheader("👧 Pomeriggio SARA")
            c7, c8 = st.columns(2)
            chi_s = c7.selectbox("Chi?", OPZIONI_CHI, index=OPZIONI_CHI.index(dati_g["pomeriggio_sara"]["chi"]), key="s1")
            cos_s = c8.selectbox("Attività?", OPZIONI_ATTIVITA, index=OPZIONI_ATTIVITA.index(dati_g["pomeriggio_sara"]["cosa"]) if dati_g["pomeriggio_sara"]["cosa"] in OPZIONI_ATTIVITA else 0, key="s2")
            in_s = st.text_input("Inizio Sara", dati_g["pomeriggio_sara"]["inizio"], key="s_in")
            fi_s = st.text_input("Fine Sara", dati_g["pomeriggio_sara"]["fine"], key="s_fi")

        if st.button("💾 SALVA PROGRAMMA"):
            programma[sett_scelta][giorno_sel]["mattina"] = {"chi": chi_m, "cosa": "Scuola 🏫"}
            programma[sett_scelta][giorno_sel]["pomeriggio_leo"] = {"chi": chi_l, "cosa": cos_l, "inizio": in_l, "fine": fi_l}
            programma[sett_scelta][giorno_sel]["sara_uguale"] = sara_uguale
            if sara_uguale:
                programma[sett_scelta][giorno_sel]["pomeriggio_sara"] = programma[sett_scelta][giorno_sel]["pomeriggio_leo"].copy()
            else:
                programma[sett_scelta][giorno_sel]["pomeriggio_sara"] = {"chi": chi_s, "cosa": cos_s, "inizio": in_s, "fine": fi_s}
            salva_programma(programma)
            st.success("Salvato!")
            st.rerun()
