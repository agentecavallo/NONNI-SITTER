import streamlit as st
import json
import os
from datetime import datetime, timedelta

# 1. IMPOSTAZIONI PAGINA
st.set_page_config(page_title="Taxi Nipoti", page_icon="🚕", layout="centered")

FILE_MEMORIA = "programma_v3.json"
OPZIONI_CHI = ["🟢 FACCIAMO NOI GENITORI", "🔴 TOCCA AI NONNI"] # Invertito ordine per default verde
OPZIONI_ATTIVITA = ["Ginnastica Artistica 🤸‍♀️", "Eufonio 🎺", "Yoga 🧘‍♂️", "Musica 🎵", "Casa 🏠"]

# --- FUNZIONI CORE ---
def ottieni_calendario():
    oggi = datetime.now().date()
    lunedi_curr = oggi - timedelta(days=oggi.weekday())
    lunedi_next = lunedi_curr + timedelta(days=7)
    mesi = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]
    
    def formatta(base):
        return {["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì"][i]: {
            "data_testo": f"{['Lunedì', 'Martedì', 'Mercoledì', 'Giovedì', 'Venerdì'][i]} {(base + timedelta(days=i)).day} {mesi[(base + timedelta(days=i)).month-1]} {(base + timedelta(days=i)).year}",
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

def salva_programma(dati):
    with open(FILE_MEMORIA, "w", encoding="utf-8") as file:
        json.dump(dati, file, indent=4)

cal = ottieni_calendario()
programma = carica_programma()

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
                imp = programma[id_sett][nome_g]
                st.markdown(f"## 🌟 {info['data_testo'].upper()}" if info["data_obj"] == cal["oggi_obj"] else f"### 📅 {info['data_testo']}")
                
                t_mat = f"**☀️ MATTINA:** Scuola 🏫\n\n👉 *Ore 7:00 a casa!*"
                st.success(t_mat) if "GENITORI" in imp['mattina']['chi'] else st.error(t_mat)
                
                if imp.get("sara_uguale", True):
                    t_ins = f"**👦👧 LEO E SARA ({imp['pomeriggio_leo']['inizio']}-{imp['pomeriggio_leo']['fine']}):**\n\n{imp['pomeriggio_leo']['cosa']}"
                    st.success(t_ins) if "GENITORI" in imp['pomeriggio_leo']['chi'] else st.error(t_ins)
                else:
                    for f, k in [("👦 LEO", "pomeriggio_leo"), ("👧 SARA", "pomeriggio_sara")]:
                        t = f"**{f} ({imp[k]['inizio']}-{imp[k]['fine']}):** {imp[k]['cosa']}"
                        st.success(t) if "GENITORI" in imp[k]['chi'] else st.error(t)
                st.markdown("---")

# --- MODIFICA GENITORI (AUTOSAVE) ---
with sch_genitori:
    st.title("⚙️ Programmazione")
    col_s, col_g = st.columns(2)
    sett_scelta = col_s.radio("Settimana:", ["corrente", "prossima"], horizontal=True, format_func=lambda x: "Questa" if x=="corrente" else "La Prossima")
    
    opzioni_giorni = [n for n, i in cal[sett_scelta].items() if i["data_obj"] >= cal["oggi_obj"]]
    giorno_sel = col_g.selectbox("Giorno:", opzioni_giorni, format_func=lambda x: cal[sett_scelta][x]["data_testo"])

    if giorno_sel:
        # Carichiamo i dati attuali
        d = programma[sett_scelta][giorno_sel]
        
        st.subheader("☀️ Mattina: Scuola 🏫")
        # Ogni widget ha un 'on_change' che salva immediatamente
        new_chi_m = st.selectbox("Chi accompagna?", OPZIONI_CHI, index=OPZIONI_CHI.index(d["mattina"]["chi"]), key="m_chi")
        
        st.markdown("---")
        st.subheader("👦 Pomeriggio LEO")
        c1, c2 = st.columns(2)
        new_chi_l = c1.selectbox("Chi?", OPZIONI_CHI, index=OPZIONI_CHI.index(d["pomeriggio_leo"]["chi"]), key="l_chi")
        new_cos_l = c2.selectbox("Attività?", OPZIONI_ATTIVITA, index=OPZIONI_ATTIVITA.index(d["pomeriggio_leo"]["cosa"]) if d["pomeriggio_leo"]["cosa"] in OPZIONI_ATTIVITA else 0, key="l_cos")
        
        c3, c4 = st.columns(2)
        new_in_l = st.text_input("Inizio", d["pomeriggio_leo"]["inizio"], key="l_in")
        new_fi_l = st.text_input("Fine", d["pomeriggio_leo"]["fine"], key="l_fi")

        new_sara_uguale = st.checkbox("✅ Sara fa lo stesso di Leo", value=d.get("sara_uguale", True), key="s_ug")
        
        # Logica per Sara
        if not new_sara_uguale:
            st.subheader("👧 Pomeriggio SARA")
            c5, c6 = st.columns(2)
            new_chi_s = c5.selectbox("Chi Sara?", OPZIONI_CHI, index=OPZIONI_CHI.index(d["pomeriggio_sara"]["chi"]), key="s_chi")
            new_cos_s = c6.selectbox("Attività Sara?", OPZIONI_ATTIVITA, index=OPZIONI_ATTIVITA.index(d["pomeriggio_sara"]["cosa"]) if d["pomeriggio_sara"]["cosa"] in OPZIONI_ATTIVITA else 0, key="s_cos")
            new_in_s = st.text_input("Inizio Sara", d["pomeriggio_sara"]["inizio"], key="s_in")
            new_fi_s = st.text_input("Fine Sara", d["pomeriggio_sara"]["fine"], key="s_fi")
        else:
            new_chi_s, new_cos_s, new_in_s, new_fi_s = new_chi_l, new_cos_l, new_in_l, new_fi_l

        # AGGIORNAMENTO DATI (Salvataggio automatico ad ogni interazione)
        programma[sett_scelta][giorno_sel] = {
            "mattina": {"chi": new_chi_m, "cosa": "Scuola 🏫"},
            "sara_uguale": new_sara_uguale,
            "pomeriggio_leo": {"chi": new_chi_l, "cosa": new_cos_l, "inizio": new_in_l, "fine": new_fi_l},
            "pomeriggio_sara": {"chi": new_chi_s, "cosa": new_cos_s, "inizio": new_in_s, "fine": new_fi_s}
        }
        salva_programma(programma)
        st.caption("✨ Modifiche salvate automaticamente")
