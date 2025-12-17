import streamlit as st
import pandas as pd
from db import get_connection
from sidebar import render_sidebar

st.set_page_config(
    page_title="Agences de Voyage",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

lang_choice = render_sidebar()

LANGS = {
    "ENG": {
        "main_title": "TRAVEL AGENCIES",
        "subtitle": "Your next trip awaits",
        "caption_main": "Explore our network of agencies worldwide",
        "metrics_title": "Key Metrics",
        "metric_agencies": "Number of agencies",
        "metric_agencies_cap": "Active partner agencies",
        "metric_cities": "Cities served",
        "metric_cities_cap": "Available destinations",
        "metric_leader": "Leader city",
        "metric_leader_cap": "Main hub",
        "chart_title": "Agency distribution by city",
        "chart_cap": "Top 10 cities with the most agencies",
        "map_title": "Agency locations",
        "tab_map": "Interactive map",
        "tab_data": "Geographic data",
        "map_cap": "locations displayed",
        "search_title": "Search agencies",
        "search_expander": "Advanced search by city",
        "search_label": "City name",
        "search_placeholder": "Ex: City1, City2",
        "search_btn": "Search",
        "search_none": "No agencies found in this city.",
        "search_success": "agency(s) found",
        "search_info": "Enter a city name to search for agencies.",
        "table_title": "Full agency catalog",
        "table_total": "Total",
        "table_download": "Download (CSV)",
        "col_code": "Code",
        "col_address": "Full Address",
        "col_contact": "Contact",
        "col_web": "Website"
    },
    "FR": {
        "main_title": "AGENCES DE VOYAGE",
        "subtitle": "Votre prochain voyage vous attend",
        "caption_main": "Explorez notre réseau d'agences à travers le monde",
        "metrics_title": "Indicateurs clés",
        "metric_agencies": "Nombre d'agences",
        "metric_agencies_cap": "Agences partenaires actives",
        "metric_cities": "Villes desservies",
        "metric_cities_cap": "Destinations disponibles",
        "metric_leader": "Ville leader",
        "metric_leader_cap": "Hub principal",
        "chart_title": "Répartition des agences par ville",
        "chart_cap": "Top 10 des villes avec le plus d'agences",
        "map_title": "Localisation des agences",
        "tab_map": "Carte interactive",
        "tab_data": "Données géographiques",
        "map_cap": "emplacements affichés",
        "search_title": "Recherche d'agences",
        "search_expander": "Recherche avancée par ville",
        "search_label": "Nom de la ville",
        "search_placeholder": "Ex : Ville1, Ville2",
        "search_btn": "Rechercher",
        "search_none": "Aucune agence trouvée dans cette ville.",
        "search_success": "agence(s) trouvée(s)",
        "search_info": "Entrez le nom d'une ville pour rechercher des agences.",
        "table_title": "Catalogue complet des agences",
        "table_total": "Total",
        "table_download": "Télécharger (CSV)",
        "col_code": "Code",
        "col_address": "Adresse complète",
        "col_contact": "Contact",
        "col_web": "Site web"
    },
    "AR": {
        "main_title": "وكالات السفر",
        "subtitle": "رحلتك القادمة في انتظارك",
        "caption_main": "استكشف شبكة وكالاتنا حول العالم",
        "metrics_title": "المؤشرات الرئيسية",
        "metric_agencies": "عدد الوكالات",
        "metric_agencies_cap": "وكالات شريكة نشطة",
        "metric_cities": "المدن المخدومة",
        "metric_cities_cap": "الوجهات المتاحة",
        "metric_leader": "المدينة الرائدة",
        "metric_leader_cap": "المركز الرئيسي",
        "chart_title": "توزيع الوكالات حسب المدينة",
        "chart_cap": "أفضل 10 مدن من حيث عدد الوكالات",
        "map_title": "مواقع الوكالات",
        "tab_map": "خريطة تفاعلية",
        "tab_data": "البيانات الجغرافية",
        "map_cap": "مواقع معروضة",
        "search_title": "البحث عن الوكالات",
        "search_expander": "بحث متقدم حسب المدينة",
        "search_label": "اسم المدينة",
        "search_placeholder": "مثال: مدينة 1، مدينة 2",
        "search_btn": "بحث",
        "search_none": "لم يتم العثور على وكالات في هذه المدينة.",
        "search_success": "وكالات تم العثور عليها",
        "search_info": "أدخل اسم المدينة للبحث عن الوكالات.",
        "table_title": "دليل الوكالات الكامل",
        "table_total": "المجموع",
        "table_download": "تحميل (CSV)",
        "col_code": "الرمز",
        "col_address": "العنوان الكامل",
        "col_contact": "الاتصال",
        "col_web": "الموقع الإلكتروني"
    }
}

T = LANGS[lang_choice]

st.markdown(f"# {T['main_title']}")
st.markdown(f"## {T['subtitle']}")
st.caption(T['caption_main'])
st.divider()

connection = get_connection()

st.markdown(f"### {T['metrics_title']}")

nbr_agences = pd.read_sql("SELECT COUNT(*) AS total FROM TRAVEL_AGENCY", connection).iloc[0, 0]
nbr_villes = pd.read_sql("SELECT COUNT(DISTINCT City_Address) FROM TRAVEL_AGENCY", connection).iloc[0, 0]
ville_max_agences = pd.read_sql("SELECT City_Address FROM TRAVEL_AGENCY GROUP BY City_Address ORDER BY COUNT(*) DESC LIMIT 1", connection).iloc[0, 0]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(T['metric_agencies'], nbr_agences)
    st.caption(T['metric_agencies_cap'])

with col2:
    st.metric(T['metric_cities'], nbr_villes)
    st.caption(T['metric_cities_cap'])

with col3:
    st.metric(T['metric_leader'], ville_max_agences)
    st.caption(T['metric_leader_cap'])

st.divider()

st.markdown(f"### {T['chart_title']}")
df_distribution = pd.read_sql("SELECT City_Address, COUNT(*) AS nombre_agences FROM TRAVEL_AGENCY GROUP BY City_Address ORDER BY nombre_agences DESC LIMIT 10", connection)

if not df_distribution.empty:
    st.bar_chart(df_distribution.set_index("City_Address")["nombre_agences"], height=400, use_container_width=True)
    st.caption(T['chart_cap'])

st.divider()

st.markdown(f"### {T['map_title']}")
tab1, tab2 = st.tabs([T['tab_map'], T['tab_data']])

with tab1:
    df_map = pd.read_sql("SELECT c.Latitude AS lat, c.Longitude AS lon, c.Name AS City FROM CITY c JOIN TRAVEL_AGENCY a ON c.Name = a.City_Address", connection)
    st.map(df_map, size=20)
    st.caption(f"{len(df_map)} {T['map_cap']}")

with tab2:
    st.dataframe(df_map.groupby("City").size().reset_index(name=T['metric_agencies']), use_container_width=True, hide_index=True)

st.divider()

st.markdown(f"### {T['search_title']}")
with st.expander(T['search_expander'], expanded=True):
    ville_recherchee = st.text_input(T['search_label'], placeholder=T['search_placeholder'])
    search_button = st.button(T['search_btn'], type="primary", use_container_width=True)

    if ville_recherchee:
        sql = "SELECT CodA, WebSite, Tel, CONCAT(Num_Address, ' ', Street_Address, ', ', City_Address, ', ', Country_Address, ' ', ZIP_Address) AS Adresse FROM TRAVEL_AGENCY WHERE City_Address LIKE %s"
        df_ville = pd.read_sql(sql, connection, params=[f"%{ville_recherchee}%"])

        if df_ville.empty:
            st.warning(T['search_none'])
        else:
            st.success(f"{len(df_ville)} {T['search_success']}")
            st.dataframe(
                df_ville,
                use_container_width=True,
                column_config={
                    "CodA": T['col_code'],
                    "Adresse": T['col_address'],
                    "Tel": T['col_contact'],
                    "WebSite": st.column_config.LinkColumn(T['col_web'])
                },
                hide_index=True
            )
    else:
        st.info(T['search_info'])

st.divider()

st.markdown(f"### {T['table_title']}")
df_agences = pd.read_sql("SELECT CodA, WebSite, Tel, CONCAT(Num_Address, ' ', Street_Address, ', ', City_Address, ', ', Country_Address, ' ', ZIP_Address) AS Adresse FROM TRAVEL_AGENCY", connection)

col_info, col_download = st.columns([3, 1])
with col_info:
    st.caption(f"{T['table_total']} : {len(df_agences)}")

with col_download:
    csv = df_agences.to_csv(index=False).encode("utf-8")
    st.download_button(T['table_download'], csv, "agences_voyage.csv", "text/csv", use_container_width=True)

st.dataframe(
    df_agences,
    use_container_width=True,
    height=400,
    column_config={
        "CodA": T['col_code'],
        "Adresse": T['col_address'],
        "Tel": T['col_contact'],
        "WebSite": st.column_config.LinkColumn(T['col_web'])
    },
    hide_index=True
)

st.divider()
connection.close()