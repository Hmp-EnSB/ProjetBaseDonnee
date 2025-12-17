import streamlit as st
import pandas as pd
import datetime as dt
from datetime import date
from db import get_connection
from sidebar import render_sidebar

# 1. SET PAGE CONFIG FIRST
st.set_page_config(
    page_title="Hotel Management",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. HIDE DEFAULT NAV
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] { display: none; }
    </style>
""", unsafe_allow_html=True)

# 3. INITIALIZE SIDEBAR & LANG
# Note: Since your sidebar.py now returns the lang_choice, we catch it here
lang_choice = render_sidebar()

LANGS = {
    "ENG": {
        "page_title": "Hotel Reservation Management",
        "welcome_title": "Welcome to our Hotel Booking Dashboard",
        "welcome_sub": "This interactive dashboard provides an overview of performance and cost trends.",
        "kpi_section": "OVERALL PERFORMANCE",
        "metric_res": "Total Reservations",
        "metric_rev": "Total Revenue",
        "metric_price": "Average Daily Price",
        "metric_days": "Total Occupied Days",
        "unit_days": "days",
        "tab_trend": "Cost Evolution",
        "tab_top": "Most expensive rooms by month",
        "tab_book": "Book Your Stay",
        "book_title": "Book Your Next Stay Easily",
        "agency_label": "Travel Agency",
        "room_type_label": "Room Type",
        "room_label": "ROOM",
        "start_label": "Start Date",
        "end_label": "End Date",
        "total_price_info": "Total Price",
        "nights": "nights",
        "date_error": "End date must be after start date",
        "confirm_btn": "Confirm Booking",
        "invalid_dates": "Invalid Dates",
        "room_busy": "Room already booked",
        "booking_success": "Booking successfully saved",
        "chart_title": "Monthly Average Cost Evolution",
        "chart_desc": "Track price fluctuations to adapt strategy",
        "top_rooms_title": "Most expensive rooms per month",
        "filter_section": "Filters available through our types of rooms",
        "select_type": "SELECT ROOM TYPES",
        "select_period": "SELECT A PERIOD",
        "full_list": "Full booking List Based on Selected Filters",
        "show_data": "show filtered data",
        "rows": "rows",
        "agency_filter_section": "Filters available through our agencies",
        "agency_label_filter": "Agency",
        "details_section": "Details for all reservations depending on agency"
    },
    "FR": {
        "page_title": "Gestion des Réservations",
        "welcome_title": "Bienvenue sur le tableau de bord",
        "welcome_sub": "Ce tableau de bord interactif donne un aperçu des performances.",
        "kpi_section": "PERFORMANCE GLOBALE",
        "metric_res": "Total Réservations",
        "metric_rev": "Revenu Total",
        "metric_price": "Prix Journalier Moyen",
        "metric_days": "Total Jours Occupés",
        "unit_days": "jours",
        "tab_trend": "Évolution des Coûts",
        "tab_top": "Chambres les plus chères",
        "tab_book": "Réserver",
        "book_title": "Réservez votre séjour en quelques clics",
        "agency_label": "Agence de Voyage",
        "room_type_label": "Type de Chambre",
        "room_label": "CHAMBRE",
        "start_label": "Date de début",
        "end_label": "Date de fin",
        "total_price_info": "Prix Total",
        "nights": "nuits",
        "date_error": "La date de fin doit être après le début",
        "confirm_btn": "Confirmer la réservation",
        "invalid_dates": "Dates invalides",
        "room_busy": "Chambre déjà occupée",
        "booking_success": "Réservation enregistrée",
        "chart_title": "Évolution du coût moyen mensuel",
        "chart_desc": "Suivez les fluctuations de prix",
        "top_rooms_title": "Chambres les plus chères par mois",
        "filter_section": "Filtres par types de chambres",
        "select_type": "CHOISIR TYPES",
        "select_period": "CHOISIR PÉRIODE",
        "full_list": "Liste complète selon filtres",
        "show_data": "afficher les données",
        "rows": "lignes",
        "agency_filter_section": "Filtres par agences",
        "agency_label_filter": "Agence",
        "details_section": "Détails des réservations par agence"
    },
    "AR": {
        "page_title": "إدارة حجز الفنادق",
        "welcome_title": "مرحباً بكم في لوحة تحكم الحجوزات",
        "welcome_sub": "توفر هذه اللوحة نظرة عامة على الأداء واتجاهات التكلفة",
        "kpi_section": "الأداء العام",
        "metric_res": "إجمالي الحجوزات",
        "metric_rev": "إجمالي الإيرادات",
        "metric_price": "متوسط السعر اليومي",
        "metric_days": "إجمالي الأيام المحجوزة",
        "unit_days": "أيام",
        "tab_trend": "تطور التكلفة",
        "tab_top": "أغلى الغرف شهرياً",
        "tab_book": "احجز إقامتك",
        "book_title": "احجز إقامتك التالية بسهولة",
        "agency_label": "وكالة السفر",
        "room_type_label": "نوع الغرفة",
        "room_label": "الغرفة",
        "start_label": "تاريخ البدء",
        "end_label": "تاريخ الانتهاء",
        "total_price_info": "السعر الإجمالي",
        "nights": "ليالي",
        "date_error": "تاريخ الانتهاء يجب أن يكون بعد تاريخ البدء",
        "confirm_btn": "تأكيد الحجز",
        "invalid_dates": "تواريخ غير صالحة",
        "room_busy": "الغرفة محجوزة بالفعل",
        "booking_success": "تم حفظ الحجز بنجاح",
        "chart_title": "تطور متوسط التكلفة الشهري",
        "chart_desc": "تتبع تقلبات الأسعار لتكييف الاستراتيجية",
        "top_rooms_title": "أغلى الغرف حسب الشهر",
        "filter_section": "التصفيات المتاحة حسب نوع الغرفة",
        "select_type": "اختر أنواع الغرف",
        "select_period": "اختر الفترة",
        "full_list": "قائمة الحجوزات الكاملة حسب الفلاتر",
        "show_data": "إظهار البيانات المصقاة",
        "rows": "صفوف",
        "agency_filter_section": "التصفيات المتاحة حسب الوكالات",
        "agency_label_filter": "الوكالة",
        "details_section": "التفاصيل لجميع الحجوزات حسب الوكالة"
    }
}

T = LANGS[lang_choice]

# 4. DATABASE FETCH
try:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query_base = """
        SELECT B.*, R.Type, R.Floor, R.SurfaceArea 
        FROM BOOKING B 
        JOIN ROOM R ON B.ROOM_CodR = R.CodR
    """
    df = pd.read_sql(query_base, conn)
except Exception as e:
    st.error(f"Error: {e}")
    st.stop()

# 5. DATA PRE-PROCESSING
df['StartDate'] = pd.to_datetime(df['StartDate'])
df['EndDate'] = pd.to_datetime(df['EndDate'])
df['duration'] = (df['EndDate'] - df['StartDate']).dt.days

# THE 't' WAS REMOVED FROM HERE

df['total_cost'] = df['Cost'] * df['duration']
df['month_year'] = df['StartDate'].dt.to_period('M')

# 6. UI HEADER
st.title(T['welcome_title'])
st.markdown(T['welcome_sub'])
st.divider()

# 7. KPI SECTION
st.header(T['kpi_section'])
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(T['metric_res'], f"{len(df):,.0f}")
with col2:
    st.metric(T['metric_rev'], f"{df['total_cost'].sum():,.0f} €")
with col3:
    st.metric(T['metric_price'], f"{df['Cost'].mean():,.2f} €")
with col4:
    st.metric(T['metric_days'], f"{df['duration'].sum():,.0f} {T['unit_days']}")

st.divider()

# 8. TABS SECTION
tab_graph, tab_top_rooms, tab_book = st.tabs([T['tab_trend'], T['tab_top'], T['tab_book']])

with tab_book:
    st.header(T['book_title'])
    price_per_night = {"single": 100, "double": 150, "suite": 300, "triple": 200}
    
    cursor.execute("SELECT CodA FROM TRAVEL_AGENCY")
    agencies = [row['CodA'] for row in cursor.fetchall()]
    
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        agency = st.selectbox(T['agency_label'], agencies)
        room_type = st.selectbox(T['room_type_label'], list(price_per_night.keys()))
    
    with col_b2:
        cursor.execute("SELECT CodR FROM ROOM WHERE Type = %s", (room_type,))
        rooms = [row['CodR'] for row in cursor.fetchall()]
        room = st.selectbox(T['room_label'], rooms)
        
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        StartDate = st.date_input(T['start_label'], min_value=date.today())
    with col_d2:
        EndDate = st.date_input(T['end_label'], value=date.today() + dt.timedelta(days=1), min_value=date.today())

    if EndDate > StartDate:
        nb_nights = (EndDate - StartDate).days
        total_p = nb_nights * price_per_night.get(room_type, 0)
        st.info(f"{T['total_price_info']} : {total_p} € ({nb_nights} {T['nights']})")
        
        if st.button(T['confirm_btn'], type="primary"):
            cursor.execute("""
                SELECT * FROM BOOKING 
                WHERE ROOM_CodR = %s 
                AND NOT (%s >= EndDate OR %s <= StartDate)
            """, (room, StartDate, EndDate))
            
            if cursor.fetchone():
                st.error(T['room_busy'])
            else:
                cursor.execute("""
                    INSERT INTO BOOKING (ROOM_CodR, TRAVEL_AGENCY_CodA, StartDate, EndDate, Cost) 
                    VALUES (%s, %s, %s, %s, %s)
                """, (room, agency, StartDate, EndDate, price_per_night[room_type]))
                conn.commit()
                st.success(T['booking_success'])
                st.rerun()
    else:
        st.warning(T['date_error'])

with tab_graph:
    st.header(T['chart_title'])
    df_graph = df.groupby('month_year')['Cost'].mean().reset_index()
    df_graph['Month'] = df_graph['month_year'].astype(str)
    st.line_chart(df_graph.set_index('Month')['Cost'])

with tab_top_rooms:
    st.header(T['top_rooms_title'])
    idx = df.groupby('month_year')['Cost'].idxmax()
    st.dataframe(df.loc[idx, ['month_year', 'ROOM_CodR', 'Type', 'Cost', 'Floor']], use_container_width=True, hide_index=True)

st.divider()

# 9. FILTER & LIST SECTION
st.subheader(T['filter_section'])
col_f1, col_f2 = st.columns(2)
with col_f1:
    selected_types = st.multiselect(T['select_type'], options=df['Type'].unique(), default=df['Type'].unique())
with col_f2:
    date_range = st.date_input(T['select_period'], value=(df['StartDate'].min().date(), df['StartDate'].max().date()))

if len(date_range) == 2:
    df_filtered = df[
        (df['Type'].isin(selected_types)) & 
        (df['StartDate'].dt.date >= date_range[0]) & 
        (df['StartDate'].dt.date <= date_range[1])
    ]
else:
    df_filtered = df[df['Type'].isin(selected_types)]

st.header(T['full_list'])
with st.expander(f"{T['show_data']} ({len(df_filtered)} {T['rows']})"):
    st.dataframe(df_filtered.sort_values(by='StartDate', ascending=False), use_container_width=True)

st.divider()
st.subheader(T['agency_filter_section'])
agency_list = ["ALL"] + list(df['TRAVEL_AGENCY_CodA'].unique())
agency_filter = st.selectbox(T['agency_label_filter'], agency_list)

df_agency_final = df_filtered.copy()
if agency_filter != "ALL":
    df_agency_final = df_agency_final[df_agency_final['TRAVEL_AGENCY_CodA'] == agency_filter]

st.dataframe(df_agency_final[['ROOM_CodR', 'SurfaceArea', 'Floor', 'StartDate', 'EndDate', 'Cost', 'TRAVEL_AGENCY_CodA']], use_container_width=True)

conn.close()