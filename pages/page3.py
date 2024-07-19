
#from navigation import make_sidebar
import streamlit as st

#make_sidebar()
import streamlit as st
import sqlite3
import pandas as pd
import requests
import base64
from io import BytesIO



# Configuration
GITHUB_USERNAME = 'shankar0213'
GITHUB_REPO = 'Anshid'
GITHUB_TOKEN = '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'
FILE_PATH = 'your_database_file.db'
BRANCH_NAME = 'main'

def github_api_headers():
    return {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Content-Type": "application/json"
    }

def download_file():
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_REPO}/contents/{FILE_PATH}?ref={BRANCH_NAME}"
    response = requests.get(url, headers=github_api_headers())
    file_content = response.json().get('content')
    if file_content:
        return base64.b64decode(file_content)
    return None

def upload_file(content):
    encoded_content = base64.b64encode(content).decode()
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_REPO}/contents/{FILE_PATH}"
    response = requests.get(url, headers=github_api_headers())
    sha = response.json().get('sha')
    
    data = {
        "message": "Update database",
        "content": encoded_content,
        "branch": BRANCH_NAME,
        "sha": sha
    }
    response = requests.put(url, json=data, headers=github_api_headers())
    return response.status_code == 200

def get_connection():
    db_content = download_file()
    if db_content:
        with open(FILE_PATH, 'wb') as f:
            f.write(db_content)
    conn = sqlite3.connect(FILE_PATH)
    return conn

def create_table():
    conn = get_connection()
    with conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT
        )
        """)
    conn.close()

def insert_data(name, email):
    conn = get_connection()
    with conn:
        conn.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
    conn.close()
    db_content = BytesIO()
    with open(FILE_PATH, 'rb') as f:
        db_content.write(f.read())
    upload_file(db_content.getvalue())

def read_data():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM users", conn)
    conn.close()
    return df

# Streamlit app layout
st.title("Database Operations")

create_table()

st.subheader("Insert Data")
name = st.text_input("Name")
email = st.text_input("Email")
if st.button("Insert"):
    insert_data(name, email)
    st.success("Data inserted successfully!")

if st.button("read Data"):
    dff=read_data()
    st.write(dff)

st.subheader("Data")
df = read_data()
st.write(df)
