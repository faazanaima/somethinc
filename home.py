import streamlit as st
import pymysql
from conn import create_connection
from theme import apply_custom_theme

# Apply custom theme for background and styles
apply_custom_theme()

# Function to register a user
def register_user(username, password):
    connection = create_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
                connection.commit()
                st.markdown("<div style='color: #ffffff; background-color: #77f059; padding: 10px; border-radius: 5px; font-size: 14px;'>Registration successful!</div>", unsafe_allow_html=True)
        except pymysql.MySQLError as e:
            st.error("An error occurred: " + str(e))
        finally:
            connection.close()

# Function to check user credentials
def check_user(username, password):
    connection = create_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
                user = cursor.fetchone()
                
                if user and user[2] == password:  # Validate password
                    return True
        except pymysql.MySQLError as e:
            st.error("An error occurred: " + str(e))
        finally:
            connection.close()
    
    return False  # Indicates login failure

# Display registration form
def show_register():
    st.title("Register")
    
    st.markdown("""
        <style>
            div.stTextInput > label {
                color: #3F2C68;
            }
            div.stPasswordInput > label {
                color: #3F2C68;
            }
        </style>
    """, unsafe_allow_html=True)
        
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')

    if st.button("Register"):
        if username and password:
            register_user(username, password)
        else:
            st.markdown("<div style='color: #9C27B0; background-color: #F8BBD0; padding: 10px; border-radius: 5px; font-size: 12px;'>Please fill in both fields.</div>", unsafe_allow_html=True)

# Display login form
def show_login():
    st.title("Login")
    
    # Apply custom CSS directly to the input labels
    st.markdown("""
        <style>
            div.stTextInput > label {
                color: #3F2C68;
            }
            div.stPasswordInput > label {
                color: #3F2C68;
            }
        </style>
    """, unsafe_allow_html=True)
    
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')

    if st.button("Login"):
        if check_user(username, password):
            st.markdown("<div style='color: #ffffff; background-color: #77f059; padding: 10px; border-radius: 5px; font-size: 14px;'>Login successful!</div>", unsafe_allow_html=True)
            st.session_state['username'] = username
            st.session_state['logged_in'] = True  # Set login status
            return
        else:
            st.markdown("<div style='color: #9C27B0; background-color: #F8BBD0; padding: 10px; border-radius: 5px; font-size: 12px;'>Invalid username or password.</div>", unsafe_allow_html=True)

# Display home page content
def show_home():
    # Display image on the left and text on the right using flexbox layout
    st.markdown(
        """
        <style>
            .stImage {
                padding-top: 0 !important; /* Remove any padding at the top of the image */
            }
            .content-container {
                margin-top: -60px; /* Adjust the space for text, closer to the image */
            }
            .content-container {
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .image-container {
                flex: 1;
                margin-right: 20px;  /* Adjust the space between image and text */
            }
            .text-container {
                flex: 2;
                text-align: left;
            }
        </style>
        """, unsafe_allow_html=True)

    # Create a container with image on the left and text on the right
    st.markdown('<div class="content-container">', unsafe_allow_html=True)
    
    # Left side image
    st.markdown('<div class="image-container">', unsafe_allow_html=True)
    st.image(r"C:\proyek\somethinc\foto\brand_ambassador.jpg", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Right side text
    st.markdown('<div class="text-container">', unsafe_allow_html=True)
    st.markdown(
    """
    <h1>Discover Your Perfect Somethinc Product!</h1>
    <p style="color: #3F2C68;">
    Welcome to the <strong>Somethinc Product Recommendation Expert System</strong>, your personal skincare advisor! 🌟
    </p>
    <p style="color: #3F2C68;">
        Whether you're new to skincare or a seasoned beauty enthusiast, finding the right product can be overwhelming. That's where we come in!
        Our expert system helps you diagnose your skin needs and suggests the <strong>perfect Somethinc products</strong> tailored just for you.
        From tackling skin concerns to boosting radiance, we provide personalized recommendations to help you achieve glowing, healthy skin. ✨
    </p>
    <p style="color: #3F2C68;">
        Let's get started on your journey to radiant skin – just tell us a bit about your skin type, concerns, and goals, and we'll do the rest!
    </p>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Display username in the sidebar if logged in
    if 'username' in st.session_state:
        st.sidebar.markdown(
    f"<div style='color: white;'>Hai, {st.session_state['username']}</div>", 
    unsafe_allow_html=True
    )

# Function to log out the user
def logout():
    st.session_state['logged_in'] = False  # Reset login status
    st.session_state.pop('username', None)  # Remove username from session state
    st.markdown("<div style='color: #ffffff; background-color: #77f059; padding: 10px; border-radius: 5px; font-size: 14px;'>Logout successful!</div>", unsafe_allow_html=True)

# Main application function
def main_app():
    st.sidebar.markdown("## Navigation")
    
    # Check user login status
    if st.session_state.get('logged_in', False):
        if st.sidebar.button("Logout"):
            logout()  # Call logout function
        show_home()  # Only show home when logged in
    else:
        # Use a unique key for the radio button by incorporating the session state
        choice = st.sidebar.radio("Go to", ["Home", "Login", "Register"], key="nav_choice_home")

        if choice == "Home":
            show_home()
        elif choice == "Login":
            show_login()
        elif choice == "Register":
            show_register()

# Run the main app
if __name__ == "__main__":
    main_app()
