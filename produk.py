import streamlit as st
import pandas as pd
from conn import fetch_data

def show_produk():
    query = "SELECT * FROM produk"
    produk_data = fetch_data(query)

    if produk_data:
        # Create DataFrame from fetched data
        produk_df = pd.DataFrame(produk_data, columns=['id_produk', 'KP', 'Nama Produk'])
        
        # Rename columns for display
        produk_df.columns = ['ID', 'KP', 'PRODUK']

        # Display header
        st.markdown("<h1 style='text-align: center;'>DATA PRODUK</h1>", unsafe_allow_html=True)

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
        st.markdown("<div class='styled-table-container'>" + produk_df.to_html(classes='styled-table', escape=False) + "</div>", unsafe_allow_html=True)

    else:
        st.error("Failed to load products.")
