import streamlit as st
import json
import os
from datetime import datetime, timedelta

# 1. IMPOSTAZIONI PAGINA
st.set_page_config(page_title="Taxi Nipoti", page_icon="🚕", layout="centered")

FILE_MEMORIA = "programma_v5.json" # Cambiato per evitare errori con il vecchio nome Leo
OPZIONI_CHI = ["🔴 TOCCA AI NONNI", "🟢 FACCIAMO NOI GENITORI"]
OPZIONI_ATTIVITA = ["Ginnastica Artistica 🤸‍♀️", "Eufonio 🎺", "Yoga 🧘‍♂️", "Musica 🎵", "Scuola 🏫"]

# --- FUNZIONE CALENDARIO ---
def ottieni_calendario():
    oggi = datetime.now().date()
    # Calcola il lunedì della settimana corrente
    lunedi_curr = oggi - timedelta(days=oggi.weekday())
    # Calcola il lunedì della settimana prossima
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
            # Mostra solo i giorni da oggi in poi
            if info["data_obj"] >= cal["oggi_obj"]:
                imp = programma[id_sett][nome_g]
                
                if info["data_obj"] == cal["oggi_obj"]:
                    st.markdown(f"## 🌟 {info['data_testo'].upper()} (OGGI)")
                else:
                    st.markdown(f"### 📅 {info['data_testo']}")
                
                # --- LOGICA MATTINA ---
                if "NONNI" in imp['mattina']['chi']:
                    st.error(f"**☀️ MATTINA:** Scuola 🏫\n\n👉 *Ore 7:00 vi aspettiamo a casa!*")
                else:
                    st.success(f"**☀️ MATTINA:** Scuola 🏫")
                
                # --- LOGICA POMERIGGIO ---
                if imp.get("sara_uguale", True):
                    # Nasconde l'orario se è Scuola
                    orari_str = "" if imp['pomeriggio_leonardo']['cosa'] == "Scuola 🏫" else f" ({imp['pomeriggio_leonardo']['inizio']}-{imp['pomeriggio_leonardo']['fine']})"
                    t_ins = f"**👦👧 LEONARDO E SARA{orari_str}:**\n\n{imp['pomeriggio_leonardo']['cosa']}"
                    
                    if "NONNI" in imp['pomeriggio_leonardo']['chi']: st.error(t_ins)
                    else: st.success(t_ins)
                else:
                    # Nasconde l'orario se è Scuola per Leonardo
                    orari_l = "" if imp['pomeriggio_leonardo']['cosa'] == "Scuola 🏫" else f" ({imp['pomeriggio_leonardo']['inizio']}-{imp['pomeriggio_leonardo']['fine']})"
                    t_l = f"**👦 LEONARDO{orari_l}:** {imp['pomeriggio_leonardo']['cosa']}"
                    
                    # Nasconde l'orario se è Scuola per Sara
                    orari_s = "" if imp['pomeriggio_sara']['cosa'] == "Scuola 🏫" else f" ({imp['pomeriggio_sara']['inizio']}-{imp['pomeriggio_sara']['fine']})"
                    t_s = f"**👧 SARA{orari_s}:** {imp['pomeriggio_sara']['cosa']}"
                    
                    if "NONNI" in imp['pomeriggio_leonardo']['chi']: st.error(t_l)
                    else: st.success(t_l)
                    
                    if "NONNI" in imp['pomeriggio_sara']['chi']: st.error(t_s)
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
        
        # Logica di visualizzazione orari Leonardo
        if cos_l != "Scuola 🏫":
            c5, c6 = st.columns(2)
            in_l = c5.text_input("Inizio", dati_g["pomeriggio_leonardo"]["inizio"], key="l_in")
            fi_l = c6.text_input("Fine", dati_g["pomeriggio_leonardo"]["fine"], key="l_fi")
        else:
            in_l = ""
            fi_l = ""

        # Checkbox SARA uguale a LEONARDO
        sara_uguale = st.checkbox("✅ Sara fa lo stesso di Leonardo", value=dati_g.get("sara_uguale", True))
        
        # Gestione SARA (se diversa da LEONARDO)
        if not sara_uguale:
            st.subheader("👧 Pomeriggio SARA")
            c7, c8 = st.columns(2)
            chi_s = c7.selectbox("Chi?", OPZIONI_CHI, index=OPZIONI_CHI.index(dati_g["pomeriggio_sara"]["chi"]), key="s1")
            
            idx_cosa_s = OPZIONI_ATTIVITA.index(dati_g["pomeriggio_sara"]["cosa"]) if dati_g["pomeriggio_sara"]["cosa"] in OPZIONI_ATTIVITA else OPZIONI_ATTIVITA.index("Scuola 🏫")
            cos_s = c8.selectbox("Attività?", OPZIONI_ATTIVITA, index=idx_cosa_s, key="s2")
            
            # Logica di visualizzazione orari Sara
            if cos_s != "Scuola 🏫":
                c9, c10 = st.columns(2)
                in_s = c9.text_input("Inizio Sara", dati_g["pomeriggio_sara"]["inizio"], key="s_in")
                fi_s = c10.text_input("Fine Sara", dati_g["pomeriggio_sara"]["fine"], key="s_fi")
            else:
                in_s = ""
                fi_s = ""
        else:
            # Se uguale, i dati verranno sovrascritti al salvataggio
            chi_s, cos_s, in_s, fi_s = chi_l, cos_l, in_l, fi_l

        if st.button("💾 SALVA PROGRAMMA"):
            # Aggiornamento dizionario programma
            programma[sett_scelta][giorno_sel] = {
                "mattina": {"chi": chi_m, "cosa": "Scuola 🏫"},
                "pomeriggio_leonardo": {"chi": chi_l, "cosa": cos_l, "inizio": in_l, "fine": fi_l},
                "sara_uguale": sara_uguale,
                "pomeriggio_sara": {"chi": chi_s, "cosa": cos_s, "inizio": in_s, "fine": fi_s}
            }
            salva_programma(programma)
            st.success("Programma salvato con successo!")
            st.rerun()
