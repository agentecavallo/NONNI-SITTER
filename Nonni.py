# --- SCHEDA 1: VISTA NONNI ---
with sch_nonni:
    st.title("🚕 Il Taxi dei Nipoti")
    # Messaggio di benvenuto con la data di oggi ben visibile
    st.info(f"📅 **Oggi è {date_settimana[datetime.now().strftime('%A').replace('Monday','Lunedì').replace('Tuesday','Martedì').replace('Wednesday','Mercoledì').replace('Thursday','Giovedì').replace('Friday','Venerdì')]}**")
    st.markdown("---")

    for giorno_chiave, impegni in programma.items():
        data_completa = date_settimana[giorno_chiave]
        
        # --- LOGICA DI EVIDENZIAZIONE GIORNO CORRENTE ---
        # Controlliamo se il nome del giorno nel ciclo corrisponde a oggi
        giorno_oggi_ita = datetime.now().strftime('%A').replace('Monday','Lunedì').replace('Tuesday','Martedì').replace('Wednesday','Mercoledì').replace('Thursday','Giovedì').replace('Friday','Venerdì')
        
        if giorno_chiave == giorno_oggi_ita:
            # Titolo più grande e con stella per oggi
            st.markdown(f"## 🌟 {data_completa.upper()} (OGGI)")
        else:
            # Titolo normale per gli altri giorni
            st.subheader(f"📅 {data_completa}")
        
        # --- Visualizzazione impegni (Mattina e Pomeriggio) ---
        # (Il resto del codice rimane uguale per mantenere la coerenza dei colori)
        testo_mat = f"**☀️ MATTINA:** {impegni['mattina']['cosa']}"
        if impegni['mattina']['cosa'] == "Scuola 🏫":
             testo_mat += "\n\n👉 *Vi aspettiamo alle 7:00 a casa!*"

        if "NONNI" in impegni['mattina']['chi']:
            st.error(testo_mat)
        else:
            st.success(testo_mat)
            
        # Pomeriggio (Leo e Sara)
        if impegni.get("sara_uguale", True):
            testo_ins = f"**👦👧 LEO E SARA ({impegni['pomeriggio_leo']['inizio']} - {impegni['pomeriggio_leo']['fine']}):**\n\n{impegni['pomeriggio_leo']['cosa']}"
            if "NONNI" in impegni['pomeriggio_leo']['chi']: st.error(testo_ins)
            else: st.success(testo_ins)
        else:
            # Visualizzazione separata se la spunta è tolta
            t_leo = f"**👦 LEO ({impegni['pomeriggio_leo']['inizio']} - {impegni['pomeriggio_leo']['fine']}):**\n\n{impegni['pomeriggio_leo']['cosa']}"
            t_sara = f"**👧 SARA ({impegni['pomeriggio_sara']['inizio']} - {impegni['pomeriggio_sara']['fine']}):**\n\n{impegni['pomeriggio_sara']['cosa']}"
            
            if "NONNI" in impegni['pomeriggio_leo']['chi']: st.error(t_leo)
            else: st.success(t_leo)
            
            if "NONNI" in impegni['pomeriggio_sara']['chi']: st.error(t_sara)
            else: st.success(t_sara)
            
        st.markdown("---")
