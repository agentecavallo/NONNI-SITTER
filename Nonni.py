import streamlit as st
import json
import os
from datetime import datetime, timedelta

# 1. IMPOSTAZIONI PAGINA
st.set_page_config(page_title="Taxi Nipoti", page_icon="🚕", layout="centered")

FILE_MEMORIA = "programma_v6.json" # Cambiato per attivare i nuovi automatismi
OPZIONI_CHI = ["🔴 TOCCA AI NONNI", "🟢 FACCIAMO NOI GENITORI"]
OPZIONI_ATTIVITA = ["Ginnastica Artistica 🤸‍♀️", "Eufonio 🎺", "Yoga 🧘‍♂️", "Musica 🎵", "Scuola 🏫"]

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
            "mattina": {"chi": "🔴 TOCCA AI NONNI", "cosa": "Scuola 🏫"},
            "sara_uguale": True,
            "pomeriggio_leonardo": {"chi": "🟢 FACCIAMO NOI GENITORI", "cosa": "Scuola 🏫", "inizio": "", "fine": ""},
            "pomeriggio_sara": {"chi": "🟢 FACCIAMO NOI GENITORI", "cosa": "Scuola 🏫", "inizio": "", "fine": ""}
        } for g in ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì"]}
    return {"corrente": sett_vuota(), "prossima": sett_vuota()}

def carica_programma():
    if os.path.exists(FILE_MEMORIA):
        try:
            with open(FILE_MEMORIA, "r", encoding="utf-8") as file:
                return json.load(file)
        except:
            return crea_struttura_vuota()
    return crea_struttura_vuota()

def salva_programma(dati):
    with open(FILE_MEMORIA, "w", encoding="utf-8") as file:
        json.dump(dati, file, indent=4)

# Inizializzazione dati
cal = ottieni_calendario()
programma = carica_programma()

# ==========================================
# 3. INTERFACCIA (TABS)
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
                
                # --- Titolo Giorno ---
                if info["data_obj"] == cal["oggi_obj"]:
                    st.markdown(f"## 🌟 {info['data_testo'].upper()} (OGGI)")
                else:
                    st.markdown(f"### 📅 {info['data_testo']}")
                
                # --- LOGICA MATTINA ---
                if "NONNI" in imp['mattina']['chi']:
                    st.error(f"**☀️ MATTINA:** Scuola 🏫\n\n👉 *Ore 7:00 vi aspettiamo a casa!*")
                else:
                    st.success(f"**☀️ MATTINA:** Scuola 🏫")
                
                # --- LOGICA POMERIGGIO E SEMAFORI ---
                chi_l_str = imp['pomeriggio_leonardo']['chi']
                chi_s_str = imp['pomeriggio_sara']['chi']
                
                # Estraiamo il bollino in base a chi deve andare
                bollino_l = "🔴 (NONNI)" if "NONNI" in chi_l_str else "🟢 (GENITORI)"
                bollino_s = "🔴 (NONNI)" if "NONNI" in chi_s_str else "🟢 (GENITORI)"
                
                # Funzione per formattare il blocco con il semaforo in evidenza
                def formatta_blocco(nome, emoji, dati, bollino):
                    if dati['cosa'] == "Scuola 🏫":
                        return f"**{emoji} {nome}:** {dati['cosa']}"
                    else:
                        return f"**{emoji} {nome}:** {dati['cosa']}\n\n**👉 Orario: {bollino} {dati['inizio']} - {dati['fine']}**"

                # Controllo se possiamo unirli (stessa persona, stessa attività, STESSI ORARI)
                identici = (
                    imp.get("sara_uguale", True) and
                    chi_l_str == chi_s_str and
                    imp['pomeriggio_leonardo']['cosa'] == imp['pomeriggio_sara']['cosa'] and
                    imp['pomeriggio_leonardo']['inizio'] == imp['pomeriggio_sara']['inizio'] and
                    imp['pomeriggio_leonardo']['fine'] == imp['pomeriggio_sara']['fine']
                )

                if identici:
                    t_ins = formatta_blocco("LEONARDO E SARA", "👦👧", imp['pomeriggio_leonardo'], bollino_l)
                    if "NONNI" in chi_l_str: st.error(t_ins)
                    else: st.success(t_ins)
                else:
                    # Leonardo
                    t_l = formatta_blocco("LEONARDO", "👦", imp['pomeriggio_leonardo'], bollino_l)
                    if "NONNI" in chi_l_str: st.error(t_l)
                    else: st.success(t_l)
                    
                    # Sara
                    t_s = formatta_blocco("SARA", "👧", imp['pomeriggio_sara'], bollino_s)
                    if "NONNI" in chi_s_str: st.error(t_s)
                    else: st.success(t_s)
                
                st.markdown("---")

# --- PANNELLO GENITORI ---
with sch_genitori:
    st.title("⚙️ Programmazione")
    col_s, col_g = st.columns(2)
    
    sett_scelta = col_s.radio("Settimana:", ["corrente", "prossima"], horizontal=True, format_func=lambda x: "Questa" if x=="corrente" else "La Prossima")
    
    opzioni_giorni = [n for n, i in cal[sett_scelta].items() if i["data_obj"] >= cal["oggi_obj"]]
    
    if not opzioni_giorni and sett_scelta == "corrente":
        st.warning("La settimana corrente è terminata. Seleziona 'La Prossima'.")
        giorno_sel = None
    else:
        giorno_sel = col_g.selectbox("Giorno:", opzioni_giorni, format_func=lambda x: cal[sett_scelta][x]["data_testo"])

    if giorno_sel:
        dati_g = programma[sett_scelta][giorno_sel]
        
        # Gestione MATTINA
        st.subheader("☀️ Mattina: Scuola 🏫")
        chi_m = st.selectbox("Chi accompagna a scuola?", OPZIONI_CHI, index=OPZIONI_CHI.index(dati_g["mattina"]["chi"]), key="m_chi")
        
        st.markdown("---")
        
        # Gestione LEONARDO
        st.subheader("👦 Pomeriggio LEONARDO")
        c3, c4 = st.columns(2)
        chi_l = c3.selectbox("Chi?", OPZIONI_CHI, index=OPZIONI_CHI.index(dati_g["pomeriggio_leonardo"]["chi"]), key="l1")
        
        idx_cosa_l = OPZIONI_ATTIVITA.index(dati_g["pomeriggio_leonardo"]["cosa"]) if dati_g["pomeriggio_leonardo"]["cosa"] in OPZIONI_ATTIVITA else OPZIONI_ATTIVITA.index("Scuola 🏫")
        cos_l = c4.selectbox("Attività?", OPZIONI_ATTIVITA, index=idx_cosa_l, key="l2")
        
        # Automatismi Orari Leonardo
        if cos_l == "Scuola 🏫":
            in_l, fi_l = "", ""
        elif cos_l == "Ginnastica Artistica 🤸‍♀️":
            st.info("⏱️ Orari Ginnastica prefissati per Leo: **17:00 - 18:30**")
            in_l, fi_l = "17:00", "18:30"
        else:
            c5, c6 = st.columns(2)
            in_l = c5.text_input("Inizio", dati_g["pomeriggio_leonardo"]["inizio"], key="l_in")
            fi_l = c6.text_input("Fine", dati_g["pomeriggio_leonardo"]["fine"], key="l_fi")

        # Checkbox SARA
        sara_uguale = st.checkbox("✅ Sara fa lo stesso di Leonardo", value=dati_g.get("sara_uguale", True))
        
        # Gestione SARA
        if not sara_uguale:
            st.subheader("👧 Pomeriggio SARA")
            c7, c8 = st.columns(2)
            chi_s = c7.selectbox("Chi?", OPZIONI_CHI, index=OPZIONI_CHI.index(dati_g["pomeriggio_sara"]["chi"]), key="s1")
            
            idx_cosa_s = OPZIONI_ATTIVITA.index(dati_g["pomeriggio_sara"]["cosa"]) if dati_g["pomeriggio_sara"]["cosa"] in OPZIONI_ATTIVITA else OPZIONI_ATTIVITA.index("Scuola 🏫")
            cos_s = c8.selectbox("Attività?", OPZIONI_ATTIVITA, index=idx_cosa_s, key="s2")
            
            # Automatismi Orari Sara
            if cos_s == "Scuola 🏫":
                in_s, fi_s = "", ""
            elif cos_s == "Ginnastica Artistica 🤸‍♀️":
                st.info("⏱️ Orari Ginnastica prefissati per Sara: **16:30 - 17:30**")
                in_s, fi_s = "16:30", "17:30"
            else:
                c9, c10 = st.columns(2)
                in_s = c9.text_input("Inizio Sara", dati_g["pomeriggio_sara"]["inizio"], key="s_in")
                fi_s = c10.text_input("Fine Sara", dati_g["pomeriggio_sara"]["fine"], key="s_fi")
        else:
            # Sincronizzazione Intelligente:
            chi_s = chi_l
            cos_s = cos_l
            
            # Anche se fanno "la stessa cosa", controlliamo gli orari specifici se è ginnastica
            if cos_s == "Ginnastica Artistica 🤸‍♀️":
                in_s, fi_s = "16:30", "17:30"
            elif cos_s == "Scuola 🏫":
                in_s, fi_s = "", ""
            else:
                in_s, fi_s = in_l, fi_l

        if st.button("💾 SALVA PROGRAMMA"):
            programma[sett_scelta][giorno_sel] = {
                "mattina": {"chi": chi_m, "cosa": "Scuola 🏫"},
                "pomeriggio_leonardo": {"chi": chi_l, "cosa": cos_l, "inizio": in_l, "fine": fi_l},
                "sara_uguale": sara_uguale,
                "pomeriggio_sara": {"chi": chi_s, "cosa": cos_s, "inizio": in_s, "fine": fi_s}
            }
            salva_programma(programma)
            st.success("Programma salvato con successo!")
            st.rerun()
