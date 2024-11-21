import streamlit as st
import pymysql
from conn import create_connection
from theme import apply_custom_theme

# Apply custom theme for background and styles
apply_custom_theme()

# Function to fetch user data from the database
def get_user_data(username):
    connection = create_connection()
    
    if connection:
        try:
            with connection.cursor() as cursor:
                select_query = """
                SELECT username, password, gender, age, skin_type, skin_concern
                FROM users
                WHERE username = %s
                """
                cursor.execute(select_query, (username,))
                result = cursor.fetchone()

                if result:
                    return {
                        "username": result[0],
                        "password": result[1],
                        "gender": result[2],
                        "age": result[3],
                        "skin_type": result[4],
                        "skin_concern": result[5]
                    }
                else:
                    st.error("User  not found.")
                    return None
        except pymysql.MySQLError as e:
            st.error(f"An error occurred while fetching data: {e}")
            return None
        finally:
            connection.close()
    else:
        st.markdown("<div style='color: #9C27B0; background-color: #F8BBD0; padding: 10px; border-radius: 5px; font-size: 16px;'>Failed to connect to the database.</div>", unsafe_allow_html=True)
        return None

# Function to render the form and handle registration or update
def render_add_form(username=None, password=None, gender=None, age=None, skin_type=None, skin_concern=None):
    # Initialize session state for inputs if not already initialized
    if 'username_input' not in st.session_state:
        st.session_state['username_input'] = username if username else ""
    if 'password_input' not in st.session_state:
        st.session_state['password_input'] = password if password else ""
    if 'gender_input' not in st.session_state:
        st.session_state['gender_input'] = gender if gender else "Male"
    if 'age_input' not in st.session_state:
        st.session_state['age_input'] = age if age else 25
    if 'skin_type_input' not in st.session_state:
        st.session_state['skin_type_input'] = skin_type if skin_type else "Oily"
    if 'skin_concern_input' not in st.session_state:
        st.session_state['skin_concern_input'] = skin_concern if skin_concern else ""

    # Input fields
    
    with st.form(key='user_form', clear_on_submit=False):
        st.markdown(
        """
        <style>
        label {
            color: #3F2C68 !important;
            font-weight: bold; /* Opsional: Membuat label tebal */
        }
        </style>
        """,
        unsafe_allow_html=True,
        )
    
        username_input = st.text_input("Username", value=st.session_state['username_input'])
        password_input = st.text_input("Password", type="password", value=st.session_state['password_input'])
        gender_input = st.selectbox("Gender", options=["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(st.session_state['gender_input']))
        age_input = st.number_input("Age", min_value=0, max_value=120, value=st.session_state['age_input'])
        skin_type_input = st.selectbox("Skin Type", options=["Oily", "Dry", "Combination", "Sensitive"], index=["Oily", "Dry", "Combination", "Sensitive"].index(st.session_state['skin_type_input']))
        skin_concern_input = st.text_area("Skin Concern", value=st.session_state['skin_concern_input'])

        # Button to trigger form submission
        submit_button = st.form_submit_button("Submit")

        if submit_button:
            # Update session state with new values from input fields
            st.session_state['username_input'] = username_input
            st.session_state['password_input'] = password_input
            st.session_state['gender_input'] = gender_input
            st.session_state['age_input'] = age_input
            st.session_state['skin_type_input'] = skin_type_input
            st.session_state['skin_concern_input'] = skin_concern_input

            # Validate all fields are filled
            if username_input and password_input and gender_input and age_input and skin_type_input and skin_concern_input:
                # Insert into or update database
                connection = create_connection()
                try:
                    if connection:
                        with connection.cursor() as cursor:
                            if username:  # If username exists, update the user
                                cursor.execute("""
                                    UPDATE users 
                                    SET password=%s, gender=%s, age=%s, skin_type=%s, skin_concern=%s 
                                    WHERE username=%s
                                """, (password_input, gender_input, age_input, skin_type_input, skin_concern_input, username_input))
                            else:  # Otherwise, insert new user
                                cursor.execute("""
                                    INSERT INTO users (username, password, gender, age, skin_type, skin_concern) 
                                    VALUES (%s, %s, %s, %s, %s, %s)
                                """, (username_input, password_input, gender_input, age_input, skin_type_input, skin_concern_input))
                            connection.commit()
                            st.success("User  data saved successfully!")
                except pymysql.MySQLError as e:
                    st.error(f"An error occurred while saving data: {e}")
                finally:
                    connection.close()
            else:
                st.markdown("<div style='color: #9C27B0; background-color: #F8BBD0; padding: 10px; border-radius: 5px; font-size: 16px;'>Please fill in all fields.</div>", unsafe_allow_html=True)

# Main application logic
def view_user_data_page():
    st.markdown("<h1 style='text-align: center;'>USER DATA</h1>", unsafe_allow_html=True)

    # Periksa apakah pengguna sudah login
    if 'username' in st.session_state and st.session_state.get('logged_in', False):
        username = st.session_state['username']
        user_data = get_user_data(username)

        if user_data:
            # Tampilkan profil pengguna
            st.title("User Profile")
            st.write(f"**Username       :** {user_data['username']}")
            st.write(f"**Gender         :** {user_data['gender']}")
            st.write(f"**Age            :** {user_data['age']}")
            st.write(f"**Skin Type      :** {user_data['skin_type']}")
            st.write(f"**Skin Concern   :** {user_data['skin_concern']}")

        # Inisialisasi session state untuk kontrol tombol
        if "action" not in st.session_state:
            st.session_state.action = None

        # Tombol Update
        if st.button("Update"):
            st.session_state.action = "update"

        # Tombol Add hanya untuk admin
        if username == "admin":
            if st.button("Add"):
                st.session_state.action = "add"

        # Tampilkan form berdasarkan aksi tombol
        if st.session_state.action == "update":
            st.title("Update User Data")
            if user_data:
                render_add_form(**user_data)
            else:
                st.markdown("<div style='color: #9C27B0; background-color: #F8BBD0; padding: 10px; border-radius: 5px; font-size: 16px;'>User data not found. Please add a new user.</div>", unsafe_allow_html=True)
                

        elif st.session_state.action == "add":
            st.markdown(
            """
            <style>
            label {
                color: #3F2C68 !important;
                font-weight: bold; /* Opsional: Membuat label tebal */
            }
            </style>
            """,
            unsafe_allow_html=True,
            )
            
            st.title("Add New User")
            username_input = st.text_input("Enter username for new user")
            if username_input:
                user_data = get_user_data(username_input)
                if user_data:
                    render_add_form(**user_data)
                else:
                    render_add_form()

    else:
        st.markdown("<div style='color: #9C27B0; background-color: #F8BBD0; padding: 10px; border-radius: 5px; font-size: 16px;'>Please log in first.</div>", unsafe_allow_html=True)


if __name__ == "__view_user_data_page__":
    view_user_data_page()