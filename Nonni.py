import streamlit as st
import json
import os
from datetime import datetime, timedelta

# 1. IMPOSTAZIONI PAGINA
st.set_page_config(page_title="Taxi Nipoti", page_icon="🚕", layout="centered")

FILE_MEMORIA = "programma_v3.json"
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

def crea_struttura_vuota():
    def sett_vuota():
        return {g: {
            "mattina": {"chi": "🟢 FACCIAMO NOI GENITORI", "cosa": "Scuola 🏫"},
            "sara_uguale": True,
            "pomeriggio_leo": {"chi": "🟢 FACCIAMO NOI GENITORI", "cosa": "Casa 🏠", "inizio": "16:30", "fine": "18:00"},
            "pomeriggio_sara": {"chi": "🟢 FACCIAMO NOI GENITORI", "cosa": "Casa 🏠", "inizio": "16:30", "fine": "18:00"}
        } for g in ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì"]}
    return {"corrente": sett_vuota(), "prossima": sett_vuota()}

def carica_programma():
    if os.path.exists(FILE_MEMORIA):
        try:
            with open(FILE_MEMORIA, "r", encoding="utf-8") as file: return json.load(file)
        except: return crea_struttura_vuota()
    return crea_struttura_vuota()

def salva_programma():
    with open(FILE_MEMORIA, "w", encoding="utf-8") as file:
        json.dump(st.session_state.programma, file, indent=4)

# Inizializzazione dati nella sessione (per evitare reset continui)
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
                
                # Header con stella se oggi
                if info["data_obj"] == cal["oggi_obj"]:
                    st.markdown(f"## 🌟 {info['data_testo'].upper()} (OGGI)")
                else:
                    st.markdown(f"### 📅 {info['data_testo']}")
                
                # Mattina
                t_mat = f"**☀️ MATTINA:** Scuola 🏫\n\n👉 *Ore 7:00 a casa!*"
                if "GENITORI" in imp['mattina']['chi']: st.success(t_mat)
                else: st.error(t_mat)
                
                # Pomeriggio
                if imp.get("sara_uguale", True):
                    t_ins = f"**👦👧 LEO E SARA ({imp['pomeriggio_leo']['inizio']}-{imp['pomeriggio_leo']['fine']}):**\n\n{imp['pomeriggio_leo']['cosa']}"
                    if "GENITORI" in imp['pomeriggio_leo']['chi']: st.success(t_ins)
                    else: st.error(t_ins)
                else:
                    # Leo
                    t_l = f"**👦 LEO ({imp['pomeriggio_leo']['inizio']}-{imp['pomeriggio_leo']['fine']}):** {imp['pomeriggio_leo']['cosa']}"
                    if "GENITORI" in imp['pomeriggio_leo']['chi']: st.success(t_l)
                    else: st.error(t_l)
                    # Sara
                    t_s = f"**👧 SARA ({imp['pomeriggio_sara']['inizio']}-{imp['pomeriggio_sara']['fine']}):** {imp['pomeriggio_sara']['cosa']}"
                    if "GENITORI" in imp['pomeriggio_sara']['chi']: st.success(t_s)
                    else: st.error(t_s)
                st.markdown("---")

# --- MODIFICA GENITORI (CON SALVATAGGIO FLUIDO) ---
with sch_genitori:
    st.title("⚙️ Pannello Genitori")
    c_s, c_g = st.columns(2)
    sett_scelta = c_s.radio("Settimana:", ["corrente", "prossima"], horizontal=True, format_func=lambda x: "Questa" if x=="corrente" else "La Prossima")
    
    opzioni_g = [n for n, i in cal[sett_scelta].items() if i["data_obj"] >= cal["oggi_obj"]]
    giorno_sel = c_g.selectbox("Scegli Giorno:", opzioni_g, format_func=lambda x: cal[sett_scelta][x]["data_testo"])

    if giorno_sel:
        # Recupero dati per brevità
        d = st.session_state.programma[sett_scelta][giorno_sel]
        
        st.subheader("☀️ Mattina: Scuola 🏫")
        d["mattina"]["chi"] = st.selectbox("Chi accompagna?", OPZIONI_CHI, 
                                          index=OPZIONI_CHI.index(d["mattina"]["chi"]), 
                                          key=f"m_chi_{giorno_sel}_{sett_scelta}", on_change=salva_programma)
        
        st.markdown("---")
        st.subheader("👦 Pomeriggio LEO")
        col1, col2 = st.columns(2)
        d["pomeriggio_leo"]["chi"] = col1.selectbox("Chi?", OPZIONI_CHI, 
                                                  index=OPZIONI_CHI.index(d["pomeriggio_leo"]["chi"]), 
                                                  key=f"l_chi_{giorno_sel}_{sett_scelta}", on_change=salva_programma)
        d["pomeriggio_leo"]["cosa"] = col2.selectbox("Attività?", OPZIONI_ATTIVITA, 
                                                   index=OPZIONI_ATTIVITA.index(d["pomeriggio_leo"]["cosa"]) if d["pomeriggio_leo"]["cosa"] in OPZIONI_ATTIVITA else 0, 
                                                   key=f"l_cos_{giorno_sel}_{sett_scelta}", on_change=salva_programma)
        
        col3, col4 = st.columns(2)
        d["pomeriggio_leo"]["inizio"] = col3.text_input("Inizio", d["pomeriggio_leo"]["inizio"], key=f"l_in_{giorno_sel}_{sett_scelta}", on_change=salva_programma)
        d["pomeriggio_leo"]["fine"] = col4.text_input("Fine", d["pomeriggio_leo"]["fine"], key=f"l_fi_{giorno_sel}_{sett_scelta}", on_change=salva_programma)

        d["sara_uguale"] = st.checkbox("✅ Sara fa lo stesso di Leo", value=d.get("sara_uguale", True), key=f"s_ug_{giorno_sel}_{sett_scelta}", on_change=salva_programma)
        
        if not d["sara_uguale"]:
            st.subheader("👧 Pomeriggio SARA")
            col5, col6 = st.columns(2)
            d["pomeriggio_sara"]["chi"] = col5.selectbox("Chi Sara?", OPZIONI_CHI, index=OPZIONI_CHI.index(d["pomeriggio_sara"]["chi"]), key=f"s_chi_{giorno_sel}_{sett_scelta}", on_change=salva_programma)
            d["pomeriggio_sara"]["cosa"] = col6.selectbox("Attività Sara?", OPZIONI_ATTIVITA, index=OPZIONI_ATTIVITA.index(d["pomeriggio_sara"]["cosa"]) if d["pomeriggio_sara"]["cosa"] in OPZIONI_ATTIVITA else 0, key=f"s_cos_{giorno_sel}_{sett_scelta}", on_change=salva_programma)
            
            col7, col8 = st.columns(2)
            d["pomeriggio_sara"]["inizio"] = col7.text_input("Inizio Sara", d["pomeriggio_sara"]["inizio"], key=f"s_in_{giorno_sel}_{sett_scelta}", on_change=salva_programma)
            d["pomeriggio_sara"]["fine"] = col8.text_input("Fine Sara", d["pomeriggio_sara"]["fine"], key=f"s_fi_{giorno_sel}_{sett_scelta}", on_change=salva_programma)
        else:
            # Sincronizza Sara con Leo se la spunta è attiva
            d["pomeriggio_sara"] = d["pomeriggio_leo"].copy()
            
        st.caption("✅ Le modifiche vengono salvate istantaneamente.")
