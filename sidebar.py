import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.header("Agence de Voyage")
        st.caption("Systeme de Gestion")
        st.divider()
        
        st.markdown("### Navigation")
        st.page_link("Accueil.py", label="Accueil")
        st.page_link("pages/Agence.py", label="Agences de Voyage")
        st.page_link("pages/Reservation.py", label="Reservations")
        st.page_link("pages/Chambre.py", label="Chambres")
        
        st.divider()

        if 'global_lang' not in st.session_state:
            st.session_state['global_lang'] = "FR"

        options = ["FR", "ENG", "AR"]
        current_idx = options.index(st.session_state['global_lang'])

        selected = st.selectbox(
            "Language / Langue / اللغة",
            options=options,
            index=current_idx,
            key="lang_selector"
        )
        
        st.session_state['global_lang'] = selected
        
        st.divider()
        return st.session_state['global_lang']