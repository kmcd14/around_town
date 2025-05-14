import streamlit as st
from sqlalchemy.orm import sessionmaker
from db_conn import engine, Session
from models import Group, Category
import plotly.express as px
import pandas as pd
#from geopy.geocoders import Nominatim
#from geopy.exc import GeocoderTimedOut
import time
from contextlib import contextmanager

# Create a session context manager to ensure proper cleanup
@contextmanager
def get_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()

# Now use the context manager in your app
########################### SIDEBAR #############################################
st.sidebar.title('Around Town 🔍')
st.sidebar.divider()

# Category filter
with get_session() as session:
    categories = session.query(Category).all()
    category_options = ['All'] + sorted([category.category for category in categories])
    selected_cat = st.sidebar.selectbox('Category', category_options)

    # Age group filter
    age_groups = session.query(Group.age_group).distinct().all()
    age_options = ['All'] + sorted([age[0] for age in age_groups])
    selected_age = st.sidebar.multiselect('Age Group', age_options, default='All')

    # Area filter
    areas = session.query(Group.area).distinct().all()
    area_options = ['All'] + sorted([area[0] for area in areas])
    selected_area = st.sidebar.selectbox('Area', area_options)

    # Apply filters
    query = session.query(Group)
    if selected_cat != 'All':
        category_obj = session.query(Category).filter_by(category=selected_cat).first()
        if category_obj:
            query = query.filter(Group.category_id == category_obj.category_id)
    if 'All' not in selected_age:
        query = query.filter(Group.age_group.in_(selected_age))    
    if selected_area != 'All':
        query = query.filter(Group.area == selected_area)

    group_count = query.count()
    groups = query.order_by(Group.name.asc()).all()





























  






st.sidebar.divider()
st.sidebar.page_link(
    'https://docs.google.com/forms/d/e/1FAIpQLSecRjjoJ3OGduMiqu1CMmIu0wFeK0BHezjHW383ipB_erYA6w/viewform?usp=sharing',
    label='Submit a group', icon='👨‍👩‍👧‍👦')

########################### MAIN #############################################
st.title('Around Town 🔍')
st.divider()
st.subheader(f"🕵️‍♀️ Found {group_count} group(s) 🎯")

tab1, tab2 = st.tabs(["🗂️ Groups", "📈 Insights"])

######################## GROUP DISPLAY ##############################
with tab1:
    cols = st.columns(2)
    for i, group in enumerate(groups):
        with cols[i % 2]:
            st.markdown(f"""
            <div style="background-color:#ffffff; padding: 16px; border-radius: 12px;
                        box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 20px;">
                <h4 style="color:#e11d48;">{group.name}</h4>
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

######################## GEOCODING + MAP ##############################
#geolocator = Nominatim(user_agent="Around Town")
#
#def get_lat_long(address, area, retries=3):
#    for attempt in range(retries):
#        try:
#            if address:
#                location = geolocator.geocode(address, timeout=10)
#                if location:
#                    return location.latitude, location.longitude
#            location = geolocator.geocode(area, timeout=10)
#            if location:
#                return location.latitude, location.longitude
#        except GeocoderTimedOut:
#            time.sleep(2)
#    return None, None
#
#locations = []
#for group in groups:
#    lat, lon = get_lat_long(group.address if group.address else None, group.area)
#    locations.append([group.name, lat, lon, group.area])
#
#locations_df = pd.DataFrame(locations, columns=["Group", "Latitude", "Longitude", "Area"])
#
#fig_map = px.scatter_map(locations_df, lat="Latitude", lon="Longitude", hover_name="Group", hover_data=["Area"],
#                         title="Groups on Map", mapbox_style="carto-positron")
#st.plotly_chart(fig_map, use_container_width=True, key="map_chart")

######################## VISUAL INSIGHTS ##############################
with tab2:
    st.subheader("Data Insights")
    insight_metric = st.selectbox('Choose an Insight', ['Groups by Area', 'Category Distribution', 'Age Group Distribution'])

    # Groups per Area
    area_df = pd.DataFrame([g.area for g in groups], columns=['Area'])
    area_counts = area_df.value_counts().reset_index(name='Count')
    fig_area = px.bar(area_counts, x='Area', y='Count', title='Groups per Area')

    # Category Distribution
    category_map = {cat.category_id: cat.category for cat in categories}
    category_labels = [category_map.get(g.category_id, 'Unknown') for g in groups]
    cat_df = pd.DataFrame(category_labels, columns=['Category'])
    cat_counts = cat_df.value_counts().reset_index(name='Count')
    fig_cat = px.pie(cat_counts, names='Category', values='Count', title='Group Categories')

    # Age Group Distribution
    age_df = pd.DataFrame([g.age_group for g in groups], columns=['Age Group'])
    age_counts = age_df.value_counts().reset_index(name='Count')
    fig_age = px.bar(age_counts, x='Age Group', y='Count', title='Age Group Distribution')

    if insight_metric == 'Groups by Area':
        st.plotly_chart(fig_area, use_container_width=True, key="area_chart")
    elif insight_metric == 'Category Distribution':
        st.plotly_chart(fig_cat, use_container_width=True, key="category_chart")
    elif insight_metric == 'Age Group Distribution':
        st.plotly_chart(fig_age, use_container_width=True, key="age_group_chart")