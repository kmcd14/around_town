import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Get DB URL from Streamlit secrets or from .env file
DATABASE_URL = st.secrets["general"]["DB_URL"]

# Create SQLAlchemy engine with the Session Pooler URL
engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20, pool_timeout=30)

# Create a Session object bound to the engine
Session = sessionmaker(bind=engine)

# Test connection
try:
    with engine.connect() as connection:
        print("Connection successful!")
except Exception as e:
    print(f"Failed to connect: {e}")
