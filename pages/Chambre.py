import streamlit as st
import pandas as pd
from db import get_connection
from sidebar import render_sidebar

st.set_page_config(
    page_title="MorY HOTELS",
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
        "title": "MorY HOTELS",
        "filter": "Filter Rooms",
        "type": "Room Type",
        "all": "All",
        "simple": "single",
        "double": "double",
        "triple": "triple",
        "suite": "suite",
        "floor": "Floor",
        "amenities": "Amenities",
        "kitchen": "Kitchen",
        "results": "Available Rooms",
        "none": "No rooms found"
    },
    "FR": {
        "title": "MorY HOTELS",
        "filter": "Filtrer les Chambres",
        "type": "Type",
        "all": "Toutes",
        "simple": "single",
        "double": "double",
        "triple": "triple",
        "suite": "suite",
        "floor": "Étage",
        "amenities": "Équipements",
        "kitchen": "Cuisine",
        "results": "Chambres Disponibles",
        "none": "Aucune chambre"
    },
    "AR": {
        "title": "فنادق موري",
        "filter": "تصفية الغرف",
        "type": "النوع",
        "all": "الكل",
        "simple": "single",
        "double": "double",
        "triple": "triple",
        "suite": "suite",
        "floor": "الطابق",
        "amenities": "المرافق",
        "kitchen": "مطبخ",
        "results": "الغرف المتاحة",
        "none": "لا توجد غرف"
    }
}

T = LANGS[lang_choice]

if lang_choice == "AR":
    st.markdown("""
        <style>
            [data-testid="stMainBlockContainer"] {
                direction: RTL;
                text-align: right;
            }
            [data-testid="stSidebar"] {
                direction: LTR;
                text-align: left;
            }
        </style>
    """, unsafe_allow_html=True)

st.title(T['title'])
st.divider()

conn = get_connection()
cursor = conn.cursor(dictionary=True)

cursor.execute("SELECT DISTINCT AMENITIES_Amenity FROM HAS_AMENITIES")
amenities_list = [row['AMENITIES_Amenity'] for row in cursor.fetchall()]

st.subheader(T['filter'])
col1, col2, col3, col4 = st.columns(4)

with col1:
    type_opts = [T["all"], T["simple"], T["double"], T["triple"], T["suite"]]
    type_display = st.selectbox(T["type"], type_opts)
    type_map = {T["all"]: "All", T["simple"]: "single", T["double"]: "double",
                T["triple"]: "triple", T["suite"]: "suite"}
    room_type = type_map[type_display]

with col2:
    floor_filter = st.selectbox(T["floor"], ["All", "1", "2", "3", "4", "5", "6", "7", "8"])

with col3:
    selected_amenities = st.multiselect(T["amenities"], amenities_list)

with col4:
    has_kitchen = st.checkbox(T["kitchen"])

st.divider()

query = "SELECT CodR, Floor, SurfaceArea, Type FROM ROOM WHERE 1=1"

if room_type != "All":
    query += f" AND Type = '{room_type}'"

if floor_filter != "All":
    query += f" AND Floor = {floor_filter}"

for amenity in selected_amenities:
    query += f"""
        AND EXISTS (
            SELECT 1 FROM HAS_AMENITIES H
            WHERE H.ROOM_CodR = ROOM.CodR AND H.AMENITIES_Amenity = '{amenity}'
        )
    """

if has_kitchen:
    query += """
        AND EXISTS (
            SELECT 1 FROM HAS_SPACES S
            WHERE S.ROOM_CodR = ROOM.CodR AND S.SPACES_Space = 'kitchen'
        )
    """

cursor.execute(query)
rooms = cursor.fetchall()

IMAGES = {
    "single": "https://i.pinimg.com/originals/81/d2/d4/81d2d4092bdeb4ac85950085541d31ca.jpg",
    "double": "https://i.pinimg.com/originals/f9/cd/83/f9cd83db4e00175770998abeca0f3299.jpg",
    "triple": "https://www.causeway.com.au/static/uploads/images/causeway-353-hotel-deluxe-triple-room-dtr01-wfjxnbgbxuoa.jpg",
    "suite": "https://ik.imgkit.net/3vlqs5axxjf/external/http://www.cfmedia.vfmleonardo.com/imageRepo/7/0/145/173/302/mc-rbamc-rbamc-rendering-guestroom-29261_Classic-Hor_O.jpg"
}

st.subheader(T['results'])

if rooms:
    df = pd.DataFrame(rooms)
    
    for index, row in df.head(5).iterrows():
        col_text, col_image = st.columns(2)
        
        with col_text:
            st.markdown(f"**Room {row['CodR']}**")
            st.write(f"Type: {row['Type']}")
            st.write(f"{T['floor']}: {row['Floor']}")
            st.write(f"Surface: {row['SurfaceArea']} m²")
        
        with col_image:
            st.image(IMAGES.get(row['Type'], ""), use_container_width=True)
        
        st.divider()
    
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info(T['none'])

cursor.close()
conn.close()