import streamlit as st
import json
import os

# 1. IMPOSTAZIONI INIZIALI
st.set_page_config(page_title="Taxi Nipoti", page_icon="🚕", layout="centered")

FILE_MEMORIA = "programma.json"

# Le nostre opzioni (puoi aggiungerne altre qui se serve in futuro!)
OPZIONI_CHI = ["🔴 TOCCA AI NONNI", "🟢 FACCIAMO NOI GENITORI"]
OPZIONI_ATTIVITA = [
    "Scuola 🏫", 
    "Ginnastica Artistica 🤸‍♀️", 
    "Eufonio 🎺", 
    "Yoga 🧘‍♂️", 
    "Casa 🏠"
]

# 2. FUNZIONI PER LA MEMORIA DELL'APP (Leggere e Salvare)
def carica_programma():
    # Se il file esiste, lo legge
    if os.path.exists(FILE_MEMORIA):
        with open(FILE_MEMORIA, "r", encoding="utf-8") as file:
            return json.load(file)
    else:
        # Se non esiste (la prima volta), crea una settimana base
        settimana_base = {}
        giorni = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì"]
        for giorno in giorni:
            settimana_base[giorno] = {
                "mattina": {"chi": "🔴 TOCCA AI NONNI", "cosa": "Scuola 🏫"},
                "pomeriggio": {"chi": "🟢 FACCIAMO NOI GENITORI", "cosa": "Casa 🏠"}
            }
        return settimana_base

def salva_programma(dati):
    # Scrive le modifiche nel file
    with open(FILE_MEMORIA, "w", encoding="utf-8") as file:
        json.dump(dati, file, indent=4)

# Carichiamo i dati all'avvio
programma = carica_programma()


# ==========================================
# 3. LA BARRA LATERALE (SOLO PER VOI GENITORI)
# ==========================================
with st.sidebar:
    st.title("⚙️ Pannello Genitori")
    st.write("Modificate qui la giornata. I nonni vedranno l'aggiornamento in automatico!")
    st.markdown("---")
    
    # Scegliete quale giorno modificare
    giorno_scelto = st.selectbox("📅 Scegli il giorno da modificare:", list(programma.keys()))
    
    st.subheader("☀️ Mattina")
    chi_mat = st.selectbox("Chi fa il taxi la mattina?", OPZIONI_CHI, index=OPZIONI_CHI.index(programma[giorno_scelto]["mattina"]["chi"]))
    cosa_mat = st.selectbox("Dove vanno la mattina?", OPZIONI_ATTIVITA, index=OPZIONI_ATTIVITA.index(programma[giorno_scelto]["mattina"]["cosa"]))
    
    st.subheader("🌙 Pomeriggio")
    chi_pom = st.selectbox("Chi fa il taxi il pomeriggio?", OPZIONI_CHI, index=OPZIONI_CHI.index(programma[giorno_scelto]["pomeriggio"]["chi"]))
    cosa_pom = st.selectbox("Dove vanno il pomeriggio?", OPZIONI_ATTIVITA, index=OPZIONI_ATTIVITA.index(programma[giorno_scelto]["pomeriggio"]["cosa"]))
    
    st.markdown("---")
    # Il pulsante per salvare
    if st.button("💾 SALVA MODIFICHE", use_container_width=True):
        programma[giorno_scelto]["mattina"]["chi"] = chi_mat
        programma[giorno_scelto]["mattina"]["cosa"] = cosa_mat
        programma[giorno_scelto]["pomeriggio"]["chi"] = chi_pom
        programma[giorno_scelto]["pomeriggio"]["cosa"] = cosa_pom
        
        salva_programma(programma)
        st.success(f"✅ {giorno_scelto} aggiornato!")


# ==========================================
# 4. LA SCHERMATA PRINCIPALE (PER I NONNI)
# ==========================================
st.title("🚕 Il Taxi dei Nipoti")
st.write("Programma della settimana. Fate attenzione ai colori!")
st.markdown("---")

# Disegniamo i bottononi colorati leggendo dalla memoria
for giorno, impegni in programma.items():
    st.header(f"📅 {giorno}")
    
    # --- MATTINA ---
    testo_mattina = f"**☀️ MATTINA:** {impegni['mattina']['cosa']}"
    if "NONNI" in impegni['mattina']['chi']:
        st.error("🔴 TOCCA AI NONNI \n\n" + testo_mattina)
    else:
        st.success("🟢 FACCIAMO NOI \n\n" + testo_mattina)
        
    # --- POMERIGGIO ---
    testo_pomeriggio = f"**🌙 POMERIGGIO:** {impegni['pomeriggio']['cosa']}"
    if "NONNI" in impegni['pomeriggio']['chi']:
        st.error("🔴 TOCCA AI NONNI \n\n" + testo_pomeriggio)
    else:
        st.success("🟢 FACCIAMO NOI \n\n" + testo_pomeriggio)
        
    st.markdown("---")
