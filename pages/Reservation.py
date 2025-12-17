import streamlit as st
import pandas as pd
import datetime as dt
from datetime import date
from db import get_connection


# --- Charger les données depuis MySQL ---
try:
    conn = get_connection()
    cursor = conn.cursor()
    df = pd.read_sql("SELECT * FROM BOOKING", conn)  # suppose que la table a les colonnes suivantes : date, code, et autres infos
except Exception as e:
    st.error(f"Error while loading data : {e}")
    st.stop()


# --- 0. Configuration de la page Streamlit ---
st.set_page_config(
    page_title="Hotel Reservation management project",
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

# Nettoyage et préparation des données
df['StartDate'] = pd.to_datetime(df['StartDate'])
df['EndDate'] = pd.to_datetime(df['EndDate'])

# Calcul des métriques
df['duration'] = (df['EndDate'] - df['StartDate']).dt.days
df['total_cost'] = df['Cost'] * df['duration']
df['month_year'] = df['StartDate'].dt.to_period('M')


# --- 2. En-tête et Personnalisation ---

st.title("Welcome to our Hotel Booking Dashboard")
st.markdown("""
 This interactive dashboard provides an overview of performance and cost trends.
Use the filters to explore hotel booking statistics.
""")

st.divider()

# --- 3. Indicateurs Clés de Performance (KPIs) ---

st.header("📊 OVERALL PERFORMANCE")


# Utilisation de colonnes pour une mise en page claire
col1, col2, col3, col4 = st.columns(4)
total_revenue = df['total_cost'].sum()
average_daily_price = df['Cost'].mean()
total_occupied_days = df['duration'].sum()
total_reservations = len(df)
with col1:
    st.metric("Total Réservations", f"*{total_reservations:,.0f}*")
with col2:
    st.metric("Total Revenue", f"*{total_revenue:,.0f} €*")
with col3:
    st.metric("Average Daily Price", f"*{average_daily_price:,.2f} €*")
with col4:
    st.metric("ToTal Occupied Days", f"*{total_occupied_days:,.0f} jours*")

st.markdown("---")


# --- 4. Analyse Détaillée (Utilisation des Onglets) ---
st.header("🔍 Trend Analysis & Reservations Management")
tab_graph, tab_top_rooms,tab_reserv = st.tabs(["📉 Cost Evolution ", "🛏️ Most expensive rooms by month","🏨Book Your Stay"])

# ---------------- Prix par type ----------------
with tab_reserv:
  st.title("🏨 Your Next trip starts here, Book Your Next Stay Easily in a Few Clicks")
  price_per_night = {
        "Single": 100,
        "Double": 150,
        "suite": 300
    }

    # ---------------- Agences ----------------
  cursor.execute("SELECT CodA FROM TRAVEL_AGENCY")
  agencies = [row[0] for row in cursor.fetchall()]

    # ---------------- Interface ----------------
  agency = st.selectbox("Travel Agency", agencies)

  room_type = st.selectbox(
        "Room Type",
        list(price_per_night.keys())
    )

    # Chambres correspondant au type
  cursor.execute("""
        SELECT CodR
        FROM ROOM
        WHERE Type= %s
    """, (room_type,))
  rooms = [row[0] for row in cursor.fetchall()]

  room = st.selectbox("ROOM",rooms)

  StartDate= st.date_input("StartDate", min_value=date.today())
  EndDate= st.date_input("EndDate", min_value=date.today())

# ---------------- Calcul automatique ----------------
  if EndDate > StartDate:
   nb_nights = (EndDate - StartDate).days
   total_price= nb_nights * price_per_night[room_type]

   st.info(f"💰total Price : {total_price} € ({nb_nights} nights)")
  else:
   st.warning("End date must be after start date")

# ---------------- Bouton ----------------
  if st.button("Confirm Booking"):
    if EndDate <= StartDate:
            st.error("❌ invalid Dates ")
    else:
            # Vérifier si la chambre est libre
            cursor.execute("""
                SELECT *
                FROM BOOKING
                WHERE ROOM_CodR= %s
                AND NOT (%s >= EndDate OR %s <= StartDate)
            """, (room, StartDate, EndDate))

            if cursor.fetchone():
                st.error("❌ Room already booked ")
            else:
                cursor.execute("""
                    INSERT INTO BOOKING
                    (ROOM_CodR,TRAVEL_AGENCY_CodA,StartDate,EndDate,Cost)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    room,
                    agency,
                    StartDate,
                    EndDate,
                    total_price
                ))
                conn.commit()

                st.success("✅ Booking successfully saved")

with tab_graph:
 st.header(" 📈 Monthly Average Cost Evolution")
 st.markdown("You can track price fluctuations over the months to adapt your pricing strategy")
# Préparation des données pour le graphique
 df_graph = df.groupby('month_year')['Cost'].mean().reset_index()
 df_graph['Month'] = df_graph['month_year'].astype(str)
 # Affichage du graphique linéaire
 st.line_chart(df_graph, x='Month', y='Cost', use_container_width=True)

with tab_top_rooms:
    st.header("Most expensive rooms per month")
    st.markdown("You will find the code,area,type and floor of the rooms with the highest average daily cost for each period")
 # Calcul de la chambre la plus chère par mois
    df_month_room = df.groupby(['month_year', 'ROOM_CodR']).agg(avg_daily_price=('Cost', 'mean')).reset_index()
    idx = df_month_room.groupby('month_year')['avg_daily_price'].idxmax()
    df_top_room = df_month_room.loc[idx]
    # Jointure pour les détails (superficie, étage, type)
    conn=get_connection()
    df['SurfaceArea']=pd.read_sql("SELECT SurfaceArea FROM ROOM",conn)
    df['Floor']=pd.read_sql("SELECT Floor FROM ROOM",conn)
    df["Type"]=pd.read_sql("SELECT Type FROM ROOM",conn)
    conn.close()
    df_top_details = pd.merge(df_top_room, df[['ROOM_CodR', 'SurfaceArea', 'Floor', 'Type']].drop_duplicates(), on='ROOM_CodR', how='left').drop_duplicates(subset=['month_year'])
 # Formatage de l'affichage
    df_top_display = df_top_details[['month_year', 'ROOM_CodR', 'Floor', 'SurfaceArea', 'Type', 'avg_daily_price']]
    df_top_display.columns = ['Month', 'Cod', 'Floor', 'Area(m²)', 'Room Type', 'Average price (€)']
    df_top_display['Average price(€)'] = df_top_display['Average price (€)'].map('{:,.2f} €'.format)
# Affichage dans un tableau
    st.dataframe(df_top_display, use_container_width=True, hide_index=True)
# --- 5.  Filtre par type de chambre---
st.subheader("🔍Filters available through our types of rooms")

col1, col2 = st.columns(2)

with col1:
 selected_types = st.multiselect(
            'SELECT ROOM TYPES',
            options=df['Type'].unique(),
            default=df['Type'].unique()
)

with col2:
 min_date = df['StartDate'].min().date()
 max_date = df['StartDate'].max().date()
 date_range = st.date_input(
            "SELECT A PERIOD",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date)
# Application des filtres pour la vue détaillée
 if len(date_range) == 2:
        StartDate, EndDate = date_range
        df_filtered = df[(df['Type'].isin(selected_types)) &
                         (df['StartDate'].dt.date >= StartDate) &
                         (df['StartDate'].dt.date <= EndDate) ]
 else:
# Gère le cas où l'utilisateur n'a sélectionné qu'une seule date
        df_filtered = df[df['Type'].isin(selected_types)]

# --- 6. Vue Détaillée des Données Filtrées (Bas de Page) ---

st.header("Full booking List Based on Selected Filters")

# Utilisation d'un expander pour ne pas surcharger la page
with st.expander(f" 🔍⚙️ show filtred data ({df_filtered.shape[0]} lignes)", expanded=False):
    st.markdown("Here is the liste of all available booking.")
    st.dataframe(df_filtered.sort_values(by='StartDate', ascending=False), use_container_width=True)

####FILTRES##
st.subheader("🔍 Filters available through our agencies")
try:
    conn = get_connection()
    df_agencies= pd.read_sql("SELECT CodA FROM TRAVEL_AGENCY", conn)
except Exception as e:
    st.error(f"Error loading agencies : {e}")
    st.stop()

# Filtre agence
agency_list = ["ALL"] + df_agencies["CodA"].tolist()
agency_filter = st.selectbox("Agency",agency_list)

# Filtres dates
col1, col2 = st.columns(2)
with col1:
    StartDate_filter = st.date_input("StartDate(filtre)", value=None)
with col2:
    EndDate_filter = st.date_input("EndDate(filtre)", value=None)

# ==================================================
# ============ REQUÊTE 1 : DÉTAIL ==================
# ==================================================

st.divider()
st.subheader("Details that you can view for all reservations depending on your chosen agency")

query1 = """
SELECT
    B.ROOM_CodR AS Room_Code,
    R.SurfaceArea,
    R.Floor,
    B.StartDate,
    B.EndDate,
    DATEDIFF(B.StartDate,B.EndDate) AS Nb_nights,
    B.Cost AS Total_Cost,
    T.CodA AS Agency_Code,
    T.WebSite,
    C.Name AS City
FROM BOOKING B
INNER JOIN ROOM R ON B.ROOM_CodR = R.CodR
INNER JOIN TRAVEL_AGENCY T ON B.TRAVEL_AGENCY_CodA = T.CodA
INNER JOIN CITY C ON T.City_Address = C.Name
WHERE 1=1
"""

params1 = []

if agency_filter != "ALL":
    query1 += " AND T.CodA = %s"
    params1.append(agency_filter)

if StartDate_filter:
    query1 += " AND B.StartDate >= %s"
    params1.append(StartDate_filter)

if EndDate_filter:
    query1 += " AND B.EndDate<= %s"
    params1.append(EndDate_filter)

query1 += " ORDER BY B.ROOM_CodR, B.StartDate"

df_detail = pd.read_sql(query1, conn, params=params1)

st.dataframe(df_detail, use_container_width=True)
