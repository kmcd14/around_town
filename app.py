import streamlit as st
from sqlalchemy.orm import joinedload
from sqlalchemy import or_
from contextlib import contextmanager
from db_conn import Session
from models import Group, Category
import pandas as pd
import plotly.express as px

# Load CSS
def load_css(file_path):
    with open(file_path) as f:
        css = f.read()
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

load_css("styles.css")

@contextmanager
def get_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()

# Sidebar
st.sidebar.title('Around Town 🏙️')
st.sidebar.divider()

with get_session() as session:
    categories = session.query(Category).all()
    category_options = ['All'] + sorted([c.category for c in categories])
    selected_cat = st.sidebar.selectbox("Category", category_options)

    age_groups = session.query(Group.age_group).distinct().all()
    age_options = ['All'] + sorted([age[0] for age in age_groups])
    selected_age = st.sidebar.multiselect("Age Group", age_options, default=['All'])

    areas = session.query(Group.area).distinct().all()
    area_options = ['All'] + sorted([a[0] for a in areas])
    selected_area = st.sidebar.selectbox("Area", area_options)

st.sidebar.divider()
st.sidebar.page_link(
    'https://docs.google.com/forms/d/e/1FAIpQLSecRjjoJ3OGduMiqu1CMmIu0wFeK0BHezjHW383ipB_erYA6w/viewform?usp=sharing',
    label='Submit a group', icon='👨‍👩‍👧‍👦'
)

# Main
st.title('Around Town 🏙️')
st.divider()

search_query = st.text_input("🔎 Search for a group", "", key="main_search")

with get_session() as session:
    query = session.query(Group).options(joinedload(Group.category))

    if selected_cat != 'All':
        category_obj = session.query(Category).filter_by(category=selected_cat).first()
        if category_obj:
            query = query.filter(Group.category_id == category_obj.category_id)

    if 'All' not in selected_age:
        query = query.filter(Group.age_group.in_(selected_age))

    if selected_area != 'All':
        query = query.filter(Group.area == selected_area)

    if search_query:
        query = query.filter(
            or_(
                Group.name.ilike(f"%{search_query}%"),
                Group.description.ilike(f"%{search_query}%"),
                Group.area.ilike(f"%{search_query}%")
            )
        )

    groups = query.order_by(Group.name.asc()).all()
    group_count = len(groups)

st.subheader(f"Found {group_count} group(s) 🕵️‍♀️ ")

tab1, tab2 = st.tabs(["🗂️ Groups", "📈 Insights"])

# Groups tab
with tab1:
    cols = st.columns(2)
    for i, group in enumerate(groups):
        with cols[i % 2]:
            st.markdown(f"""
                <div style="background-color:#ffffff; padding: 16px; border-radius: 12px;
                            box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 20px;">
                    <h4 style="color:#0b2c75;">{group.name}</h4>
            """, unsafe_allow_html=True)

            st.markdown(f"**📍 Area:** {group.area} | **👥 Age:** {group.age_group}")

            with st.expander("See more info"):
                st.markdown(f"**📍 Area:** {group.area}")
                st.markdown(f"**👥 Age Group:** {group.age_group}")
                st.markdown(f"**📄 Description:** {group.description or 'N/A'}")
                st.markdown(f"**🌐 Website:** [{group.website}]({group.website})" if group.website else "**🌐 Website:** N/A")
                st.markdown(f"**📧 Email:** {group.email or 'N/A'}")
                st.markdown(f"**📞 Phone:** {group.phone or 'N/A'}")

            st.markdown("</div>", unsafe_allow_html=True)

# Insights tab
with tab2:
    st.subheader("Data Insights")
    insight_metric = st.selectbox('Choose an Insight', ['Groups by Area', 'Category Distribution', 'Age Group Distribution'])

    area_df = pd.DataFrame([g.area for g in groups], columns=['Area'])
    area_counts = area_df.value_counts().reset_index(name='Count')
    fig_area = px.bar(area_counts, x='Area', y='Count', title='Groups per Area')

    category_map = {cat.category_id: cat.category for cat in categories}
    category_labels = [category_map.get(g.category_id, 'Unknown') for g in groups]
    cat_df = pd.DataFrame(category_labels, columns=['Category'])
    cat_counts = cat_df.value_counts().reset_index(name='Count')
    fig_cat = px.pie(cat_counts, names='Category', values='Count', title='Group Categories')

    age_df = pd.DataFrame([g.age_group for g in groups], columns=['Age Group'])
    age_counts = age_df.value_counts().reset_index(name='Count')
    fig_age = px.bar(age_counts, x='Age Group', y='Count', title='Age Group Distribution')

    if insight_metric == 'Groups by Area':
        st.plotly_chart(fig_area, use_container_width=True, key="area_chart")
    elif insight_metric == 'Category Distribution':
        st.plotly_chart(fig_cat, use_container_width=True, key="category_chart")
    elif insight_metric == 'Age Group Distribution':
        st.plotly_chart(fig_age, use_container_width=True, key="age_group_chart")
