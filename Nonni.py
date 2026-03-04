import streamlit as st
import json
import os

# 1. IMPOSTAZIONI INIZIALI
st.set_page_config(page_title="Taxi Nipoti", page_icon="🚕", layout="centered")

FILE_MEMORIA = "programma.json"

OPZIONI_CHI = ["🔴 TOCCA AI NONNI", "🟢 FACCIAMO NOI GENITORI"]
OPZIONI_ATTIVITA = ["Scuola 🏫", "Ginnastica Artistica 🤸‍♀️", "Eufonio 🎺", "Yoga 🧘‍♂️", "Musica 🎵", "Casa 🏠"]

# 2. FUNZIONI PER LA MEMORIA DELL'APP
def crea_settimana_base():
    settimana = {}
    giorni = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì"]
    for giorno in giorni:
        settimana[giorno] = {
            "mattina": {"chi": "🔴 TOCCA AI NONNI", "cosa": "Scuola 🏫"},
            "sara_uguale": True, # Di base impostiamo che stanno insieme
            "pomeriggio_leo": {"chi": "🟢 FACCIAMO NOI GENITORI", "cosa": "Casa 🏠", "inizio": "16:30", "fine": "18:00"},
            "pomeriggio_sara": {"chi": "🟢 FACCIAMO NOI GENITORI", "cosa": "Casa 🏠", "inizio": "16:30", "fine": "18:00"}
        }
    return settimana

def carica_programma():
    if os.path.exists(FILE_MEMORIA):
        try:
            with open(FILE_MEMORIA, "r", encoding="utf-8") as file:
                dati = json.load(file)
                # Sicurezza: se il file vecchio non ha la regola della "spunta", l'aggiungiamo al volo
                for giorno in dati:
                    if "sara_uguale" not in dati[giorno]:
                        dati[giorno]["sara_uguale"] = False
                return dati
        except:
            return crea_settimana_base()
    return crea_settimana_base()

def salva_programma(dati):
    with open(FILE_MEMORIA, "w", encoding="utf-8") as file:
        json.dump(dati, file, indent=4)

programma = carica_programma()

# ==========================================
# 3. CREAZIONE DELLE DUE SCHEDE (TABS)
# ==========================================
# Creiamo i due "bottoni" in alto per navigare
scheda_nonni, scheda_genitori = st.tabs(["🚕 Vista Nonni", "⚙️ Modifica Genitori"])

# --- SCHEDA 1: QUELLO CHE VEDONO I NONNI ---
with scheda_nonni:
    st.title("🚕 Il Taxi dei Nipoti")
    st.write("Programma aggiornato. Ricordate: Rosso = Nonni, Verde = Genitori!")
    st.markdown("---")

    for giorno, impegni in programma.items():
        st.header(f"📅 {giorno}")
        
        # MATTINA
        testo_mattina = f"**☀️ MATTINA:** {impegni['mattina']['cosa']}"
        if impegni['mattina']['cosa'] == "Scuola 🏫":
             testo_mattina += "\n\n👉 *Vi aspettiamo alle 7:00 a casa!*"

        if "NONNI" in impegni['mattina']['chi']:
            st.error(f"🔴 TOCCA AI NONNI \n\n {testo_mattina}")
        else:
            st.success(f"🟢 FACCIAMO NOI \n\n {testo_mattina}")
            
        # POMERIGGIO: Controllo se sono insieme o separati
        if impegni.get("sara_uguale", True):
            # 👦👧 SONO INSIEME: Mostriamo un unico blocco!
            testo_insieme = f"**👦👧 LEO E SARA ({impegni['pomeriggio_leo']['inizio']} - {impegni['pomeriggio_leo']['fine']}):** {impegni['pomeriggio_leo']['cosa']}"
            if "NONNI" in impegni['pomeriggio_leo']['chi']:
                st.error(f"🔴 NONNI PER ENTRAMBI \n\n {testo_insieme}")
            else:
                st.success(f"🟢 GENITORI PER ENTRAMBI \n\n {testo_insieme}")
        
        else:
            # 👦👧 SONO SEPARATI: Mostriamo due blocchi distinti
            # 1. LEO
            testo_leo = f"**👦 LEO ({impegni['pomeriggio_leo']['inizio']} - {impegni['pomeriggio_leo']['fine']}):** {impegni['pomeriggio_leo']['cosa']}"
            if "NONNI" in impegni['pomeriggio_leo']['chi']:
                st.error(f"🔴 NONNI PER LEO \n\n {testo_leo}")
            else:
                st.success(f"🟢 GENITORI PER LEO \n\n {testo_leo}")

            # 2. SARA
            testo_sara = f"**👧 SARA ({impegni['pomeriggio_sara']['inizio']} - {impegni['pomeriggio_sara']['fine']}):** {impegni['pomeriggio_sara']['cosa']}"
            if "NONNI" in impegni['pomeriggio_sara']['chi']:
                st.error(f"🔴 NONNI PER SARA \n\n {testo_sara}")
            else:
                st.success(f"🟢 GENITORI PER SARA \n\n {testo_sara}")
            
        st.markdown("---")


# --- SCHEDA 2: QUELLO CHE USATE VOI GENITORI ---
with scheda_genitori:
    st.title("⚙️ Pannello Genitori")
    st.write("Scegli il giorno e organizza la giornata. I nonni vedranno l'aggiornamento nell'altra scheda.")
    
    giorno_scelto = st.selectbox("📅 Seleziona il giorno da modificare:", list(programma.keys()))
    
    # MATTINA (Affiancati su due colonne per risparmiare spazio)
    st.subheader("☀️ Mattina (Insieme)")
    col1, col2 = st.columns(2)
    chi_mat = col1.selectbox("Taxi mattina?", OPZIONI_CHI, index=OPZIONI_CHI.index(programma[giorno_scelto]["mattina"]["chi"]))
    cosa_mat = col2.selectbox("Dove?", OPZIONI_ATTIVITA, index=OPZIONI_ATTIVITA.index(programma[giorno_scelto]["mattina"]["cosa"]))
    
    st.markdown("---")
    
    # POMERIGGIO LEO
    st.subheader("👦 Pomeriggio - LEO (o Entrambi)")
    col3, col4 = st.columns(2)
    chi_leo = col3.selectbox("Taxi Leo?", OPZIONI_CHI, index=OPZIONI_CHI.index(programma[giorno_scelto]["pomeriggio_leo"]["chi"]))
    cosa_leo = col4.selectbox("Attività Leo?", OPZIONI_ATTIVITA, index=OPZIONI_ATTIVITA.index(programma[giorno_scelto]["pomeriggio_leo"]["cosa"]))
    col5, col6 = st.columns(2)
    inizio_leo = col5.text_input("Ora Inizio (Leo)", value=programma[giorno_scelto]["pomeriggio_leo"]["inizio"])
    fine_leo = col6.text_input("Ora Fine (Leo)", value=programma[giorno_scelto]["pomeriggio_leo"]["fine"])

    st.markdown("---")

    # LA SPUNTA MAGICA PER SARA
    sara_uguale_val = programma[giorno_scelto].get("sara_uguale", True)
    sara_uguale = st.checkbox("✅ Nel pomeriggio Sara fa la STESSA COSA di Leo con gli stessi orari", value=sara_uguale_val)
    
    # Se NON c'è la spunta, mostriamo i campi per Sara
    if not sara_uguale:
        st.subheader("👧 Pomeriggio - SARA")
        col7, col8 = st.columns(2)
        chi_sara = col7.selectbox("Taxi Sara?", OPZIONI_CHI, index=OPZIONI_CHI.index(programma[giorno_scelto]["pomeriggio_sara"]["chi"]))
        cosa_sara = col8.selectbox("Attività Sara?", OPZIONI_ATTIVITA, index=OPZIONI_ATTIVITA.index(programma[giorno_scelto]["pomeriggio_sara"]["cosa"]))
        col9, col10 = st.columns(2)
        inizio_sara = col9.text_input("Ora Inizio (Sara)", value=programma[giorno_scelto]["pomeriggio_sara"]["inizio"])
        fine_sara = col10.text_input("Ora Fine (Sara)", value=programma[giorno_scelto]["pomeriggio_sara"]["fine"])

    st.markdown("---")
    
    # IL PULSANTE PER SALVARE
    if st.button(f"💾 SALVA IL PROGRAMMA DI {giorno_scelto.upper()}", use_container_width=True):
        # Salviamo la mattina
        programma[giorno_scelto]["mattina"]["chi"] = chi_mat
        programma[giorno_scelto]["mattina"]["cosa"] = cosa_mat
        
        # Salviamo Leo
        programma[giorno_scelto]["pomeriggio_leo"]["chi"] = chi_leo
        programma[giorno_scelto]["pomeriggio_leo"]["cosa"] = cosa_leo
        programma[giorno_scelto]["pomeriggio_leo"]["inizio"] = inizio_leo
        programma[giorno_scelto]["pomeriggio_leo"]["fine"] = fine_leo
        
        # Salviamo lo stato della spunta
        programma[giorno_scelto]["sara_uguale"] = sara_uguale

        # Gestione di Sara
        if sara_uguale:
            # Se è uguale, copiamo i dati di Leo su Sara in automatico
            programma[giorno_scelto]["pomeriggio_sara"]["chi"] = chi_leo
            programma[giorno_scelto]["pomeriggio_sara"]["cosa"] = cosa_leo
            programma[giorno_scelto]["pomeriggio_sara"]["inizio"] = inizio_leo
            programma[giorno_scelto]["pomeriggio_sara"]["fine"] = fine_leo
        else:
            # Altrimenti, salviamo i dati inseriti manualmente per Sara
            programma[giorno_scelto]["pomeriggio_sara"]["chi"] = chi_sara
            programma[giorno_scelto]["pomeriggio_sara"]["cosa"] = cosa_sara
            programma[giorno_scelto]["pomeriggio_sara"]["inizio"] = inizio_sara
            programma[giorno_scelto]["pomeriggio_sara"]["fine"] = fine_sara
        
        salva_programma(programma)
        st.success(f"✅ {giorno_scelto} aggiornato! Vai nella scheda 'Vista Nonni' in alto per vedere il risultato.")
