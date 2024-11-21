import streamlit as st
import pandas as pd
from conn import fetch_data
from theme import apply_custom_theme

# Apply custom theme for background and styles
apply_custom_theme()

def display_rules():
    query = "SELECT * FROM rule"
    rule_data = fetch_data(query)

    if rule_data:
        # Create DataFrame from fetched data, including 'No' but not displaying it
        rule_df = pd.DataFrame(rule_data, columns=['No', 'Aturan', 'id_rule', 'AND', 'OR'])
        
        # Optionally, you can drop the 'No' column before displaying
        rule_df = rule_df.drop(columns=['No'])  # This line drops the 'No' column
        
        # Move 'id_rule' column to the leftmost position
        rule_df = rule_df[['id_rule', 'Aturan', 'AND', 'OR']]
        
        # Renaming columns as needed
        rule_df.columns = ['ID', 'RULE', 'AND_CONDITION', 'OR_CONDITION']
        
        # Display subheader in the center
        st.markdown("<h1 style='text-align: center;'>DATA RULES</h1>", unsafe_allow_html=True)

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
        st.markdown("<div class='styled-table-container'>" + rule_df.to_html(classes='styled-table', escape=False) + "</div>", unsafe_allow_html=True)

    else:
        st.error("Failed to load rules.")
