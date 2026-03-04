import streamlit as st
import json
import os

# 1. IMPOSTAZIONI INIZIALI
st.set_page_config(page_title="Taxi Nipoti", page_icon="🚕", layout="centered")

FILE_MEMORIA = "programma.json"

OPZIONI_CHI = ["🔴 TOCCA AI NONNI", "🟢 FACCIAMO NOI GENITORI"]
OPZIONI_ATTIVITA = [
    "Scuola 🏫", 
    "Ginnastica Artistica 🤸‍♀️", 
    "Eufonio 🎺", 
    "Yoga 🧘‍♂️", 
    "Musica 🎵",
    "Casa 🏠"
]

# 2. FUNZIONI PER LA MEMORIA DELL'APP
def crea_settimana_base():
    settimana = {}
    giorni = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì"]
    for giorno in giorni:
        settimana[giorno] = {
            "mattina": {"chi": "🔴 TOCCA AI NONNI", "cosa": "Scuola 🏫"},
            "pomeriggio_leo": {"chi": "🟢 FACCIAMO NOI GENITORI", "cosa": "Casa 🏠", "inizio": "16:30", "fine": "18:00"},
            "pomeriggio_sara": {"chi": "🟢 FACCIAMO NOI GENITORI", "cosa": "Casa 🏠", "inizio": "16:30", "fine": "18:00"}
        }
    return settimana

def carica_programma():
    if os.path.exists(FILE_MEMORIA):
        with open(FILE_MEMORIA, "r", encoding="utf-8") as file:
            try:
                dati = json.load(file)
                # Controllo di sicurezza: se è il vecchio formato senza "pomeriggio_leo", ricrea la memoria
                if "pomeriggio_leo" not in dati["Lunedì"]:
                    return crea_settimana_base()
                return dati
            except:
                return crea_settimana_base()
    else:
        return crea_settimana_base()

def salva_programma(dati):
    with open(FILE_MEMORIA, "w", encoding="utf-8") as file:
        json.dump(dati, file, indent=4)

programma = carica_programma()

# ==========================================
# 3. LA BARRA LATERALE (PANNELLO GENITORI)
# ==========================================
with st.sidebar:
    st.title("⚙️ Pannello Genitori")
    st.write("Organizza la giornata per Leo e Sara.")
    st.markdown("---")
    
    giorno_scelto = st.selectbox("📅 Seleziona il giorno:", list(programma.keys()))
    
    st.subheader("☀️ Mattina (Insieme)")
    chi_mat = st.selectbox("Taxi mattina?", OPZIONI_CHI, index=OPZIONI_CHI.index(programma[giorno_scelto]["mattina"]["chi"]), key="chi_mat")
    cosa_mat = st.selectbox("Dove?", OPZIONI_ATTIVITA, index=OPZIONI_ATTIVITA.index(programma[giorno_scelto]["mattina"]["cosa"]), key="cosa_mat")
    
    st.markdown("---")
    
    st.subheader("👦 Pomeriggio - LEO")
    chi_leo = st.selectbox("Taxi Leo?", OPZIONI_CHI, index=OPZIONI_CHI.index(programma[giorno_scelto]["pomeriggio_leo"]["chi"]), key="chi_leo")
    cosa_leo = st.selectbox("Attività Leo?", OPZIONI_ATTIVITA, index=OPZIONI_ATTIVITA.index(programma[giorno_scelto]["pomeriggio_leo"]["cosa"]), key="cosa_leo")
    col1, col2 = st.columns(2)
    inizio_leo = col1.text_input("Ora Inizio (Leo)", value=programma[giorno_scelto]["pomeriggio_leo"]["inizio"], key="in_leo")
    fine_leo = col2.text_input("Ora Fine (Leo)", value=programma[giorno_scelto]["pomeriggio_leo"]["fine"], key="fi_leo")

    st.markdown("---")

    st.subheader("👧 Pomeriggio - SARA")
    chi_sara = st.selectbox("Taxi Sara?", OPZIONI_CHI, index=OPZIONI_CHI.index(programma[giorno_scelto]["pomeriggio_sara"]["chi"]), key="chi_sara")
    cosa_sara = st.selectbox("Attività Sara?", OPZIONI_ATTIVITA, index=OPZIONI_ATTIVITA.index(programma[giorno_scelto]["pomeriggio_sara"]["cosa"]), key="cosa_sara")
    col3, col4 = st.columns(2)
    inizio_sara = col3.text_input("Ora Inizio (Sara)", value=programma[giorno_scelto]["pomeriggio_sara"]["inizio"], key="in_sara")
    fine_sara = col4.text_input("Ora Fine (Sara)", value=programma[giorno_scelto]["pomeriggio_sara"]["fine"], key="fi_sara")
    
    st.markdown("---")
    if st.button("💾 SALVA MODIFICHE", use_container_width=True):
        programma[giorno_scelto]["mattina"]["chi"] = chi_mat
        programma[giorno_scelto]["mattina"]["cosa"] = cosa_mat
        
        programma[giorno_scelto]["pomeriggio_leo"]["chi"] = chi_leo
        programma[giorno_scelto]["pomeriggio_leo"]["cosa"] = cosa_leo
        programma[giorno_scelto]["pomeriggio_leo"]["inizio"] = inizio_leo
        programma[giorno_scelto]["pomeriggio_leo"]["fine"] = fine_leo
        
        programma[giorno_scelto]["pomeriggio_sara"]["chi"] = chi_sara
        programma[giorno_scelto]["pomeriggio_sara"]["cosa"] = cosa_sara
        programma[giorno_scelto]["pomeriggio_sara"]["inizio"] = inizio_sara
        programma[giorno_scelto]["pomeriggio_sara"]["fine"] = fine_sara
        
        salva_programma(programma)
        st.success(f"✅ {giorno_scelto} aggiornato con successo!")

# ==========================================
# 4. LA SCHERMATA PRINCIPALE (PER I NONNI)
# ==========================================
st.title("🚕 Il Taxi dei Nipoti")
st.write("Programma aggiornato. Ricordate: Rosso = Nonni, Verde = Genitori!")
st.markdown("---")

for giorno, impegni in programma.items():
    st.header(f"📅 {giorno}")
    
    # --- MATTINA ---
    testo_mattina = f"**☀️ MATTINA:** {impegni['mattina']['cosa']}"
    # Aggiunta automatica della frase per la scuola
    if impegni['mattina']['cosa'] == "Scuola 🏫":
         testo_mattina += "\n\n👉 *Vi aspettiamo alle 7:00 a casa!*"

    if "NONNI" in impegni['mattina']['chi']:
        st.error(f"🔴 TOCCA AI NONNI \n\n {testo_mattina}")
    else:
        st.success(f"🟢 FACCIAMO NOI \n\n {testo_mattina}")
        
    # --- POMERIGGIO LEO ---
    testo_leo = f"**👦 LEO ({impegni['pomeriggio_leo']['inizio']} - {impegni['pomeriggio_leo']['fine']}):** {impegni['pomeriggio_leo']['cosa']}"
    if "NONNI" in impegni['pomeriggio_leo']['chi']:
        st.error(f"🔴 NONNI PER LEO \n\n {testo_leo}")
    else:
        st.success(f"🟢 GENITORI PER LEO \n\n {testo_leo}")

    # --- POMERIGGIO SARA ---
    testo_sara = f"**👧 SARA ({impegni['pomeriggio_sara']['inizio']} - {impegni['pomeriggio_sara']['fine']}):** {impegni['pomeriggio_sara']['cosa']}"
    if "NONNI" in impegni['pomeriggio_sara']['chi']:
        st.error(f"🔴 NONNI PER SARA \n\n {testo_sara}")
    else:
        st.success(f"🟢 GENITORI PER SARA \n\n {testo_sara}")
        
    st.markdown("---")
