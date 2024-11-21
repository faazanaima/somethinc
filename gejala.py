import streamlit as st
import pandas as pd
from conn import fetch_data

def show_gejala():
    query = "SELECT * FROM gejala"
    gejala_data = fetch_data(query)

    if gejala_data:
        # Create DataFrame from fetched data
        gejala_df = pd.DataFrame(gejala_data, columns=['KG', 'Gejala', 'Nilai_MB', 'Nilai_MD', 'CF_Pakar', 'id_gejala'])

        # Move the 'id_gejala' column to the first position
        gejala_df = gejala_df[['id_gejala', 'KG', 'Gejala', 'Nilai_MB', 'Nilai_MD', 'CF_Pakar']]

        # Format columns for cleaner display
        gejala_df['Nilai_MB'] = gejala_df['Nilai_MB'].map('{:,.2f}'.format)
        gejala_df['Nilai_MD'] = gejala_df['Nilai_MD'].map('{:,.2f}'.format)
        gejala_df['CF_Pakar'] = gejala_df['CF_Pakar'].map('{:,.2f}'.format)

        # Rename columns
        gejala_df.columns = ['ID', 'KG', 'GEJALA', 'MB', 'MD', 'CF']

        # Display header
        st.markdown("<h1 style='text-align: center;'>DATA GEJALA</h1>", unsafe_allow_html=True)

        # Inject custom CSS for dark blue color scheme
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
        st.markdown("<div class='styled-table-container'>" + gejala_df.to_html(classes='styled-table', escape=False) + "</div>", unsafe_allow_html=True)

    else:
        st.error("Failed to load rules.")
        return None
