import streamlit as st
import json
import os
from datetime import datetime, timedelta

# 1. IMPOSTAZIONI PAGINA
st.set_page_config(page_title="Taxi Nipoti", page_icon="🚕", layout="centered")

FILE_MEMORIA = "programma_definitivo_v3.json" 
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

# 2. GESTIONE MEMORIA CON SETTIMANA TIPO
def crea_struttura_vuota():
    def sett_vuota():
        sett = {}
        chi_def = "🟢 FACCIAMO NOI GENITORI"
        
        for g in ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì"]:
            if g == "Lunedì":
                sett[g] = {
                    "mattina": {"chi": chi_def, "cosa": "Scuola 🏫"},
                    "sara_uguale": False,
                    "pomeriggio_leonardo": {"chi_andata": chi_def, "chi_ritorno": chi_def, "cosa": "Eufonio 🎺", "inizio": "", "fine": "18:00", "dove_ritorno": "Casa Nostra 🏠"},
                    "pomeriggio_sara": {"chi_andata": chi_def, "chi_ritorno": chi_def, "cosa": "Scuola 🏫", "inizio": "", "fine": "16:00", "dove_ritorno": "Casa Nostra 🏠"}
                }
            elif g == "Martedì" or g == "Venerdì":
                sett[g] = {
                    "mattina": {"chi": chi_def, "cosa": "Scuola 🏫"},
                    "sara_uguale": True,
                    "pomeriggio_leonardo": {"chi_andata": chi_def, "chi_ritorno": chi_def, "cosa": "Ginnastica Artistica 🤸‍♀️", "inizio": "17:00", "fine": "18:30", "dove_ritorno": "Casa Nostra 🏠"},
                    "pomeriggio_sara": {"chi_andata": chi_def, "chi_ritorno": chi_def, "cosa": "Ginnastica Artistica 🤸‍♀️", "inizio": "16:30", "fine": "17:30", "dove_ritorno": "Casa Nostra 🏠"}
                }
            elif g == "Mercoledì":
                sett[g] = {
                    "mattina": {"chi": chi_def, "cosa": "Scuola 🏫"},
                    "sara_uguale": False,
                    "pomeriggio_leonardo": {"chi_andata": chi_def, "chi_ritorno": chi_def, "cosa": "Yoga 🧘‍♂️", "inizio": "", "fine": "", "dove_ritorno": "Casa Nostra 🏠"},
                    "pomeriggio_sara": {"chi_andata": chi_def, "chi_ritorno": chi_def, "cosa": "Scuola 🏫", "inizio": "", "fine": "16:00", "dove_ritorno": "Casa Nostra 🏠"}
                }
            else: # Giovedì
                sett[g] = {
                    "mattina": {"chi": chi_def, "cosa": "Scuola 🏫"},
                    "sara_uguale": True,
                    "pomeriggio_leonardo": {"chi_andata": chi_def, "chi_ritorno": chi_def, "cosa": "Scuola 🏫", "inizio": "", "fine": "", "dove_ritorno": "Casa Nostra 🏠"},
                    "pomeriggio_sara": {"chi_andata": chi_def, "chi_ritorno": chi_def, "cosa": "Scuola 🏫", "inizio": "", "fine": "", "dove_ritorno": "Casa Nostra 🏠"}
                }
        return sett
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
                
                # --- LOGICA POMERIGGIO ---
                def formatta_blocco(nome, emoji, dati):
                    b_ritorno = "🔴 (NONNI)" if "NONNI" in dati['chi_ritorno'] else "🟢 (GENITORI)"
                    dest = dati.get('dove_ritorno', 'Casa Nostra 🏠')
                    
                    if dati['cosa'] == "Scuola 🏫":
                        orario_scuola = f" (ore {dati['fine']})" if dati['fine'] else ""
                        if "NONNI" in dati['chi_ritorno']:
                            return f"**{emoji} {nome}:** Fine giornata DA Scuola 🏫\n\n👉 **Ritiro{orario_scuola}:** {b_ritorno}\n📍 **Destinazione:** Portare a {dest}"
                        else:
                            return f"**{emoji} {nome}:** Fine giornata DA Scuola 🏫\n\n👉 **Ritiro{orario_scuola}:** {b_ritorno}"
                    
                    elif dati['cosa'] in ["Eufonio 🎺", "Yoga 🧘‍♂️"]:
                        if "NONNI" in dati['chi_ritorno']:
                            return (f"**{emoji} {nome}:** {dati['cosa']}\n\n👉 **Ritiro{nome} (ore {dati['fine']}):** {b_ritorno}\n*(📍 Riprendere DA {dati['cosa'].upper()} e portare a {dest})*")
                        else:
                            return (f"**{emoji} {nome}:** {dati['cosa']}\n\n👉 **Ritiro{nome} (ore {dati['fine']}):** {b_ritorno}")
                    
                    else:
                        b_andata = "🔴 (NONNI)" if "NONNI" in dati.get('chi_andata', '') else "🟢 (GENITORI)"
                        attivita = dati['cosa'].upper()
                        
                        if "NONNI" in dati.get('chi_andata', ''):
                            txt_andata = f"👉 **Andata (ore {dati['inizio']}):** {b_andata}\n*(📍 Prendere DA Scuola 🏫 e portare a {attivita})*"
                        else:
                            txt_andata = f"👉 **Andata (ore {dati['inizio']}):** {b_andata}"
                            
                        if "NONNI" in dati['chi_ritorno']:
                            txt_ritorno = f"👉 **Ritorno (ore {dati['fine']}):** {b_ritorno}\n*(📍 Riprendere DA {attivita} e portare a {dest})*"
                        else:
                            txt_ritorno = f"👉 **Ritorno (ore {dati['fine']}):** {b_ritorno}"
                            
                        return f"**{emoji} {nome}:** {dati['cosa']}\n\n{txt_andata}\n\n{txt_ritorno}"

                def calcola_colore(dati):
                    if dati['cosa'] in ["Scuola 🏫", "Eufonio 🎺", "Yoga 🧘‍♂️"]:
                        return "red" if "NONNI" in dati['chi_ritorno'] else "green"
                    else:
                        andata_n = "NONNI" in dati.get('chi_andata', '')
                        ritorno_n = "NONNI" in dati['chi_ritorno']
                        if andata_n and ritorno_n: return "red"
                        elif not andata_n and not ritorno_n: return "green"
                        else: return "orange"

                colore_l = calcola_colore(imp['pomeriggio_leonardo'])
                colore_s = calcola_colore(imp['pomeriggio_sara'])

                identici = (
                    imp.get("sara_uguale", True) and
                    imp['pomeriggio_leonardo']['chi_andata'] == imp['pomeriggio_sara']['chi_andata'] and
                    imp['pomeriggio_leonardo']['chi_ritorno'] == imp['pomeriggio_sara']['chi_ritorno'] and
                    imp['pomeriggio_leonardo']['cosa'] == imp['pomeriggio_sara']['cosa'] and
                    imp['pomeriggio_leonardo']['inizio'] == imp['pomeriggio_sara']['inizio'] and
                    imp['pomeriggio_leonardo']['fine'] == imp['pomeriggio_sara']['fine'] and
                    (not ("NONNI" in imp['pomeriggio_leonardo']['chi_ritorno']) or imp['pomeriggio_leonardo'].get('dove_ritorno') == imp['pomeriggio_sara'].get('dove_ritorno'))
                )

                if identici:
                    t_ins = formatta_blocco("LEONARDO E SARA", "👦👧", imp['pomeriggio_leonardo'])
                    if colore_l == "red": st.error(t_ins)
                    elif colore_l == "orange": st.warning(t_ins)
                    else: st.success(t_ins)
                else:
                    t_l = formatta_blocco("LEONARDO", "👦", imp['pomeriggio_leonardo'])
                    if colore_l == "red": st.error(t_l)
                    elif colore_l == "orange": st.warning(t_l)
                    else: st.success(t_l)
                    
                    t_s = formatta_blocco("SARA", "👧", imp['pomeriggio_sara'])
                    if colore_s == "red": st.error(t_s)
                    elif colore_s == "orange": st.warning(t_s)
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
        k_id = f"{sett_scelta}_{giorno_sel}"
        dati_g = programma[sett_scelta][giorno_sel]
        
        # --- MATTINA ---
        st.subheader("☀️ Mattina: Scuola 🏫")
        chi_m = st.selectbox("Chi li porta a scuola?", OPZIONI_CHI, index=OPZIONI_CHI.index(dati_g["mattina"]["chi"]), key=f"m_chi_{k_id}")
        
        st.markdown("---")
        
        # --- POMERIGGIO LEONARDO ---
        st.subheader("👦 Pomeriggio LEONARDO")
        idx_cosa_l = OPZIONI_ATTIVITA_LEO.index(dati_g["pomeriggio_leonardo"]["cosa"]) if dati_g["pomeriggio_leonardo"]["cosa"] in OPZIONI_ATTIVITA_LEO else OPZIONI_ATTIVITA_LEO.index("Scuola 🏫")
        cos_l = st.selectbox("Attività Leonardo?", OPZIONI_ATTIVITA_LEO, index=idx_cosa_l, key=f"l_cosa_{k_id}")
        
        opz_dest_l = ["Casa Nostra 🏠", "Casa Nonni 🏡", "Lavoro Mamma 💼"] if cos_l == "Scuola 🏫" else ["Casa Nostra 🏠", "Casa Nonni 🏡"]
        dest_attuale_l = dati_g["pomeriggio_leonardo"].get("dove_ritorno", "Casa Nostra 🏠")
        idx_dest_l = opz_dest_l.index(dest_attuale_l) if dest_attuale_l in opz_dest_l else 0

        if cos_l == "Scuola 🏫":
            chi_and_l = OPZIONI_CHI[0]
            c_rit, c_dest = st.columns(2)
            chi_rit_l = c_rit.selectbox("🚕 Chi lo riprende DA Scuola?", OPZIONI_CHI, index=OPZIONI_CHI.index(dati_g["pomeriggio_leonardo"]["chi_ritorno"]), key=f"l_rit_{k_id}")
            
            if "NONNI" in chi_rit_l:
                dove_rit_l = c_dest.selectbox("📍 Dove portarlo?", opz_dest_l, index=idx_dest_l, key=f"l_dest_{k_id}")
            else:
                dove_rit_l = "Casa Nostra 🏠"
            
            in_l, fi_l = "", ""
        
        elif cos_l in ["Eufonio 🎺", "Yoga 🧘‍♂️"]:
            chi_and_l = OPZIONI_CHI[0]
            
            if cos_l == "Eufonio 🎺":
                st.info("⏱️ Regola Eufonio: **Rimane a scuola, bisogna solo andarlo a riprendere alle 18:00.**")
            else:
                st.info("🧘‍♂️ Regola Yoga: **Rimane a scuola, bisogna solo andarlo a riprendere.**")
                
            c_rit, c_dest = st.columns(2)
            nome_att = cos_l.split()[0]
            chi_rit_l = c_rit.selectbox(f"🚕 Chi RIPRENDE Leonardo DA {nome_att}?", OPZIONI_CHI, index=OPZIONI_CHI.index(dati_g["pomeriggio_leonardo"].get("chi_ritorno", OPZIONI_CHI[0])), key=f"l_rit_int_{k_id}")
            
            if "NONNI" in chi_rit_l:
                dove_rit_l = c_dest.selectbox("📍 Dove portarlo?", opz_dest_l, index=idx_dest_l, key=f"l_dest_int_{k_id}")
            else:
                dove_rit_l = "Casa Nostra 🏠"
                
            in_l = ""
            if cos_l == "Eufonio 🎺":
                fi_l = "18:00"
            else:
                fi_l = st.text_input("Orario Ritiro", dati_g["pomeriggio_leonardo"]["fine"], key=f"l_fi_int_{k_id}")
            
        else:
            c_and, c_rit = st.columns(2)
            chi_and_l = c_and.selectbox("🚕 Chi lo PORTA (Andata)?", OPZIONI_CHI, index=OPZIONI_CHI.index(dati_g["pomeriggio_leonardo"].get("chi_andata", OPZIONI_CHI[0])), key=f"l_and_{k_id}")
            chi_rit_l = c_rit.selectbox("🚕 Chi lo RIPRENDE DA {cos_l} (Ritorno)?", OPZIONI_CHI, index=OPZIONI_CHI.index(dati_g["pomeriggio_leonardo"].get("chi_ritorno", OPZIONI_CHI[0])), key=f"l_rit_est_{k_id}")
            
            if "NONNI" in chi_rit_l:
                c_dest, c_vuoto = st.columns(2)
                dove_rit_l = c_dest.selectbox("📍 Al ritorno, dove va?", opz_dest_l, index=idx_dest_l, key=f"l_dest_est_{k_id}")
            else:
                dove_rit_l = "Casa Nostra 🏠"
            
            if cos_l == "Ginnastica Artistica 🤸‍♀️":
                st.info("⏱️ Orari prefissati Leonardo: **17:00 - 18:30**")
                in_l, fi_l = "17:00", "18:30"
            else:
                c_in, c_fi = st.columns(2)
                in_l = c_in.text_input("Orario Inizio", dati_g["pomeriggio_leonardo"]["inizio"], key=f"l_in_{k_id}")
                fi_l = c_fi.text_input("Orario Fine", dati_g["pomeriggio_leonardo"]["fine"], key=f"l_fi_{k_id}")

        # --- POMERIGGIO SARA ---
        st.markdown("---")
        
        if cos_l in ["Eufonio 🎺", "Yoga 🧘‍♂️"]:
            nome_attivita_leo = cos_l.split()[0]
            st.warning(f"⚠️ Poiché Leonardo ha {nome_attivita_leo}, Sara esce DA Scuola alle **16:00**.")
            st.subheader("👧 Pomeriggio SARA")
            sara_uguale = False
            cos_s = "Scuola 🏫"
            chi_and_s = OPZIONI_CHI[0]
            
            opz_dest_s = ["Casa Nostra 🏠", "Casa Nonni 🏡", "Lavoro Mamma 💼"]
            dest_attuale_s = dati_g["pomeriggio_sara"].get("dove_ritorno", "Casa Nostra 🏠")
            idx_dest_s = opz_dest_s.index(dest_attuale_s) if dest_attuale_s in opz_dest_s else 0
            
            c_rit_s, c_dest_s = st.columns(2)
            chi_rit_s = c_rit_s.selectbox("🚕 Chi riprende Sara DA Scuola?", OPZIONI_CHI, index=OPZIONI_CHI.index(dati_g["pomeriggio_sara"]["chi_ritorno"]), key=f"s_rit_eu_{k_id}")
            
            if "NONNI" in chi_rit_s:
                dove_rit_s = c_dest_s.selectbox("📍 Dove portarla?", opz_dest_s, index=idx_dest_s, key=f"s_dest_eu_{k_id}")
            else:
                dove_rit_s = "Casa Nostra 🏠"
                
            in_s, fi_s = "", "16:00"
            
        elif cos_l not in OPZIONI_ATTIVITA_SARA:
            st.warning(f"⚠️ Poiché Leonardo fa {cos_l} (che Sara non fa), devi scegliere un'attività diversa per lei.")
            st.subheader("👧 Pomeriggio SARA")
            sara_uguale = False
            
            idx_cosa_s = OPZIONI_ATTIVITA_SARA.index(dati_g["pomeriggio_sara"]["cosa"]) if dati_g["pomeriggio_sara"]["cosa"] in OPZIONI_ATTIVITA_SARA else OPZIONI_ATTIVITA_SARA.index("Scuola 🏫")
            cos_s = st.selectbox("Attività Sara?", OPZIONI_ATTIVITA_SARA, index=idx_cosa_s, key=f"s_cosa_{k_id}")
            
            opz_dest_s = ["Casa Nostra 🏠", "Casa Nonni 🏡", "Lavoro Mamma 💼"] if cos_s == "Scuola 🏫" else ["Casa Nostra 🏠", "Casa Nonni 🏡"]
            dest_attuale_s = dati_g["pomeriggio_sara"].get("dove_ritorno", "Casa Nostra 🏠")
            idx_dest_s = opz_dest_s.index(dest_attuale_s) if dest_attuale_s in opz_dest_s else 0

            if cos_s == "Scuola 🏫":
                chi_and_s = OPZIONI_CHI[0]
                c_rit_s, c_dest_s = st.columns(2)
                chi_rit_s = c_rit_s.selectbox("🚕 Chi la riprende DA Scuola?", OPZIONI_CHI, index=OPZIONI_CHI.index(dati_g["pomeriggio_sara"]["chi_ritorno"]), key=f"s_rit_{k_id}")
                
                if "NONNI" in chi_rit_s:
                    dove_rit_s = c_dest_s.selectbox("📍 Dove portarla?", opz_dest_s, index=idx_dest_s, key=f"s_dest_{k_id}")
                else:
                    dove_rit_s = "Casa Nostra 🏠"
                in_s, fi_s = "", ""
            else:
                c_and_s, c_rit_s = st.columns(2)
                chi_and_s = c_and_s.selectbox("🚕 Chi la PORTA (Andata)?", OPZIONI_CHI, index=OPZIONI_CHI.index(dati_g["pomeriggio_sara"].get("chi_andata", OPZIONI_CHI[0])), key=f"s_and_{k_id}")
                chi_rit_s = c_rit_s.selectbox("🚕 Chi la RIPRENDE DA {cos_s}?", OPZIONI_CHI, index=OPZIONI_CHI.index(dati_g["pomeriggio_sara"].get("chi_ritorno", OPZIONI_CHI[0])), key=f"s_rit_est_{k_id}")
                
                if "NONNI" in chi_rit_s:
                    c_dest_s, c_vuoto_s = st.columns(2)
                    dove_rit_s = c_dest_s.selectbox("📍 Al ritorno, dove va?", opz_dest_s, index=idx_dest_s, key=f"s_dest_est_{k_id}")
                else:
                    dove_rit_s = "Casa Nostra 🏠"

                if cos_s == "Ginnastica Artistica 🤸‍♀️":
                    st.info("⏱️ Orari prefissati Sara: **16:30 - 17:30**")
                    in_s, fi_s = "16:30", "17:30"
                else:
                    c_in_s, c_fi_s = st.columns(2)
                    in_s = c_in_s.text_input("Orario Inizio (S)", dati_g["pomeriggio_sara"]["inizio"], key=f"s_in_{k_id}")
                    fi_s = c_fi_s.text_input("Orario Fine (S)", dati_g["pomeriggio_sara"]["fine"], key=f"s_fi_{k_id}")
            
        else:
            sara_uguale = st.checkbox("✅ Sara fa lo stesso di Leonardo (stessa destinazione)", value=dati_g.get("sara_uguale", True), key=f"s_uguale_{k_id}")
            
            if not sara_uguale:
                st.subheader("👧 Pomeriggio SARA")
                idx_cosa_s = OPZIONI_ATTIVITA_SARA.index(dati_g["pomeriggio_sara"]["cosa"]) if dati_g["pomeriggio_sara"]["cosa"] in OPZIONI_ATTIVITA_SARA else OPZIONI_ATTIVITA_SARA.index("Scuola 🏫")
                cos_s = st.selectbox("Attività Sara?", OPZIONI_ATTIVITA_SARA, index=idx_cosa_s, key=f"s_cosa_alt_{k_id}")
                
                opz_dest_s = ["Casa Nostra 🏠", "Casa Nonni 🏡", "Lavoro Mamma 💼"] if cos_s == "Scuola 🏫" else ["Casa Nostra 🏠", "Casa Nonni 🏡"]
                dest_attuale_s = dati_g["pomeriggio_sara"].get("dove_ritorno", "Casa Nostra 🏠")
                idx_dest_s = opz_dest_s.index(dest_attuale_s) if dest_attuale_s in opz_dest_s else 0

                if cos_s == "Scuol
