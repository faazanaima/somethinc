import streamlit as st
import pymysql
import datetime
import pandas as pd
import re
from collections import defaultdict
from conn import fetch_data
from theme import apply_custom_theme

# Apply custom theme for background and styles
apply_custom_theme()

def apply_custom_styles():
    st.markdown("""
        <style>
        .product-name {
            font-size: 24px;
            font-weight: bold;
            color: #2C3E50;
            text-align: center;
        }
        .result-container {
            background-color: #ECF0F1;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .checkbox-text {
            color: #9B57F6; /* Text color */
            font-size: 16px;
            font-weight: bold;
        }
        .checkbox-container input {
            accent-color: #9C27B0; /* Custom checkbox color */
        }
        </style>
    """, unsafe_allow_html=True)

# Save to history function
def save_to_history(username, user_gejala_codes, produk_rekomendasi, skin_solvers):
    # Get today's date
    tanggal = datetime.date.today()

    # Establish the database connection
    conn = pymysql.connect(host='localhost', user='root', password='admin', db='somethinc')
    cursor = conn.cursor()
    insert_query = "INSERT INTO histori (Username, Tanggal, KG, Produk, Skinsolver) VALUES (%s, %s, %s, %s, %s)"
    
    # Ensure user_gejala_codes is not empty
    if not user_gejala_codes:
        raise ValueError("user_gejala_codes must not be empty.")

    # Join user_gejala_codes into a single string
    kg = ", ".join(user_gejala_codes)  # Concatenate all gejala codes into a string

    # Save each recommendation to history
    for produk, skin_solver in zip(produk_rekomendasi, skin_solvers):
        cursor.execute(insert_query, (username, tanggal, kg, produk, skin_solver))
    
    conn.commit()
    cursor.close()
    conn.close()

# Consolidated function for the entire process
def main_process():
    """Main function to handle gejala selection, CF calculation, rule evaluation, and recommendations."""
    # Apply custom styles
    apply_custom_styles()
    
    # Fetch data from MySQL
    queries = {
        "produk": "SELECT * FROM produk",
        "gejala": "SELECT * FROM gejala",
        "rule": "SELECT * FROM rule",
        "skinsolver": "SELECT * FROM skinsolver"
    }
    data = {name: fetch_data(query) for name, query in queries.items()}

    # Check for successful retrieval
    if all(data.values()):
        produk_df = pd.DataFrame(data['produk'], columns=['id_produk', 'KP', 'Nama Produk'])
        gejala_df = pd.DataFrame(data['gejala'], columns=['KG', 'Gejala', 'Nilai_MB', 'Nilai_MD', 'CF_Pakar', 'id_gejala'])
        rule_df = pd.DataFrame(data['rule'], columns=['No', 'Aturan', 'id_rule', 'AND', 'OR'])
        skinsolver_df = pd.DataFrame(data['skinsolver'], columns=['KS', 'Skin_Solver', 'KP', 'Produk'])
    else:
        st.error("Data not retrieved successfully. Check query or database connection.")
        return

    # Input user: Symptom selection with checkboxes and CF input
    st.subheader("Select Symptoms and Enter CF User Values")
    user_inputs = []
    for index, row in gejala_df.iterrows():
        gejala_name = row['Gejala']
        id_gejala = row['id_gejala']
        kg = row['KG']
        # selected = st.checkbox(f"{id_gejala}. Do you experience {gejala_name} ({kg})?", key=f'checkbox_{id_gejala}')
        st.markdown(f"<span class='checkbox-text'>{id_gejala}. Do you experience {gejala_name} ({kg})?</span>", unsafe_allow_html=True)
        selected = st.checkbox("", key=f'checkbox_{id_gejala}')
        if selected:
            cf_user = st.number_input(f"Enter CF User value for {gejala_name} ({kg}):", min_value=0.0, max_value=1.0, step=0.1, key=f'cf_user_{id_gejala}')
            user_inputs.append({'Gejala': gejala_name, 'CF User': cf_user, 'KG': kg})

    input_df = pd.DataFrame(user_inputs)

    if st.button("Submit"):
        # 1. Calculate CF for symptoms
        cf_gejala = {}
        calculations = []
        for index, row in input_df.iterrows():
            gejala = row['Gejala']
            cf_user = row['CF User']
            if cf_user is not None and gejala in gejala_df['Gejala'].values:
                cf_pakar = gejala_df[gejala_df['Gejala'] == gejala]['CF_Pakar'].values[0]
                cf_result = cf_user * cf_pakar
                cf_gejala[row['KG']] = cf_result
                calculations.append(f"CF({gejala}) = {cf_user} * {cf_pakar} = {cf_result:.2f}")
            else:
                calculations.append(f"No CF entered for {gejala} or not found in gejala_df.")

        st.subheader("CF Calculations for Symptoms")
        st.write(calculations)

        # 2. Evaluate rules based on the symptoms selected by the user
        evaluations = {}
        evaluation_details = []
        user_gejala_codes = set(input_df[input_df['CF User'].notnull()]['KG'].dropna().tolist())
        if user_gejala_codes:
            st.write("You have selected the following symptoms:")
            st.write(", ".join(user_gejala_codes))
        else:
            st.write("No symptoms selected.")
        for index, row in rule_df.iterrows():
            rule = row['Aturan']
            and_conditions = row['AND'].split(',') if row['AND'] else []
            or_conditions = row['OR'].split(',') if row['OR'] else []
            all_and_met = all(cond.strip() in user_gejala_codes for cond in and_conditions)
            any_or_met = any(cond.strip() in user_gejala_codes for cond in or_conditions)
            detail = f"Rule: {rule}, AND Conditions: {and_conditions}, OR Conditions: {or_conditions}, All AND met: {all_and_met}, Any OR met: {any_or_met}, Result: {'YES' if all_and_met and any_or_met else 'NO'}"
            evaluation_details.append(detail)
            evaluations[rule] = "YES" if all_and_met and any_or_met else "NO"

        st.subheader("Rule Evaluations")
        st.write(evaluation_details)

        # 3. Calculate the combined confidence factors for products based on rules
        cf_kombinasi = defaultdict(float)
        combined_calculations = []
        for index, row in rule_df.iterrows():
            rule = row['Aturan']
            and_conditions = row['AND'].split(',') if row['AND'] else []
            or_conditions = row['OR'].split(',') if row['OR'] else []
            all_and_met = all(cond.strip() in user_gejala_codes for cond in and_conditions)
            any_or_met = any(cond.strip() in user_gejala_codes for cond in or_conditions)
            if all_and_met and any_or_met:
                produk = re.findall(r'P\d+', rule)
                if produk:
                    produk = produk[0]
                    kg_for_comb = [cond.strip() for cond in and_conditions if cond.strip() in user_gejala_codes] + [cond.strip() for cond in or_conditions if cond.strip() in user_gejala_codes]
                    if len(kg_for_comb) < 2:
                        continue
                    cf_comb = 0.0
                    cf_user_1 = input_df[input_df['KG'] == kg_for_comb[0]]['CF User'].iloc[0]
                    cf_pakar_1 = gejala_df[gejala_df['KG'] == kg_for_comb[0]]['CF_Pakar'].iloc[0]
                    cf_user_2 = input_df[input_df['KG'] == kg_for_comb[1]]['CF User'].iloc[0]
                    cf_pakar_2 = gejala_df[gejala_df['KG'] == kg_for_comb[1]]['CF_Pakar'].iloc[0]
                    cf_kg1 = cf_user_1 * cf_pakar_1
                    cf_kg2 = cf_user_2 * cf_pakar_2
                    cf_comb = cf_kg1 + cf_kg2 * (1 - cf_kg1)
                    combined_calculations.append(f"Step 1: CF({kg_for_comb[0]}) = {cf_kg1:.4f}, CF({kg_for_comb[1]}) = {cf_kg2:.4f}, Combined CF = {cf_comb:.4f}")
                    for kg in kg_for_comb[2:]:
                        cf_user = input_df[input_df['KG'] == kg]['CF User'].iloc[0]
                        cf_pakar = gejala_df[gejala_df['KG'] == kg]['CF_Pakar'].iloc[0]
                        cf_kg = cf_user * cf_pakar
                        cf_comb = cf_comb + cf_kg * (1 - cf_comb)
                        combined_calculations.append(f"Updated CF with {kg}: CF({kg}) = {cf_kg:.4f}, New Combined CF = {cf_comb:.4f}")
                    cf_kombinasi[produk] = cf_comb

        st.subheader("Combined CF for Products")
        st.write(combined_calculations)

        # Initialize lists to collect recommendations
        produk_rekomendasi = []
        skin_solvers = []

        selected_kp = cf_kombinasi.keys()
        filtered_skinsolver_df = skinsolver_df[skinsolver_df['KP'].isin(selected_kp)]
        if not filtered_skinsolver_df.empty:
            st.subheader("Product Recommendations")
            for index, row in filtered_skinsolver_df.iterrows():
                st.markdown(f"<div class='product-name'>Product: {row['Produk']}, Skin Solver: {row['Skin_Solver']}, Recommendation: {row['KP']}</div>", unsafe_allow_html=True)
                produk_rekomendasi.append(row['Produk'])
                skin_solvers.append(row['Skin_Solver'])
        else:
            st.write("No product recommendations available based on your symptoms.")

        # Save to history after generating recommendations
        if 'username' in st.session_state and st.session_state['logged_in']:
            username = st.session_state['username']
            if produk_rekomendasi:
                save_to_history(username, user_gejala_codes, produk_rekomendasi, skin_solvers)
                st.markdown("<div style='color: #9C27B0; background-color: #F8BBD0; padding: 10px; border-radius: 5px; font-size: 16px;'>Your recommendations have been saved to your history.</div>", unsafe_allow_html=True)

            else:
                st.markdown("<div style='color: #9C27B0; background-color: #F8BBD0; padding: 10px; border-radius: 5px; font-size: 16px;'>No recommendations to save.</div>", unsafe_allow_html=True)
        else:
            st.write("")
            st.markdown("<div style='color: #9C27B0; background-color: #F8BBD0; padding: 10px; border-radius: 5px; font-size: 16px;'>You need to be logged in to save your recommendations.</div>", unsafe_allow_html=True)
