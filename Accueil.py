import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Accueil - Projet Agences de Voyage", 
    layout="wide",
    initial_sidebar_state="expanded"
)

from sidebar import render_sidebar

# --- SIDEBAR ---
render_sidebar()

st.markdown("""
    <style>
        /* This additional css code is to hide the navigation menu */
        [data-testid="stSidebarNav"] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

# --- HERO SECTION ---
st.markdown("# 🌍 Projet Base de Données")
st.markdown("## Système de Gestion des Agences de Voyage")
st.caption("Application de gestion et visualisation des données")
st.divider()

# --- PROJECT INFORMATION ---
st.markdown("### 📋 Informations Générales")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🎓 Établissement")
    st.info("**Université/École :** Votre Université")
    
    st.markdown("#### 📚 Cours")
    st.info("**Matière :** Base de Données Relationnelles")
    
    st.markdown("#### 📅 Année Académique")
    st.info("**Période :** 2024-2025")

with col2:
    st.markdown("#### 🎯 Objectifs du Projet")
    st.success("""
    - Conception d'une base de données relationnelle
    - Implémentation avec MySQL
    - Développement d'une interface utilisateur
    - Analyse et visualisation des données
    """)

st.divider()

# --- TEAM SECTION ---
st.markdown("### 👥 Équipe du Projet")
st.caption("Les étudiants qui ont contribué à ce projet")

# Create 7 student cards in rows
row1_cols = st.columns(4)
row2_cols = st.columns(3)

students = [
    {"name": "Bouali Younes", "role": "Git & Page agence"},
    {"name": "Étudiant 2", "role": "Développeur Backend"},
    {"name": "Étudiant 3", "role": "Développeur Frontend"},
    {"name": "Étudiant 4", "role": "Designer UI/UX"},
    {"name": "Étudiant 5", "role": "Analyste de données"},
    {"name": "Étudiant 6", "role": "Testeur QA"},
    {"name": "Étudiant 7", "role": "Documentaliste"}
]

# Display first 4 students
for i, col in enumerate(row1_cols):
    with col:
        st.markdown(f"#### 👤 {students[i]['name']}")
        st.caption(f"📌 {students[i]['role']}")

st.markdown("")

# Display last 3 students
for i, col in enumerate(row2_cols):
    with col:
        st.markdown(f"#### 👤 {students[i+4]['name']}")
        st.caption(f"📌 {students[i+4]['role']}")

st.divider()

# --- PROJECT FEATURES ---
st.markdown("### ⚡ Fonctionnalités de l'Application")

feature_col1, feature_col2, feature_col3 = st.columns(3)

with feature_col1:
    st.markdown("#### 🏢 Gestion des Agences")
    st.write("""
    - Liste complète des agences
    - Recherche par ville
    - Visualisation sur carte
    - Export des données
    """)

with feature_col2:
    st.markdown("#### 📊 Statistiques")
    st.write("""
    - Indicateurs clés
    - Graphiques interactifs
    - Analyse géographique
    - Rapports détaillés
    """)

with feature_col3:
    st.markdown("#### 🔍 Recherche Avancée")
    st.write("""
    - Filtres multiples
    - Résultats en temps réel
    - Interface intuitive
    - Navigation fluide
    """)

st.divider()

# --- TECHNOLOGIES USED ---
st.markdown("### 🛠️ Technologies Utilisées")

tech_col1, tech_col2, tech_col3, tech_col4 = st.columns(4)

with tech_col1:
    st.metric(label="💾 Base de Données", value="MySQL")

with tech_col2:
    st.metric(label="🐍 Backend", value="Python")

with tech_col3:
    st.metric(label="🎨 Frontend", value="Streamlit")

with tech_col4:
    st.metric(label="📈 Visualisation", value="Pandas")

st.divider()

# --- FOOTER ---
st.markdown("---")