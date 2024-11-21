import streamlit as st
from home import show_home, main_app
from produk import show_produk
from gejala import show_gejala
from rule import display_rules
from skinsolver import show_skinsolver
from recommendation import main_process
from history import show_history
from theme import apply_custom_theme
from users import view_user_data_page
from theme import apply_custom_theme

# Apply custom theme for background and styles
apply_custom_theme()

# Display username in the sidebar if logged in
if 'username' in st.session_state:
        st.sidebar.markdown(
    f"<div style='color: white;'>Hai, {st.session_state['username']}</div>", 
    unsafe_allow_html=True
    )

# Sidebar for page navigation
st.sidebar.markdown("## Navigation")

# Options for the page selection dropdown for all users
page_options = ["Home", "Product", "Symptoms", "Rules", "Skin Solver", "Recommendation", "History", "User Data"]

# Display dropdown for page selection
page = st.sidebar.selectbox("Choose a page", page_options)

# Display selected page
if page == "Home":
    main_app()  # Call the main app function
elif page == "Product":
    show_produk()
elif page == "Symptoms":
    input_df = show_gejala()
    if input_df is not None:
        st.write(input_df)  # Display user inputs
elif page == "Rules":
    display_rules()
elif page == "Skin Solver":
    show_skinsolver()
elif page == "Recommendation":
    main_process()
elif page == "History":
    show_history()
elif page == "User Data":
    view_user_data_page()