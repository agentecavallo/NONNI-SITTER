import streamlit as st
import json
import os
from datetime import datetime, timedelta

# 1. IMPOSTAZIONI PAGINA
st.set_page_config(page_title="Taxi Nipoti", page_icon="🚕", layout="centered")

# Nome file nuovo per resettare eventuali errori precedenti
FILE_MEMORIA = "programma_famiglia.json"
OPZIONI_CHI = ["🟢 FACCIAMO NOI GENITORI", "🔴 TOCCA AI NONNI"]
OPZIONI_ATTIVITA = ["Ginnastica Artistica 🤸‍♀️", "Eufonio 🎺", "Yoga 🧘‍♂️", "Musica 🎵", "Casa 🏠"]

# --- FUNZIONI CORE ---
def ottieni_calendario():
    oggi = datetime.now().date()
    lunedi_curr = oggi - timedelta(days=oggi.weekday())
    lunedi_next = lunedi_curr + timedelta(days=7)
    mesi = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]
    
    def formatta(base):
        nomi = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì"]
        return {nomi[i]: {
            "data_testo": f"{nomi[i]} {(base + timedelta(days=i)).day} {mesi[(base + timedelta(days=i)).month-1]} {(base + timedelta(days=i)).year}",
            "data_obj": base + timedelta(days=i)
        } for i in range(5)}
    
    return {"corrente": formatta(lunedi_curr), "prossima": formatta(lunedi_next), "oggi_obj": oggi}

def crea_struttura_iniziale():
    def sett_vuota():
        return {g: {
            "mattina": {"chi": "🟢 FACCIAMO NOI GENITORI", "cosa": "Scuola 🏫"},
            "sara_uguale": True,
            "pomeriggio_leo": {"chi": "🟢 FACCIAMO NOI GENITORI", "cosa": "Casa 🏠", "inizio": "16:30", "fine": "18:00"},
            "pomeriggio_sara": {"chi": "🟢 FACCIAMO NOI GENITORI", "cosa": "Casa 🏠", "inizio": "16:30", "fine": "18:00"}
        } for g in ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì"]}
    return {"corrente": sett_vuota(), "prossima": sett_vuota()}

def carica_dati():
    if os.path.exists(FILE_MEMORIA):
        try:
            with open(FILE_MEMORIA, "r", encoding="utf-8") as f: return json.load(f)
        except: return crea_struttura_iniziale()
    return crea_struttura_iniziale()

def salva_dati():
    with open(FILE_MEMORIA, "w", encoding="utf-8") as f:
        json.dump(st.session_state.programma, f, indent=4)

def reset_giorno():
    """Forza il giorno selezionato a tornare tutto Verde di default"""
    s = st.session_state.s_settimana
    g = st.session_state.s_giorno
    st.session_state.programma[s][g] = {
        "mattina": {"chi": "🟢 FACCIAMO NOI GENITORI", "cosa": "Scuola 🏫"},
        "sara_uguale": True,
        "pomeriggio_leo": {"chi": "🟢 FACCIAMO NOI GENITORI", "cosa": "Casa 🏠", "inizio": "16:30", "fine": "18:00"},
        "pomeriggio_sara": {"chi": "🟢 FACCIAMO NOI GENITORI", "cosa": "Casa 🏠", "inizio": "16:30", "fine": "18:00"}
    }
    salva_dati()

# Inizializzazione
if "programma" not in st.session_state:
    st.session_state.programma = carica_dati()

cal = ottieni_calendario()

# ==========================================
# 3. INTERFACCIA A SCHEDE
# ==========================================
sch_nonni, sch_genitori = st.tabs(["🚕 Vista Nonni", "⚙️ Pannello Genitori"])

# --- VISTA NONNI ---
with sch_nonni:
    st.title("🚕 Il Taxi dei Nipoti")
    st.markdown("---")
    
    mostrati = 0
    fasi = [("corrente", cal["corrente"]), ("prossima", cal["prossima"])]
    
    for id_s, giorni in fasi:
        for nome_g, info in giorni.items():
            if info["data_obj"] >= cal["oggi_obj"]:
                mostrati += 1
                d = st.session_state.programma[id_s][nome_g]
                
                # Titolo Giorno
                if info["data_obj"] == cal["oggi_obj"]:
                    st.markdown(f"## 🌟 {info['data_testo'].upper()} (OGGI)")
                else:
                    st.markdown(f"### 📅 {info['data_testo']}")
                
                # Mattina
                t_m = f"**☀️ MATTINA:** Scuola 🏫\n\n👉 *Ore 7:00 a casa!*"
                st.success(t_m) if "GENITORI" in d['mattina']['chi'] else st.error(t_m)
                
                # Pomeriggio
                if d.get("sara_uguale", True):
                    t_i = f"**👦👧 LEO E SARA ({d['pomeriggio_leo']['inizio']}-{d['pomeriggio_leo']['fine']}):**\n\n{d['pomeriggio_leo']['cosa']}"
                    st.success(t_i) if "GENITORI" in d['pomeriggio_leo']['chi'] else st.error(t_i)
                else:
                    # Leo
                    t_l = f"**👦 LEO ({d['pomeriggio_leo']['inizio']}-{d['pomeriggio_leo']['fine']}):** {d['pomeriggio_leo']['cosa']}"
                    st.success(t_l) if "GENITORI" in d['pomeriggio_leo']['chi'] else st.error(t_l)
                    # Sara
                    t_s = f"**👧 SARA ({d['pomeriggio_sara']['inizio']}-{d['pomeriggio_sara']['fine']}):** {d['pomeriggio_sara']['cosa']}"
                    st.success(t_s) if "GENITORI" in d['pomeriggio_sara']['chi'] else st.error(t_s)
                st.markdown("---")
    
    if mostrati == 0: st.info("Nessun impegno imminente. Godetevi il weekend! ❤️")

# --- PANNELLO GENITORI ---
with sch_genitori:
    st.title("⚙️ Configurazione")
    
    st.radio("1. Scegli Settimana:", ["corrente", "prossima"], horizontal=True, 
             key="s_settimana", on_change=reset_giorno,
             format_func=lambda x: "Questa" if x=="corrente" else "La Prossima")
    
    opz = [n for n, i in cal[st.session_state.s_settimana].items() if i["data_obj"] >= cal["oggi_obj"]]
    st.selectbox("2. Scegli Giorno (si resetta a Verde):", opz, 
                 key="s_giorno", on_change=reset_giorno,
                 format_func=lambda x: cal[st.session_state.s_settimana][x]["data_testo"])

    # Dati del giorno selezionato (resettati via on_change)
    curr = st.session_state.programma[st.session_state.s_settimana][st.session_state.s_giorno]
    
    st.divider()
    st.subheader(f"Configurazione per {st.session_state.s_giorno}")
    
    # MATTINA
    curr["mattina"]["chi"] = st.selectbox("☀️ Chi accompagna a scuola?", OPZIONI_CHI, 
                                         index=OPZIONI_CHI.index(curr["mattina"]["chi"]), 
                                         key="w_m_chi", on_change=salva_dati)
    
    # POMERIGGIO LEO
    st.markdown("---")
    st.subheader("👦 Pomeriggio LEO")
    c1, c2 = st.columns(2)
    curr["pomeriggio_leo"]["chi"] = c1.selectbox("Chi Leo?", OPZIONI_CHI, index=OPZIONI_CHI.index(curr["pomeriggio_leo"]["chi"]), key="w_l_chi", on_change=salva_dati)
    curr["pomeriggio_leo"]["cosa"] = c2.selectbox("Cosa fa?", OPZIONI_ATTIVITA, index=OPZIONI_ATTIVITA.index(curr["pomeriggio_leo"]["cosa"]) if curr["pomeriggio_leo"]["cosa"] in OPZIONI_ATTIVITA else 0, key="w_l_cos", on_change=salva_dati)
    
    c3, c4 = st.columns(2)
    curr["pomeriggio_leo"]["inizio"] = c3.text_input("Dalle ore", curr["pomeriggio_leo"]["inizio"], key="w_l_in", on_change=salva_dati)
    curr["pomeriggio_leo"]["fine"] = c4.text_input("Alle ore", curr["pomeriggio_leo"]["fine"], key="w_l_fi", on_change=salva_dati)

    # SPUNTA SARA
    curr["sara_uguale"] = st.checkbox("✅ Sara fa le stesse cose di Leo", value=curr.get("sara_uguale", True), key="w_s_ug", on_change=salva_dati)
    
    if not curr["sara_uguale"]:
        st.markdown("---")
        st.subheader("👧 Pomeriggio SARA")
        c5, c6 = st.columns(2)
        curr["pomeriggio_sara"]["chi"] = c5.selectbox("Chi Sara?", OPZIONI_CHI, index=OPZIONI_CHI.index(curr["pomeriggio_sara"]["chi"]), key="w_s_chi", on_change=salva_dati)
        curr["pomeriggio_sara"]["cosa"] = c6.selectbox("Cosa fa?", OPZIONI_ATTIVITA, index=OPZIONI_ATTIVITA.index(curr["pomeriggio_sara"]["cosa"]) if curr["pomeriggio_sara"]["cosa"] in OPZIONI_ATTIVITA else 0, key="w_s_cos", on_change=salva_dati)
        
        c7, c8 = st.columns(2)
        curr["pomeriggio_sara"]["inizio"] = c7.text_input("Dalle ore (S)", curr["pomeriggio_sara"]["inizio"], key="w_s_in", on_change=salva_dati)
        curr["pomeriggio_sara"]["fine"] = c8.text_input("Alle ore (S)", curr["pomeriggio_sara"]["fine"], key="w_s_fi", on_change=salva_dati)
    else:
        # Sincronizzazione automatica
        curr["pomeriggio_sara"] = curr["pomeriggio_leo"].copy()

    st.caption("✨ Salvataggio automatico attivo. Il giorno selezionato è stato impostato di default su Verde.")
