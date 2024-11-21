import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from conn import fetch_data
from theme import apply_custom_theme

# Apply custom theme for background and styles
apply_custom_theme()

def show_pie_chart(skinsolver_df):
    # Hitung jumlah produk per SKIN SOLVER
    count_data = skinsolver_df['SKIN SOLVER'].value_counts()

    # Definisikan warna soft
    colors = ['#FF9999', '#66B3FF', '#99FF99', '#FFCC99', '#FFD700', '#FFB6C1', '#DDA0DD', '#FF6347']

    # Membuat pie chart
    plt.figure(figsize=(8, 6))
    wedges, texts, autotexts = plt.pie(count_data, labels=count_data.index, autopct='%1.1f%%', startangle=140, colors=colors)

    st.write("")
    st.write("")
    st.write("")
    st.write("")
    # Set the title with white color
    st.markdown("<h1 style='text-align: center; color: #0a062e;'>DISTRIBUSI SKIN SOLVER SERUM SOMETHINC</h1>", unsafe_allow_html=True)

    # Add a 3D-like effect by raising the pie chart
    for wedge in wedges:
        wedge.set_linewidth(2)
        wedge.set_edgecolor('white')  # Add a white edge to each wedge

    # Remove background
    plt.gca().set_facecolor('none')  # Set background to transparent
    plt.gcf().patch.set_alpha(0)  # Make figure background transparent
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)  # Adjust layout for spacing

    # Menampilkan pie chart di Streamlit
    st.pyplot(plt)

def show_skinsolver():
    query = "SELECT * FROM skinsolver"
    skinsolver_data = fetch_data(query)

    if skinsolver_data:
        skinsolver_df = pd.DataFrame(skinsolver_data, columns=['KS', 'Skin_Solver', 'KP', 'Produk'])
        skinsolver_df.columns = ['KS', 'SKIN SOLVER', 'KP', 'PRODUK']

        # Display header
        st.markdown("<h1 style='text-align: center;'>DATA SKIN SOLVER</h1>", unsafe_allow_html=True)

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
        st.markdown("<div class='styled-table-container'>" + skinsolver_df.to_html(classes='styled-table', escape=False) + "</div>", unsafe_allow_html=True)

        # Menampilkan pie chart
        show_pie_chart(skinsolver_df)

    else:
        st.error("Failed to load skin solver data.")
