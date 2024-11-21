import streamlit as st
import pymysql
from conn import create_connection
import pandas as pd
from theme import apply_custom_theme

# Apply custom theme for background and styles
apply_custom_theme()

# Function to get user history from the database
def get_user_history(username):
    connection = create_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM histori WHERE Username = %s", (username,))
                history = cursor.fetchall()
                return history
        except pymysql.MySQLError as e:
            st.error("An error occurred: " + str(e))
        finally:
            connection.close()
    return []

# Function to display user history
def show_history():
    st.markdown("<h1 style='text-align: center;'>HISTORY</h1>", unsafe_allow_html=True)
    
    # Check if user is logged in
    if 'username' in st.session_state and st.session_state['logged_in']:
        username = st.session_state['username']
        history = get_user_history(username)

        if history:
            # Create a DataFrame from the history data
            history_df = pd.DataFrame(history, columns=["ID", "Username", "Tanggal", "KG", "Produk", "Skinsolver"])
            
            # Reset index to have IDs starting from 1
            history_df.reset_index(drop=True, inplace=True)  # Reset index and drop old index
            history_df['ID'] = history_df.index + 1  # Create new ID column starting from 1

            # Inject custom CSS for table styling
            st.markdown("""
                <style>
                    .styled-table-container {
                        width: 100%;
                        height: 400px;  /* Set height for the scroll */
                        overflow-y: scroll;  /* Enable vertical scrolling */
                        border-radius: 10px;  /* Rounded corners */
                        border: 1px solid #ddd;  /* Light border */
                        margin-top: 20px;
                    }
                    .styled-table {
                        width: 100%;
                        border-collapse: collapse;
                        border-radius: 10px;  /* Rounded corners */
                        overflow: hidden;
                    }
                    .styled-table th, .styled-table td {
                        padding: 10px 15px;  /* Adjusted padding for softer appearance */
                        text-align: left;
                        font-size: 14px;
                        color: #003366;  /* Dark blue (biru dongker) text color */
                    }
                    .styled-table th {
                        background-color: #cfe2f3;  /* Light blue background for header */
                    }
                    .styled-table tr:nth-child(odd) {
                        background-color: #e6f0ff;  /* Softer light blue for odd rows */
                    }
                    .styled-table tr:nth-child(even) {
                        background-color: #f2f9ff;  /* Even rows with lighter blue */
                    }
                    .styled-table tr:hover {
                        background-color: #c9e0f3;  /* Slightly darker blue on hover */
                    }
                </style>
            """, unsafe_allow_html=True)

            # Render the table in the custom-styled div
            st.markdown("<div class='styled-table-container'>" + history_df.to_html(classes='styled-table', escape=False) + "</div>", unsafe_allow_html=True)
        
        else:
            st.write("No history found for this user.")
    else:
        # Directly using inline style to ensure warning message is styled properly
        st.markdown("<div style='color: #9C27B0; background-color: #F8BBD0; padding: 10px; border-radius: 5px; font-size: 16px;'>Please log in first.</div>", unsafe_allow_html=True)
