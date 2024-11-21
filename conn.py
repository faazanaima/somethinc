import pymysql
import streamlit as st

def fetch_data(query):
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='admin',
            database='somethinc'
        )
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        return result
    except pymysql.MySQLError as e:
        st.error(f"Database connection failed: {e}")
        return None
    finally:
        if connection:
            connection.close()

def create_connection():
    connection = None
    try:
        connection = pymysql.connect(
            host='localhost', 
            user='root',     
            password='admin', 
            database='somethinc'      
        )
        ## st.markdown("<div style='color: #ffffff; background-color: #77f059; padding: 10px; border-radius: 5px; font-size: 14px;'>Connection to MySQL DB successful!</div>", unsafe_allow_html=True)
    except pymysql.MySQLError as e:
        st.error(f"The error '{e}' occurred")
    
    return connection
