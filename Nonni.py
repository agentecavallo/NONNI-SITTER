import streamlit as st

# 1. IMPOSTAZIONI DELLA PAGINA (Per renderla perfetta sul cellulare)
st.set_page_config(page_title="Taxi Nipoti", page_icon="🚕", layout="centered")

# Titolo e istruzioni per i nonni
st.title("🚕 Il Taxi dei Nipoti")
st.write("Ecco il programma di questa settimana! Fate attenzione ai colori:")
st.success("🟢 VERDE: Facciamo noi genitori (Potete riposare!)")
st.error("🔴 ROSSO: Nonni, tocca a voi! Grazie ❤️")
st.markdown("---")

# 2. DATI DELLA SETTIMANA (MODIFICATE QUI OGNI DOMENICA)
# Istruzioni: 
# Alla voce "chi" scrivete "nonni" per far apparire il riquadro ROSSO, 
# oppure scrivete "genitori" per far apparire il riquadro VERDE.

giorni = {
    "Lunedì": [
        {"orario": "08:00 - Mattina", "azione": "Prendere a CASA e portare a SCUOLA 🏫", "chi": "nonni"},
        {"orario": "16:30 - Pomeriggio", "azione": "Prendere a SCUOLA e portare a GINNASTICA 🤸‍♀️", "chi": "genitori"}
    ],
    "Martedì": [
        {"orario": "08:00 - Mattina", "azione": "Andiamo noi a scuola", "chi": "genitori"},
        {"orario": "16:00 - Pomeriggio", "azione": "Prendere a SCUOLA e portare a MUSICA 🎵", "chi": "nonni"}
    ],
    "Mercoledì": [
        {"orario": "08:00 - Mattina", "azione": "Prendere a CASA e portare a SCUOLA 🏫", "chi": "nonni"},
        {"orario": "17:00 - Pomeriggio", "azione": "Prendere a SCUOLA e portare a YOGA 🧘‍♂️", "chi": "nonni"}
    ],
    "Giovedì": [
        {"orario": "08:00 - Mattina", "azione": "Andiamo noi a scuola", "chi": "genitori"},
        {"orario": "16:30 - Pomeriggio", "azione": "Riposo a casa 🏠", "chi": "genitori"}
    ],
    "Venerdì": [
         {"orario": "08:00 - Mattina", "azione": "Prendere a CASA e portare a SCUOLA 🏫", "chi": "nonni"},
         {"orario": "13:30 - Pomeriggio", "azione": "Uscita anticipata! Prendere a SCUOLA e portare a CASA dai nonni 🍝", "chi": "nonni"}
    ]
}

# 3. CREAZIONE DELL'INTERFACCIA VISIVA (Non serve toccare questo codice)
for giorno, impegni in giorni.items():
    # Crea un titolo grande per il giorno
    st.header(f"📅 {giorno}")
    
    # Crea i riquadri per mattina e pomeriggio
    for impegno in impegni:
        testo_da_mostrare = f"**{impegno['orario']}** \n\n {impegno['azione']}"
        
        if impegno["chi"] == "nonni":
            # Crea un blocco ROSSO/ARANCIO gigante
            st.error("🔴 TOCCA AI NONNI \n\n" + testo_da_mostrare)
        else:
            # Crea un blocco VERDE gigante
            st.success("🟢 FACCIAMO NOI \n\n" + testo_da_mostrare)
            
    # Riga di separazione visiva
    st.markdown("---")
