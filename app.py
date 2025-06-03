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

st.title("🇮🇹 Apprentissage interactif de l'italien")

menu = st.sidebar.radio("📚 Menu", ["Ajouter", "Réviser"])

# --- AJOUTER UNE PHRASE ---
if menu == "Ajouter":
    st.header("Ajouter une nouvelle expression")
    fr = st.text_input("🇫🇷 Français")
    it = st.text_input("🇮🇹 Italien")
    if st.button("Ajouter"):
        if fr and it:
            c.execute("INSERT INTO vocab (francais, italien) VALUES (?, ?)", (fr, it))
            conn.commit()
            st.success("Phrase ajoutée avec succès.")
        else:
            st.warning("Remplis les deux champs.")

# --- RÉVISION ---
elif menu == "Réviser":
    st.header("Révision")
    c.execute("SELECT * FROM vocab")
    data = c.fetchall()

    if not data:
        st.info("Aucune phrase enregistrée.")
    else:
        # Nouvelle question si pas encore stockée
        if "question" not in st.session_state:
            st.session_state.question = random.choice(data)
            st.session_state.input_key = random.randint(0, 1000000)  # clé dynamique pour vider le champ

        question = st.session_state.question
        st.subheader(f"Traduire : **{question[1]}**")

        reponse = st.text_input("Ta réponse en italien", key=st.session_state.input_key).strip().lower()

        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Vérifier"):
                correct = question[2].strip().lower()
                if reponse == correct:
                    st.success("✔️ Bonne réponse !")
                else:
                    st.error(f"❌ Incorrect. Réponse correcte : {correct}")

        with col2:
            if st.button("Nouvelle question"):
                st.session_state.question = random.choice(data)
                st.session_state.input_key = random.randint(0, 1000000)  # nouvelle clé = champ vidé
                st.rerun()
