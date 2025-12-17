from db import get_connection
import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Agences de Voyage",
    layout="wide",
    initial_sidebar_state="expanded"
)

from sidebar import render_sidebar
render_sidebar()

st.markdown("""
    <style>
        /* This additional css code is to hide the navigation menu */
        [data-testid="stSidebarNav"] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("# ✈️ AGENCES DE VOYAGE")
st.markdown("## 🌍 Votre prochain voyage vous attend")
st.caption("Explorez notre réseau d'agences à travers le monde")
st.divider()

# --- DATABASE CONNECTION ---
connection = get_connection()

# --- KEY METRICS ---
st.markdown("### 📊 Indicateurs clés")

nbr_agences = pd.read_sql(
    "SELECT COUNT(*) AS total FROM TRAVEL_AGENCY",
    connection
).iloc[0, 0]

nbr_villes = pd.read_sql(
    "SELECT COUNT(DISTINCT City_Address) FROM TRAVEL_AGENCY",
    connection
).iloc[0, 0]

ville_max_agences = pd.read_sql(
    """
    SELECT City_Address
    FROM TRAVEL_AGENCY
    GROUP BY City_Address
    ORDER BY COUNT(*) DESC
    LIMIT 1
    """,
    connection
).iloc[0, 0]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🏢 Nombre d'agences", nbr_agences)
    st.caption("Agences partenaires actives")

with col2:
    st.metric("🌆 Villes desservies", nbr_villes)
    st.caption("Destinations disponibles")

with col3:
    st.metric("⭐ Ville leader", ville_max_agences)
    st.caption("Hub principal")

st.divider()

# --- DISTRIBUTION CHART ---
st.markdown("### 📈 Répartition des agences par ville")

df_distribution = pd.read_sql(
    """
    SELECT City_Address, COUNT(*) AS nombre_agences
    FROM TRAVEL_AGENCY
    GROUP BY City_Address
    ORDER BY nombre_agences DESC
    LIMIT 10
    """,
    connection
)

if not df_distribution.empty:
    st.bar_chart(
        df_distribution.set_index("City_Address")["nombre_agences"],
        height=400,
        use_container_width=True
    )
    st.caption("📊 Top 10 des villes avec le plus d'agences")

st.divider()

# --- MAP ---
st.markdown("### 🗺️ Localisation des agences")

tab1, tab2 = st.tabs(["📍 Carte interactive", "📊 Données géographiques"])

with tab1:
    df_map = pd.read_sql(
        """
        SELECT c.Latitude AS lat,
               c.Longitude AS lon,
               c.Name AS City
        FROM CITY c
        JOIN TRAVEL_AGENCY a
          ON c.Name = a.City_Address
        """,
        connection
    )
    st.map(df_map, size=20)
    st.caption(f"🌍 {len(df_map)} emplacements affichés")

with tab2:
    st.dataframe(
        df_map.groupby("City").size().reset_index(name="Nombre d'agences"),
        use_container_width=True,
        hide_index=True
    )

st.divider()

# --- SEARCH ---
st.markdown("### 🔎 Recherche d'agences")

with st.expander("🔍 Recherche avancée par ville", expanded=True):
    ville_recherchee = st.text_input(
        "Nom de la ville",
        placeholder="Ex : Ville1, Ville2"
    )

    search_button = st.button("🔍 Rechercher", type="primary", use_container_width=True)

    if ville_recherchee:
        sql = """
        SELECT CodA,
               WebSite,
               Tel,
               CONCAT(
                   Num_Address, ' ',
                   Street_Address, ', ',
                   City_Address, ', ',
                   Country_Address, ' ',
                   ZIP_Address
               ) AS Adresse
        FROM TRAVEL_AGENCY
        WHERE City_Address LIKE %s
        """
        df_ville = pd.read_sql(sql, connection, params=[f"%{ville_recherchee}%"])

        if df_ville.empty:
            st.warning("⚠️ Aucune agence trouvée dans cette ville.")
        else:
            st.success(f"✅ {len(df_ville)} agence(s) trouvée(s)")
            st.dataframe(
                df_ville,
                use_container_width=True,
                column_config={
                    "CodA": "🏷️ Code",
                    "Adresse": "📍 Adresse complète",
                    "Tel": "📞 Téléphone",
                    "WebSite": st.column_config.LinkColumn("🌐 Site web")
                },
                hide_index=True
            )
    else:
        st.info("💡 Entrez le nom d'une ville pour rechercher des agences.")

st.divider()

# --- FULL TABLE ---
st.markdown("### 📋 Catalogue complet des agences")

df_agences = pd.read_sql(
    """
    SELECT CodA,
           WebSite,
           Tel,
           CONCAT(
               Num_Address, ' ',
               Street_Address, ', ',
               City_Address, ', ',
               Country_Address, ' ',
               ZIP_Address
           ) AS Adresse
    FROM TRAVEL_AGENCY
    """,
    connection
)

col_info, col_download = st.columns([3, 1])

with col_info:
    st.caption(f"📊 Total : {len(df_agences)} agences")

with col_download:
    csv = df_agences.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Télécharger (CSV)",
        csv,
        "agences_voyage.csv",
        "text/csv",
        use_container_width=True
    )

st.dataframe(
    df_agences,
    use_container_width=True,
    height=400,
    column_config={
        "CodA": "🏷️ Code",
        "Adresse": "📍 Adresse complète",
        "Tel": "📞 Contact",
        "WebSite": st.column_config.LinkColumn("🌐 Site web")
    },
    hide_index=True
)

st.divider()

connection.close()