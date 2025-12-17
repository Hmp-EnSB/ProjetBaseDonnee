import streamlit as st

def render_sidebar():
    """
    Renders a unified, fancy sidebar for the application.
    """
    with st.sidebar:
        st.header("🌍 Agence de Voyage")
        st.caption("Système de Gestion")
        st.divider()
        
        st.markdown("### 🧭 Navigation")
        
        # Using st.page_link for a native, unified look with automatic active state highlighting
        st.page_link("Accueil.py", label="Accueil", icon="🏠")
        st.page_link("pages/Agence.py", label="Agences de Voyage", icon="✈️")
        st.page_link("pages/Reservation.py", label="Reservations", icon="📊")
        st.page_link("pages/Chambre.py", label="Chambres" , icon="🛏️")
        
        st.divider()
        
        # About Section
        st.markdown("### ℹ️ À propos")
        st.info(
            "Système complet pour la gestion des agences de voyages et des réservations d'hôtels."
        )
        
        # Dashboard Details
        with st.expander("🛠️ Technologies", expanded=False):
            st.markdown("• **Python**")
            st.markdown("• **Streamlit**")
            st.markdown("• **MySQL**")
            st.markdown("• **Pandas**")

            
        st.divider()
