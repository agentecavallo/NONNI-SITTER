import streamlit as st
import json
import os
import requests
from datetime import datetime, timedelta

# 1. IMPOSTAZIONI PAGINA E STATO NAVIGAZIONE
st.set_page_config(page_title="Taxi Nipoti", page_icon="🚕", layout="centered")

if "week" not in st.session_state:
    st.session_state.week = "corrente"
if "day" not in st.session_state:
    st.session_state.day = None
if "genitori_unlocked" not in st.session_state:
    st.session_state.genitori_unlocked = False

FILE_MEMORIA = "programma_definitivo_v8.json" 
OPZIONI_CHI = ["🟢 GENITORI", "🔴 NONNI"]

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

def crea_struttura_vuota():
    def sett_vuota():
        sett = {}
        chi_def = "🟢 GENITORI"
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
            else: 
                sett[g] = {
                    "mattina": {"chi": chi_def, "cosa": "Scuola 🏫"},
                    "sara_uguale": True,
                    "pomeriggio_leonardo": {"chi_andata": chi_def, "chi_ritorno": chi_def, "cosa": "Scuola 🏫", "inizio": "", "fine": "", "dove_ritorno": "Casa Nostra 🏠"},
                    "pomeriggio_sara": {"chi_andata": chi_def, "chi_ritorno": chi_def, "cosa": "Scuola 🏫", "inizio": "", "fine": "", "dove_ritorno": "Casa Nostra 🏠"}
                }
        return sett
    return {"corrente": sett_vuota(), "prossima": sett_vuota()}

# --- FUNZIONI JSONBIN ---
def carica_programma():
    try:
        api_key = st.secrets["JSONBIN_KEY"]
        bin_id = st.secrets["JSONBIN_BIN_ID"]
        url = f"https://api.jsonbin.io/v3/b/{bin_id}"
        headers = {"X-Master-Key": api_key}
        
        req = requests.get(url, headers=headers)
        if req.status_code == 200:
            dati = req.json().get("record")
            if dati and "corrente" in dati: 
                return dati
        return crea_struttura_vuota()
    except Exception as e:
        if os.path.exists(FILE_MEMORIA):
            try:
                with open(FILE_MEMORIA, "r", encoding="utf-8") as file: return json.load(file)
            except: return crea_struttura_vuota()
        return crea_struttura_vuota()

def salva_programma(dati):
    salvato_cloud = False
    try:
        api_key = st.secrets["JSONBIN_KEY"]
        bin_id = st.secrets["JSONBIN_BIN_ID"]
        url = f"https://api.jsonbin.io/v3/b/{bin_id}"
        headers = {
            "Content-Type": "application/json",
            "X-Master-Key": api_key
        }
        req = requests.put(url, json=dati, headers=headers)
        if req.status_code == 200:
            salvato_cloud = True
    except:
        pass
    
    with open(FILE_MEMORIA, "w", encoding="utf-8") as file:
        json.dump(dati, file, indent=4)
        
    return salvato_cloud

cal = ottieni_calendario()
programma = carica_programma()

# ==========================================
# 3. INTERFACCIA A SCHEDE
# ==========================================
sch_nonni, sch_genitori = st.tabs(["🚕 Vista NONNI", "⚙️ Pannello GENITORI"])

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
                        if "NONNI" in dati['chi_ritorno']:
                            return f"**{emoji} {nome}:** Uscita scuola ore 16:00 🏫\n\n👉 **Ritiro:** {b_ritorno}\n📍 **Destinazione:** Portare a {dest}"
                        else:
                            return f"**{emoji} {nome}:** Uscita scuola ore 16:00 🏫\n\n👉 **Ritiro:** {b_ritorno}"
                    
                    elif dati['cosa'] in ["Eufonio 🎺", "Yoga 🧘‍♂️"]:
                        if "NONNI" in dati['chi_ritorno']:
                            return (f"**{emoji} {nome}:** {dati['cosa']}\n\n👉 **Ritiro {nome} (ore {dati['fine']}):** {b_ritorno}\n*(📍 Riprendere da {dati['cosa'].upper()} e portare a {dest})*")
                        else:
                            return (f"**{emoji} {nome}:** {dati['cosa']}\n\n👉 **Ritiro {nome} (ore {dati['fine']}):** {b_ritorno}")
                    
                    else:
                        b_andata = "🔴 (NONNI)" if "NONNI" in dati.get('chi_andata', '') else "🟢 (GENITORI)"
                        attivita = dati['cosa'].upper()
                        
                        if "NONNI" in dati.get('chi_andata', ''):
                            txt_andata = f"👉 **Andata (ore {dati['inizio']}):** {b_andata}\n*(📍 Prendere da scuola 🏫 e portare a {attivita})*"
                        else:
                            txt_andata = f"👉 **Andata (ore {dati['inizio']}):** {b_andata}"
                            
                        if "NONNI" in dati['chi_ritorno']:
                            txt_ritorno = f"👉 **Ritorno (ore {dati['fine']}):** {b_ritorno}\n*(📍 Riprendere da {attivita} e portare a {dest})*"
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
                    ("NONNI" not in imp['pomeriggio_leonardo']['chi_ritorno'] or imp['pomeriggio_leonardo'].get('dove_ritorno') == imp['pomeriggio_sara'].get('dove_ritorno'))
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

# --- PANNELLO GENITORI (PROTETTO DA PASSWORD) ---
with sch_genitori:
    if not st.session_state.genitori_unlocked:
        st.title("🔒 Area Riservata Genitori")
        st.info("Inserisci la password per modificare gli orari del Taxi.")
        pwd = st.text_input("Password", type="password")
        if st.button("SBLOCCA", type="primary"):
            if pwd == "0000":
                st.session_state.genitori_unlocked = True
                st.rerun()
            else:
                st.error("❌ Password errata!")
    else:
        c_lock1, c_lock2 = st.columns([3, 1])
        c_lock1.title("⚙️ Programmazione")
        if c_lock2.button("🔒 Blocca"):
            st.session_state.genitori_unlocked = False
            st.rerun()
        
        # 1. BOTTONI SETTIMANA
        cw1, cw2 = st.columns(2)
        if cw1.button("📅 QUESTA SETT.", use_container_width=True, type="primary" if st.session_state.week == "corrente" else "secondary"):
            st.session_state.week = "corrente"
            st.rerun()
        if cw2.button("⏭️ PROSSIMA SETT.", use_container_width=True, type="primary" if st.session_state.week == "prossima" else "secondary"):
            st.session_state.week = "prossima"
            st.rerun()
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 2. BARRA DEI GIORNI A PULSANTI
        sett_scelta = st.session_state.week
        giorni_dict = cal[sett_scelta]
        
        giorni_validi = [g for g, info in giorni_dict.items() if info["data_obj"] >= cal["oggi_obj"] or sett_scelta == "prossima"]
        if st.session_state.day not in giorni_validi and giorni_validi:
            st.session_state.day = giorni_validi[0]
            
        cdays = st.columns(5)
        for i, (nome_g, info) in enumerate(giorni_dict.items()):
            is_past = sett_scelta == "corrente" and info["data_obj"] < cal["oggi_obj"]
            b_type = "primary" if st.session_state.day == nome_g else "secondary"
            if cdays[i].button(nome_g[:3].upper(), disabled=is_past, use_container_width=True, type=b_type, key=f"btn_{sett_scelta}_{nome_g}"):
                st.session_state.day = nome_g
                st.rerun()

        giorno_sel = st.session_state.day

        st.markdown("---")

        # 3. PANNELLO INSERIMENTO DATI CON PULSANTI (RADIO)
        if not giorno_sel or (sett_scelta == "corrente" and not giorni_validi):
            st.warning("🎉 La settimana corrente è terminata! Clicca su PROSSIMA SETT. in alto.")
        else:
            k_id = f"{sett_scelta}_{giorno_sel}"
            dati_g = programma[sett_scelta][giorno_sel]
            
            st.subheader(f"Modifica: {giorno_sel.upper()}")
            
            # --- MATTINA ---
            with st.container(border=True):
                st.markdown("#### ☀️ MATTINA")
                chi_m = st.radio("Chi li porta a scuola?", OPZIONI_CHI, index=OPZIONI_CHI.index(dati_g["mattina"]["chi"]), horizontal=True, key=f"m_chi_{k_id}")
            
            # --- POMERIGGIO LEONARDO ---
            with st.container(border=True):
                st.markdown("#### 👦 POMERIGGIO LEONARDO")
                idx_cosa_l = OPZIONI_ATTIVITA_LEO.index(dati_g["pomeriggio_leonardo"]["cosa"]) if dati_g["pomeriggio_leonardo"]["cosa"] in OPZIONI_ATTIVITA_LEO else OPZIONI_ATTIVITA_LEO.index("Scuola 🏫")
                cos_l = st.radio("Attività Leonardo?", OPZIONI_ATTIVITA_LEO, index=idx_cosa_l, horizontal=True, key=f"l_cosa_{k_id}")
                
                opz_dest_l = ["Casa Nostra 🏠", "Casa Nonni 🏡", "Lavoro Mamma 💼"] if cos_l == "Scuola 🏫" else ["Casa Nostra 🏠", "Casa Nonni 🏡"]
                dest_attuale_l = dati_g["pomeriggio_leonardo"].get("dove_ritorno", "Casa Nostra 🏠")
                idx_dest_l = opz_dest_l.index(dest_attuale_l) if dest_attuale_l in opz_dest_l else 0

                if cos_l == "Scuola 🏫":
                    chi_and_l = OPZIONI_CHI[0]
                    chi_rit_l = st.radio("🚕 Chi lo riprende da scuola?", OPZIONI_CHI, index=OPZIONI_CHI.index(dati_g["pomeriggio_leonardo"]["chi_ritorno"]), horizontal=True, key=f"l_rit_{k_id}")
                    
                    if "NONNI" in chi_rit_l:
                        dove_rit_l = st.radio("📍 Dove portarlo?", opz_dest_l, index=idx_dest_l, horizontal=True, key=f"l_dest_{k_id}")
                    else:
                        dove_rit_l = "Casa Nostra 🏠"
                    
                    in_l, fi_l = "" , ""
                
                elif cos_l in ["Eufonio 🎺", "Yoga 🧘‍♂️"]:
                    chi_and_l = OPZIONI_CHI[0]
                    nome_att = cos_l.split()[0]
                    st.info(f"📍 Rimane a scuola, bisogna solo andarlo a riprendere da {nome_att}.")
                        
                    chi_rit_l = st.radio(f"🚕 Chi riprende Leonardo?", OPZIONI_CHI, index=OPZIONI_CHI.index(dati_g["pomeriggio_leonardo"].get("chi_ritorno", OPZIONI_CHI[0])), horizontal=True, key=f"l_rit_int_{k_id}")
                    
                    if "NONNI" in chi_rit_l:
                        dove_rit_l = st.radio("📍 Dove portarlo?", opz_dest_l, index=idx_dest_l, horizontal=True, key=f"l_dest_int_{k_id}")
                    else:
                        dove_rit_l = "Casa Nostra 🏠"
                        
                    in_l = ""
                    if cos_l == "Eufonio 🎺":
                        st.markdown("*L'orario di fine è fissato alle 18:00*")
                        fi_l = "18:00"
                    else:
                        fi_l = st.text_input("Orario Ritiro (es. 18:00)", dati_g["pomeriggio_leonardo"]["fine"], key=f"l_fi_int_{k_id}")
                    
                else:
                    chi_and_l = st.radio("🚕 Chi lo porta (Andata)?", OPZIONI_CHI, index=OPZIONI_CHI.index(dati_g["pomeriggio_leonardo"].get("chi_andata", OPZIONI_CHI[0])), horizontal=True, key=f"l_and_{k_id}")
                    chi_rit_l = st.radio(f"🚕 Chi lo riprende da {cos_l}?", OPZIONI_CHI, index=OPZIONI_CHI.index(dati_g["pomeriggio_leonardo"].get("chi_ritorno", OPZIONI_CHI[0])), horizontal=True, key=f"l_rit_est_{k_id}")
                    
                    if "NONNI" in chi_rit_l:
                        dove_rit_l = st.radio("📍 Al ritorno, dove va?", opz_dest_l, index=idx_dest_l, horizontal=True, key=f"l_dest_est_{k_id}")
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
            with st.container(border=True):
                if cos_l in ["Eufonio 🎺", "Yoga 🧘‍♂️"]:
                    st.markdown("#### 👧 POMERIGGIO SARA")
                    nome_attivita_leo = cos_l.split()[0]
                    st.warning(f"⚠️ Leonardo ha {nome_attivita_leo}, Sara esce da scuola alle **16:00**.")
                    sara_uguale = False
                    cos_s = "Scuola 🏫"
                    chi_and_s = OPZIONI_CHI[0]
                    
                    opz_dest_s = ["Casa Nostra 🏠", "Casa Nonni 🏡", "Lavoro Mamma 💼"]
                    dest_attuale_s = dati_g["pomeriggio_sara"].get("dove_ritorno", "Casa Nostra 🏠")
                    idx_dest_s = opz_dest_s.index(dest_attuale_s) if dest_attuale_s in opz_dest_s else 0
                    
                    chi_rit_s = st.radio("🚕 Chi riprende Sara da scuola?", OPZIONI_CHI, index=OPZIONI_CHI.index(dati_g["pomeriggio_sara"]["chi_ritorno"]), horizontal=True, key=f"s_rit_eu_{k_id}")
                    
                    if "NONNI" in chi_rit_s:
                        dove_rit_s = st.radio("📍 Dove portarla?", opz_dest_s, index=idx_dest_s, horizontal=True, key=f"s_dest_eu_{k_id}")
                    else:
                        dove_rit_s = "Casa Nostra 🏠"
                        
                    in_s, fi_s = "", "16:00"
                    
                elif cos_l not in OPZIONI_ATTIVITA_SARA:
                    st.markdown("#### 👧 POMERIGGIO SARA")
                    st.warning(f"⚠️ Leonardo fa {cos_l} (che Sara non fa), scegli l'attività per lei.")
                    sara_uguale = False
                    
                    idx_cosa_s = OPZIONI_ATTIVITA_SARA.index(dati_g["pomeriggio_sara"]["cosa"]) if dati_g["pomeriggio_sara"]["cosa"] in OPZIONI_ATTIVITA_SARA else OPZIONI_ATTIVITA_SARA.index("Scuola 🏫")
                    cos_s = st.radio("Attività Sara?", OPZIONI_ATTIVITA_SARA, index=idx_cosa_s, horizontal=True, key=f"s_cosa_{k_id}")
                    
                    opz_dest_s = ["Casa Nostra 🏠", "Casa Nonni 🏡", "Lavoro Mamma 💼"] if cos_s == "Scuola 🏫" else ["Casa Nostra 🏠", "Casa Nonni 🏡"]
                    dest_attuale_s = dati_g["pomeriggio_sara"].get("dove_ritorno", "Casa Nostra 🏠")
                    idx_dest_s = opz_dest_s.index(dest_attuale_s) if dest_attuale_s in opz_dest_s else 0

                    if cos_s == "Scuola 🏫":
                        chi_and_s = OPZIONI_CHI[0]
                        chi_rit_s = st.radio("🚕 Chi la riprende da scuola?", OPZIONI_CHI, index=OPZIONI_CHI.index(dati_g["pomeriggio_sara"]["chi_ritorno"]), horizontal=True, key=f"s_rit_{k_id}")
                        
                        if "NONNI" in chi_rit_s:
                            dove_rit_s = st.radio("📍 Dove portarla?", opz_dest_s, index=idx_dest_s, horizontal=True, key=f"s_dest_{k_id}")
                        else:
                            dove_rit_s = "Casa Nostra 🏠"
                        in_s, fi_s = "", ""
                    else:
                        chi_and_s = st.radio("🚕 Chi la porta (Andata)?", OPZIONI_CHI, index=OPZIONI_CHI.index(dati_g["pomeriggio_sara"].get("chi_andata", OPZIONI_CHI[0])), horizontal=True, key=f"s_and_{k_id}")
                        chi_rit_s = st.radio(f"🚕 Chi la riprende da {cos_s}?", OPZIONI_CHI, index=OPZIONI_CHI.index(dati_g["pomeriggio_sara"].get("chi_ritorno", OPZIONI_CHI[0])), horizontal=True, key=f"s_rit_est_{k_id}")
                        
                        if "NONNI" in chi_rit_s:
                            dove_rit_s = st.radio("📍 Al ritorno, dove va?", opz_dest_s, index=idx_dest_s, horizontal=True, key=f"s_dest_est_{k_id}")
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
                    sara_uguale = st.toggle("✅ Sara fa lo stesso di Leonardo", value=dati_g.get("sara_uguale", True), key=f"s_uguale_{k_id}")
                    st.markdown("#### 👧 POMERIGGIO SARA")
                    
                    if not sara_uguale:
                        idx_cosa_s = OPZIONI_ATTIVITA_SARA.index(dati_g["pomeriggio_sara"]["cosa"]) if dati_g["pomeriggio_sara"]["cosa"] in OPZIONI_ATTIVITA_SARA else OPZIONI_ATTIVITA_SARA.index("Scuola 🏫")
                        cos_s = st.radio("Attività Sara?", OPZIONI_ATTIVITA_SARA, index=idx_cosa_s, horizontal=True, key=f"s_cosa_alt_{k_id}")
                        
                        opz_dest_s = ["Casa Nostra 🏠", "Casa Nonni 🏡", "Lavoro Mamma 💼"] if cos_s == "Scuola 🏫" else ["Casa Nostra 🏠", "Casa Nonni 🏡"]
                        dest_attuale_s = dati_g["pomeriggio_sara"].get("dove_ritorno", "Casa Nostra 🏠")
                        idx_dest_s = opz_dest_s.index(dest_attuale_s) if dest_attuale_s in opz_dest_s else 0

                        if cos_s == "Scuola 🏫":
                            chi_and_s = OPZIONI_CHI[0]
                            chi_rit_s = st.radio("🚕 Chi la riprende da scuola?", OPZIONI_CHI, index=OPZIONI_CHI.index(dati_g["pomeriggio_sara"]["chi_ritorno"]), horizontal=True, key=f"s_rit_alt_{k_id}")
                            
                            if "NONNI" in chi_rit_s:
                                dove_rit_s = st.radio("📍 Dove portarla?", opz_dest_s, index=idx_dest_s, horizontal=True, key=f"s_dest_alt_{k_id}")
                            else:
                                dove_rit_s = "Casa Nostra 🏠"
                            in_s, fi_s = "", ""
                        else:
                            chi_and_s = st.radio("🚕 Chi la porta (Andata)?", OPZIONI_CHI, index=OPZIONI_CHI.index(dati_g["pomeriggio_sara"].get("chi_andata", OPZIONI_CHI[0])), horizontal=True, key=f"s_and_alt_{k_id}")
                            chi_rit_s = st.radio(f"🚕 Chi la riprende da {cos_s}?", OPZIONI_CHI, index=OPZIONI_CHI.index(dati_g["pomeriggio_sara"].get("chi_ritorno", OPZIONI_CHI[0])), horizontal=True, key=f"s_rit_est_alt_{k_id}")
                            
                            if "NONNI" in chi_rit_s:
                                dove_rit_s = st.radio("📍 Al ritorno, dove va?", opz_dest_s, index=idx_dest_s, horizontal=True, key=f"s_dest_est_alt_{k_id}")
                            else:
                                dove_rit_s = "Casa Nostra 🏠"

                            if cos_s == "Ginnastica Artistica 🤸‍♀️":
                                st.info("⏱️ Orari prefissati Sara: **16:30 - 17:30**")
                                in_s, fi_s = "16:30", "17:30"
                            else:
                                c_in_s, c_fi_s = st.columns(2)
                                in_s = c_in_s.text_input("Orario Inizio (S)", dati_g["pomeriggio_sara"]["inizio"], key=f"s_in_alt_{k_id}")
                                fi_s = c_fi_s.text_input("Orario Fine (S)", dati_g["pomeriggio_sara"]["fine"], key=f"s_fi_alt_{k_id}")
                    else:
                        st.success("✅ Segue gli orari di Leonardo.")
                        chi_and_s, chi_rit_s, cos_s, dove_rit_s = chi_and_l, chi_rit_l, cos_l, dove_rit_l
                        if cos_s == "Ginnastica Artistica 🤸‍♀️":
                            in_s, fi_s = "16:30", "17:30"
                        elif cos_s == "Scuola 🏫":
                            in_s, fi_s = "", ""
                        else:
                            in_s, fi_s = in_l, fi_l

            # PULSANTONE DI SALVATAGGIO
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("💾 SALVA PROGRAMMA", type="primary", use_container_width=True):
                programma[sett_scelta][giorno_sel] = {
                    "mattina": {"chi": chi_m, "cosa": "Scuola 🏫"},
                    "pomeriggio_leonardo": {"chi_andata": chi_and_l, "chi_ritorno": chi_rit_l, "cosa": cos_l, "inizio": in_l, "fine": fi_l, "dove_ritorno": dove_rit_l},
                    "sara_uguale": sara_uguale,
                    "pomeriggio_sara": {"chi_andata": chi_and_s, "chi_ritorno": chi_rit_s, "cosa": cos_s, "inizio": in_s, "fine": fi_s, "dove_ritorno": dove_rit_s}
                }
                salvato = salva_programma(programma)
                if salvato:
                    st.success(f"☁️ Salvato in Cloud: Programma di {giorno_sel.upper()} aggiornato!")
                else:
                    st.warning(f"⚠️ Salvato in Locale (Configura JSONBIN per salvare sul Cloud).")
                st.rerun()
