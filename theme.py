import streamlit as st

def apply_custom_theme():
    st.markdown("""
        <style>
            :root {
                --blue: #007bff;
                --indigo: #6610f2;
                --purple: #6f42c1;
                --pink: #e83e8c;
                --red: #dc3545;
                --orange: #fd7e14;
                --yellow: #ffc107;
                --green: #27ae60;
                --teal: #20c997;
                --cyan: #17a2b8;
                --white: #fff;
                --gray: #4f4f4f;
                --gray-dark: #343a40;
                --primary: #007bff;
                --secondary: #6c757d;
                --success: #27ae60;
                --info: #17a2b8;
                --warning: #ffc107;
                --danger: #dc3545;
                --light: #f8f9fa;
                --dark: #343a40;
                --lilac-p: #BB6BD9;
                --lilac-b: #9B57F6;
                --lilac-bg: #EDE6FD;
                --blue-purple: #3F2C68;
                --navigation-bg: #D4C6F5;  /* Custom background color for sidebar */
                --navigation-text: #4A2C8C; /* Custom color for navigation text */
                --navigation-text-hover: #3F2C68; /* Custom hover color for navigation text */
                --breakpoint-xs: 0;
                --breakpoint-sm: 576px;
                --breakpoint-md: 768px;
                --breakpoint-lg: 992px;
                --breakpoint-xl: 1200px;
                --breakpoint-xxl: 1440px;
                --font-family-sans-serif: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
                --font-family-monospace: SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
            }

            /* Apply background and text styles using the custom colors */
            body, .stApp {
                background-color: var(--lilac-bg);
                color: var(--gray-dark);  /* Dark text for better readability */
                font-family: var(--font-family-sans-serif);
            }

            /* Customize sidebar (navigation) background */
            .css-1d391kg {
                background-color: var(--navigation-bg);
            }

            /* Sidebar item styles */
            .css-1v3fvcr {
                background-color: var(--navigation-bg);
                color: var(--navigation-text);
            }

            .css-1v3fvcr:hover {
                background-color: var(--navigation-text);
                color: var(--navigation-text-hover);
            }

            /* Sidebar item active styles */
            .css-1v3fvcr.st-dgQqaK {
                background-color: var(--navigation-text);
                color: var(--navigation-text-hover);
            }

            /* Sidebar title styles */
            .css-1v3fvcr .stSidebar .stSelectbox {
                color: var(--navigation-text);
            }

            /* Button styles */
            .stButton>button {
                background-color: var(--lilac-p);
                color: var(--white);
                border: 1px solid var(--lilac-b);
                border-radius: 8px;
            }
            .stButton>button:hover {
                background-color: var(--lilac-b);
                color: var(--white);
            }

            /* Header and text colors */
            h1, h2, h3, h4, h5, h6 {
                color: var(--blue-purple);  /* Darker header color for visibility */
            }
            
            /* Header and text colors */
            h2 {
                color: white;  /* Darker header color for visibility */
            }

            /* Links and interactive elements */
            a {
                color: var(--primary);
            }
            a:hover {
                color: var(--blue-purple);
            }

        </style>
    """, unsafe_allow_html=True)

# Call this function at the start of your app
apply_custom_theme()
