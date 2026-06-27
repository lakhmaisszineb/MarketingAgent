import streamlit as st
import pandas as pd
from edgenia.agents.main_agent import EdgeniaAgent

st.set_page_config(page_title="Edgenia AI Growth Agent", layout="wide")
st.title("Edgenia - Autonomous AI Growth Agent")

# Sidebar
st.sidebar.header("Navigation")
page = st.sidebar.selectbox("Aller à", ["Onboarding", "Import Données", "Tableau de bord", "Générer Campagne"])

agent = EdgeniaAgent(company_id="demo_company")

if page == "Onboarding":
    st.header("Onboarding Entreprise")
    with st.form("onboarding_form"):
        company_name = st.text_input("Nom de l'entreprise")
        sector = st.selectbox("Secteur", ["Mode & Vêtements", "Beauté", "Alimentation", "Électronique", "Autre"])
        objectives = st.multiselect("Objectifs principaux", ["Augmenter les ventes", "Fidéliser clients", "Acquérir nouveaux clients"])
        channels = st.multiselect("Canaux", ["Email", "Instagram", "Facebook", "WhatsApp"])
        submitted = st.form_submit_button("Commencer Onboarding")
        
        if submitted:
            responses = {
                "1": company_name,
                "2": sector,
                "3": objectives,
                "4": channels,
                "5": "Non spécifié",
                "6": "Non spécifié"
            }
            st.success("Onboarding terminé !")
            st.session_state.company_profile = responses

elif page == "Import Données":
    st.header("Import des données clients")
    uploaded_file = st.file_uploader("Choisir un fichier CSV ou Excel", type=["csv", "xlsx"])
    
    if uploaded_file and st.button("Analyser le fichier"):
        # Simulation (dans la vraie version on appellera le manager)
        st.success("Fichier analysé avec succès !")
        st.info("Colonnes détectées et mapping effectué.")

elif page == "Tableau de bord":
    st.header("Tableau de bord de l'agent")
    st.write("Observation et analyse en cours...")
    if st.button("Lancer Analyse Complète"):
        st.success("Analyse terminée. Voir le rapport ci-dessous.")

elif page == "Générer Campagne":
    st.header("Générer une campagne")
    action = st.text_input("Quelle action voulez-vous lancer ?")
    if st.button("Générer"):
        st.subheader("Email généré")
        st.text_area("Contenu", "Bonjour...\n\nVoici une offre spéciale...", height=300)

st.sidebar.info("Edgenia v1.0 - Prototype")