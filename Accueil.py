import streamlit as st
from sidebar import render_sidebar

st.set_page_config(
    page_title="Travel Project",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        [data-testid="stSidebarNav"] { display: none; }
    </style>
""", unsafe_allow_html=True)

lang_choice = render_sidebar()

LANGS = {
    "ENG": {
        "page_title": "Home - Travel Agency Project",
        "hero_title": "Database Project",
        "hero_subtitle": "Travel Agency Management System",
        "hero_caption": "Data management and visualization application",
        "info_title": "General Information",
        "label_school": "Institution",
        "school_val": "Ensa Kenitra",
        "label_course": "Course",
        "course_val": "Relational Databases",
        "label_year": "Academic Year",
        "year_val": "2025-2026",
        "label_goals": "Project Objectives",
        "goals_list": "- Relational database design\n- MySQL implementation\n- User interface development\n- Data analysis and visualization",
        "team_title": "Project Team",
        "team_caption": "Students who contributed to this project",
        "feat_title": "Application Features",
        "feat_agency_title": "Agency Management",
        "feat_agency_list": "- Full agency list\n- Search by city\n- Map visualization\n- Data export",
        "feat_stats_title": "Statistics",
        "feat_stats_list": "- Key indicators\n- Interactive charts\n- Geographic analysis\n- Detailed reports",
        "feat_search_title": "Advanced Search",
        "feat_search_list": "- Multiple filters\n- Real-time results\n- Intuitive interface\n- Smooth navigation",
        "tech_title": "Technologies Used",
        "tech_db": "Database",
        "tech_back": "Backend",
        "tech_front": "Frontend",
        "tech_viz": "Visualization"
    },
    "FR": {
        "page_title": "Accueil - Projet Agences de Voyage",
        "hero_title": "Projet Base de Données",
        "hero_subtitle": "Système de Gestion des Agences de Voyage",
        "hero_caption": "Application de gestion et visualisation des données",
        "info_title": "Informations Générales",
        "label_school": "Établissement",
        "school_val": "Ensa Kenitra",
        "label_course": "Cours",
        "course_val": "Base de Données Relationnelles",
        "label_year": "Année Académique",
        "year_val": "2025-2026",
        "label_goals": "Objectifs du Projet",
        "goals_list": "- Conception d'une base de données relationnelle\n- Implémentation avec MySQL\n- Développement d'une interface utilisateur\n- Analyse et visualisation des données",
        "team_title": "Équipe du Projet",
        "team_caption": "Les étudiants qui ont contribué à ce projet",
        "feat_title": "Fonctionnalités de l'Application",
        "feat_agency_title": "Gestion des Agences",
        "feat_agency_list": "- Liste complète des agences\n- Recherche par ville\n- Visualisation sur carte\n- Export des données",
        "feat_stats_title": "Statistiques",
        "feat_stats_list": "- Indicateurs clés\n- Graphiques interactifs\n- Analyse géographique\n- Rapports détaillés",
        "feat_search_title": "Advanced Search",
        "feat_search_list": "- Filtres multiples\n- Résultats en temps réel\n- Interface intuitive\n- Navigation fluide",
        "tech_title": "Technologies Utilisées",
        "tech_db": "Base de Données",
        "tech_back": "Backend",
        "tech_front": "Frontend",
        "tech_viz": "Visualisation"
    },
    "AR": {
        "page_title": "الرئيسية - مشروع وكالات السفر",
        "hero_title": "مشروع قاعدة البيانات",
        "hero_subtitle": "نظام إدارة وكالات السفر",
        "hero_caption": "تطبيق إدارة وعرض البيانات",
        "info_title": "معلومات عامة",
        "label_school": "المؤسسة",
        "school_val": "Ensa Kenitra",
        "label_course": "المادة",
        "course_val": "قواعد البيانات العلايقية",
        "label_year": "السنة الأكاديمية",
        "year_val": "2025-2026",
        "label_goals": "أهداف المشروع",
        "goals_list": "- تصميم قاعدة بيانات علائقية\n- التنفيذ باستخدام MySQL\n- تطوير واجهة المستخدم\n- تحليل البيانات وتصورها",
        "team_title": "فريق المشروع",
        "team_caption": "الطلاب الذين ساهموا في هذا المشروع",
        "feat_title": "مميزات التطبيق",
        "feat_agency_title": "إدارة الوكالات",
        "feat_agency_list": "- قائمة الوكالات الكاملة\n- البحث حسب المدينة\n- العرض على الخريطة\n- تصدير البيانات",
        "feat_stats_title": "الإحصائيات",
        "feat_stats_list": "- المؤشرات الرئيسية\n- رسوم بيانية تفاعلية\n- التحليل الجغرافي\n- تقارير مفصلة",
        "feat_search_title": "البحث المتقدم",
        "feat_search_list": "- فلاتر متعددة\n- نتائج فورية\n- واجهة سهلة\n- تنقل سلس",
        "tech_title": "التقنيات المستخدمة",
        "tech_db": "قاعدة البيانات",
        "tech_back": "الخلفية",
        "tech_front": "الواجهة",
        "tech_viz": "التمثيل البياني"
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

st.markdown(f"# {T['hero_title']}")
st.markdown(f"## {T['hero_subtitle']}")
st.caption(T['hero_caption'])
st.divider()

st.markdown(f"### {T['info_title']}")
col1, col2 = st.columns(2)

with col1:
    st.info(f"**{T['label_school']} :** {T['school_val']}")
    st.info(f"**{T['label_course']} :** {T['course_val']}")
    st.info(f"**{T['label_year']} :** {T['year_val']}")

with col2:
    st.markdown(f"#### {T['label_goals']}")
    st.success(T['goals_list'])

st.divider()

st.markdown(f"### {T['team_title']}")
st.caption(T['team_caption'])

students = [
    {"name": "Bouali Younes", "role": "Git & Agency Page"},
    {"name": "Student 2", "role": "Backend Developer"},
    {"name": "Student 3", "role": "Frontend Developer"},
    {"name": "Student 4", "role": "UI/UX Designer"},
    {"name": "Student 5", "role": "Data Analyst"},
    {"name": "Student 6", "role": "QA Tester"},
    {"name": "Student 7", "role": "Documentation"}
]

row1_cols = st.columns(4)
for i, col in enumerate(row1_cols):
    with col:
        st.markdown(f"#### {students[i]['name']}")
        st.caption(students[i]['role'])

st.markdown("")

row2_cols = st.columns(3)
for i, col in enumerate(row2_cols):
    with col:
        st.markdown(f"#### {students[i+4]['name']}")
        st.caption(students[i+4]['role'])

st.divider()

st.markdown(f"### {T['feat_title']}")
fcol1, fcol2, fcol3 = st.columns(3)

with fcol1:
    st.markdown(f"#### {T['feat_agency_title']}")
    st.write(T['feat_agency_list'])

with fcol2:
    st.markdown(f"#### {T['feat_stats_title']}")
    st.write(T['feat_stats_list'])

with fcol3:
    st.markdown(f"#### {T['feat_search_title']}")
    st.write(T['feat_search_list'])

st.divider()

st.markdown(f"### {T['tech_title']}")
tcol1, tcol2, tcol3, tcol4 = st.columns(4)

with tcol1:
    st.metric(label=T['tech_db'], value="MySQL")
with tcol2:
    st.metric(label=T['tech_back'], value="Python")
with tcol3:
    st.metric(label=T['tech_front'], value="Streamlit")
with tcol4:
    st.metric(label=T['tech_viz'], value="Pandas")

st.divider()