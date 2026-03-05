import streamlit as st
import json
import os
from datetime import datetime, timedelta

# 1. IMPOSTAZIONI PAGINA
st.set_page_config(page_title="Taxi Nipoti", page_icon="🚕", layout="centered")

FILE_MEMORIA = "programma_v8.json" # Aggiornato per le nuove istruzioni di tragitto
OPZIONI_CHI = ["🟢 FACCIAMO NOI GENITORI", "🔴 TOCCA AI NONNI"]
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
            "mattina": {"chi": "🟢 FACCIAMO NOI GENITORI", "cosa": "Scuola 🏫"},
            "sara_uguale": True,
            "pomeriggio_leonardo": {"chi_andata": "🟢 FACCIAMO NOI GENITORI", "chi_ritorno": "🟢 FACCIAMO NOI GENITORI", "cosa": "Scuola 🏫", "inizio": "", "fine": ""},
            "pomeriggio_sara": {"chi_andata": "🟢 FACCIAMO NOI GENITORI", "chi_ritorno": "🟢 FACCIAMO NOI GENITORI", "cosa": "Scuola 🏫", "inizio": "", "fine": ""}
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
# 3. INTERFACCIA A SCHEDE
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
                
                # Titolo Giorno
                if info["data_obj"] == cal["oggi_obj"]:
                    st.markdown(f"## 🌟 {info['data_testo'].upper()} (OGGI)")
                else:
                    st.markdown(f"### 📅 {info['data_testo']}")
                
                # --- MATTINA ---
                if "NONNI" in imp['mattina']['chi']:
                    st.error(f"**☀️ MATTINA:** Scuola 🏫\n\n👉 *Ore 7:00 vi aspettiamo a casa!*")
                else:
                    st.success(f"**☀️ MATTINA:** Scuola 🏫")
                
                # --- LOGICA POMERIGGIO CON ISTRUZIONI ESPLICITE SUL TRAGITTO ---
                def formatta_blocco(nome, emoji, dati):
                    if dati['cosa'] == "Scuola 🏫":
                        bollino = "🔴 (NONNI)" if "NONNI" in dati['chi_ritorno'] else "🟢 (GENITORI)"
                        return f"**{emoji} {nome}:** Fine giornata a Scuola 🏫\n\n👉 **Chi li riprende da Scuola:** {bollino}"
                    else:
                        b_andata = "🔴 (NONNI)" if "NONNI" in dati['chi_andata'] else "🟢 (GENITORI)"
                        b_ritorno = "🔴 (NONNI)" if "NONNI" in dati['chi_ritorno'] else "🟢 (GENITORI)"
                        attivita = dati['cosa'].upper()
                        
                        return (f"**{emoji} {nome}:** {dati['cosa']}\n\n"
                                f"👉 **Andata (ore {dati['inizio']}):** {b_andata}\n"
                                f"*(📍 Prendere a Scuola 🏫 e portare a {attivita})*\n\n"
                                f"👉 **Ritorno (ore {dati['fine']}):** {b_ritorno}\n"
                                f"*(📍 Riprendere da {attivita} e portare a Casa 🏠)*")

                # Leonardo
                t_l = formatta_blocco("LEONARDO", "👦", imp['pomeriggio_leonardo'])
                coinvolge_nonni_l = "NONNI" in imp['pomeriggio_leonardo']['chi_andata'] or "NONNI" in imp['pomeriggio_leonardo']['chi_ritorno']
                
                # Sara
                t_s = formatta_blocco("SARA", "👧", imp['pomeriggio_sara'])
                coinvolge_nonni_s = "NONNI" in imp['pomeriggio_sara']['chi_andata'] or "NONNI" in imp['pomeriggio_sara']['chi_ritorno']

                # Controllo se possiamo unirli in un solo blocco
                identici = (
                    imp.get("sara_uguale", True) and
                    imp['pomeriggio_leonardo']['chi_andata'] == imp['pomeriggio_sara']['chi_andata'] and
                    imp['pomeriggio_leonardo']['chi_ritorno'] == imp['pomeriggio_sara']['chi_ritorno'] and
                    imp['pomeriggio_leonardo']['cosa'] == imp['pomeriggio_sara']['cosa'] and
                    imp['pomeriggio_leonardo']['inizio'] == imp['pomeriggio_sara']['inizio'] and
                    imp['pomeriggio_leonardo']['fine'] == imp['pomeriggio_sara']['fine']
                )

                if identici:
                    t_ins = formatta_blocco("LEONARDO E SARA", "👦👧", imp['pomeriggio_leonardo'])
                    if coinvolge_nonni_l: st.error(t_ins)
                    else: st.success(t_ins)
                else:
                    if coinvolge_nonni_l: st.error(t_l)
                    else: st.success(t_l)
                    
                    if coinvolge_nonni_s: st.error(t_s)
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
        
        # --- MATTINA ---
        st.subheader("☀️ Mattina: Scuola 🏫")
        chi_m = st.selectbox("Chi li porta a scuola?", OPZIONI_CHI, index=OPZIONI_CHI.index(dati_g["mattina"]["chi"]), key="m_chi")
        
        st.markdown("---")
        
        # --- POMERIGGIO LEONARDO ---
        st.subheader("👦 Pomeriggio LEONARDO")
        idx_cosa_l = OPZIONI_ATTIVITA.index(dati_g["pomeriggio_leonardo"]["cosa"]) if dati_g["pomeriggio_leonardo"]["cosa"] in OPZIONI_ATTIVITA else OPZIONI_ATTIVITA.index("Scuola 🏫")
        cos_l = st.selectbox("Attività Leonardo?", OPZIONI_ATTIVITA, index=idx_cosa_l, key="l2")
        
        if cos_l == "Scuola 🏫":
            chi_and_l = OPZIONI_CHI[0]
            chi_rit_l = st.selectbox("🚕 Chi lo riprende da Scuola?", OPZIONI_CHI, index=OPZIONI_CHI.index(dati_g["pomeriggio_leonardo"]["chi_ritorno"]), key="l_rit")
            in_l, fi_l = "", ""
        else:
            c_and, c_rit = st.columns(2)
            chi_and_l = c_and.selectbox("🚕 Chi lo PORTA (Andata)?", OPZIONI_CHI, index=OPZIONI_CHI.index(dati_g["pomeriggio_leonardo"].get("chi_andata", OPZIONI_CHI[0])), key="l_and")
            chi_rit_l = c_rit.selectbox("🚕 Chi lo RIPRENDE (Ritorno)?", OPZIONI_CHI, index=OPZIONI_CHI.index(dati_g["pomeriggio_leonardo"].get("chi_ritorno", OPZIONI_CHI[0])), key="l_rit")
            
            if cos_l == "Ginnastica Artistica 🤸‍♀️":
                st.info("⏱️ Orari prefissati Leonardo: **17:00 - 18:30**")
                in_l, fi_l = "17:00", "18:30"
            else:
                c_in, c_fi = st.columns(2)
                in_l = c_in.text_input("Orario Inizio", dati_g["pomeriggio_leonardo"]["inizio"], key="l_in")
                fi_l = c_fi.text_input("Orario Fine", dati_g["pomeriggio_leonardo"]["fine"], key="l_fi")

        # --- CHECKBOX SARA ---
        sara_uguale = st.checkbox("✅ Sara fa lo stesso di Leonardo", value=dati_g.get("sara_uguale", True))
        
        # --- POMERIGGIO SARA ---
        if not sara_uguale:
            st.subheader("👧 Pomeriggio SARA")
            idx_cosa_s = OPZIONI_ATTIVITA.index(dati_g["pomeriggio_sara"]["cosa"]) if dati_g["pomeriggio_sara"]["cosa"] in OPZIONI_ATTIVITA else OPZIONI_ATTIVITA.index("Scuola 🏫")
            cos_s = st.selectbox("Attività Sara?", OPZIONI_ATTIVITA, index=idx_cosa_s, key="s2")
            
            if cos_s == "Scuola 🏫":
                chi_and_s = OPZIONI_CHI[0]
                chi_rit_s = st.selectbox("🚕 Chi la riprende da Scuola?", OPZIONI_CHI, index=OPZIONI_CHI.index(dati_g["pomeriggio_sara"]["chi_ritorno"]), key="s_rit")
                in_s, fi_s = "", ""
            else:
                c_and_s, c_rit_s = st.columns(2)
                chi_and_s = c_and_s.selectbox("🚕 Chi la PORTA (Andata)?", OPZIONI_CHI, index=OPZIONI_CHI.index(dati_g["pomeriggio_sara"].get("chi_andata", OPZIONI_CHI[0])), key="s_and")
                chi_rit_s = c_rit_s.selectbox("🚕 Chi la RIPRENDE (Ritorno)?", OPZIONI_CHI, index=OPZIONI_CHI.index(dati_g["pomeriggio_sara"].get("chi_ritorno", OPZIONI_CHI[0])), key="s_rit")
                
                if cos_s == "Ginnastica Artistica 🤸‍♀️":
                    st.info("⏱️ Orari prefissati Sara: **16:30 - 17:30**")
                    in_s, fi_s = "16:30", "17:30"
                else:
                    c_in_s, c_fi_s = st.columns(2)
                    in_s = c_in_s.text_input("Orario Inizio (S)", dati_g["pomeriggio_sara"]["inizio"], key="s_in")
                    fi_s = c_fi_s.text_input("Orario Fine (S)", dati_g["pomeriggio_sara"]["fine"], key="s_fi")
        else:
            chi_and_s, chi_rit_s, cos_s = chi_and_l, chi_rit_l, cos_l
            if cos_s == "Ginnastica Artistica 🤸‍♀️":
                in_s, fi_s = "16:30", "17:30"
            elif cos_s == "Scuola 🏫":
                in_s, fi_s = "", ""
            else:
                in_s, fi_s = in_l, fi_l

        if st.button("💾 SALVA PROGRAMMA"):
            programma[sett_scelta][giorno_sel] = {
                "mattina": {"chi": chi_m, "cosa": "Scuola 🏫"},
                "pomeriggio_leonardo": {"chi_andata": chi_and_l, "chi_ritorno": chi_rit_l, "cosa": cos_l, "inizio": in_l, "fine": fi_l},
                "sara_uguale": sara_uguale,
                "pomeriggio_sara": {"chi_andata": chi_and_s, "chi_ritorno": chi_rit_s, "cosa": cos_s, "inizio": in_s, "fine": fi_s}
            }
            salva_programma(programma)
            st.success("Programma salvato con successo!")
            st.rerun()
