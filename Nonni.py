import streamlit as st
import json
import os

# 1. IMPOSTAZIONI INIZIALI
st.set_page_config(page_title="Taxi Nipoti", page_icon="指標", layout="centered")

FILE_MEMORIA = "programma.json"

OPZIONI_CHI = ["🔴 TOCCA AI NONNI", "🟢 FACCIAMO NOI GENITORI"]
OPZIONI_ATTIVITA = ["Scuola 🏫", "Ginnastica Artistica 🤸‍♀️", "Eufonio 🎺", "Yoga 🧘‍♂️", "Musica 🎵", "Casa 🏠"]

# 2. FUNZIONI PER LA MEMORIA (CON AUTO-REPAIR PER EVITARE KEYERROR)
def crea_settimana_base():
    settimana = {}
    giorni = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì"]
    for giorno in giorni:
        settimana[giorno] = {
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
                # --- CONTROLLO ANTI-ERRORE ---
                # Se manca la chiave 'pomeriggio_leo' in un giorno qualsiasi, il file è vecchio.
                # Lo resettiamo per evitare il crash dello screenshot.
                test_giorno = next(iter(dati)) 
                if "pomeriggio_leo" not in dati[test_giorno]:
                    return crea_settimana_base()
                return dati
        except Exception:
            return crea_settimana_base()
    return crea_settimana_base()

def salva_programma(dati):
    with open(FILE_MEMORIA, "w", encoding="utf-8") as file:
        json.dump(dati, file, indent=4)

# Caricamento dati
programma = carica_programma()

# ==========================================
# 3. INTERFACCIA A SCHEDE (TABS)
# ==========================================
scheda_nonni, scheda_genitori = st.tabs(["🚕 Vista Nonni", "⚙️ Modifica Genitori"])

# --- SCHEDA 1: VISTA NONNI ---
with scheda_nonni:
    st.title("🚕 Il Taxi dei Nipoti")
    st.write("Programma settimanale per i nonni.")
    st.markdown("---")

    for giorno, impegni in programma.items():
        st.header(f"📅 {giorno}")
        
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
            # BLOCCO UNICO
            testo_ins = f"**👦👧 LEO E SARA ({impegni['pomeriggio_leo']['inizio']} - {impegni['pomeriggio_leo']['fine']}):**\n\n{impegni['pomeriggio_leo']['cosa']}"
            if "NONNI" in impegni['pomeriggio_leo']['chi']:
                st.error(testo_ins)
            else:
                st.success(testo_ins)
        else:
            # BLOCCHI SEPARATI
            t_leo = f"**👦 LEO ({impegni['pomeriggio_leo']['inizio']} - {impegni['pomeriggio_leo']['fine']}):**\n\n{impegni['pomeriggio_leo']['cosa']}"
            t_sara = f"**👧 SARA ({impegni['pomeriggio_sara']['inizio']} - {impegni['pomeriggio_sara']['fine']}):**\n\n{impegni['pomeriggio_sara']['cosa']}"
            
            # Leo
            if "NONNI" in impegni['pomeriggio_leo']['chi']: st.error(t_leo)
            else: st.success(t_leo)
            # Sara
            if "NONNI" in impegni['pomeriggio_sara']['chi']: st.error(t_sara)
            else: st.success(t_sara)
            
        st.markdown("---")

# --- SCHEDA 2: MODIFICA GENITORI ---
with scheda_genitori:
    st.title("⚙️ Impostazioni")
    giorno_sel = st.selectbox("Seleziona Giorno:", list(programma.keys()))
    
    st.subheader("☀️ Mattina")
    c1, c2 = st.columns(2)
    chi_m = c1.selectbox("Chi?", OPZIONI_CHI, index=OPZIONI_CHI.index(programma[giorno_sel]["mattina"]["chi"]), key="m1")
    cos_m = c2.selectbox("Cosa?", OPZIONI_ATTIVITA, index=OPZIONI_ATTIVITA.index(programma[giorno_sel]["mattina"]["cosa"]), key="m2")
    
    st.markdown("---")
    st.subheader("👦 Pomeriggio LEO")
    c3, c4 = st.columns(2)
    chi_l = c3.selectbox("Chi Leo?", OPZIONI_CHI, index=OPZIONI_CHI.index(programma[giorno_sel]["pomeriggio_leo"]["chi"]), key="l1")
    cos_l = c4.selectbox("Cosa Leo?", OPZIONI_ATTIVITA, index=OPZIONI_ATTIVITA.index(programma[giorno_sel]["pomeriggio_leo"]["cosa"]), key="l2")
    c5, c6 = st.columns(2)
    in_l = c5.text_input("Inizio", programma[giorno_sel]["pomeriggio_leo"]["inizio"], key="l3")
    fi_l = c6.text_input("Fine", programma[giorno_sel]["pomeriggio_leo"]["fine"], key="l4")

    # SPUNTA SARA
    sara_uguale = st.checkbox("✅ Sara fa lo stesso di Leo", value=programma[giorno_sel].get("sara_uguale", True))
    
    if not sara_uguale:
        st.subheader("👧 Pomeriggio SARA")
        c7, c8 = st.columns(2)
        chi_s = c7.selectbox("Chi Sara?", OPZIONI_CHI, index=OPZIONI_CHI.index(programma[giorno_sel]["pomeriggio_sara"]["chi"]), key="s1")
        cos_s = c8.selectbox("Cosa Sara?", OPZIONI_ATTIVITA, index=OPZIONI_ATTIVITA.index(programma[giorno_sel]["pomeriggio_sara"]["cosa"]), key="s2")
        c9, c10 = st.columns(2)
        in_s = c9.text_input("Inizio Sara", programma[giorno_sel]["pomeriggio_sara"]["inizio"], key="s3")
        fi_s = c10.text_input("Fine Sara", programma[giorno_sel]["pomeriggio_sara"]["fine"], key="s4")

    if st.button("💾 SALVA MODIFICHE"):
        programma[giorno_sel]["mattina"] = {"chi": chi_m, "cosa": cos_m}
        programma[giorno_sel]["pomeriggio_leo"] = {"chi": chi_l, "cosa": cos_l, "inizio": in_l, "fine": fi_l}
        programma[giorno_sel]["sara_uguale"] = sara_uguale
        
        if sara_uguale:
            programma[giorno_sel]["pomeriggio_sara"] = programma[giorno_sel]["pomeriggio_leo"].copy()
        else:
            programma[giorno_sel]["pomeriggio_sara"] = {"chi": chi_s, "cosa": cos_s, "inizio": in_s, "fine": fi_s}
            
        salva_programma(programma)
        st.success("Salvato! Controlla la scheda 'Vista Nonni'.")
        st.rerun()
