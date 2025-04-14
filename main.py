import streamlit as st

st.set_page_config(page_title="Keyword Value Calculator", layout="centered")

st.markdown("""
    <style>
        .stTextInput>div>div>input,
        .stNumberInput>div>div>input {
            border-radius: 0.5rem;
        }
        .stButton>button {
            background-color: #24554F;
            color: white;
            border-radius: 0.5rem;
            padding: 0.5rem 1.5rem;
            border: none;
        }
        .stButton>button:hover {
            background-color: #1E4742;
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 800px;
            margin: 0 auto;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("## 📩 Input Your Keyword Data")

with st.container():
    with st.form("keyword_form"):
        st.markdown("### 🔍 Keyword Details")
        keyword = st.text_input("Keyword", key="kw")

        col1, col2 = st.columns(2)
        with col1:
            current_position = st.number_input("Current Keyword Position", min_value=1, max_value=100, value=5, key="cp")
        with col2:
            target_position = st.number_input("Target Keyword Position", min_value=1, max_value=100, value=1, key="tp")

        keyword_volume = st.number_input("Current Keyword Volume", min_value=0, value=100, step=10, key="vol")

        st.markdown("### 💰 Conversion & Revenue Estimates")
        col3, col4 = st.columns(2)
        with col3:
            conversion_rate = st.number_input("Estimated Conversion Rate (%)", min_value=0.0, max_value=100.0, value=25.0, step=0.1, key="cr")
        with col4:
            close_rate = st.number_input("Estimated Close Rate (%)", min_value=0.0, max_value=100.0, value=50.0, step=0.1, key="clr")

        aov = st.number_input("Average Order Value ($)", min_value=0.0, value=100.0, step=10.0, key="aov")

        submitted = st.form_submit_button("Calculate")

        if submitted:
            st.success("✅ Calculation completed! (Functionality to be added)")
