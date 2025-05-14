import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Create the Base class
Base = declarative_base()

# Get DB URL from Streamlit secrets
DATABASE_URL = st.secrets["general"]["DB_URL"]


# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# Test connection
try:
    with engine.connect() as connection:
        print("Connection successful!")
except Exception as e:
    print(f"Failed to connect: {e}")
