import streamlit as st
import json
import os
from datetime import datetime, timedelta

# 1. IMPOSTAZIONI PAGINA
st.set_page_config(page_title="Taxi Nipoti", page_icon="🚕", layout="centered")

FILE_MEMORIA = "programma_v12.json" # Memoria aggiornata per la regola Eufonio+Yoga
OPZIONI_CHI = ["🟢 FACCIAMO NOI GENITORI", "🔴 TOCCA AI NONNI"]

# Liste attività separate e personalizzate
OPZIONI_ATTIVITA_LEO = ["Ginnastica Artistica 🤸‍♀️", "Eufonio 🎺", "Yoga 🧘‍♂️", "Scuola 🏫"]
OPZIONI_ATTIVITA_SARA = ["Ginnastica Artistica 🤸‍♀️", "Scuola 🏫"]

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
            "pomeriggio_leonardo": {"chi_andata": "🟢 FACCIAMO NOI GENITORI", "chi_ritorno": "🟢 FACCIAMO NOI GENITORI", "cosa": "Scuola 🏫", "inizio": "", "fine": "", "dove_ritorno": "Casa Nostra 🏠"},
            "pomeriggio_sara": {"chi_andata": "🟢 FACCIAMO NOI GENITORI", "chi_ritorno": "🟢 FACCIAMO NOI GENITORI", "cosa": "Scuola 🏫", "inizio": "", "fine": "", "dove_ritorno": "Casa Nostra 🏠"}
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
                
                if info["data_obj"] == cal["oggi_obj"]:
                    st.markdown(f"## 🌟 {info['data_testo'].upper()} (OGGI)")
                else:
                    st.markdown(f"### 📅 {info['data_testo']}")
                
                # --- MATTINA ---
                if "NONNI" in imp['mattina']['chi']:
                    st.error(f"**☀️ MATTINA:** Scuola 🏫\n\n👉 *Ore 7:00 vi aspettiamo a casa!*")
                else:
                    st.success(f"**☀️ MATTINA:** Scuola 🏫")
                
                # --- LOGICA POMERIGGIO E NASCONDIMENTO DESTINAZIONE ---
                def formatta_blocco(nome, emoji, dati):
                    b_ritorno = "🔴 (NONNI)" if "NONNI" in dati['chi_ritorno'] else "🟢 (GENITORI)"
                    dest = dati.get('dove_ritorno', 'Casa Nostra 🏠')
                    
                    if dati['cosa'] == "Scuola 🏫":
                        orario_scuola = f" (ore {dati['fine']})" if dati['fine'] else ""
                        if "NONNI" in dati['chi_ritorno']:
                            return f"**{emoji} {nome}:** Fine giornata a Scuola 🏫\n\n👉 **Ritiro{orario_scuola}:** {b_ritorno}\n📍 **Destinazione:** Portare a {dest}"
                        else:
                            return f"**{emoji} {nome}:** Fine giornata a Scuola 🏫\n\n👉 **Ritiro{orario_scuola}:** {b_ritorno}"
                    
                    elif dati['cosa'] == "Eufonio 🎺":
                        if "NONNI" in dati['chi_ritorno']:
                            return (f"**{emoji} {nome}:** {dati['cosa']}\n\n👉 **Ritorno (ore {dati['fine']}):** {b_ritorno}\n*(📍 Riprendere da EUFONIO 🎺 e portare a {dest})*")
                        else:
                            return (f"**{emoji} {nome}:** {dati['cosa']}\n\n👉 **Ritorno (ore {dati['fine']}):** {b_ritorno}")
                    
                    else:
                        b_andata = "🔴 (NONNI)" if "NONNI" in dati.get('chi_andata', '') else "🟢 (GENITORI)"
                        attivita = dati['cosa'].upper()
                        
                        if "NONNI" in dati.get('chi_andata', ''):
                            txt_andata = f"👉 **Andata (ore {dati['inizio']}):** {b_andata}\n*(📍 Prendere a Scuola 🏫 e portare a {attivita})*"
                        else:
                            txt_andata = f"👉 **Andata (ore {dati['inizio']}):** {b_andata}"
                            
                        if "NONNI" in dati['chi_ritorno']:
                            txt_ritorno = f"👉 **Ritorno (ore {dati['fine']}):** {b_ritorno}\n*(📍 Riprendere da {attivita} e portare a {dest})*"
                        else:
                            txt_ritorno = f"👉 **Ritorno (ore {dati['fine']}):** {b_ritorno}"
                            
                        return f"**{emoji} {nome}:** {dati['cosa']}\n\n{txt_andata}\n\n{txt_ritorno}"

                coinvolge_nonni_l = "NONNI" in imp['pomeriggio_leonardo'].get('chi_andata','') or "NONNI" in imp['pomeriggio_leonardo']['chi_ritorno']
                coinvolge_nonni_s = "NONNI" in imp['pomeriggio_sara'].get('chi_andata','') or "NONNI" in imp['pomeriggio_sara']['chi_ritorno']

                identici = (
                    imp.get("sara_uguale", True) and
                    imp['pomeriggio_leonardo']['chi_andata'] == imp['pomeriggio_sara']['chi_andata'] and
                    imp['pomeriggio_leonardo']['chi_ritorno'] == imp['pomeriggio_sara']['chi_ritorno'] and
                    imp['pomeriggio_leonardo']['cosa'] == imp['pomeriggio_sara']['cosa'] and
                    imp['pomeriggio_leonardo']['inizio'] == imp['pomeriggio_sara']['inizio'] and
                    imp['pomeriggio_leonardo']['fine'] == imp['pomeriggio_sara']['fine'] and
                    imp['pomeriggio_leonardo'].get('dove_ritorno') == imp['pomeriggio_sara'].get('dove_ritorno')
                )

                if identici:
                    t_ins = formatta_blocco("LEONARDO E SARA", "👦👧", imp['pomeriggio_leonardo'])
                    if coinvolge_nonni_l: st.error(t_ins)
                    else: st.success(t_ins)
                else:
                    t_l = formatta_blocco("LEONARDO", "👦", imp['pomeriggio_leonardo'])
                    if coinvolge_nonni_l: st.error(t_l)
                    else: st.success(t_l)
                    
                    t_s = formatta_blocco("SARA", "👧", imp['pomeriggio_sara'])
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
        idx_cosa_l = OPZIONI_ATTIVITA_LEO.index(dati_g["pomeriggio_leonardo"]["cosa"]) if dati_g["pomeriggio_leonardo"]["cosa"] in OPZIONI_ATTIVITA_LEO else OPZIONI_ATTIVITA_LEO.index("Scuola 🏫")
        cos_l = st.selectbox("Attività Leonardo?", OPZIONI_ATTIVITA_LEO, index=idx_cosa_l, key="l2")
        
        opz_dest_l = ["Casa Nostra 🏠", "Casa Nonni 🏡", "Lavoro Mamma 💼"] if cos_l == "Scuola 🏫" else ["Casa Nostra 🏠", "Casa Nonni 🏡"]
        dest_attuale_l = dati_g["pomeriggio_leonardo"].get("dove_ritorno", "Casa Nostra 🏠")
        idx_dest_l = opz_dest_l.index(dest_attuale_l) if dest_attuale_l in opz_dest_l else 0

        if cos_l == "Scuola 🏫":
            chi_and_l = OPZIONI_CHI[0]
            c_rit, c_dest = st.columns(2)
            chi_rit_l = c_rit.selectbox("🚕 Chi lo riprende da Scuola?", OPZIONI_CHI, index=OPZIONI_CHI.index(dati_g["pomeriggio_leonardo"]["chi_ritorno"]), key="l_rit")
            dove_rit_l = c_dest.selectbox("📍 Dove portarlo?", opz_dest_l, index=idx_dest_l, key="l_dest")
            in_l, fi_l = "", ""
        
        elif cos_l == "Eufonio 🎺":
            chi_and_l = OPZIONI_CHI[0]
            st.info("⏱️ Regola Eufonio attiva: **Bisogna solo andarlo a riprendere alle 18:00.**")
            c_rit, c_dest = st.columns(2)
            chi_rit_l = c_rit.selectbox("🚕 Chi RIPRENDE Leonardo?", OPZIONI_CHI, index=OPZIONI_CHI.index(dati_g["pomeriggio_leonardo"].get("chi_ritorno", OPZIONI_CHI[0])), key="l_rit")
            dove_rit_l = c_dest.selectbox("📍 Dove portarlo?", opz_dest_l, index=idx_dest_l, key="l_dest")
            in_l, fi_l = "", "18:00"
            
        else:
            c_and, c_rit = st.columns(2)
            chi_and_l = c_and.selectbox("🚕 Chi lo PORTA (Andata)?", OPZIONI_CHI, index=OPZIONI_CHI.index(dati_g["pomeriggio_leonardo"].get("chi_andata", OPZIONI_CHI[0])), key="l_and")
            chi_rit_l = c_rit.selectbox("🚕 Chi lo RIPRENDE (Ritorno)?", OPZIONI_CHI, index=OPZIONI_CHI.index(dati_g["pomeriggio_leonardo"].get("chi_ritorno", OPZIONI_CHI[0])), key="l_rit")
            
            c_dest, c_vuoto = st.columns(2)
            dove_rit_l = c_dest.selectbox("📍 Al ritorno, dove va?", opz_dest_l, index=idx_dest_l, key="l_dest")
            
            if cos_l == "Ginnastica Artistica 🤸‍♀️":
                st.info("⏱️ Orari prefissati Leonardo: **17:00 - 18:30**")
                in_l, fi_l = "17:00", "18:30"
            else:
                c_in, c_fi = st.columns(2)
                in_l = c_in.text_input("Orario Inizio", dati_g["pomeriggio_leonardo"]["inizio"], key="l_in")
                fi_l = c_fi.text_input("Orario Fine", dati_g["pomeriggio_leonardo"]["fine"], key="l_fi")

        # --- POMERIGGIO SARA ---
        st.markdown("---")
        
        # ECCEZIONE PER YOGA ED EUFONIO: Sara va sempre ripresa a scuola
        if cos_l in ["Eufonio 🎺", "Yoga 🧘‍♂️"]:
            nome_attivita_leo = cos_l.split()[0] # Prende solo il nome senza l'emoji per la frase
            st.warning(f"⚠️ Poiché Leonardo ha {nome_attivita_leo}, Sara esce da Scuola alle **16:00**.")
            st.subheader("👧 Pomeriggio SARA")
            sara_uguale = False
            cos_s = "Scuola 🏫"
            chi_and_s = OPZIONI_CHI[0]
            
            opz_dest_s = ["Casa Nostra 🏠", "Casa Nonni 🏡", "Lavoro Mamma 💼"]
            dest_attuale_s = dati_g["pomeriggio_sara"].get("dove_ritorno", "Casa Nostra 🏠")
            idx_dest_s = opz_dest_s.index(dest_attuale_s) if dest_attuale_s in opz_dest_s else 0
            
            c_rit_s, c_dest_s = st.columns(2)
            chi_rit_s = c_rit_s.selectbox("🚕 Chi riprende Sara?", OPZIONI_CHI, index=OPZIONI_CHI.index(dati_g["pomeriggio_sara"]["chi_ritorno"]), key="s_rit_eu")
            dove_rit_s = c_dest_s.selectbox("📍 Dove portarla?", opz_dest_s, index=idx_dest_s, key="s_dest_eu")
            in_s, fi_s = "", "16:00"
            
        elif cos_l not in OPZIONI_ATTIVITA_SARA:
            st.warning(f"⚠️ Poiché Leonardo fa {cos_l} (che Sara non fa), devi scegliere un'attività diversa per lei.")
            st.subheader("👧 Pomeriggio SARA")
            sara_uguale = False
            
            idx_cosa_s = OPZIONI_ATTIVITA_SARA.index(dati_g["pomeriggio_sara"]["cosa"]) if dati_g["pomeriggio_sara"]["cosa"] in OPZIONI_ATTIVITA_SARA else OPZIONI_ATTIVITA_SARA.index("Scuola 🏫")
            cos_s = st.selectbox("Attività Sara?", OPZIONI_ATTIVITA_SARA, index=idx_cosa_s, key="s2")
            
            opz_dest_s = ["Casa Nostra 🏠", "Casa Nonni 🏡", "Lavoro Mamma 💼"] if cos_s == "Scuola 🏫" else ["Casa Nostra 🏠", "Casa Nonni 🏡"]
            dest_attuale_s = dati_g["pomeriggio_sara"].get("dove_ritorno", "Casa Nostra 🏠")
            idx_dest_s = opz_dest_s.index(dest_attuale_s) if dest_attuale_s in opz_dest_s else 0

            if cos_s == "Scuola 🏫":
                chi_and_s = OPZIONI_CHI[0]
                c_rit_s, c_dest_s = st.columns(2)
                chi_rit_s = c_rit_s.selectbox("🚕 Chi la riprende da Scuola?", OPZIONI_CHI, index=OPZIONI_CHI.index(dati_g["pomeriggio_sara"]["chi_ritorno"]), key="s_rit")
                dove_rit_s = c_dest_s.selectbox("📍 Dove portarla?", opz_dest_s, index=idx_dest_s, key="s_dest")
                in_s, fi_s = "", ""
            else:
                c_and_s, c_rit_s = st.columns(2)
                chi_and_s = c_and_s.selectbox("🚕 Chi la PORTA (Andata)?", OPZIONI_CHI, index=OPZIONI_CHI.index(dati_g["pomeriggio_sara"].get("chi_andata", OPZIONI_CHI[0])), key="s_and")
                chi_rit_s = c_rit_s.selectbox("🚕 Chi la RIPRENDE (Ritorno)?", OPZIONI_CHI, index=OPZIONI_CHI.index(dati_g["pomeriggio_sara"].get("chi_ritorno", OPZIONI_CHI[0])), key="s_rit")
                
                c_dest_s, c_vuoto_s = st.columns(2)
                dove_rit_s = c_dest_s.selectbox("📍 Al ritorno, dove va?", opz_dest_s, index=idx_dest_s, key="s_dest")

                if cos_s == "Ginnastica Artistica 🤸‍♀️":
                    st.info("⏱️ Orari prefissati Sara: **16:30 - 17:30**")
                    in_s, fi_s = "16:30", "17:30"
                else:
                    c_in_s, c_fi_s = st.columns(2)
                    in_s = c_in_s.text_input("Orario Inizio (S)", dati_g["pomeriggio_sara"]["inizio"], key="s_in")
                    fi_s = c_fi_s.text_input("Orario Fine (S)", dati_g["pomeriggio_sara"]["fine"], key="s_fi")
            
        else:
            sara_uguale = st.checkbox("✅ Sara fa lo stesso di Leonardo (stessa destinazione)", value=dati_g.get("sara_uguale", True))
            
            if not sara_uguale:
                st.subheader("👧 Pomeriggio SARA")
                idx_cosa_s = OPZIONI_ATTIVITA_SARA.index(dati_g["pomeriggio_sara"]["cosa"]) if dati_g["pomeriggio_sara"]["cosa"] in OPZIONI_ATTIVITA_SARA else OPZIONI_ATTIVITA_SARA.index("Scuola 🏫")
                cos_s = st.selectbox("Attività Sara?", OPZIONI_ATTIVITA_SARA, index=idx_cosa_s, key="s2")
                
                opz_dest_s = ["Casa Nostra 🏠", "Casa Nonni 🏡", "Lavoro Mamma 💼"] if cos_s == "Scuola 🏫" else ["Casa Nostra 🏠", "Casa Nonni 🏡"]
                dest_attuale_s = dati_g["pomeriggio_sara"].get("dove_ritorno", "Casa Nostra 🏠")
                idx_dest_s = opz_dest_s.index(dest_attuale_s) if dest_attuale_s in opz_dest_s else 0

                if cos_s == "Scuola 🏫":
                    chi_and_s = OPZIONI_CHI[0]
                    c_rit_s, c_dest_s = st.columns(2)
                    chi_rit_s = c_rit_s.selectbox("🚕 Chi la riprende da Scuola?", OPZIONI_CHI, index=OPZIONI_CHI.index(dati_g["pomeriggio_sara"]["chi_ritorno"]), key="s_rit")
                    dove_rit_s = c_dest_s.selectbox("📍 Dove portarla?", opz_dest_s, index=idx_dest_s, key="s_dest")
                    in_s, fi_s = "", ""
                else:
                    c_and_s, c_rit_s = st.columns(2)
                    chi_and_s = c_and_s.selectbox("🚕 Chi la PORTA (Andata)?", OPZIONI_CHI, index=OPZIONI_CHI.index(dati_g["pomeriggio_sara"].get("chi_andata", OPZIONI_CHI[0])), key="s_and")
                    chi_rit_s = c_rit_s.selectbox("🚕 Chi la RIPRENDE (Ritorno)?", OPZIONI_CHI, index=OPZIONI_CHI.index(dati_g["pomeriggio_sara"].get("chi_ritorno", OPZIONI_CHI[0])), key="s_rit")
                    
                    c_dest_s, c_vuoto_s = st.columns(2)
                    dove_rit_s = c_dest_s.selectbox("📍 Al ritorno, dove va?", opz_dest_s, index=idx_dest_s, key="s_dest")

                    if cos_s == "Ginnastica Artistica 🤸‍♀️":
                        st.info("⏱️ Orari prefissati Sara: **16:30 - 17:30**")
                        in_s, fi_s = "16:30", "17:30"
                    else:
                        c_in_s, c_fi_s = st.columns(2)
                        in_s = c_in_s.text_input("Orario Inizio (S)", dati_g["pomeriggio_sara"]["inizio"], key="s_in")
                        fi_s = c_fi_s.text_input("Orario Fine (S)", dati_g["pomeriggio_sara"]["fine"], key="s_fi")
            else:
                chi_and_s, chi_rit_s, cos_s, dove_rit_s = chi_and_l, chi_rit_l, cos_l, dove_rit_l
                if cos_s == "Ginnastica Artistica 🤸‍♀️":
                    in_s, fi_s = "16:30", "17:30"
                elif cos_s == "Scuola 🏫":
                    in_s, fi_s = "", ""
                else:
                    in_s, fi_s = in_l, fi_l

        if st.button("💾 SALVA PROGRAMMA"):
            programma[sett_scelta][giorno_sel] = {
                "mattina": {"chi": chi_m, "cosa": "Scuola 🏫"},
                "pomeriggio_leonardo": {"chi_andata": chi_and_l, "chi_ritorno": chi_rit_l, "cosa": cos_l, "inizio": in_l, "fine": fi_l, "dove_ritorno": dove_rit_l},
                "sara_uguale": sara_uguale,
                "pomeriggio_sara": {"chi_andata": chi_and_s, "chi_ritorno": chi_rit_s, "cosa": cos_s, "inizio": in_s, "fine": fi_s, "dove_ritorno": dove_rit_s}
            }
            salva_programma(programma)
            st.success("Programma salvato con successo!")
            st.rerun()
