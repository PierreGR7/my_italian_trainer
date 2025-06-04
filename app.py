import streamlit as st

st.set_page_config(page_title="Trainer Italien", layout="centered")

import sqlite3
import random

# Connexion à la base de données
conn = sqlite3.connect('db.sqlite', check_same_thread=False)
c = conn.cursor()

# Création de la table si elle n'existe pas
c.execute('''
CREATE TABLE IF NOT EXISTS vocab (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    francais TEXT NOT NULL,
    italien TEXT NOT NULL
)
''')
conn.commit()

# CSS pour style amélioré
st.markdown("""
    <style>
    .main { background-color: #f7f7f7; }
    .stButton > button {
        background-color: #009999;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5em 1em;
    }
    .stTextInput > div > input {
        border: 2px solid #009999;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Apprentissage interactif de l'italien")

menu = st.sidebar.radio("📚 Menu", ["Ajouter", "Réviser"])

# --- AJOUTER UNE PHRASE ---
from deep_translator import GoogleTranslator

if menu == "Ajouter":
    st.header("Ajouter une phrase ou un mot (en italien)")
    it = st.text_input("Mot ou phrase en italien")

    if st.button("Traduire et ajouter"):
        if it:
            try:
                fr = GoogleTranslator(source='it', target='fr').translate(it)
                c.execute("INSERT INTO vocab (francais, italien) VALUES (?, ?)", (fr, it))
                conn.commit()
                st.success(f"Ajouté : '{it}' → '{fr}'")
            except Exception as e:
                st.error(f"Erreur de traduction : {e}")
        else:
            st.warning("Saisis une phrase ou un mot en italien.")


# --- REVISION ---
elif menu == "Réviser":
    st.header("Révision")
    c.execute("SELECT * FROM vocab")
    data = c.fetchall()

    if not data:
        st.info("Aucune phrase enregistrée.")
    else:
        # Initialisation
        if "mots_ok" not in st.session_state:
            st.session_state.mots_ok = []

        # Filtrer les mots déjà réussis
        mots_restants = [row for row in data if row[0] not in st.session_state.mots_ok]

        if not mots_restants:
            st.success("Tu as répondu correctement à tous les mots pour cette session !")
        else:
            # Initialisation de la question si besoin
            if "question" not in st.session_state or st.session_state.question is None or st.session_state.question[0] in st.session_state.mots_ok:
                st.session_state.question = random.choice(mots_restants)
                st.session_state.input_key = random.randint(0, 1000000)

            question = st.session_state.question
            st.subheader(f"Traduire : **{question[1]}**")  # Français

            reponse = st.text_input("Ta réponse en italien", key=st.session_state.input_key).strip().lower()

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Vérifier"):
                    correct = question[2].strip().lower()
                    if reponse == correct:
                        st.success("Bonne réponse !")
                        st.session_state.mots_ok.append(question[0])
                        st.session_state.bonne_reponse = True
                    else:
                        st.error(f"Incorrect. Réponse correcte : {correct}")
                        st.session_state.bonne_reponse = False


            with col2:
                if st.button("Nouvelle question"):
                    st.session_state.question = None
                    st.session_state.input_key = random.randint(0, 1000000)
                    st.session_state.bonne_reponse = False
                    st.rerun()


