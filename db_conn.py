import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Create the Base class
Base = declarative_base()

# Get DB URL from Streamlit secrets
DATABASE_URL = st.secrets["general"]["DB_URL"]

# Create SQLAlchemy engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    pool_size=10,  # Max number of connections to keep in the pool
    max_overflow=20,  # Max number of connections that can exceed pool_size
    pool_timeout=30,  # Max time to wait for a connection before throwing an error
    pool_recycle=1800  # Recycle connections after this many seconds (optional)
)

# Create session maker
Session = sessionmaker(bind=engine)

# Test connection (optional but helpful for troubleshooting)
try:
    with engine.connect() as connection:
        print("Connection successful!")
except Exception as e:
    print(f"Failed to connect: {e}")